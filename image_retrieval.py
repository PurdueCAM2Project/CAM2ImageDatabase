import CAM2CameraDatabaseAPIClient.client as cam2
from CAM2ImageArchiver.CAM2ImageArchiver import CAM2ImageArchiver

clientID = '%s' %(cam2.Client.clientID)
clientSecret = '%s' %(cam2.Client.clientSecret)

db = cam2.Client(clientID, clientSecret)

archiver = CAM2ImageArchiver(num_processes=1)

# To search camera by all camera ids:
i = 0
while len(db.search_camera(offset=i)) != 0:
    cameras = db.search_camera(offset=i)
    i += 100
    archiver.archive(cameras, duration=1, interval=1)

