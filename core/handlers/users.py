import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import requests


from core.keyboards import inline
from core.keyboards.inline import questions
from core.utils import callbackdata, google_api, dict_data
import config
from core.utils.state import StateUser, OrderTracking
import time

logging.basicConfig(filename="test.log",
                    filemode='a',
                    level=logging.INFO)

async def unknown_command(message: Message):
    if message.text.startswith('/'):
        await message.answer("Извините, я не знаю такой команды. Попробуйте /help для списка доступных команд.")
    else:
        await message.answer("Я вас не понял. Напишите /help, чтобы узнать, что я умею.")


async def get_start(msg: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    first_name = msg.from_user.first_name
    if isinstance(msg, CallbackQuery):
        msg = msg.message
        await msg.delete()

    message = f'👋 Добро пожаловать, уважаемый(ая) <b>{first_name}!</b>\n\n' \
              f'👍 Ваше путешествие в мир зарубежного шоппинга начинается здесь.\n' \
              f'💵 Рассчитайте примерную стоимость вашего заказа и окунитесь в мир возможностей.'
    reply = inline.start_menu()
    await msg.answer(text=message, reply_markup=reply)

async def get_order_status(msg: Message, state: FSMContext):
    message = f'Напишите ваш трек номер!'
    reply = inline.start_menu_return()
    await msg.answer(text=message, reply_markup = reply)
    await state.set_state(OrderTracking.waiting_for_tracking_number)

async def mailing(msg: Message , bot: Bot):
    user_id = msg.from_user.id
    if user_id == 243106987:  # Тут id того, кому можно выполнять команду рассылки
        await start_mailing(bot)

def get_users_list():
    with open('users.txt', 'r') as f:
        return f.readlines()

async def start_mailing(bot: Bot):  # Функция рассылки
    print(len(get_users_list()))
    for i in get_users_list():
        try:
            time.sleep(1)
            text = '''
            🥰Доброго дня, мы не с очень приятными новостями: 

Наш канал, который находился по адресу https://t.me/drip_id0 был удален (с чем это связано не знаем, поддержка нам ничего не отвечает уже более 12 часов)

Пока мы решаем эту проблему, чтобы оставаться на связи в случае не благоприятного исхода, просим вас подписаться на https://t.me/dripid_service

Заранее очень благодарны🥶'''
            await bot.send_message(chat_id=i,
                                   text=text)
            logging.info('Отправлено пользователю - ' + i)
            print('Отправлено пользователю - ' + i)
        except Exception as e:
            logging.error('НЕ Отправлено пользователю - ' + i)
            logging.error(e)
            print('НЕ Отправлено пользователю - ' + i)
            print(e)

async def select_product_category(call: CallbackQuery, callback_data: callbackdata.StepOne):
    message = f'Выберите категорию товара:'
    reply = inline.select_product_category(callback_data.buyout)
    await call.message.edit_text(text=message, reply_markup=reply)


async def weight_product(call: CallbackQuery, callback_data: callbackdata.StepTwo, state: FSMContext):
    data = {
        'buyout': callback_data.buyout
    }
    await state.set_data(data)
    message = f'Введите вес товара в килограммах'
    reply = inline.start_menu_return()
    await call.message.edit_text(text=message, reply_markup=reply)
    await state.set_state(StateUser.waiting_weight)


async def msg_currency_product(msg: Message, state: FSMContext):
    try:
        weight = float(msg.text)
    except ValueError:
        try:
            weight_repl = msg.text.replace(',', '.')
            weight = float(weight_repl)
        except ValueError:
            message = f'Произошла ошибка. Вы должны ввести вес товара, а не текст'
            reply = inline.start_menu_return()
            await msg.answer(text=message, reply_markup=reply)
            return
    data = await state.get_data()
    message = f'В какой валюте отображается стоимость товара?'
    reply = inline.currency_product(data.get('buyout'), weight)
    await msg.answer(text=message, reply_markup=reply)
    await state.clear()


async def currency_product(call: CallbackQuery, callback_data: callbackdata.StepTwo):
    message = f'В какой валюте стоимость товара?'
    reply = inline.currency_product(callback_data.buyout, callback_data.category)
    await call.message.edit_text(text=message, reply_markup=reply)


async def specify_cost_product(call: CallbackQuery, callback_data: callbackdata.StepThree, state: FSMContext):
    data = {
        'buyout': callback_data.buyout,
        'category': callback_data.category,
        'currency': callback_data.currency
    }
    await state.set_data(data)
    message = f'Укажите стоимость товара с учетом доставки от магазина (если не знаете цену доставки, напишите только ' \
              f'стоимость товара):'
    reply = inline.start_menu_return()
    await call.message.edit_text(text=message, reply_markup=reply)
    await state.set_state(StateUser.waiting_money)


async def enter_price_product(msg: Message, state: FSMContext, bot: Bot):
    try:
        money = float(msg.text)
    except ValueError:
        try:
            money_repl = msg.text.replace(',', '.')
            money = float(money_repl)
        except ValueError:
            message = f'Произошла ошибка. Вы должны ввести стоимость товара, а не текст'
            reply = inline.start_menu_return()
            await msg.answer(text=message, reply_markup=reply)
            return

    data = await state.get_data()

    await state.clear()
    # Загрузка данных из Google Sheets
    data_api = google_api.get_google_api()

    if data.get('buyout') == 1:
        buyout = data_api[0]
    elif data.get('buyout') == 2:
        buyout = data_api[1]
    elif data.get('buyout') == 3:
        buyout = data_api[2]
    else:
        buyout = data_api[0]

    dollar = float(buyout.get('Доллар'))

    if data.get('currency') == 1:
        exchange_rate = float(buyout.get('Доллар'))
        price_per = float(data_api[8].get('Доллар'))
    elif data.get('currency') == 2:
        exchange_rate = float(buyout.get('Евро'))
        price_per = float(data_api[8].get('Евро'))
    elif data.get('currency') == 3:
        exchange_rate = float(buyout.get('Фунт'))
        price_per = float(data_api[8].get('Фунт'))
    elif data.get('currency') == 4:
        exchange_rate = float(buyout.get('Юань'))
        price_per = float(data_api[8].get('Юань'))
    else:
        exchange_rate = float(buyout.get('Доллар'))
        price_per = float(data_api[8].get('Доллар'))

    if data.get('category') == 1001:
        goods_weight = float(data_api[5].get('Доллар'))
    elif data.get('category') == 1002:
        goods_weight = float(data_api[5].get('Евро'))
    elif data.get('category') == 1003:
        goods_weight = float(data_api[5].get('Фунт'))
    elif data.get('category') == 1004:
        goods_weight = float(data_api[5].get('Юань'))
    else:
        goods_weight = data.get('category')

    if money * exchange_rate <= 5000:
        commission = 1000
    elif 5000 < (money * exchange_rate) <= 15000:
        commission = 1500
    else:
        commission = (money * exchange_rate * 0.1)
    print(price_per)
    delivery = goods_weight * price_per * exchange_rate
    if data.get('buyout') == 3:
        full_price = f'{round((((money * exchange_rate) + commission + delivery) / dollar), 2)} USDT'
    else:
        full_price = f'{round(((money * exchange_rate) + commission + delivery), 2)} руб.'

    redemption = dict_data.buyout.get(data.get('buyout'))
    category = dict_data.category.get(data.get('category'))
    if category is None:
        category = 'Без категории'
    currency = dict_data.currency.get(data.get('currency'))

    message = f'<b>Итоговый счет</b>\n\n' \
              f'Выкуп: <b>{redemption}</b>\n' \
              f'Категория: <b>{category}</b>\n' \
              f'Вес товара: <b>{round(goods_weight, 2)} кг.</b>\n' \
              f'Валюта: <b>{currency}</b>\n' \
              f'Стоимость товара: <b>{round(money, 2)}</b>\n' \
              f'Курс валюты: <b>{round(exchange_rate, 2)} руб.</b>\n\n' \
              f'Итоговая цена: <b>{full_price}</b>\n\n' \
              f'Точный расчет вам поможет произвести менеджер'
    reply = inline.get_manager()
    await msg.answer(text=message, reply_markup=reply)

    message = f'Новый расчет\n\n' \
              f'<b>Информация о пользователе:</b>\n' \
              f'ID: {msg.from_user.id}\n' \
              f'Username: @{msg.from_user.username}\n\n' \
              f'<b>Выбор пользователя:</b>\n' \
              f'Выкуп: <b>{redemption}</b>\n' \
              f'Категория: <b>{category}</b>\n' \
              f'Вес товара: <b>{round(goods_weight, 2)} кг.</b>\n' \
              f'Валюта: <b>{currency}</b>\n' \
              f'Стоимость товара: <b>{round(money, 2)}</b>\n' \
              f'Курс валюты: <b>{round(exchange_rate, 2)} руб.</b>\n\n' \
              f'Итоговая цена: <b>{full_price}</b>' \

    for admin in config.ADMIN:
        try:
            await bot.send_message(chat_id=admin, text=message)
        except Exception:
            continue

    # Переменные:
    # exchange_rate - курс валюты
    # goods_weight - вес товара
    # price_per - цена доставки за 1 кг
    # commission - комиссия
    # money - цена товара

async def get_faq(msg: CallbackQuery):
    message = f'Часто задаваемые вопросы:'
    reply = inline.faq_fulfillment()
    await msg.message.edit_text(text=message, reply_markup=reply, disable_web_page_preview=True)

# Универсальный обработчик для всех вопросов
async def process_question(msg: CallbackQuery):
    question_text = msg.data
    reply = inline.faq_menu_return()
    answer = questions.get(question_text, "Извините, ответ на этот вопрос не найден.")
    await msg.message.edit_text(text=answer, reply_markup=reply, disable_web_page_preview=True)


async def calculate_cost_order(msg: Message | CallbackQuery):
    message = f'⏱ В течении какого времени необходимо выкупить ваш заказ?\n' \
              f'Более подробно разобраться в выборе способа вам поможет <a href="https://t.me/Drip_ID0/552">этот пост</a>'
    if isinstance(msg, CallbackQuery):
        reply = inline.order_fulfillment()
        await msg.message.edit_text(text=message, reply_markup=reply, disable_web_page_preview=True)
    if isinstance(msg, Message):
        reply = inline.order_fulfillment()
        await msg.answer(text=message, reply_markup=reply, disable_web_page_preview=True)


async def handle_tracking_number(msg: Message, state: FSMContext):
    tracking_number = msg.text
    text = get_person_tracking("http://dripid-dev.sea-ls.ru", tracking_number)
    await msg.answer(f"Статус вашего заказа: {text}")
    await state.finish()


def get_person_tracking(base_url: str, tracking_number: str):
    endpoint = f"{base_url}/api/delivery-service/person/tracking"
    params = {"trackNumber": tracking_number}

    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 404:
            return f"Заказа с трекномером \"{tracking_number}\" нет"
        response.raise_for_status()
        return response.json().get('orderStatus')
    except requests.RequestException as e:
        print(f"Не удалось получить заказ: {e}")
        return f"Не удалось получить заказ"