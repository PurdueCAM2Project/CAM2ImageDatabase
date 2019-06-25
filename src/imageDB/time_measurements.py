import csv

class TimeMeasurements(object):
    def __init__(self):
        with open('image_uploading_times.csv', 'w', newline='') as file1:
            upload_writer = csv.writer(file1)
            upload_writer.writerow(['Image Uploaded Number', 'Time to Upload Image'])

        self.upload_time = file1
        self.image_upload_count = 0

        with open('video_query_times.csv', 'w', newline='') as file2:
            vq_writer = csv.writer(file2)
            vq_writer.writerow(['Video Number', 'Time to Query Video'])

        self.vq_time = vq_writer
        self.vq_count = 0

    def WriteUploadTimes(time, self):
        self.image_upload_count = self.image_upload_count + 1
        self.upload_time.writerow([self.image_upload_count, time])

    def WriteVideoQueryTimes(time, self):
        self.vq_count = self.vq_count + 1
        self.vq_time.writerow([self.vq_count, time])

    def CloseWriters(self):
        print('<=================================================================>')
        #self.upload_time.close()
