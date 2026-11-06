from types import SimpleNamespace
from game.input.controls import Controls
from game.input.actions import perform, PASSWORD_KEYS
from game.session import Session

class Storage:
    def read(self): return None
    def write(self, value): pass

class Audio:
    muted = False
    def volumes(self, **kwargs): self.muted = kwargs.get('muted', self.muted)


def test_controller_password_edit_submit_and_keyboard_confirm():
    s, c, a = Session(Storage()), Controls(), Audio()
    s.enter_screen('password');c.pad_mode=True
    for letter in 'PAINTDOG':
        c.password_index=PASSWORD_KEYS.index(letter)
        perform(s,a,c,{'confirm'})
    c.password_index=PASSWORD_KEYS.index('GO');perform(s,a,c,{'confirm'})
    assert s.qa and s.world.act=='act1' and s.screen=='training'
    s.enter_screen('password');s.password='NIGHTMAN';c.pad_mode=False
    perform(s,a,c,{'confirm'})
    assert s.world.act=='act3' and s.screen=='training'


def test_password_limit_delete_invalid_and_back():
    s,c,a=Session(Storage()),Controls(),Audio();s.enter_screen('password');c.pad_mode=True
    s.password='A'*16;perform(s,a,c,{'confirm'});assert len(s.password)==16
    c.password_index=36;perform(s,a,c,{'confirm'});assert len(s.password)==15
    c.password_index=37;perform(s,a,c,{'confirm'});assert s.screen=='password' and 'Unknown' in s.message
    perform(s,a,c,{'back'});assert s.screen=='title'


def test_controller_options_and_pause_do_not_emit_attacks():
    s,c,a=Session(Storage()),Controls(),Audio()
    s.enter_screen('options');old=s.progress.settings['music']
    perform(s,a,c,{'left'});assert s.progress.settings['music']==round(old-.1,1)
    s.enter_screen('training')
    assert not perform(s,a,c,{'pause','jump','bat'})
    assert s.screen=='pause'
    perform(s,a,c,{'pause'});assert s.screen=='training'
    assert perform(s,a,c,{'jump','bat','beam'})=={'jump','bat','beam'}


def test_mute_and_menu_confirm_single_action():
    s,c,a=Session(Storage()),Controls(),Audio()
    perform(s,a,c,{'mute'});assert a.muted
    perform(s,a,c,{'confirm','down'});assert s.screen=='dialogue' and s.dialogue==0


def test_editing_password_clears_stale_error():
    s,c,a=Session(Storage()),Controls(),Audio();s.enter_screen('password');c.pad_mode=True
    s.message='Unknown password';perform(s,a,c,{'confirm'});assert s.message==''
    s.message='Unknown password';c.password_index=36;perform(s,a,c,{'confirm'});assert s.message==''
