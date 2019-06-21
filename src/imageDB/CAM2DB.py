import csv
import CAM2CameraDatabaseAPIClient.client as cam2

# This class is for connecting to the CAM2 Mongo Database,
# retrieving cameras information, and generating the information csv file
class CAM2DB:

	# Require user for clientID and clientSecret
	def __init__(self, clientID, clientSecret, file_name):
		self.db = cam2.Client(clientID, clientSecret)
		self.file_name = file_name
		self.output_file = open(self.file_name, 'w', newline="")
		self.writer = csv.writer(self.output_file)


	# Generate the camera information csv file
	def generateCSV(self):
		# initial CSV header
		
		fields = ['Camera_ID', 'type', 'Country', 'State', 'City', 'Latitude', \
		'Longtitude', 'Resolution_w', 'Resolution_h', 'Ip', 'Port', \
		'Image_path', 'Video_path', 'Snapshot_url', 'm3u8_url']
		
		self.writer.writerow(fields)

		# get three type of camera informatoin, ip, nonip, stream
		self.getIPCamerasInfo()
		self.getNonIPCamerasInfo()
		self.getStreamCamerasInfo()

		self.output_file.close()


	# Get the information of IP type camera
	def getIPCamerasInfo(self):
		i = 0
		cameras = self.db.search_camera(offset=i, camera_type='ip')
		while len(cameras) != 0:
			for camera in cameras:
				self.writer.writerow(camera['cameraID'], camera['type'], camera['country'], 
				camera['state'], camera['city'], camera['latitude'], 
				camera['longitude'], camera['resolution_width'], 
				camera['resolution_height'],camera['ip'],
				camera['port'], camera['image_path'], camera['video_path'], 'Null', 'Null')
			i += 100
			cameras = self.db.search_camera(offset=i, camera_type='ip')


	# Get the information of NON-IP type camera
	def getNonIPCamerasInfo(self):
		i = 0
		cameras = self.db.search_camera(offset=i, camera_type='non_ip')
		while len(cameras) != 0:
			for camera in cameras:
				self.writer.writerow(camera['cameraID'], camera['type'], camera['country'], \
				camera['state'], camera['city'], camera['latitude'], \
				camera['longitude'], camera['resolution_width'], \
				camera['resolution_height'], 'Null', 'Null', 'Null', 'Null', \
				camera['snapshot_url'], 'Null')
			i += 100
			cameras = self.db.search_camera(offset=i, camera_type='non_ip')


	# Get the information of NON-IP type camera
	def getStreamCamerasInfo(self):
		# CAM2 DB doesn't have stream type camera for now
		pass
