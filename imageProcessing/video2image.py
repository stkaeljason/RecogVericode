import cv2
import sys
import os


def video2image(videos_src, im_base_path):
    frame_interval = 10
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
            print('frame---->%d'%frame_index)
            if frame_index % frame_interval == 0:
                im_name = 'frame_%d.jpg'%frame_index
                frame_save_path = os.path.join(im_base_path,im_name)
                cv2.imwrite(frame_save_path, frame)
                print("第%d帧保存成功"%frame_index)
            frame_index += 1
        print(video, 'done')
        cap.release()
    print('all done')


if __name__ == "__main__":
    videos_src = sys.argv[1]
    im_base_path = sys.argv[2]
    video2image(videos_src, im_base_path)