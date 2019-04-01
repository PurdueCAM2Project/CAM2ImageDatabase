import os, time
import filetype
import csv

path = '/Users/sandeepgupta/Desktop/CAM2/script/results'
minio_link = 'None'
dataset = 'None'
is_processed = 0

try:
    output_file = open('file_name.csv', 'w')

    fields = ['file_name', 'camera_id', 'file_size', 'file_type', 'file_time', 'Minio_link', 'Dataset', 'isProcessed']
    writer = csv.writer(output_file)
    writer.writerow(fields)

    dirs = os.listdir(path)

    for subdir in dirs:
        path2 = os.path.join(path, subdir)
        if os.path.isfile(path2):
            continue
        for f in os.listdir(path2):
            curr_path = os.path.join(path2, f)
            if os.path.isdir(curr_path):
                continue
            st = os.stat(curr_path)
            file_size = st.st_size
            file_time = time.asctime(time.localtime(st.st_mtime))

            ftype = filetype.guess(curr_path)
            if ftype:
                file_type = ftype.extension

            writer.writerow([f, subdir, file_size, file_type, file_time, minio_link, dataset, is_processed])   # add the camera id to the csv file as well

except Exception as e:
    if output_file:
        output_file.close()
    print(e)

output_file.close()
