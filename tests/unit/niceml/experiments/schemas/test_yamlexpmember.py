from niceml.experiments.schemas.yamlexpmember import ExpInfoMember


def test_exp_info_member(exp_info_data: dict):
    exp_info_member = ExpInfoMember()
    assert exp_info_member._validate_schema(exp_info_data)
