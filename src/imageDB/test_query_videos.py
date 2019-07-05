from imageDB import ImageDB
import time
import csv

def query_videos_test():
   # query video
   db = ImageDB()
   vq_time_list = []
   # TODO: arguments type
   arguments = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': 'US', 'Camera_ID': None, 'date': None, 'start_time': None, 'end_time': None, 'download': True,'feature': None}

   vq_time = time.time()                   ####

   db.get_video(arguments)
'''
   vq_time = time.time() - vq_time         ####
   vq_time_list.append(vq_time)            ####
   with open('image_upload_times.csv', 'w', newline='') as file1:
       ui_writer = csv.writer(file1)
       ui_writer.writerow(['Camera Upload Times'])
       for i in vq_times:
           ui_writer.writerow([i])
    file1.close()
'''
query_videos_test()
