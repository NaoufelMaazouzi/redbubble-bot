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
import uuid
from aiohttp.client import ClientSession
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleSheets import writeData, getAllNichesFromSheets
from utils import goNextPage

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
viablesNiches = []


def getUrls(driver, retry=False):
    try:
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

        start = time.time()
        scriptResult = getAllUrls(driver)
        end = time.time()
        print(f"download links in {end - start} seconds")
        print("Write new niches to Google Sheets")
        writeData(viablesNiches)
        return scriptResult
    except Exception as e:
        print(f"ERROR IN getUrls: {e}")


async def download_link(niche: str, url: str, session: ClientSession):
    try:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            spanResults = soup.find(
                "span",
                class_="styles__box--2Ufmy styles__text--23E5U styles__body--3StRc styles__muted--8wjeu",
            )
            if spanResults:
                spanResults = spanResults.get_text()
                resultsParsed = spanResults.replace(",", "")
                results = re.findall("[0-9]+", resultsParsed)[0]

                if results and int(results) <= 20:
                    print(f"YEEESS, {niche} has less than 20 results ({results})")
                    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
                    data = {
                        "_token": f"ix7aSzt3DnV52ebZt2P1gTydRqRVuxrCkTNZHiJt&keyword={niche}&token=03AEkXODBADrISxICX4JOj_m-WJlamqjn8MFwwqD9aRSt13PtyxYJysi9rmuCbXOharYi8oENmQbR3r2qQViZngCSMvdYe8CM1EZVDPIqjU3lUA3DG_re1pKe6yIqsd5PYYqEhf4SDKIrBn8TUiam_L8_Kf2-eMNWqAP87ydDAGMoZYQ9-2IzJ2DukVi-HhD2FvFynREW40CaFxxmOGtjsfMIBjzjuxK31VebpG0y_rA-2LhgkSnbm_9UW1gImejXz7tg3PyjMJq-nPC_WiZO9TtKrT-lPcjCrTDRooaYTFxGdTOidBOD0HmKPQJ_9Bdj4NIDckeMIdH4qXEE0Sq74EDgTOD1cOFAACBl9NLfpsFTMwZayVIRAiiyk-JHXa514gyGMj-XMpfo3PmUJl7WVKmdsNeLWnvHG1WV_tNkrJi9T3MYWY42A88MnITdFwTUn_NG2bjIFznVKGGUz7kCYzSiBWoWvApOhvali0z2x-bICJdi2bYuspyJGyp5MctjR2vg2PfqSXmEH8M9nhJ1-MEK1dFnvBR9HpU52tg2rocJG3Z-ast_s_SrsXmcsvgLwKyllhj3e-65iwitBuuDkPyB1Evv3HUvZbw&version=version_3"
                    }
                    responseTags = requests.post('https://www.topbubbleindex.com/generate-tag/get_generated_tag', headers=headers, json=data)
                    tags = responseTags.json()
                    if(tags.keys()):
                        firstTenTags = list(tags.keys())[:10]
                        viablesNiches.append({"niche": niche, "tags": firstTenTags})
                    else:
                        viablesNiches.append({"niche": niche, "tags": []})
                else:
                    print(f"NOOOO, {niche} has more than 20 results ({results})")
    except Exception as e:
        print(f"ERROR IN download_link: {e}")

async def download_all(allUrlsAndNames: list):
    try:
        my_conn = aiohttp.TCPConnector(limit=30)
        async with aiohttp.ClientSession(connector=my_conn) as session:
            tasks = []
            filteredNiches = filterUrls(allUrlsAndNames)
            for item in filteredNiches:
                task = asyncio.ensure_future(download_link(niche=item["niche"], url=item["url"], session=session))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"ERROR IN download_all: {e}")


