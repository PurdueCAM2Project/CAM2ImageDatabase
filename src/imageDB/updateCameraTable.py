from CAM2DB import CAM2DB
from imageDB import ImageDB

# Update the Camera Table by get the Updated Camera Information from CAM2DB
class updateCameraTable:
    def __init__(self):
        self.db = ImageDB()

    # get the updated camera information from CAM2 Mongo DB
    def getUpdatedCAM2DB(self):
        #clientID = input("ClientID: \n")
        #clientSecret = input("ClientSecret: \n")
        #file_name = 'camera_list.csv'
        #cam2db = CAM2DB(clientID, clientSecret, file_name)
        #cam2db.generateCSV()
        self.db.single_insert_camera('camera_list.csv')

    # get the updated camera informatoin from camera information file
    def updateCamera(self, file_name):
        self.db.batch_insert_camera(file_name)


if __name__ == '__main__':
    update = updateCameraTable()
    update.getUpdatedCAM2DB()
