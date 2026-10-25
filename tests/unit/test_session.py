from game.session import Session
from test_progress import Memory

def test_skip_is_once_and_replay_does_not_save():
    store=Memory();s=Session(store);s.start();writes=store.writes
    s.next_dialogue(skip=True);assert s.screen=='training'
    s.enter_screen('pause');s.selection=2;s.activate();s.next_dialogue(skip=True)
    assert s.screen=='pause' and store.writes==writes

def test_passwords_are_isolated_and_exit_restores_normal():
    s=Session(Memory());normal=s.world;s.password='bad';s.submit_password();assert s.message and not s.qa
    s.password='PAINTDOG';s.submit_password();assert s.qa and s.world is not normal
    s.enter_screen('pause');s.selection=s.menu().index('QA checkpoint');s.activate()
    assert s.world.checkpoint==1400 and s.progress.saved is None
    s.enter_screen('pause');s.selection=s.menu().index('Exit QA');s.activate();assert s.world is normal and not s.qa

def test_new_game_confirmation_and_blur_pause():
    s=Session(Memory());s.start();s.next_dialogue(skip=True);s.blur();assert s.screen=='pause' and s.world.paused
    s.enter_screen('title');s.activate();assert s.screen=='confirm'
    s.activate();assert s.screen=='title'
