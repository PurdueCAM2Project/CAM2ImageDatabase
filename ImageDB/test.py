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








    #test image retrieval 

    #db.batch_insert_camera("./vitess_test/camera_test_standard.csv")

    '''test time range query''' 
    #arg1 = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': None, 'camera_id': None, 'date': None, 'start_time': '13:00:00', 'end_time': '14:00:00', 'download': None}
    #db.get_image(arg1)

    ''' test time range and date query '''
    #arg2 = {'latitude': 72.06, 'longitude': None, 'city': None, 'state': 'NY', 'country': None, 'camera_id': None, 'date': '02/01/2019', 'start_time': '20:00:00', 'end_time': '18:00:00', 'download': None}
    #db.get_image(arg2)


    '''test camera_id and city query'''
    #arg3 = {'latitude': None, 'longitude': None, 'city': 'Boston', 'state': None, 'country': None, 'camera_id': '1', 'date': None, 'start_time': None, 'end_time': None, 'download': None}
    #db.get_image(arg3)

    '''test state and camera_id query'''
    #arg4 = {'latitude': None, 'longitude': None, 'city': None, 'state': 'MA', 'country': None, 'camera_id': '1', 'date': None, 'start_time': None, 'end_time': None, 'download': None}
    #db.get_image(arg4)

    '''test country only query'''
    #arg5 = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': 'USA', 'camera_id': None, 'date': None, 'start_time': None, 'end_time': None, 'download': None}
    #db.get_image(arg5)

    ''' test latitude and longitude '''


    ''' test no matching results '''
    #arg6 = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': 'UK', 'camera_id': '1', 'date': None, 'start_time': None, 'end_time': None, 'download': None}
    #db.get_image(arg6)


    ''' test download data '''
    #arg7 = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': None, 'camera_id': '1', 'date': None, 'start_time': None, 'end_time': None, 'download': '1'}
    #db.get_image(arg7)


    '''test city only query'''
    #arg8 = {'latitude': None, 'longitude': None, 'city': 'Boston', 'state': None, 'country': None, 'camera_id': None, 'date': None, 'start_time': None, 'end_time': None, 'download': None}
    #db.get_image(arg8)






test()









