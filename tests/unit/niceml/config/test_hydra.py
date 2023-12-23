"""Module for test for the configuration"""

from typing import List, Dict

from niceml.config.hydra import InitConfig, MapInitConfig, get_class_path
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


def configure(cls):
    """
    Configures a class with an initialization configuration method.

    This decorator enhances a class by adding a `_conf` method, which generates
    an initialization configuration for an instance of the class. The
    initialization configuration includes the values of attributes, recursively
    parsing nested structures such as lists, tuples, and dictionaries.

    Args:
        cls: The class to be configured.

    Returns:
        The configured class with the added `_conf` method.

    Example:
        @configure
        class MyClass:
            def __init__(self, name, age, data):
                self.name = name
                self.age = age
                self.data = data

        # Usage
        obj = MyClass(name="John", age=30, data={"key": [1, 2, {"nested": True}]})
        config = obj._conf()  # Generates an initialization configuration
    """

    def create_init_config(instance) -> InitConfig:
        def parse_value(value):
            if isinstance(value, (int, str, float, bool)):
                return value
            elif isinstance(value, (list, tuple)):
                return [parse_value(item) for item in value]
            elif isinstance(value, dict):
                return {key: parse_value(value) for key, value in value.items()}
            else:
                return create_init_config(value)

        values = vars(instance)
        parsed_values = {key: parse_value(value) for key, value in values.items()}
        return InitConfig.create_conf(target_class=type(instance), **parsed_values)()

    setattr(cls, "_conf", create_init_config)
    return cls


@configure
class Engine:
    def __init__(self, power: int):
        self.power = power

    def __eq__(self, other):
        return self.power == other.power


@configure
class Wheel:
    def __init__(self, radius: int = 10):
        self.radius = radius

    def __eq__(self, other):
        return self.radius == other.radius


@configure
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


def test_conf_class_method():
    car = Car(color="red", engine=Engine(power=100), wheels=dict(left=Wheel()))
    config = car._conf()
    car2 = config.instantiate()
    assert car == car2
