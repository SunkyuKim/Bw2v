"""
Util Functions
"""
import numpy as np
import time
import datetime
import os
import tensorflow as tf

def time_checker(func):
    def new_func(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print "\t".join(["Time elpased",func.__name__, str(end-start)])
        return result
    return new_func


def get_time_str():
    d = datetime.datetime.now()
    d_list = [d.year, d.month, d.day, d.hour, d.minute, d.second]
    return_str = "_".join([str(v) for v in d_list])
    return return_str

def make_folder_by_time(dir):
    return_dir = dir+ "/" + get_time_str()
    os.mkdir(return_dir)
    return return_dir


def accuracy(predictions, labels):
  return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
          / predictions.shape[0])


def variable_summaries(var, name):
  with tf.name_scope("summaries"):
    mean = tf.reduce_mean(var)
    tf.scalar_summary('mean/' + name, mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_sum(tf.square(var - mean)))
    tf.scalar_summary('sttdev/' + name, stddev)
    tf.scalar_summary('max/' + name, tf.reduce_max(var))
    tf.scalar_summary('min/' + name, tf.reduce_min(var))
    tf.histogram_summary(name, var)


if __name__ == '__main__':
    a = tf.constant(1)
    b = a + 1
    c = b + 1

    s = tf.Session()
    r1, r2 = s.run([b,c])

    print r1,r2