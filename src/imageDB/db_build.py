from imageDB import ImageDB
from vitess_connection import VitessConn
from minio_connection import MinioConn
import detection.utils as utils
from camera import Camera
import config
import uuid
import sys
import cv2
import csv
import time


# Update the Camera Table by get the Updated Camera Information from CAM2DB
class DBbuild:
    """
    This class is used to set up and update different parts of the database.
    """
    def __init__(self):
        """
        Initialize database and vitess
        """

        self.db = ImageDB()
        self.vitess = VitessConn()
        self.minio = MinioConn()

    def start(self, filename):
        """
        Initialize all the tables and insert camera data.

        :param filename: .csv file containing saved camera information
        """

        self.db.init_tables()
        self.db.single_insert_camera(filename)
        self.vitess.mydb.commit()

    def append(self, filename):
        """
        Insert camera data to the current tables.

        :param filename: .csv file containing new camera information
        """

        self.db.single_insert_camera(filename)
        self.db.batch_insert_camera(filename)

    def fill(self):
        """
        Insert camera data to the current tables from the API.

        """

        self.db.batch_insert_camera_from_api()

    def feature(self, filename):
        """
        ?

        :param filename: .csv file containing ...
        """
        try:
            classes = utils.read_class_names(filename)

            for i in range(len(classes)):
                self.vitess.insertFeature(tuple([str(uuid.uuid1()), classes[i]]))
                if self.minio.mc.bucket_exists(classes[i]) is False:
                    self.minio.create_bucket(classes[i])
            if self.minio.mc.bucket_exists("none") is False:
                self.minio.create_bucket("none")

            self.vitess.mydb.commit()

            print("Features Inserted")
        except:
            print("Error inserting feature or creating bucket")

    def update(self, filename):
        """
        Update the resolution of all cameras within the .csv file given
        as an argument.

        :param filename: .csv file containing camera information
        """

        cam_info, cam_header = self.db.read_data(filename, config.CAM_HEADER, 'tuple', None)

        with open('updated_camera_list.csv', mode='w') as csv_file:
            cam_writer = csv.writer(csv_file, delimiter=',')
            cam_writer.writerow(cam_header)

            for info in cam_info:
                cam = Camera(camera_id=info[0], ip_address=info[8], image_path=info[10], video_path=info[11])
                cam.capture = cv2.VideoCapture(cam.video_path)
                cam.get_image()

                if cam.newImage is not None:
                    img_w = cam.newImage.shape[0]
                    img_h = cam.newImage.shape[1]

                cam_writer.writerow([info[0], info[1], info[2], info[3], info[4], info[5],
                                  img_w, img_h, info[8], info[9], info[10], info[11]])
                cam.capture.release()
                print('updated camera: {}'.format(info[0]))

        csv_file.close()

    def queryTest(self):
        """
        ??
        :return:
        """
        # Query 1
        label = 'person'
        start_query = time.time()
        self.vitess.allFramesWithFeature(label)
        end_query1 = time.time() - start_query

        # Query 2
        Timestamp1 = '14:43:00'
        Timestamp2 = '14:43:10'
        CountryName = 'MA'
        StateName = 'Null'
        start_query = time.time()
        frames_between_timestamps = self.vitess.framesBetweenTimestamps(Timestamp1, Timestamp2, CountryName, StateName)
        end_query2 = time.time() - start_query

        # Query 3
        start_query = time.time()
        self.vitess.findOneImage()
        end_query2 = time.time() - start_query


if __name__ == '__main__':
    """
    This file takes in two argument inputs
    argv[1] is mode (start, append, feature, update, fill, or queryTest)
    argv[2] is the csv file name
    """

    imgDB_build = DBbuild()

    if sys.argv[1] == 'start':
        imgDB_build.start(sys.argv[2])

    elif sys.argv[1] == 'append':
        imgDB_build.append(sys.argv[2])

    elif sys.argv[1] == 'feature':
        imgDB_build.feature(sys.argv[2])

    elif sys.argv[1] == 'update':
        imgDB_build.update(sys.argv[2])

    elif sys.argv[1] == 'fill':
        imgDB_build.fill()

    elif sys.argv[1] == 'queryTest':
        imgDB_build.queryTest()
