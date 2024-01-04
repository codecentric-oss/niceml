"""Module for test for the configuration"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

from dagster import Config as DagsterConfig
from pydantic import Field, BaseModel

from niceml.config.config import get_class_path, InitConfig, Configurable


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
            seats=None
    ):
        super().__init__(
            color=color, engine=engine, wheels=wheels, lights=lights, horn=horn
        )
        self.speed = speed
        self.seats = seats


class Driver(DagsterConfig):
    name: str


class TestCarConfig(DagsterConfig):
    car: InitConfig = InitConfig.create_config_field(
        target_class=Car,
    )
    distance: float = Field(default=100)
    driver: Driver


def test_initialize_from_dict():
    wheel_map_dict = dict(
        lf_wheel=dict(_target_=get_class_path(Wheel)),
        rf_wheel=dict(_target_=get_class_path(Wheel), radius=20),
        lr_wheel=dict(_target_=get_class_path(Wheel)),
        rr_wheel=dict(_target_=get_class_path(Wheel)),
    )
    engine_dict = dict(_target_=get_class_path(Engine), power=100)
    car_config = InitConfig.create(
        Car, color="red", engine=engine_dict, wheels=wheel_map_dict, lights=[
            dict(_target_=get_class_path(Light), size=5,
                 position=dict(_target_=LightPosition, value="front left")),
            dict(_target_=get_class_path(Light), size=7,
                 position=dict(_target_=LightPosition, value="front right")),
        ]
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
                Light.create_config(size=5, position=LightPosition.FRONT_LEFT),
                Light.create_config(size=7, position=LightPosition.FRONT_RIGHT),
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
                Light.create_config(size=5, position=LightPosition.FRONT_LEFT),
                Light.create_config(size=7, position=LightPosition.FRONT_RIGHT),
            ],
            horn=0.1,
            seats=1
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
                Light.create_config(size=5, position=LightPosition.FRONT_LEFT),
                Light.create_config(size=7, position=LightPosition.FRONT_RIGHT),
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
    assert car.engine.power == 100
    assert car.color == "red"
    assert not car.engine.running
