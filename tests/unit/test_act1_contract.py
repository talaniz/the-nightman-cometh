from pathlib import Path
from tools.build_web import fingerprint
from game.session import Session

class Memory:
    def read(self): return None
    def write(self,value): pass

def test_opening_preserves_approved_first_line():
    from game.session import DIALOGUE
    assert DIALOGUE[0][1] == 'Come ye of good faith one and all. So I may tell ye a tale of intrigue, and villainy. For ye see—'

def test_new_run_enters_story_act_not_rehearsal():
    session=Session(Memory());session.start();session.next_dialogue(skip=True)
    assert getattr(session.world,'act',None)=='act1'

def test_art_changes_invalidate_build_evidence(tmp_path,monkeypatch):
    import tools.build_web as build
    # Reuse existing inputs while isolating the additional asset root.
    root=tmp_path/'root';root.mkdir()
    for name in ('game','tools','pyproject.toml','requirements.lock'):
        (root/name).symlink_to(build.ROOT/name,target_is_directory=(build.ROOT/name).is_dir())
    (root/'assets').mkdir();(root/'assets/audio').symlink_to(build.ROOT/'assets/audio',target_is_directory=True)
    art=root/'assets/scenes/act1';art.mkdir(parents=True)
    image=art/'intro.png';image.write_bytes(b'first-art')
    monkeypatch.setattr(build,'ROOT',root)
    before=fingerprint();image.write_bytes(b'revised-art')
    assert fingerprint()!=before,'Shipped art must participate in source fingerprint'

def test_approach_has_distinct_enemies_and_telegraphed_chicken():
    from game.levels.act1 import Act1
    w=Act1()
    assert {'rat','ghoul','chicken'} <= {t.get('kind') for t in w.targets}
    chicken=next(t for t in w.targets if t.get('kind')=='chicken')
    assert chicken['state']=='waiting'

def test_checkpoint_retry_uses_act1_flags():
    from game.levels.act1 import Act1
    w=Act1();w.player.hearts=1;w.flag('mid',1700);w.retry()
    assert w.player.x==1700 and w.player.hearts==3
    w.player.hearts=1;w.flag('mid',1700);assert w.player.hearts==1

def test_boss_isolated_and_only_stunned_hits_count():
    from game.levels.act1 import Act1
    w=Act1();w.player.x=3500;w.step({})
    assert getattr(w,'boss_active',False),'Crossing arena threshold starts Cricket'
    assert all(t.get('kind')=='cricket' for t in w.targets)
    boss=w.targets[0];health=boss['hp']
    w.hit_target(boss,'bat-hit');assert boss['hp']==health
    boss['state']='stunned';w.hit_target(boss,'bat-hit');assert boss['hp']==health-1
    w.hit_target(boss,'bat-hit');assert boss['hp']==health-1

def test_boss_retry_clears_battle_and_transformation():
    from game.levels.act1 import Act1
    w=Act1();w.flag('preboss',3350);w.player.x=3500;w.step({});w.meal();w.retry()
    assert not getattr(w,'boss_active',True)
    assert w.player.dayman==0 and w.player.x==3350

def test_legacy_save_migrates_settings_without_fake_story_progress():
    import json
    from game.progress import Progress
    class Store:
        def read(self):return json.dumps(dict(v=1,checkpoint=1400,flags=['preboss'],settings=dict(music=.3,effects=.6)))
        def write(self,value):pass
    p=Progress(Store());p.load()
    assert p.settings['music']==.3
    assert p.saved['checkpoint']==80 and p.saved['flags']==[]
    assert 'rehearsal' in p.message.lower()

def test_act1_save_roundtrip_retains_completed_flag():
    from game.progress import Progress
    from game.levels.act1 import Act1
    class Store:
        raw=None
        def read(self):return self.raw
        def write(self,value):self.raw=value
    store=Store();w=Act1();w.flag('preboss',3350);w.complete=True
    Progress(store).save(w);p=Progress(store);p.load();restored=Act1();p.restore(restored)
    assert restored.complete and restored.checkpoint==3350

def test_replay_completed_act_preserves_completion():
    s=Session(Memory());s.world.complete=True;s.progress.save(s.world);s.enter_screen('complete')
    s.selection=s.menu().index('Replay Act 1');s.activate()
    assert s.screen=='dialogue'
    assert s.progress.saved['complete'] is True
    assert not s.world.complete

def test_opening_advance_and_skip_reach_identical_start():
    a=Session(Memory());b=Session(Memory());a.start();b.start()
    for _ in a.sequence:a.next_dialogue()
    b.next_dialogue(skip=True)
    assert a.screen==b.screen=='training'
    assert a.world.snapshot()==b.world.snapshot()

def test_win_transition_runs_once_and_never_loads_bridge():
    s=Session(Memory());s.start();s.next_dialogue(skip=True);s.world.complete=True;s.update(0,{})
    assert s.screen=='dialogue' and s.sequence[0].speaker=='DEE'
    s.next_dialogue(skip=True);assert s.screen=='complete'
    s.update(1,{});assert s.screen=='complete'

