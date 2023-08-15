"""Module to get all exp schemas"""
from niceml.experiments.schemas.baseexpschema import BaseExperimentSchema
from niceml.experiments.schemas.objdetexpschema import ObjDetExpSchema
from niceml.experiments.schemas.sampleexpschemas import NumRegExpSchema


def get_all_schemas():
    """Returns a list of all exp schemas"""
    return [BaseExperimentSchema, NumRegExpSchema, ObjDetExpSchema]
