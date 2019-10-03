from imageDB import ImageDB
import time
import csv


def query_test():
   # query video
   db = ImageDB()
   vq_time_list = []
   # TODO: arguments type

   arguments = {'latitude': None, 'longitude': None, 'city': None, 'state': None, 'country': None, 'Camera_ID': '0',
                'date': None, 'start_time': None, 'end_time': None, 'download': "True", 'feature': None, 'size': 5000}

   query_time = time.time()
   ####
   db.get_video(arguments)
   #db.cam_images()
   ####
   print("Time taken to query: {}".format(time.time() - query_time))

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
query_test()
