import mysql.connector
from mysql.connector import errorcode

import sys
import os.path
import csv
#import pandas as pd



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

  # cameradata stores the metadata of camera
  # camera_bool check whether the data is valid
  def __init__(self):
    self.check = True
    self.cameradata = None
    self.camera_bool = False
    
    self.ivdata = None
    self.iv_bool = False
    
    self.featuredata = None
    self.feature_bool = False
    
    self.ifdata = None
    self.if_bool = False

  def readData(self, file_content, filename):
    if (file_content == 0):
      try:
        self.cameradata = []
        with open(filename, 'rb') as csvfile:
          spamreader = csv.reader(csvfile, delimiter='|')
          for row in spamreader:
            if (row[0] != ',,,,,,,'):
              temp = row[0].split(",")
              self.cameradata.append(temp)
            
        # if it is valid dataset
        if (self.cameradata[0] == ["Transaction id", "Expired", "country", \
                                   "city", "latitude", "longtitude", \
                                   "resolution_w", "resolution_h"]):
          self.cameradata = self.cameradata[1:]

        # if it missing optional column - city
        elif (self.cameradata[0] == ["Transaction id", "Expired", "country", \
                                   "latitude", "longtitude", \
                                   "resolution_w", "resolution_h"]):
          self.cameradata = self.cameradata[1:]
          for i in range (len(self.cameradata)):
            self.cameradata[i] = self.cameradata[i][:3] + ["None"] + self.cameradata[i][3:]

        elif (len(self.cameradata[0]) < 8):
          print "File", filename, "is missing required column."
          print
          self.check = False
          return
        elif (len(self.cameradata[0]) > 8):
          print "File", filename, "exceed the expected number of columns."
          print
          self.check = False
          return
          
        self.camera_bool = True
      except:
        print "The camera file", filename, "does not exist"
        print
        self.check = False
        return
      
    elif (file_content == 1):
      try:
        self.ivdata = []
        with open(filename, 'rb') as csvfile:
          spamreader = csv.reader(csvfile, delimiter='|')
          for row in spamreader:
            if (row[0] != ',,,,,,,'):
              temp = row[0].split(",")
              self.ivdata.append(temp)
        if (self.ivdata[0] == ["iv_id", "Transaction id", "iv_date",\
                               "iv_time", "file type", "file size",\
                               "minio link", "data set", "is processed"]):
          self.ivdata = self.ivdata[1:]
        elif (len(self.ivdata[0]) < 9):
          print "File", filename, "is missing required column."
          print
          self.check = False
          return
        elif (len(self.ivdata[0]) > 9):
          print "File", filename, "exceed the expected number of columns."
          print
          self.check = False
          return
        self.iv_bool = True
      except:
        print "The imagevideo file", filename, "does not exist"
        print
        self.check = False
        return
      
    elif (file_content == 2):
      try:
        self.featuredata = []
        with open(filename, 'rb') as csvfile:
          spamreader = csv.reader(csvfile, delimiter='|')
          for row in spamreader:
            temp = row[0].split(",")
            self.featuredata.append(temp)   
        self.feature_bool = True
      except:
          print "The feature file", filename, "does not exist"
          print
          self.check = False
          return
        
    else:
      try:
        self.ifdata = []
        with open(filename, 'rb') as csvfile:
          spamreader = csv.reader(csvfile, delimiter='|')
          for row in spamreader:
            temp = row[0].split(",")
            self.ifdata.append(temp)   
        self.if_bool = True
      except:
        print "The imagefeature file", filename, "does not exist"
        print
        self.check = False
        return

class communacation:

  # connect to the mysql
  def __init__(self, camera_set, iv_set, feature_set, if_set):

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
    self.camera_set = camera_set
    self.iv_set = iv_set
    self.feature_set = feature_set
    self.if_set = if_set


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
    for i in self.camera_set:
      sql = "INSERT INTO CAMERA(Transaction_ID, Expired, Country, City, Latitude, Longitude, \
                  Resolution_w, Resolution_h) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                  ON DUPLICATE KEY UPDATE Transaction_ID = " + `i[0]`
      val=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
      self.mycursor.execute(sql, val)
      
    self.mydb.commit()
    print "CAMERA table updated."
    print


  def insertImage(self):
    for i in self.iv_set:
      sql = "INSERT INTO IMAGE_VIDEO(IV_ID, Transaction_ID, IV_date, IV_time, File_type, File_size, \
                Minio_link, Dataset, Is_processed) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE iv_ID = " + `i[0]`
      val = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
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
  if (len(sys.argv) < 5):
    print "Please use the format"
    print ">> python connect_vitess.py <camera filename> <image&video filename> <feature filename> <image&feature filename>"
    print
    print "If does not have any of the file, use None"
    print ">> python connect_vitess.py <camera filename> None None None"
    print
    return
  else:
    camera_file = sys.argv[1]
    iv_file = sys.argv[2]
    feature_file = sys.argv[3]
    if_file = sys.argv[4]

  for i in range (1,5):
    if (sys.argv[i] != "None"):
      name, ext = os.path.splitext(sys.argv[i])
      if (ext != ".csv"):
        print "Only accept the csv file type"
        print
        return

  ## read file
  camera_data = Datafile()
  iv_data = Datafile()
  feature_data = Datafile()
  if_data = Datafile()
    
  if (camera_file != "None"):
    camera_data = Datafile()
    camera_data.readData(0, camera_file)

  if (iv_file != "None"):
    iv_data = Datafile()
    iv_data.readData(1, iv_file)

  if (feature_file != "None"):
    feature_data = Datafile()
    feature_data.readData(2, iv_file)

  if (if_file != "None"):
    if_data = Datafile()
    if_data.readData(3, if_file)

  if (not camera_data.check or not iv_data or not feature_data or not if_data ):
    return
  
  ## initialize newData
  newData = communacation(camera_data.cameradata, iv_data.ivdata, feature_data.featuredata, \
                        if_data.ifdata)

  ## drop test table
  #newData.dropCameraTable()
  #newData.dropImageTable()

  ## create and insert data table

  if (camera_data.camera_bool):
    newData.createCameraTable()
    newData.insertCamera()

  if (iv_data.iv_bool):
    newData.createImageTable()
    newData.insertImage()

  if (feature_data.feature_bool):
    newData.createFeatureTable()
    newData.insertFeature()

  if (if_data.if_bool):
    newData.createImagefeature()
    newData.insertImagefeature()
  

main()
  


