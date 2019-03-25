from imageDB import ImageDB

def test():
    db = ImageDB()
    db.init_tables()
    
    ''' TEST CAMERA FILE '''
    
    ''' test correct case '''
    db.batch_insert_camera("./vitess_test/camera_test_standard.csv")
    
    ''' test wrong hearder name '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkHeader.csv")
    
    ''' test exceed column '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkExceedColumn.csv")
    
    ''' test missing column '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkMissingColumn.csv")

    ''' test missing values '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkMissingValues.csv")

    ''' test empty cell -- FAIL !!!!!!!!!!  '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkEmptyCell.csv")

    ''' test add same things twice '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkInsertExistValue.csv")



    ''' TEST ImageVideo FILE '''
    
    ''' test correct case '''
    db.insert_image("./vitess_test/imageVideo_test_standard.csv")
    
    ''' test wrong hearder name '''
    #db.insert_image("./vitess_test/imageVideo_test_checkHeader.csv")
    
    ''' test exceed column -- FAIL !!!!!!!!!!  '''
    #db.insert_image("./vitess_test/imageVideo_test_checkExceedColumn.csv")
    
    ''' test missing column '''
    #db.insert_image("./vitess_test/imageVideo_test_checkMissingColumn.csv")

    ''' test missing values '''
    #db.insert_image("./vitess_test/imageVideo_test_checkMissingValues.csv")

    ''' test empty cell -- FAIL !!!!!!!!!!  '''
    #db.insert_image("./vitess_test/imageVideo_test_checkEmptyCell.csv")

    ''' test add same things twice '''
    #db.insert_image("./vitess_test/imageVideo_test_checkInsertExistValue.csv")

    
test()
