import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from semrush import getUrls
from utils import switchWindow

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

try:
    EMAIL = os.environ["EMAIL"]
    PASSWORD = os.environ["PASSWORD"]
except KeyError:
    EMAIL = "EMAIL not available!"
    PASSWORD = "PASSWORD not available!"


def login():
    driver.get("https://rankerfox.com/login/")
    driver.maximize_window()

    inputElement = driver.find_element(By.ID, "iump_login_username")
    inputElement.send_keys(EMAIL)
    inputElement = driver.find_element(By.ID, "iump_login_password")
    inputElement.send_keys(PASSWORD)
    inputElement.submit()
    time.sleep(1)
    popUp = driver.find_element(
        By.ID,
        "cp_close_image-2-24066",
    )
    popUp.click()
    print('Logged in rankerfox')
    openSemrush()


def openSemrush():
    userSemrush = driver.find_elements(By.CSS_SELECTOR, "input[value*='User Semrush']")
    for index, i in enumerate(userSemrush):
        switchWindow(driver, 0)
        i.submit()
        # time.sleep(5)
        switchWindow(driver, -1)
        currentUrl = driver.current_url
        x = re.search("projects/$", currentUrl)

        if x is None:
            print(f"Link {index} don't work")
            driver.close()

        elif index == 2:
            getUrls(driver)
            break


login()
