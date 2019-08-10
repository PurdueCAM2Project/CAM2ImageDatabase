import cv2
import os
import shutil
import numpy as np
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import detection.utils as utils
from detection.config import cfg
from detection.yolov3 import YOLOV3
from PIL import Image
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1, 2"

class YoloTest(object):
    def __init__(self, PID, classes):
        #import tensorflow as tf
        self.input_size       = cfg.TEST.INPUT_SIZE
        #self.anchor_per_scale = cfg.YOLO.ANCHOR_PER_SCALE
        self.classes          = classes #utils.read_class_names(cfg.YOLO.CLASSES)
        self.num_classes      = len(self.classes)
        #self.anchors          = np.array(utils.get_anchors(cfg.YOLO.ANCHORS))
        self.score_threshold  = cfg.TEST.SCORE_THRESHOLD
        self.iou_threshold    = cfg.TEST.IOU_THRESHOLD
        self.moving_ave_decay = cfg.YOLO.MOVING_AVE_DECAY
        #self.annotation_path  = cfg.TEST.ANNOT_PATH
        self.weight_file      = cfg.TEST.WEIGHT_FILE
        self.PID = PID
        #self.write_image      = cfg.TEST.WRITE_IMAGE
        #self.write_image_path = cfg.TEST.WRITE_IMAGE_PATH
        #self.show_label       = cfg.TEST.SHOW_LABEL
        #self.show_label       = cfg.TEST.SHOW_LABEL

        if PID == 3:
            os.environ["CUDA_VISIBLE_DEVICES"] = "1"
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"


        with tf.name_scope('input'):
            self.input_data = tf.placeholder(dtype=tf.float32, name='input_data')
            self.trainable  = tf.placeholder(dtype=tf.bool,    name='trainable')

        model = YOLOV3(self.input_data, self.trainable)
        self.pred_sbbox, self.pred_mbbox, self.pred_lbbox = model.pred_sbbox, model.pred_mbbox, model.pred_lbbox

        with tf.name_scope('ema'):
            ema_obj = tf.train.ExponentialMovingAverage(self.moving_ave_decay)
        config = tf.ConfigProto()
        '''
        if PID == 0:
            config = tf.ConfigProto(device_count = {'GPU':2})
            print ('if')
        elif PID == 1:
            config = tf.ConfigProto(device_count = {'GPU':2})
            print ('elif')
        else:
            config = tf.ConfigProto(device_count = {'GPU':2})
            print ('else')
        '''

        #config.gpu_options.visible_device_list = '0' #this line not doing anythin
        #config.gpu_options.per_process_gpu_memory_fraction = 0.33
        config.gpu_options.allow_growth = True
        config.allow_soft_placement=True
        self.sess = tf.Session(config=config)
        self.saver = tf.train.Saver(ema_obj.variables_to_restore())
        self.saver.restore(self.sess, self.weight_file)

    def predict(self, image, show_plot = False):

        org_h, org_w, _ = image.shape

        image_data = utils.image_preporcess(image, [self.input_size, self.input_size])
        image_data = image_data[np.newaxis, ...]
        pred_sbbox, pred_mbbox, pred_lbbox = self.sess.run(
            [self.pred_sbbox, self.pred_mbbox, self.pred_lbbox],
            feed_dict={
                self.input_data: image_data,
                self.trainable: False
            }
        )

        pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + self.num_classes)),
                                    np.reshape(pred_mbbox, (-1, 5 + self.num_classes)),
                                    np.reshape(pred_lbbox, (-1, 5 + self.num_classes))], axis=0)
        bboxes = utils.postprocess_boxes(pred_bbox, (org_h, org_w), self.input_size, self.score_threshold)
        bboxes = utils.nms(bboxes, self.iou_threshold)
        if show_plot:
            image = utils.draw_bbox(image, bboxes)
            filename = str(time.time())
            cv2.imwrite("./detected_images/" + filename + ".jpg", image)
        return bboxes
