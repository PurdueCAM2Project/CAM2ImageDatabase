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

os.environ["GPU_MAX_HEAP_SIZE"] = "60"

class Routine:
    def __init__(self):
        self.db = ImageDB()


    def retrieveImage(self, media_list, is_real_camera, threshold, store_interval, PID, num_proc, class_dict, classes):

        """
        This function performs the following:
        1. Opens cameras and retrieves images
        2. Compares the retrieved image with the last stored image
        3. Makes decision to store retrieved image based on difference results
        4. Passes image to be stored through object detection
        5. Passes the image and image feature information to be inserted into Vitess and Minio

        :param media_list:          list,  camera information to be initialized
        :param is_real_camera:      bool,  True if a real camera
                                           False if a test video
        :param threshold:           float, value representing threshold for difference calculations
        :param store_interval:      float, how long before the old images from a camera needs to be updated (seconds)
        :param PID:                 int,   process id
        :param num_proc:            int,   number of processes
        :param class_dict:          dict,  dictionary of objects that can be detected and their id's
        """
        from SSIM_PIL import compare_ssim

        print ('Process {}: {}'.format(PID, media_list))
        folder_path = "output_images/"
        information = ""
        runtime = 0
        information += "querying camera data..." + "------>"
        timestamp = time.perf_counter()

        cam_list = []
        k = 0
        for media in media_list:
            if is_real_camera == 'ip':
                cam = setup_cams(media)
                cam.number = k
            else:
                cam = setup_vids(media, PID, is_real_camera, k)
                cam.number = k
            k += 1
            cam_list.append(cam)

        information += str(time.perf_counter() - timestamp) + " seconds\n"
        yolo = YOLO(PID, classes)
        # TODO: Check if output_images folder exists
        start_time = time.time()

        size = 0
        i = 0
        j = 0

        count_proc1 = 0
        count_proc2 = 0
        count_proc3 = 0

        start_time = time.time()
        flag = True
        store_size = 0
        #while flag == True:
        while(time.time() - start_time < 180):
            # Track cycles for each process
            if PID == 0:
                count_proc1 += 1
            elif PID == 1:
                count_proc2 += 1
            else:
                count_proc3 += 1

            # Run each camera in camera list
            for cam in cam_list:
                try:
                    # Start time of one single round
                    ui_time = time.perf_counter()

                    # Date string for image name
                    ts = datetime.datetime.now()

                    # Information will be a long string of time performance written to a text file
                    information += "retrieving image ------>"

                    timestamp = time.perf_counter()

                    # Download image from current camera
                    cam.get_image()

                    image_date = ts.strftime("%Y-%m-%d")
                    image_time = ts.strftime("%H:%M:%S.%f")[:-3]
                    j += 1

                    information += str(time.perf_counter() - timestamp) + "seconds\n"

                    # Score is the old and new image difference value
                    score = 0
                    image_name = cam.camera_id + "_" + image_date + "_" + image_time + ".jpg"

                    # Crop image to increase accuracy and speed of difference calculations
                    # TODO: Cropping for ip and public_vid flags
                    # TODO: Perform Automatic cropping
                    '''
                    if is_real_camera != 'our_vid':
                        cropImage = cam.newImage[cam.crop_y_max:cam.crop_y_min, cam.crop_x_max:cam.crop_x_min]
                    else:
                        cropImage = cam.newImage
                    '''
                    cropImage = cam.newImage[cam.crop_y_max:cam.crop_y_min, cam.crop_x_max:cam.crop_x_min]

                    # Comparison of old and new image
                    npImage = Image.fromarray(cropImage)
                    image_size = getsizeof(cam.newImage)
                    size += image_size
                    # If oldImage exits compare with the new image
                    if cam.oldImage:
                        timestamp = time.perf_counter()  # Time stamp to see how long difference calculation takes
                        score = compare_ssim(cam.oldImage, npImage)
                        information += "Difference calculations: " + str(time.perf_counter() - timestamp) + "seconds\n"
                    # If old and new image difference score is less than the minimum threshold difference percentage...
                    if score < threshold:
                        # Record current time for last difference check
                        cam.last_dif_check = time.time()

                        # Overwrite new image as the old image
                        cam.oldImage = npImage

                        # Reset store interval
                        cam.store_interval = store_interval

                        cv2.imwrite(folder_path + image_name, cam.newImage)
                        store_size += os.stat('./' + folder_path + image_name).st_size

                        # object detection
                        timestamp = time.perf_counter()
                        bounding_box = yolo.predict(cam.newImage)
                        isprocessed = 1

                        information += "Object Detection: " + str(time.perf_counter() - timestamp) + "seconds\n"

                        # store into database
                        path = folder_path + image_name

                        timestamp = time.perf_counter()
                        self.db.insert_image(image_name, cam.camera_id, isprocessed, bounding_box, classes, image_date,
                                             image_time, image_size, class_dict, path)

                        information += "Image Insertion: " + str(time.perf_counter() - timestamp) + "seconds\n"

                    # If the interval between current time and last difference check is greater than store interval
                    elif time.time() - cam.last_dif_check >= cam.store_interval:
                        cam.last_dif_check = time.time()
                        cam.oldImage = npImage
                        cv2.imwrite(folder_path + image_name, cam.newImage)
                        store_size += os.stat('./' + folder_path + image_name).st_size

                        # object detection
                        timestamp = time.perf_counter()
                        bounding_box = yolo.predict(cam.newImage)
                        isprocessed = 1

                        information += "Object Detection: " + str(time.perf_counter() - timestamp) + "seconds\n"

                        # Store into database
                        path = folder_path + image_name

                        # Inserting images and features into database
                        timestamp = time.perf_counter()
                        self.db.insert_image(image_name, cam.camera_id, isprocessed, bounding_box, classes, image_date,
                                             image_time, image_size, class_dict, path)

                        information += "Image Insertion: " + str(time.perf_counter() - timestamp) + "seconds\n"

                        # If the difference score is the meeting the minimum threshold, double the store interval
                        if (1 - score) < (1 - threshold) / 2:
                            cam.store_interval *= 2


                    try:
                        os.remove(path)
                    except:
                        pass


                    # Tracking the run time for cameras
                    if cam.oldImage:
                        runtime += time.perf_counter() - ui_time

                    # Adding time information to text file
                    information += "Single Round for cam " + cam.camera_id + ":" + str(time.perf_counter() - ui_time) \
                                   + "seconds\n"
                    information += "\n"

                except Exception as e:
                    print(e)
                    cam_list.remove(cam)
                    if len(cam_list) == 0:
                        flag = False

                    pass
            cam.frames = cam.frames + 1
            i += 1


        print("Number of frames processed for {} : {}".format(PID, j))
        print("Runtime for process {}: {}".format(PID, runtime), " seconds")
        print("Processed size: {}".format(size))
        print("store size : {}".format(store_size))

        with open ('output.txt', 'a') as f:
            f.write("Number of frames processed for {} : {}\n".format(PID, j))
            f.write("Runtime for process {}: {} seconds\n".format(PID, runtime))
            f.write("Processed size: {}\n".format(size))            #Size written to file is in bytes
            f.write("Stored size: {}\n".format(store_size))         #Size written to file is in bytes
            f.write("\n")
        cam.capture.release()

        for cam in cam_list:
            print("ID: {}".format(cam.camera_id), ", Number of frames processed = {}".format(cam.frames))

        file = open('image_upload_times.txt', 'w')
        file.write(information)
        file.close()
