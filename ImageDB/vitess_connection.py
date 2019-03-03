#!/usr/bin/env python3

# When using this class, all transactions invloving 
# DML(data manipulation language), including insert, delete, update, etc.,
# needs to be commited by calling [vitessConnObject].mydb.commit()
# and [vitessConnObject].mydb.rollback() when thrwoing exception

# Developers are encouraged to lookup the diffrence between DDL and DML in SQL

import mysql.connector
from mysql.connector import errorcode

class VitessConn:

	# connect to the mysql
	def __init__(self):

		# Define database
		mydatabase = 'test_keyspace'
	
		try:
			self.mydb = mysql.connector.connect(
				host='127.0.0.1',
				#user='root',
				#password='',
				port='15306',
				database = mydatabase,
				auth_plugin='mysql_native_password'
			)
			print('Connected to mysql database ' + mydatabase)
			
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print('Something is wrong with your user name or password.')
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print('Database does not exist')
			else:
				print(err)
			return

		self.mycursor = self.mydb.cursor(buffered=True)


	# drop test table IF NEEDED
	def dropCameraTable(self):
		self.mycursor.execute('drop table IF EXISTS CAMERA')
		print('CAMERA table dropped.')

	# drop test table IF NEEDED
	def dropImageTable(self):
		self.mycursor.execute('drop table IF EXISTS IMAGE_VIDEO')
		print('IMAGE_VIDEO table dropped.')
		

	# CREATE CAMERA TABLE IF NEEDED
	def createCameraTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM CAMERA LIMIT 1')
			print('CAMERA table exist')
			
		except:
			# create table
			self.mycursor.execute('CREATE TABLE CAMERA(Camera_ID INT NOT NULL,\
									Country VARCHAR(30) NOT NULL, State VARCHAR(30), City VARCHAR(30) NOT NULL, \
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
			self.mycursor.execute('CREATE TABLE IMAGE_VIDEO(IV_ID INT, Camera_ID INT, \
									IV_date DATE, IV_time TIME, \
									File_type VARCHAR(10), File_size VARCHAR(10), \
									Minio_link VARCHAR(500), Dataset VARCHAR(500), Is_processed INT, \
									PRIMARY KEY (IV_ID))')
													
			print('IMAGE_VIDEO table created.')


	# CREATE FEATURE TABLE IF NEEDED	
	def createFeatureTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM FEATURE LIMIT 1')
			print('FEATURE table exist')
		except:
			## create table
			self.mycursor.execute('CREATE TABLE FEATURE(Feature_ID INT, \
									Feature_Name VARCHAR(100)')
			print('Feature table created.')


	def createImagefeatureTable(self):
		try:
			self.mycursor.execute('SELECT 1 FROM RELATION LIMIT 1')
			print('RELATION table exist.')
		except:
			## create table
			self.mycursor.execute('CREATE TABLE RELATION(Feature_ID INT NOT NULL, \
									IV_ID INT NOT NULL, PRIMARY KEY (Feature_ID, IV_ID))')
			print('Relation table created.')


	# INSERT the element from the input into the database
	# camera is tuple

	# mannual commit after calling the method
	def insertCameras(self, cameras):
		
		sql = 'INSERT INTO CAMERA(Camera_ID, Country, State, City, Latitude, Longitude, \
				Resolution_w, Resolution_h) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
				ON DUPLICATE KEY UPDATE \
				Camera_ID=VALUES(Camera_ID), Country=VALUES(Country), State=VALUES(State), \
				City=VALUES(City), Latitude=VALUES(Latitude), Longitude=VALUES(Longitude)'

		self.mycursor.executemany(sql, cameras)

	# Insert one image tuple 
	def insertImage(self, image):

		sql = 'INSERT INTO IMAGE_VIDEO(IV_ID, Camera_ID, IV_date, IV_time, File_type, File_size, \
				Minio_link, Dataset, Is_processed) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

		self.mycursor.execute(sql, image)
		

	# this function get feature ID of a feature name
	def getFeature(self, featureName):

		# see if the feature already exist
		# if so, return the feature ID
		self.mycursor.execute('SELECT Feature_ID FROM feature WHERE Feature_Name=%s', featureName)
		result = self.mycursor.fetchall()
		if(len(result) > 0):
			return result[0]
		return None


	# this function takes in a list of feature tuples (Feature_ID, Feature_Name)
	def insertFeature(self, feature):

		sql = 'INSERT INTO feature(Feature_ID, Feature_Name) VALUES (%s, %s)'
		self.mycursor.execute(sql, feature)
		

	# this function takes a list of feature_ID-image_ID tuples
	def insertImagefeatures(self, relations):
		sql = 'INSERT INTO RELATION(Feature_ID, IV_ID) VALUES (%s, %s)'
		self.mycursor.executemany(sql, relations)
		
	
	## check permission if needed
	def select(self, tablename):
		self.mycursor.execute('SELECT * FROM ' + tablename)
		myresult = self.mycursor.fetchall()
		for x in myresult:
			print(x)
