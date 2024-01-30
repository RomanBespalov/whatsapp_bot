import feedparser
import requests
from PIL import Image
import base64
import io


RSS_URL = 'https://primamedia.ru/export/new/newsByRubric_43_37.rss'


def get_rss_news(RSS_URL):
    feed = feedparser.parse(RSS_URL)
    last_entry = feed.entries
    return last_entry[0]


image_url = get_rss_news(RSS_URL)['links'][1]['href']


def download_and_resize_image(image_url, target_width, target_height):
    # Скачиваем изображение
    response = requests.get(image_url, verify=False)

    if response.status_code == 200:
        try:
            # Открываем изображение с использованием PIL
            original_image = Image.open(io.BytesIO(response.content))

            # Изменяем размер изображения
            resized_image = original_image.resize((target_width, target_height))

            # Преобразуем изображение в байты
            with io.BytesIO() as output_buffer:
                resized_image.save(output_buffer, format="JPEG")
                image_bytes = output_buffer.getvalue()

            # Преобразуем байты в строку base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            return encoded_image

        except Exception as e:
            print(f"Error processing image: {e}")

    else:
        print(f"Failed to download image. Status code: {response.status_code}")


encoded_image = download_and_resize_image(image_url, target_width=135, target_height=90)

print(encoded_image)
