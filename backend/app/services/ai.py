import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are Citizen-AI, an AI assistant that helps citizens understand
government services, schemes, applications, eligibility requirements,
documents, and application procedures.

Your responsibilities:
1. Give simple and easy-to-understand answers.
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

Answer in the same language as the user whenever possible.
"""


async def generate_ai_response(
    user_message: str,
    context: str = ""
) -> str:
    """
    Generate an AI response for a citizen's question.

    Args:
        user_message: Question/message from the citizen.
        context: Optional information retrieved by RAG.

    Returns:
        AI-generated response as a string.
    """

    if not user_message or not user_message.strip():
        return "Please enter your question."

    # Add RAG information if available
    context_text = ""

    if context and context.strip():
        context_text = f"""
Use the following information as supporting context.
Do not contradict this information.

--- Retrieved Information ---
{context}
--- End Retrieved Information ---
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
{context_text}

Citizen's question:
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
