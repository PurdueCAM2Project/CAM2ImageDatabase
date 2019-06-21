from __future__ import print_function
import os
#import camera
#import time
import shutil
from cv2 import cv2

"""
Description:
    This script determine the camera's frame rate by calling functions in camera.py and stream_parser.py
How to run:
    url = "http://207.251.86.238/cctv290.jpg"
    duration = 60
    framerate = setup(url=url, duration=duration)
"""

'''
For the Imagedatabse team, we will query camera information
from our database, convert it to a necesaary form, ex. list or
dictionary, and pass the data to the 'setup' function
'''

# As long as we find a way to download video from web
def assessFramerate(video_file):
    # Initialize a VideoCapture object
    video = cv2.VideoCapture(video_file)

    # We will be using opencv version above 3, so the function will be "cv2.CAP_PROP_FPS"
    fps = video.get(cv2.CAP_PROP_FPS)
    #print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    video.release()

    return fps
    
    '''
    if fps > 0:
        return fps, True
    else:
        return fps, False
    '''
    
'''
For the start_check function, this is where we try to download images by calling
stream parser part, which is done by Luke. We might have to tweak several things
when we are integrating this part with Luke's part.
Especially, we might face some problems with the video downloading part since we
never discused it together during our meetings.
'''

def start_check(cam):
    if os.path.isdir("Pictures"):
        shutil.rmtree('Pictures')

    try:
        os.makedirs('Pictures')

    except OSError:
        raise OSError("Directory already existed")

    # For Ip cameras, check images as well as videos
    if cam.camera_type == 'ip':

        image_check = cam.get_image()
        #video_check =
        return image_check#, video_check

    # For non-Ip cameras, check images
    elif cam.camera_type == 'non-ip':
        image_check = cam.get_image()
        return image_check

    # For Stream cameras, check videos
    else:
        #video_check =
        #return video_check
        pass
