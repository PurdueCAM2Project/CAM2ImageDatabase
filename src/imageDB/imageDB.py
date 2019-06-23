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

Minio
1. [Done] Insert Images to Minio Server
2. [Done] Batch Download Images taken a data frame object as input (reduce I/O)
3. [Done] Batch Download Images taken a CSV file as input (if user wants to download later)
4. Transaction Rollback mechanism

'''

import csv
import uuid
import sys
import os
from cv2 import cv2
import time
import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime
import config
from vitess_connection import VitessConn
from minio_connection import MinioConn

import detection.utils as utils
import detection.config as cfg

# minio error
from minio.error import ResponseError

class ImageDB:

	def __init__(self):

		# connect to Vitess-MySql and Minio
		self.vitess = VitessConn()
		self.minio = MinioConn()
		# self.minio = self.minio_conf.connect_to_minio_server(endpoint, access_key, secret_key)

	def init_tables(self):
		# drop if needed
		self.vitess.dropCameraTable()
		self.vitess.dropImageTable()
		self.vitess.dropFeatureTable()
		self.vitess.dropRelationTable()
		self.vitess.dropBoxTable()

		self.vitess.createCameraTable()
		self.vitess.createImageTable()
		self.vitess.createFeatureTable()
		self.vitess.createRelationTable()
		self.vitess.createBoxTable()

	# check if the given file has desired header
	@classmethod
	def check_header(self, csv_file, csv_header, required_header):

		if required_header == config.IF_HEADER:
			# for image feature csv only, check if header is there is enough
			if csv_header[0] == required_header[0]:
				return 1
			else:
				raise ValueError('\nFile ' + csv_file + ' does not have required header.')
				return 0
		elif csv_header == required_header:
			return 1
		elif len(csv_header) < len(required_header):
			raise ValueError('\nFile ' + csv_file + ' is missing required column.')
			return 0

		elif len(csv_header) > len(required_header):
			raise ValueError('\nFile ' + csv_file + ' exceeds the expected number of columns.')
			return 0
		else:
			raise ValueError('\nFile ' + csv_file + ' does not have correct header. \nExpect: ' + str(required_header))
			return 0


	# TODO: the csv file integrity check incorporate with Lakshya's code
	@classmethod
	def read_data(self, csv_file, required_header, data_format, folder_path):
		# Get the list of files in the folder containing the images
		if data_format != 'tuple':
			files_in_folder = os.listdir(folder_path)

		# List of names of files that are missing in either the CSV or folder
		missing_from_CSV = []
		missing_from_folder = []

		header = []
		if data_format == 'dict':
			items = {}
		elif data_format == 'tuple' or data_format == 'list':
			items = []
		else:
			print('Must specify to read as dict, list of lists or tuples.')
			return 0, 0
		with open(csv_file, 'rt', encoding = 'utf-8-sig') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			reader = list(reader)
			# check if it has the corret header
			if ImageDB.check_header(csv_file, reader[0], required_header):
				header = reader[0]
				reader = reader[1:]
				for i in reader:
					if ((required_header == config.IF_HEADER and len(i) != len(header)) or
						(required_header != config.IF_HEADER and len(i) != len(required_header))):
						raise ValueError('\nFile ' + csv_file + ' content column does not match header.')

					# check whether there's empty value
					for j in i:
						if j == '':
							j = 'Null'

						if j == '':
							raise ValueError('\nFile ' + csv_file + ' content missing value.')

					if data_format == 'tuple':
						items.append(tuple(i))
					elif data_format == 'list':
						items.append(i)
					elif data_format == 'dict':
						# key: image file name; value: entire row (list)
						items[i[0]] = i
					else:
						raise ValueError('\nMust specify to read as dict, list of lists or tuples.')

					# If the data_format is not a 'tuple' then it means that image files are being
					# inserted. Comparison takes place here to check for file existance
					if data_format != 'tuple':

						if data_format == 'list':
							items.append(i)
						else:
							items[i[0]] = i

						# Check if file name exists in the folder
						if i[0] not in files_in_folder:
							missing_from_folder.append(i[0])
						# Else, if the file exists in both, remove it from the list of files in the folder.
						# files_in_folder will be left with the files which aren't in the CSV
						else:
							files_in_folder.remove(i[0])

						# If there are missing files, in the folder, print them
						if missing_from_folder:
							raise ValueError('\nFiles ' + str(missing_from_folder) + ' are missing from folder.')

						# If there are missing files, in the CSV, print them
						if missing_from_CSV:
							raise ValueError('\nFilenames ' + str(missing_from_CSV) + ' are missing from CSV.')

				return items, header

			else:
				return 0, 0

		return 0, 0

	def single_insert_camera(self, camera_csv):
		camera_list, camera_header = ImageDB.read_data(camera_csv, config.CAM_HEADER, 'tuple', None)
			
		if camera_list and camera_header:
			try:
				for cam in camera_list:					
					self.vitess.insertCamera(cam)
				print('Camera metadata updated')
				self.vitess.mydb.commit()
			except mysql.connector.Error as e:
				print('Error inserting cameras: ' + str(e))
				self.vitess.mydb.rollback()
			except Exception as e2:
				print(e2)
		else:
			print("Check Camera List and Header")
			return 0
		

	def batch_insert_camera(self, camera_csv):

		# camera_list is a list of tuple, each element is a row in csv
		camera_list, camera_header = ImageDB.read_data(camera_csv, config.CAM_HEADER, 'tuple', None)
		if camera_list and camera_header:
			try:
				'''# save it into vitess-mysql
				i=0

				# 50 is harded code number. May need to be chnaged for different csv file

				for i in range(0, len(camera_list) - 50, 5000):'''
				self.vitess.insertCameras(camera_list)#[i:i+5000])
				self.vitess.mydb.commit()
				print('Camera metadata updated')
			except mysql.connector.Error as e:
				print('Error inserting cameras: ' + str(e))
				self.vitess.mydb.rollback()
			except Exception as e2:
				print(e2)
		else:
			return 0


	def insert_BoundBox(self, boundbox_csv):
		''' name_list is a list of tuple, each element is a row in csv.
		It contains the image name, feature name along with bounding boxes. '''
		name_list, name_header = ImageDB.read_data(boundbox_csv, config.BOX_NAME_HEADER, 'tuple', None)

		''' boundboxes_list is a list of tuple, each element is a row(boundbox_list) in csv.
		It contains the image id, feature id along with bounding boxes. '''
		boundboxes_list = []
		boundbox_list = []

		i = 0
		while i < len(name_list):
			boundbox_list = [self.vitess.getIVID(name_list[i][0]), self.vitess.getFeature(name_list[i][1]), name_list[i][2], name_list[i][3], name_list[i][4], name_list[i][5]]
			boundboxes_list.append(boundbox_list)
			i += 1

		if boundboxes_list and config.BOX_HEADER: 
			try:
				# save it into vitess-mysql
				self.vitess.insertBox(boundboxes_list)
				self.vitess.mydb.commit()
				print('Bounding Box metadata updated')
			except mysql.connector.Error as e:
				print('Error inserting bounding boxes' + str(e))
				self.vitess.mydb.rollback()
			except Exception as e2:
				print(e2)
		else:
			return 0


	# this function should read one image and corresponding bounding box
	def insert_image(self, folder_path, image_name, cam_ID, isprocessed, bounding_box):
		try:
			# generate the image metadata for image_table
			image_id = str(uuid.uuid1())
			path = folder_path + image_name
			image_date = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(path)))
			image_time = time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(path)))
			name = os.path.splitext(image_name)[0]
			image_type = os.path.splitext(image_name)[1][1:]
			image_size = os.stat(path).st_size

			# generate the feature information for feature_table, and the bounding box informatoin for box feature
			num_of_feature = {}
			class_dir = "./detection/data/classes/coco.names"
			classes = utils.read_class_names(class_dir)

			for box in bounding_box:
				feature_name = classes[box[5]]
				if feature_name not in num_of_feature:
					num_of_feature[feature_name] = 1
					feature_id = self.vitess.getFeature(feature_name)
					if not feature_id:
						self.vitess.insertFeature(tuple([str(uuid.uuid1()), feature_name]))
				else:
					num_of_feature[feature_name] += 1
					# confidence, xmin, xmax, ymin, ymax
				self.vitess.insertBox(tuple([image_id, self.vitess.getFeature(feature_name), box[4], box[0], box[2], box[1], box[3]]))

			# Insert metadata into the relation table
			for key in num_of_feature:
				self.vitess.insertImagefeatures(tuple([self.vitess.getFeature(key), image_id, num_of_feature[key]]))

			# sort features in descending
			# most popular feature is going to being the bucket_name
			'''sorted_features = sorted(num_of_feature.items(), key=lambda item: item[1], reverse=True)
			bucket_name = sorted_features[0][0]'''

			if not('person' in num_of_feature) or num_of_feature['car'] > num_of_feature['person']:
				bucket_name = 'car'
			elif not('car' in num_of_feature) or num_of_feature['car'] < num_of_feature['person']:
				bucket_name = 'person'
			else:
				bucket_name = 'none'

			minio_link = self.minio.endpoint + "/" + bucket_name + "/" + image_id
			dataset = bucket_name

			image = [image_id, name, cam_ID, image_date, image_time, image_type, image_size, minio_link, dataset,
					 isprocessed]
			self.vitess.insertImage(tuple(image))

			# Image is inserted after all database interaction as there is no rollback supported by minio.
			# We thus make sure that we only insert image when information is written to database.
			# If error occurs while inserting the image, we only need to rollback database operations

			# create the bucket if not existed
			if self.minio.mc.bucket_exists(bucket_name) is False:
				self.minio.create_bucket(bucket_name)
			# upload image to bucket
			self.minio.upload_single_file(bucket_name, image_id, path)
			self.vitess.mydb.commit()
			#print('Image_Video metadata updated')

		except mysql.connector.Error as e:
			print('Error inserting image information: ' + str(e))
			self.vitess.mydb.rollback()
			sys.exit()
		except ResponseError as e1:
			print('Error uploading image: ' + str(e))
			self.vitess.mydb.rollback()
			sys.exit()
		except Exception as e2:
			print(e2)
			sys.exit()



	# this function should read the images, image csv file, feature csv file
	def insert_image_csv(self, bucket_name, folder_path, image_csv, image_feature_csv):
		try:

			# image_list is a list of list, each element is a row in csv
			image_list, image_header = ImageDB.read_data(image_csv, config.IV_HEADER, 'list', folder_path)

			# image feature relation dict
			# key: file name; value: csv row as list

			relation_header = None
			relation_list = None

			if image_feature_csv != None:

				relation_list, relation_header = ImageDB.read_data(image_feature_csv, config.IF_HEADER, 'dict', folder_path)

		except IOError as e:
			print('IOError({0}): {1}'.format(e.errno, e.strerror))
			sys.exit()
		except ValueError as e2:
			print('Error processing file ' + str(e2))
			sys.exit()
		except Exception as e3:
			print(str(e3))
			sys.exit()

		if image_list and image_header:
			try:
				# Process the image feature header list to a list of feature ids (except for first entry)

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
					# allowing updating image information
					iv_id = self.vitess.getIVID(image_filename)

					if iv_id is not None:
						image_id = iv_id
					else:
						image_id = str(uuid.uuid1())

					# find the corresponding image in the folder, save for later image uploading
					file_path = folder_path + image_list[i][0]

					# prepare the minio link before inserting
					minio_link = ""#self.minio.endpoint + ":/" + bucket_name + ":/" + image_id

					# TODO: which column is feature "minio_link"? -- 6
					image_list[i][6] = minio_link

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
						self.vitess.insertImagefeatures(list(if_list))

					# image is inserted after all database interaction as there is no rollback supported by minio.
					# We thus make sure that we only insert image when information is written to database.
					# If error occurs while inserting the image, we only need to rollback database operations

					# create the bucket if not existed
					'''
					if self.minio.mc.bucket_exists(bucket_name) is False:
						self.minio.create_bucket(bucket_name)

					# upload image to bucket
					self.minio.upload_single_file(bucket_name, image_id, file_path)
					'''

				self.vitess.mydb.commit()

				print('Image_Video metadata updated')

			except mysql.connector.Error as e:
				print('Error inserting image information: ' + str(e))
				self.vitess.mydb.rollback()
				sys.exit()
			except ResponseError as e1:
				print('Error uploading image: ' + str(e))
				self.vitess.mydb.rollback()
				sys.exit()
			except Exception as e2:
				print(e2)
				sys.exit()
		else:
			return 0


	# Get all cameras information
	def get_all_cameras(self):
		camera_data = self.vitess.getAllCameras()

		if camera_data == -1:
			sys.exit()
		elif len(camera_data) == 0:
			print("There's no satisfied query result")
			sys.exit()

		return camera_data


	'''This fucntion takes a dictionary of arguments from the CLI and performs the following tasks - 1. Retreieved Image ID's from
	the Vitess database that match the query parameters. 2. Stores a csv file of all the results. 3. Calls the minio docwnload
	function to download the images if the download flag was specified.'''
	def get_image(self, arguments):
		try:
			if arguments != None:
				result = self.vitess.getImage(arguments)

				'''
				if result == 0:
					print("No files match your query. Please try again.")
				elif result == -1 :
					print("Please pass valid arguments.")
				else:
					fp = open('query_result.csv', 'w')
					outputFile = csv.writer(fp, lineterminator='\n')
					outputFile.writerow(["IV_ID", "IV_Name", "Image_Camera_ID","IV_date","IV_time","File_type","File_size","Minio_link","Dataset"
							,"Is_processed","Camera_ID","Country","State","City","Latitude","Longitude","Resolution_w","Resolution_h"])
					outputFile.writerows(result)
					fp.close()
					print("Results were found and successfully stored in the CSV file.")
				'''
				if arguments['download'] is not None:
					data_dict = {}
					file_names = []
					bucket_names = []
					bucket_link = []
					for row in result:
						file_names.append(row[0])
						bucket_names.append(row[5])
						bucket_link.append(row[4])
					data_dict["File_Names"] = file_names
					data_dict["Bucket_Name"] = bucket_names
					data_dict["Bucket_Link"] = bucket_link
					df = pd.DataFrame(data_dict)
					self.minio.batch_download(self.minio.mc, df)


		except mysql.connector.Error as e:
			print('Error retreiving image information: ' + str(e))
			sys.exit()
		except ResponseError as e1:
			print('Error downloading image: ' + str(e))
			sys.exit()
		except Exception as e2:
			print(e2)
			sys.exit()


	def get_video(self, arguments):
		try:
			if arguments != None:
				results = self.vitess.getImage(arguments)
				if results == 0:
					print("No files match your query. Please try again.")
				elif results == -1:
					print("Please pass valid arguments.")
				else:
					df_results= pd.DataFrame(results)
					#df_results[0] is the CamID column.
					unique_camID = df_results[0].unique()
					sorted_list = df_results.groupby([0])

					video_list = []
					#Gap between frames. Depends on fps thereshold
					fps = 10.0
					frame_gap = 100#1.0 / fps
					video_length = 60 # default to be 60 sec

					for cam in unique_camID:
						#sort[2,3] sorts by IV_date and IV_time
						sameID_list = sorted_list.get_group(cam).sort_values(by=[2,3]).values.tolist()
						j = 0
						frames_list = [] #emptying list
						for i in range(len(sameID_list)):
							#first image in frame list requires no check
							if i == 0 or len(frames_list) == 0:
								frames_list.append(sameID_list[i])
							else:
								if len(frames_list) > 20:
									video_list.append(frames_list)
									frames_list = []

								d1 = datetime.strptime(str(sameID_list[i-1][2]) + str(sameID_list[i-1][3])[6:], '%Y-%m-%d %H:%M:%S')
								d2 = datetime.strptime(str(sameID_list[i][2]) + str(sameID_list[i][3])[6:], '%Y-%m-%d %H:%M:%S')
								time_gap =(d2 - d1).total_seconds()
								#continue or break frames_list depending on time_gap
								if time_gap > frame_gap:
									#if condition is experitmental. Not sure details about thereshold and implementation
									#thereshold len set to min 10fps for 10sec => 100 images
									if len(frames_list) >= 10:
										video_list.append(frames_list)
									frames_list = []
								else:
									frames_list.append(sameID_list[i])
					#print(video_list)
					for i in range(len(video_list)):
						frames_list = video_list[i]
						data_dict = {}
						file_names = []
						bucket_names = []
						bucket_link = []
						for row in frames_list:
							file_names.append(row[1])
							bucket_names.append(row[5])
							bucket_link.append(row[4])
						data_dict["File_Names"] = file_names
						data_dict["Bucket_Name"] = bucket_names
						data_dict["Bucket_Link"] = bucket_link
						df = pd.DataFrame(data_dict)
						self.minio.batch_video_download(self.minio.mc, df)
						print("download complete")

						img_array = []
						size = 0
						images = os.listdir('output_images/')
						images.sort()
						for i in images:
							#print(os.path.join('Cat2/', filename))
							img = cv2.imread(os.path.join('output_images/', i))
							#cv2.imshow('image', img)
							#cv2.waitKey(500)

							height, width, layers = img.shape
							size = (width, height)
							img_array.append(img)

						ts = datetime.now()
						file_name = ts.strftime("%Y-%m-%d") + "_" + ts.strftime("%H:%M:%S")
						out = cv2.VideoWriter(filename=file_name + '.avi',
											  fourcc=cv2.VideoWriter_fourcc(*'MJPG'),
											  fps=2,
											  frameSize=size)

						for i in range(len(img_array)):
							out.write(img_array[i])

						out.release()

						self.minio.rm_cmd("output_images")
						self.minio.mkdir_cmd("output_images")


		except mysql.connector.Error as e:
			print('Error retreiving image information: ' + str(e))
			sys.exit()
		except ResponseError as e1:
			print('Error downloading image: ' + str(e))
			sys.exit()
		except Exception as e2:
			print(e2)
			sys.exit()