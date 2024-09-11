from aiogram.fsm.state import StatesGroup, State


class StateUser(StatesGroup):
    waiting_weight = State()
    waiting_money = State()