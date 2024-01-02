import time
import subprocess

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def custom_firefox():
    option = webdriver.FirefoxOptions()
    option.page_load_strategy = "eager"
    option.set_preference('Default', '1')
    option.set_preference('dom.webnotifications.disabled', False)
    option.set_preference('media.volume_scale', '0.0')
    # option.add_argument("--headless")
    option.add_argument('--enable-gpu')
    # option.add_argument('disable-blink-features=AutomationControlled')
    option.add_argument("user-agent=Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0")
    browser = webdriver.Firefox(options=option)
    return browser


def browser_with_options():
    browser = custom_firefox()
    browser.get("https://www.aviasales.ru/search/MRV1301IST1?expected_price=10380&expected_price_currency=rub&expected_price_source=share&expected_price_uuid=f025a7f6-bbed-4bd0-90f8-2c15163f0601&expected_price_value=10380&request_source=ticket_url&search_date=02012024&search_label=Red+Wings&t=WZ17051472001705156200000150MRVIST_f56245a5cb9f44694a29e3d54c752050_10380&utm_source=ticket_sharing")
    return browser


browser = browser_with_options()


def find_by_xpath(xpath: str):
    return WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, xpath)))




btn = find_by_xpath("div.ticket-desktop__share:nth-child(4) > div:nth-child(1) > button:nth-child(1) > svg:nth-child(1)")
btn.click()


# Запустите команду xclip для получения содержимого буфера обмена
process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Проверьте наличие ошибок
if process.returncode == 0:
    # Получите текст из вывода команды
    copied_text = output.decode('utf-8').strip()

    # Выведите содержимое буфера обмена или сохраните в переменной
    print("Скопированный текст:", copied_text)

    # Если вы хотите сохранить в переменной, просто присвойте значение переменной
    # содержимому буфера обмена
    your_variable = copied_text
else:
    # Выведите сообщение об ошибке, если не удалось получить содержимое буфера обмена
    print("Ошибка при получении содержимого буфера обмена:", error.decode('utf-8'))
