from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.db import (
    create_application,
    get_latest_user_application,
)
from bot.keyboards import (
    cancel_keyboard,
    confirm_keyboard,
    main_menu,
)
from bot.states import ApplicationForm


router = Router()


QUESTIONS = {
    ApplicationForm.name:
        "1/7. Як тебе звати?\n\n"
        "Напиши свій RP-нік або ім'я.",

    ApplicationForm.age:
        "2/7. Скільки тобі років?",

    ApplicationForm.contact:
        "3/7. Як із тобою зв'язатися?\n\n"
        "Наприклад: @username або Discord.",

    ApplicationForm.rp_experience:
        "4/7. Розкажи коротко про свій досвід у RP.",

    ApplicationForm.motivation:
        "5/7. Чому хочеш приєднатися до нашої ролівки?",

    ApplicationForm.desired_role:
        "6/7. Яку роль або фракцію хочеш отримати?",

    ApplicationForm.extra:
        "7/7. Є щось додаткове, що хочеш повідомити адміністрації?",
}


async def start_form(
    message: Message,
    state: FSMContext,
) -> None:
    await state.clear()

    await state.set_state(ApplicationForm.name)

    await message.answer(
        "<b>📝 Заявка на вступ</b>\n\n"
        "Відповідай на запитання по черзі.\n"
        "Після завершення ти зможеш перевірити всю заявку "
        "перед відправленням.",
        reply_markup=cancel_keyboard(),
    )

    await message.answer(
        QUESTIONS[ApplicationForm.name],
        reply_markup=cancel_keyboard(),
    )


@router.callback_query(F.data == "app:start")
async def application_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    if callback.message:
        await start_form(callback.message, state)


@router.message(ApplicationForm.name)
async def form_name(
    message: Message,
    state: FSMContext,
) -> None:
    await save_and_next(
        message,
        state,
        "name",
        ApplicationForm.age,
    )


@router.message(ApplicationForm.age)
async def form_age(
    message: Message,
    state: FSMContext,
) -> None:
    await save_and_next(
        message,
        state,
        "age",
        ApplicationForm.contact,
    )


@router.message(ApplicationForm.contact)
async def form_contact(
    message: Message,
    state: FSMContext,
) -> None:
    await save_and_next(
        message,
        state,
        "contact",
        ApplicationForm.rp_experience,
    )


@router.message(ApplicationForm.rp_experience)
async def form_experience(
    message: Message,
    state: FSMContext,
) -> None:
    await save_and_next(
        message,
        state,
        "rp_experience",
        ApplicationForm.motivation,
    )


@router.message(ApplicationForm.motivation)
async def form_motivation(
    message: Message,
    state: FSMContext,
) -> None:
    await save_and_next(
        message,
        state,
        "motivation",
        ApplicationForm.desired_role,
    )


@router.message(ApplicationForm.desired_role)
async def form_role(
    message: Message,
    state: FSMContext,
) -> None:
    await save_and_next(
        message,
        state,
        "desired_role",
        ApplicationForm.extra,
    )


@router.message(ApplicationForm.extra)
async def form_extra(
    message: Message,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Будь ласка, надішли відповідь текстом."
        )
        return

    await state.update_data(
        extra=message.text.strip()
    )

    data = await state.get_data()

    preview = format_application(data)

    await state.set_state(ApplicationForm.confirm)

    await message.answer(
        "<b>🔎 Перевір заявку</b>\n\n"
        + preview,
        reply_markup=confirm_keyboard(),
    )


@router.callback_query(F.data == "app:submit")
async def application_submit(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    data = await state.get_data()

    if not data.get("name"):
        await callback.message.answer(
            "Заявка втратила дані. Почни заново."
        )

        await state.clear()
        return

    existing = await get_latest_user_application(
        callback.from_user.id
    )

    if existing and existing["status"] == "pending":
        await state.clear()

        await callback.message.edit_text(
            f"У тебе вже є заявка "
            f"<b>#{existing['id']}</b>, "
            f"яка перебуває на розгляді.",
            reply_markup=main_menu(),
        )

        return

    application_id = await create_application(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        data=data,
    )

    text = (
        f"<b>📝 Нова заявка #{application_id}</b>\n\n"
        f"<b>Telegram:</b> "
        f"{callback.from_user.full_name}\n"
        f"<b>Username:</b> "
        f"@{callback.from_user.username or 'немає'}\n"
        f"<b>User ID:</b> "
        f"<code>{callback.from_user.id}</code>\n\n"
        f"{format_application(data)}"
    )

    from bot.handlers.admin import (
        send_application_to_admins,
    )

    await send_application_to_admins(
        callback.bot,
        text,
        application_id,
    )

    await state.clear()

    await callback.message.edit_text(
        f"✅ Заявку "
        f"<b>#{application_id}</b> "
        f"надіслано адміністрації.\n\n"
        f"Коли рішення буде прийнято, "
        f"бот повідомить тебе.",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "app:restart")
async def application_restart(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    if callback.message:
        await start_form(
            callback.message,
            state,
        )


@router.callback_query(F.data == "app:cancel")
async def application_cancel(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer(
        "Заявку скасовано"
    )

    await state.clear()

    if callback.message:
        await callback.message.edit_text(
            "Головне меню:",
            reply_markup=main_menu(),
        )


@router.callback_query(F.data == "app:status")
async def application_status(
    callback: CallbackQuery,
) -> None:
    await callback.answer()

    row = await get_latest_user_application(
        callback.from_user.id
    )

    if not row:
        text = (
            "📊 Ти ще не подавав заявку."
        )
    else:
        statuses = {
            "pending": "⏳ На розгляді",
            "accepted": "✅ Прийнята",
            "rejected": "❌ Відхилена",
            "review": "🔎 Додатковий розгляд",
        }

        text = (
            f"<b>📊 Заявка #{row['id']}</b>\n\n"
            f"Статус: "
            f"<b>{statuses.get(row['status'], row['status'])}</b>\n"
            f"Створена: {row['created_at']}"
        )

    if callback.message:
        await callback.message.edit_text(
            text,
            reply_markup=main_menu(),
        )


async def save_and_next(
    message: Message,
    state: FSMContext,
    key: str,
    next_state: ApplicationForm,
) -> None:
    if not message.text or not message.text.strip():
        await message.answer(
            "Будь ласка, введи відповідь текстом.",
            reply_markup=cancel_keyboard(),
        )
        return

    await state.update_data(
        **{key: message.text.strip()}
    )

    await state.set_state(next_state)

    await message.answer(
        QUESTIONS[next_state],
        reply_markup=cancel_keyboard(),
    )


def format_application(
    data: dict,
) -> str:
    return (
        f"<b>Ім'я / нік:</b> "
        f"{escape(data.get('name'))}\n"

        f"<b>Вік:</b> "
        f"{escape(data.get('age'))}\n"

        f"<b>Контакт:</b> "
        f"{escape(data.get('contact'))}\n"

        f"<b>Досвід RP:</b> "
        f"{escape(data.get('rp_experience'))}\n"

        f"<b>Мотивація:</b> "
        f"{escape(data.get('motivation'))}\n"

        f"<b>Бажана роль:</b> "
        f"{escape(data.get('desired_role'))}\n"

        f"<b>Додатково:</b> "
        f"{escape(data.get('extra'))}"
    )


def escape(
    value: str | None,
) -> str:
    if value is None:
        return "-"

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
