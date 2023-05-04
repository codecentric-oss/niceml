import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import Model

from niceml.data.datadescriptions.objdetdatadescription import ObjDetDataDescription
from niceml.dlframeworks.tensorflow.models.retinanet import RetinaNetFactory
from niceml.utilities.imagesize import ImageSize


def test_retinanet_factory():
    factory = RetinaNetFactory()
    img_size = ImageSize(1024, 1024)
    classes = ["a", "b", "c"]
    datadesc = ObjDetDataDescription(
        featuremap_scales=[8, 16, 32, 64, 128],
        classes=classes,
        input_image_size=img_size,
        anchor_aspect_ratios=[1, 0.5, 2.0],
        anchor_scales=[1, 1.25, 1.6],
        anchor_base_area_side=4,
        box_variance=[0.1, 0.1, 0.2, 0.2],
    )
    assert datadesc.get_anchorcount_per_image() == 196416
    retina_model: Model = factory.create_model(datadesc)
    # retina_model.build((None, 1024, 1024, 3))
    retina_model.summary()
    input_img = np.zeros((2, img_size.width, img_size.height, 3))
    output = retina_model.predict(input_img)
    shape = tf.shape(output).numpy()
    assert np.array_equal(shape, np.array([2, 196416, 7]))
    # :1 = 147456 :: 147456 = 128 * 128 * 9
    # :2 = 184320 :: 36864 = 64 * 64 * 9
    # :3 = 193536 :: 9216 = 32 * 32 * 9
    # :4 = 195840 :: 2304 = 16 * 16 * 9
    # :5 = 196416 :: 576 = 8 * 8 * 9
    # :1 = 147456 / 147456
    # :2 = 184320 / 36864
    # :3 = 193536 / 9216
    # :4 = 195840 / 2304
    # :5 = 196416 / 576
