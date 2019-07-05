import cv2
import numpy as np
import csv

def diff():
    img1 = cv2.imread("./img1.jpeg")

    print(img1)
    img2 = cv2.imread("./img1.jpeg")
    #img1 = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), -1)
    print(img2)
    #img2 = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), -1)
    difference = float(np.sum(np.absolute(img1 - img2))) / (img1.shape[0] * img1.shape[1] * img1.shape[2] * 255.0)

    print(img1)
    print(img2)
    print("1: ", float(np.sum(np.absolute(img1 - img2))))
    print("2: ", (img1.shape[0] * img1.shape[1] * img1.shape[2] * 255.0))
    print("3: ", difference)


    with open('old.txt', 'w', newline='') as file1:
        ui_writer = csv.writer(file1)
        ui_writer.writerow([img1])
    with open('new.txt', 'w', newline='') as file2:
        ui_writer = csv.writer(file2)
        ui_writer.writerow([img2])

diff()
