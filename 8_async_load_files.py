import requests
from time import time


def get_file(url):
    response = requests.get(url, allow_redirects=True)
    return response


def write_file(response):
    # https://loremflickr.com/cache/resized/65535_50238123602_69f8d08022_320_240_nofilter.jpg
    filename = 'files/' + response.url.split('/')[-1]
    with open (filename, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()
    url = 'https://loremflickr.com/320/240'
    for i in range(10):
        write_file(get_file(url))
    print(time() - t0)


# if __name__ == '__main__':
#     main()

##################################################

import asyncio
import aiohttp


def write_image(date):
    filename = 'files/file-{}.jpeg'.format(int(time() * 1000))
    with open(filename, 'wb') as file:
        file.write(date)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main2())
    print(time() - t0)













