from os.path import dirname, join

import pytest
from hydra.utils import instantiate
from omegaconf.dictconfig import DictConfig

from niceml.scripts.hydraconfreader import load_hydra_conf


@pytest.fixture(
    params=[
        "configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml",
        "configs/jobs/job_train/job_train_cls/job_train_cls_multitarget.yaml",
        "configs/jobs/job_train/job_train_cls/job_train_cls_softmax.yaml",
        "configs/jobs/job_train/job_train_objdet/job_train_objdet_number.yaml",
        "configs/jobs/job_train/job_train_reg/job_train_reg_number.yaml",
        "configs/jobs/job_train/job_train_semseg/job_train_semseg_number.yaml",
        # Eval Configs
        "configs/jobs/job_eval/job_eval_objdet/job_eval_objdet_number.yaml",
        "configs/jobs/job_eval/job_eval_reg/job_eval_reg_number.yaml",
    ]
)
def yaml_path(request):
    cur_dir = dirname(__file__)
    project_dir = dirname(dirname(cur_dir))
    return join(project_dir, request.param)


def test_load_confs(yaml_path: str):
    load_hydra_conf(yaml_path)


def test_instantiate_confs(yaml_path: str):
    conf = load_hydra_conf(yaml_path)
    res = instantiate(conf)
    assert isinstance(res, DictConfig)
