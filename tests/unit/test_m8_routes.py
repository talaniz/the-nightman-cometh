"""Longer authored approaches and compatibility with pre-polish saves."""
import json
import pytest
from game.levels.act1 import Act1
from game.levels.act2 import Act2
from game.levels.act3 import Act3
from game.session import Session
from test_progress import Memory

@pytest.mark.parametrize('level,old,expected',[(Act1,3350,4250),(Act2,2800,3550),(Act3,3000,3850)])
def test_longer_approach_preserves_existing_checkpoint_save(level,old,expected):
    assert level.flag_positions['preboss']==expected
    store=Memory();store.raw=json.dumps(dict(v=2,stage=level.act,checkpoint=old,flags=['mid','preboss'],complete=False,settings=dict(music=.3,effects=.6)))
    s=Session(store)
    assert s.world.act==level.act and s.world.checkpoint==expected
    assert s.world.player.x==expected and s.world.flags=={'mid','preboss'}
    assert s.progress.settings==dict(music=.3,effects=.6)


def test_preboss_flag_approach_has_a_safe_moment_to_accept_input():
    from game.fixtures import apply
    s=Session(Memory());apply(s,{'name':'act3-preboss'})
    s.update(1/60,{})
    assert s.screen=='training' and s.world.player.hearts==1
