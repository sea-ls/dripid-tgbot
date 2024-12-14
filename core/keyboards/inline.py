from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from core.utils import callbackdata

def start_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text='🔍 Отследить заказ', callback_data='get_order_status')
    builder.button(text='📇 Ответы на популярные вопросы', callback_data='get_faq')
    builder.button(text='✏ Отзывы', url=config.URL_REVIEWS)
    builder.button(text='👩‍💻 Связь с менеджером', url=config.URL_MANAGER)
    builder.button(text='🖥 Рассчитать стоимость заказа', callback_data='calculate_cost_order')

    return builder.adjust(1).as_markup()

def faq_fulfillment():
    builder = InlineKeyboardBuilder()
    for question in questions.keys():
        builder.button(text=question, callback_data=question)
    builder.button(text='Не нашел свой вопрос', url=config.URL_MANAGER)
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
    "1. Как оформить заказ?": """Оформить заказ через [Drip ID](https://t.me/Drip_ID0) очень просто — давайте разберемся как это сделать

1️⃣Заходим на сайт, от куда вы хотите сделать заказ\. Выбираете понравившуюся позицию, копируете на неё ссылку, указываете нужный вам размер и отправляете информацию менеджеру @dripid

2️⃣Менеджер расчитывает заказ с учетом доставки до РФ и сообщает вам итоговую стоимость

3️⃣Далее от вас потребуется оплатить заказ \(мы подскажем, как это сделать\), и после оплаты заказ будет выкуплен

4️⃣ Заказ оформлен""",

    "2. Что можете доставить?": """Мы доставляем все типы товаров, которые не запрещены к ввозу в РФ, в том числе категории товаров, входящие в санкционные списке США и ЕС""",

    "3. Какую комиссию берете?": """За услугу выкупа мы берём комиссию:
1000₽ — для заказов до 5000₽
1500₽ — для заказов до 15000₽
10% от стоимости — для заказов свыше 15000₽""",

    "4. Сколько стоит доставка?": """Цена доставки напрямую зависит от страны, из которой мы выкупаем и доставляем заказ, от веса и габаритов посылки\.

🇺🇸 Из США🇺🇸 
23$/кг \(в среднем 25—30 рабочих дней без учета задержек на таможне\)

🇪🇺 Из Европы🇪🇺 
18€/кг \(в среднем 25 рабочих дней без учета задержек на таможне\)

🇨🇳 Из Китая🇨🇳 
Стандартная доставка — 8$/кг \(в среднем 25 рабочих дней без учета задержек на таможне\)
Экспресс доставка — 30$/кг \(в среднем 1—2 рабочих дня после принятия груза на авиарейс\)

🇹🇷Из Турции🇹🇷 
12$/кг \(в среднем 25 рабочих дней без учета задержек на таможне\)

🇬🇧 Из Англии🇬🇧 
23$/кг \(в среднем 25—30 рабочих дней без учета задержек на таможне\)

🇰🇿Из Казахстана🇰🇿
8$/кг \(10—14 рабочих дней\)""",

    "5. Какой срок доставки?": """🇺🇸 Из США🇺🇸 
в среднем 25—30 рабочих дней без учета задержек на таможне

🇪🇺 Из Европы🇪🇺 
в среднем 25 рабочих дней без учета задержек на таможне

🇨🇳 Из Китая🇨🇳 
Стандартная доставка —  в среднем 25 рабочих дней без учета задержек на таможне
Экспресс доставка — в среднем 1—2 рабочих дня после принятия груза на авиарейс

🇹🇷Из Турции🇹🇷 
в среднем 25 рабочих дней без учета задержек на таможне

🇬🇧 Из Англии🇬🇧 
в среднем 25—30 рабочих дней без учета задержек на таможне

🇰🇿Из Казахстана🇰🇿
10—14 рабочих дней""",

"6. Какой курс валют?": """Актуальный курс валют вы можете увидеть, если сделаете расчёт своего заказа через нашего бота \(а собственно вы в нем и находитесь, так что жмите сюда\) \(добавить кнопку чтобы перекидовало на расчет\)""",

"7. Как отследить заказ?": """После оформления заказа менеджер предоставит вам трек номер, а статус по нему можно отследить, нажав сюда"""

}