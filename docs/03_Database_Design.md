# Database Design

## Database

TaxSarthi AI uses **SQLite** as its relational database and **SQLAlchemy ORM** for database operations.

---

# Database Tables

## 1. User

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String | User Name |
| email | String | Email Address |
| password | String | Encrypted Password |

---

## 2. Business Profile

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key |
| business_name | String | Business Name |
| owner_name | String | Owner Name |
| business_type | String | Business Category |
| state | String | State |
| turnover | Float | Annual Turnover |
| gstin | String | GST Number |
| registration_type | String | Regular / Composition |
| created_at | DateTime | Record Creation Time |

---

## 3. Product

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String | Product Name |
| category | String | Product Category |
| gst_rate | Float | GST Rate |
| hsn_code | String | HSN Code |
| description | String | Product Description |

---

## 4. HSN

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| hsn_code | String | HSN Code |
| description | String | Product Description |
| gst_rate | Float | GST Percentage |
| category | String | Product Category |

---

## 5. FAQ

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| question | String | GST Question |
| answer | String | GST Answer |

---

## 6. GST Return

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| return_name | String | Return Name |
| description | String | Return Description |
| due_date | String | Due Date |
| frequency | String | Monthly / Quarterly |
| late_fee | String | Penalty Information |

---

## 7. Chat History

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | User ID |
| role | String | User / Assistant |
| message | Text | Chat Message |
| created_at | DateTime | Timestamp |

---

# Entity Relationship

```
User
 │
 ├───────────────┐
 ▼               ▼
BusinessProfile  ChatHistory

Product

HSN

FAQ

GSTReturn
```

---

# Database Relationships

- One User → One Business Profile
- One User → Many Chat History Records
- Product and HSN are linked using the HSN Code.
- FAQ stores GST-related knowledge.
- GST Return stores return filing information.

---

# ORM

The application uses **SQLAlchemy ORM**, which provides:

- Object Relational Mapping
- Automatic Table Creation
- CRUD Operations
- Query Builder
- Relationship Management

---

# Advantages of SQLite

- Lightweight
- Easy Deployment
- No Separate Database Server
- Perfect for Educational Projects
- Fully Compatible with SQLAlchemy