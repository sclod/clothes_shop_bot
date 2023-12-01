import telebot
from db.db import *  # Импортируем класс Databases из файла databases.py

bot = telebot.TeleBot("6554414994:AAFtE-6SjsU3brsibCTBACliOowcdIMfG3M",parse_mode='HTML')

db = Databases("database.db")
db.connect()
db.create_table_headdress()
db.create_table_outerwear()
db.create_table_underwear()
db.create_table_shoes()
db.create_table_accessories()
db.create_table_accessories()
db.create_table_users()
db.create_table_basket()
