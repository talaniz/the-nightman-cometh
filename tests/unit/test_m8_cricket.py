"""Cricket's feint must have a safe tell and still lead to a punish window."""
from game.levels.act1 import Act1
from game.world import DT


def encounter():
    world = Act1()
    world.player.x = 5000
    world.enter_boss()
    return world, world.targets[0]


def test_charge_brakes_then_reverses_before_dumpster_and_eventually_crashes():
    world, boss = encounter()
    initial_direction = boss['direction']
    braked = reversed_charge = False
    stationary_frames = 0
    for _ in range(360):
        old_x, old_state = boss['x'], boss['state']
        world.step({})
        if boss['state'] == 'brake':
            braked = True
            assert 4440 < boss['x'] < 4950
            assert not world.contact_hurts(boss), 'braking tell must not deal contact damage'
            if old_state == 'brake':
                assert boss['x'] == old_x
                stationary_frames += 1
        if boss['state'] == 'charge' and boss['direction'] != initial_direction:
            reversed_charge = True
        if boss['state'] == 'stunned':
            break
    assert braked, 'Cricket must telegraph an occasional mid-charge reversal'
    assert stationary_frames >= 15, 'player needs time to react to the reversal'
    assert reversed_charge
    assert boss['state'] == 'stunned', 'bounded feint must still end at a dumpster'
    assert boss['x'] in (4440, 4950)


def test_brake_pause_is_stable_and_retry_resets_encounter():
    world, boss = encounter()
    for _ in range(180):
        world.step({})
        if boss['state'] == 'brake':
            break
    assert boss['state'] == 'brake'
    world.paused = True
    before = dict(boss)
    world.advance(2, {})
    assert boss == before
    world.paused = False
    world.retry()
    assert not world.boss_active
    world.enter_boss()
    assert world.targets[0]['state'] == 'warning'


def test_cricket_has_four_distinct_running_poses_at_a_fixed_position():
    import pygame
    from game.render import Renderer
    pygame.display.init();pygame.font.init();pygame.display.set_mode((960,540))
    renderer=Renderer(pygame.Surface((960,540)))
    _,boss=encounter();boss.update(x=400.,state='charge')
    frames=[]
    for tick in (0,6,12,18):
        boss['animation_step']=tick
        renderer.screen.fill((0,0,0));renderer.enemy(boss,0)
        frames.append(pygame.image.tobytes(renderer.screen,'RGB'))
    assert len(set(frames))==4
