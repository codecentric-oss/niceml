#!python
#cython: language_level=3

import numpy
cimport numpy

ctypedef numpy.float_t DTYPE_t

def cy_calc_iou(numpy.ndarray[DTYPE_t, ndim=3] data, numpy.ndarray[DTYPE_t, ndim=3] gt,
            double threshold):
    cdef int y_size, x_size, cls_count
    cdef int cur_x, cur_y
    cdef double data_val, gt_val, cur_union, cur_intersect
    cdef double one = 1.0
    cdef double zero = 0.0

    intersect_sum = list()
    union_sum = list()
    y_size = data.shape[0]
    x_size = data.shape[1]
    cls_count = data.shape[2]
    for cls in range(cls_count):
        cur_intersect = 0.0
        cur_union = 0.0

        for cur_x in range(x_size):
            for cur_y in range(y_size):
                data_val = data[cur_y, cur_x, cls]
                data_val = one if data_val >= threshold else zero
                gt_val = gt[cur_y, cur_x, cls]
                if data_val == one and gt_val == one:
                    cur_intersect += one
                if data_val == one or gt_val == one:
                    cur_union += one
        intersect_sum.append(cur_intersect)
        union_sum.append(cur_union)

    return numpy.array(intersect_sum), numpy.array(union_sum)
