from niceml.experiments.schemas.sampleexpschemas import SinRegExpSchema
from niceml.mkdocs.schemadocgeneration import expschema_to_markdown


def test_expschema_to_markdown():
    result = expschema_to_markdown(SinRegExpSchema, col_widths=[50, 80])
    assert len(result) > 1000
