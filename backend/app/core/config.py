import os

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://kitchen:change_me@db:5432/kitchen"
    )

settings = Settings()

