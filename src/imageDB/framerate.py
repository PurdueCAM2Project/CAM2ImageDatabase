import cv2
import time
from camera import Camera
import sys

def get_fps(video_path):
    """
    Calculate the approximate the retrievable frame rate from
    the inputted camera url.

    :param video_path: camera url
    :return: approximate retrievable framerate
    """
    video = cv2.VideoCapture(video_path)
    i = 0
    img = None
    num_frames = 0
    ret, img = video.read()

    starttime = time.time()
    #print ('video path:', video_path)
    while (ret and i < 10):
        i += 1
        ret, img = video.read()
        num_frames += 1
        #print(i)
    total_time = time.time() - starttime

    fps = num_frames / total_time

    return fps
