"""Synthetic fixtures included ONLY by --test-fixtures builds."""
from game.world import World

def apply(session,request):
    name=request.get('name')
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
