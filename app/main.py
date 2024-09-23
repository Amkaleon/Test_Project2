import json

from services.webdriver_init import get_data_from_api
from services.extract_product_info import extract_product_info


def main():
    url = 'https://www.perekrestok.ru/cat/197/p/pecene-ubilejnoe-vitaminizirovannoe-s-glazuru-232g-4027703'

    # Инициализация браузера, чтобы взять ключ аутентификации.
    # Затем собираем данные товара.
    data = get_data_from_api(url)

    # content - главный ключ, который содержит словарь
    # с данными о продукте
    content = data.get('content')
    if content:
        product_info = extract_product_info(content, url)

        with open('../product.json', 'w', encoding='UTF-8') as json_file:
            json.dump(product_info, json_file, indent=4, ensure_ascii=False)
            print("[+] Данные успешно записаны в файл product.json")
    else:
        print("[!] Ключ 'content' отсутствует")


if __name__ == '__main__':
    main()
