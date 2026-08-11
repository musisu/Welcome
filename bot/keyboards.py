from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📖 Дізнатися більше",
                    callback_data="info:menu",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Подати заявку",
                    callback_data="app:start",
                )
            ],
        ]
    )


def info_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎭 Що таке ролівка?",
                    callback_data="info:rp",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌎 Про світ Ріжці",
                    callback_data="info:world",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 Правила",
                    callback_data="info:rules",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎮 Як проходить гра?",
                    callback_data="info:game",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="menu",
                )
            ],
        ]
    )


def yes_no_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Так",
                    callback_data="app:rp_yes",
                ),
                InlineKeyboardButton(
                    text="❌ Ні",
                    callback_data="app:rp_no",
                ),
            ]
        ]
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📨 Надіслати заявку",
                    callback_data="app:submit",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Заповнити заново",
                    callback_data="app:restart",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="app:cancel",
                )
            ],
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="menu",
                )
            ]
        ]
    )
