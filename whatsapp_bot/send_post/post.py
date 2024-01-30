import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from parser_rss import get_rss_news


RSS_URL = 'https://static.primamedia.ru/export/new/news_main_WhatsApp_43.rss'
group_name = 'Ватсап бот'
message = get_rss_news(RSS_URL)['link']
title = get_rss_news(RSS_URL)['title']
image = get_rss_news(RSS_URL)['links'][1]['href']


class Whatapp():
    """Класс бота для Whatsapp"""

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(r'user-data-dir=/Users/romanbespalov/Dev/whatsapp_bot/whatsapp_bot/send_post/test')
        options.add_argument('--profile-directory=Profile Roman')
        options.add_argument('--profiling-flush=n')
        options.add_argument('--enable-aggressive-domstorage-flushing')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 60)

    def send_message(self, message):
        """Функция отправки новостей в группы."""
        url = 'https://web.whatsapp.com/'
        self.driver.get(url)

        # ожидания появления блока настройки на странице(3 точки)
        element_xpath = '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span'
        self.wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))

        # поиск и выбор группы через поле поиска
        search_input = self.driver.find_element('xpath', '//div[@contenteditable="true"][@data-tab="3"]')
        search_input.send_keys(group_name)
        search_input.send_keys(Keys.RETURN)

        # Ищем поле ввода сообщения и отправляем сообщение
        message_input = self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]')
        message_input.send_keys(message)
        time.sleep(5)
        message_input.send_keys(Keys.RETURN)
        time.sleep(5)

    def finish(self):
        """Функция выхода из браузера."""
        self.driver.quit()


def main():
    wa = Whatapp()
    try:
        wa.send_message(message)
    except KeyboardInterrupt:
        wa.finish()


if __name__ == "__main__":
    main()
