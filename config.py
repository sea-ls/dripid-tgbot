import os
from get_docker_secret import get_docker_secret

BOT_TOKEN =  get_docker_secret(os.getenv('BOT_TOKEN'), default=os.getenv('BOT_TOKEN'))
DB_NAME = 'base.db'
ADMIN = [6183809792, 1308948539]

# FAQ
URL_FAQ = 'https://teletype.in/@dripid/FAQdripid'
# Как сделать заказ
URL_ORDER = 'https://teletype.in/@dripid/makeanorderdripid'
# Как оплатить заказ
URL_PAYMENT = 'https://teletype.in/@dripid/kEOEfL-fbiO'
# Отзывы
URL_REVIEWS = 'https://t.me/dripidfeedback'
# Связь с менеджером
URL_MANAGER = 'https://t.me/dripID'

# API GOOGLE
API_KEY = get_docker_secret(os.getenv('API_KEY'), default=os.getenv('API_KEY'))
SERVICE = 'api/service.json'
TABLE_ID = get_docker_secret(os.getenv('TABLE_ID'), default=os.getenv('TABLE_ID'))