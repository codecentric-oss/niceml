"""cython module to transform mask images to target mask images"""
import numpy
cimport numpy

ctypedef numpy.int_t DTYPE_t

def transform_mask_image(numpy.ndarray[unsigned char, ndim=3] mask_image, numpy.ndarray[DTYPE_t, ndim=2] color_array, numpy.ndarray[DTYPE_t, ndim=2] out_mask_image):
    """
    This function works similar like a LUT.
    Args:
        mask_image: Input mask values. Also works with colors.
        color_array: size: num_classes x color_channels
        out_mask_image: Same size as mask image but without the 3rd axis.
            All values are 255.

    Returns:
        If the values of one row in the color array are the same as for one pixel the
        corresponding out_mask_image is set to the row_idx (same as class_idx).
    """
    cdef int y_size, x_size, cls_count
    cdef int cur_x, cur_y, cur_color_idx
    cdef int channels, cur_channel
    y_size = mask_image.shape[0]
    x_size = mask_image.shape[1]
    cls_count = color_array.shape[0]
    channels = color_array.shape[1]
    cdef int set_value = 0

    for cur_y in range(y_size):
        for cur_x in range(x_size):
            for cur_color_idx in range(cls_count):
                for cur_channel in range(channels):
                    color_val = color_array[cur_color_idx, cur_channel]
                    set_value = 1
                    if color_val != -1 and color_val != mask_image[cur_y, cur_x, cur_channel]:
                        set_value = 0
                        break
                if set_value == 1:
                    out_mask_image[cur_y, cur_x] = cur_color_idx

    return out_mask_image
