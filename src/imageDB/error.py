"""
    error.py

    This file represents a variety of errors that may
    be encountered during the various processes of the
    image database

"""

class Error(Exception):
    """ General Error """
    pass

class unreachable_camera_error(Error):
    """ Camera unavailable """
    pass

class corrupted_image_error(Error):
    """ Image has been corrupted """
    pass

class closed_stream_error(Error):
    """ Stream is closed when image is requested """
    pass
