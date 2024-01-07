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
    return browser


def find_by_xpath(xpath: str, browser):
    return WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, xpath)))


def get_data(url):
    try:
        browser = browser_with_options()
        browser.get(url=url)
        time.sleep(3)

        ticket = find_by_xpath(
            xpath=".highlighted-ticket__ticket > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)",
            browser=browser
        )
        ticket.click()
        time.sleep(10)

        # main_window = browser.current_window_handle
        # popup_window_handle = None

        # for handle in browser.window_handles:
        #     if handle != main_window:
        #         popup_window_handle = handle
        #
        # browser.switch_to.window(popup_window_handle)

        my_data = browser.find_element(by=By.CLASS_NAME, value='ticket-desktop__side-container')
        my_data

        # time.sleep(5)
        #
        # with open("index_selenium.html", "w") as file:
        #     file.write(browser.page_source)

    except Exception as e:
        print(e)

    finally:
        browser.close()
        browser.quit()


def main():
    get_data(
        "https://www.aviasales.ru/search/MRV1301IST1?expected_price=10380&expected_price_currency=rub&expected_price_source=share&expected_price_uuid=f025a7f6-bbed-4bd0-90f8-2c15163f0601&expected_price_value=10380&request_source=ticket_url&search_date=02012024&search_label=Red+Wings&t=WZ17051472001705156200000150MRVIST_f56245a5cb9f44694a29e3d54c752050_10380&utm_source=ticket_sharing")


if __name__ == "__main__":
    main()

#
#


# ticket_click = find_by_xpath(".highlighted-ticket__ticket > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").click()
#
# baggage_info =  find_by_xpath("div.s__bn8P2quViKWeH4_bMPib:nth-child(2)")
