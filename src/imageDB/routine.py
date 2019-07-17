import time
import sys
import os
import numpy as np
import datetime
from imageDB import ImageDB
from camera import Camera
import detection.image_demo as detection
from detection.detect_objects import YoloTest as YOLO
import csv
from PIL import Image
import cv2
from sys import getsizeof
from cam_setup import *


class Routine:
    def __init__(self):
        self.db = ImageDB()

    # Retrieve image from camera every second
    def retrieveImage(self, media_list, is_real_camera, threshold, store_interval, PID, class_dict):
        from SSIM_PIL import compare_ssim

        information = ""
        runtime = 0
        information += "querying camera data..." + "------>"
        timestamp = time.perf_counter()

        if is_real_camera:
            cam = setup_cams(media_list[PID])
        else:
            cam = setup_vids(media_list[PID], PID)

        information += str(time.perf_counter() - timestamp) + " seconds\n"
        yolo = YOLO()
        # TODO: Check if output_images folder exists
        start_time = time.time()

        size = 0
        i = 0
        j = 0

        count_proc1 = 0
        count_proc2 = 0
        count_proc3 = 0

        # TODO:
        #while True:
        while(time.time() - start_time < 60):
        #while(size < 8589934592):       # 1 gig in bits
        #while (size < 42949672960):     # 5gb in bits
        #while (size < 85899345920):  # 10 gig in bits
        #for i in range(21):
            if PID == 0:
                count_proc1 += 1
            elif PID == 1:
                count_proc2 += 1
            else:
                count_proc3 += 1

            folder_path = 'output_images/'

            try:

                ui_time = time.perf_counter()
                ts = datetime.datetime.now()

                information += "retrieving image ------>"
                timestamp = time.perf_counter()
                cam.get_image()

                image_date = ts.strftime("%Y-%m-%d")
                image_time = ts.strftime("%H:%M:%S.%f")[:-3]
                j += 1

                information += str(time.perf_counter() - timestamp) + "seconds\n"

                score = 0
                image_name = cam.camera_id + "_" + image_date + "_" + image_time + ".jpg"

                grayImage = Image.fromarray(cam.newImage)

                if i >= 1:
                    timestamp = time.perf_counter()
                    score = compare_ssim(cam.oldImage, grayImage)
                    information += "Difference calculations: " + str(time.perf_counter() - timestamp) + "seconds\n"

                if score < threshold:
                    cam.last_dif_check = time.time()
                    cam.oldImage = grayImage
                    cam.store_interval = store_interval
                    #a = time.perf_counter()
                    #cv2.imwrite(folder_path + image_name, cam.newImage)
                    #print("Writing time: {}".format(time.perf_counter() - a), "seconds\n")
                    image_size = getsizeof(cam.newImage)
                    size += image_size


                    # object detection
                    timestamp = time.perf_counter()
                    bounding_box, classes = yolo.predict(cam.newImage)
                    isprocessed = 1

                    '''save bbox in txt file for eval
                    with open ('detection/detected/' + image_name[:-4] + '.txt', 'w') as f:
                        for box in bounding_box:
                            f.write(str(classes[box[5]]) + ' ')
                            f.write(str(box[4]) + ' ')
                            f.write(str(box[0]) + ' ')
                            f.write(str(box[1]) + ' ')
                            f.write(str(box[2]) + ' ')
                            f.write(str(box[3]) + '\n')
                            #f.write('\n')
                    '''
                    information += "Object Detection: " + str(time.perf_counter() - timestamp) + "seconds\n"

                    # store into database
                    timestamp = time.perf_counter()

                    self.db.insert_image(cam.newImage, image_name, cam.camera_id, isprocessed,
                                         bounding_box, classes, image_date, image_time, image_size, class_dict)

                    information += "Image Insertion: " + str(time.perf_counter() - timestamp) + "seconds\n"

                elif time.time() - cam.last_dif_check >= cam.store_interval:
                    cam.last_dif_check = time.time()
                    cam.oldImage = grayImage
                    #a = time.perf_counter()
                    #cv2.imwrite(folder_path + image_name, cam.newImage)
                    #print("Writing time : {}".format(time.perf_counter() - a), "seconds\n")
                    image_size = getsizeof(cam.newImage)
                    size += image_size

                    # object detection
                    timestamp = time.perf_counter()
                    bounding_box, classes = yolo.predict(cam.newImage)
                    isprocessed = 1
                    '''
                    save bbox in txt file for eval
                    with open ('detection/detected/' + image_name[:-4] + '.txt', 'w') as f:
                        for box in bounding_box:
                            f.write(str(classes[box[5]]) + ' ')
                            f.write(str(box[4]) + ' ')
                            f.write(str(box[0]) + ' ')
                            f.write(str(box[1]) + ' ')
                            f.write(str(box[2]) + ' ')
                            f.write(str(box[3]) + '\n')
                            #f.write('\n')
                    '''
                    information += "Object Detection: " + str(time.perf_counter() - timestamp) + "seconds\n"

                    # Store into database
                    timestamp = time.perf_counter()

                    self.db.insert_image(cam.newImage, image_name, cam.camera_id, isprocessed,
                                         bounding_box, classes, image_date, image_time, image_size)

                    information += "Image Insertion: " + str(time.perf_counter() - timestamp) + "seconds\n"

                    if (1 - score) < (1 - threshold) / 2:
                        cam.store_interval *= 2

                if i >= 1:
                    runtime += time.perf_counter() - ui_time

                information += "Single Round for cam " + cam.camera_id + ":" + str(time.perf_counter() - ui_time) + "seconds\n"
                information += "\n"

            except Exception as e:
                print(e)
                size = 429496729600
                #sys.exit()
                #pass
                break
            i += 1

        print ('process 1: ', count_proc1, 'process 2: ', count_proc2, 'process 3: ', count_proc3)
        print("Number of frames processed : {}".format(j))
        print("Runtime for system : {}".format(runtime), " seconds\n")
        cam.capture.release()

        file = open('image_upload_times.txt', 'w')
        file.write(information)
        file.close()
