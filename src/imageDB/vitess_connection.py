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


	# drop test table IF NEEDED
	def dropCameraTable(self):
		self.mycursor.execute('drop table IF EXISTS CAMERA')
		print('CAMERA table dropped.')

	# drop test table IF NEEDED
	def dropImageTable(self):
		self.mycursor.execute('drop table IF EXISTS IMAGE_VIDEO')
		print('IMAGE_VIDEO table dropped.')

	# drop test table IF NEEDED
	def dropFeatureTable(self):
		self.mycursor.execute('drop table IF EXISTS FEATURE')
		print('FEATURE table dropped.')

	# drop test table IF NEEDED
	def dropRelationTable(self):
		self.mycursor.execute('drop table IF EXISTS RELATION')
		print('RELATION table dropped.')

	# drop test table IF NEEDED
	def dropBoxTable(self):
		self.mycursor.execute('drop table IF EXISTS BOUND_BOX')
		print('BOUND_BOX table dropped.')

	# CREATE CAMERA TABLE IF NEEDED
	def createCameraTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM CAMERA LIMIT 1')
			print('CAMERA table exist')

		except:
			# create table
			self.mycursor.execute('CREATE TABLE CAMERA(Camera_ID VARCHAR(25), type VARCHAR(6),\
									Country VARCHAR(30), State VARCHAR(30), City VARCHAR(30), \
									Latitude VARCHAR(15), Longitude VARCHAR(15), \
									Resolution_w VARCHAR(5), Resolution_h VARCHAR(5), \
									Ip VARCHAR(15), Port VARCHAR(5), Image_path VARCHAR(100), Video_path VARCHAR(100), \
									Snapshot_url VARCHAR(300), m3u8_url VARCHAR(50),\
									PRIMARY KEY (Camera_ID))')
			print('CAMERA table created.')


	# CREATE IMAGE TABLE IF NEEDED
	def createImageTable(self):
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
		try:
			self.mycursor.execute('SELECT 1 FROM FEATURE LIMIT 1')
			print('FEATURE table exist')

		except:
			## create table
			self.mycursor.execute('CREATE TABLE FEATURE(Feature_ID VARCHAR(36) NOT NULL, Feature_Name VARCHAR(10) NOT NULL, \
			PRIMARY KEY (Feature_ID))')
			print('FEATURE table created.')


	def createRelationTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM RELATION LIMIT 1')
			print('RELATION table exist.')

		except:
			## create table
			self.mycursor.execute('CREATE TABLE RELATION(Feature_ID VARCHAR(36) NOT NULL, IV_ID VARCHAR(36) NOT NULL, Feature_Num INT, \
			PRIMARY KEY (Feature_ID, IV_ID))')
			print('RELATION table created.')


	# INSERT the element from the input into the database
	# camera is tuple

	def createBoxTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM BOUND_BOX LIMIT 1')
			print('BOUND_BOX table exist.')
		except:
			## create table
			self.mycursor.execute('CREATE TABLE BOUND_BOX(IV_ID VARCHAR(36), Feature_ID VARCHAR(36), Confidence VARCHAR(5), Xmin VARCHAR(10), Xmax VARCHAR(10), Ymin VARCHAR(10), Ymax VARCHAR(10), PRIMARY KEY(IV_ID, Feature_ID, Xmin, Xmax, Ymin, Ymax))')
			print('BOUND_BOX table created.')

	def insertCamera(self, camera):

		sql = 'INSERT INTO CAMERA(Camera_ID, type, Country, State, City, Latitude, Longitude, Resolution_w, Resolution_h, \
				Ip, Port, Image_path, Video_path, Snapshot_url, m3u8_url) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), type = VALUES(type), Country=VALUES(Country), State=VALUES(State), \
				City=VALUES(City), Latitude=VALUES(Latitude), Longitude=VALUES(Longitude), \
				Resolution_w=VALUES(Resolution_w), Resolution_h=VALUES(Resolution_h), \
				Ip=VALUES(Ip), Port= VALUES(Port), Image_path=VALUES(Image_path), Video_path=VALUES(Video_path), \
				Snapshot_url=VALUES(Snapshot_url), m3u8_url=VALUES(m3u8_url)'

		self.mycursor.execute(sql, camera)

	# mannual commit after calling the method
	def insertCameras(self, cameras):

		sql = 'INSERT INTO CAMERA(Camera_ID, type, Country, State, City, Latitude, Longitude, Resolution_w, Resolution_h, \
				Ip, Port, Image_path, Video_path, Snapshot_url, m3u8_url) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), type = VALUES(type), Country=VALUES(Country), State=VALUES(State), \
				City=VALUES(City), Latitude=VALUES(Latitude), Longitude=VALUES(Longitude), \
				Resolution_w=VALUES(Resolution_w), Resolution_h=VALUES(Resolution_h), \
				Ip=VALUES(Ip), Port= VALUES(Port), Image_path=VALUES(Image_path), Video_path=VALUES(Video_path), \
				Snapshot_url=VALUES(Snapshot_url), m3u8_url=VALUES(m3u8_url)'

		self.mycursor.executemany(sql, cameras)

	# Update the camera information in the camera table
	# Update using Camera_ID as key and so first swap the order of tuple elements
	def updateCamera(self, camera):

		camID = camera[0]
		camData = camera[1:]
		data = (camData, camID) # The tuple with Camera_ID as the last element

		sql = 'UPDATE CAMERA SET \
				Country=%s, State=%s, City=%s, Latitude=%s, Longitude=%s \
				Ip=%s, Port=%s, Image_path=%s, Video_path=%s, Snapshot_url=%s, m3u8_url=%s\
				WHERE Camera_ID=%s'

		self.mycursor.executemany(sql, data)

	# this function get image_video ID of a image_video name
	def getIVID(self, image_video_name):
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
		sql = 'INSERT INTO FEATURE(Feature_ID, Feature_Name) VALUES (%s, %s)'
		self.mycursor.execute(sql, feature)


	# this function takes a list of feature_ID-image_ID tuples
	def insertImagefeatures(self, relations):
		sql = 'INSERT IGNORE INTO RELATION(Feature_ID, IV_ID, Feature_Num) VALUES (%s, %s, %s)'
		self.mycursor.execute(sql, relations)


	def insertBox(self, bound_boxes):
		sql = 'INSERT INTO BOUND_BOX(IV_ID, Feature_ID, Confidence, Xmin, Xmax, Ymin, Ymax) VALUES (%s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				IV_ID=VALUES(IV_ID),Feature_ID=VALUES(Feature_ID), Confidence=VALUES(Confidence), Xmin=VALUES(Xmin), Xmax=VALUES(Xmax), Ymin=VALUES(Ymin), Ymax=VALUES(Ymax)'
		self.mycursor.execute(sql,bound_boxes)


	def getAllCameras(self):
		'''
		This function get all the cameras in the camera table, store in cam_data as

	    ip: data[0] -> camera id                non-ip: data[0] -> camera id            Stream: data[0] -> camera id
	        data[1] -> camera type                      data[1] -> camera type                  data[1] -> camera type
	        data[2] -> camera ip address                data[2] -> snpashot_url                 data[2] -> m3u8 url
	        data[3] -> image path
	        data[4] -> video path

		'''
		cam_data = []
		#try:
		self.mycursor.execute("SELECT Camera_ID, type, Ip, Image_path, Video_path FROM CAMERA WHERE type='ip'")
		cam_data.extend(self.mycursor.fetchall())

		self.mycursor.execute("SELECT Camera_ID, type, Snapshot_url FROM CAMERA WHERE type='non-ip'")
		cam_data.extend(self.mycursor.fetchall())

		self.mycursor.execute("SELECT Camera_ID, type, m3u8_url FROM CAMERA WHERE type='stream'")
		cam_data.extend(self.mycursor.fetchall())

		return cam_data

	'''this function takes a dictionary of arguments and queries the Vitess database, returns 0 if no results are found,
	-1 if there was an error in the query response and the results if matches were found.'''
	def getImage(self,arguments):
		query = "SELECT CAMERA.CAMERA_ID, IMAGE_VIDEO.IV_ID, IMAGE_VIDEO.IV_date, IMAGE_VIDEO.IV_time, IMAGE_VIDEO.Minio_link, IMAGE_VIDEO.Dataset FROM IMAGE_VIDEO INNER JOIN CAMERA ON IMAGE_VIDEO.Camera_ID = CAMERA.Camera_ID WHERE "
		image_arguments = ["date","start_time","end_time"]
		camera_arguments = ["latitude","longitude","city","state","country","Camera_ID"]
		feature_parameters = arguments["feature"]
		if feature_parameters is not None:
			features = "("
			for feat in feature_parameters:
				features += "'"+ feat +"'" + ","
			features = features[:-1]
			features += ")"
		camera_parameters = ""
		for arg in camera_arguments:
			if arguments[arg] is not None:
				camera_parameters = camera_parameters + "CAMERA."+ arg + " = " +"'"+ str(arguments[arg])+"'" + " AND "
		image_parameters = ""
		if arguments["date"] is not None:
			image_parameters = image_parameters + "IMAGE_VIDEO.IV_date = " + str(arguments["date"]) + " AND "
		if arguments["start_time"] is not None:
			image_parameters = image_parameters + "IMAGE_VIDEO.IV_time BETWEEN " + "'" + str(arguments["start_time"])+"'" + " AND " + "'"+str(arguments["end_time"])+"'"

		image_parameters = image_parameters[:-5] if image_parameters.endswith("AND ") else image_parameters
		camera_parameters = camera_parameters[:-5] if len(image_parameters) == 0 else camera_parameters
		if len(camera_parameters) == 0 and len(image_parameters) == 0:
			query = query[:-7]

		else:
			query = query + camera_parameters + image_parameters
		
		if feature_parameters is None:
			fquery = query + ";"
		else:
			fquery = "SELECT aTable.Camera_ID, aTable.IV_ID, aTable.IV_date, aTable.IV_time, aTable.Minio_link, aTable.Dataset FROM (SELECT RELATION.IV_ID FROM RELATION left join FEATURE on RELATION.Feature_ID = FEATURE.Feature_ID WHERE Feature_Name IN " + features
			fquery += ") AS bTable INNER JOIN (" + query + ") AS aTable ON aTable.IV_ID = bTable.IV_ID;"
		result = ""
		try:
			#print(fquery)
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
		query = "SELECT Camera_ID, IV_ID, IV_date, IV_time, Minio_link, Dataset FROM IMAGE_VIDEO"

		self.mycursor.excute(query)
		results = self.mycursor.fetchall()
		if self.mycursor.rowcount == 0:
			return 0
		else:
			return results