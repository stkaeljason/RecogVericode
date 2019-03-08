import requests

import asyncio
from collections import namedtuple
import aiohttp

impack_queue = asyncio.Queue()

async def coll_im(cap_url,i):

    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/webp,image/apng,image/*,*/*;q=0.8',
               # 'Accept-Encoding':'gzip, deflate, br',
               # 'Accept-Language': 'en-US,en;q=0.9',
               # 'Connection': 'keep-alive',
               'Referer': 'https://weibo.com/',
               # 'Upgrade-Insecure-Requests': 1,
               'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36',
               # 'Cookie':'usrc=1.1.1.1.1.1.1.1; midea_mk=612bd7622d4f956f813431462555b28; '
               #          'env=%7B%22channel%22%3A3%7D; Hm_lvt_94d2fcdc25bf11213329895f51da83d0=1551841682; '
               #          'Hm_lpvt_94d2fcdc25bf11213329895f51da83d0=1551841752'
               }

    im_pack = namedtuple('impack', ['im_content', 'im_name'])
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(cap_url) as res:
                # content = await res.content
                content =  await res.read()
                print('coll',i)
                im = im_pack(content,i)
                impack_queue.put_nowait(im)
                asyncio.sleep(0.15)
                # print(len(impack_queue))
    except Exception as e:
        print(str(e))


async def save_im(i):
    while True:
        im = await impack_queue.get()
        with open('./captcha_image5/'+str(im.im_name)+'.png', 'wb') as f:
            f.write(im.im_content)
            print('***write***', im.im_name)


def get_num(start, stop):
    n = start
    while n < stop:
        n+=1
        yield n


if __name__ == "__main__":
    weibo_url = 'https://login.sina.com.cn/cgi/pin.php?r=20613788&s=0&p=gz-051c329a8c11bbd250710d34a3e1d812638c'
    tasks = [asyncio.ensure_future(coll_im(weibo_url, i)) for i in get_num(16000,24000)]
    tasks.extend([save_im(i) for i in get_num(0,4)])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
