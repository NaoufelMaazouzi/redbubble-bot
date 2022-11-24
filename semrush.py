# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time
# import re
# import requests
# from bs4 import BeautifulSoup
# import asyncio
# import aiohttp
# from aiohttp.client import ClientSession
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from googleSheets import writeData, getAllNichesFromSheets

# # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# viablesNiches = []

# def getUrls(driver):
#     newUrl = driver.current_url.replace(
#         "projects/",
#         'analytics/organic/positions/?sortField=&sortDirection=desc&filter=%' +
#         '7B"search"%3A""%2C"volume"%3A"10-500"%2C"positions"%3A"1-10"%2C"serp' +
#         'Features"%3A""%2C"intent"%3A""%2C"intentPositions"%3A""%2C"clickPoten' +
#         'tial"%3A""%2C"clickPotentialPercent"%3A""%2C"kd"%3A""%2C"advanced"%3A%7' + 
#         'B"0"%3A%7B"inc"%3Afalse%2C"fld"%3A"kt"%2C"val"%3A3%7D%7D%7D&db=us&q=red' + 
#         'bubble.com&searchType=domain',
#     )
#     driver.get(newUrl)

#     # cookiesBtn = driver.find_element(
#     #     By.XPATH,
#     #     "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary')]",
#     #     # "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary ch2-btn-text-xxs')]",
#     # )
#     # cookiesBtn.click()
#     start = time.time()
#     getAllUrls(driver)
#     end = time.time()
#     print(f"download links in {end - start} seconds")
#     print("Write new niches to Google Sheets")
#     writeData(viablesNiches)


# async def download_link(hrefOfUrl: str, result: str, session: ClientSession):
#     async with session.get(hrefOfUrl) as response:
#         soup = BeautifulSoup(await response.text(), "html.parser")
#         spanResults = soup.find(
#             "span",
#             class_="styles__box--2Ufmy styles__text--23E5U styles__body--3StRc styles__muted--8wjeu",
#         ).get_text()
#         resultsParsed = spanResults.replace(",", "")
#         results = re.findall("[0-9]+", resultsParsed)[0]
#         print(f'{results} results')

#         if results and int(results) <= 20:
#             # keywords = hrefOfUrl.rsplit("/", 1)[-1]
#             # keywords = keywords.replace("+", " ")

            
#             headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
#             data = {
#                 "_token": f"ix7aSzt3DnV52ebZt2P1gTydRqRVuxrCkTNZHiJt&keyword={result}&token=03AEkXODBADrISxICX4JOj_m-WJlamqjn8MFwwqD9aRSt13PtyxYJysi9rmuCbXOharYi8oENmQbR3r2qQViZngCSMvdYe8CM1EZVDPIqjU3lUA3DG_re1pKe6yIqsd5PYYqEhf4SDKIrBn8TUiam_L8_Kf2-eMNWqAP87ydDAGMoZYQ9-2IzJ2DukVi-HhD2FvFynREW40CaFxxmOGtjsfMIBjzjuxK31VebpG0y_rA-2LhgkSnbm_9UW1gImejXz7tg3PyjMJq-nPC_WiZO9TtKrT-lPcjCrTDRooaYTFxGdTOidBOD0HmKPQJ_9Bdj4NIDckeMIdH4qXEE0Sq74EDgTOD1cOFAACBl9NLfpsFTMwZayVIRAiiyk-JHXa514gyGMj-XMpfo3PmUJl7WVKmdsNeLWnvHG1WV_tNkrJi9T3MYWY42A88MnITdFwTUn_NG2bjIFznVKGGUz7kCYzSiBWoWvApOhvali0z2x-bICJdi2bYuspyJGyp5MctjR2vg2PfqSXmEH8M9nhJ1-MEK1dFnvBR9HpU52tg2rocJG3Z-ast_s_SrsXmcsvgLwKyllhj3e-65iwitBuuDkPyB1Evv3HUvZbw&version=version_3"
#             }
#             responseTags = requests.post('https://www.topbubbleindex.com/generate-tag/get_generated_tag', headers=headers, json=data)
#             tags = responseTags.json()
#             if(tags.keys()):
#                 firstTenTags = list(tags.keys())[:10]
#                 viablesNiches.append({"niche": result, "tags": firstTenTags})
#             else:
#                 viablesNiches.append({"niche": result, "tags": []})

# async def download_all(urls: list, allNichesInSheets: list):
#     my_conn = aiohttp.TCPConnector(limit=30)
#     async with aiohttp.ClientSession(connector=my_conn) as session:
#         tasks = []
#         print("Before FOR LOOP")
#         for url in urls:
#             print("start FOR LOOP !!")            
#             hrefOfUrl = url.get_attribute("href")
#             tagFromUrl = re.findall(
#                 "[^\/]+$",
#                 hrefOfUrl,
#             )
#             tagFromUrl = tagFromUrl[0].replace("+", " ")
#             if tagFromUrl.count(".") <= 0:
#                 stopwords = ['t-shirts', 'shirts', 'stickers', 'prints', '-prints', 'art-prints', 'photographic-prints', 'posters', 'flag']
#                 querywords = tagFromUrl.split()

#                 resultwords  = [word for word in querywords if word.lower() not in stopwords]
#                 result = ' '.join(resultwords)
#                 print(result)
#                 if allNichesInSheets.count(result) <= 0:
#                     print('Ok, Not in sheets !')
#                     task = asyncio.ensure_future(download_link(hrefOfUrl=hrefOfUrl, result=result, session=session))
#                     tasks.append(task)
#         print("Out of FOR LOOP !!")            
#         await asyncio.gather(*tasks, return_exceptions=True)


