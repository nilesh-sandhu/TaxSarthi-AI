from fastapi import FastAPI

from core.database import Base, engine
from models.gst_return import GSTReturn
from routes.gst_return import router as gst_return_router
# -----------------------------
# Models
# -----------------------------
from models.user import User
from models.product import Product
from models.faq import FAQ

# -----------------------------
# Routers
# -----------------------------
from routes.auth import router as auth_router
from routes.gst import router as gst_router
from routes.registration import router as registration_router
from routes.product import router as product_router
from routes.chat import router as chat_router
from routes.faq import router as faq_router
from models.notification import Notification
from routes.notification import router as notification_router

app.include_router(notification_router)
# -----------------------------
# Create Database Tables
# -----------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaxSarthi AI API",
    description="India's Intelligent GST Copilot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth_router)
app.include_router(gst_router)
app.include_router(registration_router)
app.include_router(product_router)
app.include_router(chat_router)
app.include_router(faq_router)
app.include_router(gst_return_router)
# -----------------------------
# Home
# -----------------------------
@app.get("/", tags=["Home"])
def home():
    return {
        "project": "TaxSarthi AI",
        "version": "1.0.0",
        "status": "Running",
        "message": "Welcome to India's Intelligent GST Copilot 🚀",
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "server": "online",
        "database": "connected",
    }


# -----------------------------
# About
# -----------------------------
@app.get("/about", tags=["System"])
def about():
    return {
        "developer": "Nilesh Sandhu",
        "project": "TaxSarthi AI",
        "description": "AI-powered GST Assistant for India",
        "framework": "FastAPI",
        "database": "SQLite",
        "version": "1.0.0",
    }