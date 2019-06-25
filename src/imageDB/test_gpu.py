import sys
import numpy as np
import tensorflow as tf
from datetime import datetime
import os


print ("GPU Available aaaaaaaaaaaaaaaaaaaaaaaaaa: ",tf.test.is_gpu_available())
device_name = sys.argv[1]
shape = (int(sys.argv[2]), int(sys.argv[2]))

with tf.device('/gpu:0'):
    random_matrix = tf.random.uniform(shape=shape, minval=0, maxval=1)
    dot_operation = tf.matmul(random_matrix, tf.transpose(random_matrix))
    sum_operation = tf.reduce_sum(dot_operation)

startTime = datetime.now()
with tf.Session(config = tf.ConfigProto(log_device_placement=True)) as session:
    result = session.run(sum_operation)
    print (result)

print ("\n" * 5)
print ("Shape:", shape, "Device:", device_name)
print ("Time taken:", datetime.now() - startTime)

print ("\n" * 5)

