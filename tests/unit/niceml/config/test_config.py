"""Module for test for the configuration"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple, Union

import numpy as np
import pytest
from dagster import Config
from keras.optimizers import Adam
from pydantic import Field, BaseModel
from pydantic.fields import FieldInfo

from niceml.config.config import (
    get_class_path,
    InitConfig,
    Configurable,
    parse_value_type,
    MapInitConfig,
)
from niceml.dlframeworks.keras.callbacks.nancheckcallback import LossNanCheckCallback


# Test classes for config creation and instantiation


class Engine(Configurable):
    def __init__(self, power: int = 50):
        self.power = power
        self.running = False

    def __eq__(self, other):
        return self.power == other.power


class Wheel(Configurable):
    def __init__(self, radius: int = 10):
        self.radius = radius

    def __eq__(self, other):
        return self.radius == other.radius


class LightPosition(str, Enum):
    FRONT_LEFT: str = "front left"
    FRONT_RIGHT: str = "front right"


@dataclass
class Light(Configurable):
    size: float
    position: LightPosition


class Car(Configurable):
    def __init__(
        self,
        color: str,
        engine: Engine,
        wheels: Dict[str, Wheel],
        lights: List[Light],
        horn: Optional[float] = None,
    ):
        self.lights = lights
        self.horn = horn
        self.color = color
        self.engine = engine
        self.wheels = wheels

    def __eq__(self, other):
        return (
            self.color == other.color
            and self.engine == other.engine
            and self.wheels == other.wheels
        )


class FastCar(Car):
    def __init__(
        self,
        color: str,
        engine: Engine,
        wheels: Dict[str, Wheel],
        lights: List[Light],
        speed=100,
        horn: Optional[float] = None,
        seats=None,
    ):
        super().__init__(
            color=color, engine=engine, wheels=wheels, lights=lights, horn=horn
        )
        self.speed = speed
        self.seats = seats


class Driver(Config):
    name: str


class TestCarConfig(Config):
    car: InitConfig = InitConfig.create_config_field(
        target_class=Car,
    )
    distance: float = Field(default=100)
    driver: Driver


class DictEngineConfig(Config):
    engines: Dict[str, InitConfig] = InitConfig.create_dict_config_field(
        target_class=Engine
    )


def test_initialize_from_dict():
    wheel_map_dict = dict(
        lf_wheel=dict(_target_=get_class_path(Wheel)),
        rf_wheel=dict(_target_=get_class_path(Wheel), radius=20),
        lr_wheel=dict(_target_=get_class_path(Wheel)),
        rr_wheel=dict(_target_=get_class_path(Wheel)),
    )
    engine_dict = dict(_target_=get_class_path(Engine), power=100)
    car_config = InitConfig.create(
        Car,
        color="red",
        engine=engine_dict,
        wheels=wheel_map_dict,
        lights=[
            dict(
                _target_=get_class_path(Light),
                size=5,
                position=dict(_target_=LightPosition, value="front left"),
            ),
            dict(
                _target_=get_class_path(Light),
                size=7,
                position=dict(_target_=LightPosition, value="front right"),
            ),
        ],
    )
    car = car_config.instantiate()
    assert isinstance(car.engine, Engine)
    assert isinstance(car.wheels["lr_wheel"], Wheel)
    assert isinstance(car.lights[0].position, LightPosition)
    assert isinstance(car.lights[0], Light)
    assert car.color == "red"
    assert car.engine.power == 100
    assert len(car.lights) == 2
    assert car.lights[0].size == 5
    assert car.lights[0].position.value == "front left"
    assert car.wheels["lf_wheel"].radius == 10
    assert car.wheels["rf_wheel"].radius == 20


def test_create_class_config():
    config_car = TestCarConfig(
        car=Car.create_config(
            color="red",
            engine=Engine.create_config(power=100),
            wheels=dict(left=Wheel.create_config()),
            lights=[
                Light.create_config(
                    size=5,
                    position=InitConfig.create(LightPosition, value="front left"),
                ),
                Light.create_config(
                    size=7,
                    position=InitConfig.create(LightPosition, value="front left"),
                ),
            ],
        ),
        distance=200,
        driver=Driver(name="Adam"),
    )

    config_fast_car = TestCarConfig(
        car=FastCar.create_config(
            color="red",
            engine=Engine.create_config(power=100),
            wheels=dict(left=Wheel.create_config()),
            speed=200,
            lights=[
                Light.create_config(
                    size=5,
                    position=InitConfig.create(LightPosition, value="front left"),
                ),
                Light.create_config(
                    size=7,
                    position=InitConfig.create(LightPosition, value="front right"),
                ),
            ],
            horn=0.1,
            seats=1,
        ),
        distance=200,
        driver=Driver(name="John"),
    )

    config_default_fast_car = TestCarConfig(
        car=FastCar.create_config(
            color="red",
            engine=Engine.create_config(power=100),
            wheels=dict(left=Wheel.create_config()),
            lights=[
                Light.create_config(
                    size=5,
                    position=InitConfig.create(LightPosition, value="front left"),
                ),
                Light.create_config(
                    size=7,
                    position=InitConfig.create(LightPosition, value="front right"),
                ),
            ],
        ),
        distance=200,
        driver=Driver(name="Eve"),
    )

    for config in [config_car, config_fast_car, config_default_fast_car]:
        assert isinstance(config.car, InitConfig)
        assert isinstance(config.distance, float)
        assert isinstance(config.driver, BaseModel)

        car = config.car.instantiate()
        assert isinstance(car.engine, Engine)
        assert isinstance(car.wheels["left"], Wheel)
        assert isinstance(car.lights[0], Light)
        assert isinstance(car.lights[0].position, LightPosition)
        assert car.color == "red"


def test_create_class_config_with_init_config():
    config = TestCarConfig(
        car=InitConfig.create(
            Car,
            color="red",
            engine=InitConfig.create(Engine, power=100),
            wheels=dict(left=InitConfig.create(Wheel)),
            horn=100,
            lights=[
                InitConfig.create(
                    Light,
                    position=InitConfig.create(LightPosition, value="front left"),
                    size=10,
                ),
                InitConfig.create(
                    Light,
                    position=InitConfig.create(LightPosition, value="front right"),
                    size=5,
                ),
            ],
        ),
        distance=200,
        driver=Driver(name="Adam"),
    )

    assert isinstance(config.car, InitConfig)
    assert isinstance(config.distance, float)
    assert isinstance(config.driver, BaseModel)
    assert not hasattr(config.car.engine, "running")

    car = config.car.instantiate()
    assert isinstance(car.engine, Engine)
    assert isinstance(car.wheels["left"], Wheel)
    assert isinstance(car.lights[0], Light)
    assert isinstance(car.lights[0].position, LightPosition)
    assert car.engine.power == 100
    assert car.color == "red"
    assert not car.engine.running


@pytest.mark.parametrize(
    "input_value_type,result",
    [
        (int, int),
        (str, str),
        (float, float),
        (bool, bool),
        (Enum, InitConfig),
        (dict, dict),
        (Dict[str, str], Dict[str, str]),
        (Dict[str, int], Dict[str, int]),
        (Dict[str, Dict[str, str]], Dict[str, Dict[str, str]]),
        (Dict[str, Dict[str, int]], Dict[str, Dict[str, int]]),
        #        (Dict[str, Engine], MapInitConfig),
        (Tuple[str], Tuple[str]),
        (Tuple[str, Engine], Tuple[str, InitConfig]),
        (Tuple[str, Car], Tuple[str, InitConfig]),
        (List[Union[str, int, bool]], List[Union[str, int, bool]]),
        (Optional[str], Optional[str]),
        (Union[str, int, bool], Union[str, int, bool]),
        (Union[str, int, Dict[str, str]], Union[str, int, Dict[str, str]]),
        (List, List),
        (Optional[List[Engine]], Optional[List[InitConfig]]),
        (Optional[Union[str, str]], Optional[Union[str, str]]),
        (Optional[Union[str, Dict[str, int]]], Optional[Union[str, Dict[str, int]]]),
        (
            Optional[Union[str, Dict[str, Engine]]],
            Optional[Union[str, Dict[str, InitConfig]]],
        ),
    ],
)
def test_parse_value_type(input_value_type, result):
    output_value_type = parse_value_type(input_value_type)
    assert output_value_type == result


@pytest.mark.parametrize(
    "implementation_reference,kwargs",
    [
        (LossNanCheckCallback, {}),
        (LossNanCheckCallback, {"check_logs": ["test_loss"]}),
        (Adam, {"learning_rate": 1e5}),
    ],
)
def test_foreign_implementation_config_creation(implementation_reference, kwargs):
    config = InitConfig.create(implementation_reference, **kwargs)
    config.instantiate()
    config_attributes = config.dict(by_alias=True)
    kwargs.update({"_target_": "test_target "})
    for kwarg in kwargs:
        assert kwarg in config_attributes.keys()


def test_create_dict_config_field():
    config_dict = InitConfig.create_dict_config_field(target_class=Engine)
    assert isinstance(config_dict, dict)
    for config_entry in config_dict.values():
        assert isinstance(config_entry, FieldInfo)


@pytest.mark.parametrize(
    "config_input,expected_result",
    [
        (
            {
                "a": Engine.create_config(power=100),
                "b": Engine.create_config(power=200),
            },
            {
                "a": Engine(power=100),
                "b": Engine(power=200),
            },
        ),
        (
            {
                "a": Engine.create_config(power=100),
                "b": Engine.create_config(power=200),
                "c": Engine.create_config(power=300),
            },
            {
                "a": Engine(power=100),
                "b": Engine(power=200),
                "c": Engine(power=300),
            },
        ),
    ],
)
def test_initialize_dict_config_entry(
    config_input: Dict[str, InitConfig], expected_result: Dict[str, Engine]
):
    config = DictEngineConfig(engines=config_input)

    result = {
        engine_key: engine_conf.instantiate()
        for engine_key, engine_conf in config.engines.items()
    }

    assert result == expected_result
