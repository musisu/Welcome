from aiogram import Bot, Router

from bot.config import settings


router = Router()


async def send_application_to_admins(
    bot: Bot,
    text: str,
) -> None:
    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=text,
    )
