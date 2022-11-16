# import asyncio
# import time
# import aiohttp
# from aiohttp.client import ClientSession

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# async def download_link(url: str, session: ClientSession):
#     async with session.get(url) as response:
#         result = await response.text()
#         print(f"Read {len(result)} from {url}")


# async def download_all(urls: list):
#     my_conn = aiohttp.TCPConnector(limit=10)
#     async with aiohttp.ClientSession(connector=my_conn) as session:
#         tasks = []
#         for url in urls:
#             task = asyncio.ensure_future(download_link(url=url, session=session))
#             tasks.append(task)
#         await asyncio.gather(
#             *tasks, return_exceptions=True
#         )  # the await must be nest inside of the session


# url_list = ["https://www.google.com", "https://www.bing.com"] * 50
# print(url_list)
# start = time.time()
# asyncio.run(download_all(url_list))
# end = time.time()
# print(f"download {len(url_list)} links in {end - start} seconds")


import requests
from requests.sessions import Session
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local

url_list = ["https://www.google.com/", "https://www.bing.com"] * 50
thread_local = local()


def get_session() -> Session:
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_link(url: str):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all(urls: list) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_link, url_list)


start = time.time()
download_all(url_list)
end = time.time()
print(f"download {len(url_list)} links in {end - start} seconds")
