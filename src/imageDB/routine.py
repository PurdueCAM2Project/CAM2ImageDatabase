import time
import sys
import os
import numpy as np
import datetime
from crontab import CronTab
from imageDB import ImageDB
from camera import Camera, Ip_Camera, Non_Ip_Camera, Stream
from check_active import *
import detection.image_demo as detection


class Routine:
    def __init__(self):
        self.db = ImageDB()

    # Read cameras from CAM2DB every month
    def updateCameraTable(self):
        '''try:
            cron = CronTab()
            job = cron.new(command='python updateCameraTable.py')
            job.every(1).month  # can change according to requirement (hours, week, month, etc.)
            cron.write('cronjob.tab')
        except:
            print('Error updating camera table')
            sys.exit()'''
        self.db.single_insert_camera('camera_list.csv')
        
        
    # Retrieve image from camera every second
    def retrieveImage(self, threshold, max_fps):
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
        
        
        while (True):
            #bucket_name = 'testhahaha5'
            folder_path = 'output_images/'
            for cam in cam_list:
                ts = datetime.datetime.now()
                image_name = cam.camera_id + "_" + ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%H:%M:%S") + ".jpg"

                # check whether reach the retrieve interval
                #if time.time() - cam.last_ret_check >= cam.ret_interval:
                    #cam = check_active(cam, max_fps)
                    # check whether the camera is active
                    # TODO: when stream type of camera working, add on is_active_video
                    #if cam.is_active_image:
                        
                        # check the difference between the current image and the previous image
                try:
                    cam.get_image()
                    difference = np.count_nonzero(np.absolute(cam.oldImage - cam.newImage)) / cam.image_size
                    if difference > threshold:
                        cam.oldImage = cam.newImage
                        cam.last_dif_check = time.time()
                        cam.store_interval = 0.1
                        cv2.imwrite(folder_path + image_name, cam.newImage)

                        isprocessed = 0

                        # object detection
                        bounding_box = detection.getBbox(folder_path, image_name)

                        # If there's no error raised from object detection    
                        if True:
                            isprocessed = 1

                        # store into database
                        self.db.insert_image(folder_path, image_name, cam.camera_id, isprocessed, bounding_box)

                    elif time.time() - cam.last_dif_check >= cam.store_interval:
                        cam.oldImage = cam.newImage
                        cam.last_dif_check = time.time()
                        cv2.imwrite(folder_path + image_name, cam.newImage)

                        isprocessed = 0

                        # object detection
                        bounding_box = detection.getBbox(folder_path, image_name)

                        # If there's no error raised from object detection    
                        if True:
                            isprocessed = 1

                        # Store into database
                        self.db.insert_image(folder_path, image_name, cam.camera_id, isprocessed, bounding_box)

                        if difference < threshold/2:
                            cam.store_interval *= 2

                    try:
                        os.remove(folder_path + image_name)
                    except Exception as e2:
                        pass

                except Exception as e:
                    print(e)
                    pass

            # sleep for 0.1 sec for every round
            time.sleep(0.1)


