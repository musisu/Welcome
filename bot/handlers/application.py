from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    username = State()
    confirm = State()
