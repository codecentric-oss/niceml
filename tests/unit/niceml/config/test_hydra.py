"""Module for test for the configuration"""
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, TypedDict

import pytest
from pydantic import Field, BaseModel

from niceml.config.config import Config, get_class_path, InitConfig, MapInitConfig
from niceml.mlcomponents.resultanalyzers.dataframes.clsmetric import ClsMetric
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import (
    DataframeAnalyzer,
    DfMetric,
)

from dagster import Config as DagsterConfig


class InitClsMetric(InitConfig):
    target: str = InitConfig.create_target_field(ClsMetric)
    function: str = "confusion_matrix"
    source_col: str = "class_idx"
    target_cols_prefix: str = "pred_"


dfanalyzer_class = (
    "niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer.DataframeAnalyzer"
)
clsmetrics_class = "niceml.mlcomponents.resultanalyzers.dataframes.clsmetric.ClsMetric"


class InitResultAnalyzer(InitConfig):
    target: str = InitConfig.create_target_field(DataframeAnalyzer)
    metrics: List[DfMetric] = [InitClsMetric()]


def test_init_simple():
    init = InitClsMetric()
    cur_dict = init.dict(by_alias=True)
    assert cur_dict == {
        "_target_": clsmetrics_class,
        "function": "confusion_matrix",
        "source_col": "class_idx",
        "target_cols_prefix": "pred_",
    }
    assert init.target == clsmetrics_class
    assert init.function == "confusion_matrix"
    assert init.source_col == "class_idx"
    assert init.target_cols_prefix == "pred_"
    target_obj = init.instantiate()
    assert type(target_obj) == ClsMetric


def test_class_path():
    assert get_class_path(ClsMetric) == clsmetrics_class


def test_init_nested():
    init = InitResultAnalyzer()
    cur_dict = init.dict(by_alias=True)
    assert cur_dict == {
        "_target_": "niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer.DataframeAnalyzer",
        "metrics": [
            {
                "_target_": "niceml.mlcomponents.resultanalyzers.dataframes.clsmetric.ClsMetric",
                "function": "confusion_matrix",
                "source_col": "class_idx",
                "target_cols_prefix": "pred_",
            }
        ],
    }
    assert init.target == dfanalyzer_class
    assert len(init.metrics) == 1
    assert type(init.metrics[0]) == InitClsMetric
    target_obj = init.instantiate()
    assert type(target_obj) == DataframeAnalyzer
    assert type(target_obj.df_metrics[0]) == ClsMetric
    assert target_obj.df_metrics[0].source_col == "class_idx"
    assert target_obj.df_metrics[0].target_cols_prefix == "pred_"


class Configurable(ABC):
    @classmethod
    def create_config(cls, **kwargs) -> InitConfig:
        return InitConfig.create_conf(cls, **kwargs)


class Engine(Configurable):
    def __init__(self, power: int = 100):
        self.power = power + 10

    def __eq__(self, other):
        return self.power == other.power


class ConfigurableMeta(type):
    def __new__(cls, name, bases, attrs):
        instance = super().__new__(cls, name, bases, attrs)
        instance.config = InitConfig.create_conf(cls)
        return instance


class Wheel(metaclass=ConfigurableMeta):
    def __init__(self, radius: int = 10):
        self.radius = radius

    def __eq__(self, other):
        return self.radius == other.radius


class LightPosition(str, Enum):
    FRONT_LEFT: str = "front left"
    FRONT_RIGHT: str = "front right"


@dataclass
class Light:
    size: float
    position: LightPosition


class Car:
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
        speed: float = 100,
        horn: Optional[float] = None,
    ):
        super().__init__(
            color=color, engine=engine, wheels=wheels, lights=lights, horn=horn
        )
        self.speed = speed


class Driver(DagsterConfig):
    name: str


class TestCarConfig(Config):
    car: InitConfig = InitConfig.create_config_field(
        target_class=Car,
    )
    distance: float = Field(default=100)
    driver: Driver


def test_init_complex_create():
    wheel_map_dict = dict(
        lf_wheel=dict(_target_=get_class_path(Wheel)),
        rf_wheel=dict(_target_=get_class_path(Wheel), radius=20),
        lr_wheel=dict(_target_=get_class_path(Wheel)),
        rr_wheel=dict(_target_=get_class_path(Wheel)),
    )
    engine_dict = dict(_target_=get_class_path(Engine), power=100)
    car_config = InitConfig.create(
        Car, color="red", engine=engine_dict, wheels=wheel_map_dict
    )
    car_config.instantiate()


def test_create_class_config():
    config_car = TestCarConfig.create(
        car=Car(
            color="red",
            engine=Engine(power=100),
            wheels=dict(left=Wheel()),
            lights=[
                Light(5, LightPosition.FRONT_LEFT),
                Light(7, LightPosition.FRONT_RIGHT),
            ],
        ),
        distance=200,
        driver=Driver(name="Horst"),
    )

    config_fast_car = TestCarConfig.create(
        car=FastCar(
            color="red",
            engine=Engine(power=100),
            wheels=dict(left=Wheel()),
            speed=200,
            lights=[
                Light(1, LightPosition.FRONT_LEFT),
                Light(1, LightPosition.FRONT_RIGHT),
            ],
        ),
        distance=200,
        driver=Driver(name="Horst"),
    )

    for config in [config_car, config_fast_car]:
        assert isinstance(config.car, InitConfig)
        assert isinstance(config.distance, float)
        assert isinstance(config.driver, BaseModel)

        car = config.car.instantiate()
        assert isinstance(car.engine, Engine)
        assert isinstance(car.wheels["left"], Wheel)
        assert isinstance(car.lights[0].position, LightPosition)
        assert car.color == "red"


def test_create_class_config_with_init_config():
    Car.Conf(
        color="red",
        wheel=dict(left=Wheel.Conf()),
        engine=InitConfig.create_conf(Engine, power=100),
    )

    config = TestCarConfig(
        car=InitConfig.create_conf(
            Car,
            color="red",
            engine=InitConfig.create_conf(Engine, power=100),
            wheels=dict(left=InitConfig.create_conf(Wheel)),
            horn=100,
            lights=[
                InitConfig.create_conf(
                    Light,
                    position=InitConfig.create_conf(LightPosition, value="front left"),
                    size=10,
                ),
                InitConfig.create_conf(
                    Light,
                    position=InitConfig.create_conf(LightPosition, value="front right"),
                    size=5,
                ),
            ],
        ),
        distance=200,
        driver=Driver(name="Horst"),
    )

    assert isinstance(config.car, InitConfig)
    assert isinstance(config.distance, float)
    assert isinstance(config.driver, BaseModel)

    car = config.car.instantiate()
    assert isinstance(car.engine, Engine)
    assert isinstance(car.wheels["left"], Wheel)
    assert car.engine.power == 110
    assert car.color == "red"


def test_dinge():
    engine_conf = Engine(power=100).create_config()
    wheel_conf = Wheel(radius=100).config
    l = 1