# def getAllUrls(driver):
#     allNichesInSheets = getAllNichesFromSheets()
#     for i in range(1, 100):
#         try:
#             print(i)
#             urls = WebDriverWait(driver, 10).until(
#                 EC.presence_of_all_elements_located(
#                     (
#                         By.XPATH,
#                         "//*[contains(@class, '___SLink_1hgw7-red-team __noWrapText_1hgw7-red-team __color_1hgw7-red-team ___SText_ekhvk-red-team __color_ekhvk-red-team')]",
#                     )
#                 )
#             )
#             asyncio.run(download_all(urls, allNichesInSheets))
#             print(viablesNiches)
#             nextPageBtn = driver.find_element(
#                 By.XPATH,
#                 "//*[contains(@class, '___SNextPage_12i0x-red-team ___SButton_1c1ei-red-team _size_m_1c1ei-red-team _theme_primary-info_1c1ei-red-team')]",
#             )
#             nextPageBtn.click()
#         except Exception:
#             driver.quit()




from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from aiohttp.client import ClientSession
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleSheets import writeData

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
viablesNiches = []


def getUrls(driver, retry=False):
    newUrl = driver.current_url.replace(
        "projects/",
        'analytics/organic/positions/?sortField=&sortDirection=desc&filter=%' +
        '7B"search"%3A""%2C"volume"%3A"10-500"%2C"positions"%3A"1-10"%2C"serp' +
        'Features"%3A""%2C"intent"%3A""%2C"intentPositions"%3A""%2C"clickPoten' +
        'tial"%3A""%2C"clickPotentialPercent"%3A""%2C"kd"%3A""%2C"advanced"%3A%7' + 
        'B"0"%3A%7B"inc"%3Afalse%2C"fld"%3A"kt"%2C"val"%3A3%7D%7D%7D&db=us&q=red' + 
        'bubble.com&searchType=domain',
    )
    driver.get(newUrl)

    # cookiesBtn = driver.find_element(
    #     By.XPATH,
    #     "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary')]",
    #     # "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary ch2-btn-text-xxs')]",
    # )
    # cookiesBtn.click()
    start = time.time()
    getAllUrls(driver)
    end = time.time()
    print(f"download links in {end - start} seconds")
    print("Write new niches to Google Sheets")
    writeData(viablesNiches)


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

            if results and int(results) <= 20:
                keywords = hrefOfUrl.rsplit("/", 1)[-1]
                keywords = keywords.replace("+", " ")

                stopwords = ['t-shirts', 'shirts', 'stickers', 'prints', '-prints', 'art-prints', 'photographic-prints', 'posters', 'flag']
                querywords = keywords.split()

                resultwords  = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)
                headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
                data = {
                    "_token": f"ix7aSzt3DnV52ebZt2P1gTydRqRVuxrCkTNZHiJt&keyword={result}&token=03AEkXODBADrISxICX4JOj_m-WJlamqjn8MFwwqD9aRSt13PtyxYJysi9rmuCbXOharYi8oENmQbR3r2qQViZngCSMvdYe8CM1EZVDPIqjU3lUA3DG_re1pKe6yIqsd5PYYqEhf4SDKIrBn8TUiam_L8_Kf2-eMNWqAP87ydDAGMoZYQ9-2IzJ2DukVi-HhD2FvFynREW40CaFxxmOGtjsfMIBjzjuxK31VebpG0y_rA-2LhgkSnbm_9UW1gImejXz7tg3PyjMJq-nPC_WiZO9TtKrT-lPcjCrTDRooaYTFxGdTOidBOD0HmKPQJ_9Bdj4NIDckeMIdH4qXEE0Sq74EDgTOD1cOFAACBl9NLfpsFTMwZayVIRAiiyk-JHXa514gyGMj-XMpfo3PmUJl7WVKmdsNeLWnvHG1WV_tNkrJi9T3MYWY42A88MnITdFwTUn_NG2bjIFznVKGGUz7kCYzSiBWoWvApOhvali0z2x-bICJdi2bYuspyJGyp5MctjR2vg2PfqSXmEH8M9nhJ1-MEK1dFnvBR9HpU52tg2rocJG3Z-ast_s_SrsXmcsvgLwKyllhj3e-65iwitBuuDkPyB1Evv3HUvZbw&version=version_3"
                }
                responseTags = requests.post('https://www.topbubbleindex.com/generate-tag/get_generated_tag', headers=headers, json=data)
                tags = responseTags.json()
                if(tags.keys()):
                    firstTenTags = list(tags.keys())[:10]
                    viablesNiches.append({"niche": result, "tags": firstTenTags})
                else:
                    viablesNiches.append({"niche": result, "tags": []})

async def download_all(urls: list):
    my_conn = aiohttp.TCPConnector(limit=30)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_link(url=url, session=session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def getAllUrls(driver):
    for i in range(1, 100):
        try:
            print(i)
            urls = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "//*[contains(@class, '___SLink_1hgw7-red-team __noWrapText_1hgw7-red-team __color_1hgw7-red-team ___SText_ekhvk-red-team __color_ekhvk-red-team')]",
                    )
                )
            )
            asyncio.run(download_all(urls))
            print(viablesNiches)
            nextPageBtn = driver.find_element(
                By.XPATH,
                "//*[contains(@class, '___SNextPage_12i0x-red-team ___SButton_1c1ei-red-team _size_m_1c1ei-red-team _theme_primary-info_1c1ei-red-team')]",
            )
            nextPageBtn.click()
        except Exception:
            driver.quit()