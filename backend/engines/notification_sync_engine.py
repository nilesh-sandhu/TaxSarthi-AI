import os
from datetime import datetime

import requests

from models.notification import Notification


# =====================================================
# CBIC TAX INFORMATION PORTAL
# =====================================================

CBIC_API_URL = (
    "https://taxinformation.cbic.gov.in/"
    "api/cbic-notification-msts/"
    "fetchNotificationByYearAndCategory"
)

CBIC_TAX_ID = "1000001"
CBIC_CATEGORY = "Central Tax"


# =====================================================
# HTTP HEADERS
# =====================================================

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://taxinformation.cbic.gov.in",
    "Referer": (
        "https://taxinformation.cbic.gov.in/"
        "content-page/explore-notification"
    ),
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    ),
    "language": "en",
}


# =====================================================
# GET CBIC TOKEN
# =====================================================

def get_cbic_token():
    """
    Read CBIC homeToken from environment variable.

    DO NOT hard-code the token inside Python source.
    """

    token = os.getenv("CBIC_HOME_TOKEN")

    if not token:
        return None

    return token.strip()


# =====================================================
# BUILD HEADERS
# =====================================================

def build_headers():

    headers = HEADERS.copy()

    token = get_cbic_token()

    if token:

        headers["Authorization1"] = (
            f"homeToken {token}"
        )

    return headers


# =====================================================
# FETCH NOTIFICATIONS
# =====================================================

def fetch_notifications(
    year=None,
    page=0,
    size=10,
):

    if year is None:

        year = datetime.now().year

    params = {
        "year": year,
        "page": page,
        "size": size,
        "taxId": CBIC_TAX_ID,
        "category": CBIC_CATEGORY,
    }

    try:

        response = requests.get(
            CBIC_API_URL,
            params=params,
            headers=build_headers(),
            timeout=(10, 30),
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:

        print(
            "CBIC Notification API Error:",
            e,
        )

        return None

    except ValueError as e:

        print(
            "CBIC Notification JSON Error:",
            e,
        )

        return None


# =====================================================
# PARSE DATE
# =====================================================

def parse_cbic_date(value):

    if not value:
        return None

    if isinstance(value, datetime):

        return value

    value = str(value).strip()

    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt,
            )

        except ValueError:

            continue

    return None


# =====================================================
# PARSE API RESPONSE
# =====================================================

def parse_notifications(data):

    if not data:

        return []

    # -------------------------------------------------
    # API currently returns a list.
    # But support common wrapper formats too.
    # -------------------------------------------------

    if isinstance(data, list):

        records = data

    elif isinstance(data, dict):

        records = (
            data.get("content")
            or data.get("data")
            or data.get("results")
            or data.get("items")
            or []
        )

    else:

        return []

    results = []

    seen_numbers = set()

    for item in records:

        if not isinstance(item, dict):

            continue

        # ---------------------------------------------
        # Notification Number
        # ---------------------------------------------

        number = (
            item.get("notificationNo")
            or item.get("notificationNumber")
            or item.get("notification_no")
        )

        if not number:

            continue

        number = str(number).strip()

        if number in seen_numbers:

            continue

        seen_numbers.add(number)

        # ---------------------------------------------
        # Notification Name / Subject
        # ---------------------------------------------

        title = (
            item.get("notificationName")
            or item.get("title")
            or number
        )

        title = str(title).strip()

        # ---------------------------------------------
        # Date
        # ---------------------------------------------

        notification_date = parse_cbic_date(
            item.get("notificationDt")
            or item.get("notificationDate")
            or item.get("issueDt")
        )

        # ---------------------------------------------
        # Active status
        # ---------------------------------------------

        active_value = item.get(
            "isActive",
            "Y",
        )

        if isinstance(
            active_value,
            str,
        ):

            is_active = (
                active_value.upper() == "Y"
            )

        else:

            is_active = bool(
                active_value
            )

        # ---------------------------------------------
        # Build TaxSarthi record
        # ---------------------------------------------

        results.append(
            {
                "notification_number":
                    number,

                "title":
                    title,

                "message":
                    title,

                "notification_date":
                    notification_date,

                "type":
                    "GST",

                "priority":
                    "Medium",

                "source":
                    "CBIC",

                "applicable_to":
                    "GST Taxpayers",

                "is_active":
                    is_active,
            }
        )

    return results


# =====================================================
# FETCH ALL PAGES
# =====================================================

def fetch_all_notifications(
    year=None,
    page_size=10,
    max_pages=100,
):

    if year is None:

        year = datetime.now().year

    all_records = []

    seen_numbers = set()

    for page in range(max_pages):

        print(
            f"Fetching CBIC notifications: "
            f"year={year}, page={page}"
        )

        data = fetch_notifications(
            year=year,
            page=page,
            size=page_size,
        )

        if data is None:

            print(
                "CBIC API unavailable."
            )

            break

        records = parse_notifications(
            data
        )

        if not records:

            break

        new_records = 0

        for record in records:

            number = record[
                "notification_number"
            ]

            if number in seen_numbers:

                continue

            seen_numbers.add(
                number
            )

            all_records.append(
                record
            )

            new_records += 1

        # -------------------------------------------------
        # If this page contains fewer records than page size,
        # we have reached the last page.
        # -------------------------------------------------

        if len(records) < page_size:

            break

        # -------------------------------------------------
        # Safety condition
        # -------------------------------------------------

        if new_records == 0:

            break

    return all_records


# =====================================================
# SYNC TO DATABASE
# =====================================================

def sync_notifications(
    db,
    year=None,
):

    if year is None:

        year = datetime.now().year

    records = fetch_all_notifications(
        year=year,
        page_size=10,
    )

    # -------------------------------------------------
    # Source unavailable
    # -------------------------------------------------

    if not records:

        return {
            "success": False,

            "source":
                CBIC_API_URL,

            "year":
                year,

            "found":
                0,

            "added":
                0,

            "skipped":
                0,

            "message":
                "No notifications were received from CBIC.",
        }

    added = 0
    skipped = 0

    try:

        for item in records:

            number = item[
                "notification_number"
            ]

            existing = (

                db.query(
                    Notification
                )

                .filter(
                    Notification
                    .notification_number
                    == number
                )

                .first()

            )

            # -----------------------------------------
            # Already exists
            # -----------------------------------------

            if existing:

                skipped += 1

                # Update active status/date/message
                existing.title = item["title"]

                existing.message = item["message"]

                existing.notification_date = (
                    item["notification_date"]
                )

                existing.is_active = (
                    item["is_active"]
                )

                continue

            # -----------------------------------------
            # New notification
            # -----------------------------------------

            db.add(
                Notification(
                    **item
                )
            )

            added += 1

        db.commit()

        return {

            "success":
                True,

            "source":
                CBIC_API_URL,

            "year":
                year,

            "found":
                len(records),

            "added":
                added,

            "skipped":
                skipped,

            "message":
                "CBIC GST notification sync completed successfully.",
        }

    except Exception as e:

        db.rollback()

        print(
            "Notification Database Error:",
            e,
        )

        return {

            "success":
                False,

            "source":
                CBIC_API_URL,

            "year":
                year,

            "found":
                len(records),

            "added":
                0,

            "skipped":
                skipped,

            "message":
                "Notification database update failed.",

            "error":
                str(e),
        }