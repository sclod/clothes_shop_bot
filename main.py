from telebot import types
from db.db import *
from admin import *
from bot_shared import bot
import ast


@bot.message_handler(commands=['start'])
def start(message):
    try:
        db = Databases("database.db")
        db.connect()
        db.create_table_users()
        if not db.user_exists(message.from_user.id):
            db.add_user_to_db(message.from_user.id, message.from_user.username, 'user')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("🔰 Головне меню")
            button2 = types.KeyboardButton("❓ FAQ")
            button3 = types.KeyboardButton("🛍 Кошик")
            keyboard.add(button1, button2)
            keyboard.add(button3)
            bot.send_message(message.from_user.id, text='Вітаю вас у моєму магазині, У мене багато одягу на будь-який смак!', reply_markup=keyboard)
        else:
            main_menu_buttons = types.InlineKeyboardMarkup(row_width=2)
            menu_button = types.InlineKeyboardButton(text='®️ Одяг', callback_data='all_clothes')
            menu_button1 = types.InlineKeyboardButton(text='©️ Аксесуари', callback_data='clothes_access')
            menu_new = types.InlineKeyboardButton(text='🔥 Нове постачання 🔥', callback_data='new_clothes')
            menu_button2 = types.InlineKeyboardButton(text='🛍 Кошик', callback_data='basket')
            menu_button3 = types.InlineKeyboardButton(text='⌨️ Підтримка', callback_data='help')
            main_menu_buttons.add(menu_button, menu_button1)
            main_menu_buttons.add(menu_new)
            main_menu_buttons.add(menu_button2, menu_button3)
            bot.send_message(message.chat.id, text=
                            f'⏳  Работаем с 10:00 до 23.00:\n'
                            , reply_markup=main_menu_buttons)
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda message: message.text == "🔰 Головне меню")
def main_menu(message):
    start(message)


@bot.message_handler(func=lambda message: message.text == "❓ FAQ")
def FAQ_descr(message):
    bot.send_message(message.chat.id, text='Тут буде опис доставки, ціни, популярні питання крч!')


