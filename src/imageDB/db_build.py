from imageDB import ImageDB
from vitess_connection import VitessConn
import detection.utils as utils
import uuid
import sys

# Update the Camera Table by get the Updated Camera Information from CAM2DB
class DBbuild:
    def __init__(self):
        self.db = ImageDB()
        self.vitess = VitessConn()

    # Initialize all the tables and insert camera data
    def start(self, filename):
        self.db.init_tables()
        self.db.single_insert_camera(filename)
        #self.db.batch_insert_camera(filename)

    # Insert camera data to the current tables
    def append(self, filename):
        self.db.single_insert_camera(filename)
        self.db.batch_insert_camera(filename)

    def feature(self, filename):
        classes = utils.read_class_names(filename)

        for i in range(len(classes)):
            self.vitess.insertFeature(tuple([str(uuid.uuid1()), classes[i]]))
        #self.vitess.insertFeature('1', 'car')
        self.vitess.mydb.commit()
        print("Features Inserted")

if __name__ == '__main__':

    # This file takes in two argument inputs
    # argv[1] is mode (either start or append or feature)
    # argv[2] is the csv file name
    
    imgDB_build = DBbuild()

    if sys.argv[1] == 'start':
        imgDB_build.start(sys.argv[2])

    elif sys.argv[1] == 'append':
        imgDB_build.append(sys.argv[2])

    elif sys.argv[1] == 'feature':
        imgDB_build.feature(sys.argv[2])
