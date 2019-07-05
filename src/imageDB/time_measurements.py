import csv

class TimeMeasurements:
    '''
    def __init__(self):
        """ Initialize files """
        # uif = upload image file
        with open('image_upload_times.csv', 'w', newline='') as file1:
            ui_writer = csv.writer(file1)
            ui_writer.writerow(['Camera Upload Times'])
        self.uif = file1
        # vq = video query file
        with open('video_query_times.csv', 'w', newline='') as file2:
            vq_writer = csv.writer(file2)
            vq_writer.writerow(['Video Query Times'])
        self.vqf = file2
    '''
    def WriteUploadTimes(self, ui_times):
        """ Write list of times to output file 'image_upload_times.csv' """
        with open('image_upload_times.csv', 'w', newline='') as file1:
            ui_writer = csv.writer(file1)
            ui_writer.writerow(['Camera Upload Times'])
            for i in ui_times:
                print(i)
                ui_writer.writerow(i)
                
        file1.close()

    def WriteVideoQueryTimes(self, vq_times):
        """ Write list of times to output file 'video_query_times.csv' """
        with open('image_upload_times.csv', 'w', newline='') as file1:
            ui_writer = csv.writer(file1)
            ui_writer.writerow(['Camera Upload Times'])
            for i in vq_times:
                ui_writer.writerow(i)
                
        file2.close()


