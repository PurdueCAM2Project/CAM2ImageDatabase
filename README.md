# CAM2ImageDatabase

To run the program:
The 2 python scripts (image_metadata_script.py and camera_metadata_script.py) are standalone applications which can be run by simply copying them into an IDE

To run the image_metadata_script.py:
To the image_metadata function, pass the path to the 'results' folder. 
The 'results' folder contains sub directories each named after the camera ID of the individual cameras. Each of these sub directories contains the images from that particular camera.
This will create the image metadata csv file.

To run the camera_metadata_script.py:
The camera_metadata function accepts teh image metadata csv file generated in the previous step. Therefore, run the image_metadata_script.py before running this file.
This will create the camera metadata csv file.
