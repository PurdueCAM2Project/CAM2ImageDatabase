from imageDB import ImageDB

def query_videos_test():
    # query video
    db = ImageDB()
    # TODO: arguments type
    arguments = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': 'US', 'Camera_ID': None, 'date': None, 'start_time': None, 'end_time': None, 'download': True,'feature': None}
    db.get_video(arguments)


query_videos_test()
