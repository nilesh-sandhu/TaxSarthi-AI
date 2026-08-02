# TaxSarthi AI
# System Architecture Document

**Version:** 1.0

**Project:** TaxSarthi AI – Intelligent GST & Business Copilot

---

# 1. System Overview

TaxSarthi AI follows a modular three-tier architecture consisting of:

- Presentation Layer
- Application Layer
- Data Layer

This architecture ensures scalability, maintainability, and future AI integration.

---

# 2. High Level Architecture

```
                    USER
                      │
                      ▼
          Next.js Frontend (React)
                      │
          HTTPS / REST API
                      │
                      ▼
              FastAPI Backend
                      │
     ┌────────────────┼────────────────┐
     ▼                ▼                ▼
Authentication   Business Logic   AI Engine
     │                │                │
     └────────────┬───┴────────────┬───┘
                  ▼                ▼
           PostgreSQL      Knowledge Base
                  │
                  ▼
            Admin Dashboard
```

---

# 3. Architecture Layers

## Presentation Layer

Responsible for user interaction.

Components:

- Landing Page
- Login
- Dashboard
- AI Chat
- Product Search
- GST Forms
- Calculator
- Notifications
- Profile
- Admin Panel

Technology:

- Next.js
- React
- Tailwind CSS

---

## Application Layer

Responsible for business logic.

Components:

- Authentication Service
- Product Service
- Business Service
- GST Forms Service
- Notification Service
- AI Service
- Search Engine
- Calculator Service

Technology:

- FastAPI
- Python

---

## Data Layer

Responsible for data storage.

Database:

- PostgreSQL

Storage includes:

- Users
- Products
- Businesses
- GST Rates
- HSN Codes
- GST Forms
- Notifications
- Chat History

---

# 4. Backend Architecture

The backend follows a modular architecture.

```
backend/

api/

auth/

core/

dependencies/

middleware/

models/

routes/

schemas/

services/

utils/

main.py
```

Each module has a single responsibility.

---

# 5. Frontend Architecture

```
frontend/

components/

pages/

hooks/

services/

styles/

public/

utils/
```

The frontend communicates only through REST APIs.

---

# 6. Authentication Flow

User

↓

Register

↓

Password Hashing (bcrypt)

↓

Database

↓

Login

↓

JWT Token

↓

Protected APIs

↓

Dashboard

---

# 7. AI Processing Flow

User Question

↓

Intent Detection

↓

Knowledge Base Search

↓

Business Logic

↓

AI Response Generation

↓

Response to User

Future versions may integrate OpenAI and Retrieval-Augmented Generation (RAG).

---

# 8. Product Search Flow

User

↓

Search Product

↓

Product Database

↓

GST Rate

↓

HSN Code

↓

Display Result

---

# 9. GST Registration Flow

User

↓

Business Selection

↓

Eligibility Check

↓

Required Documents

↓

Registration Steps

↓

GST Registration Guidance

---

# 10. Admin Flow

Administrator

↓

Login

↓

Manage Products

↓

Manage Businesses

↓

Manage GST Rates

↓

Manage Notifications

↓

Manage Forms

↓

Save Changes

↓

Database Updated

---

# 11. Security Architecture

Security includes:

- JWT Authentication
- Password Hashing (bcrypt)
- HTTPS
- Input Validation
- SQL Injection Protection
- CORS Protection

---

# 12. Scalability

The architecture supports:

- Microservices (Future)
- AI APIs
- Government APIs
- Mobile Application
- Cloud Deployment

---

# 13. Deployment Architecture

Frontend

↓

Vercel

↓

FastAPI Backend

↓

Render / Railway

↓

PostgreSQL

↓

Cloud Storage

---

# 14. Future Enhancements

- Voice Assistant
- OCR for GST Invoices
- AI Invoice Generator
- GST Return Filing
- Government API Integration
- Predictive GST Analytics