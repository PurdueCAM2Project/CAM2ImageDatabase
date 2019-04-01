import CAM2CameraDatabaseAPIClient.client as cam2
import csv
from CAM2CameraDatabaseAPIClient.client import Client
from CAM2ImageArchiver.CAM2ImageArchiver import CAM2ImageArchiver


clientID = '%s' %(cam2.Client.clientID)
clientSecret = '%s' %(cam2.Client.clientSecret)
db = cam2.Client(clientID, clientSecret)

archiver = CAM2ImageArchiver(num_processes=1)

cameras = db.search_camera(city="NY", offset=0)

#To search camera by all camera ids:
# i = 0
# while len(cameras) != 0:
#     cameras = db.search_camera(offset=i)
#     i += 100

IDList = []
for camera in cameras:
    IDList.append(camera['cameraID'])

cameras1 = []

for camId in IDList:
    cameras1.append(db.camera_by_id(camId))

archiver.archive(cameras1, duration=1, interval=1)

output_file = open('file2_name.csv', 'w')

fields = ['Camera_ID', 'camera_country', 'camera_state', 'camera_city', 'camera_latitude', 'camera_longitude', 'resolution_width', 'resolution_height']
writer = csv.writer(output_file)
writer.writerow(fields)

for camera in cameras1:
    Camera_ID = camera['cameraID']
    camera_city = camera['city']
    camera_country = camera['country']
    camera_state = camera['state']
    camera_longitude = camera['camera_longitude']
    camera_latitude = camera['camera_latitude']
    camera_rwidth = camera['resolution_width']
    camera_rheight = camera['resolution_height']
    writer.writerow([Camera_ID, camera_country, camera_state, camera_city, camera_latitude, camera_longitude, camera_rwidth, camera_rheight])




