from sqlalchemy.orm import Session

from models.circular import Circular


def latest_circulars(
    db: Session,
    limit=10,
):

    return (

        db.query(Circular)

        .filter(Circular.is_active == True)

        .order_by(
            Circular.issue_date.desc()
        )

        .limit(limit)

        .all()

    )


def search_circular(
    keyword,
    db,
):

    return (

        db.query(Circular)

        .filter(

            Circular.title.ilike(f"%{keyword}%")

        )

        .all()

    )


def circular_summary(circular):

    return {

        "title": circular.title,

        "date": circular.issue_date,

        "summary": circular.summary,

    }