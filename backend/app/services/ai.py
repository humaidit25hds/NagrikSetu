import os
from typing import List, Optional, Dict, Any
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.chat import ChatResponse, ChatMessage, UserDemographics, SchemeCard, SourceDocument

load_dotenv()

# Load API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-3.6-flash")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


SYSTEM_PROMPT = """
You are NagrikSetu, an AI assistant that helps Indian citizens understand
government services, schemes, applications, eligibility requirements,
documents, and application procedures.

Your responsibilities:
1. Give simple and easy-to-understand answers in the citizen's language.
2. Help users understand government services and schemes.
3. Explain eligibility requirements clearly.
4. Tell users what documents may be required.
5. Explain application procedures step-by-step.
6. If you are not sure about something, clearly say that you are not sure.
7. Never invent government rules, benefits, deadlines, or documents.
8. Ask a clarification question when the user's request is unclear.
9. Prefer concise answers suitable for ordinary citizens.
10. Do not provide legal, financial, or medical advice as a substitute
    for a qualified professional.

Answer in the same language as the user whenever possible (English, Hindi, or Hinglish).
"""


class AIService:
    """
    AI-powered service for generating civic assistant responses.
    Integrates with OpenAI API and RAG/Eligibility services.
    """

    def __init__(self, rag_service=None, eligibility_service=None):
        self.rag_service = rag_service
        self.eligibility_service = eligibility_service
        self.client = client

    async def generate_chat_response(
        self,
        message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        user_profile: Optional[UserDemographics] = None,
        language: str = "en"
    ) -> ChatResponse:
        """
        Generate a complete chat response including AI response, recommended schemes, and sources.
        
        Args:
            message: User's query
            conversation_history: Previous messages in the conversation
            user_profile: User demographic information for eligibility matching
            language: Preferred response language
            
        Returns:
            ChatResponse with AI answer, schemes, and metadata
        """
        
        if not message or not message.strip():
            return ChatResponse(
                response="Please enter your question about Indian government schemes or services.",
                language=language,
                recommended_schemes=[],
                source_documents=[],
                suggested_followups=[]
            )

        # Retrieve relevant scheme information via RAG
        rag_context = ""
        recommended_schemes: List[SchemeCard] = []
        source_documents: List[SourceDocument] = []
        
        if self.rag_service:
            try:
                rag_result = self.rag_service.retrieve_relevant_schemes(
                    query=message,
                    limit=3
                )
                recommended_schemes = rag_result.get("schemes", [])
                source_documents = rag_result.get("sources", [])
                rag_context = rag_result.get("context", "")
            except Exception as e:
                print(f"RAG retrieval error: {e}")

        # Generate AI response using OpenAI
        ai_response = await self._generate_ai_text(
            user_message=message,
            context=rag_context,
            language=language
        )

        # Get eligibility-based scheme suggestions if user profile provided
        if user_profile and self.eligibility_service:
            try:
                eligibility_schemes = self.eligibility_service.get_eligible_schemes(
                    user_profile=user_profile
                )
                recommended_schemes.extend(eligibility_schemes[:2])
            except Exception as e:
                print(f"Eligibility service error: {e}")

        # Generate follow-up suggestions
        suggested_followups = self._generate_followups(message, language)

        return ChatResponse(
            response=ai_response,
            language=language,
            recommended_schemes=recommended_schemes[:3],
            source_documents=source_documents[:3],
            suggested_followups=suggested_followups,
            metadata={
                "model": "gpt-4o-mini",
                "query_type": self._detect_query_type(message),
                "user_language": language
            }
        )

    async def _generate_ai_text(
        self,
        user_message: str,
        context: str = "",
        language: str = "en"
    ) -> str:
        """Generate AI text response using OpenAI API."""
        
        if GEMINI_API_KEY:
            return await self._generate_gemini_text(
                user_message=user_message,
                context=context,
                language=language,
            )

        if not self.client:
            return (
                "AI service is not configured. Please set GEMINI_API_KEY or OPENAI_API_KEY in environment."
            )

        if not user_message or not user_message.strip():
            return "Please enter your question."

        context_text = ""
        if context and context.strip():
            context_text = f"""
Use the following information as supporting context:

{context}

---
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"""{context_text}
Citizen's question (preferred language: {language}):
{user_message}
"""
                    }
                ],
                temperature=0.2,
                max_tokens=800
            )

            answer = response.choices[0].message.content

            if not answer:
                return "Sorry, I could not generate a response."

            return answer.strip()

        except Exception as e:
            print(f"AI service error: {e}")
            return (
                "Sorry, I am unable to process your request right now. "
                "Please try again later."
            )

    async def _generate_gemini_text(
        self,
        user_message: str,
        context: str = "",
        language: str = "en",
    ) -> str:
        """Generate a response using Google Gemini's REST API."""
        context_text = f"\nSupporting scheme information:\n{context}\n" if context.strip() else ""
        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{DEFAULT_MODEL}:generateContent?key={GEMINI_API_KEY}"
        )
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{
                "parts": [{
                    "text": f"{context_text}\nCitizen question (preferred language: {language}):\n{user_message}"
                }]
            }],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 800},
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                response = await http_client.post(endpoint, json=payload)
                response.raise_for_status()
                data = response.json()
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            return answer.strip() or "Sorry, I could not generate a response."
        except Exception as error:
            print(f"Gemini service error: {type(error).__name__}")
            return "Sorry, I am unable to process your request right now. Please try again later."

    def _detect_query_type(self, message: str) -> str:
        """Detect the type of query from the message."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["eligible", "qualify", "meet", "criteria"]):
            return "eligibility_check"
        elif any(word in message_lower for word in ["documents", "required", "papers"]):
            return "document_inquiry"
        elif any(word in message_lower for word in ["apply", "application", "submit"]):
            return "application_help"
        else:
            return "general_inquiry"

    def _generate_followups(self, message: str, language: str) -> List[str]:
        """Generate suggested follow-up questions."""
        query_type = self._detect_query_type(message)
        
        followups = {
            "eligibility_check": [
                "What documents do I need to apply?" if language == "en" else "मुझे आवेदन के लिए कौन से दस्तावेज़ चाहिए?",
                "How do I apply for this scheme?" if language == "en" else "मैं इस योजना के लिए आवेदन कैसे करूं?",
                "What are the benefits?" if language == "en" else "लाभ क्या हैं?"
            ],
            "document_inquiry": [
                "What is the application process?" if language == "en" else "आवेदन प्रक्रिया क्या है?",
                "Am I eligible for this scheme?" if language == "en" else "क्या मैं इस योजना के लिए पात्र हूं?",
                "When will I get a decision?" if language == "en" else "मुझे निर्णय कब मिलेगा?"
            ],
            "application_help": [
                "What are the eligibility criteria?" if language == "en" else "पात्रता मानदंड क्या हैं?",
                "Which documents are required?" if language == "en" else "कौन से दस्तावेज़ आवश्यक हैं?",
                "How do I track my application?" if language == "en" else "मैं अपने आवेदन को कैसे ट्रैक करूं?"
            ],
            "general_inquiry": [
                "What other schemes are available?" if language == "en" else "अन्य कौन सी योजनाएं उपलब्ध हैं?",
                "Who is eligible?" if language == "en" else "कौन पात्र है?",
                "How do I apply?" if language == "en" else "मैं कैसे आवेदन करूं?"
            ]
        }
        
        return followups.get(query_type, followups["general_inquiry"])
