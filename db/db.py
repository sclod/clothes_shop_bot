import sqlite3



class Databases():
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None
        self.cursor = None

    # Конектимся к базе
    def connect(self):
        self.db = sqlite3.connect(self.db_name)
        self.cursor = self.db.cursor()

    # Создаём таблицу пользователей
    def create_table_users(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                status TEXT,
                basket_id,
                FOREIGN KEY (basket_id) REFERENCES basket(id)
            )
        ''')
        self.db.commit()

    # Создаём таблицу головного убора
    def create_table_headdress(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS headdress (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                image_url TEXT
            )
        ''')
        self.db.commit()

    # Создаём таблицу верхней одежды
    def create_table_outerwear(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS outerwear (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                image_url TEXT
            )
        ''')
        self.db.commit()

    # Создаём таблицу нижней одежды
    def create_table_underwear(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS underwear (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                image_url TEXT
            )
        ''')
        self.db.commit()

    # Создаём таблицу обуви
    def create_table_shoes(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shoes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                image_url TEXT
            )
        ''')
        self.db.commit()

    # Создаём таблицу аксессуаров
    def create_table_accessories(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                image_url TEXT
            )
        ''')
        self.db.commit()

    # Создаём таблицу нового поступления
    def create_table_accessories(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS new (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                image_url TEXT
            )
        ''')
        self.db.commit()

    # Создаём таблицу корзины
    def create_table_basket(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS basket (
                id INTEGER PRIMARY KEY,
                image TEXT,
                id_users INTEGER,
                FOREIGN KEY (id_users) REFERENCES users(id)
            )
        ''')
        self.db.commit()


    # Функции проверки и добавления пользователя в бд
    # <!---------------------------------------------------------------------------------------------------
    # Добавляем пользователя в таблицу users
    def add_user_to_db(self, user_id, user_name, status):
        self.cursor.execute("INSERT INTO users (id, name, status) VALUES (?, ?, ?)", (user_id, user_name, status))
        self.db.commit()

    # Проверка существования пользователя
    def user_exists(self, user_id):
        self.cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
        result = self.cursor.fetchone()
        return result 

    # Проверка статуса пользователя
    def get_user_status(self, user_id):
        self.cursor.execute('SELECT status FROM users WHERE id = ?', (user_id,))
        status = self.cursor.fetchone()
        if status and status[0] == 'admin':
            return status[0]
        return user_id

    # Получаем логин(собаку) пользователя
    def get_login_user(self, id):
        result = self.cursor.execute('SELECT name FROM users WHERE id = ?', (id,)).fetchall()[0]
        return result

    # Получаем общее количество пользователей в бд
    def get_all_count_users(self):
        result = self.cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        return result
    
    # Получаем все логины пользователей в бд
    def get_all_id(self):
        result = self.cursor.execute('SELECT id FROM users').fetchall()[0]
        return result

    # <!---------------------------------------------------------------------------------------------------
    # Возвращаем общее количество товаров по id пользователя
    def get_all_count_basket(self, id_users):
        result = self.cursor.execute('SELECT COUNT(*) FROM basket WHERE id_users = ?', (id_users,)).fetchone()[0]
        return result

    # Возвращаем все товары  в корзине по id пользователя
    def fetch_basket_items(self, user_id):
        products = self.cursor.execute('SELECT id, image FROM basket WHERE id_users = ?', (user_id,)).fetchall()
        return products
    
    # Возвращаем id товара в корзине
    def get_id(self, user_id):
        id = self.cursor.execute('SELECT id FROM basket WHERE id_users = ?', (user_id,)).fetchall()
        return id
    
    # Возвращаем id товара с корзины по id пользователя
    def get_product_id_in_basket(self, id_users):
        id_product = self.cursor.execute('SELECT id FROM basket WHERE id_users = ?', (id_users,)).fetchall()
        return id_product
    
    # Удаляем товар из корзины по id пользователя
    def delete_product_basket(self, id, id_users):
        try:
            self.cursor.execute('DELETE FROM basket WHERE id = ? AND id_users = ?', (id, id_users))
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            print(f"Ошибка при удалении товара из корзины: {e}")

    # Получаем все товары по id пользователя 
    def get_items_in_basket(self, user_id):
        self.cursor.execute('''
            SELECT * FROM basket
            WHERE id_users = ?
            ORDER BY id
        ''', (user_id,))
        items = self.cursor.fetchall()
        return items

    # <!---------------------------------------------------------------------------------------------------
    # Добавление товара в бд
    def insert_clothes(self, name, price, descr, image_url, table_name):
        self.cursor.execute(f"INSERT INTO {table_name} (name, price, descr, image_url) VALUES (?, ?, ?, ?)", (name, price, descr, image_url))
        self.db.commit()

    # <!---------------------------------------------------------------------------------------------------
    # Возвращаем одежду из переданной колонки в бд
    def fetch_types_clothes(self, name_column):
        self.cursor.execute(f'SELECT id, name, price, descr, image_url FROM {name_column}')
        return self.cursor.fetchall()

    # Возвращаем всю одежду с переданной категории одежды и id
    def fetch_types_clothes_by_id(self, name_column,id):
        self.cursor.execute(f'SELECT id, name, price, descr, image_url FROM {name_column} WHERE id = {id}')
        return self.cursor.fetchall()
    
    # Делаем проверку на уникальность в корзине пользователя
    def is_product_in_basket(self, user_id, product_image):
        self.cursor.execute('SELECT id FROM basket WHERE id_users = ? AND image = ?', (user_id, product_image))
        result = self.cursor.fetchone()
        return result is not None
    
    # Возвращаем названия всех категорий
    def fetch_categories(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") 
        categories = self.cursor.fetchall()
        return categories
    
    # Изменяем информацию о товаре
    def edit_one_order(self,id,table,info,value):
        self.cursor.execute(f'UPDATE {table} SET {value} = "{info}" WHERE id = {id}')
        self.db.commit()

    # Проверяем есть ли товары в переданной категории одежды
    def fetch_id_in_db(self,table):
        result = self.cursor.execute(f'SELECT * FROM {table}').fetchall()
        if result:
            return result  
    
    # Возвращаем общее количество товаров в таблице
    def get_all_count(self,table):
        result = self.cursor.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        return result

    # <!---------------------------------------------------------------------------------------------------
    # Добавляем товар в корзину
    def add_to_basket(self, user_id, product_image):
        try:
            self.cursor.execute("INSERT INTO basket (image, id_users) VALUES (?, ?)", (product_image, user_id))
            self.db.commit()
            return True
        except sqlite3.Error:
            self.db.rollback()
            return False

    # <!---------------------------------------------------------------------------------------------------
    # Общие функции
    # Удаление товара в бд по ID
    def delete_product(self, product_id, name_column):
        query = f'DELETE FROM {name_column} WHERE id = ?'
        self.cursor.execute(query, (product_id,))
        self.db.commit()

    # Закрываем подключение к базе
    def close(self):
        self.cursor.close()
        self.db.close()