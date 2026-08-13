# Add this GOOGLE_CLIENT_ID field to your existing backend/core/config.py
# or replace the file with the complete version below.

import os


class Settings:
    PROJECT_NAME = "TaxSarthi AI"
    PROJECT_VERSION = "2.0.0"

    DATABASE_URL = "sqlite:///./taxsarthi.db"

    SECRET_KEY = "taxsarthi_super_secret_key_2026"

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    GOOGLE_CLIENT_ID = os.getenv(
        "GOOGLE_CLIENT_ID",
        "302870624868-pdoh4it6tj80ql8v8i79dih7pbs4k1pq.apps.googleusercontent.com",
    )


settings = Settings()