@bot.message_handler(func=lambda message: message.text == "🛍 Кошик")
def basket(message):
    try:
        db = Databases("database.db")
        db.connect()

        user_id = message.chat.id
        basket_items = db.fetch_basket_items(user_id)
        count = db.get_all_count_basket(user_id)
        list_dasdasd = db.get_id(user_id)
        listok = []

        for item in list_dasdasd:
            listok.append(item[0])  # Добавляем первый элемент кортежа в список
        print(basket_items)
        if basket_items:
            number_id = 0
            id, image = basket_items[number_id]
            current_id = number_id

            markup_order = types.InlineKeyboardMarkup()
            prev = types.InlineKeyboardButton(text='<', callback_data=f'prev_{number_id}_{listok}')
            button = types.InlineKeyboardButton(text=f' {number_id + 1} / {count}', callback_data='b')
            next_product = types.InlineKeyboardButton(text='>', callback_data=f'next_{number_id}_{listok}')
            send_BOG = types.InlineKeyboardButton(text='Створити замовлення', callback_data=f'sendbog_{image}')
            deletebuttons = types.InlineKeyboardButton(text='❌', callback_data=f'delete2_{current_id}_{listok}')
            back1 = types.InlineKeyboardButton(text='Назад', callback_data='back1')
            markup_order.add(prev, button, next_product, back1, send_BOG, deletebuttons)
            bot.send_message(message.chat.id, text=f'Кошик:\n{image}', reply_markup=markup_order, disable_web_page_preview=False)
        else:
            start(message)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        db = Databases("database.db")
        db.connect()
        req = call.data.split('_')
        if call.data == 'all_clothes':
            clothes_menu_buttons = types.InlineKeyboardMarkup(row_width=1)
            clothes_menu_buttons1 = types.InlineKeyboardButton(text='🧢 Головний убір', callback_data='clothes_headdress')
            clothes_menu_buttons2 = types.InlineKeyboardButton(text='👕 Верхній одяг', callback_data='clothes_outerwear')
            clothes_menu_buttons3 = types.InlineKeyboardButton(text='👖 Нижній одяг', callback_data='clothes_underwear')
            clothes_menu_buttons4 = types.InlineKeyboardButton(text='👟 Взуття', callback_data='clothes_shoes')
            clothes_menu_buttons5 = types.InlineKeyboardButton(text='🔙 Назад', callback_data='back1')
            clothes_menu_buttons.add(clothes_menu_buttons1, clothes_menu_buttons2, clothes_menu_buttons3, clothes_menu_buttons4, clothes_menu_buttons5)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='📌 Выбирите категорию одежды 📌', reply_markup=clothes_menu_buttons)       
    except Exception as e:
        print(e)

    # Меню поддержки
    if call.data == 'help':
        try:
            help_buttons = types.InlineKeyboardMarkup(row_width=1)
            help_button1 = types.InlineKeyboardButton(text='🔗Зв\'язатись з продавцем🔗', url='https://t.me/hatredmark')
            help_button2 = types.InlineKeyboardButton(text='🔗Посилання на інстаграм🔗', url='https://www.instagram.com/hatredmarket/')
            help_button3 = types.InlineKeyboardButton(text='🔙Назад', callback_data='back1')
            help_buttons.add(help_button1, help_button2, help_button3)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='♿️Поддержка♿️', reply_markup=help_buttons)
        except Exception as e:
            print(e)

    # Выборка категории одежды
    if req[0] == 'clothes':
        try:
            types_clothes = req[1]
            if types_clothes == 'headdress' or 'outerwear' or 'underwear' or 'shoes' or 'access':
                by_one_id = db.fetch_types_clothes_by_id(types_clothes,1)
                all_count = db.get_all_count(types_clothes)
                if by_one_id:
                    markup_order = types.InlineKeyboardMarkup()
                    current_product = by_one_id[0]
                    id, name, price, discr, img = current_product
                    button = types.InlineKeyboardButton(text=f'{id} / {all_count}', callback_data='b')
                    next = types.InlineKeyboardButton(text=f'>', callback_data=f'right_{id+1}_{types_clothes}')
                    back = types.InlineKeyboardButton(text=f'<', callback_data=f'left_{id-1}_{types_clothes}')
                    
                    markup_order.row(back,button,next)
                    button_busket = types.InlineKeyboardButton(text = '🛍 В кошик', callback_data=f'inbasket_{id}_{img}')
                    if types_clothes == 'access':
                        back = types.InlineKeyboardButton(text = '🔚Назад', callback_data='back1')
                    else:
                        back = types.InlineKeyboardButton(text = '🔚Назад', callback_data='all_clothes')
                    markup_order.row(button_busket, back)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=
                                            f'Название товара: {name}\n'+
                                            f'Цена: {price}$\n'+
                                            f'Описание: {discr}\n'+
                                            f'<a href="{img}">&#8205;</a>'
                                            ,reply_markup=markup_order,disable_web_page_preview=False)
                    
                    
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text="У даній категорії немає товарів.")
        except Exception as e:
            print(e)

    # Нажатия кнопки вправо
    if req[0] == 'right':
        try:
            next_id = req[1]
            types_clothes = req[2]
            by_one_id = db.fetch_types_clothes_by_id(types_clothes,next_id)
            all_count = db.get_all_count(types_clothes)
            if by_one_id:
                    markup_order = types.InlineKeyboardMarkup()
                    current_product = by_one_id[0]
                    id, name, price, discr, img = current_product
                    button = types.InlineKeyboardButton(text=f'{id} / {all_count}', callback_data='b')
                    next = types.InlineKeyboardButton(text=f'>', callback_data=f'right_{id+1}_{types_clothes}')
                    back = types.InlineKeyboardButton(text=f'<', callback_data=f'left_{id-1}_{types_clothes}')
                    markup_order.row(back,button,next)

                    button_busket = types.InlineKeyboardButton(text = '🛍 В кошик', callback_data=f'inbasket_{id}_{img}')
                    back = types.InlineKeyboardButton(text = '🔚Назад', callback_data='all_clothes')
                    markup_order.row(button_busket, back)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=
                                            f'Назва товару: {name}\n'+
                                            f'Ціна: {price}$\n'+
                                            f'Опис: {discr}\n'+
                                            f'<a href="{img}">&#8205;</a>'
                                            ,reply_markup=markup_order,disable_web_page_preview=False)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше немає!')
        except Exception as e:
            print(e)

    # Нажатия кнопки влево
    if req[0] == 'left':
        try:
            next_id = req[1]
            types_clothes = req[2]
            by_one_id = db.fetch_types_clothes_by_id(types_clothes, next_id)
            all_count = db.get_all_count(types_clothes)
            if by_one_id:
                    markup_order = types.InlineKeyboardMarkup()
                    current_product = by_one_id[0]
                    id, name, price, discr, img = current_product
                    button = types.InlineKeyboardButton(text=f'{id} / {all_count}', callback_data='b')
                    next = types.InlineKeyboardButton(text=f'>', callback_data=f'right_{id+1}_{types_clothes}')
                    back = types.InlineKeyboardButton(text=f'<', callback_data=f'left_{id-1}_{types_clothes}')
                    markup_order.row(back,button,next)

                    button_busket = types.InlineKeyboardButton(text = '🛍 В кошик', callback_data=f'inbasket_{id}_{img}')
                    back = types.InlineKeyboardButton(text = '🔚Назад', callback_data='all_clothes')
                    markup_order.row(button_busket, back)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=
                                            f'Назва товару: {name}\n'+
                                            f'Ціна: {price}$\n'+
                                            f'Опис: {discr}\n'+
                                            f'<a href="{img}">&#8205;</a>'
                                            ,reply_markup=markup_order,disable_web_page_preview=False)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше немає!')
        except Exception as e:
            print(e)

    # Меню новых поставок
    if req[0] == 'new':
        try:
            name_table = req[0]
            all_new_clothes = db.fetch_types_clothes(name_table)
            all_count = db.get_all_count(name_table)
            if all_new_clothes:
                current_product = all_new_clothes[0]
                id, name, price, discr, img = current_product
                print(id, name, price, discr, img)
                new_clothes_buttons = types.InlineKeyboardMarkup()
                new_clothes_button = types.InlineKeyboardButton(text=f'{id} / {all_count}', callback_data='b')
                new_clothes_next = types.InlineKeyboardButton(text=f'>', callback_data=f'right_{id+1}_{name_table}')
                new_clothes_back = types.InlineKeyboardButton(text=f'<', callback_data=f'left_{id-1}_{name_table}')
                new_clothes_buttons.row(new_clothes_back, new_clothes_button, new_clothes_next)
                button_busket = types.InlineKeyboardButton(text = '🛍 В кошик', callback_data=f'inbasket_{id}_{img}')
                back = types.InlineKeyboardButton(text = '🔚Назад', callback_data='all_clothes')
                new_clothes_buttons.row(button_busket, back)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=
                                            f'Назва товару: {name}\n'+
                                            f'Ціна: {price}$\n'+
                                            f'Опис: {discr}\n'+
                                            f'<a href="{img}">&#8205;</a>'
                                            ,reply_markup=new_clothes_buttons,disable_web_page_preview=False)
        except Exception as e:
            print(e)


    # Меню добавления продукта в бд (adminka)
    if call.data == 'add-product-menu':
        try:
            add_buttons = types.InlineKeyboardMarkup(row_width=1)
            buttonadd = types.InlineKeyboardButton(text='🧢 Головний убір', callback_data=f'add_headdress')
            button1add = types.InlineKeyboardButton(text='👕 Верхній одяг', callback_data=f'add_outerwear')
            button2add = types.InlineKeyboardButton(text='👖 Нижній одяг', callback_data=f'add_underwear')
            button3add = types.InlineKeyboardButton(text='👟 Взуття', callback_data=f'add_shoes')
            button4add = types.InlineKeyboardButton(text='🪬 Аксессуары', callback_data=f'add_accessories')
            button5add = types.InlineKeyboardButton(text='🔥 Нові поставки ', callback_data=f'add_new')
            button6add = types.InlineKeyboardButton(text='🔙 Назад', callback_data=f'back-admin')
            add_buttons.add(buttonadd, button1add, button2add, button3add, button4add, button5add, button6add)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='♿️Выбирите какой товар хотите добавить♿️', reply_markup=add_buttons)
        except Exception as e:
            print(e)

    # Меню изменения продукта (adminka)
    if call.data == 'edit-product-menu':
        try:
            edit_buttons = types.InlineKeyboardMarkup(row_width=1)
            buttonedit = types.InlineKeyboardButton(text='🧢 Головний убір', callback_data=f'editmenu_headdress')
            button1edit = types.InlineKeyboardButton(text='👕 Верхній одяг', callback_data=f'editmenu_outerwear')
            button2edit = types.InlineKeyboardButton(text='👖 Нижній одяг', callback_data=f'editmenu_underwear')
            button3edit = types.InlineKeyboardButton(text='👟 Взуття', callback_data=f'editmenu_shoes')
            button4edit = types.InlineKeyboardButton(text='🪬 Аксессуары', callback_data=f'editmenu_accessories')
            button5edit = types.InlineKeyboardButton(text='🔥 Нові поставки ', callback_data=f'editmenu_new')
            button6edit = types.InlineKeyboardButton(text='🔙 Назад', callback_data=f'back-admin')
            edit_buttons.add(buttonedit, button1edit, button2edit, button3edit, button4edit, button5edit, button6edit)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='♿️Выбирите какой товар хотите редактировать♿️', reply_markup=edit_buttons)
        except Exception as e:
            print(e)

    # Меню товаров категории (adminka)
    if req[0] == 'editmenu':
        try:
            type_clothes = req[1]
            result = db.fetch_id_in_db(table=type_clothes)
            if result == None:
                bot.send_message(call.from_user.id, text='❕Немає товарів у цій категорії❕')
            else:
                markup = types.InlineKeyboardMarkup(row_width=2)
                for i in result:
                    id = i[0]
                    name = i[1]
                    button = types.InlineKeyboardButton(text = f'{name}', callback_data=f'edit-one_{id}_{type_clothes}')
                    button_delete = types.InlineKeyboardButton(text='❌', callback_data=f'delete-button_{id}_{type_clothes}')
                    button_back = types.InlineKeyboardButton(text='🔙 Назад', callback_data=f'edit-product-menu')
                    markup.add(button, button_delete)
                markup.add(button_back)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='♿️Что хочешь изменить:♿️', reply_markup=markup)
        except Exception as e:
            print(e)

    # Меню изменения параметров товара (adminka)
    if req[0] == 'edit-one':
        try:
            id = req[1]
            table = req[2]
            edit_buttons = types.InlineKeyboardMarkup()
            edit_button1 = types.InlineKeyboardButton(text='Изменить фото', callback_data=f'edit-order_photo_{id}_{table}')
            edit_button2 = types.InlineKeyboardButton(text='Изменить имя', callback_data=f'edit-order_name_{id}_{table}')
            edit_button3 = types.InlineKeyboardButton(text='Изменить цену', callback_data=f'edit-order_price_{id}_{table}')
            edit_button4 = types.InlineKeyboardButton(text='Изменить описанние', callback_data=f'edit-order_descr_{id}_{table}')
            edit_button5 = types.InlineKeyboardButton(text='Назад', callback_data=f'editmenu_{table}')
            edit_buttons.add(edit_button1, edit_button2, edit_button3, edit_button4, edit_button5)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f'Выбирите, что хотите изменить:', reply_markup = edit_buttons)
        except Exception as e:
            print(e)

    # Записываем изменения (adminka)
    if req[0] == 'edit-order':
        try:
            filter = req[1]
            id = req[2]
            table = req[3]
            time_text  = ''
            if filter == 'photo':
                time_text  = 'Фото'
            if filter == 'name':
                time_text  = 'Название'
            if filter == 'price':
                time_text  = 'Цена'
            if filter == 'descr':
                time_text  = 'Описание'
            msg = bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'Введите новое значение для: [{time_text}]')
            bot.register_next_step_handler(msg,edit_order,id,table,time_text)
        except Exception as e:
            print(e)

    # Добавления товара в корзину
    if req[0] == 'inbasket':
        try:
            id = req[1]
            img = req[2]
            if db.is_product_in_basket(call.from_user.id, img):
                bot.answer_callback_query(callback_query_id=call.id, text='Уже в корзине!')
            else:
                if db.add_to_basket(call.from_user.id, img):
                    bot.answer_callback_query(callback_query_id=call.id, text='Товар добавлен!')
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Ошибка при добавлении товара в корзину!')
        except Exception as e:
            print(e)

    # Меню корзины пользователя
    if call.data == 'basket':
        try:
            user_id = call.from_user.id
            basket_items = db.fetch_basket_items(user_id)
            count = db.get_all_count_basket(user_id)
            list_dasdasd = db.get_id(user_id)
            
            listok = []
            for item in list_dasdasd:
                listok.append(item[0])  # Добавляем первый элемент кортежа в список

            if basket_items:
                number_id = 0
                id, image = basket_items[number_id]
                current_id = number_id

                markup_order = types.InlineKeyboardMarkup()
                prev = types.InlineKeyboardButton(text='<', callback_data=f'prev_{number_id}_{listok}')
                button = types.InlineKeyboardButton(text=f' {number_id + 1} / {count}', callback_data='b')
                next_product = types.InlineKeyboardButton(text='>', callback_data=f'next_{number_id}_{listok}')
                send_BOG = types.InlineKeyboardButton(text='Створити замовлення', callback_data=f'sendbog_{image}')
                deletebuttons = types.InlineKeyboardButton(text='❌', callback_data=f'delete2_{current_id}_{listok}')
                back1 = types.InlineKeyboardButton(text='Назад', callback_data='back1')
                markup_order.add(prev, button, next_product, back1, send_BOG, deletebuttons)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'Корзина:\n{image}', reply_markup=markup_order, disable_web_page_preview=False)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Корзина пуста!')
        except Exception as e:
            print(e)
    
    # Листание одежды в корзине
    if req[0] == 'prev' or req[0] == 'next':
        try:
            number_id = int(req[1])
            listok = req[2]

            if req[0] == 'prev':
                number_id -= 1
            elif req[0] == 'next':
                number_id += 1

            user_id = call.from_user.id
            basket_items = db.fetch_basket_items(user_id)
            count = db.get_all_count_basket(user_id)

            if 0 <= number_id < len(basket_items):
                id, image = basket_items[number_id]
                markup_order = types.InlineKeyboardMarkup()

                prev = types.InlineKeyboardButton(text='<', callback_data=f'prev_{number_id}_{listok}')
                button = types.InlineKeyboardButton(text=f' {number_id + 1} / {count}', callback_data='b')
                next_product = types.InlineKeyboardButton(text='>', callback_data=f'next_{number_id}_{listok}')
                send_BOG = types.InlineKeyboardButton(text='Створити замовлення', callback_data=f'sendbog_{image}')
                deletebuttons = types.InlineKeyboardButton(text='❌', callback_data=f'delete2_{number_id}_{listok}')
                back1 = types.InlineKeyboardButton(text='Назад', callback_data='back1')

                markup_order.add(prev, button, next_product, back1, send_BOG, deletebuttons)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'Корзина: {image}', reply_markup=markup_order, disable_web_page_preview=False)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше нікуди!')
        except Exception as e:
            print(e)

    # Первая часть добавления товара в бд (adminka)
    if req[0] == 'add':
        try:
            products_info = req[1]
            msg_url = bot.send_message(call.message.chat.id, "Пожалуйста, отправьте фотографию товара.\nВоспользуйтесь ботом: @tlgur_bot")
            bot.register_next_step_handler(msg_url, upload_photo_and_ask_name,products_info)
        except Exception as e:
            print(e)

    # Формирование заказа и отправка админу
    if req[0] == 'sendbog':
        try:
            image_product = req[1]
            username = db.get_login_user(call.from_user.id)
            if username == None:
                bot.send_message(call.from_user.id, text='❗️ В вас немає логіна вашого аккаунта телеграмм, напишіть будь-ласка ваш номер телефона в такому форматі - 🇺🇦0999999999, щоб ми з вами зв\'язалися або напишіть мені ❗️')
                username = call.message.text
                bot.register_next_step_handler(call.message, send_phone_number, image_product)
            else:
                id_product = db.get_product_id_in_basket(call.from_user.id)
                count = db.get_all_count_basket(call.from_user.id)
                bot.answer_callback_query(callback_query_id=call.id, text='Ваше замовлення оформлене!')
                bot.send_message(6198791765, text='------------------------------')
                bot.send_message(6198791765, text=f'Клієнт @{username[0]} створив замовлення!')
                url_buttons = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text='Написать клиенту', url=f'https://t.me/{username[0]}')
                url_buttons.add(url_button)
                for i in id_product:
                    basket_items = db.fetch_basket_items(call.from_user.id)
                    if basket_items:
                        id, image = basket_items[0]
                        bot.send_message(chat_id=6198791765, text=f'Заказ:\n<a href="{image}">&#8205;</a>', reply_markup=url_buttons)
        except Exception as e:
            print(e)

    if call.data == 'send-all-users':
        try:
            all_users = db.get_all_id()
            for user_id in all_users:
                bot.send_message(user_id, text='🔥 Увага! З\'явився новий одяг 🔥')
            bot.send_message(call.from_user.id, text="📬 Рассылка завершена! Новая одежда отправлена всем пользователям.")
        except Exception as e:
            print(e)

    if req[0] == 'delete-button':
        try:
            id = req[1]
            name_table = req[2]
            db.delete_product(id, name_table)
            result = db.fetch_id_in_db(table=name_table)
            if result is None:
                bot.send_message(call.from_user.id, text='❕Немає товарів у цій категорії❕')
                admin(call.message)
            else:
                markup = types.InlineKeyboardMarkup(row_width=2)
                for i in result:
                    id = i[0]
                    name = i[1]
                    button = types.InlineKeyboardButton(text=f'{name}', callback_data=f'edit-one_{id}_{name_table}')
                    button_delete = types.InlineKeyboardButton(text='❌', callback_data=f'delete-button_{id}_{name_table}')
                    button_back = types.InlineKeyboardButton(text='🔙 Назад', callback_data='edit-product-menu')
                    markup.add(button, button_delete)
                markup.add(button_back)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='♿️Что хочешь изменить:♿️', reply_markup=markup)
        except Exception as e:
            print(e)

    # Удаление товара в корзине пользователя
    if req[0] == 'delete2':
        try:
            number_id = int(req[1])
            list_id = req[2]
            basket_items = db.fetch_basket_items(call.from_user.id)
            listok = ast.literal_eval(list_id)
            count = db.get_all_count_basket(call.from_user.id)
            db.delete_product(listok[number_id], 'basket')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            basket(call.message)
        except:
            start(call.message)

    # Возврат в главное меню
    if call.data == 'back1':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    
    # Возврат в главное меню (admin)
    if call.data == 'back-admin':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        admin(call.message)

    db.close()

