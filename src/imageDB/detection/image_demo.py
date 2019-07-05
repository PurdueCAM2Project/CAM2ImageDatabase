import cv2
import numpy as np
import numba
import detection.utils as utils
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
from tensorflow.python.client import device_lib
import time
#os.environ['NUMBA_DISABLE_JIT'] = '1'


def initial():
    return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
    pb_file = "./detection/yolov3_coco.pb"
    graph = tf.Graph()
    return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)
    sess = tf.Session(graph=graph)
    return return_tensors, graph, sess


#Seems like the program is running on gpu but the time is increased because the session is being started everytime in the loop and it is taking time to start and asssign the gpu for a certain computation
def getBbox(return_tensors, image_dir, image_name, sess, show_plot=False):

    image_path      = os.path.join(image_dir, image_name)
    num_classes     = 80
    input_size      = 416
    #print (type(return_tensors))
    #print (type(return_tensors[0]))
    #print (type(return_tensors[1]))
    #for op in graph.get_operations():
    #    print(str(op.name))

    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image_size = original_image.shape[:2]
    a = time.time()
    image_data = utils.image_preprocess(np.copy(original_image), [input_size, input_size])
    #print("================>preprocess :", time.time() - a)
    image_data = image_data[np.newaxis, ...]


    #a = time.time()
    #with graph.device('/device:GPU:1'):
        #with tf.Session(graph=graph) as sess:

     #, config = tf.ConfigProto(device_count = {'GPU':0}))
    #sess = tf.Session(graph = graph)
    pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
                [return_tensors[1], return_tensors[2], return_tensors[3]],      #we can most probably split this into 3 different sessions but thats for later
                        feed_dict={return_tensors[0]: image_data})
    #print("================>pred :", time.time() - a)
    #b = time.time()
    pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                            np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                            np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)
    #print("================>conct :", time.time() - b)

    #b = time.time()
    bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.3)
    bboxes = utils.nms(bboxes, 0.45, method='nms')
    #print("================>boxes :", time.time() - b)
    #print("prediction session : ", time.time() - a)

    if show_plot:
        image = utils.draw_bbox(original_image, bboxes)
        #image = Image.fromarray(image)

        #image.show()
        filename = str(time.time())
        cv2.imwrite("./output_images/" + filename + ".jpg", image)

    return bboxes
