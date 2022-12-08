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
from seleniumwire.utils import decode as sw_decode
from ast import literal_eval

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
viablesNiches = []
paramsForRequest = False

def getCookiesHeaders(driver):
    global paramsForRequest
    for request in driver.requests:
            if request.response and request.url == "https://sem.waveserver.click/dpa/rpc" and request.response.status_code == 200:
                cookie = request.headers['Cookie']
                userAgent = request.headers['User-Agent']
                data = sw_decode(request.body, request.response.headers.get('Content-Encoding', 'identity'))
                data = data.decode("utf8")
                bodyData = literal_eval(data)
                isList = isinstance(bodyData, list)
                methods = ['organic.Positions', 'organic.PositionsTotal']
                if(isList and methods.count(bodyData[0]["method"]) >= 1):
                    uniqueId = str(uuid.uuid4())
                    for item in bodyData:
                        item["params"]["request_id"] = uniqueId
                        item["params"]["args"]["display"]["pageSize"] = 10
                    paramsForRequest = { "bodyData": bodyData, "headers": { "User-Agent": userAgent, "Cookie": cookie } }


def getUrls(driver, retry=False):
    try:
        global paramsForRequest
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
        getCookiesHeaders(driver)
        for index in range(1, 4):
            if (paramsForRequest):
                uniqueId = str(uuid.uuid4())
                for item in paramsForRequest["bodyData"]:
                    item["params"]["args"]["display"]["page"] = index
                    item["params"]["request_id"] = uniqueId
                scriptResult = getAllUrls(driver, paramsForRequest)
                if(scriptResult == False):
                    return False
        end = time.time()
        print(f"download links in {end - start} seconds")
        print("Write new niches to Google Sheets")
        writeData(viablesNiches)
        return True
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


def getAllUrls(driver, data):
    try:
        response = requests.post('https://sem.waveserver.click/dpa/rpc', headers=data["headers"], json=data["bodyData"])
        statusCode = response.status_code
        print('StatusCode:', statusCode)
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