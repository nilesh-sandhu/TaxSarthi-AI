from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from models.product_master import ProductMaster
from models.chat_history import ChatHistory
from models.business_profile import BusinessProfile
from models.gst_return import GSTReturn
from models.notification import Notification
from models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ==========================================================
# Dashboard Statistics
# ==========================================================

@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
):

    total_products = db.query(Product).count()

    total_chats = db.query(ChatHistory).count()

    total_returns = db.query(GSTReturn).count()

    total_businesses = db.query(BusinessProfile).count()

    total_notifications = db.query(Notification).count()

    total_users = db.query(User).count()

    return {

        "products": total_products,

        "chats": total_chats,

        "returns": total_returns,

        "businesses": total_businesses,

        "notifications": total_notifications,

        "users": total_users,

    }