import numpy as np

from generate_captcha import gen_captcha_text_and_image
from train import crack_captcha_cnn, MAX_CAPTCHA, CHAR_SET_LEN, keep_prob, X, vec2text, convert2gray
import tensorflow as tf

def crack_captcha(captcha_image):
    output = crack_captcha_cnn()

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint('.'))

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

        text = text_list[0].tolist()
        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        i = 0
        for n in text:
            vector[i * CHAR_SET_LEN + n] = 1
            i += 1
        return vec2text(vector)


def test_crack_captcha(test_step):
    output = crack_captcha_cnn()

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint('./models'))
        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        sum_correct = 0
        for _ in range(test_step):

            text_source, image = gen_captcha_text_and_image()
            image = convert2gray(image)
            captcha_image = image.flatten() / 255
            text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})
            text = text_list[0].tolist()
            vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
            i = 0
            for n in text:
                vector[i * CHAR_SET_LEN + n] = 1
                i += 1
            predict_text=vec2text(vector)
            print("正确: {}  预测: {}".format(text_source, predict_text))

            if  text_source.lower() == predict_text.lower():
                sum_correct += 1
        print('sum_correct:%s' % sum_correct)
        print('成功率：%s' % (sum_correct / test_step))



def test_captcha_model(test_step):
    sum_correct = 0
    for _ in range(test_step):
        text, image = gen_captcha_text_and_image()
        image = convert2gray(image)
        image = image.flatten() / 255
        predict_text = crack_captcha(image)
        print("正确: {}  预测: {}".format(text, predict_text))
        if text == predict_text:
            sum_correct+=1
    print('sum_correct:%s'%sum_correct)
    print('成功率：%s'%(sum_correct/test_step))


if __name__ == "__main__":
    test_crack_captcha(10000)