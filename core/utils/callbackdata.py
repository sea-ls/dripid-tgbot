from aiogram.filters.callback_data import CallbackData


class StepOne(CallbackData, prefix='step_one'):
    buyout: int


class StepTwo(CallbackData, prefix='step_two'):
    buyout: int
    category: float


class StepThree(CallbackData, prefix='step_three'):
    buyout: int
    category: float
    currency: int