def test_normal_input_route_can_win_without_beams():
    from game.levels.act1 import Act1
    from game.world import DT
    w=Act1();last_bat=-100;used_beam=False
    for frame in range(12000):
        p=w.player;keys={}
        assert not w.dead, ('route died',p.x,w.checkpoint)
        if w.complete:break
        if not w.boss_active:
            keys['right']=True
            gap=any(0<edge-p.x<55 for edge in (1050,2500))
            enemy=any(t['alive'] and 0<t['x']-p.x<80 and abs(t['y']-p.y)<60 for t in w.targets)
            avoid_meal=0<1810-p.x<65
            keys['jump']=p.grounded and (gap or enemy or avoid_meal)
            keys['bat']=frame-last_bat>15
        else:
            boss=w.targets[0];dx=boss['x']-p.x
            if boss['state']=='stunned':
                keys.update(right=dx>30,left=dx<-30,bat=abs(dx)<70 and frame-last_bat>16)
            else:
                keys.update(right=dx>130,left=dx<-130,jump=p.grounded and abs(dx)<125 and boss['state']=='charge')
        if keys.get('bat'):last_bat=frame
        w.advance(DT,keys)
        assert not w.beams and w.player.dayman==0
    assert w.complete,'Ordinary bat/stomp route must finish'
    assert w.flags=={'mid','preboss'}

def test_boss_telegraph_crash_stun_and_pause():
    from game.levels.act1 import Act1
    from game.world import DT
    w=Act1();w.player.x=3500;w.step({});boss=w.targets[0]
    assert boss['state']=='warning' and boss['timer']>.5
    w.paused=True;before=w.snapshot();w.advance(3,{});assert w.snapshot()==before
    w.paused=False;w.player.x=4100
    for _ in range(200):
        w.step({})
        if boss['state']=='stunned':break
    assert boss['state']=='stunned' and boss['timer']==1.5
    assert boss['x'] in (3540,4050)

def test_missing_required_art_fails_before_packaging(tmp_path,monkeypatch):
    import pytest
    import tools.build_web as build
    monkeypatch.setattr(build,'ROOT',tmp_path)
    with pytest.raises(ValueError,match='Missing required art'):
        build.validate_art()

def test_corrupt_art_is_rejected_before_browser_build(tmp_path,monkeypatch):
    import pytest
    import tools.build_web as build
    monkeypatch.setattr(build,'ROOT',tmp_path)
    for rel in ['sprites/cast.png','scenes/act1/opening.png','scenes/act1/kidnapping.png','backgrounds/act1/street.png','ui/kitten-mittens.png']:
        p=tmp_path/'assets'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'broken png')
    with pytest.raises(ValueError,match='Invalid art'):
        build.validate_art()

def test_chicken_warning_cannot_damage_before_swoop():
    from game.levels.act1 import Act1
    w=Act1();chicken=next(t for t in w.targets if t['kind']=='chicken')
    w.player.x=2200;w.player.y=160;w.player.grounded=False
    chicken.update(x=2200,y=160,state='warning',timer=1.2)
    w.step({})
    assert w.player.hearts==3,'A warning must precede damaging contact'

def test_qa_completion_replay_does_not_overwrite_normal_save():
    import json
    class Store:
        raw=None
        def read(self):return self.raw
        def write(self,value):self.raw=value
    store=Store();s=Session(store);s.start();s.next_dialogue(skip=True)
    before=store.raw;normal=s.world
    s.password='PAINTDOG';s.submit_password();s.world.complete=True;s.update(0,{})
    s.next_dialogue(skip=True)
    assert s.menu()==['Replay QA Act 1','Exit QA']
    s.activate();assert s.qa and store.raw==before
    s.next_dialogue(skip=True);s.back();s.selection=s.menu().index('Exit QA');s.activate()
    assert not s.qa and s.world is normal and store.raw==before

def test_knocked_out_cricket_does_not_hurt_player_on_contact():
    from game.levels.act1 import Act1
    w=Act1();w.player.x=3500;w.step({});boss=w.targets[0]
    boss.update(state='stunned',timer=1.5,x=3700);w.player.x=3700
    w.step({})
    assert w.player.hearts==3,'A stunned Cricket is an opening, not a contact hazard'

def test_title_from_future_qa_restores_normal_act_before_continue():
    s=Session(Memory());s.start();s.next_dialogue(skip=True);normal=s.world
    s.password='TROLLTOLL';s.submit_password();s.back();s.selection=s.menu().index('Title');s.activate()
    assert not s.qa and s.world is normal
    s.selection=s.menu().index('Continue Act 1');s.activate()
    assert s.screen=='training' and s.world.act=='act1'

def test_cricket_actual_stomp_and_beam_collision_windows():
    from game.levels.act1 import Act1
    for attack in ('stomp','beam'):
        for vulnerable in (False,True):
            w=Act1();w.player.x=3500;w.step({});boss=w.targets[0]
            boss.update(x=3750,state='stunned' if vulnerable else 'warning',timer=1.5)
            if attack=='stomp':
                w.player.x=3750;w.player.y=345;w.player.vy=200;w.player.grounded=False
            else:
                w.player.x=3700;w.meal();w.shoot()
            for _ in range(12):w.step({})
            assert boss['hp']==(2 if vulnerable else 3),(attack,vulnerable,boss)

def test_act1_simulation_is_independent_of_render_frequency():
    from game.levels.act1 import Act1
    samples=[]
    for hz in (30,60,120):
        w=Act1()
        for _ in range(hz*2):w.advance(1/hz,{'right':True})
        samples.append(w.snapshot())
    assert samples[0]==samples[1]==samples[2]

def test_linked_art_root_cannot_package_outside_content(tmp_path,monkeypatch):
    import pytest
    import tools.build_web as build
    root=tmp_path/'repo';(root/'assets').mkdir(parents=True)
    external=tmp_path/'outside';external.mkdir();(external/'private.png').write_bytes(b'not approved')
    (root/'assets/scenes').symlink_to(external,target_is_directory=True)
    monkeypatch.setattr(build,'ROOT',root)
    with pytest.raises(ValueError,match='Linked production art'):
        build.art_files()
