from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_chat_id: int
    database_path: str
    rules_text: str
    about_text: str


token = os.getenv("BOT_TOKEN", "").strip()

if not token:
    raise RuntimeError(
        "BOT_TOKEN is not set."
    )


admin_chat_id = os.getenv("ADMIN_CHAT_ID", "").strip()

if not admin_chat_id:
    raise RuntimeError(
        "ADMIN_CHAT_ID is not set."
    )


settings = Settings(
    bot_token=token,

    admin_chat_id=int(admin_chat_id),

    database_path=os.getenv(
        "DATABASE_PATH",
        "data/bot.db",
    ),

    rules_text=os.getenv(
        "RULES_TEXT",
        "Тут будуть правила Ріжця.",
    ),

    about_text=os.getenv(
        "ABOUT_TEXT",
        "Тут буде інформація про Ріжце.",
    ),
)
