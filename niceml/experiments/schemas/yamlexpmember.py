"""Module for yaml exp members"""
from typing import Optional, Union

import schema

from niceml.config import envconfig as envc
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.schemas.expmember import ExpMember


class YamlMember(ExpMember):
    """yaml-file which is member of the experiment"""

    def __init__(
        self,
        path: str,
        required: bool,
        description: str,
        yaml_schema: Optional[schema.Schema] = None,
    ):
        super().__init__(
            path=path,
            required=required,
            description=description,
            member_type="yaml-file",
        )
        self.yaml_schema: Optional[schema.Schema] = yaml_schema

    def validate(self, exp_data: ExperimentData) -> bool:
        result = super().validate(exp_data)
        val_data = exp_data.get_loaded_yaml(self.path)
        val_result = self._validate_schema(val_data)
        return result and val_result

    def _validate_schema(self, val_data: Union[dict, list]) -> bool:
        if self.yaml_schema is None:
            return True
        try:
            self.yaml_schema.validate(val_data)
        except schema.SchemaError:
            return False
        return True


class ExpInfoMember(YamlMember):
    """Specific member of the experiment containing the experiment info"""

    def __init__(self):
        exp_schema = schema.Schema(
            {
                envc.EXP_NAME_KEY: str,
                envc.ENVIRONMENT_KEY: dict,
                envc.DESCRIPTION_KEY: str,
                envc.EXP_PREFIX_KEY: str,
                envc.SHORT_ID_KEY: lambda val: isinstance(val, str) and len(val) == 4,
                envc.RUN_ID_KEY: lambda val: isinstance(val, str) and len(val) == 24,
                envc.EXP_TYPE_KEY: str,
                envc.EXP_DIR_KEY: str,
            }
        )
        super().__init__(
            path=ExperimentFilenames.EXP_INFO,
            required=True,
            description="This file contains experiment info like id, environment and runtime",
            yaml_schema=exp_schema,
        )
