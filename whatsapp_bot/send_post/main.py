from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
from parser_rss import get_rss_news, RSS_URL
from selenium.webdriver.common.keys import Keys

image = get_rss_news(RSS_URL)['links'][1]['href']
message = get_rss_news(RSS_URL).link
NUMBER = "+79959820234"


class Whatapp():
    """Класс бота для Whatsapp"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(r'user-data-dir=/Users/romanbespalov/Dev/base_whatsapp_bot/test')
        options.add_argument('--profile-directory=Profile Roman')
        options.add_argument('--profiling-flush=n')
        options.add_argument('--enable-aggressive-domstorage-flushing')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 60)

    def send_message(self, message):
        url = f"https://web.whatsapp.com/send?phone={NUMBER}&text={message}"
        self.driver.get(url)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
        button = self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
        time.sleep(10)
        button.click()
        time.sleep(10)

    def finish(self):
        self.driver.quit()


def main():
    wa = Whatapp()
    try:
        wa.send_message(message)
    except KeyboardInterrupt:
        wa.finish()


if __name__ == "__main__":
    main()


# def check_for_updates():
#     old_news = get_rss_entries(RSS_URL).title
#     while True:
#         time.sleep(60)
#         new_news = get_rss_entries(RSS_URL).title
#         if old_news != new_news:
#             old_news = new_news
#             main()


# check_for_updates()


# Код для создания нового профиля (После создания связи нельзя разлинковывать связь на мобилке)

# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from time import sleep

# options = webdriver.ChromeOptions()
# options.add_argument('--allow-profiles-outside-user-dir')
# options.add_argument('--enable-profile-shortcut-manager')
# options.add_argument(r'user-data-dir=/Users/romanbespalov/Dev/base_whatsapp_bot/test')  # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
# options.add_argument('--profile-directory=Profile Roman')
# options.add_argument('--profiling-flush=n')
# options.add_argument('--enable-aggressive-domstorage-flushing')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# url = "https://web.whatsapp.com/"
# driver.get(url)
# sleep(90)
