import time
import sys
import os
import numpy as np
import datetime
from imageDB import ImageDB
from camera import Camera, Ip_Camera
import detection.image_demo as detection
import csv
from PIL import Image
import cv2
#from skimage.measure import compare_ssim
from SSIM_PIL import compare_ssim

class Routine:
    def __init__(self):
        self.db = ImageDB()

    # Retrieve image from camera every second
    def retrieveImage(self, threshold, max_fps, store_interval, num_of_cams):

        print("\t{0: <25}".format("querying camera data..."), "------>", end="")
        timestamp = time.perf_counter()

        # Set up cameras
        cam_data = self.db.get_all_cameras(num_of_cams)
        cam_list = []
        for data in cam_data:
            cam = Ip_Camera(camera_id=data[0], ip_address=data[1], image_path=data[2], video_path=data[3])
            cam_list.append(cam)
        print(time.perf_counter() - timestamp, " seconds")

        tensors, graph, sess = detection.initial()

        # TODO: Check if output_images folder exists
        #ui_time_list = []
        start_time = time.time()
        #size = 0
        i = 0

        while(time.time() - start_time < 10):
        #while(size < 1073741824):       # 1 gig
        #while(size < 5368709120):      # 5 gigs
        #for i in range(21):
            folder_path = 'output_images/'
            for cam in cam_list:
                try:
                    ui_time = time.perf_counter()
                    ts = datetime.datetime.now()

                    ####
                    #print("\t{0: <25}".format("retrieving image..."), "------>", end = "")
                    #timestamp = time.perf_counter()
                    ####
                    cam.get_image()
                    ####
                    #print(time.perf_counter() - timestamp, "seconds")
                    ####
                    score = 0
                    image_name = cam.camera_id + "_" + ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%H:%M:%S.%f")[:-3] + ".jpg"
                    grayImage = cv2.cvtColor(cam.newImage, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(folder_path + image_name, grayImage)
                    cam.newImage = Image.open(folder_path + image_name)
                    if i >= 1:
                        timestamp = time.perf_counter()
                        score = compare_ssim(cam.oldImage, cam.newImage)
                        print("\tDifference calculations: {}".format(time.perf_counter() - timestamp), "seconds")
                        ####
                        # print("\tSSIM {} : {}".format(i, 1 - score))

                    if score < threshold:
                        cam.last_dif_check = time.time()
                        cam.oldImage = cam.newImage
                        cam.store_interval = store_interval
                        # size += cam.image_size

                        # object detection
                        timestamp = time.perf_counter()
                        ####
                        bounding_box = detection.getBbox(tensors, folder_path, image_name, sess)# [['1', '1', 1, 1, 1, 1]]
                        isprocessed = 1
                        ####
                        print("\tObject Detection: {}".format(time.perf_counter() - timestamp), "seconds")

                        # store into database
                        timestamp = time.perf_counter()
                        self.db.insert_image(folder_path, image_name, cam.camera_id, isprocessed, bounding_box)
                        print("\tImage Insertion: {}".format(time.perf_counter() - timestamp), "seconds")

                        #fi_time = time.perf_counter() - ui_time
                        #ui_time_list.append(fi_time)

                    elif time.time() - cam.last_dif_check >= cam.store_interval:
                        cam.last_dif_check = time.time()
                        cam.oldImage = cam.newImage

                        # object detection
                        # size += cam.image_size
                        timestamp = time.perf_counter()
                        ####
                        bounding_box = detection.getBbox(tensors, folder_path, image_name, sess)# [['1', '1', 1, 1, 1, 1]]
                        isprocessed = 1
                        ####
                        print("\tObject Detection: {}".format(time.perf_counter() - timestamp, "seconds"))

                        # Store into database
                        timestamp = time.perf_counter()
                        self.db.insert_image(folder_path, image_name, cam.camera_id, isprocessed, bounding_box)
                        print("\tImage Insertion: {}".format(time.perf_counter() - timestamp, "seconds"))

                        #fi_time = time.perf_counter() - ui_time
                        #ui_time_list.append(fi_time)
                        # print(cam.store_interval)

                        if (1 - score) < (1 - threshold) / 2:
                            cam.store_interval *= 2
                            # print(cam.store_interval)

                    print("\tSingle Round for cam {}: {} seconds\n".format(cam.camera_id, time.perf_counter() - ui_time))

                    '''try:
                        os.remove(folder_path + image_name)
                    except Exception as e2:
                        #print(e2)
                        pass'''

                except Exception as e:
                    print(e)
                    pass
            i += 1

        #print("{0: <25}".format("Interval between images"), "------>", time.perf_counter() - gb_time)

        '''ith open('image_upload_times.csv', 'w', newline='') as file1:
            ui_writer = csv.writer(file1)
            ui_writer.writerow(['Camera Upload Times'])
            for i in ui_time_list:
                ui_writer.writerow([i])'''
