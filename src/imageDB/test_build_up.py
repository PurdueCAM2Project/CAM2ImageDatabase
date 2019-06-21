from routine import Routine
from imageDB import ImageDB

def build_up_test():
    # initial the tables
    db = ImageDB()
    db.init_tables()

    # Insert info and keep updating the camera table every 1 month
    example = Routine()
    example.updateCameraTable()
    
    # Keep retrieving images from camera
    example.retrieveImage(0.2, 10)


build_up_test()
