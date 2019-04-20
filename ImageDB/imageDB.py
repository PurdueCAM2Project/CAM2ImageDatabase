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
import mysql.connector
import config
from vitess_connection import VitessConn
from minio_connection import MinioConn
# minio error
from minio.error import ResponseError



class ImageDB:

	def __init__(self):

		# connect to Vitess-MySql and Minio
		self.vitess = VitessConn()
		self.minio = MinioConn()
		#self.minio = self.minio_conf.connect_to_minio_server(endpoint, access_key, secret_key)

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
	def read_data(self, csv_file, required_header, data_format):
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
							raise ValueError('\nFile ' + csv_file + ' content missing value.')
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
			except mysql.connector.Error as e:
				print('Error inserting cameras: ' + str(e))
				self.vitess.mydb.rollback()
			except Exception as e2:
				print(e2)
		else:
			return 0



	# this function should read image and image feature file,
	def insert_image(self, bucket_name, folder_path, image_csv, image_feature_csv=None):
		try:

			# image_list is a list of list, each element is a row in csv
			image_list, image_header = ImageDB.read_data(image_csv, config.IV_HEADER, 'list')

			# image feature relation dict
			# key: file name; value: csv row as list

			relation_header = None
			relation_list = None

			if image_feature_csv != None:
				relation_list, relation_header = ImageDB.read_data(image_feature_csv, config.IF_HEADER, 'dict')

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
					minio_link = self.minio.endpoint + ":/" + bucket_name + ":/" + image_id

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
					if self.minio.mc.bucket_exists(bucket_name) is False:
						self.minio.create_bucket(bucket_name)

					# upload image to bucket
					self.minio.upload_single_file(bucket_name, image_id, file_path)


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

	#self.minio.batch_download(mc, df)
