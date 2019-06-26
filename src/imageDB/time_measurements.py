import csv

class TimeMeasurements(object):
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

    def WriteUploadTimes(self, ui_times=[]):
        """ Write list of times to output file 'image_upload_times.csv' """
        for i in ui_times:
            self.uif.writerow(i)
        self.uif.close()

    def WriteVideoQueryTimes(self, vq_times=[]):
        """ Write list of times to output file 'video_query_times.csv' """
        for i in vq_times:
            self.vqf.writerow(i)
        self.vqf.close()


