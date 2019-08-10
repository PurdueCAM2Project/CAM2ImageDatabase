# Author: Haoran Wang
# Purpose: Batch Download Images from Minio Server

from minio import Minio
from minio.error import ResponseError

import sys
import pandas as pd
import subprocess as sp
import time
import datetime
import config
import io
import cv2
import numpy as np
import os

class MinioConn:

    # Constructor
    def __init__(self):

        self.endpoint = config.MINIO_ENDPOINT
        self.access_key = config.MINIO_ACCESS_KEY
        self.secret_key = config.MINIO_SECRET_KEY

        # Connect Minio Client to Minio Server
        self.mc = Minio(self.endpoint, access_key=self.access_key, secret_key=self.secret_key, secure=False)

    # Read in CSV file and output a data frame
    def read_csv(self, csv_file_name):
        """
        Reads csv file

        :param csv_file_name:
        :return:
        """

        return pd.read_csv(csv_file_name, sep=',', header=0, engine='python')

    # Create temp folder
    def mkdir_cmd(self, folder_name):
        """
        Makes a folder

        :param folder_name:     str, name of folder
        """

        cmd = "mkdir " + folder_name
        # print(cmd)
        sp.call(cmd, shell=True)

    # Compress the folder and deliver a .tar file
    def tar_cmd(self, folder_name):
        """
        Compress a folder

        :param folder_name:     str, name of folder
        """

        cmd = "tar -cvf " + folder_name + ".tar " + folder_name
        sp.call(cmd, shell=True)

    # Delete temp folder
    def rm_cmd(self, folder_name):
        """
        Removes a folder

        :param folder_name:     str, name of folder
        """

        cmd = "rm -r " + folder_name
        sp.call(cmd, shell=True)

    # TODO: I dont think we need this fuction
    # Batch download
    def batch_download(self, mc, df):

        start_time = time.time()

        # File name is named after time stamp
        ts = datetime.datetime.now()
        folder_name = ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%H:%M:%S")

        # Extract from Data Frame
        file_names = df.File_Names.tolist()
        bucket_name = df.Bucket_Name.tolist()
        bucket_link = df.Bucket_Link.tolist()

        # Check if two lists are valid before proceeding
        for i in range(file_names.__len__()):
            if isinstance(file_names[i], str) is False or isinstance(bucket_name[i], str) is False or  isinstance(bucket_link[i], str) is False or \
                    file_names[i] == "" or bucket_name[i] == "" or bucket_link[i] == "":
                print("Please Fix CSV Before Proceeding")
                sys.exit()

        # Make a folder named with timestamp
        MinioConn.mkdir_cmd(self, folder_name)

        # Get a full object and prints the original object stat information.
        try:
            for i in range(file_names.__len__()):
                #mc.fget_object(bucket_name[i], file_names[i], './' + folder_name + '/' + file_names[i])
                npImg = mc.get_object(bucket_name[i], file_names[i])
                img = np.frombuffer(npImg.read(), dtype='int')
                print(type(img))
                #cv2.imwrite('./' + folder_name + '/' + image_name, img)
        except ResponseError as err:
            print(err)

        # Compress temp folder
        MinioConn.tar_cmd(self, folder_name)

        # Delete temp folder
        MinioConn.rm_cmd(self, folder_name)

        print("===============================================================")
        print("Finished in --%s-- seconds" % (time.time() - start_time))

    #TODO: I think we should remove the other function and rename this
    def batch_video_download(self, mc, df, size_limit):
        """
        Downloads images from Minio

        :param mc:
        :param df:              dataframe, image name bucket name and minio link
        :param size_limit:      int, total size of images to download in MB
        :return:
        """
        start_time = time.time()
        size = 0
        folder_name = "output_images/"

        # Extract from Data Frame
        file_names = df.File_Names.tolist()
        bucket_name = df.Bucket_Name.tolist()
        bucket_link = df.Bucket_Link

        # Check if two lists are valid before proceeding
        for i in range(file_names.__len__()):
            if isinstance(file_names[i], str) is False or isinstance(bucket_name[i], str) is False or \
                    file_names[i] == "" or bucket_name[i] == "" or bucket_link[i] == "":
                print("Please Fix CSV Before Proceeding")
                sys.exit()

        # Get a full object and prints the original object stat information.
        #bucket_name[i]
        try:
            for i in range(file_names.__len__()):
                mc.fget_object(bucket_name[i], file_names[i], './' + folder_name + file_names[i] + '.jpg')

                img_size = os.path.getsize('./' + folder_name + file_names[i] + '.jpg')
                size += img_size

                if size >= size_limit * 1024 * 1024:
                    break
        except ResponseError as err:
            print(err)

        print("===============================================================")
        #print("Finished in --%s-- seconds" % (time.time() - start_time))
    # remove error handling, so that it can be caught in imageDB.py and allow rollback of vitess


    # Create a bucket on Minio server
    # Location choices: "us-east-1", "us-west-1", "us-west-2"
    def create_bucket(self, bucket_name, location='us-east-1'):
        """
        Creates a minio bucket

        :param bucket_name:         str, name of bucket
        :param location:            str, location of server
        """

        self.mc.make_bucket(bucket_name, location=location)

    # Upload a file from local storage to Minio server
    def upload_single_file(self, bucket_name, object_name, path):
        """
        Uploads image to Minio

        :param bucket_name:     str, name of bucket
        :param object_name:     str, name of image
        :param path:            str, local path where image is stored
        """

        self.mc.fput_object(bucket_name, object_name, path)


if __name__ == '__main__':
    new_mc = MinioConn()#('localhost:9000', 'FX770DGQ10M2ALSRVX3F', 'qCO+rTTAGoPdaf5m39dleP5+vr9f15sCT0RGAbLl')

    df = new_mc.read_csv('nyc_traffic_sample.csv')

    #mc = new_mc.connect_to_minio_server(new_mc.endpoint, new_mc.access_key, new_mc.secret_key)

    # new_mc.create_bucket(mc, "testing", "us-east-1")

    # new_mc.upload_single_file(mc, "testing", "myobject", "./test_image.jpg")

    # new_mc.batch_download(mc, df)

