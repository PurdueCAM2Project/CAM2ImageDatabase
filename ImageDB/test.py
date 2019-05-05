from imageDB import ImageDB

def test():
    db = ImageDB()
    db.init_tables()
    
    ''' TEST CAMERA FILE '''
    
    ''' 1. test correct case '''
    #db.batch_insert_camera("./vitess_test/camera_test_standard.csv")
    
    ''' 2. test wrong hearder name '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkHeader.csv")
    
    ''' 3. test exceed column '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkExceedColumn.csv")
    
    ''' 4. test missing column '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkMissingColumn.csv")

    ''' 5. test missing values '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkMissingValues.csv")

    ''' 6. test empty cell '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkEmptyCell.csv")

    ''' 7. test add same things twice '''
    #db.batch_insert_camera("./vitess_test/camera_test_checkInsertExistValue.csv")



    ''' TEST ImageVideo FILE without feature csv'''
    
    ''' 1. test correct case'''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv")
    
    ''' 8. test wrong hearder name '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkHeader.csv")
    
    ''' 9. test exceed column '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkExceedColumn.csv")
    
    ''' 10. test missing column '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkMissingColumn.csv")

    ''' 11. test missing values '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkMissingValues.csv")

    ''' 12. test empty cell '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkEmptyCell.csv")

    ''' 13. test add same things twice '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkInsertExistValue.csv")

    

    ''' TEST ImageVideo FILE with feature csv, with feature csv correct all the time'''
    
    ''' 1. test correct case'''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_standard.csv")

    ''' test wrong hearder name '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkHeader.csv", "./vitess_test/imageFeature_test_standard.csv")
    
    ''' test exceed column '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkExceedColumn.csv", "./vitess_test/imageFeature_test_standard.csv")
    
    ''' test missing column '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkMissingColumn.csv", "./vitess_test/imageFeature_test_standard.csv")

    ''' test missing values '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkMissingValues.csv", "./vitess_test/imageFeature_test_standard.csv")

    ''' test empty cell '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkEmptyCell.csv", "./vitess_test/imageFeature_test_standard.csv")

    ''' test add same things twice '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkInsertExistValue.csv", "./vitess_test/imageFeature_test_standard.csv")



    ''' TEST ImageVideo FILE with feature csv, with ImageVideo csv correct all the time'''

    ''' 14. test wrong hearder name '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_checkHeader.csv")
    
    # TODO: This should not fail
    ''' 15. test exceed column '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_checkExceedColumn.csv")

    ''' 16. test missing column '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_checkMissingColumn.csv")

    ''' 17. test missing values '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_checkMissingValues.csv")

    ''' 18. test empty cell '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_checkEmptyCell.csv")

    ''' 19. test add same things twice '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_standard.csv", "./vitess_test/imageFeature_test_checkInsertExistValue.csv")


    
    ''' TEST ImageVideo FILE with feature csv, both invalid'''
    ''' This section is obsoleted, any violation of csv format will exit the program '''

    ''' test wrong hearder name '''
    #db.insert_image('any', './test_images/', "./vitess_test/imageVideo_test_checkHeader.csv", "./vitess_test/imageFeature_test_checkHeader.csv")
    
    ''' test exceed column '''
    #db.insert_image("./vitess_test/imageVideo_test_checkExceedColumn.csv", "./vitess_test/imageFeature_test_checkExceedColumn.csv")
    
    ''' test missing column '''
    #db.insert_image("./vitess_test/imageVideo_test_checkMissingColumn.csv", "./vitess_test/imageFeature_test_checkMissingColumn.csv")

    ''' test missing values '''
    #db.insert_image("./vitess_test/imageVideo_test_checkMissingValues.csv", "./vitess_test/imageFeature_test_checkMissingValues.csv")

    ''' test empty cell -- FAIL !!!!!!!!!! '''
    #db.insert_image("./vitess_test/imageVideo_test_checkEmptyCell.csv", "./vitess_test/imageFeature_test_checkEmptyCell.csv")

    ''' test add same things twice '''
    #db.insert_image("./vitess_test/imageVideo_test_checkInsertExistValue.csv", "./vitess_test/imageFeature_test_checkInsertExistValue.csv")




test()









