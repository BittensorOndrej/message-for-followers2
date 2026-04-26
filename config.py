import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ACCESS_TOKEN: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    PAGE_ID: str      = os.getenv("INSTAGRAM_PAGE_ID", "")
    APP_SECRET: str   = os.getenv("APP_SECRET", "")
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN", "")
    REPLY_COOLDOWN: int = int(os.getenv("REPLY_COOLDOWN", "86400"))

    @classmethod
    def validate(cls) -> None:
        missing = [k for k in ("ACCESS_TOKEN", "PAGE_ID", "APP_SECRET", "VERIFY_TOKEN")
                   if not getattr(cls, k)]
        if missing:
            raise ValueError(f"Chybí env proměnné: {', '.join(missing)}")
