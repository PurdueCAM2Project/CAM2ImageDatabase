#!/usr/bin/env python3

# When using this class, all transactions invloving
# DML(data manipulation language), including insert, delete, update, etc.,
# needs to be commited by calling [vitessConnObject].mydb.commit()
# and [vitessConnObject].mydb.rollback() when thrwoing exception

# Developers are encouraged to lookup the diffrence between DDL and DML in SQL

import _mysql_connector
import mysql.connector
from mysql.connector import errorcode

import sys
import config


class VitessConn:

    # connect to the mysql
    def __init__(self):

        # Define database
        mydatabase = config.KEYSPACE

        try:
            self.mydb = mysql.connector.connect(
                host=config.VITESS_HOST,
                #user='root',
                #password='',
                port=config.VITESS_PORT,
                database = mydatabase,
                auth_plugin=config.VITESS_PASS
            )
            print('Connected to mysql database ' + mydatabase)
        except mysql.connector.Error as err:
            print(str(err))
            sys.exit()
        except _mysql_connector.MySQLInterfaceError as e:
            print(str(e))
            sys.exit()
        except Exception as e:
            print(str(e))
            sys.exit()

        self.mycursor = self.mydb.cursor(buffered=True)


    def dropCameraTable(self):
        """
        drop Camera table if it exists
        """
        self.mycursor.execute('drop table IF EXISTS CAMERA')
        print('CAMERA table dropped.')

    def dropImageTable(self):
        """
        drop Image table if it exists
        """
        self.mycursor.execute('drop table IF EXISTS IMAGE_VIDEO')
        print('IMAGE_VIDEO table dropped.')

    def dropFeatureTable(self):
        """
        drop Feature table if it exists
        """
        self.mycursor.execute('drop table IF EXISTS FEATURE')
        print('FEATURE table dropped.')

    def dropRelationTable(self):
        """
        drop Relation table if it exists
        """
        self.mycursor.execute('drop table IF EXISTS RELATION')
        print('RELATION table dropped.')

    def dropBoxTable(self):
        """
        drop Bounding Box table if it exists
        """
        self.mycursor.execute('drop table IF EXISTS BOUND_BOX')
        print('BOUND_BOX table dropped.')

    def dropCropImgTable(self):
        """
        drop Cropped Image table if it exists
        """
        self.mycursor.execute('drop table IF EXISTS CROPPED_IMAGE')
        print('CROPPED_IMAGE table dropped.')

    # CREATE CAMERA TABLE IF NEEDED
    def createCameraTable(self):
        """
        create Camera table if it does not exists
        """

        try:
            self.mycursor.execute('SELECT 1 FROM CAMERA LIMIT 1')
            print('CAMERA table exist')

        except:
            # create table
            self.mycursor.execute('CREATE TABLE CAMERA(Camera_ID VARCHAR(25),\
									Country VARCHAR(30), State VARCHAR(30), City VARCHAR(30), \
									Latitude VARCHAR(15), Longitude VARCHAR(15), \
									Resolution_w VARCHAR(5), Resolution_h VARCHAR(5), Ip VARCHAR(15), Port VARCHAR(5), \
									Image_path VARCHAR(100), Video_path VARCHAR(100), Fps VARCHAR(5)\
									PRIMARY KEY (Camera_ID))')
            print('CAMERA table created.')


    # CREATE IMAGE TABLE IF NEEDED
    def createImageTable(self):
        """
        create Image table if it does not exists
        """

        try:
            self.mycursor.execute('SELECT 1 FROM IMAGE_VIDEO LIMIT 1')
            print('IMAGE_VIDEO table exist')
        except:
            ## create table
            self.mycursor.execute('CREATE TABLE IMAGE_VIDEO(IV_ID VARCHAR(36) NOT NULL, IV_Name VARCHAR(50) NOT NULL, Camera_ID VARCHAR(25) NOT NULL, \
									IV_date DATE NOT NULL, IV_time TIME NOT NULL, \
									File_type VARCHAR(5) NOT NULL, File_size VARCHAR(10) NOT NULL, \
									Minio_link VARCHAR(100) NOT NULL, Dataset VARCHAR(10) NOT NULL, Is_processed INT NOT NULL, \
									PRIMARY KEY (IV_ID))')

            print('IMAGE_VIDEO table created.')


    # CREATE FEATURE TABLE IF NEEDED
    def createFeatureTable(self):
        """
        create Feature table if it does not exists
        """

        try:
            self.mycursor.execute('SELECT 1 FROM FEATURE LIMIT 1')
            print('FEATURE table exist')

        except:
            ## create table
            self.mycursor.execute('CREATE TABLE FEATURE(Feature_ID VARCHAR(36) NOT NULL, Feature_Name VARCHAR(10) NOT NULL, \
			PRIMARY KEY (Feature_ID))')
            print('FEATURE table created.')


    def createRelationTable(self):
        """
        create Relation table if it does not exists
        """

        try:
            self.mycursor.execute('SELECT 1 FROM RELATION LIMIT 1')
            print('RELATION table exist.')

        except:
            ## create table
            self.mycursor.execute('CREATE TABLE RELATION(Feature_ID VARCHAR(36) NOT NULL, IV_ID VARCHAR(36) NOT NULL, Feature_Num INT, \
			PRIMARY KEY (Feature_ID, IV_ID))')
            print('RELATION table created.')

    def createBoxTable(self):
        """
        create Bounding Box table if it does not exists
        """

        try:
            self.mycursor.execute('SELECT 1 FROM BOUND_BOX LIMIT 1')
            print('BOUND_BOX table exist.')
        except:
            ## create table
            self.mycursor.execute('CREATE TABLE BOUND_BOX(IV_ID VARCHAR(36), Feature_ID VARCHAR(36), Confidence VARCHAR(30), Xmin VARCHAR(30), Xmax VARCHAR(30), Ymin VARCHAR(30), Ymax VARCHAR(30), PRIMARY KEY(IV_ID, Feature_ID, Xmin, Xmax, Ymin, Ymax))')
            print('BOUND_BOX table created.')

    def createCropImgTable(self):
        """
        create Cropped Image table if it does not exists
        """

        try:
            self.mycursor.execute('SELECT 1 FROM CROPPED_IMAGE LIMIT 1')
            print('CROPPED_IMAGE table exist')

        except:
            # create table
            self.mycursor.execute('CREATE TABLE CROPPED_IMAGE(Camera_ID VARCHAR(25), \
									Xmin VARCHAR(10), Xmax VARCHAR(10), Ymin VARCHAR(10), Ymax VARCHAR(10)\
									PRIMARY KEY (Camera_ID))')
            print('CROPPED_IMAGE table created.')

    # INSERT the element from the input into the database
    # camera is tuple
    def insertCamera(self, camera):
        """
        Inserts information of one camera

        :param camera:      list, camera information
        """

        sql = 'INSERT INTO CAMERA(Camera_ID, Country, State, City, Latitude, Longitude, Resolution_w, Resolution_h, \
				Ip, Port, Image_path, Video_path) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), Country=VALUES(Country), State=VALUES(State), \
				City=VALUES(City), Latitude=VALUES(Latitude), Longitude=VALUES(Longitude), \
				Resolution_w=VALUES(Resolution_w), Resolution_h=VALUES(Resolution_h), \
				Ip=VALUES(Ip), Port= VALUES(Port), Image_path=VALUES(Image_path), Video_path=VALUES(Video_path)'

        self.mycursor.execute(sql, camera)

    # mannual commit after calling the method
    def insertCameras(self, cameras):
        """
        Inserts information of multiple camera

        :param cameras:         list, list of camera information
        """

        sql = 'INSERT INTO CAMERA(Camera_ID, Country, State, City, Latitude, Longitude, Resolution_w, Resolution_h, \
				Ip, Port, Image_path, Video_path) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), Country=VALUES(Country), State=VALUES(State), \
				City=VALUES(City), Latitude=VALUES(Latitude), Longitude=VALUES(Longitude), \
				Resolution_w=VALUES(Resolution_w), Resolution_h=VALUES(Resolution_h), \
				Ip=VALUES(Ip), Port= VALUES(Port), Image_path=VALUES(Image_path), Video_path=VALUES(Video_path)'

        self.mycursor.executemany(sql, cameras)

    # Update the camera information in the camera table
    # Update using Camera_ID as key and so first swap the order of tuple elements
    def updateCamera(self, camera):
        """
        Updates information for a camera in Vitess using Camera ID as key. Ensure Camera ID is the first element
        in camera

        :param camera:      tuple, updated camera information with Camera ID as key
        """

        camID = camera[0]
        camData = camera[1:]
        data = (camData, camID) # The tuple with Camera_ID as the last element

        sql = 'UPDATE CAMERA SET \
				Country=%s, State=%s, City=%s, Latitude=%s, Longitude=%s \
				Ip=%s, Port=%s, Image_path=%s, Video_path=%s\
				WHERE Camera_ID=%s'

        self.mycursor.executemany(sql, data)

    # this function get image_video ID of a image_video name
    def getIVID(self, image_video_name):
        """
        Queries Vitess for input image_video name and return its ID

        :param image_video_name:        str, name of image
        :return:                        str, ID of image
        """

        # see if the feature already exist
        # if so, return the feature ID
        sql = 'SELECT IV_ID FROM IMAGE_VIDEO WHERE IV_Name = \'' + image_video_name + '\''
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        result = list(sum(result, ()))
        if(len(result) > 0):
            return result[0]
        return None

    # Insert one image tuple
    def insertImage(self, image):
        """
        Inserts image metadata into Vitess

        :param image:       list, image metadata
        """

        sql = 'INSERT INTO IMAGE_VIDEO(IV_ID, IV_Name, Camera_ID, IV_date, IV_time, File_type, File_size, \
				Minio_link, Dataset, Is_processed) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), IV_date=VALUES(IV_date), IV_time=VALUES(IV_time), \
				File_type=VALUES(File_type), File_size=VALUES(File_size), \
				Minio_link=VALUES(Minio_link), Dataset=VALUES(Dataset), Is_processed=VALUES(Is_processed)'

        self.mycursor.execute(sql, image)

    # this function get feature ID of a feature name
    def getFeature(self, featureName):
        """
        Queries Vitess for feature and return its ID

        :param featureName:     str, name of feature
        :return:                str, ID of feature
        """

        # see if the feature already exist
        # if so, return the feature ID
        sql = 'SELECT Feature_ID FROM FEATURE WHERE Feature_Name = \'' + featureName + '\''
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        result = list(sum(result, ()))
        if(len(result) > 0):
            return result[0]
        return None

    # this function takes in a list of feature tuples (Feature_ID, Feature_Name)
    def insertFeature(self, feature):
        """
        Inserts feature and its ID into Vitess

        :param feature:     tuple, feature id and feature anme
        """

        try:
            sql = 'INSERT INTO FEATURE(Feature_ID, Feature_Name) VALUES (%s, %s)'
            self.mycursor.execute(sql, feature)
        except Exception as e:
            print(e)
            sys.exit()

    # this function takes a list of feature_ID-image_ID tuples
    def insertImagefeatures(self, relations):
        """
        Inserts feature ID, image ID and number of occurrence of feature into Vitess

        :param relations:       tuple, feature id, image id, feature num
        """

        sql = 'INSERT IGNORE INTO RELATION(Feature_ID, IV_ID, Feature_Num) VALUES (%s, %s, %s)'
        self.mycursor.execute(sql, relations)

    def insertBox(self, bound_boxes):
        """
        Inserts a list of bounding boxes into Vitess

        :param bound_boxes:         tuple, image id, feature id, confidence, coordinates
        """

        sql = 'INSERT INTO BOUND_BOX(IV_ID, Feature_ID, Confidence, Xmin, Xmax, Ymin, Ymax) VALUES (%s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				IV_ID=VALUES(IV_ID),Feature_ID=VALUES(Feature_ID), Confidence=VALUES(Confidence), Xmin=VALUES(Xmin), Xmax=VALUES(Xmax), Ymin=VALUES(Ymin), Ymax=VALUES(Ymax)'
        self.mycursor.execute(sql,bound_boxes)

    def getAllCameras(self, num_of_cams):
        """
        Queries Vitess of a given number of cameras based on input

        :param num_of_cams:         int, number of desired cameras
        :return:                    list, information for desired number of cameras
        """

        '''
        This function get all the cameras in the camera table, store in cam_data as

        ip: data[0] -> camera id                non-ip: data[0] -> camera id            Stream: data[0] -> camera id
            data[1] -> camera type                      data[1] -> camera type                  data[1] -> camera type
            data[2] -> camera ip address                data[2] -> snpashot_url                 data[2] -> m3u8 url
            data[3] -> image path
            data[4] -> video path

        '''
        cam_data = []
        self.mycursor.execute("SELECT Camera_ID, Ip, Image_path, Video_path FROM CAMERA LIMIT {}".format(num_of_cams))
        cam_data.extend(self.mycursor.fetchall())
        return cam_data

    '''this function takes a dictionary of arguments and queries the Vitess database, returns 0 if no results are found,
    -1 if there was an error in the query response and the results if matches were found.'''
    def getImage(self, arguments):
        """
        This function takes a dictionary of arguments and queries for images in the Vitess database, returns 0
		if no results are found, -1 if there was an error in the query response and the results if matches  were found.

        :param arguments:       dict, set of arguments to base query upon
        :return:                list, results of image query
        """

        query = "SELECT CAMERA.CAMERA_ID, IMAGE_VIDEO.IV_ID, IMAGE_VIDEO.IV_date, IMAGE_VIDEO.IV_time, " \
                "IMAGE_VIDEO.Minio_link, IMAGE_VIDEO.Dataset FROM IMAGE_VIDEO INNER JOIN CAMERA ON " \
                "IMAGE_VIDEO.Camera_ID = CAMERA.Camera_ID WHERE "

        # image_arguments = ["date", "start_time", "end_time"]
        camera_arguments = ["latitude", "longitude", "city", "state", "country", "Camera_ID"]
        feature_parameters = arguments["feature"]
        if feature_parameters is not None:
            features = "("
            for feat in feature_parameters:
                features += "'" + feat + "'" + ","
            features = features[:-1]
            features += ")"
        camera_parameters = ""
        for arg in camera_arguments:
            if arguments[arg] is not None:
                camera_parameters = camera_parameters + "CAMERA." + arg + " = " + "'" + str(arguments[arg])+ "'" \
                                    + " AND "
        image_parameters = ""
        if arguments["date"] is not None:
            image_parameters = image_parameters + "IMAGE_VIDEO.IV_date = " + str(arguments["date"]) + " AND "
        if arguments["start_time"] is not None:
            image_parameters = image_parameters + "IMAGE_VIDEO.IV_time BETWEEN " + "'" + str(arguments["start_time"]) \
                               + "'" + " AND " + "'" + str(arguments["end_time"]) + "'"

        image_parameters = image_parameters[:-5] if image_parameters.endswith("AND ") else image_parameters
        camera_parameters = camera_parameters[:-5] if len(image_parameters) == 0 else camera_parameters
        if len(camera_parameters) == 0 and len(image_parameters) == 0:
            query = query[:-7]

        else:
            query = query + camera_parameters + image_parameters

        if feature_parameters is None:
            fquery = query + ";"
        else:
            fquery = "SELECT aTable.Camera_ID, aTable.IV_ID, aTable.IV_date, aTable.IV_time, aTable.Minio_link, " \
                     "aTable.Dataset FROM (SELECT RELATION.IV_ID FROM RELATION left join FEATURE " \
                     "on RELATION.Feature_ID = FEATURE.Feature_ID WHERE Feature_Name IN " + features
            fquery += ") AS bTable INNER JOIN (" + query + ") AS aTable ON aTable.IV_ID = bTable.IV_ID;"
        try:
            print(fquery)
            self.mycursor.execute(fquery)
            result = self.mycursor.fetchall()
            if self.mycursor.rowcount == 0:
                return 0
            else:
                return result

        except:
            print("There was an error in the image query response")
            return -1

    def getImageV2(self, arguments):
        """
        This function is an edited version of getImage. It works the same way except the feature argument here queries
        image bucket and not detected features in image.

        :param arguments:       dict, set of arguments to base query upon
        :return:                list, results of image query
        """

        query = "SELECT CAMERA.CAMERA_ID, IMAGE_VIDEO.IV_ID, IMAGE_VIDEO.IV_date, IMAGE_VIDEO.IV_time, " \
                "IMAGE_VIDEO.Minio_link, IMAGE_VIDEO.Dataset FROM IMAGE_VIDEO INNER JOIN CAMERA ON " \
                "IMAGE_VIDEO.Camera_ID = CAMERA.Camera_ID WHERE "

        # image_arguments = ["date", "start_time", "end_time"]
        camera_arguments = ["latitude", "longitude", "city", "state", "country", "Camera_ID"]
        feature_parameters = arguments["feature"]
        if feature_parameters is not None:
            features = "("
            for feat in feature_parameters:
                features += "'" + feat + "'" + ","
            features = features[:-1]
            features += ")"
        camera_parameters = ""
        for arg in camera_arguments:
            if arguments[arg] is not None:
                camera_parameters = camera_parameters + "CAMERA." + arg + " = " + "'" + str(arguments[arg]) + "'" + \
                                    " AND "
        image_parameters = ""
        if arguments["date"] is not None:
            image_parameters = image_parameters + "IMAGE_VIDEO.IV_date = " + str(arguments["date"]) + " AND "
        if arguments["start_time"] is not None:
            image_parameters = image_parameters + "IMAGE_VIDEO.IV_time BETWEEN " + "'" + str(arguments["start_time"]) \
                               + "'" + " AND " + "'" + str(arguments["end_time"]) + "'"

        image_parameters = image_parameters[:-5] if image_parameters.endswith("AND ") else image_parameters
        camera_parameters = camera_parameters[:-5] if len(image_parameters) == 0 else camera_parameters
        if len(camera_parameters) == 0 and len(image_parameters) == 0:
            query = query[:-7]

        else:
            query = query + camera_parameters + image_parameters

        if feature_parameters is None:
            fquery = query + ";"
        else:
            fquery = "SELECT aTable.Camera_ID, aTable.IV_ID, aTable.IV_date, aTable.IV_time, aTable.Minio_link, " \
                     "aTable.Dataset FROM (SELECT IMAGE_VIDEO.IV_ID FROM IMAGE_VIDEO WHERE IMAGE_VIDEO.Minio_link IN " \
                     + features + " AND IMAGE_VIDEO.Dataset IN ('bucket')"

            fquery += ") AS bTable INNER JOIN (" + query + ") AS aTable ON aTable.IV_ID = bTable.IV_ID;"

        try:
            print(fquery)
            self.mycursor.execute(fquery)
            result = self.mycursor.fetchall()
            if self.mycursor.rowcount == 0:
                return 0
            else:
                return result
        except:
            print("There was an error in the image query response")
            return -1

    def getAll(self):
        """
        Queries Vitess of all images

        :return:        list, all images in Vitess
        """

        query = "SELECT Camera_ID, IV_ID, IV_date, IV_time, Minio_link, Dataset FROM IMAGE_VIDEO"

        self.mycursor.execute(query)
        results = self.mycursor.fetchall()
        if self.mycursor.rowcount == 0:
            return 0
        else:
            return results

    def clearTable(self, table_name):
        """
        Empties a table in Vitess

        :param table_name:      str, name of table
        """

        try:
            sql = "DELETE FROM " + table_name
            self.mycursor.execute(sql)
            self.mydb.commit()
        except Exception as e:
            print(e)
            sys.exit()

    def allFramesWithFeature(self, feature_name):
        """

        :param feature_name:
        :return:
        """

        query = "SELECT IV_Name, Minio_link FROM IMAGE_VIDEO WHERE IV_ID IN (SELECT IV_ID FROM BOUND_BOX WHERE Feature_ID = (SELECT Feature_ID FROM FEATURE WHERE Feature_name='%s'))" %(feature_name)

        self.mycursor.execute(query)
        results = self.mycursor.fetchall()
        print (results)

        return results

    def framesBetweenTimestamps(self, Timestamp1, Timestamp2,CountryName,StateName):
        """

        :param Timestamp1:
        :param Timestamp2:
        :param CountryName:
        :param StateName:
        :return:
        """

        query = "SELECT IV_NAME FROM IMAGE_VIDEO WHERE Camera_ID=(SELECT Camera_ID FROM CAMERA WHERE Country='%s' AND State='%s') AND IV_time BETWEEN '%s' AND '%s' ORDER BY IV_time" %(CountryName, StateName, Timestamp1, Timestamp2)
        self.mycursor.execute(query)
        results = self.mycursor.fetchall()
        #print (results2)
        return results

    def findOneImage(self):
        """

        :return:
        """

        query = ""

        self.mycursor.execute(query)
        results = self.mycursor.fetchall()

        return results
