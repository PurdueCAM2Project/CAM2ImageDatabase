from routine import Routine
from vitess_connection import VitessConn
import detection.utils as utils
import time
import multiprocessing
from camera import Camera
from cam_setup import setup_cams
import cv2
import sys
import subprocess

def build_up_test(num_of_cams, is_real_camera):
    # Initialize start time variable and routine object
    start_time = time.perf_counter()
    print("\nInitializing Connection...")
    example = Routine()
    print("Finished connection intialization... ELAPSED: ", time.perf_counter() - start_time)

    print("querying camera data..." + "------> ", end="")
    timestamp = time.perf_counter()

    # Set up cameras
    #cam_data = example.db.get_all_cameras(num_of_cams)

    print("{} seconds\n".format(time.perf_counter() - timestamp))
    processes = []

    classes = utils.read_class_names("my_classes.names")
    class_dict = {}

    vitess = VitessConn()
    for i in range(len(classes)):
        class_dict.update({classes[i] : vitess.getFeature(classes[i])})

    # Start multiprocessing
    if is_real_camera:
        media_list = example.db.get_all_cameras(num_of_cams)
    else:
        media_list = ['video_moving.mp4', 'video_static.mp4', 'video_inbetween.mp4']

    for PID in range(num_of_cams):
        print("Start retrieveImage...\n")
        p = multiprocessing.Process(target=example.retrieveImage, args=(media_list, is_real_camera, 1.0, 0.1, PID, class_dict))
        processes.append(p)
        p.start()

    print ('Active Processes:', len(processes), '\n')

    # Merge the processes
    for process in processes:
        process.join()

    print ('Full video: ', time.perf_counter() - start_time)
    print('Finished')

if __name__ == '__main__':
    build_up_test(3, False)
    '''
    This file takes in two arguments as input.
    
    argv[1], type: str, options: 'camera' / 'video' 
        - This decides whether or not the program will use real
          ip cameras, or the test videos.
        - camera: yes it will use real cameras, it will import the 
          cameras information from the 'camera_list.csv' (if used 
          when 'db_build.py' is run).
        - video: no it will not use real cameras, instead it uses
          the test videos we've taken.
    
    argv[2], type: int
        - This is a number representing how many cameras(videos)
          the user wants to use capture images from.
    '''

    # Bash script to end subprocesses
    #subprocess.call('end_process.sh')
    '''
    if sys.argv[1] == 'camera':
        build_up_test(sys.argv[2], True)

    elif sys.argv[1] == 'video':
        build_up_test(sys.argv[2], False)

    else:
        print('Incorrect input arguments!')
        print('argv[1]: "camera" or "video"')
        print('argv[2]: integer greater than zero')
        '''
