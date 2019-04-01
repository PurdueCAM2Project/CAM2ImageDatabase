import sys
import os.path
import csv
import config
from connect_vitess import VitessConn
#import pandas as pd



'''
When this file been called, it will create ### two ### tables first,
the CAMERA table, and the IMAGE/VIDEO table,
and then the content of CAMERA.csv and IV.csv file will be added to
these two tables.


## the input, content of csv file, need to be decided ##

For now, the CAMERA.csv file would looks something similar to

-------------------------------------------------------------------------------------------------------
| Transaction id | Expired | Country | City     | Latitude | Longtitude | Resolution_w | Resolution_h | 
-------------------------------------------------------------------------------------------------------
|         000001 |       0 | USA     | Boston   |  42.3692 |   -71.0658 |         2048 |         1536 |
-------------------------------------------------------------------------------------------------------
|         000002 |       0 | USA     | New York |  40.7047 |   -74.0211 |         1024 |          768 |
-------------------------------------------------------------------------------------------------------
...

and the IV.csv file would looks something similar to

----------------------------------------------------------------------------------------------------------------------
| IV_id      | Transaction id | iv_ date   | iv_time  | file type | file size | minio link | data set | is processed |
----------------------------------------------------------------------------------------------------------------------
| 0000000001 |         000001 | 2019-01-02 | 13:38:22 | PNG       | 1.4 MB    | None       | None     |            0 |
----------------------------------------------------------------------------------------------------------------------
| 0000000002 |         000001 | 2019-01-03 | 14:57:19 | JPEG      | 390 KB    | None       | None     |            0 |
----------------------------------------------------------------------------------------------------------------------
...


'''


class Datafile:
	data = None
	length = None

	# camera_data stores the metadata of camera
	# camera_bool check whether the data is valid
	def __init__(self):
		self.check = True
		self.camera_data = []
		self.camera_bool = False
		
		self.iv_data = []
		self.iv_bool = False
		
		self.feature_data = []
		self.feature_bool = False
		
		self.ifdata = []
		self.if_bool = False

	def read_data_to_obj(self, filename, required_header):

		# check which csv file we are reading
		if required_header == config.CAM_HEADER:
			csv_data = self.camera_data
			bool_result = self.camera_bool
		elif required_header == config.IV_CSV:
			csv_data = self.iv_data
			bool_result = self.iv_bool
		elif required_header == config.FEAT_CSV:
			csv_data = self.feature_data
			bool_result = self.feature_bool
		else:
			print "Invalid request header."
			print
			self.check = False
			return

		# if it is valid dataset
		if (set(csv_data[0]) == required_header):

			# remove header 
			# Error checking for null field will be handled by sql
			csv_data = csv_data[1:]

		elif (len(csv_data[0]) < len(required_header)):
			print "File", filename, "is missing required column."
			print
			self.check = False
			return
		elif (len(csv_data[0]) > len(required_header)):
			print "File", filename, "exceed the expected number of columns."
			print
			self.check = False
			return
		else:
			print "File", filename, "is missing header."
			print
			self.check = False
			return
			
		bool_result = True

	def read_csv_to_data(self, filename, file_content): 

		try:
			with open(filename, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				if (file_content == config.CAM_CSV):
					self.camera_data = list(reader)
				elif (file_content == config.IV_CSV):
					self.iv_data = list(reader)
				elif (file_content == config.FEAT_CSV):
					self.feature_data = list(reader)
		except:
			print "The file", filename, "does not exist"
			print
			self.check = False
			return

	def readData(self, file_content, filename):
		
		
			
		elif (file_content == config.IV_CSV):
			try:
				self.iv_data = []
				with open(filename, 'rb') as csvfile:
					spamreader = csv.reader(csvfile, delimiter='|')
					for row in spamreader:
						if (row[0] != ',,,,,,,'):
							temp = row[0].split(",")
							self.iv_data.append(temp)
				if (self.iv_data[0] == ["iv_id", "Transaction id", "iv_date",\
															 "iv_time", "file type", "file size",\
															 "minio link", "data set", "is processed"]):
					self.iv_data = self.iv_data[1:]
				elif (len(self.iv_data[0]) < 9):
					print "File", filename, "is missing required column."
					print
					self.check = False
					return
				elif (len(self.iv_data[0]) > 9):
					print "File", filename, "exceed the expected number of columns."
					print
					self.check = False
					return
				self.iv_bool = True
			except:
				print "The imagevideo file", filename, "does not exist"
				print
				self.check = False
				return
			
		elif (file_content == config.FEAT_CSV):
			try:
				self.feature_data = []
				with open(filename, 'rb') as csvfile:
					spamreader = csv.reader(csvfile, delimiter='|')
					for row in spamreader:
						temp = row[0].split(",")
						self.feature_data.append(temp)   
				self.feature_bool = True
			except:
					print "The feature file", filename, "does not exist"
					print
					self.check = False
					return
				
		else:
			try:
				self.ifdata = []
				with open(filename, 'rb') as csvfile:
					spamreader = csv.reader(csvfile, delimiter='|')
					for row in spamreader:
						temp = row[0].split(",")
						self.ifdata.append(temp)   
				self.if_bool = True
			except:
				print "The imagefeature file", filename, "does not exist"
				print
				self.check = False
				return

def main():
	if (len(sys.argv) < 5):
		print "Please use the format"
		print ">> python connect_vitess.py <camera filename> <image&video filename> <feature filename> <image&feature filename>"
		print
		print "If does not have any of the file, use None"
		print ">> python connect_vitess.py <camera filename> None None None"
		print
		return
	else:
		camera_file = sys.argv[1]
		iv_file = sys.argv[2]
		feature_file = sys.argv[3]
		if_file = sys.argv[4]

	for i in range (1,5):
		if (sys.argv[i] != "None"):
			name, ext = os.path.splitext(sys.argv[i])
			if (ext != ".csv"):
				print "Only accept the csv file type"
				print
				return

	## read file
	data = Datafile()
		
	if (camera_file != "None"):
		camera_data = Datafile()
		camera_data.readData(config.CAM_CSV, camera_file)

	if (iv_file != "None"):
		iv_data = Datafile()
		iv_data.readData(config.IV_CSV, iv_file)

	if (feature_file != "None"):
		feature_data = Datafile()
		feature_data.readData(config.FEAT_CSV, iv_file)

	if (if_file != "None"):
		if_data = Datafile()
		if_data.readData(config.IF_RELATION_CSV, if_file)

	if (not camera_data.check or not iv_data or not feature_data or not if_data ):
		return
	
	## initialize newData
	newData = VitessConn(camera_data.camera_data, iv_data.iv_data, feature_data.feature_data, \
												if_data.ifdata)

	## drop test table
	#newData.dropCameraTable()
	#newData.dropImageTable()

	## create and insert data table

	if (camera_data.camera_bool):
		newData.createCameraTable()
		newData.insertCamera()

	if (iv_data.iv_bool):
		newData.createImageTable()
		newData.insertImage()

	if (feature_data.feature_bool):
		newData.createFeatureTable()
		newData.insertFeature()

	if (if_data.if_bool):
		newData.createImagefeature()
		newData.insertImagefeature()
	

main()
	


