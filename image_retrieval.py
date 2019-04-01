import CAM2CameraDatabaseAPIClient.client as cam2
from CAM2ImageArchiver.CAM2ImageArchiver import CAM2ImageArchiver

clientID = '%s' %(cam2.Client.clientID)
clientSecret = '%s' %(cam2.Client.clientSecret)

db = cam2.Client(clientID, clientSecret)

archiver = CAM2ImageArchiver(num_processes=1)

cameras = db.search_camera(offset=0)

# To search camera by all camera ids:
i = 0
while len(cameras) != 0:
    cameras = db.search_camera(offset=i)
    i += 100

IDList = []
for camera in cameras:
    IDList.append(camera['cameraID'])

cameras1 = []

for camId in IDList:
    cameras1.append(db.camera_by_id(camId))

archiver.archive(cameras1, duration=1, interval=1)
