'''
In this file, we define camera object that
will have all the necessary attributes and
functions

'''
import time

class Camera():

    def __init__(self, camera_id, ip_address, image_path, video_path):
        self.camera_id = camera_id                 # This is ID of a camera

        self.parser = None
        self.image_path = 'http://' + ip_address + image_path
        self.video_path = 'http://' + ip_address + video_path

        self.store_interval = 1             # Time interval to store image from camera

        self.last_dif_check = 0             # The most recent time stamp for checking image difference

        self.oldImage = 0                # Holds the last image been stored
        self.newImage = 0                # Holds the current image

        self.image_size = 0
        self.capture = None


    def get_image(self):
         try:
            ret, self.newImage = self.capture.read()
            self.image_size = 0 #self.newImage.shape[0] * self.newImage.shape[1] * self.newImage.shape[2]
            return True

         except Exception as e:
            print("Error possibly caused by incorrect format.", e)
            return False
