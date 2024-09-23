# Перекрёсток Product Scraper

Этот проект собирает данные о товаре с сайта "Перекрёсток" и сохраняет их в файл product.json и в таблицу Product. Для получения ключа аутентификации используется **Selenium**, а для хранения данных – **PostgreSQL** и **json**.

## Структура проекта

- `app/` – содержит основной скрипт и связанные файлы.
  - `main.py` – основной скрипт для запуска скрапера.
  - `services/` - содержит скрипты работы с данными продукта и браузером 
    - `webdriver_init.py` – содержит функцию инициализации браузера и работы с API.
    - `extract_product_info.py` - функция собирает полученную информацию о товаре
  - `database/` - содержит скрипт по работе с базой данных
    - `database.py` - подключение и запись в базу данных
- `chromedriver/` - содержит chromedriver.exe 
- `product.json` - файл с информацией о продукте
- `Dockerfile` – конфигурация для Docker-образа.
- `docker-compose.yml` – конфигурация для управления сервисом PostgreSQL.
- `requirements.txt` – список необходимых Python-библиотек.
- `README.md`

## Предварительные требования

Перед запуском проекта убедитесь, что у вас установлен Docker Desktop:

- [Docker](https://www.docker.com/)

## Настройка проекта

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Amkaleon/Test_Project2.git
   cd Test_Project2
   pip install -r requirements.txt
   ```

2. **Соберите и запустите сервисы:**

   Для сборки и запуска базы данных PostgreSQL и приложения выполните команду:

   ```bash
   docker-compose up --build
   ```
Эта команда соберет и запустит PostgreSQL.

3. **Подключение к PostgreSQL:**

   Вы можете получить доступ к базе данных через следующую команду Docker:

   ```bash
   docker exec -it test_project2-db-1 psql -U postgres -d postgres
   ```

   Также можно подключиться с помощью инструментов, таких как **pgAdmin**, используя следующие параметры:
   - Хост: `localhost`
   - Порт: `5432`
   - База данных: `postgres`
   - Пользователь: `postgres`
   - Пароль: `3225`

## Запуск скрейпера

Скрипт в файле `main.py` выполняет следующие действия:

- Сбор данных о товарах с сайта "Перекрёсток".
- Сохранение данных в таблице `Product` в базе данных PostgreSQL.
- Сохранение данных в файле `product.json`

- В поле **url** можно использовать ссылку на любой товар. 

Для запуска скрейпера:

1. После запуска `docker-compose up --build` станет доступна запись данных в базу PostgreSQL.
   
2. Откройте файл `main.py`, который находится в директории `app/` в интерпретаторе.
   В поле url вставьте ссылку на товар и запустите скрипт.

## Структура базы данных

Таблица `Product` в PostgreSQL имеет следующую структуру:

| Колонка       | Тип        | Описание                              |
|---------------|------------|---------------------------------------|
| `id`          | SERIAL     | Первичный ключ                        |
| `name`        | TEXT       | Название товара                       |
| `price`       | REAL       | Цена товара                           |
| `price_sale`  | REAL       | Цена со скидкой (если есть)           |
| `description` | TEXT       | Описание товара                       |
| `code`        | INT        | Код товара                            |
| `images`      | JSONB      | Список изображений товара в формате JSON|
| `comment_count`| INT       | Количество отзывов                    |
| `rating`      | REAL       | Рейтинг товара                        |
| `brand`       | VARCHAR(255)| Бренд товара                         |
| `categories`  | VARCHAR(255)| Категории товара                      |
| `content_url` | TEXT       | Ссылка на страницу товара             |

