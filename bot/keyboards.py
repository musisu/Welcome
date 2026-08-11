from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Подати заявку",
                    callback_data="app:start",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Статус заявки",
                    callback_data="app:status",
                ),
                InlineKeyboardButton(
                    text="📜 Правила",
                    callback_data="info:rules",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Про ролівку",
                    callback_data="info:about",
                )
            ],
        ]
    )


def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="app:cancel",
                )
            ]
        ]
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Надіслати",
                    callback_data="app:submit",
                ),
                InlineKeyboardButton(
                    text="✏️ Заповнити заново",
                    callback_data="app:restart",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="app:cancel",
                )
            ],
        ]
    )


def admin_keyboard(application_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Прийняти",
                    callback_data=f"admin:accept:{application_id}",
                ),
                InlineKeyboardButton(
                    text="❌ Відхилити",
                    callback_data=f"admin:reject:{application_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⏳ На розгляд",
                    callback_data=f"admin:review:{application_id}",
                )
            ],
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Головне меню",
                    callback_data="menu",
                )
            ]
        ]
    )
