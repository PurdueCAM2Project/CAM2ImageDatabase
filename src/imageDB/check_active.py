'''
The ImageDatabase team will be implementing this code
to check for active cameras that we could download and
store images from. This code was initially created by

******************************
Authors: Jia En Chua,
******************************

The ImageDatabase Team has adjusted the code.

'''

from camera import Camera
from active_and_fps import *
import time

def check_active(cam, max_fps):
    """
    In this function we initiate a list of camera objects that we can use to download images/videos
    and store in the minio database. The attributes we aimed to update are camera_ID, camera_type, url,
    is_active, is_video, framerate, ret_interval, store_interval and time.

    Specifically, ret_interval is short for retrieve interval which is the time interval between two
    consecutive image/video retrieval from one camera. This will be determined by whether will can
    download image/video or not. The default ret_interval will be 1 and the unit is in seconds. Every
    time we are unable to download image/video we will double the ret_interval (ret_interval *= 2) and
    reset back to 1 once we are able download image/video.

    Store_interval is the interval between two consecutive downloads of images/videos. This is determined
    by the camera's frame rate because it would be meaningless to download more often than the camera's
    frame rate.

    The flow of the process:
    check_active -> active_and_fps -> camera -> stream_parser

    """

    # check whether the url is working
    if cam.camera_type == 'ip':
        cam.is_active_image = start_check(cam)
        if cam.is_active_image:
            video_length = 1   # downloading images for 1 sec
            number_of_images = 1
            # Download images in range of video_length
            starttime = time.time()
            while (time.time() - starttime) < video_length:
                # TODO: use the image path for getting images. Video path?
                image, image_size = cam.parser.get_image()
                if image_size >= 0:
                    number_of_images += 1
            
            cam.framerate = number_of_images

            if cam.framerate > max_fps:
                cam.framerate = max_fps
                
    # for non-ip type of camera
    elif cam.camera_type == 'non_ip':
        cam.is_active_image = start_check(cam)
        if cam.is_active_image:
            cam.framerate = max_fps

    # for stream type of camera
    else:
        cam.is_active_video = start_check(cam)
        if cam.is_active_video:
            cam.framerate = max_fps

    # upate the last time for retrieving
    cam.last_ret_check = time.time()

    return cam
