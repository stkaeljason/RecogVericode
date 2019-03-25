
import cv2
import sys
import os
import time

from multiprocessing import Pool


def video2image(videos_src, im_base_path):
    """从视频源路径将多个视频截帧保存图片,同步程序"""
    frame_interval = 50               # 帧率间隔
    video_list = os.listdir(videos_src)

    for video in video_list:
        print(video,"------>开始截帧")
        video_path = os.path.join(videos_src, video)
        cap = cv2.VideoCapture(video_path)

        frame_index = 0

        if cap.isOpened():
            rval, frame = cap.read()
        else:
            rval = False
            print(video, "------>读取失败")

        while rval:
            rval, frame = cap.read()
            # print('%s_frame---->%d'%(video, frame_index))
            if frame_index % frame_interval == 0:
                im_name = '%s_frame_%d.jpg' % (video, frame_index)
                frame_save_path = os.path.join(im_base_path,video)
                im_save_path = os.path.join(frame_save_path, im_name)
                if not os.path.exists(frame_save_path):
                    os.makedirs(frame_save_path)
                cv2.imwrite(im_save_path, frame)
                print("%s_第%d帧保存成功" % (video, frame_index))
            frame_index += 1
        print(video, 'done')
        cap.release()
    print('all done')


class Video2Image:

    def __init__(self, video_src, im_base_path, frame_interval):
        self.frame_interval = frame_interval
        self.video_src = video_src
        self.im_base_path = im_base_path

    def v2f(self, video_path):
        cap = cv2.VideoCapture(video_path)
        video_name = os.path.basename(video_path)
        video_save_path = os.path.join(self.im_base_path, video_name)
        if not os.path.exists(video_save_path):
            os.makedirs(video_save_path)
        frame_index = 0

        if cap.isOpened():
            rval, frame = cap.read()
        else:
            rval = False
            print(video_path, "------>读取失败")

        while rval:
            rval, frame = cap.read()
            # print('%s_frame---->%d' % (video_path, frame_index))
            if frame_index % self.frame_interval == 0:
                im_name = '%s_frame_%d.jpg' % (video_name, frame_index)
                frame_save_path = os.path.join(video_save_path, im_name)
                cv2.imwrite(frame_save_path, frame)
                print("%s_第%d帧保存成功" % (video_name, frame_index))
            frame_index += 1

        print(video_name, '*****done*****')
        cap.release

    def main(self):
        pool = Pool(5)
        video_path_list = [os.path.join(self.video_src, video) for video in os.listdir(self.video_src)]
        for video_path in video_path_list:
            pool.apply_async(self.v2f, (video_path,))
        print('process start')
        pool.close()
        pool.join()
        print('process stop')


if __name__ == "__main__":
    now = lambda: time.time()
    videos_src = sys.argv[1]
    im_base_path = sys.argv[2]
    frame_interval = 50
    start = now()
    # video2image(videos_src, im_base_path)

    v2im = Video2Image(videos_src, im_base_path, frame_interval)
    v2im.main()
    stop = now()
    print('use time', stop - start)