from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.keyboards import back_keyboard, main_menu


router = Router()


WELCOME = (
    "<b>🎭 Вітаємо в боті рольової гри!</b>\n\n"
    "Через цей бот ти можеш:\n"
    "📝 подати заявку на вступ;\n"
    "📊 перевірити статус заявки;\n"
    "📜 ознайомитися з правилами;\n"
    "ℹ️ дізнатися більше про ролівку."
)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        WELCOME,
        reply_markup=main_menu(),
    )


@router.message(Command("menu"))
async def menu(message: Message) -> None:
    await message.answer(
        "Головне меню:",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "menu")
async def menu_callback(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    if callback.message:
        await callback.message.edit_text(
            WELCOME,
            reply_markup=main_menu(),
        )


@router.callback_query(F.data == "info:rules")
async def rules(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    if callback.message:
        await callback.message.edit_text(
            f"<b>📜 Правила</b>\n\n"
            f"{settings.rules_text}",
            reply_markup=back_keyboard(),
        )


@router.callback_query(F.data == "info:about")
async def about(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    if callback.message:
        await callback.message.edit_text(
            f"<b>ℹ️ Про ролівку</b>\n\n"
            f"{settings.about_text}",
            reply_markup=back_keyboard(),
        )