#<!-----------------------------------------------------------------------------------
# Вторая часть добавления товара в бд
def upload_photo_and_ask_name(message,products_info):
    try:
        msg_url = message.text
        msg_name = bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message_id - 1, text ='Введите название товара')
        bot.register_next_step_handler(msg_name, ask_name_product,msg_url,products_info)
    except Exception as e:
        print(e)

# Записись изменений товара в бд
def edit_order(message,id,table,time_text):
    try:
        db = Databases("database.db")
        db.connect()
        msg = message.text
        value = ''
        if time_text == 'Фото':
            value = 'image_url'
        if time_text == 'Название':
            value = 'name'
        if time_text == 'Цена':
            value = 'price'
        if time_text == 'Описание':
            value = 'descr'
        bot.edit_message_text(chat_id=message.from_user.id,message_id=message.message_id - 1,text = f'Вы изменили значение на: {msg}')
        bot.delete_message(chat_id=message.from_user.id,message_id=message.message_id)
        db.edit_one_order(id = id, table = table,info = msg,value=value)
        admin(message)
        db.close()
    except Exception as e:
        print(e)

# Третья часть добавления товара в бд. Запись названия
def ask_name_product(message, msg_url,products_info):
    try:
        msg_name = message.text
        msg_price = bot.send_message(message.from_user.id, "Введите цену товара.")
        bot.register_next_step_handler(msg_price, ask_price_product, msg_name, msg_url,products_info)
    except Exception as e:
        print(e)

