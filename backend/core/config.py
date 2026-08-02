class Settings:
    PROJECT_NAME = "TaxSarthi AI"
    PROJECT_VERSION = "1.0.0"

    DATABASE_URL = "sqlite:///./taxsarthi.db"

    SECRET_KEY = "taxsarthi_super_secret_key_2026"

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60


settings = Settings()