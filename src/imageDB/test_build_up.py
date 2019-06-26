from routine import Routine
from imageDB import ImageDB

def build_up_test():
    # initial the tables
    db = ImageDB()
    db.init_tables()

    # Insert info for the camera table
    db.single_insert_camera('camera_list.csv')
    
    # Keep retrieving images from camera
    example = Routine()
    example.retrieveImage(0.2, 10)


build_up_test()
