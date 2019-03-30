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
import csv
import uuid
import codecs
import mysql.connector.errors as mysqlError
import config
from vitess_connection import VitessConn


class ImageDB:

    def __init__(self):

        # connect to Vitess-MySql and Minio

        self.vitess = VitessConn()
        # TODO: Haoran add a line for Mino connection
    
    def init_tables(self):
        # drop if needed
        '''
        self.vitess.dropCameraTable()
        self.vitess.dropImageTable()
        self.vitess.dropFeatureTable()
        self.vitess.dropRelationTable()
        '''
        self.vitess.createCameraTable()
        self.vitess.createImageTable()
        self.vitess.createFeatureTable()
        self.vitess.createRelationTable()
        

    # check if the given file has desired header
    @classmethod
    def check_header(self, csv_header, required_header):
        if required_header == config.IF_HEADER:
            # for image feature csv only, check if header is there is enough
            if csv_header[0] == required_header[0]:
                return 1
            else:
                raise ValueError('File does not having correct header.')
                return 0
        elif csv_header == required_header:
            return 1
        elif len(csv_header) < len(required_header):
            raise ValueError("File is missing required column.")
            return 0

        elif len(csv_header) > len(required_header):
            raise ValueError("File exceeds the expected number of columns.")
            return 0
        else:
            raise ValueError('File does not having correct header.')
            return 0


    # TODO: the csv file integrity check incorporate with Lakshya's code
    @classmethod
    def read_data(self, csv_file, required_header, data_format):
        header = []
        if data_format == 'dict':
            items = {}
        elif data_format == 'tuple' or data_format == 'list':
            items = []
        else:
            print('Must specify to read as dict, list of lists or tuples.')
            return 0, 0
        
        try:
            with open(csv_file, 'rb') as csvfile:
                reader = csv.reader(codecs.EncodedFile(csvfile, 'utf8', 'utf_8_sig'), delimiter=',')
                reader = list(reader)
                # check if it has the corret header
                if ImageDB.check_header(reader[0], required_header):
                    header = reader[0]
                    reader = reader[1:]
                    for i in reader:
                        if required_header == config.IF_HEADER and len(i) != len(header):
                            raise ValueError("Feature file content column does not match header.")
                        elif  required_header != config.IF_HEADER and len(i) != len(required_header):
                            raise ValueError("File content column does not match header.")
                        if data_format == 'tuple':
                            items.append(tuple(i))
                        elif data_format == 'list':
                            items.append(i)
                        elif data_format == 'dict':
                            # key: image file name; value: entire row (list)
                            items[i[0]] = i
                            
                    return items, header
                
                else:
                    return 0, 0
                
        except IOError as e:
            print('IOError({0}): {1}'.format(e.errno, e.strerror))
        except ValueError as e2:
            print('Error processing file ' + csv_file + repr(e2))
        except Exception as e3:
            print(e3)
            
        return 0, 0
            


    def batch_insert_camera(self, camera_csv):

        # camera_list is a list of tuple, each element is a row in csv
        camera_list, camera_header = ImageDB.read_data(camera_csv, config.CAM_HEADER, 'tuple')
        if camera_list and camera_header:
            try:
                # save it into vitess-mysql
                self.vitess.insertCameras(camera_list)
                self.vitess.mydb.commit()
                print('Camera metadata updated')
            except mysqlError as e:
                print('Error inserting cameras: ' + repr(e))
                self.vitess.mydb.rollback()
            except Exception as e2:
                print(e2)
        else:
            return 0


                   
    # this function should read image and image feature file, 
    def insert_image(self, image_csv, image_feature_csv=None):
        
        # image_list is a list of list, each element is a row in csv
        image_list, image_header = ImageDB.read_data(image_csv, config.IV_HEADER, 'list')

        # image feature relation dict
        # key: file name; value: csv row as list
        if image_feature_csv != None:
            relation_list, relation_header = ImageDB.read_data(image_feature_csv, config.IF_HEADER, 'dict')
    
        if image_list and image_header: 
            try:
                if relation_header:
                    for i in range(len(relation_header)):
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
                            f_id = str(uuid.uuid1())
                            self.vitess.insertFeature((f_id, relation_header[i]))
                            relation_header[i] = f_id

                # insert image with metadata and feature inside the database one-by-one
                for i in range(len(image_list)):

                    # image_list[i] is the i th row of image metadata
                    image_filename = image_list[i][0]
                    
                    # get image_video_id of the image_video
                    iv_id = self.vitess.getIVID(image_filename)
                    
                    if iv_id is not None:
                        image_id = iv_id
                    else:
                        image_id = str(uuid.uuid1())

                    # TODO: image file by file name in the folder to Minio
                    # change its file name to image_id value
                    # record the Minio name/bucket/link in the image_list

                    # substitude the filename with image_id
                    # NOW change to => add the image_id
                    image_list[i] = [image_id] + image_list[i]

                    # save image metadata to DB
                    self.vitess.insertImage(tuple(image_list[i][0:len(config.IV_HEADER)+1]))

                    # get list of feature ids that belong to this image
                    if relation_list:
                        feature_info_list = relation_list[image_filename]
                        
                        featureID_list = []
                        for i in range(len(feature_info_list)):
                            if i == 0:
                                continue
                            elif feature_info_list[i] == '1':
                                featureID_list.append(relation_header[i])
                        # zip into list of (feature id, image id) tuples
                        if_list = zip(tuple(featureID_list), tuple([image_id] * len(featureID_list)))
                        self.vitess.insertImagefeatures(if_list)

                self.vitess.mydb.commit()
                
                print('Image_Video metadata updated')
                
            except mysqlError as e:
                print('Error inserting cameras: ' + repr(e))
                self.vitess.mydb.rollback()
            except Exception as e2:
                print(e2)
        else:
            return 0

 
