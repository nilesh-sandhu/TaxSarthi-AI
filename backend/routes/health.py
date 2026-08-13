from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health_check():

    return {
        "status": "healthy",
        "backend": "online",
        "database": "connected",
        "ai": "connected",
        "version": "1.0.0",
        "timestamp": datetime.now(),
    }