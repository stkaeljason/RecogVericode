from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
# import matplotlib.pyplot as plt
from PIL import Image
import random
import os

# 验证码中的字符, 就不用汉字了
from config import char_set


# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=char_set, captcha_size=4):
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return ''.join(captcha_text)


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha()

    captcha_text = random_captcha_text()

    captcha = image.generate(captcha_text)
    # image.write(captcha_text, captcha_text + '.jpg')  # 写到文件

    captcha_image = Image.open(captcha)
    # print(captcha_image)
    captcha_image = np.array(captcha_image)
    return captcha_text, captcha_image


def gen_image(image_path):
    for image in os.listdir(image_path)[:1]:
        captcha_text = image.strip('.png')
        image = os.path.join(image_path, image)
        # print(image)
        captcha_image = Image.open(image)
        # print(captcha_image, captcha_text)
        captcha_image = np.array(captcha_image)
        yield captcha_text, captcha_image



# gen_image('./captcha_image')
# gen_captcha_text_and_image()