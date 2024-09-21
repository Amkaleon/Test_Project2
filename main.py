import json

from config import get_data_from_api
from extract_product_info import extract_product_info


def main():
    url = 'https://www.perekrestok.ru/cat/230/p/biotvorog-s-klubnikoj-s-6-mesacev-4-2-zelenaa-linia-100g-4050946'

    data = get_data_from_api(url)

    content = data.get('content')
    if content:
        product_info = extract_product_info(content, url)

        with open('product.json', 'w', encoding='UTF-8') as json_file:
            json.dump(product_info, json_file, indent=4, ensure_ascii=False)
            print("[+] Данные успешно записаны в файл product.json")
    else:
        print("[!] Ключ 'content' отсутствует")


if __name__ == '__main__':
    main()
