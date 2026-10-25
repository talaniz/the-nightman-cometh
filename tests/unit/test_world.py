from game.world import World

def test_flag_cannot_heal_twice_even_after_retry():
    w=World();w.player.hearts=1;w.flag('mid',400);assert w.player.hearts==2
    w.flag('mid',400);assert w.player.hearts==2
    w.retry();w.player.hearts=1;w.flag('mid',400);assert w.player.hearts==1

def test_meal_timer_pauses_and_food_caps():
    w=World();w.meal();w.paused=True
    for _ in range(120):w.step()
    assert w.player.dayman==10
    w.food();assert w.player.hearts==3

def test_contact_invulnerability():
    w=World();w.hurt();w.hurt();assert w.player.hearts==2

def test_beam_is_one_horizontal_projectile():
    w=World();w.meal();w.shoot();assert len(w.beams)==1 and w.beams[0]['dy']==0

def test_side_contact_is_not_stomp():
    assert World().contact(440,400,True)=='hurt'

def test_render_rates_produce_same_world():
    results=[]
    for hz in (30,60,120):
        w=World()
        for _ in range(hz):w.advance(1/hz,{'right':True})
        results.append((round(w.player.x,6),round(w.player.y,6),w.steps))
    assert results[0]==results[1]==results[2]

def test_bat_window_and_stomp_actually_remove_targets():
    w=World();w.player.x=480;w.attack()
    for _ in range(10):w.step()
    assert not w.targets[0]['alive'] and w.events.count('bat-hit')==1
    w=World();w.player.x=520;w.player.y=340;w.player.vy=220;w.player.grounded=False
    for _ in range(8):w.step()
    assert not w.targets[0]['alive'] and 'stomp' in w.events and w.player.hearts==3

def test_retry_clears_transients_and_restores_checkpoint():
    w=World();w.flag('mid',400);w.meal();w.shoot();w.player.hearts=0;w.dead=True;w.retry()
    assert w.player.x==400 and w.player.hearts==3 and w.player.dayman==0 and not w.beams
    assert w.flags=={'mid'} and all(t['alive'] for t in w.targets)

def test_no_fall_through_floor_and_timer_expires():
    w=World();w.meal();w.player.y=0;w.player.vy=800
    for _ in range(601):w.step()
    assert w.player.y==386 and w.player.dayman==0

def test_training_projectile_can_be_batted_without_damage():
    w=World()
    for _ in range(125):w.step()
    assert w.snapshot().get('shots'), 'training launcher must emit a visible projectile'
    shot=w.shots[0];w.player.x=shot['x']-45;w.attack()
    for _ in range(8):w.step()
    assert not w.shots and w.player.hearts==3
