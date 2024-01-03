"""Module for test for the configuration"""

from typing import List, Dict

from pydantic import Field, BaseModel

from niceml.config.config import Config, get_class_path, InitConfig, MapInitConfig
from niceml.mlcomponents.resultanalyzers.dataframes.clsmetric import ClsMetric
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import (
    DataframeAnalyzer,
    DfMetric,
)


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


class Engine:
    def __init__(self, power: int):
        self.power = power

    def __eq__(self, other):
        return self.power == other.power


class Wheel:
    def __init__(self, radius: int = 10):
        self.radius = radius

    def __eq__(self, other):
        return self.radius == other.radius


class Car:
    def __init__(self, color: str, engine: Engine, wheels: Dict[str, Wheel]):
        self.color = color
        self.engine = engine
        self.wheels = wheels

    def __eq__(self, other):
        return (
            self.color == other.color
            and self.engine == other.engine
            and self.wheels == other.wheels
        )


class Driver(BaseModel):
    name: str


class InitEngine(InitConfig):
    target: str = InitConfig.create_target_field(Engine)
    power: int = 100


class InitWheel(InitConfig):
    target: str = InitConfig.create_target_field(Wheel)
    radius: int = 10


class InitWheelMap(MapInitConfig):
    lf_wheel: InitWheel = InitWheel()
    rf_wheel: InitWheel = InitWheel(radius=20)
    lr_wheel: InitWheel = InitWheel()
    rr_wheel: InitWheel = InitWheel()


class InitCar(InitConfig):
    target: str = InitConfig.create_target_field(Car)
    color: str = "red"
    engine: InitEngine = InitEngine()
    wheels: InitWheelMap = InitWheelMap()


def test_init_complex():
    car_config = InitCar()
    car_obj = car_config.instantiate()
    assert type(car_obj) == Car
    assert car_obj.color == "red"
    assert car_obj.engine.power == 100
    assert car_obj.wheels["lf_wheel"].radius == 10
    assert len(car_obj.wheels) == 4


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


def test_config():
    class TestConfig(Config):
        car: InitConfig = InitConfig.create_config_field(target_class=Car)
        distance: float = Field(default=100)
        driver: Driver

    config = TestConfig.create(
        car=Car(color="red", engine=Engine(power=100), wheels=dict(left=Wheel())),
        distance=200,
        driver=Driver(name="Horst"),
    )
    assert isinstance(config.car, InitConfig)
    assert isinstance(config.distance, float)
    assert isinstance(config.driver, BaseModel)

    car = config.car.instantiate()
    assert isinstance(car.engine, Engine)
    assert isinstance(car.wheels["left"], Wheel)
    assert car.color == "red"
