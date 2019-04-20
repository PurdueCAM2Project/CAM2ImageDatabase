#!/usr/bin/env python3
'''
This file contains the main functionalities of the imageDB system.

----- Table Initialization -----

1. Initialize camera table
2. Initialize image table
3. Initialize feature table
4. Initialize image-feature relation table

----- Data Insertion -----

5. Insert camera data to camera table
6. Insert image data to image table
7. Insert image-feature data to feature table and image-feature relation table
8. Insert image/video to storage

----- Data Retrieval -----

9. Search image by feature, with constrains?
10. Get image by image ID list

----- Table Update -----

11. Add column to camera table
12. Add column to image table
13. Add column to image-feature relation table

----- Item Update -----

14. Update camera item
15. Update image item
16. Update feature item
17. Update image-feature relation item

----- To Be Added -----


'''
from vitess_connection import VitessConn
import config
import mysql.connector.Error as mysqlError
import uuid
import os

class ImageDB:

    def __init__(self):

        # connect to Vitess-MySql and Minio

        self.vitess = VitessConn()
        # TODO: Haoran add a line for Mino connection

    def init_tables(self):
        self.vitess.createCameraTable()
        self.vitess.createFeatureTable()
        self.vitess.createImagefeatureTable()
        self.vitess.createImageTable()

    # check if the given file has desired header
    @classmethod
    def check_header(csv_header, required_header):

        if required_header == config.IF_HEADER:
            # for image feature csv only, check if header is there is enough
            if csv_header[0] == required_header[0]:
                return
            else:
                raise ValueError('File does not having correct header.')
        elif csv_header == required_header:
            return
        elif len(csv_header) < len(required_header):
            raise ValueError("File is missing required column.")
        elif len(csv_header) > len(required_header):
            raise ValueError("File exceeds the expected number of columns.")
        else:
            raise ValueError('File does not having correct header.')

    # TODO: The csv file integrity check incorporate with Lakshya's code
    # TODO: Compare function needs the path to folder containing image files.
    #       This parameter needs to be added to the read_data function
    # TODO: Still need to check if files in folder exist in CSV. Would this be a separate function?
    @classmethod
    def read_data(csv_file, required_header, data_format, folder_path):
        # Get the list of files in the folder containing the images
        files_in_folder = os.listdir(folder_path)
        # List of names of files that are missing in either the CSV or folder
        missing_from_CSV = []
        missing_from_folder = []

        header = []
        if data_format == 'dict':
            items = {}
        else:
            items = []
        try:
            with open(csv_file, 'rb') as csvfile:
                # reader is the list of rows from the CSV
                reader = csv.reader(csvfile, delimiter=',')

                # Check if it has the corret header
                ImageDB.check_header(reader[0], required_header)
                header = reader[0]
                reader = reader[1:]

                for row in reader:
                    if len(row) != len(required_header):
                        raise ValueError("File content column does not match header.")
                    if data_format == 'tuple':
                        items.append(tuple(row))
                    elif data_format == 'list':
                        # If the data_format is a 'list' then it means that image files are being
                        # inserted. Comparison takes place here to check for file existance
                        items.append(row)

                        # Check if file name exists in the folder
                        if row[0] not in files_in_folder:
                            missing_from_folder.append(row[0])
                        # Else, if the file exists in both, remove it from the list of files in the folder. files_in_folder will be left with the files which aren't in the CSV
                        else:
                            files_in_folder.remove(row[0])

                        # If there are missing files, in the folder, print them
                        if missing_from_folder:
                            print("The following files are missing from the folder:")
                            print(missing_from_folder)

                        # If there are missing files, in the CSV, print them
                        if files_in_folder:
                            print("The following files are missing from the CSV:")
                            print(files_in_folder)

                    elif data_format == 'dict':
                        # key: image file name; value: entire row (list)
                        items[row[0]] = row
                    else:
                        print('Must specify to read as dict, list of lists or tuples.')
        except IOError as e:
            print('IOError({0}): {1}'.format(e.errno, e.strerror))
        except ValueError as e2:
            print('Error processing file ' + csv_file + repr(e2))
        except Exception as e3:
            print(e3)
        finally:
            return item_list, header

    def batch_insert_camera(self, camera_csv):

        # camera_list is a list of tuple, each element is a row in csv
        camera_list, camera_header = ImageDB.read_data(camera_csv, config.CAM_HEADER, 'tuple')
        try:
            # save it into vitess-mysql
            self.vitess.insertCameras(camera_list)
            self.vitess.mydb.commit()

        except mysqlError as e:
            print('Error inserting cameras: ' + repr(e))
            self.vitess.mydb.rollback()
        except Exception as e2:
            print(e2)

    # this function should read image and image feature file,
    def insert_image(self, image_csv, image_feature_csv=None):

        # image_list is a list of list, each element is a row in csv
        image_list, image_header = ImageDB.read_data(image_csv, config.IV_HEADER, 'list')

        # image feature relation dict
        # key: file name; value: csv row as list
        relation_list, relation_header = ImageDB.read_data(image_feature_csv, config.IF_HEADER, 'dict')

        try:
            # Process the image feature header list to a list of feature ids (except for first entry)

            for i in len(relation_header):
                if i == 0:
                    continue
                # get featureID of the feature
                f_id = self.vitess.getFeature(relation_header[i])

                # check if the feature has already exists;
                # if not, create new feature in the feature table
                if f_id is not None:
                    relation_header[i] = f_id
                else:
                    # generate feature id, insert new feature
                    f_id = uuid.uuid1()
                    self.vitess.insertFeature((f_id, relation_header[i]))
                    relation_header[i] = f_id

            # insert image with metadata and feature inside the database one-by-one

            for i in len(image_list):

                # image_list[i] is the i th row of image metadata

                image_filename = image_list[i][0]
                image_id = uuid.uuid1()

                # TODO: image file by file name in the folder to Minio
                # change its file name to image_id value
                # record the Minio name/bucket/link in the image_list

                # substitude the filename with image_id
                image_list[i][0] = image_id
                # save image metadata to DB
                self.vitess.insertImage(tuple(image_list[i]))

                # get list of feature ids that belong to this image
                feature_info_list = relation_list[image_filename]
                featureID_list = []
                for i in feature_info_list:
                    if i == 0:
                        continue
                    elif feature_info_list[i] != 0:
                        featureID_list.append(relation_header[i])

                # zip into list of (feature id, image id) tuples

                if_list = zip(tuple(featureID_list), tuple([image_id] * len(featureID_list)))
                self.vitess.insertImagefeatures(if_list)

            self.vitess.mydb.commit()

        except mysqlError as e:
            print('Error inserting cameras: ' + repr(e))
            self.vitess.mydb.rollback()
        except Exception as e2:
            print(e2)
