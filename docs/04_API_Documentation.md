# API Documentation

## Overview

TaxSarthi AI provides REST APIs developed using **FastAPI**.

Base URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# Authentication APIs

## Register User

**POST**

```
/auth/register
```

Purpose

- Register a new user.

---

## Login

**POST**

```
/auth/login
```

Purpose

- Authenticate user.

---

# AI Assistant APIs

## AI Chat

**POST**

```
/ai/chat
```

Request

```json
{
  "message": "GST on Laptop"
}
```

Response

```json
{
  "response": "...",
  "verified": true
}
```

Purpose

- AI-powered GST assistant using Google Gemini and TaxSarthi Database.

---

# Product APIs

## Get All Products

**GET**

```
/products/
```

---

## Search Product

**GET**

```
/products/search/{product_name}
```

Example

```
/products/search/Laptop
```

Purpose

- Search GST details by product name.

---

## Create Product

**POST**

```
/products/
```

Purpose

- Add a new product.

---

## Update Product

**PUT**

```
/products/{id}
```

---

## Delete Product

**DELETE**

```
/products/{id}
```

---

# Business Profile APIs

## Create Profile

**POST**

```
/business-profile/
```

Purpose

- Save business information.

---

## Get Profile

**GET**

```
/business-profile/
```

---

## Update Profile

**PUT**

```
/business-profile/
```

---

# GST Calculator

## Calculate GST

**POST**

```
/calculator/
```

Request

```json
{
  "amount":1000,
  "gst_rate":18,
  "calculation_type":"Exclusive",
  "interstate":false
}
```

Purpose

- Calculate GST, CGST, SGST or IGST.

---

# GST Registration Advisor

## Registration Check

**GET**

```
/registration/check/{user_id}
```

Purpose

- Check whether GST registration is mandatory.

---

# GST Return Advisor

## Return Advisor

**POST**

```
/returns/advisor
```

Request

```json
{
   "registration_type":"Regular"
}
```

Purpose

- Recommend GST returns based on registration type.

---

# Dashboard APIs

## Dashboard Statistics

**GET**

```
/dashboard/stats
```

Purpose

- Returns dashboard metrics.

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
|200|Success|
|201|Created|
|400|Bad Request|
|401|Unauthorized|
|404|Not Found|
|500|Internal Server Error|

---

# API Features

- REST Architecture
- JSON Responses
- FastAPI Validation
- Pydantic Schemas
- SQLAlchemy ORM
- Google Gemini Integration
- Interactive Swagger Documentation