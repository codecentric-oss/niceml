"""module for writing config files"""
from os.path import join

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames


def write_op_config(op_conf: dict, exp_context: ExperimentContext, op_name: str):
    """Writes a dict as yamls. With one file per key"""
    for key, values in op_conf.items():
        outfile = join(ExperimentFilenames.CONFIGS_FOLDER, op_name, f"{key}.yaml")
        exp_context.write_yaml(values, outfile)
