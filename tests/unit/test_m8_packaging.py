"""Missing new production artwork must fail before browser packaging."""
import pytest
import tools.build_web as build

@pytest.mark.parametrize('relative',[
 'sprites/dumpster.png','sprites/cricket-run.png','sprites/dennis-transformation.png',
 'scenes/act3/transformation.png','ui/shadynasty-sign.png','ui/title-m8.png',
])
def test_new_required_art_is_validated_before_build(relative,monkeypatch):
    files=build.art_files();missing=build.ROOT/'assets'/relative
    monkeypatch.setattr(build,'art_files',lambda:[p for p in files if p!=missing])
    with pytest.raises(ValueError,match='Missing required art'):
        build.validate_art()
