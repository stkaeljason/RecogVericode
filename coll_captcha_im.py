import datetime
import random
import time
import asyncio
from collections import namedtuple
import aiohttp
from threading import Thread


class CaptchaCrawl:
    im_sum_num = 1

    def __init__(self, site_url, headers, im_name, save_path):
        self.queue = asyncio.Queue()
        self.site_url = site_url
        self.headers = headers
        self.im_name = im_name
        self.save_path = save_path


    async def fetch(self, name):

        im_pack = namedtuple('impack', ['im_content', 'im_name'])
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(self.site_url) as res:
                    content = await res.read()
                    im = im_pack(content, name)
                    return im
        except Exception as e:
            print(str(e))

    async def product(self, im_name):
        im = await self.fetch(im_name)
        self.queue.put_nowait(im)
        print('product---->', im_name)

    async def save_im(self, im):
        with open(self.save_path + str(im.im_name) + '.png', 'wb') as f:
            f.write(im.im_content)
            # print('***write***', im.im_name)

    def save_callback(self,future):
        print('----callbackcallback----')
        self.im_sum_num+=1


class Engine:

    def __init__(self, crawl):
        self.crawl = crawl

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        # while True:
        #     im_name = compute_id(self.crawl.im_name)
        #     # task = asyncio.ensure_future(self.crawl.product(im_name))
        #     # task.add_done_callback(self.crawl.save_callback)
        #     asyncio.run_coroutine_threadsafe(self.crawl.product(im_name), loop)
        #     print('sdflsfsld')

    def start_product(self, loop):
        asyncio.set_event_loop(loop)
        while True:
            im_name = compute_id(self.crawl.im_name)
            coroutine = self.crawl.product(im_name)
            task = asyncio.ensure_future(coroutine)
            task.add_done_callback(self.crawl.save_callback)
            asyncio.run_coroutine_threadsafe(coroutine, loop)

    def run(self):
        new_loop = asyncio.new_event_loop()
        print('---start loop---')
        thread1 = Thread(target=self.start_loop, args=(new_loop,))

        print('---start product---')
        thread2 = Thread(target=self.start_product, args=(new_loop,))
        thread1.setDaemon(True)
        thread1.start()
        thread2.setDaemon(True)
        thread2.start()

        try:
            while True:
                if self.crawl.im_sum_num % 100 == 0:
                    print('success crawl captcha image---->%d'%self.crawl.im_sum_num)
                im = self.crawl.queue.get()
                if not im:
                    print('nononono')
                    time.sleep(1)
                    continue
                asyncio.run_coroutine_threadsafe(self.crawl.save_im(im), new_loop)

        except KeyboardInterrupt as e:
            print(e)
            new_loop.stop()
        except Exception as e:
            print(e)


def get_num(start, stop):
        n = start
        while n < stop:
            n += 1
            yield n


def compute_id(lable_str):
    return lable_str + '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.choice('t5hrwop6ksq9mvfx8g3c4dzu01n72yeabijl')) for i in range(5)])


if __name__ == "__main__":
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/webp,image/apng,image/*,*/*;q=0.8',
        # 'Accept-Encoding':'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9',
        # 'Connection': 'keep-alive',
        'Referer': 'https://weibo.com/',
        # 'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36',
        # 'Cookie':'usrc=1.1.1.1.1.1.1.1; midea_mk=612bd7622d4f956f813431462555b28; '
        #          'env=%7B%22channel%22%3A3%7D; Hm_lvt_94d2fcdc25bf11213329895f51da83d0=1551841682; '
        #          'Hm_lpvt_94d2fcdc25bf11213329895f51da83d0=1551841752'
        }
    weibo_url = 'https://login.sina.com.cn/cgi/pin.php?r=20613788&s=0&p=gz-051c329a8c11bbd250710d34a3e1d812638c'
    captcha_crawl = CaptchaCrawl(weibo_url, headers, 'weibo', save_path='./captcha_image/')
    engine = Engine(captcha_crawl)
    engine.run()
