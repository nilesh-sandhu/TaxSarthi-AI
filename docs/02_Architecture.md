# TaxSarthi AI - System Architecture

## Architecture Overview

```
                    ┌─────────────────────────────┐
                    │            User             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │     Streamlit Frontend      │
                    │                             │
                    │ Dashboard                   │
                    │ AI Copilot                 │
                    │ GST Search                │
                    │ Registration Advisor      │
                    │ GST Calculator            │
                    │ Return Advisor            │
                    │ Business Profile          │
                    └──────────────┬──────────────┘
                                   │
                           REST API Requests
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       FastAPI Backend       │
                    │                             │
                    │ Authentication             │
                    │ AI Services                │
                    │ Product Search             │
                    │ GST Calculator             │
                    │ Registration Engine        │
                    │ Return Advisor             │
                    │ Dashboard APIs             │
                    └──────────────┬──────────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
      ┌──────────────────────┐          ┌─────────────────────┐
      │     Google Gemini    │          │   SQLite Database   │
      │      AI Model        │          │                     │
      └──────────────────────┘          │ Users              │
                                        │ Products           │
                                        │ HSN Codes          │
                                        │ FAQs               │
                                        │ GST Returns        │
                                        │ Business Profile   │
                                        │ Chat History       │
                                        └─────────────────────┘
```

---

## Components

### Frontend
- Streamlit
- Responsive Dashboard
- Interactive Forms
- AI Chat Interface

### Backend
- FastAPI
- REST APIs
- Business Logic
- AI Integration

### Database
- SQLite
- SQLAlchemy ORM

### Artificial Intelligence
- Google Gemini
- Prompt Engineering
- Local GST Knowledge Integration

---

## Workflow

1. User submits a request from the Streamlit interface.
2. FastAPI receives the request.
3. Backend searches the local SQLite database.
4. If local data is available, it is used as context.
5. Gemini AI generates a response using the provided context.
6. The response is returned to the frontend.
7. Chat history is stored for future reference.