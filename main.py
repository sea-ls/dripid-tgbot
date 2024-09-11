import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

import config
from core.handlers import users
from core.utils import callbackdata
from core.utils.state import StateUser


async def start():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    bot = Bot(token=config.BOT_TOKEN, parse_mode='html')
    dp = Dispatcher()

    dp.message.register(users.get_start, Command(commands='start'))
    dp.callback_query.register(users.get_start, F.data == 'start_menu')
    dp.callback_query.register(users.calculate_cost_order, F.data == 'calculate_cost_order')
    dp.callback_query.register(users.select_product_category, callbackdata.StepOne.filter())
    dp.callback_query.register(users.weight_product, callbackdata.StepTwo.filter(F.category == 5))
    dp.message.register(users.msg_currency_product, StateUser.waiting_weight)
    dp.callback_query.register(users.currency_product, callbackdata.StepTwo.filter())
    dp.callback_query.register(users.specify_cost_product, callbackdata.StepThree.filter())
    dp.message.register(users.enter_price_product, StateUser.waiting_money)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())