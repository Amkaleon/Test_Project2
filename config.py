import os
import requests
from getuseragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

def get_data_from_api(url: str) -> dict:
    code_product = url.split('-')[-1]

    # Получаем путь к папке с вебдрайвером
    driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver', 'chromedriver/chromedriver.exe')

    # Инициализация сервиса для драйвера
    service = Service(driver_path)

    # Инициализация веб-драйвера
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)

        # Обработка запросов
        for request in driver.requests:
            if request.response:  # Проверка наличия ответа
                # Находим файл с продуктом для извлечения токена подключения
                if f'plu{code_product}' in request.url:
                    # Извлекаем токен
                    auth_header = request.headers.get('auth', '')
                    if 'Bearer' in auth_header:
                        token = auth_header.split('Bearer ')[-1]
                    break

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрытие веб-драйвера
        driver.quit()
    # Fake useragent Windows
    useragent = UserAgent("windows+chrome").Random()

    # headers = {"User-Agent": useragent,
    headers = {
        'Authorization':
            f"Bearer {token}",
        'User-Agent': useragent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.perekrestok.ru',
        'Cookie': 'agreements=j:{"isCookieAccepted":true,"isAdultContentEnabled":false,...}',
        'Sec-CH-UA': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"'}

    url_api = f'https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/product/plu{code_product}'

    response = requests.get(url=url_api, headers=headers)

    if response.status_code == 200:
        return response.json()  # Преобразуем ответ в JSON
    else:
        print(f'Ошибка: {response.status_code}')
        return {}
