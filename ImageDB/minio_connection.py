# Author: Haoran Wang
# Purpose: Batch Download Images from Minio Server

from minio import Minio
from minio.error import ResponseError

import sys
import pandas as pd
import subprocess as sp
import time
import datetime


class MinioConn:

    # Constructor
    def __init__(self, endpoint, access, secret):
        self.endpoint = endpoint
        self.access = access
        self.secret = secret

    # Connect Minio Client to Minio Server
    def connect_to_minio_server(self, endpoint, access, secret):
        return Minio(endpoint, access_key=access, secret_key=secret, secure=False)

    # Read in CSV file and output a data frame
    def read_csv(self, csv_file_name):
        return pd.read_csv(csv_file_name, sep=',', header=0, engine='python')

    # Create temp folder
    def mkdir_cmd(self, folder_name):
        cmd = "mkdir " + folder_name
        # print(cmd)
        sp.call(cmd, shell=True)

    # Compress the folder and deliver a .tar file
    def tar_cmd(self, folder_name):
        cmd = "tar -cvf " + folder_name + ".tar " + folder_name
        sp.call(cmd, shell=True)

    # Delete temp folder
    def rm_cmd(self, folder_name):
        cmd = "rm -r " + folder_name
        sp.call(cmd, shell=True)

    # Batch download
    def batch_download(self, mc, df):

        start_time = time.time()

        # File name is named after time stamp
        ts = datetime.datetime.now()
        folder_name = ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%I.%M.%S_%p")

        # Extract from Data Frame
        file_names = df.File_Names.tolist()
        bucket_name = df.Bucket_Name.tolist()

        # Check if two lists are valid before proceeding
        for i in range(file_names.__len__()):
            if isinstance(file_names[i], str) is False or isinstance(bucket_name[i], str) is False or \
                    file_names[i] == "" or bucket_name[i] == "":
                print("Please Fix CSV Before Proceeding")
                sys.exit()

        # Make a folder named with timestamp
        MinioConn.mkdir_cmd(self, folder_name)

        # Get a full object and prints the original object stat information.
        try:
            for i in range(file_names.__len__()):
                mc.fget_object('nyc', file_names[i], './' + folder_name + '/' + file_names[i])
        except ResponseError as err:
            print(err)

        # Compress temp folder
        MinioConn.tar_cmd(self, folder_name)

        # Delete temp folder
        MinioConn.rm_cmd(self, folder_name)

        print("===============================================================")
        print("Finished in --%s-- seconds" % (time.time() - start_time))


'''

if __name__ == '__main__':
    new_mc = MinioConn('localhost:9000', 'FX770DGQ10M2ALSRVX3F', 'qCO+rTTAGoPdaf5m39dleP5+vr9f15sCT0RGAbLl')

    df = new_mc.read_csv('nyc_traffic_sample.csv')

    mc = new_mc.connect_to_minio_server(new_mc.endpoint, new_mc.access, new_mc.secret)

    new_mc.batch_download(mc, df)
'''
