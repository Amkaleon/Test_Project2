import json
import os

import psycopg2
from psycopg2 import Error

connection = None
try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        database=os.getenv("DATABASE_NAME"))

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # SQL-запрос для создания новой таблицы
    create_table_query = """
        CREATE TABLE IF NOT EXISTS Product (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        price_sale REAL,
        description TEXT,
        code INT NOT NULL,
        images JSONB,
        comment_count INT,
        rating REAL, 
        brand VARCHAR(255),
        categories VARCHAR(255),
        content_url TEXT
    );
    """

    # Выполнение команды: это создает новую таблицу
    cursor.execute(create_table_query)
    connection.commit()
except (Exception, Error) as error:
    print('[!] Ошибка подключения к базе данных')

finally:
    if connection:
        cursor.close()
        connection.close()


# Функция подключения к базе данных
def connect_to_db():
    try:
        # Подключение к существующей базе данных

        connection = psycopg2.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"))
        return connection

    except (Exception, Error) as error:
        return None


# Функция для записи значений в таблицу DetMir
def insert_data_list(connection, name, price, price_sale, description, code,
                     images, comment_count, rating, brand, categories, content_url):
    try:
        cursor = connection.cursor()
        images_str = json.dumps(images)

        insert_query = """
        INSERT INTO Product (name, price, price_sale, description, code,
        images, comment_count, rating, brand, categories, content_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (name, price, price_sale, description, code,
                                      images_str, comment_count, rating, brand, categories, content_url))
        connection.commit()
        print(f'[+] Данные успешно записаны в таблицу Product')

    except (Exception, Error) as error:
        print(f'Ошибка записи в базу данных: {error}')
    finally:
        if cursor:
            cursor.close()
