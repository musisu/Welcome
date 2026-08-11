from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def parse_admin_ids(value: str) -> list[int]:
    result = []
    for item in value.split(","):
        item = item.strip()
        if item:
            result.append(int(item))
    return result


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: list[int]
    database_path: str
    rules_text: str
    about_text: str


token = os.getenv("BOT_TOKEN", "").strip()

if not token:
    raise RuntimeError(
        "BOT_TOKEN is not set. Copy .env.example to .env and configure it."
    )


settings = Settings(
    bot_token=token,
    admin_ids=parse_admin_ids(os.getenv("ADMIN_IDS", "")),
    database_path=os.getenv("DATABASE_PATH", "data/bot.db"),
    rules_text=os.getenv(
        "RULES_TEXT",
        "1. Поважайте інших гравців.\n"
        "2. Дотримуйтесь правил RP.\n"
        "3. Заборонені образи, спам і навмисний зрив гри.\n"
        "4. Адміністрація має право відхилити заявку.",
    ),
    about_text=os.getenv(
        "ABOUT_TEXT",
        "Ласкаво просимо до нашої рольової гри!",
    ),
)
