from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from bot.keyboards import back_keyboard, info_menu, main_menu


router = Router()


WELCOME_TEXT = (
    "<b>🎭 Вітаємо в Ріжці!</b>\n\n"
    "Ріжця — це рольова гра, де ти можеш "
    "створити власну історію, познайомитися "
    "з іншими гравцями та зануритися у світ "
    "рольової гри.\n\n"
    "Якщо ти тут уперше — радимо спочатку "
    "дізнатися більше про нашу ролівку."
)


INFO_ARTICLES = {
    "info:rp": (
        "<b>🎭 Що таке ролівка?</b>\n\n"
        "Рольова гра — це формат гри, у якому "
        "ти береш на себе роль персонажа та "
        "взаємодієш з іншими учасниками.\n\n"
        "Ти не просто граєш за готового героя — "
        "ти сам вирішуєш, ким він буде, як "
        "він поводитиметься та яку історію "
        "пройде."
    ),
    "info:about": (
        "<b>🌎 Про світ Ріжці</b>\n\n"
        "Тут згодом з'явиться опис світу, "
        "його історії, фракцій, важливих подій "
        "та місць."
    ),
    "info:rules": (
        "<b>📜 Правила</b>\n\n"
        "Тут згодом будуть основні правила "
        "Ріжці та правила поведінки гравців."
    ),
    "info:post": (
        "<b>🎮 Як проходить гра?</b>\n\n"
        "Тут згодом буде пояснення того, як "
        "проходить гра, як створити персонажа "
        "та як почати свою історію."
    ),
    "info:character": (
        "<b>🎮 Як проходить гра?</b>\n\n"
        "Тут згодом буде пояснення того, як "
        "проходить гра, як створити персонажа "
        "та як почати свою історію."
}


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu(),
    )


@router.message(Command("menu"))
async def menu(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "menu")
async def menu_callback(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    await callback.message.edit_text(
        WELCOME_TEXT,
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "info:menu")
async def info_menu_callback(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    await callback.message.edit_text(
        "<b>📖 Дізнатися більше</b>\n\n"
        "Обери тему, про яку хочеш дізнатися:",
        reply_markup=info_menu(),
    )


@router.callback_query(
    F.data.in_(
        {
            "info:rp",
            "info:world",
            "info:rules",
            "info:game",
        }
    )
)
async def info_article(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    text = INFO_ARTICLES.get(
        callback.data,
        "Статтю не знайдено.",
    )

    await callback.message.edit_text(
        text,
        reply_markup=back_keyboard(),
    )
