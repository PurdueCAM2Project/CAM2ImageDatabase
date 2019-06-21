
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

from __future__ import absolute_import
from six.moves import urllib

from binascii import hexlify
from cv2 import cv2
import signal
import urllib.request
import numpy as np
from error import Error, unreachable_camera_error, corrupted_image_error, closed_stream_error

class StreamParser(object):

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
            image = ''
            #urllib.urlretrieve(self.url, image)
            #print(self.url)
            image = urllib.request.urlopen(self.url, timeout=5)
            #print(image)
            def handler(signum):
                print('Signal handler called with signal', signum)
                raise OSError("Camera could not be opened.")

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(5)
            image = image.read()
            signal.alarm(0)

        except Exception as e:
            #print("Error possibly caused by incorrect format.")
            raise unreachable_camera_error()

        if image == '':
            #print("Image is corrupted.")
            raise corrupted_image_error()

        image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
        
        image_size = image.shape[0] * image.shape[1] * image.shape[2] 

        if image is None:
            #print("Image is corrupted.")
            raise corrupted_image_error()

        return image, image_size

class MJPEGStreamParser(StreamParser):
    """
    This class is a subclass of StreamParser.

    Requires the URL of the MJPEG stream (url -> string).
    """

    def __init__(self, url):
        super(MJPEGStreamParser, self).__init__(url)
        self.mjpeg_stream = None

    def open_stream(self):
        """
        Open the MJPEG stream.

        Can raise an unreachable camera error.
        """
        try:
            self.mjpeg_stream = urllib.request.urlopen(self.url, timeout=5)
        except:
            print("Camera is unreachable.")
            raise unreachable_camera_error()

    def close_stream(self):
        """
        Open the MJPeg stream.

        Can raise the unreachable camera error
        """
        if self.mjpeg_stream is not None:
            self.mjpeg_stream.close()
            self.mjpeg_stream = None

    def get_image(self):
        """
        Get the most recent frame from the MJPEG stream.

        Can raise the corrpted image error and/or closed stream error.
        """

        if self.mjpeg_stream is None:
            print("Error, stream is closed or has not been opened.")
            raise closed_stream_error()

        #print(str(hexlify(self.mjpeg_stream.readline().rstrip()), "utf-8"))
        #print(self.mjpeg_stream.readline())
        if self.mjpeg_stream.readline().rstrip() != b'--myboundary':
            print(self.mjpeg_stream.readline())
            print("corrupted image error")
            raise corrupted_image_error

        #print(self.mjpeg_stream.readline())
        if self.mjpeg_stream.readline().rstrip() != b'Content-Type: image/jpeg':
            print("corrupted image error 2")
            raise corrupted_image_error

        line = [s.strip() for s in self.mjpeg_stream.readline().split(b':')]
        print(line)
        if len(line) == 2 and line[0] == b'Content-Length' and line[1].isdigit():
            image_size = int(line[1])
        else:
            print("Image is corrupted.")
            raise corrupted_image_error()

        if self.mjpeg_stream.readline().strip() != b'':
            print("Image is corrupted.2")
            raise corrupted_image_error()

        image = self.mjpeg_stream.read(image_size)

        if self.mjpeg_stream.readline().strip() != b'':
            print("Image is corrupted.3")
            raise corrupted_image_error()

        image = cv2.imdecode(np.fromstring(image, dtype=np.uint8), -1)

        if image is None:
            print("Image is corrupted.4")
            raise corrupted_image_error()

        return image, image_size

    def __del__(self):
        """
        Close the MJPEG stream when the object is going to be deleted.

        In case the user does not call close_stream, this serves as a backup
        to avoid putting unnecessary work on the network.
        """
        self.close_stream()

class MJPGm3u8StreamParser(StreamParser):
    """
    This class is a subclass of StreamParser.

    This class is a parser for a camera MJPEG stream.

    Requires the URL of the MJPEG stream (url -> str)
    """

    def __init__(self, url):
        super(MJPGm3u8StreamParser, self).__init__(url)
        self.mjpeg_stream = None

    def get_image(self):
        """
        Get the most recent image from the camera MJPEG stream.

        Can raise corrupted image error or closed stream error.
        """

        vc = cv2.VideoCapture(self.url)
        if vc.isOpened():
            _, image = vc.read()
            vc.release()
            return image, 1
        print("No Image was returned")
        vc.release()
        return None, 1


"""
class download_image(object);

  #initialize camera_type
  def __init__(self):
      camera_type = self.type
      pass

  #select correct camera type
  if camera_type == 'ip':
      pass

  elif camera_type == 'non_ip':
      pass

  elif camera_type == 'stream':
      pass

  else :
      print("camera_type is not in correct format")
      return

  # Retrieve image from a non-ip camera
  def get_non_ip_image(self):


  # Retrieve image from a stream
  def get_steam_image(self):
      pass
"""
