from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import switchWindow
import time
import re
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from aiohttp.client import ClientSession
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
viablesNiches = []


def getUrls(driver, retry=False):
    newUrl = driver.current_url.replace(
        "projects/",
        'analytics/organic/positions/?sortField=&sortDirection=desc&filter=%7B"search"%3A""%2C"volume"%3A"10-500"%2C"positions"%3A"1-10"%2C"serpFeatures"%3A""%2C"intent"%3A""%2C"intentPositions"%3A""%2C"clickPotential"%3A""%2C"clickPotentialPercent"%3A""%2C"kd"%3A""%2C"advanced"%3A%7B"0"%3A%7B"inc"%3Afalse%2C"fld"%3A"kt"%2C"val"%3A3%7D%7D%7D&db=us&q=redbubble.com&searchType=domain',
    )
    driver.get(newUrl)

    cookiesBtn = driver.find_element(
        By.XPATH,
        "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary')]",
        # "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary ch2-btn-text-xxs')]",
    )
    cookiesBtn.click()
    start = time.time()
    getAllUrls(driver)
    end = time.time()
    print(f"download links in {end - start} seconds")


async def download_link(url: str, session: ClientSession):
    hrefOfUrl = url.get_attribute("href")
    isGoodUrl = re.findall(
        "[^\/]+$",
        hrefOfUrl,
    )
    if len(isGoodUrl) and isGoodUrl[0].count(".") <= 0:
        async with session.get(hrefOfUrl) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            spanResults = soup.find(
                "span",
                class_="styles__box--2Ufmy styles__text--23E5U styles__body--3StRc styles__muted--8wjeu",
            ).get_text()
            resultsParsed = spanResults.replace(",", "")
            results = re.findall("[0-9]+", resultsParsed)[0]

            if results and int(results) <= 50:
                keywords = hrefOfUrl.rsplit("/", 1)[-1]
                viablesNiches.append(keywords.replace("+", " "))


async def download_all(urls: list):
    my_conn = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_link(url=url, session=session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def getAllUrls(driver):
    for i in range(1, 10):
        # try:
        print(i)
        # urls = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located(
        #         (
        #             By.XPATH,
        #             "//*[contains(@class, '___SLink_1hgw7-red-team __noWrapText_1hgw7-red-team __color_1hgw7-red-team ___SText_ekhvk-red-team __color_ekhvk-red-team')]",
        #         )
        #     )
        # )
        urls = driver.find_elements(
            By.XPATH,
            "//*[contains(@class, '___SLink_1hgw7-red-team __noWrapText_1hgw7-red-team __color_1hgw7-red-team ___SText_ekhvk-red-team __color_ekhvk-red-team')]",
        )
        asyncio.run(download_all(urls))
        print(viablesNiches)
        nextPageBtn = driver.find_element(
            By.XPATH,
            "//*[contains(@class, '___SNextPage_12i0x-red-team ___SButton_1c1ei-red-team _size_m_1c1ei-red-team _theme_primary-info_1c1ei-red-team')]",
        )
        nextPageBtn.click()
        time.sleep(5)
        # finally:
        #     driver.quit()
