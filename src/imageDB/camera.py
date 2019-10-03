'''
In this file, we define camera object that
will have all the necessary attributes and
functions
'''
import time

class Camera:

    def __init__(self, camera_id, ip_address, image_path, video_path, x_max, x_min, y_max, y_min):
        """
        Initialize important variables used during the camera routine to gather
        images and image metadata.

        :param camera_id: Camera's unique identification string
        :param ip_address: camera ip, used to retrieve frames
        :param image_path: part of url, used to retrieve frames
        :param video_path: part of url, used to retrieve frames
        TO BE ADDED:
        :param x_max: maximum x value used to crop image
        :param x_min: minimum x value used to crop image
        :param y_max: maximum y value used to crop image
        :param y_min: minimum y value used to crop image
        """

        self.camera_id = camera_id      # This is ID of a camera

        self.parser = None
        self.image_path = 'http://' + ip_address + image_path
        self.video_path = 'http://' + ip_address + video_path

        self.store_interval = 1         # Time interval to store image from camera

        self.last_dif_check = 0         # The most recent time stamp for checking image difference

        self.oldImage = 0               # Holds the last image been stored
        self.newImage = 0               # Holds the current image

        self.image_size = 0
        self.capture = None

        self.frames = 0
        self.fps = 0
        self.totalResolution = 0

        #TODO: Hold the size restrictions of cropped image to find difference in region of interest in an image from a specific camera.
        #      This needs to be saved in the camera table. Each camera has unique cropping coordinates.
        #      Further research on how to automate the process of finding region of interests in images.

        self.crop_x_max = x_max
        self.crop_x_min = x_min
        self.crop_y_max = y_max
        self.crop_y_min = y_min

        self.number = 0

    def get_image(self):
        """
        Using cv2's VideoCapture, retrieve an image from camera.

        :return: self.newImage holds new image retrieved from camera
                 and True value returned if successful
        """
        try:
            ret, self.newImage = self.capture.read()
            self.image_size = 0 #self.newImage.shape[0] * self.newImage.shape[1] * self.newImage.shape[2]
            return True

        except Exception as e:
            print("Error possibly caused by incorrect format.", e)
            return False
