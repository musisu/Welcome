from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.db import create_application
from bot.keyboards import (
    confirm_keyboard,
    main_menu,
    yes_no_keyboard,
)
from bot.states import ApplicationForm


router = Router()


@router.callback_query(F.data == "app:start")
async def application_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.clear()

    username = callback.from_user.username

    if username:
        username_text = f"@{username}"

        await state.update_data(
            username=username_text
        )

        await state.set_state(
            ApplicationForm.username
        )

        await callback.message.edit_text(
            "📝 <b>Заявка на вступ</b>\n\n"
            f"👤 Твій Telegram: <b>{username_text}</b>\n\n"
            "Тепер одне коротке питання."
        )

        await callback.message.answer(
            "🎭 Чи грав/грала ти раніше "
            "в рольові ігри?",
            reply_markup=yes_no_keyboard(),
        )

    else:
        await state.set_state(
            ApplicationForm.username
        )

        await callback.message.edit_text(
            "📝 <b>Заявка на вступ</b>\n\n"
            "Я не бачу Telegram username у твоєму "
            "профілі.\n\n"
            "Напиши його повідомленням, наприклад:\n"
            "<code>@username</code>"
        )


@router.message(ApplicationForm.username)
async def username_received(
    message: Message,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Будь ласка, введи username текстом."
        )
        return

    username = message.text.strip()

    if not username.startswith("@"):
        username = f"@{username}"

    await state.update_data(
        username=username
    )

    await message.answer(
        "🎭 Чи грав/грала ти раніше "
        "в рольові ігри?",
        reply_markup=yes_no_keyboard(),
    )


@router.callback_query(F.data == "app:rp_yes")
async def rp_yes(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.update_data(
        rp_experience="✅ Так"
    )

    await show_preview(
        callback,
        state,
    )


@router.callback_query(F.data == "app:rp_no")
async def rp_no(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.update_data(
        rp_experience="❌ Ні"
    )

    await show_preview(
        callback,
        state,
    )


async def show_preview(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    data = await state.get_data()

    username = data.get(
        "username",
        "Не вказано",
    )

    experience = data.get(
        "rp_experience",
        "Не вказано",
    )

    await state.set_state(
        ApplicationForm.confirm
    )

    text = (
        "📋 <b>Перевір свою заявку</b>\n\n"
        f"👤 Telegram: <b>{username}</b>\n"
        f"🎭 Досвід у рольових іграх: "
        f"<b>{experience}</b>\n\n"
        "Все правильно?"
    )

    await callback.message.edit_text(
        text,
        reply_markup=confirm_keyboard(),
    )


@router.callback_query(F.data == "app:submit")
async def application_submit(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    data = await state.get_data()

    username = data.get(
        "username",
        "Не вказано",
    )

    experience = data.get(
        "rp_experience",
        "Не вказано",
    )

application_id = await create_application(
    user_id=callback.from_user.id,
    username=username,
    rp_experience=experience,
)
    from bot.handlers.admin import (
        send_application_to_admins,
    )

    text = (
        "📝 <b>НОВА ЗАЯВКА</b>\n\n"
        f"🆔 Заявка: <b>#{application_id}</b>\n"
        f"👤 Telegram: <b>{username}</b>\n"
        f"🎭 Досвід у рольових іграх: "
        f"<b>{experience}</b>\n\n"
        f"🆔 User ID: "
        f"<code>{callback.from_user.id}</code>"
    )

    await send_application_to_admins(
        callback.bot,
        text,
    )

    await state.clear()

    await callback.message.edit_text(
        "✅ <b>Заявку надіслано!</b>\n\n"
        "Дякуємо за інтерес до Ріжці.\n\n"
        "Адміністрація ознайомиться із заявкою "
        "та, якщо буде потрібно, зв'яжеться "
        "з тобою в Telegram.",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "app:restart")
async def application_restart(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.clear()

    await application_start(
        callback,
        state,
    )


@router.callback_query(F.data == "app:cancel")
async def application_cancel(
    callback: Callback,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.clear()

    await callback.message.edit_text(
        "Головне меню:",
        reply_markup=main_menu(),
    )
