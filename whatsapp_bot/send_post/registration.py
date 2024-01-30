# Код для создания нового профиля (После создания связи нельзя разлинковывать связь на мобилке)

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(r'user-data-dir=/Users/romanbespalov/Dev/base_whatsapp_bot/test')  # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
options.add_argument('--profile-directory=Profile Roman')
options.add_argument('--profiling-flush=n')
options.add_argument('--enable-aggressive-domstorage-flushing')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://web.whatsapp.com/"
driver.get(url)
sleep(90)
