# TaxSarthi AI
## Software Requirements Specification (SRS)

**Version:** 1.0

**Project Name:** TaxSarthi AI – Intelligent GST & Business Copilot

**Prepared By:** Nilesh Sandhu

**Technology Stack:** FastAPI, Next.js, PostgreSQL, AI

**Date:** July 2026

---

# 1. Introduction

## 1.1 Project Overview

TaxSarthi AI is an AI-powered GST and Business Assistant designed to simplify Goods and Services Tax (GST) related tasks for businesses, professionals, students, and entrepreneurs in India.

Unlike traditional government portals that primarily provide static information, TaxSarthi AI delivers an interactive, intelligent, and user-friendly experience by combining Artificial Intelligence with a structured GST knowledge base.

The platform will help users understand GST rules, search GST rates and HSN codes, access GST forms, calculate GST, receive business-specific guidance, and interact with an AI assistant through natural language.

---

## 1.2 Purpose

The purpose of TaxSarthi AI is to reduce the complexity of GST compliance by providing a centralized intelligent platform where users can obtain reliable GST information, registration guidance, product tax details, and AI-powered assistance.

The system aims to improve accessibility, reduce manual searching, and simplify GST-related decision making.

---

## 1.3 Problem Statement

The current GST ecosystem presents several challenges:

- Information is scattered across multiple websites.
- Users struggle to find applicable GST rates.
- Business owners often do not know GST registration requirements.
- Understanding GST forms can be difficult.
- Government portals provide limited conversational guidance.
- Users spend significant time searching for GST notifications and updates.

TaxSarthi AI addresses these problems by offering a unified AI-powered platform.

---

## 1.4 Objectives

The primary objectives are:

- Build an AI-powered GST assistant.
- Provide intelligent GST guidance.
- Help users identify GST applicability.
- Search GST rates and HSN codes.
- Explain GST forms.
- Provide GST calculator.
- Maintain updated GST knowledge.
- Offer business-specific recommendations.
- Create an intuitive and responsive web application.

---

## 1.5 Scope

The system includes:

- User Authentication
- AI Chat Assistant
- GST Product Search
- HSN Code Search
- Business Registration Guide
- GST Forms
- GST Notifications
- GST Calculator
- User Dashboard
- Admin Dashboard

Future versions may include GST Return Filing Integration, Invoice Generation, and Government API integration.

---

## 1.6 Target Users

- Small Business Owners
- Shopkeepers
- Startups
- Chartered Accountants
- Tax Consultants
- Students
- Entrepreneurs
- Freelancers
- GST Learners

---

## 1.7 User Roles

### Administrator

The administrator can:

- Manage products
- Manage GST rates
- Manage HSN codes
- Manage GST forms
- Manage notifications
- Manage businesses
- Manage users
- View analytics

### Registered User

Registered users can:

- Chat with AI
- Save chat history
- Search products
- View GST forms
- Calculate GST
- Receive personalized recommendations

### Guest User

Guest users can:

- Search products
- Search GST rates
- Use GST calculator
- Read notifications
- Access public information

---

## 1.8 Project Goals

The project aims to become one of India's most comprehensive AI-powered GST assistance platforms by providing intelligent recommendations, structured GST knowledge, and an easy-to-use interface.
---

# 2. Functional Requirements

The following functional requirements define the core capabilities of TaxSarthi AI.

## FR-01 User Authentication

The system shall allow users to:

- Register with email and password.
- Login securely using JWT authentication.
- Logout from all active sessions.
- Reset forgotten passwords.
- Update their profile information.

---

## FR-02 AI GST Assistant

The AI assistant shall:

- Answer GST-related questions.
- Understand natural language.
- Remember conversation context.
- Recommend GST registration.
- Explain GST rules.
- Explain HSN codes.
- Suggest applicable GST rates.
- Guide users through GST filing procedures.

---

## FR-03 Product Search

Users shall be able to:

- Search products.
- View GST percentage.
- View HSN Code.
- View product category.
- Search using product name or keywords.

---

## FR-04 Business Guide

The system shall provide:

- Business-specific GST guidance.
- Registration eligibility.
- Required documents.
- Applicable GST returns.
- Business compliance checklist.

---

## FR-05 GST Forms

The system shall:

- Display all GST forms.
- Explain each form.
- Show filing purpose.
- Show filing frequency.
- Provide download links (future).

---

## FR-06 GST Calculator

The calculator shall support:

- Inclusive GST Calculation
- Exclusive GST Calculation
- Multiple GST Slabs
- Invoice Tax Calculation

---

## FR-07 Notifications

Users shall receive:

- Latest GST Updates
- Circulars
- Government Notifications
- Due Date Alerts

---

## FR-08 Admin Panel

Administrator shall manage:

- Products
- Businesses
- GST Rates
- HSN Codes
- Forms
- Notifications
- Users
- AI Knowledge Base

---

# 3. Non-Functional Requirements

## Performance

- Response time should be under 2 seconds.
- AI responses should be optimized.
- Database queries should be indexed.

---

## Security

- JWT Authentication
- Password Hashing (bcrypt)
- HTTPS Communication
- SQL Injection Protection
- Input Validation

---

## Scalability

The platform should support:

- 1000+ concurrent users
- Millions of products
- Thousands of businesses
- Future API integrations

---

## Reliability

- 99.9% uptime
- Automatic error handling
- Logging and monitoring

---

## Usability

The interface should be:

- Mobile Responsive
- Beginner Friendly
- Fast
- Accessible
- Interactive

---

# 4. Project Modules

TaxSarthi AI consists of the following modules:

1. Authentication Module
2. AI Chat Module
3. Product Module
4. Business Module
5. GST Forms Module
6. GST Calculator Module
7. Notification Module
8. Dashboard Module
9. Admin Module
10. Analytics Module

---

# 5. Technology Stack

## Backend

- FastAPI
- Python

## Frontend

- Next.js
- React.js
- Tailwind CSS

## Database

- PostgreSQL

## AI

- OpenAI API (Future)
- LangChain (Future)
- Vector Database (Future)

## Authentication

- JWT
- bcrypt

## Deployment

- Docker
- Render / Railway
- Vercel