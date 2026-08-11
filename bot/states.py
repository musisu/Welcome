from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    name = State()
    age = State()
    contact = State()
    rp_experience = State()
    motivation = State()
    desired_role = State()
    extra = State()
    confirm = State()
