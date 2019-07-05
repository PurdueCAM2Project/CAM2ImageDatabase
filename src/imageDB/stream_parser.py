
"""
Steps to get image and record all neccessary information

    1. Call correct function depending on the
       type of camera

*    2. Attempt to retrieve image from the camera
       and check to see if real image was returned

       i.  if image was successfully retrieved, continue
       ii. if image was not successfully retrieved, add camera
           to a 'not working' list

    3. Send image to a function to check the similarity
       to the previous image recorded to file

       i.  if image similarity is below threshold, add
           the image to the folder
       ii. if image similarity is above threshold, then
           the image can be discarded

"""
from cv2 import cv2
import signal
import urllib.request
import numpy as np
import time

class StreamParser:

    def __init__(self, url):
        self.url = url

    def open_stream(self):
        """
        Open the stream, can raise an unreachable camera error.
        """
        pass

    def close_stream(self):
        """
        Close the stream.
        """
        pass

    def restart_stream(self):
        """
        Restart the stream by closing it and opening it back up.
        -> Some cameras close a stream if they have been open for a long time,
           thus it may be neccessary to restart the stream.
        """
        self.close_stream()
        self.open_stream()


    def get_image(self):
        """

        Download the most recent image from the given camera.
        Subclasses used for specialized type of images.

        Can raise:
        -> corrupted image error: image has been corrupted
        -> unreachable camera error: couldn't retrieve an image from the camera
        -> closed stream error: stream has been closed or has not been opened
        """
        pass


class ImageStreamParser(StreamParser):
    """
    This class is a subclass of StreamParser.

    This class gets an image from an image stream camera that provides a URL to the
    most recent frame. Since the URL directly gives the image there is no need to
    open or close the stream.
    """

    def get_image(self):
        #print(urllib.__version__)
        try:
            timestamp = time.perf_counter()
            image = urllib.request.urlopen(self.url, timeout=60)
            image = image.read()
            print("\tUrl Open: {}".format(time.perf_counter() - timestamp), "seconds")
            timestamp = time.perf_counter()
            image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
            print("\tImage Decode: {}".format(time.perf_counter() - timestamp), "seconds")
            image_size = image.shape[0] * image.shape[1] * image.shape[2]
            return image, image_size

        except Exception as e:
            print("Error possibly caused by incorrect format.", e)
            #raise unreachable_camera_error()
'''
        if image == '':
            #print("Image is corrupted.")
            raise corrupted_image_error()



        if image is None:
        #print("Image is corrupted.")
            raise corrupted_image_error()
'''
