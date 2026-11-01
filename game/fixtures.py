"""Synthetic fixtures included ONLY by --test-fixtures builds."""
from game.world import World

def apply(session,request):
    name=request.get('name')
    if name.startswith('act2-'):
        return act2_fixture(session,name)
    if name.startswith('act1-'):
        return act1_fixture(session,name)
    if name=='clear':session.enter_screen('title');return
    session.world=World();session.qa=True;session.qa_label='AUTOMATED FIXTURE';session.enter_screen('training')
    w=session.world
    if name=='bat':w.player.x=480
    elif name=='stomp':w.player.x=520;w.player.y=335;w.player.vy=220;w.player.grounded=False
    elif name=='side':w.player.x=519
    elif name=='meal':w.player.x=610
    elif name=='flag':w.player.hearts=1;w.player.x=360
    elif name=='repeat-flag':w.flag('mid',400);w.player.hearts=1;w.player.x=360
    elif name=='death':w.flag('mid',400);w.player.hearts=1;w.player.x=519
    elif name=='food':w.player.x=220;w.player.hearts=2
    elif name=='full-food':w.player.x=220
    elif name=='dayman':w.meal()
    else:raise ValueError('Unknown test fixture')


def act1_fixture(session,name):
    from game.levels.act1 import Act1
    from game.scenes.opening import OPENING,FRANK
    session.world=Act1();session.qa=True;session.qa_label='ACT1 AUTOMATED FIXTURE'
    session.replaying=False;session.enter_screen('training');w=session.world
    suffix=name[5:]
    frozen=suffix.startswith('pose-')
    if frozen:suffix=suffix[5:]
    if suffix.startswith('story-'):
        session.sequence=OPENING;session.dialogue=int(suffix.split('-')[1]);session.enter_screen('dialogue')
    elif suffix.startswith('frank-'):
        session.sequence=FRANK;session.dialogue=int(suffix.split('-')[1]);session.enter_screen('dialogue')
    elif suffix=='approach':pass
    elif suffix in ('platform-first','platform-second','platform-third'):
        # Isolate geometry from combat while preserving real platforms and jump physics.
        w.player.x={'platform-first':720,'platform-second':2080,'platform-third':2860}[suffix]
        w.targets=[]
    elif suffix=='bat':w.player.swing=.12
    elif suffix=='jump':w.player.y=300;w.player.grounded=False
    elif suffix=='hurt':w.player.hearts=2;w.player.invulnerable=.6
    elif suffix=='meal':w.player.x=1810
    elif suffix=='chicken':
        w.player.x=2080
        chicken=next(t for t in w.targets if t['kind']=='chicken')
        chicken.update(state='warning',timer=1.2,x=2400)
    elif suffix=='mid':w.player.x=1660;w.player.hearts=1
    elif suffix=='preboss':w.player.x=3310;w.player.hearts=1
    elif suffix=='death':w.flag('preboss',3350);w.player.hearts=0;w.dead=True;session.enter_screen('dead')
    elif suffix.startswith('boss-'):
        w.flag('preboss',3350);w.player.x=3700;w.enter_boss();b=w.targets[0]
        state=suffix[5:];b['state']=state;b['timer']=1.5
        if state=='stunned':b['x']=3750
        if state=='defeated':b['alive']=False;b['hp']=0
    elif suffix=='complete':w.complete=True;session.enter_screen('complete')
    else:raise ValueError('Unknown Act1 fixture')
    # Visual-pose fixtures freeze only test-build simulation; live interaction tests are separate.
    if frozen:w.paused=True

def act2_fixture(session,name):
    from game.levels.act2 import Act2
    from game.scenes.opening import FRANK,NIGHTMAN
    session.world=Act2();session.qa=True;session.qa_label='AUTOMATED ACT2 FIXTURE';session.enter_screen('training')
    w=session.world;suffix=name[5:]
    if suffix.startswith('frank-story-') or suffix.startswith('nightman-story-'):
        session.sequence=FRANK if suffix.startswith('frank-story-') else NIGHTMAN
        session.dialogue=int(suffix.rsplit('-',1)[1]);session.replaying=False;session.enter_screen('dialogue');return
    if suffix=='approach':w.player.x=120
    elif suffix=='crew':w.player.x=1170
    elif suffix=='gun':w.player.x=660
    elif suffix=='meal':w.player.x=1520
    elif suffix=='mid':w.player.x=1460;w.player.hearts=1
    elif suffix=='preboss':w.player.x=2760;w.player.hearts=1
    elif suffix=='death':w.flag('preboss',2800);w.player.hearts=0;w.dead=True;session.enter_screen('dead')
    elif suffix=='complete':w.complete=True;session.enter_screen('complete')
    elif suffix.startswith('platform-'):
        w.targets=[];w.pickups=[];w.player.x=590 if suffix=='platform-first' else 1770
    elif suffix.startswith('boss'):
        w.flag('preboss',2800);w.player.x=3200;w.enter_boss();b=w.targets[0]
        if suffix=='boss-close':b['x']=3250;b['timer']=10
        elif suffix=='boss-stomp':w.player.x=b['x'];w.player.y=b['y']-64;w.player.vy=100;w.player.grounded=False
        elif suffix=='boss-beam':w.meal()
    else:raise ValueError('Unknown Act2 fixture')
