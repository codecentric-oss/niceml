from math import isclose

from niceml.dlframeworks.keras.optimizers.schedules.cycliclrschedule import (
    CyclicLRSchedule,
)


def test_min_max_lr():
    """Test min and max lr"""
    max_lr = 0.1
    min_lr = 0.01
    cycle_size = 100
    cyclic_lr = CyclicLRSchedule(max_lr, cycle_size, min_lr)
    assert cyclic_lr.max_lr == max_lr
    assert cyclic_lr.min_lr == min_lr
    assert cyclic_lr.cycle_size == cycle_size


def test_cycle_iteration():
    """Iterates over one cycle and checks min and max lr"""
    max_lr = 0.1
    min_lr = 0.01
    cycle_size = 100
    cyclic_lr = CyclicLRSchedule(max_lr, cycle_size, min_lr)
    measured_max_lr = 0
    measured_min_lr = 10000
    first_lr = cyclic_lr(0)
    assert isclose(float(first_lr), min_lr, abs_tol=1e-3)
    for cur_step in range(cycle_size):
        learning_rate = cyclic_lr(cur_step)
        measured_max_lr = max(measured_max_lr, learning_rate)
        measured_min_lr = min(measured_min_lr, learning_rate)

    assert isclose(float(measured_max_lr), max_lr, abs_tol=1e-3)
    assert isclose(float(measured_min_lr), min_lr, abs_tol=1e-3)
