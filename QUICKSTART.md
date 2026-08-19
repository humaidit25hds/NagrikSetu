# NagrikSetu - Quick Start Guide

## ✅ Connection Status

All files in the backend have been properly connected:

### ✓ Package Structure
- [x] `__init__.py` files created for all packages (models, routers, schemas, services)
- [x] Proper import statements in each module
- [x] Package exports defined in `__init__.py`

### ✓ Configuration
- [x] `config.py` contains all required settings
- [x] `get_settings()` function implemented
- [x] Environment variables properly loaded from `.env`
- [x] `.env.example` template created

### ✓ Database Layer
- [x] `database.py` creates SQLAlchemy engine and session
- [x] All models (User, Service, Application) defined
- [x] Relationships properly configured
- [x] `get_db()` dependency injection ready

### ✓ Services Layer
- [x] **AIService** (ai.py)
  - Integrates with OpenAI API
  - Uses RAGService for context
  - Uses EligibilityService for recommendations
  - Generates responses with suggested follow-ups

- [x] **RAGService** (rag.py)
  - Searches 10+ Indian government schemes
  - Demographic-based relevance scoring
  - Formats schemes for LLM consumption
  - Extracts citations and source documents

- [x] **EligibilityService** (eligibility.py)
  - Evaluates user eligibility
  - Checks age, income, state, occupation, category
  - Generates match score and status (ELIGIBLE/LIKELY_ELIGIBLE/INELIGIBLE)
  - Provides actionable next steps

### ✓ API Routers
- [x] **chat.py**
  - POST /api/v1/chat (Chatbot interaction)
  - POST /api/v1/chat/eligibility (Eligibility check)
  - Integrates all services

- [x] **services.py**
  - GET /api/v1/services (List and search schemes)
  - Filters by category, department, state, level
  - Keyword search support

- [x] **applications.py**
  - POST /api/v1/applications (Submit application)
  - GET /api/v1/applications/track/{tracking_number} (Track status)
  - Generates unique tracking numbers

### ✓ Schemas
- [x] All request/response models defined
- [x] Validation logic in Pydantic models
- [x] Config class for ORM serialization

### ✓ Dependencies
- [x] `requirements.txt` populated with all needed packages
- [x] FastAPI, SQLAlchemy, Pydantic, OpenAI all included

## 🚀 Setup & Run

### 1. Install Dependencies
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

### 3. Run the Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📋 Test the API

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am a farmer in Punjab. What government schemes are available for me?",
    "language": "en"
  }'
```

### Test Eligibility Check
```bash
curl -X POST http://localhost:8000/api/v1/chat/eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": 1,
    "demographics": {
      "age": 35,
      "gender": "male",
      "occupation": "farmer",
      "state": "Punjab",
      "annual_income": 200000,
      "category": "General"
    }
  }'
```

### Test List Services
```bash
curl "http://localhost:8000/api/v1/services?category=Agriculture&state=Punjab"
```

### Test Application Submission
```bash
curl -X POST http://localhost:8000/api/v1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": 1,
    "applicant_name": "Raj Kumar Singh",
    "applicant_phone": "9876543210",
    "applicant_email": "raj@example.com",
    "applicant_aadhaar_last4": "1234",
    "documents_submitted": ["Aadhaar Card", "Land Papers", "Bank Passbook"],
    "user_demographics": {
      "age": 35,
      "gender": "Male",
      "state": "Punjab",
      "occupation": "farmer",
      "annual_income": 250000
    }
  }'
```

### Track Application
```bash
curl http://localhost:8000/api/v1/applications/track/NS-2026-ABC123
```

## 🗄️ Database

### SQLite (Default)
Database file will be created at: `backend/nagriksetu.db`

### PostgreSQL (Optional)
To use PostgreSQL, update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/nagriksetu
```

Then install postgres driver:
```bash
pip install psycopg2-binary
```

## 📦 File Connections Summary

```
main.py (Entry Point)
  ├─→ config.get_settings()
  ├─→ database.SessionLocal, Base, engine
  ├─→ models.User, Service, Application
  ├─→ routers.chat, services, applications
  └─→ services.rag.INDIAN_SCHEMES_KNOWLEDGE

routers/chat.py
  ├─→ AIService (uses RAGService, EligibilityService)
  ├─→ EligibilityService
  └─→ database.get_db()

routers/services.py
  ├─→ Service model (database query)
  ├─→ INDIAN_SCHEMES_KNOWLEDGE (fallback)
  └─→ database.get_db()

routers/applications.py
  ├─→ User model (create/query)
  ├─→ Service model (create/query)
  ├─→ Application model (create/query)
  └─→ database.get_db()

services/ai.py
  ├─→ OpenAI client (from config)
  ├─→ RAGService.retrieve_relevant_schemes()
  ├─→ EligibilityService.get_eligible_schemes()
  └─→ Returns ChatResponse

services/rag.py
  ├─→ INDIAN_SCHEMES_KNOWLEDGE (seed data)
  ├─→ Service model (database queries)
  └─→ Returns SchemeCard, SourceDocument

services/eligibility.py
  ├─→ RAGService.search_schemes() (scheme lookup)
  ├─→ Service model (database queries)
  └─→ Returns EligibilityResult
```

## 🔧 Environment Variables

```
# Application
APP_NAME=NagrikSetu
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# OpenAI (REQUIRED)
OPENAI_API_KEY=sk-your-api-key-here

# Database
DATABASE_URL=sqlite:///./nagriksetu.db

# API
API_PREFIX=/api
API_V1_STR=/api/v1

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
FRONTEND_URL=http://localhost:3000
```

## 🐛 Troubleshooting

### Import Errors
- **Solution:** Make sure `pip install -r requirements.txt` completed successfully
- **Check:** Run `pip list` to see installed packages

### OpenAI API Key Error
- **Solution:** Add `OPENAI_API_KEY` to `.env` file
- **Check:** Verify your API key is valid at https://platform.openai.com/api-keys

### Database Connection Error
- **Solution:** For SQLite, ensure write permissions in `backend/` directory
- **For PostgreSQL:** Verify connection string and database exists

### CORS Issues
- **Solution:** Update `ALLOWED_ORIGINS` in `.env` to match your frontend URL

## 📚 API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Root status endpoint |
| GET | `/health` | Health check |
| POST | `/api/v1/chat` | Chat with AI assistant |
| POST | `/api/v1/chat/eligibility` | Check scheme eligibility |
| GET | `/api/v1/services` | List and search schemes |
| POST | `/api/v1/applications` | Submit scheme application |
| GET | `/api/v1/applications/track/{tracking_number}` | Track application status |

## 🎯 Next Steps

1. **Frontend Integration:** Connect React/Next.js frontend to these APIs
2. **Add Authentication:** Implement JWT/OAuth for user accounts
3. **Expand Schemes:** Add more government schemes to knowledge base
4. **Deploy:** Set up CI/CD pipeline and deploy to cloud
5. **Monitor:** Add logging, analytics, and error tracking

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed technical documentation.
