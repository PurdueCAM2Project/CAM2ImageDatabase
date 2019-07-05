import cv2
import urllib.request
import numpy as np

try:
    while True:
        print("start")
        image = urllib.request.urlopen("http://10.186.119.173:8080")
        print("end")
        image = image.read()
        
        image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
        image_size = image.shape[0] * image.shape[1] * image.shape[2]

        cv2.imshow('', image)
        cv2.waitKey(2)


except Exception as e:
    print(e)

