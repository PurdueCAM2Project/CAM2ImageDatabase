import os, time
import filetype
import csv
import sys


def image_metadata(path):

    minio_link = 'None'
    dataset = 'None'
    is_processed = 0

    try:
        output_file = open('file_name.csv', 'w')

        fields = ['IV_Name', 'Camera_ID', 'IV_date', 'IV_time', 'File_type', 'File_size', 'Minio_link', 'Dataset',
                  'is_processed']
        writer = csv.writer(output_file)
        writer.writerow(fields)

        try:
            dirs = os.listdir(path)
        except Exception as e:
            print("Path is not a valid directory")
            sys.exit(1)

        for subdir in dirs:
            path2 = os.path.join(path, subdir)
            if os.path.isfile(path2):
                st = os.stat(path2)
                file_size = st.st_size
                file_date = time.strftime('%Y.%m.%d', time.localtime(os.path.getmtime(path2)))
                file_time = time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(path2)))

                ftype = filetype.guess(curr_path)
                if ftype:
                    file_type = ftype.extension

                writer.writerow([subdir, 'None', file_date, file_time, file_type, file_size, minio_link, dataset,
                                 is_processed])  # add the camera id to the csv file as well
                continue
            for f in os.listdir(path2):
                curr_path = os.path.join(path2, f)
                if os.path.isdir(curr_path):
                    continue
                st = os.stat(curr_path)
                file_size = st.st_size
                file_date = time.strftime('%Y.%m.%d', time.localtime(os.path.getmtime(curr_path)))
                file_time = time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(curr_path)))

                ftype = filetype.guess(curr_path)
                if ftype:
                    file_type = ftype.extension

                writer.writerow([f, subdir, file_date, file_time, file_type, file_size, minio_link, dataset,
                                 is_processed])  # add the camera id to the csv file as well

    except Exception as e:
        if output_file:
            output_file.close()
        print(e)

    output_file.close()
