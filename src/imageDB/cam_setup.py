from camera import Camera
import cv2
from framerate import *


def findmin(min_list):
    """
    :param min_list: list of items
    :return: minimum value within the inputted list
    """
    return min_list.index(min(min_list))


def setup_cams(data, coords):
    """
    Using information from arguments, initialize a camera object.

    :param data: camera ID, IP, image path, and video path
    :param coords: cropping coordinates used to improve accuracy and efficiency of difference measurement
    :return: camera object
    """
    # Create camera object
    cam = Camera(camera_id=data[0], ip_address=data[1], image_path=data[2], video_path=data[3],
                 x_max=coords[0], x_min=coords[1], y_max=coords[2], y_min=coords[3])

    # Initialize camera capture object
    cam.capture = cv2.VideoCapture(cam.video_path)

    return cam


# TODO: camera ID should be seperated from PID
def setup_vids(video, PID, is_real_camera):
    """
    Using information from arguments, initialize a camera object from a video file.

    :param video:   str, name of video file
    :param PID:     int, process id
    :return:        initialized camera object
    """
    if is_real_camera == 'our_vid':
        coords = [0, 1920, 0, 1080]

        # Select cropping dimensions
        if video == 'video_moving.mp4':
            coords = [0, 1920, 400, 1080]
        elif video == 'video_static.mp4':
            coords = [250, 1000, 650, 1080]
        elif video == 'video_inbetween.mp4':
            coords = [0, 1300, 300, 1080]
        elif video == 'long_video_moving.mp4':
            coords = [0, 1920, 400, 1080]

        # Create camera object
        cam = Camera(camera_id=str(PID), ip_address='0000', image_path=video, video_path=video, x_max=coords[0],
                 x_min=coords[1], y_max=coords[2], y_min=coords[3])

    elif is_real_camera == 'public_vid':
        # Create camera object
        cam = Camera(camera_id=str(PID), ip_address='0000', image_path=video, video_path=video, x_max=288,
                 x_min=0, y_max=360, y_min=0)

    # Initialize camera capture object
    cam.capture = cv2.VideoCapture(video)

    return cam


def divide_cams(info_list, num_of_cams, num_procs):
    """
    Using the info_list, distribute the camera workload based on normalized values for
    each cameras frame rate and resolution.

    :param info_list: camera information
    :param num_of_cams: number of camera objects to be divided
    :param num_procs: number of processes to divide cameras into
    :return: list, an evenly divided list of camera information
    """

    # Initialize variables
    media_list = []
    divided_list = []
    size = 0

    # Add up the image sizes
    i = 0
    new_list = []
    new_sublist = []
    for info in info_list:
        if i >= num_of_cams:
            break
        else:
            fps = get_fps('http://' + info[8] + info[11])
            print(fps, info[0])
            new_sublist.append(info[0])
            new_sublist.append(info[8])
            new_sublist.append(info[10])
            new_sublist.append(info[11])
            new_sublist.append(int(info[6]) * int(info[7]))
            print(info[6], info[7])
            new_sublist.append(fps)
            size += int(new_sublist[4])
            i += 1
            new_list.append(new_sublist)
            new_sublist = []

    if num_procs == 1:
        return [new_list]

    # Find range of fps and resolution
    resolution_range = max(new_list, key=lambda x: (x[4]))[4] - min(new_list, key=lambda x: (x[4]))[4]
    fps_range = max(new_list, key=lambda x: (x[5]))[5] - min(new_list, key=lambda x: (x[5]))[5]
    print(resolution_range, fps_range)

    # Normalize fps and resolution based on range and multiply normalized values
    for cam in new_list:
        cam.append((cam[4] / resolution_range) * (cam[5] / fps_range))
        print((cam[4] / resolution_range) * (cam[5] / fps_range))

    # Reverse sort based on normalized values
    new_list = sorted(new_list, reverse=True, key=lambda x: (x[6]))

    # Add first 3 elements from reverse sorted list
    temp_list = []
    min_track_list = []
    for cam in range(num_procs):
        temp_list.append(new_list[cam][0:4])
        divided_list.append(temp_list)
        min_track_list.append(new_list[cam][6])
        temp_list = []

    # Keep adding to min normalized value among processes
    min_idx = 0
    for cam in range(num_procs, len(new_list)):
        min_idx = findmin(min_track_list)
        divided_list[min_idx].append(new_list[cam][0:4])
        min_track_list[min_idx] = min_track_list[min_idx] + new_list[cam][6]

    return divided_list
