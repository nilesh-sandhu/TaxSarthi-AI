from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine

# =====================================================
# MODELS
# =====================================================

from models.user import User
from models.category import Category
from models.product_master import ProductMaster
from models.product_alias import ProductAlias
from models.hsn import HSNMaster
from models.gst_slab import GSTSlab
from models.faq import FAQ
from models.notification import Notification
from models.circular import Circular


# =====================================================
# ROUTERS
# =====================================================

from routes.auth import router as auth_router
from routes.health import router as health_router
from routes.category import router as category_router
from routes.hsn import router as hsn_router
from routes.gst_slab import router as gst_slab_router
from routes.product_master import router as product_master_router
from routes.product_alias import router as product_alias_router
from routes.faq import router as faq_router
from routes.ai import router as ai_router
from routes.business_profile import router as business_profile_router

from routes import document
from routes import invoice_analysis

from routes.notification import router as notification_router
from routes.circular import router as circular_router
from routes.search import router as search_router
from routes.gst import router as gst_router
from routes.calculator import router as calculator_router
from routes.registration import router as registration_router
from routes.returns_advisor import router as returns_router

from dashboard.routes import router as dashboard_router
from routes.chat import router as chat_router


# =====================================================
# DATABASE
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="TaxSarthi AI",
    description="AI Chartered Accountant for Indian Businesses",
    version="2.0.0",
)


# =====================================================
# CORS
# =====================================================

ALLOWED_ORIGINS = [
    # Local development
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # Production frontend
    "https://tax-sarthi-ai.vercel.app",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROUTERS
# =====================================================

app.include_router(auth_router)
app.include_router(health_router)

app.include_router(category_router)
app.include_router(hsn_router)
app.include_router(gst_slab_router)

app.include_router(product_master_router)
app.include_router(product_alias_router)

app.include_router(faq_router)

app.include_router(ai_router)
app.include_router(business_profile_router)

app.include_router(document.router)
app.include_router(invoice_analysis.router)

app.include_router(notification_router)
app.include_router(circular_router)
app.include_router(search_router)

app.include_router(gst_router)
app.include_router(calculator_router)

app.include_router(registration_router)
app.include_router(returns_router)

app.include_router(dashboard_router)
app.include_router(chat_router)


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():
    return {
        "project": "TaxSarthi AI",
        "version": "2.0.0",
        "status": "Running",
        "message": "AI Chartered Accountant for Indian Businesses",
    }


# =====================================================
# ABOUT
# =====================================================

@app.get("/about")
def about():
    return {
        "developer": "Nilesh Sandhu",
        "project": "TaxSarthi AI",
        "database": "SQLite",
        "framework": "FastAPI",
        "version": "2.0.0",
    }