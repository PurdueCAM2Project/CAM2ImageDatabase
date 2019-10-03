from routine import Routine
from vitess_connection import VitessConn
import detection.utils as utils
import time
import multiprocessing
from cam_setup import divide_cams
from imageDB import ImageDB
import config
import sys
import os
import argparse


def _retrieveImage_alias(args):
    example = Routine()
    example.retrieveImage(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])

def build_up_test(num_of_cams, is_real_camera, num_procs, diff_thresh, store_interval):
    # Handle exceptions and edge cases
    if num_procs > 3:
        print ('Please limit number of processes to 3\n') #Limit processes to 3 to prevent memory error
        return
    if num_procs > num_of_cams:
        print ('Cannot start more processes than number of cameras')
        print ('Reducing number of processes to {}...\n'.format(num_procs))
        num_procs = num_of_cams

    # Initialize start time variable and routine object
    start_time = time.perf_counter()
    print("\nInitializing Connection...")

    print("Finished connection intialization... ELAPSED: ", time.perf_counter() - start_time)

    print("querying camera data..." + "------> ", end="")
    timestamp = time.perf_counter()


    print("{} seconds\n".format(time.perf_counter() - timestamp))

    #Read predefined classes from class names file
    classes = utils.read_class_names("my_classes.names")
    class_dict = {}

    vitess = VitessConn()
    for i in range(len(classes)):
        class_dict.update({classes[i]: vitess.getFeature(classes[i])})

    # Assign Cameras to media list
    if is_real_camera == 'ip':
        imageDB = ImageDB()
        media_list, header = imageDB.read_data('camera_list.csv', config.CAM_HEADER, 'tuple', None)
        media_list = divide_cams(media_list, num_of_cams, num_procs)

    elif is_real_camera == 'our_vid':
        media_list = ['video_moving.mp4']
        #media_list = [['video_moving.mp4'], ['video_static.mp4'], ['video_moving.mp4'], ['video_static.mp4'], ['video_moving.mp4'], ['video_static.mp4'], ['video_moving.mp4'], ['video_static.mp4'], ['video_moving.mp4'], ['video_static.mp4']]  # 'video_static.mp4', 'video_inbetween.mp4']

        if num_procs < num_of_cams:
            chunked_media = [media_list[0], media_list[1], media_list[2]]
            for media in range(3, len(media_list[:num_of_cams])):
                chunked_media[media%3].append(media_list[media][0])
            media_list = chunked_media
            print (len(media_list[0]))
            print (len(media_list[1]))
            print (len(media_list[2]))


    else:
        print ('is_real_camera flag set to invalid value')
        print ('Valid values for is_real_camera: ip, our_vid')
        return
    # Start multiprocessing
    '''
    args = []
    for PID in range(num_procs):
        args.append((media_list[PID], is_real_camera, diff_thresh, store_interval, PID, num_procs, class_dict, classes))

    with multiprocessing.Pool(num_procs) as pool:
        pool.map(_retrieveImage_alias, args)
    '''
    

    myroutine = Routine()
    myroutine.retrieveImage(media_list, is_real_camera, diff_thresh, store_interval, 0, num_procs, class_dict, classes)
    

    print('Full video: ', time.perf_counter() - start_time)
    print('Finished')

# Parsing Arguments from User
parser = argparse.ArgumentParser(description='Test Build Up')
parser.add_argument('--num_cams', type=int, default=1,
                    help='Number of cameras')
parser.add_argument('--num_procs', type=int, default=1,
                    help='Number of Processes')
parser.add_argument('--is_real_camera', default='our_vid',
                    help='ip or our_vid')
parser.add_argument('--diff', type=float, default=0.85,
                    help='difference threshold')
parser.add_argument('--store_interval', type=float, default=0.1,
                    help='store interval')

if __name__ == '__main__':
    arguments = parser.parse_args()
    build_up_test(arguments.num_cams, arguments.is_real_camera, arguments.num_procs, arguments.diff, arguments.store_interval)
    '''
    This user can pass in 5 arguments as input.

    Argument 1, type: int, Default = 1
        - This is a number representing how many cameras(videos)
          the user wants to use capture images from.

    Argument 2, type: int, Default = 1
        - The number of processes used in multiprocessing will be
          inputted by the user as the third argument.

    Argument 3, type: str, options: 'ip' / 'our_vid'
        - This decides whether or not the program will use real
          ip cameras, or the test videos.
        - camera: yes it will use real cameras, it will import the
          cameras information from the 'camera_list.csv' (if used
          when 'db_build.py' is run).
        - video: no it will not use real cameras, instead it uses
          the test videos we've taken.

    Argument 4, type: float, Default = 0.85
        - The difference threshold can be changed by the user

    Argument 5, type: float, Default = 0.1
        - The store interval can be changed by the user
    '''
