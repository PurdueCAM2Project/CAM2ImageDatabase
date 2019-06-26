from imageDB import ImageDB
from time_measurements import TimeMeasurements

def query_videos_test():
   # query video
   db = ImageDB()
   tm = TimeMeasurements()
   vq_time_list = []
   # TODO: arguments type
   arguments = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': 'US', 'Camera_ID': None, 'date': None, 'start_time': None, 'end_time': None, 'download': True,'feature': None}

   vq_time = time.time()                   ####

   db.get_video(arguments)

   vq_time = time.time() - vq_time         ####
   vq_time_list.append(vq_time)            ####
   tm.WriteVideoQueryTimes(vq_time_list)   ####

query_videos_test()
