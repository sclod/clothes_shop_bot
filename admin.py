from bot_shared import bot
from db.db import *
from telebot import types


@bot.message_handler(commands=['admin'])
def admin(message):
    db = Databases("database.db")
    db.connect()
    user_status = db.get_user_status(message.chat.id)
    print(user_status)
    if user_status == 'admin':
      count_users = db.get_all_count_users()
      admin_menu = types.InlineKeyboardMarkup(row_width=1)
      admin_button = types.InlineKeyboardButton(text='Редактировать товар', callback_data='edit-product-menu')
      admin_button1 = types.InlineKeyboardButton(text='Добавить товар', callback_data='add-product-menu')
      admin_button2 = types.InlineKeyboardButton(text='Уведомить всех о новом товаре', callback_data='send-all-users')
      admin_menu.add(admin_button, admin_button1, admin_button2)
      bot.send_message(message.chat.id, "<b>💼Панель администратора</b>\n\n"+
                                        f"Количество user - {count_users}"
                                      , parse_mode='HTML', reply_markup=admin_menu)
    else:
        bot.send_message(message.chat.id, "Вы не админ!")\
