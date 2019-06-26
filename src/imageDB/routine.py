import time
import sys
import os
import numpy as np
import datetime
#from crontab import CronTab
from imageDB import ImageDB
from camera import Camera, Ip_Camera, Non_Ip_Camera, Stream
from check_active import *
import detection.image_demo as detection
from time_measurements import TimeMeasurements


class Routine:
    def __init__(self):
        self.db = ImageDB()
        self.tm = TimeMeasurements()
        
    # Retrieve image from camera every second
    def retrieveImage(self, threshold, max_fps, store_interval):
        # Set up cameras
        cam_data = self.db.get_all_cameras()
        cam_list = []
        for data in cam_data:
            if data[1] == "ip":
                cam = Ip_Camera(camera_id=data[0], camera_type=data[1], ip_address=data[2], image_path=data[3], video_path=data[4])
            elif data[1] == "non-ip":
                cam = Non_Ip_Camera(camera_id=data[0], camera_type=data[1], snapshot_url=data[2])
            else:
                cam = Stream(camera_id=data[0], camera_type=data[1], m3u8_url=data[2])
            cam_list.append(cam)
        
        # TODO: Check if output_images folder exists
        ui_time = 0
        ui_time_list = []
        loop_start_time = time.time()
        while (time.time() - loop_start_time < 120):
            folder_path = 'output_images/'
            for cam in cam_list:
                try:
                    ui_time = time.time()
                    ts = datetime.datetime.now()
                    cam.get_image()
                    image_name = cam.camera_id + "_" + ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%H:%M:%S") + ".jpg"
                    difference = np.count_nonzero(np.absolute(cam.oldImage - cam.newImage)) / cam.image_size

                    if difference > threshold:
                        cam.last_dif_check = time.time()
                        cam.oldImage = cam.newImage
                        cam.store_interval = store_interval
                        cv2.imwrite(folder_path + image_name, cam.newImage)

                        # object detection
                        bounding_box = detection.getBbox(folder_path, image_name)

                        # If there's no error raised from object detection
                        isprocessed = 1


                        # store into database
                        self.db.insert_image(folder_path, image_name, cam.camera_id, isprocessed, bounding_box)
                        ui_time = time.time() - ui_time
                        ui_time_list.append(ui_time)

                    elif time.time() - cam.last_dif_check >= cam.store_interval:
                        cam.last_dif_check = time.time()
                        cam.oldImage = cam.newImage
                        cv2.imwrite(folder_path + image_name, cam.newImage)

                        # object detection
                        bounding_box = detection.getBbox(folder_path, image_name)

                        # If there's no error raised from object detection
                        isprocessed = 1

                        # Store into database
                        self.db.insert_image(folder_path, image_name, cam.camera_id, isprocessed, bounding_box)
                        ui_time = time.time() - ui_time
                        ui_time_list.append(ui_time)

                        if difference < threshold/2:
                            cam.store_interval *= 2

                    try:
                        os.remove(folder_path + image_name)
                    except Exception as e2:
                        pass

                except Exception as e:
                    print(e)
                    pass

        self.tm.WriteUploadTimes(ui_time_list)