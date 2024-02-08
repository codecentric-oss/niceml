from keras.optimizers import Adam as KerasAdam

from niceml.mlcomponents.optimizers import Optimizer


class Adam(KerasAdam, Optimizer):
    pass
