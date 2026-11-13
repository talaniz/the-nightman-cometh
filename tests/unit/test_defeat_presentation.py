import pytest
from game.session import Session
from game.levels.act1 import Act1
from game.levels.act2 import Act2
from game.levels.act3 import Act3
from game.scenes.opening import FRANK,NIGHTMAN
from game.scenes.finale import FINALE
from test_progress import Memory

@pytest.mark.parametrize('level,story',[(Act1,FRANK),(Act2,NIGHTMAN),(Act3,FINALE)])
def test_final_hit_holds_boss_then_transitions_once_and_pause_freezes(level,story):
    store=Memory();s=Session(store);s.world=level();s.world.enter_boss();s.enter_screen('training')
    boss=s.world.targets[0];boss['hp']=1;boss['state']='stunned';boss['immune']=0
    assert s.world.hit_target(boss,'bat-hit')
    s.update(.1,{})
    assert s.screen=='training','final hit must show boss defeat before the story'
    assert s.world.complete and not boss['alive']
    pos=(s.world.player.x,s.world.player.y);hp=s.world.player.hearts
    for _ in range(10):s.update(.1,{'right':True,'jump':True,'bat':True})
    assert (s.world.player.x,s.world.player.y)==pos and s.world.player.hearts==hp
    s.blur();assert s.screen=='pause'
    for _ in range(100):s.update(.1,{})
    s.activate();assert s.screen=='training'
    for _ in range(18):s.update(.1,{})
    assert s.screen=='training'
    s.update(.1,{})
    assert s.screen=='dialogue' and s.sequence is story
    writes=store.writes
    for _ in range(10):s.update(.1,{})
    assert s.dialogue==0 and store.writes==writes

@pytest.mark.parametrize('elapsed',[.1,.6,1.1,2.8])
@pytest.mark.parametrize('kind',['cricket','frank','nightman'])
@pytest.mark.parametrize('direction',[-1,1])
def test_hurt_boss_stays_upright_at_floor_despite_faint_padding(kind,direction,elapsed):
    import pygame
    from game.render import Renderer
    sprite=pygame.Surface((80,80),pygame.SRCALPHA)
    sprite.fill((200,100,50,1))
    pygame.draw.rect(sprite,(200,100,50,255),(10,12,55,58))
    class Art:
        def image(self,*args,**kwargs):return sprite.copy()
        def sequence(self,*args,**kwargs):return sprite.copy()
        def nightman(self,*args,**kwargs):return sprite.copy(),None
    renderer=Renderer.__new__(Renderer)
    renderer.screen=pygame.Surface((960,540),pygame.SRCALPHA)
    renderer.art=Art();renderer.small=None;renderer.text=lambda *args:None
    renderer.defeated_boss(dict(kind=kind,direction=direction,x=400,y=380,defeat_elapsed=elapsed),0)
    bounds=renderer.screen.get_bounding_rect(min_alpha=20)
    assert bounds.bottom==430
    assert bounds.size==(55,58),'hurt pose must not rotate sideways'
