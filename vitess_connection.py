import mysql.connector
from mysql.connector import errorcode

class VitessConn:

  # connect to the mysql
  def __init__(self):

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


  # drop test table IF NEEDED
  def dropCameraTable(self):
    self.mycursor.execute("drop table IF EXISTS CAMERA")
    print "CAMERA table dropped."
    print

  # drop test table IF NEEDED
  def dropImageTable(self):
    self.mycursor.execute("drop table IF EXISTS IMAGE_VIDEO")
    print "IMAGE_VIDEO table dropped."
    print
    

  # CREATE CAMERA TABLE IF NEEDED
  def createCameraTable(self):
    try:
      self.mycursor.execute("SELECT 1 FROM CAMERA LIMIT 1")
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
      self.mycursor.execute("SELECT 1 FROM IMAGE_VIDEO LIMIT 1")
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
    self.mycursor.execute("CREATE TABLE feature(Feature_ID INT, \
                  Feature_Name VARCHAR(100)")
    print(self.mycursor.rowcount, "table created.")


  def createImagefeatureTable(self):
    self.mycursor.execute("CREATE TABLE RELATION(Feature_ID INT, \
                  IV_ID INT, PRIMARY KEY (Feature_ID, IV_ID))")
    print(self.mycursor.rowcount, "table created.")


  # INSERT the element from the input into the database
  # camera is tuple

  # mannual commit after calling the method
  def insertCamera(self, camera):
    
    sql = 'INSERT IGNORE INTO CAMERA(Transaction_ID, Expired, Country, City, Latitude, Longitude, \
          Resolution_w, Resolution_h) \
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

    try:
      self.mycursor.execute(sql, camera)
      return True
    except mysql.connect.Error as err:
      print("Error inserting camera data ".format(err))
      return False

  def insertImage(self, image):

    sql = 'INSERT IGNORE INTO IMAGE_VIDEO(IV_ID, Transaction_ID, IV_date, IV_time, File_type, File_size, \
            Minio_link, Dataset, Is_processed) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

    try:
      self.mycursor.executemany(sql, image)
      return True
    except mysql.connect.Error as err:
      print("Error inserting image/video data ".format(err))
      return False
    

  # this function get feature ID of a feature name
  def getFeature(self, featureName):

    # see if the feature already exist
    # if so, return the feature ID
    self.mycursor.execute('SELECT Feature_ID FROM feature WHERE Feature_Name=%s', featureName)
    result = self.mycursor.fetchall()
    if(len(result) > 0):
      return result[0]
    return None


  # this function takes in a list of feature tuples (Feature_ID, Feature_Name)
  def insertFeature(self, features)

    sql = "INSERT INTO feature(Feature_ID, Feature_Name) VALUES (%s, %s)"
    self.mycursor.executemany(sql, features)


  # this function takes a list of feature_ID-image_ID tuples
  def insertImagefeature(self, relations):
    sql = "INSERT INTO RELATION(Feature_ID, IV_ID) VALUES (%s, %s)"
    self.mycursor.executemany(sql, relations)
    
  
  ## check permission if needed
  def select(self, tablename):
    self.mycursor.execute("SELECT * FROM " + tablename)
    myresult = self.mycursor.fetchall()
    for x in myresult:
      print(x)