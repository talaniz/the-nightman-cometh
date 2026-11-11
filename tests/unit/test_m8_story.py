"""Approved M8 dialogue and final credits route, through the real session."""
from game.scenes.opening import FRANK, NIGHTMAN
from game.scenes.finale import FINALE
from game.session import Session
from test_progress import Memory


def test_rescue_and_abduction_reactions():
    assert FRANK[0].text == 'Don’t you ever leave me with that looney—I mean, my hero…I guess…'
    assert NIGHTMAN[1].text == 'I hate this storyyyy!!!!'


def test_transformation_precedes_manually_advanced_proposal():
    texts = [still.text for still in FINALE]
    assert texts[0] == 'I was a boy, now I am…'
    assert 'The Dayman!' in texts
    assert texts.index('The Dayman!') < texts.index('ah ah ah ah ah ah ah ah')
    assert 'Won’t you come on stage and join me?' not in texts  # preserve supplied ASCII apostrophe
    assert "Won't you come on stage and join me?" in texts
    assert texts[-6:] == [
        'You said if I came to the show, you’d leave me alone. So, no….',
        'Well, technically I didn’t sign anything', 'So, I guess I’ll see you tomorrow?…',
        'I told you no one writes a musical for no reason!',
        'Dee, I’m right here right now…',
        '…but I’m about to go here!',
    ]


def test_final_joke_goes_directly_to_credits_without_extra_end_screen():
    session = Session(Memory())
    session.sequence = FINALE
    session.dialogue = len(FINALE)-1
    session.enter_screen('dialogue')
    session.next_dialogue()
    assert session.screen == 'credits'
    assert session.music_scene() == 'credits'


def test_transformation_runs_automatically_with_exactly_three_effect_cues():
    session = Session(Memory())
    session.sequence = FINALE
    session.dialogue = 0
    session.enter_screen('dialogue')
    session.next_dialogue()
    assert session.sequence[session.dialogue].effect == 'dayman'
    # Pressing next during the effect must not skip its reveal or jump into lyrics.
    session.next_dialogue()
    assert session.sequence[session.dialogue].effect == 'dayman'
    for _ in range(46):
        session.update(.1, {})
    assert session.sequence[session.dialogue].text == 'The Dayman!'
    assert session.story_events == ['beam', 'meal', 'beam']
    assert session.world.steps == 0
