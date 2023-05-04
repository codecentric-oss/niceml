from niceml.config import envconfig as envc


def test_produce_exp_info(exp_info_data: dict):
    assert isinstance(exp_info_data, dict)
    assert envc.EXP_NAME_KEY in exp_info_data
    assert envc.ENVIRONMENT_KEY in exp_info_data
    assert envc.DESCRIPTION_KEY in exp_info_data
    assert envc.EXP_PREFIX_KEY in exp_info_data
    assert envc.SHORT_ID_KEY in exp_info_data
    assert envc.RUN_ID_KEY in exp_info_data
