# NagrikSetu Backend - File Architecture & Connections Guide

## Overview
NagrikSetu is an AI-powered civic assistant connecting Indian citizens with government schemes. The backend uses FastAPI, SQLAlchemy ORM, and OpenAI integration.

## Directory Structure & File Connections

```
backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration & environment settings
│   ├── database.py              # Database setup & session management
│   │
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py              # User/Citizen entity
│   │   ├── service.py           # Government Scheme entity
│   │   └── application.py       # Scheme Application entity
│   │
│   ├── routers/                 # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── chat.py              # Chatbot & eligibility endpoints
│   │   ├── services.py          # Scheme search & list endpoints
│   │   └── applications.py      # Application submission & tracking
│   │
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── __init__.py
│   │   └── chat.py              # All schema definitions
│   │
│   └── services/                # Business logic layer
│       ├── __init__.py
│       ├── ai.py                # AI response generation (OpenAI integration)
│       ├── rag.py               # RAG - Scheme retrieval & matching
│       └── eligibility.py       # Eligibility evaluation logic
│
├── database/
│   └── init.sql                 # Database initialization script
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── .env                         # Local environment (git ignored)
└── nagriksetu.db               # SQLite database (auto-generated)
```

## File Connections Map

### Entry Point
- **main.py** orchestrates everything:
  - Imports `config.Settings` → gets API configuration
  - Imports `database` → initializes engine, session factory, Base ORM
  - Imports `models` → User, Service, Application
  - Imports `routers` → chat_router, services_router, applications_router
  - Imports `INDIAN_SCHEMES_KNOWLEDGE` from rag.py → seeds database

### Configuration Layer
```
config.py (Settings class & get_settings() function)
   ↓
   - Reads .env file for environment variables
   - Provides APP_NAME, API_V1_STR, OPENAI_API_KEY, DATABASE_URL, etc.
   - Used by: main.py, database.py, services/ai.py
```

### Data Layer
```
database.py (Database initialization)
   ↓
   - Creates engine from DATABASE_URL
   - Creates SessionLocal for session management
   - Provides get_db() dependency for FastAPI
   ↓
   - Used by all routers & services for DB access

models/
   ├── user.py (User model)
   │   - Fields: id, full_name, email, phone_number, demographics, etc.
   │   - Relationship: applications ←→ Application
   │
   ├── service.py (Service/Scheme model)
   │   - Fields: id, title, title_hi, benefits, eligibility_criteria, etc.
   │   - Relationship: applications ←→ Application
   │
   └── application.py (Application/Submission model)
       - Fields: id, tracking_number, status, documents_submitted, etc.
       - Relationships: user ←→ User, service ←→ Service
```

### Business Logic Layer (Services)
```
services/rag.py (RAG Service)
   ├── INDIAN_SCHEMES_KNOWLEDGE: Seed data with 10 major schemes
   └── RAGService class
       ├── search_schemes()           → Keyword search + demographic matching
       ├── build_rag_prompt_context() → Format schemes for LLM
       ├── extract_cards_and_sources()→ Convert to API response format
       └── retrieve_relevant_schemes()→ High-level API for AIService
           ↓
           Used by: services/ai.py, services/eligibility.py

services/eligibility.py (Eligibility Service)
   ├── check_eligibility() function  → Basic eligibility checker
   └── EligibilityService class
       ├── evaluate()                → Detailed eligibility assessment
       ├── get_eligible_schemes()    → Find schemes user qualifies for
       ├── _evaluate_criteria()      → Check age, income, state, etc.
       └── _generate_next_steps()    → Actionable guidance
           ↓
           Uses: RAGService (for scheme lookup)
           Used by: routers/chat.py, services/ai.py

services/ai.py (AI Service)
   ├── SYSTEM_PROMPT               → GPT instructions
   └── AIService class
       ├── generate_chat_response()  → Main API for chatbot
       ├── _generate_ai_text()       → Call OpenAI API
       ├── _detect_query_type()      → Categorize user queries
       └── _generate_followups()     → Suggest next questions
           ↓
           Uses: RAGService, EligibilityService
           Used by: routers/chat.py
```

### API Routers (HTTP Endpoints)
```
routers/chat.py
   ├── POST /api/v1/chat            → Main chatbot endpoint
   │   └── Uses: AIService, RAGService, get_db()
   │
   └── POST /api/v1/chat/eligibility → Eligibility check endpoint
       └── Uses: EligibilityService, get_db()

routers/services.py
   ├── GET /api/v1/services         → List/search schemes
   │   └── Uses: Service model, INDIAN_SCHEMES_KNOWLEDGE
   │
   └── Filters: category, department, level, state, search term
       └── Uses: get_db()

routers/applications.py
   ├── POST /api/v1/applications    → Submit scheme application
   │   └── Creates: User, Service (if needed), Application records
   │       Uses: get_db()
   │
   └── GET /api/v1/applications/track/{tracking_number}
       └── Queries: Application by tracking number
           Uses: get_db()
```

### Request/Response Schemas
```
schemas/chat.py contains all Pydantic models:
   
   Input Models:
   ├── ChatRequest     → message, conversation_history, user_profile, language
   ├── EligibilityCheckRequest → scheme_id/name, demographics
   └── ApplicationCreateRequest → service_id, applicant_info, documents

   Output Models:
   ├── ChatResponse    → response, schemes, sources, followups, metadata
   ├── EligibilityResult → status, criteria_met, required_docs, next_steps
   ├── ApplicationResponse → tracking_number, status, timeline
   └── ServiceResponse → id, title, benefits, eligibility, etc.

   Data Models:
   ├── UserDemographics → age, gender, income, occupation, category, etc.
   ├── SchemeCard       → Summarized scheme info for recommendations
   └── SourceDocument   → Citation with title, URL, snippet
```

