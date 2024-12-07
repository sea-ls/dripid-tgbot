from aiogram.fsm.state import StatesGroup, State


class StateUser(StatesGroup):
    waiting_weight = State()
    waiting_money = State()

class OrderTracking(StatesGroup):
    waiting_for_tracking_number = State()