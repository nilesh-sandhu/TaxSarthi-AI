from fastapi import FastAPI

from core.database import Base, engine
from models.user import User

from routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaxSarthi AI API",
    description="India's Intelligent GST Copilot",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "project": "TaxSarthi AI",
        "version": "1.0.0",
        "status": "Running",
        "message": "Welcome to India's Intelligent GST Copilot 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "server": "online"
    }


@app.get("/about")
def about():
    return {
        "developer": "Nilesh Sandhu",
        "project": "TaxSarthi AI",
        "description": "AI-powered GST Assistant for India"
    }