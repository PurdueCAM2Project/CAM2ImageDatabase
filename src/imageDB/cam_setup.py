from camera import Camera
import cv2

def setup_cams(data):
    # Create camera objects
    cam = Camera(camera_id=data[0], ip_address=data[1], image_path=data[2], video_path=data[3])

    # Initialize camera capture object
    cam.capture = cv2.VideoCapture(cam.video_path)

    return cam

# TODO: camera ID should be seperated from PID
def setup_vids(video, PID):
    # Create camera objects
    cam = Camera(camera_id=str(PID), ip_address='0000', image_path=video, video_path=video)

    # Initialize camera capture object
    cam.capture = cv2.VideoCapture(video)

    return cam
