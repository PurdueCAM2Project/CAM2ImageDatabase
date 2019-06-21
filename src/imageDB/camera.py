'''
In this file, we define camera object that
will have all the necessary attributes and
functions

'''

from cv2 import cv2
import time
import datetime
import error
from stream_parser import *


class Camera():

    def __init__(self, camera_id, camera_type):
        self.camera_id = camera_id                 # This is ID of a camera
        self.camera_type = camera_type      # Type of the camera

        self.parser = None
        self.image_path = None
        self.video_path = None
        self.snapshot_url = None
        self.m3u8_url = None
        self.video_file = None
        #self.is_active_image = False
        #self.is_active_video = False

        #self.framerate = 0                  # Frame rate of the camera
        #self.ret_interval = 1               # Time interval to retrieve image from camera
        self.store_interval = 1             # Time interval to store image from camera

       # self.last_ret_check = 0             # The most recent time stamp for checking camera actite
        self.last_dif_check = 0             # The most recent time stamp for checking image difference

        self.sampleImage = None                # Holds the string name of the reference image

        self.oldImage = 0                # Holds the last image been stored
        self.newImage = 0                # Holds the current image

        self.image_size = 0


    def get_image(self):
        # Set the timestamp of the snapshot that will be downloaded
        frame_timestamp = time.time()
        try:
            # Download the image
            self.newImage, self.image_size = self.parser.get_image()
            #self.sampleImage = 'Pictures/sample_{}.png'.format(datetime.datetime.fromtimestamp(frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
            #cv2.imwrite(self.sampleImage, self.newImage)
            return True
            
        except error.unreachable_camera_error as unreachable_camera_error:
            #raise error.UnreachableCameraError('get_ref_image_ERROR: Image could not be retrieved for Url: {}'.format(self.url))
            print(unreachable_camera_error, 'get_ref_image_ERROR: Image could not be retrieved')
            return False

        except Exception as e:
            #raise e
            print(e)
            return False


class Ip_Camera(Camera):
    def __init__(self, camera_id, camera_type, ip_address, image_path, video_path):
        super().__init__(camera_id, camera_type)
        self.image_path = 'http://' + ip_address + image_path        # Image path for ip types
        self.video_path = 'http://' + ip_address + video_path        # Video path for ip types
        self.parser = ImageStreamParser(self.image_path)  # This is the StreamParser object responsible for grabbing image/video
        self.video_file = None


class Non_Ip_Camera(Camera):
    def __init__(self, camera_id, camera_type, snapshot_url):
        super().__init__(camera_id, camera_type)
        self.snapshot_url = snapshot_url    # Url for non-ip types
        self.parser = ImageStreamParser(self.snapshot_url)  # This is the StreamParser object responsible for grabbing image/video

class Stream(Camera):
    def __init__(self, camera_id, camera_type, m3u8_url):
        super().__init__(camera_id, camera_type)
        self.m3u8_url = m3u8_url    # Url for non-ip types
        self.parser = ImageStreamParser(self.m3u8_url)  # This is the StreamParser object responsible for grabbing image/video
