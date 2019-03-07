from gevent import monkey
monkey.patch_all()
import gevent
import requests

from gevent.queue import Queue
impack_queue = Queue()


def coll_im(cap_url,i):

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

    try:
        im_content = requests.get(cap_url, headers=headers).content
        im_pack = (im_content, i)
        impack_queue.put(im_pack)
    except Exception as e:
        print(str(e))


def save_im():
    while not impack_queue.empty():
        im_pack = impack_queue.get()
        with open('./captcha_image5/'+str(im_pack[1])+'.png', 'wb') as f:
            f.write(im_pack[0])
            print('***write***', im_pack[1])


if __name__ == "__main__":
    # coll_im('https://login.sina.com.cn/cgi/pin.php?r=20613788&s=0&p=gz-051c329a8c11bbd250710d34a3e1d812638c')

    a=[gevent.spawn(coll_im, 'https://login.sina.com.cn/cgi/pin.php?r=20613788&s=0&p=gz-051c329a8c11bbd250710d34a3e1d812638c',i) for i in range(6000,16000)]
    gevent.joinall(a)
    save_im()