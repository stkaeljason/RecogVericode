import requests


def coll_im(cap_url):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/webp,image/apng,image/*,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'www.midea.cn',
               # 'Upgrade-Insecure-Requests': 1,
               'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36',
               'Cookie':'usrc=1.1.1.1.1.1.1.1; midea_mk=612bd7622d4f956f813431462555b28; '
                        'env=%7B%22channel%22%3A3%7D; Hm_lvt_94d2fcdc25bf11213329895f51da83d0=1551841682; '
                        'Hm_lpvt_94d2fcdc25bf11213329895f51da83d0=1551841752'
               }
    for i in range(10):
        res = requests.get(cap_url, headers=headers)
        print(res.content)
        im_content = res.content
        with open('./captcha_image/'+str(i)+'.jpg', 'wb') as f:
            f.write(im_content)


if __name__ == "__main__":
    coll_im('https://www.midea.cn/next/user_assist/getimagevc?scene=userlogin&t=0.5966588233775472')