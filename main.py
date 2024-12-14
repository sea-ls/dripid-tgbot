import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BotCommand, BotCommandScopeDefault, Message


import config
from core.handlers import users
from core.keyboards.inline import questions
from core.utils import callbackdata
from core.utils.state import StateUser, OrderTracking

commands = [
        BotCommand(command='menu', description='Вызвать Меню'),
        BotCommand(command='calculate_cost_order', description='Рассчитать стоимость заказа'),
        BotCommand(command='get_order_status', description='Узнать статус заказа')
    ]

async def start():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    bot = Bot(token=config.BOT_TOKEN, parse_mode='html')
    dp = Dispatcher()

    dp.message.register(users.get_start, Command(commands=['start', 'menu']))
    dp.message.register(users.get_order_status, Command(commands='get_order_status'))
    #dp.message.register(users.mailing, Command(commands='mailing'))
    dp.message.register(users.calculate_cost_order, Command(commands='calculate_cost_order'))

    dp.callback_query.register(users.process_question, lambda c: c.data in questions)
    dp.callback_query.register(users.get_start, F.data == 'start_menu')
    dp.callback_query.register(users.get_faq, F.data == 'get_faq')
    dp.callback_query.register(users.calculate_cost_order, F.data == 'calculate_cost_order')
    dp.callback_query.register(users.select_product_category, callbackdata.StepOne.filter())
    dp.callback_query.register(users.weight_product, callbackdata.StepTwo.filter(F.category == 5))

    dp.message.register(users.msg_currency_product, StateUser.waiting_weight)
    dp.message.register(users.handle_tracking_number, OrderTracking.waiting_for_tracking_number)
    dp.callback_query.register(users.currency_product, callbackdata.StepTwo.filter())
    dp.callback_query.register(users.specify_cost_product, callbackdata.StepThree.filter())
    dp.message.register(users.enter_price_product, StateUser.waiting_money)

    dp.message.register(users.unknown_command, F.text)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())