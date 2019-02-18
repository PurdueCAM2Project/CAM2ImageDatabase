import mysql.connector
from mysql.connector import errorcode

import pandas as pd
import unicodedata


'''
## the communacation between the database and the command line need to be decided ##

When this file been called, it will create ### two ### tables first,
the camera table, and the image/video table,
and then the content of camera.csv and iv.csv file will be added to
these two tables.


## the input, content of csv file, need to be decided ##

For now, the camera.csv file would looks something similar to

----------------------------------------------------------------------------------------
| camera id | country | city     | latitude | longtitude | resolution_w | resolution_h | 
----------------------------------------------------------------------------------------
|    000001 | USA     | Boston   |  42.3692 |   -71.0658 |         2048 |         1536 |
----------------------------------------------------------------------------------------
|    000002 | USA     | New York |  40.7047 |   -74.0211 |         1024 |          768 |
----------------------------------------------------------------------------------------
...

and the iv.csv file would looks something similar to

-----------------------------------------------------------------------------------------------------------------
| iv_id      | camera id | iv_ date   | iv_time  | file type | file size | minio link | data set | is processed |
-----------------------------------------------------------------------------------------------------------------
| 0000000001 | 000001    | 2019-01-02 | 13:38:22 | PNG       | 1.4 MB    | None       | None     |            0 |
-----------------------------------------------------------------------------------------------------------------
| 0000000002 | 000001    | 2019-01-03 | 14:57:19 | JPEG      | 390 KB    | None       | None     |            0 |
-----------------------------------------------------------------------------------------------------------------
...


'''


class Datafile:
  data = None
  length = None

  def __init__(self):
    self.camera_raw_data = None
    self.iv_raw_data = None
    self.cameradata = None
    self.imagedata = None
    self.featuredata = None
    self.imagefeaturedata = None

  def readcameraData(self, filename):
    self.camera_raw_data = pd.read_csv(filename, header=0)
    self.cameradata = self.camera_raw_data.iloc[:]

  def readivData(self, filename):
    self.iv_raw_data = pd.read_csv(filename, header=0)
    self.imagedata = self.iv_raw_data.iloc[:]


class communacation:

  # connect to the mysql
  def __init__(self, cameraset, imageset): #, featureset, imagefeature):

    # CREATE THE DATABASE IF NEEDED
    # mycursor.execute("CREATE DATABASE mydatabase")

    # Define database
    mydatabase = "test_keyspace"
  
    try:
      self.mydb = mysql.connector.connect(
        host='127.0.0.1',
        #user='root',
        #password='',
        port="15306",
        database = mydatabase,
        auth_plugin='mysql_native_password'
      )
      print "Connected to mysql database", mydatabase
      
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "Something is wrong with your user name or password"
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print "Database does not exist"
      else:
        print(err)

    self.mycursor = self.mydb.cursor()
    self.cameraset = cameraset
    self.imageset = imageset
    ##self.featureset = featureset
    ##self.imagefeature = imagefeature



  # CREATE CAMERA TABLE IF NEEDED
  
  def createCameraTable(self):
    # drop test table IF NEEDED
    #self.mycursor.execute("drop table camera")

    # create table
    self.mycursor.execute("CREATE TABLE camera(CameraID INT, \
                  Country VARCHAR(30), City VARCHAR(30), \
                  Latitude FLOAT, Longitude FLOAT, \
                  resolution_w INT, resolution_h INT, PRIMARY KEY (CameraID))")

    print "camera table created."
    

  # CREATE IMAGE TABLE IF NEEDED

  def createImageTable(self):
    ## drop test table IF NEEDED
    #self.mycursor.execute("drop table image")

    ## create table
    self.mycursor.execute("CREATE TABLE image(iv_ID INT, CameraID INT, \
                  iv_date DATE, iv_time TIME, \
                  file_type VARCHAR(10), file_size VARCHAR(10), \
                  minio_link VARCHAR(500), dataset VARCHAR(500), is_processed INT, \
                  PRIMARY KEY (iv_ID))")
                          
    print "image table created."


  # The features need to be decided, thus the following two functions
  #     will not been called for now.
  
  def createFeatureTable(self):
    self.mycursor.execute("CREATE TABLE feature(featureid INT, \
                  featurename VARCHAR(100)")
    print(self.mycursor.rowcount, "table created.")


  def createImagefeature(self):
    self.mycursor.execute("CREATE TABLE imagefeature(Feature_ID INT, \
                  IV_ID INT")
    print(self.mycursor.rowcount, "table created.")



  # INSERT the element from the input into the database
  
  def insertCamera(self):
    for i in self.cameraset.iterrows():
      sql = "INSERT INTO camera(CameraID, Country, City, Latitude, Longitude, \
                  resolution_w, resolution_h) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s)"
      val=(i[1][0], i[1][1], i[1][2], i[1][3], i[1][4], i[1][5],i[1][6])
      
      self.mycursor.execute(sql, val)
      
    self.mydb.commit()
    print "Camera record inserted."


  def insertImage(self):
    for i in self.imageset.iterrows():
      sql = "INSERT INTO image(iv_ID, CameraID, iv_date, iv_time, file_type, file_size, \
            minio_link, dataset, is_processed) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
      
      val = (i[1][0], i[1][1], i[1][2], i[1][3], i[1][4], i[1][5], i[1][6], i[1][7], i[1][8])

      self.mycursor.execute(sql, val)
      
    self.mydb.commit()
    
    print "Image record inserted."
    


  # The features need to be decided, thus the following two functions
  #     will not been called for now.
  
  def insertFeature(self):
    for i in self.featureset:
      sql = "INSERT INTO feature(featureid, featurename) \
          VALUES (%s, %s)"
      val = (i[1][0], i[1][1])
      self.mycursor.execute(sql, val)
    self.mydb.commit()
    print(self.mycursor.rowcount, "record inserted.")


  def insertImagefeature(self):
    for i in self.imagefeature:
      sql = "INSERT INTO imagefeature(Feature_ID, IV_ID) VALUES (%s, %s)"
      val = (i[1][0], i[1][1])
      self.mycursor.execute(sql, val)
    self.mydb.commit()
    print(self.mycursor.rowcount, "record inserted.")
    
  
  ## check permission if needed
  def select(self, tablename):
    self.mycursor.execute("SELECT * FROM " + tablename)
    myresult = self.mycursor.fetchall()
    for x in myresult:
      print(x)



def main():
  ## read file
  camera_data = Datafile()
  camera_data.readcameraData("camera.csv");
  
  iv_data = Datafile()
  iv_data.readivData("iv.csv");

  ## initialize newData
  newData = communacation(camera_data.cameradata, iv_data.imagedata) #, data.featuredata, \
                        #data.imagefeaturedata)

  
  ## create data table
  newData.createCameraTable()
  newData.createImageTable()
  #newData.createFeatureTable()
  #newData.createImagefeature()

  ## insert data
  newData.insertCamera()
  newData.insertImage()
  #newData.insertFeature()
  #newData.insertImagefeature()
  

main()
  


