from database.database import connect_to_db, insert_data_list
from psycopg2 import Error


def extract_product_info(content: dict, url: str) -> dict:
    product = {}

    # Собираем название продукта
    title = content.get('title')

    """ Собираем цену и цену без скидки из ключа grossPrice
    И цену со скидкой в ключе price. Если цена без скидки,
    то у price_sale значение None """
    price_tag = content.get('priceTag', {})
    # Приводим в вид, где две цифры после запятой
    if price_tag.get('grossPrice') is not None:
        price = float(price_tag.get('grossPrice')) / 100
        price_sale = float(price_tag.get('price')) / 100
    else:
        price = float(price_tag.get('price')) / 100
        price_sale = None

    # Описание продукта из ключа description
    description = content.get('description', '')

    # Уникальный код товара SKU
    code = content.get('plu', '')

    # Собираем ссылки на фото товара из ключа images,
    # во вложенном ключе cropUrlTemplate
    images = []
    for image in content.get('images'):
        # Без указания размера изображение не находится
        img = image.get('cropUrlTemplate').replace(
            '/%s', '/800x800-fit')
        images.append({"image_url": img})

    # Собираем количество отзывов на товар
    comment_count = content.get('reviewCount', 0)

    # Получаем рейтинг товара.
    # Приводим в вид, где две цифры после запятой
    rating = float(content.get('rating', 0)) / 100

    # Получаем бренд товара. Находится в ключе analyticsInfo
    brand = None
    # Добавляем пустой список, если не будет найден analyticsInfo
    for item in content.get('analyticsInfo', []):
        if item.get('name') == "brandName":
            brand = item.get('value')
            break  # Выходим из цикла, как только нашли бренд

    # Получаем названия категорий, к которому относится продукт
    # в ключе primaryCategory, во вложенном ключе title
    categories = content.get('primaryCategory', {}).get(
        'title', [])

    # Получаем полную ссылку на товар
    content_url = url

    product["name"] = title
    product["price"] = price
    product["price_sale"] = price_sale
    product["description"] = description
    product["code"] = code
    product["images"] = images
    product["comment_count"] = comment_count
    product["rating"] = rating
    product["brand"] = brand
    product["categories"] = categories
    product["content_url"] = content_url

    connection = connect_to_db()

    try:
        if connection:
            insert_data_list(connection, title, price, price_sale, description, code,
                             images, comment_count, rating, brand, categories, content_url)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.close()

    return product
