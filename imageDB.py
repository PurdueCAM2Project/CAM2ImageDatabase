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


'''
from vitess_connection import VitessConn
import config
import mysql.connector.Error as mysqlError

class ImageDB:

    def __init__(self):

        # connect to Vitess-MySql and Minio

        self.vitess = VitessConn()
        # add a line for Mino connection
    
    def init_tables(self):
        self.vitess.createCameraTable()
        self.vitess.createFeatureTable()
        self.vitess.createImagefeatureTable()
        self.vitess.createImageTable()

    @classmethod
    def check_header(csv_header, required_header):
        if csv_header == required_header:
            return
        elif len(csv_header) < len(required_header):
            raise ValueError("File is missing required column.") 
        elif len(csv_header) > len(required_header):
            raise ValueError("File exceeds the expected number of columns.")
        else:
            raise ValueError("File is missing header.")

    def batch_insert_camera(self, camera_csv):
        camera_list = []
        try:
            with open(camera_csv, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')

                # check if it has the corret format
                # if it is valid dataset
                ImageDB.check_header(reader[0], config.CAM_HEADER, camera_csv)
                
                for i in reader:
                    if len(i) != len(config.CAM_HEADER):
                        raise ValueError("File content column does not match header.")
                    camera_list.append(tuple(i))
            self.vitess.insertCamera(camera_list)
            self.vitess.mydb.commit()
        except IOError as e:
            print('IOError({0}): {1}'.format(e.errno, e.strerror))
        except ValueError as e2:
            print('Error opening file ' + camera_csv + repr(e2))
        except mysqlError as e3:
            print('Error inserting cameras: ' + repr(e3))
            self.vitess.mydb.rollback()
        except Exception as e4:
            print(e4)

    def insert_image

