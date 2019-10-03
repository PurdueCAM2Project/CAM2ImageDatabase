import numpy as np
import cv2
import time

cap = cv2.VideoCapture('video_dataset/TownCenterXVID.avi')

while(True):

    ret, frame = cap.read()
    print(ret)
    if not ret:
        break
    cv2.imshow('frame', frame)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
