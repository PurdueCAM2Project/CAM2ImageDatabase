import cv2
import numpy as np
import detection.utils as utils
import tensorflow as tf
from PIL import Image
import os
from tensorflow.python.client import device_lib

def getBbox(image_dir, image_name, show_plot=False):
    return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
    pb_file         = "./detection/yolov3_coco.pb"
    image_path      = os.path.join(image_dir, image_name)
    num_classes     = 80
    input_size      = 416
    graph           = tf.Graph()

    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image_size = original_image.shape[:2]
    image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size])
    image_data = image_data[np.newaxis, ...]

    return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)
    device_name = "/gpu:1"

    local_device_protos = device_lib.list_local_devices()
    print(x.name for x in local_device_protos if x.device_type == 'GPU')
    '''
    if device_name != 'device:gpu:1':
        raise SystemError('GPU device not found')
    print('Found GPU at: {}'.format(device_name))
    '''
    with tf.device('/gpu:1'):
        with tf.Session(graph=graph) as sess:
            #devices = sess.list_devices()
            #print(devices)
            pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
                [return_tensors[1], return_tensors[2], return_tensors[3]],
                        feed_dict={ return_tensors[0]: image_data})

        pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                                np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                                np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)

        bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.3)
        bboxes = utils.nms(bboxes, 0.45, method='nms')
        #print (type(bboxes)) - List of lists
        #print (bboxes)-  bboxes: [x_min, y_min, x_max, y_max, probability, cls_id] format coordinates.
        if show_plot:
            image = utils.draw_bbox(original_image, bboxes)
            image = Image.fromarray(image)
            image.show()

    return bboxes
