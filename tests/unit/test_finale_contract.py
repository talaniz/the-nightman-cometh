"""Exact ending order and state transitions, without requiring an illustration."""
from game.session import Session
from game.levels.act3 import Act3
from test_progress import Memory

LINES=['You said if I came to the show, you’d leave me alone. So, no….',
       '…', 'So…see you tomorrow…?', 'I told you no one writes a musical for no reason!',
       'Dee, I’m right here right now…', '…but I’m about to go here!']

def finish():
    s=Session(Memory());s.world=Act3();s.world.complete=True;s.enter_screen('training');s.update(0,{})
    return s

def test_finale_exact_sequence_and_distinct_waitress():
    s=finish()
    assert [still.text for still in s.sequence][-6:]==LINES
    assert s.sequence[-6].speaker=='WAITRESS' and s.sequence[-3].speaker=='DEE'
    assert s.sequence[-6].music=='dialogue-silence' # silence beneath final spoken joke

def test_play_and_skip_end_directly_at_credits():
    for skip in (False,True):
        s=finish()
        if skip:s.next_dialogue(skip=True)
        else:
            while s.screen=='dialogue':
                if s.sequence[s.dialogue].effect:
                    for _ in range(46):s.update(.1,{})
                else:s.next_dialogue()
        assert s.screen=='credits' and s.world.act=='act3'
        assert s.music_scene()=='credits'
        assert s.music_scene()=='credits'
        assert 'Replay ending' in s.menu() and 'Title' in s.menu()

def test_completed_save_replay_is_non_mutating_and_reload_safe():
    s=finish();stored=s.progress.storage.raw;s=Session(s.progress.storage)
    s.selection=s.menu().index('Continue Act 3');s.activate()
    assert s.screen=='credits'
    s.selection=s.menu().index('Replay ending');s.activate()
    assert s.screen=='dialogue'
    s.next_dialogue(skip=True);assert s.screen=='credits'
    assert s.screen=='credits' and s.progress.storage.raw==stored