## Data Flow Examples

### Example 1: User Asks About Eligibility
```
1. User sends: POST /api/v1/chat/eligibility
   {
     "scheme_id": 1,
     "demographics": {"age": 30, "occupation": "farmer", "state": "Maharashtra"}
   }

2. routers/chat.py:check_scheme_eligibility()
   ├── Creates EligibilityService(db)
   ├── Calls: eligibility_service.evaluate(scheme_id, demographics)
   │
   └─→ services/eligibility.py:EligibilityService.evaluate()
       ├── _get_scheme(1) → Looks up PM Kisan scheme
       ├── _evaluate_criteria() → Checks age, occupation, state
       ├── Computes match_score and status
       └── Returns: EligibilityResult (ELIGIBLE/LIKELY_ELIGIBLE/INELIGIBLE)

3. Response sent to client with criteria, documents, next steps
```

### Example 2: User Sends Chat Message
```
1. User sends: POST /api/v1/chat
   {
     "message": "I'm a farmer in Maharashtra. What schemes am I eligible for?"
   }

2. routers/chat.py:chat_with_assistant()
   ├── Creates RAGService(db)
   ├── Creates EligibilityService(db)
   ├── Creates AIService(rag_service, eligibility_service)
   │
   └─→ services/ai.py:AIService.generate_chat_response()
       ├── Calls: rag_service.retrieve_relevant_schemes(query)
       │   └─→ RAGService.search_schemes() 
       │       ├── Tokenizes "farmer" + "Maharashtra"
       │       ├── Scores INDIAN_SCHEMES_KNOWLEDGE schemes
       │       ├── Boosts PM Kisan (agriculture + farmer keywords)
       │       └── Returns: [PM Kisan, Mudra, etc.]
       │
       ├── Calls: ai_service._generate_ai_text(message, rag_context)
       │   └─→ Sends to OpenAI with SYSTEM_PROMPT + context
       │       Returns: Natural language response
       │
       ├── Calls: eligibility_service.get_eligible_schemes(demographics)
       │   └─→ Returns: SchemeCards for recommended schemes
       │
       └─→ Returns: ChatResponse (text + schemes + sources + followups)

3. Response sent with AI answer, recommended schemes, and document sources
```

### Example 3: User Submits Application
```
1. User sends: POST /api/v1/applications
   {
     "service_id": 1,
     "applicant_name": "Raj Kumar",
     "applicant_phone": "9876543210",
     "documents_submitted": ["Aadhaar", "Land Papers"]
   }

2. routers/applications.py:submit_application()
   ├── db.query(User).filter(phone=9876543210) 
   │   ├── If exists: Use existing user
   │   └── Else: Create new User record
   │
   ├── db.query(Service).filter(id=1)
   │   ├── If exists: Use existing service
   │   └── Else: Create stub Service from INDIAN_SCHEMES_KNOWLEDGE
   │
   ├── Generate unique tracking_number (NS-2026-XXXXX)
   │
   ├── db.add(Application(...)) 
   │   └── Save with status="SUBMITTED"
   │
   └─→ Returns: ApplicationResponse with tracking_number

3. Client gets tracking number for later status checks
```

## Dependencies & Imports Summary

```
External Libraries:
├── FastAPI         → Web framework (routers, dependencies)
├── SQLAlchemy      → ORM (models, database)
├── Pydantic        → Schema validation (schemas)
├── OpenAI          → LLM API (services/ai.py)
├── python-dotenv   → Environment loading (config.py)
└── Starlette       → CORS middleware (main.py)

Internal Imports:
├── config.py       → Used by main.py, database.py, services/ai.py
├── database.py     → Used by all routers and services
├── models/*        → Used by routers (queries) and services (logic)
├── schemas/chat.py → Used by routers (request/response) and services
├── services/*      → Used by routers (business logic)
└── INDIAN_SCHEMES_KNOWLEDGE → Seed data for all modules
```

## Setup Instructions

1. **Install dependencies:**
   ```bash
   cd backend
   python -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY
   ```

3. **Run application:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Key Design Patterns

1. **Dependency Injection:** FastAPI's `Depends(get_db)` injects database sessions
2. **Service Layer:** Business logic isolated in `services/` modules
3. **Pydantic Schemas:** Automatic request validation and response serialization
4. **RAG Pattern:** Knowledge base search + LLM context enrichment
5. **Database Seeding:** INDIAN_SCHEMES_KNOWLEDGE bootstraps initial data
6. **Error Handling:** HTTP exceptions with status codes in routers

## Testing Endpoints

```bash
# Chat endpoint
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What farming schemes exist?"}'

# List services
curl http://localhost:8000/api/v1/services?category=Agriculture

# Check eligibility
curl -X POST http://localhost:8000/api/v1/chat/eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": 1,
    "demographics": {"age": 30, "occupation": "farmer"}
  }'

# Submit application
curl -X POST http://localhost:8000/api/v1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": 1,
    "applicant_name": "John Doe",
    "applicant_phone": "9999999999"
  }'
```
