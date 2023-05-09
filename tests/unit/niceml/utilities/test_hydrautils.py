import pytest

from os.path import dirname, join
from niceml.utilities.hydrautils import build_import_graph, parse_defaults_content, nx_to_mermaid


@pytest.fixture(
    params=[
        "configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml",
        "configs/jobs/job_train/job_train_cls/job_train_cls_multitarget.yaml",
        "configs/jobs/job_train/job_train_cls/job_train_cls_softmax.yaml",
        "configs/jobs/job_train/job_train_objdet/job_train_objdet_number.yaml",
        "configs/jobs/job_train/job_train_reg/job_train_reg_sinus.yaml",
        "configs/jobs/job_train/job_train_semseg/job_train_semseg_number.yaml",
        # Eval Configs
        "configs/jobs/job_eval/job_eval_objdet/job_eval_objdet_number.yaml",
        "configs/jobs/job_eval/job_eval_reg/job_eval_reg_sinus.yaml",
    ]
)
def yaml_path(request):
    cur_dir = dirname(__file__)
    project_dir = dirname(dirname(dirname(dirname(cur_dir))))
    return join(project_dir, request.param)


@pytest.fixture()
def search_paths():
    cur_dir = dirname(__file__)
    project_dir = dirname(dirname(dirname(dirname(cur_dir))))
    return [join(project_dir, "configs")]


def test_build_import_graph_and_mermaid_conversion(yaml_path: str, search_paths: list):
    import_graph = build_import_graph(yaml_path, search_paths=search_paths)
    assert import_graph.number_of_nodes() > 0
    assert import_graph.number_of_edges() > 0
    mermaid_graph = nx_to_mermaid(import_graph)
    assert mermaid_graph.startswith("graph LR;")
    assert mermaid_graph.count(" --> ") == import_graph.number_of_edges()
    assert mermaid_graph.count(";\n") == import_graph.number_of_edges() + 1
    assert mermaid_graph.endswith(";\n")


@pytest.mark.parametrize(
    "input, target",
    [
        ({"ops/experiment@ops.experiment.config": "op_experiment_default.yaml"}, "ops/experiment/op_experiment_default.yaml"),
        ("ops/experiment/op_experiment_default.yaml@ops.experiment.config", "ops/experiment/op_experiment_default.yaml"),
        ("_self_", "_self_"),
    ]
)
def test_parse_defaults_content(input, target):
    assert parse_defaults_content(input) == target
