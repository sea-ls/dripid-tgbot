from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from core.utils import callbackdata

def start_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text='📇 FAQ', callback_data='get_faq')
    builder.button(text='📦 Как сделать заказ?', url=config.URL_ORDER)
    builder.button(text='💲 Как оплатить криптовалютой?', url=config.URL_PAYMENT)
    builder.button(text='✏ Отзывы', url=config.URL_REVIEWS)
    builder.button(text='👩‍💻  Связь с менеджером', url=config.URL_MANAGER)
    builder.button(text='🖥 Рассчитать стоимость заказа', callback_data='calculate_cost_order')

    return builder.adjust(1).as_markup()

def faq_fulfillment():
    builder = InlineKeyboardBuilder()
    for question in questions.keys():
        builder.button(text=question, callback_data=question)
    builder.button(text='🔙 Главное меню', callback_data='start_menu')

    return builder.adjust(1).as_markup()


def order_fulfillment():
    builder = InlineKeyboardBuilder()

    builder.button(text='Срочный выкуп (в течении дня)', callback_data=callbackdata.StepOne(buyout=1))
    builder.button(text='Не срочно, главное подешевле (3-4 дня)', callback_data=callbackdata.StepOne(buyout=2))
    builder.button(text='Оплата криптовалютой (1-2 дня)', callback_data=callbackdata.StepOne(buyout=3))
    builder.button(text='🔙 Главное меню', callback_data='start_menu')

    return builder.adjust(1).as_markup()


def select_product_category(buyout):
    builder = InlineKeyboardBuilder()

    builder.button(text='Обувь/Верхняя одежда', callback_data=callbackdata.StepTwo(buyout=buyout, category=1001))
    builder.button(text='Толстовки/Штаны', callback_data=callbackdata.StepTwo(buyout=buyout, category=1002))
    builder.button(text='Футболки/Шорты', callback_data=callbackdata.StepTwo(buyout=buyout, category=1003))
    builder.button(text='Носки/Нижнее белье', callback_data=callbackdata.StepTwo(buyout=buyout, category=1004))
    builder.button(text='Ввести свой вес', callback_data=callbackdata.StepTwo(buyout=buyout, category=5))
    builder.button(text='🔙 Главное меню', callback_data='start_menu')

    return builder.adjust(1).as_markup()


def currency_product(buyout, category):
    builder = InlineKeyboardBuilder()

    builder.button(text='Американский доллар', callback_data=callbackdata.StepThree(buyout=buyout, category=category, currency=1))
    builder.button(text='Евро', callback_data=callbackdata.StepThree(buyout=buyout, category=category, currency=2))
    builder.button(text='Английский фунт стерлингов', callback_data=callbackdata.StepThree(buyout=buyout, category=category, currency=3))
    builder.button(text='Юань', callback_data=callbackdata.StepThree(buyout=buyout, category=category, currency=4))
    builder.button(text='🔙 Главное меню', callback_data='start_menu')

    return builder.adjust(1).as_markup()


def start_menu_return():
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Главное меню', callback_data='start_menu')

    return builder.adjust(1).as_markup()

def faq_menu_return():
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Вопросы', callback_data='get_faq')

    return builder.adjust(1).as_markup()

def get_manager():
    builder = InlineKeyboardBuilder()

#Могло перенестись криво

    builder.button(text='👩‍💻  Связь с менеджером', url=config.URL_MANAGER)
    builder.button(text='🔙 Главное меню', callback_data='start_menu')

    return builder.adjust(1).as_markup()

questions = {
    "Вопрос 1": "Ответ на вопрос 1.",
    "Вопрос 2": "Ответ на вопрос 2.",
    "Вопрос 3": "Ответ на вопрос 3.",
    # Добавьте остальные вопросы
}