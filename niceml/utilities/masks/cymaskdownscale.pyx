"""cython module for downscale mask hist function"""
import numpy
cimport numpy
import numpy as np

ctypedef numpy.int_t DTYPE_t
ctypedef numpy.int8_t DTYPE_int8

def cy_mask_downscale(numpy.ndarray[unsigned char, ndim=2] mask_img,
                      numpy.ndarray[DTYPE_t, ndim=3] hist_array, default_value: int,
                      ds_factor: int):
    """Calculates the histogram mask image in cython to be faster than in plain python"""
    cdef int y_size, x_size
    cdef int cur_x, cur_y, cur_mask_val
    cdef int target_hist_x, target_hist_y
    cdef int cdefault_value, cds_factor
    y_size = mask_img.shape[0]
    x_size = mask_img.shape[1]
    cds_factor = ds_factor
    cdefault_value = default_value

    for cur_y in range(y_size):
        for cur_x in range(x_size):
            cur_mask_val = mask_img[cur_y, cur_x]
            if cur_mask_val != cdefault_value:
                target_hist_x = int(np.floor_divide(cur_x, cds_factor))
                target_hist_y = int(np.floor_divide(cur_y, cds_factor))

                hist_array[target_hist_y, target_hist_x, cur_mask_val] = \
                    hist_array[target_hist_y, target_hist_x, cur_mask_val] + 1

    return hist_array