# Четвёртая часть добавления товара. Запись Цены
def ask_price_product(message,msg_url,msg_name,products_info):
    try:
        msg_price = message.text
        msg_discr = bot.send_message(message.from_user.id, "Введите описание товара.")
        bot.register_next_step_handler(msg_discr, ask_description_and_insert_product,msg_url,msg_name,msg_price,products_info)
    except Exception as e:
        print(e)

# Пятая часть добавления, определяем в какую категорию записать товар
def ask_description_and_insert_product(message, msg_url,msg_name,msg_price,products_info):
    try:
        msg_discr = message.text
        db = Databases("database.db")
        db.connect()

        db.insert_clothes(msg_url, msg_price, msg_discr, msg_name, products_info)
        bot.send_message(message.from_user.id, f"Товар успешно добавлен")

        admin(message)
        db.close()
    except Exception as e:
        print(e)

# Отправка номера телефона если нет логина в телеге
def send_phone_number(message, image_product):
    try:
        number = message.text
        bot.send_message(message.chat.id, text='ЗЗамовлення підтверджено, з вами зв\'яжется продавець 💌')
        bot.send_message(6198791765, text=f'🛍 Клієнт +38{number} зробив замовлення 🛍\n{image_product}')
    except:
        bot.send_message(message.chat.id, text='Что-то пошло не так, попробуйте ещё раз👁‍🗨')


# Олдскульная кнопка "Главное меню"
def send_main_menu(message):
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(text='Главное меню')
    main_menu_markup.add(menu_button)
    bot.send_message(message.from_user.id, '', reply_markup=main_menu_markup)
