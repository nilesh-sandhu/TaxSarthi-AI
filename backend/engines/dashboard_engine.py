from sqlalchemy.orm import Session

from engines.business_engine import business_summary
from engines.registration_engine import registration_summary
from engines.compliance_engine import compliance_summary
from engines.recommendation_engine import generate_recommendations
from engines.notification_engine import latest_notifications
from engines.circular_engine import latest_circulars


def dashboard_summary(
    business,
    db: Session,
):

    return {

        "business":
            business_summary(business),

        "registration":
            registration_summary(business),

        "compliance":
            compliance_summary(business),

        "recommendations":
            generate_recommendations(business),

        "notifications":
            latest_notifications(db, 5),

        "circulars":
            latest_circulars(db, 5),

    }