#!/usr/bin/env python3

# When using this class, all transactions invloving 
# DML(data manipulation language), including insert, delete, update, etc.,
# needs to be commited by calling [vitessConnObject].mydb.commit()
# and [vitessConnObject].mydb.rollback() when thrwoing exception

# Developers are encouraged to lookup the diffrence between DDL and DML in SQL

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

	# CREATE CAMERA TABLE IF NEEDED
	def createCameraTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM CAMERA LIMIT 1')
			print('CAMERA table exist')
			
		except:
			# create table
			self.mycursor.execute('CREATE TABLE CAMERA(Camera_ID INT NOT NULL,\
									Country VARCHAR(30) NOT NULL, State VARCHAR(30) NOT NULL, City VARCHAR(30) NOT NULL, \
									Latitude FLOAT NOT NULL, Longitude FLOAT NOT NULL, \
									Resolution_w INT NOT NULL, Resolution_h INT NOT NULL, PRIMARY KEY (Camera_ID))')
			print('CAMERA table created.')
		

	# CREATE IMAGE TABLE IF NEEDED
	def createImageTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM IMAGE_VIDEO LIMIT 1')
			print('IMAGE_VIDEO table exist')		
		except:
			## create table      
			self.mycursor.execute('CREATE TABLE IMAGE_VIDEO(IV_ID VARCHAR(50) NOT NULL, IV_Name VARCHAR(500) NOT NULL, Camera_ID INT NOT NULL, \
									IV_date DATE NOT NULL, IV_time TIME NOT NULL, \
									File_type VARCHAR(10) NOT NULL, File_size VARCHAR(10) NOT NULL, \
									Minio_link VARCHAR(500) NOT NULL, Dataset VARCHAR(500) NOT NULL, Is_processed INT NOT NULL, \
									PRIMARY KEY (IV_ID))')
													
			print('IMAGE_VIDEO table created.')


	# CREATE FEATURE TABLE IF NEEDED	
	def createFeatureTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM FEATURE LIMIT 1')
			print('FEATURE table exist')
                              
		except:
			## create table
			self.mycursor.execute('CREATE TABLE FEATURE(Feature_ID VARCHAR(50) NOT NULL, Feature_Name VARCHAR(100) NOT NULL, PRIMARY KEY (Feature_ID))')
			print('FEATURE table created.')


	def createRelationTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM RELATION LIMIT 1')
			print('RELATION table exist.')
			
		except:
			## create table
			self.mycursor.execute('CREATE TABLE RELATION(Feature_ID VARCHAR(50) NOT NULL, IV_ID VARCHAR(50) NOT NULL, PRIMARY KEY (Feature_ID, IV_ID))')
			print('RELATION table created.')


	# INSERT the element from the input into the database
	# camera is tuple


	# mannual commit after calling the method
	def insertCameras(self, cameras):
		
		sql = 'INSERT INTO CAMERA(Camera_ID, Country, State, City, Latitude, Longitude, \
				Resolution_w, Resolution_h) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), Country=VALUES(Country), State=VALUES(State), \
				City=VALUES(City), Latitude=VALUES(Latitude), Longitude=VALUES(Longitude), \
				Resolution_w=VALUES(Resolution_w), Resolution_h=VALUES(Resolution_h)'

		self.mycursor.executemany(sql, cameras)



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
		sql = 'INSERT IGNORE INTO RELATION(Feature_ID, IV_ID) VALUES (%s, %s)'
		self.mycursor.executemany(sql, relations)
		
	
