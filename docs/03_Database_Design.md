# TaxSarthi AI
# Database Design Document

**Version:** 1.0

**Project:** TaxSarthi AI – Intelligent GST & Business Copilot

---

# 1. Database Overview

TaxSarthi AI uses a relational database to store user information, GST knowledge, business categories, products, HSN codes, forms, notifications, and AI chat history.

The database is designed to be scalable, secure, and optimized for fast searching.

Database:

- PostgreSQL (Production)
- SQLite (Development)

---

# 2. Entity Relationship Overview

Main Entities:

- Users
- Products
- HSN Codes
- Businesses
- GST Forms
- GST Notifications
- GST Rules
- AI Conversations
- Chat Messages
- Calculator Logs
- Admin Users
- Audit Logs

---

# 3. Users Table

Table Name:

users

Columns:

- id
- full_name
- email
- password_hash
- mobile
- role
- created_at
- updated_at
- last_login
- is_active

Purpose:

Stores registered users.

---

# 4. Products Table

Table Name:

products

Columns:

- id
- product_name
- category
- gst_rate
- hsn_code
- description
- created_at
- updated_at

Purpose:

Stores GST products.

---

# 5. HSN Codes Table

Table Name:

hsn_codes

Columns:

- id
- hsn_code
- product_name
- gst_rate
- chapter
- description

Purpose:

Stores HSN master database.

---

# 6. Businesses Table

Table Name:

businesses

Columns:

- id
- business_name
- business_type
- annual_turnover
- gst_required
- registration_threshold
- required_documents
- created_at

Purpose:

Stores supported business categories.

---

# 7. GST Forms Table

Table Name:

gst_forms

Columns:

- id
- form_name
- form_number
- purpose
- frequency
- description
- due_date

Purpose:

Stores GST forms.

---

# 8. Notifications Table

Table Name:

notifications

Columns:

- id
- title
- description
- category
- publish_date
- source
- status

Purpose:

Stores GST updates and notifications.

---

# 9. GST Rules Table

Table Name:

gst_rules

Columns:

- id
- title
- category
- description
- effective_date
- reference

Purpose:

Stores GST rules and regulations.

---

# 10. AI Conversations Table

Table Name:

conversations

Columns:

- id
- user_id
- title
- created_at
- updated_at

Purpose:

Stores AI chat sessions.

---

# 11. Chat Messages Table

Table Name:

messages

Columns:

- id
- conversation_id
- sender
- message
- timestamp

Purpose:

Stores every chat message.

---

# 12. GST Calculator Logs

Table Name:

calculator_logs

Columns:

- id
- user_id
- amount
- gst_rate
- gst_amount
- total_amount
- created_at

Purpose:

Stores GST calculations.

---

# 13. Admin Users

Table Name:

admins

Columns:

- id
- name
- email
- password_hash
- role
- created_at

Purpose:

Stores administrator accounts.

---

# 14. Audit Logs

Table Name:

audit_logs

Columns:

- id
- admin_id
- action
- table_name
- record_id
- timestamp

Purpose:

Tracks every admin action.

---

# 15. Relationships

Users

↓

Conversations

↓

Messages

Products

↓

HSN Codes

Businesses

↓

GST Rules

Notifications

↓

Users

Admins

↓

Audit Logs

---

# 16. Indexing Strategy

Indexes will be created on:

- email
- product_name
- hsn_code
- business_type
- form_number
- category

to improve search performance.

---

# 17. Future Database Expansion

Future tables:

- GST Return Filing
- Invoice Generator
- Payment Gateway
- OCR Documents
- AI Feedback
- User Preferences
- Saved Searches
- Bookmarks

---

# 18. Database Security

Security measures include:

- Password Hashing
- JWT Authentication
- Foreign Keys
- Cascading Deletes
- Input Validation
- Database Backups
- Role-Based Access Control

---

# 19. Estimated Database Size

Version 1:

- 10,000+ Products
- 5,000+ HSN Codes
- 500+ Business Categories
- 100+ GST Forms
- Unlimited Chat History

---

# 20. Conclusion

The TaxSarthi AI database is designed using a modular relational architecture to support future AI capabilities, government API integration, and nationwide scalability.