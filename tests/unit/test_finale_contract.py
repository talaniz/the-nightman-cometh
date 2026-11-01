"""Exact ending order and state transitions, without requiring an illustration."""
from game.session import Session
from game.levels.act3 import Act3
from test_progress import Memory

LINES=["I'm not going to marry you, Charlie.","Well, see you tomorrow.",
       'I told you no one writes a musical for no reason!',"Dee, I'm right here right now","but I'm about to go here!"]

def finish():
    s=Session(Memory());s.world=Act3();s.world.complete=True;s.enter_screen('training');s.update(0,{})
    return s

def test_finale_exact_sequence_and_distinct_waitress():
    s=finish()
    assert [still.text for still in s.sequence][-5:]==LINES
    assert s.sequence[-5].speaker=='WAITRESS' and s.sequence[-3].speaker=='DEE'
    assert s.sequence[-5].music=='credits' # silence beneath final spoken joke

def test_play_and_skip_end_at_ending_then_silent_credits():
    for skip in (False,True):
        s=finish()
        if skip:s.next_dialogue(skip=True)
        else:
            for _ in s.sequence:s.next_dialogue()
        assert s.screen=='ending' and s.world.act=='act3'
        assert s.music_scene()=='ending'
        s.activate();assert s.screen=='credits' and s.music_scene()=='credits'
        assert 'Replay ending' in s.menu() and 'Title' in s.menu()

def test_completed_save_replay_is_non_mutating_and_reload_safe():
    s=finish();stored=s.progress.storage.raw;s=Session(s.progress.storage)
    s.selection=s.menu().index('Continue Act 3');s.activate()
    assert s.screen=='credits'
    s.selection=s.menu().index('Replay ending');s.activate()
    assert s.screen=='dialogue'
    s.next_dialogue(skip=True);assert s.screen=='ending'
    s.activate();assert s.screen=='credits' and s.progress.storage.raw==stored