def getAllUrls(driver):
    try:
        uniqueId = str(uuid.uuid4())
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Cookie": "wpInfo=eyJ1c2VyIjp7ImlkIjoiMjIxNyIsImlzQWRtaW4iOjAsInVzZXJuYW1lIjoiTmFvdWZlbCIsImFjY2Vzc0FibGUiOnRydWV9LCJzaXRlIjoiaHR0cHM6Ly9yYW5rZXJmb3guY29tIn0%3D; prefix=www; _gcl_au=1.1.864296799.1669994321; _ga=GA1.2.485312357.1669994310; _rdt_uuid=1669994321026.ad43fbf8-44ab-4fb8-896e-1abfd252334e; __pdst=2c3e2e7339b84d91a04bcd4d7bd41c3c; _fbp=fb.1.1669994321172.1439109524; _mkto_trk=id:519-IIY-869&token:_mch-waveserver.click-1669994321195-26277; _uetvid=9a5a5f10725411ed85fe79c6c18146ab; sa-user-id=s%253A0-d3b773cf-26ef-41ca-63da-987779c148a9.7rEc1OTzKHKR9e4dKhlXbYq%252BMOl2CZPAMFdN%252Fle4V8c; sa-user-id-v2=s%253A07dzzybvQcpj2ph3ecFIqbmS3L4.kQqil7uTHz%252FDWZxE6%252BPo10t8QMoWu9FnYwCw8WO6CmU; _ga_BPNLXP3JQG=GS1.1.1669998227.2.1.1669998682.60.0.0; _ga_HYWKMHR981=GS1.1.1669998227.2.1.1669998682.60.0.0; sess=lDBH89uIgZXMeM%2BPgVTZL9%2BtT4I%3D%232FWQYw%3D%3D%23WyIyMjE3Iiwid29yZHByZXNzX2xvZ2dlZF9pbl83OTIzOTRkMDRlYzQ5MWMxMzU1YTQxM2E4OWIzZWIxND1OYW91ZmVsfDE2NzA1NzYzMzB8d3Zxenh6S2s3TTdYbTlmZ0VEWkFqN2N0MXZidHpkd2ZiRG9zVkFJVG1pcXxhMThkOWMxNDIyMWU2MTNjN2FlMTY1M2M1MDIyZTdiNjE1NmRiNGZmNDBkZjIwNzE1Y2MyMTMzMjgwZDE2YzA4IiwiMThlNmU3ZjMxYiIsMF0%3D; PHPSESSID=dbb2e72ff879621d527743f9976e4178; SSO-JWT=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkYmIyZTcyZmY4Nzk2MjFkNTI3NzQzZjk5NzZlNDE3OCIsImlhdCI6MTY3MDQwMzU1NSwiaXNzIjoic3NvIiwidWlkIjoxMzM2NjkzNX0.MzHIYwAVnNeQdoixOlsJD67mjFxY5AYwwtModxP0Npb30UyMeQlJAOawtE-sYzXH-OdeqMbhbqc_IAtFfB2AnQ"
        }
        data = [{"id":11,"jsonrpc":"2.0","method":"organic.Positions","params":{"request_id":uniqueId,"report":"organic.positions","args":{"database":"us","dateType":"daily","searchItem":"redbubble.com","searchType":"domain","filter":{"keywordType":[{"sign":"-","value":3}],"volume":[{"sign":"+","operation":">","value":9},{"sign":"+","operation":"<","value":501}],"position":[{"sign":"+","operation":">","value":0},{"sign":"+","operation":"<","value":11}]},"display":{"order":{"field":"trafficPercent","direction":"desc"},"page":1,"pageSize":10000}},"userId":13289797,"apiKey":"73030f50f9f245d9da3fc6cb36bccdbe"}},{"id":12,"jsonrpc":"2.0","method":"organic.PositionsTotal","params":{"request_id":uniqueId,"report":"organic.positions","args":{"database":"us","dateType":"daily","searchItem":"redbubble.com","searchType":"domain","filter":{"keywordType":[{"sign":"-","value":3}],"volume":[{"sign":"+","operation":">","value":9},{"sign":"+","operation":"<","value":501}],"position":[{"sign":"+","operation":">","value":0},{"sign":"+","operation":"<","value":11}]},"display":{"order":{"field":"trafficPercent","direction":"desc"},"page":1,"pageSize":10000}},"userId":13289797,"apiKey":"73030f50f9f245d9da3fc6cb36bccdbe"}}]

        response = requests.post('https://sem.waveserver.click/dpa/rpc', headers=headers, json=data)
        response = response.json()
        tuple_keys = ('url','phrase')
        allUrlsAndNames = [{k: d[k] for k in tuple_keys if k in d} for d in response[0]['result']]
        asyncio.run(download_all(allUrlsAndNames))
        print(viablesNiches)
    except Exception as e:
        print(f"ERROR IN getAllUrls: {e}, links can't be displayed on")
        driver.close()
        return False
    return True

def filterUrls(allUrlsAndNames):
    try:
        allNichesInSheets = getAllNichesFromSheets()
        filteredNiches = []
        for item in allUrlsAndNames:
            querywords = item['phrase'].split() 
            stopwords = ['t-shirts', 'shirts', 'stickers', 'prints', '-prints', 'art-prints', 'photographic-prints', 'posters', 'flag']
            resultwords  = [word for word in querywords if word.lower() not in stopwords]
            result = ' '.join(resultwords)
            if allNichesInSheets.count(result) <= 0:
                print(f'Good, {result} Not in sheets !')
                filteredNiches.append({"niche": result, "url": item['url']})
            else:
                print(f'Failed, {result} already in sheets !')
        return filteredNiches
    except Exception as e:
        print(f"ERROR IN filterUrls: {e}")
    
