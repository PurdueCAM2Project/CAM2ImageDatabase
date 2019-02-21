import mysql.connector
from mysql.connector import errorcode

import pandas as pd
import unicodedata


'''
When this file been called, it will create ### two ### tables first,
the CAMERA table, and the IMAGE/VIDEO table,
and then the content of CAMERA.csv and IV.csv file will be added to
these two tables.


## the input, content of csv file, need to be decided ##

For now, the CAMERA.csv file would looks something similar to

-------------------------------------------------------------------------------------------------------
| Transaction id | Expired | Country | City     | Latitude | Longtitude | Resolution_w | Resolution_h | 
-------------------------------------------------------------------------------------------------------
|         000001 |       0 | USA     | Boston   |  42.3692 |   -71.0658 |         2048 |         1536 |
-------------------------------------------------------------------------------------------------------
|         000002 |       0 | USA     | New York |  40.7047 |   -74.0211 |         1024 |          768 |
-------------------------------------------------------------------------------------------------------
...

and the IV.csv file would looks something similar to

----------------------------------------------------------------------------------------------------------------------
| IV_id      | Transaction id | iv_ date   | iv_time  | file type | file size | minio link | data set | is processed |
----------------------------------------------------------------------------------------------------------------------
| 0000000001 |         000001 | 2019-01-02 | 13:38:22 | PNG       | 1.4 MB    | None       | None     |            0 |
----------------------------------------------------------------------------------------------------------------------
| 0000000002 |         000001 | 2019-01-03 | 14:57:19 | JPEG      | 390 KB    | None       | None     |            0 |
----------------------------------------------------------------------------------------------------------------------
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
      print
      
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "Something is wrong with your user name or password"
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print "Database does not exist"
      else:
        print(err)
      return

    self.mycursor = self.mydb.cursor(buffered=True)
    self.cameraset = cameraset
    self.imageset = imageset
    ##self.featureset = featureset
    ##self.imagefeature = imagefeature


  # drop test table IF NEEDED
  def dropCameraTable(self):
    self.mycursor.execute("drop table CAMERA")
    print "CAMERA table dropped."
    print

  # drop test table IF NEEDED
  def dropImageTable(self):
    self.mycursor.execute("drop table IMAGE_VIDEO")
    print "IMAGE_VIDEO table dropped."
    print
    

  # CREATE CAMERA TABLE IF NEEDED
  def createCameraTable(self):
    try:
      self.mycursor.execute("SELECT * FROM CAMERA")
      print "CAMERA table exist"
      print
      
    except:
      # create table
      self.mycursor.execute("CREATE TABLE CAMERA(Transaction_ID INT,\
                  Expired INT, \
                  Country VARCHAR(30), City VARCHAR(30), \
                  Latitude FLOAT, Longitude FLOAT, \
                  Resolution_w INT, Resolution_h INT, PRIMARY KEY (Transaction_ID))")
      print "CAMERA table created."
      print
    

  # CREATE IMAGE TABLE IF NEEDED
  def createImageTable(self):
    try:
      self.mycursor.execute("SELECT * FROM IMAGE_VIDEO")
      print "IMAGE_VIDEO table exist"
      print
    except:
      ## create table
      self.mycursor.execute("CREATE TABLE IMAGE_VIDEO(IV_ID INT, Transaction_ID INT, \
                  IV_date DATE, IV_time TIME, \
                  File_type VARCHAR(10), File_size VARCHAR(10), \
                  Minio_link VARCHAR(500), Dataset VARCHAR(500), Is_processed INT, \
                  PRIMARY KEY (iv_ID))")
                          
      print "IMAGE_VIDEO table created."
      print


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
      sql = "INSERT INTO CAMERA(Transaction_ID, Expired, Country, City, Latitude, Longitude, \
                  Resolution_w, Resolution_h) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                  ON DUPLICATE KEY UPDATE Transaction_ID = " + `i[1][0]`
      val=(i[1][0], i[1][1], i[1][2], i[1][3], i[1][4], i[1][5], i[1][6], i[1][7])
      self.mycursor.execute(sql, val)
      
    self.mydb.commit()
    print "CAMERA table updated."
    print


  def insertImage(self):
    for i in self.imageset.iterrows():
      sql = "INSERT INTO IMAGE_VIDEO(IV_ID, Transaction_ID, IV_date, IV_time, File_type, File_size, \
                Minio_link, Dataset, Is_processed) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE iv_ID = " + `i[1][0]`
      val = (i[1][0], i[1][1], i[1][2], i[1][3], i[1][4], i[1][5], i[1][6], i[1][7], i[1][8])
      self.mycursor.execute(sql, val)
      
    self.mydb.commit()
    print "IMAGE_VIDEO table updated."
    print
    

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
  camera_data.readcameraData("CAMERA.csv")
  
  iv_data = Datafile()
  iv_data.readivData("IV.csv")

  ## initialize newData
  newData = communacation(camera_data.cameradata, iv_data.imagedata) #, data.featuredata, \
                        #data.imagefeaturedata)


  ## drop test table
  #newData.dropCameraTable()
  #newData.dropImageTable()
  
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
  


