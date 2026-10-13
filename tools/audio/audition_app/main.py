import asyncio
import json
from pathlib import Path
import sys
import time
import pygame
from director import Director
from backend import Mixer

WEB = sys.platform == 'emscripten'
if WEB:
    from platform import window

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((960, 640))
pygame.display.set_caption('The Nightman Cometh · Sound check')
manifest = json.loads(Path('audio/manifest.json').read_text())
mixer = Mixer(manifest, 'audio')
director = Director(manifest, mixer)
scenes = list(manifest['scenes'])
effects = manifest['effects']
selected = 0
fx = 0
font = pygame.font.Font(None, 26)
small = pygame.font.Font(None, 23)
heading = pygame.font.Font(None, 44)
last_time = time.monotonic()


def text(words, x, y, color=(229,222,195), face=None):
    screen.blit((face or font).render(words, True, color), (x,y))


def draw():
    screen.fill((15,19,32))
    pygame.draw.rect(screen,(192,148,59),(28,30,904,2))
    text('THE NIGHTMAN COMETH',32,48,(229,184,76),heading)
    text('SOUND CHECK  /  M2 AUDITION',34,98,(155,170,194),small)
    state='Press Enter to enable audio' if not director.unlocked else ('Paused' if director.paused else ('Muted' if director.muted else 'Playing'))
    if director.error:state='Audio unavailable - press R to retry'
    text(state,34,139,(247,180,110) if director.error else (151,216,187))
    for i,scene in enumerate(scenes):
        y=185+i*28
        if i==selected:pygame.draw.rect(screen,(47,57,79),(28,y-3,292,27),border_radius=3)
        text(('> ' if i==selected else '  ')+scene.replace('-',' ').title(),34,y)
    text('NOW PLAYING',360,185,(155,170,194),small)
    text((director.playing or 'Silence').replace('-',' ').title(),360,216,(229,184,76))
    text('Scene: '+director.scene,360,255)
    text('Dayman: '+str(round(director.remaining,1))+' s',360,288)
    text(f'Music {director.music_volume:.0%}   /   Effects {director.sfx_volume:.0%}',360,327)
    text('Effect: '+effects[fx].replace('-',' ').title(),360,368)
    for j,line in enumerate(['Up/Down  choose scene    Enter  play',
        'D  Dayman    P  pause/resume    M  mute',
        'Left/Right  effect    Space  play effect',
        '1/2  music volume    3/4  effect volume',
        'X  missing-file check    R  retry current scene']):
        text(line,360,421+j*29,(174,186,209),small)
    text('Listen for phrasing, loop joins, transitions and effect clarity.',34,589,(155,170,194),small)
    pygame.display.flip()


async def main():
    global selected, fx, last_time
    while True:
        now=time.monotonic();dt=min(.1,now-last_time);last_time=now
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return
            if event.type==pygame.WINDOWFOCUSLOST:
                director.pause(True)
            if event.type!=pygame.KEYDOWN:
                continue
            key=event.key
            if key==pygame.K_UP:selected=(selected-1)%len(scenes)
            elif key==pygame.K_DOWN:selected=(selected+1)%len(scenes)
            elif key==pygame.K_RETURN:
                director.set_scene(scenes[selected]);director.unlock()
            elif key==pygame.K_d:director.transform()
            elif key==pygame.K_p:director.pause(not director.paused)
            elif key==pygame.K_m:director.volumes(muted=not director.muted)
            elif key==pygame.K_LEFT:fx=(fx-1)%len(effects)
            elif key==pygame.K_RIGHT:fx=(fx+1)%len(effects)
            elif key==pygame.K_SPACE:director.effect(effects[fx])
            elif key in (pygame.K_1,pygame.K_2):director.volumes(music=round(max(0,min(1,director.music_volume+(-.1 if key==pygame.K_1 else .1))),2))
            elif key in (pygame.K_3,pygame.K_4):director.volumes(sfx=round(max(0,min(1,director.sfx_volume+(-.1 if key==pygame.K_3 else .1))),2))
            elif key==pygame.K_x:
                mixer.fail_next=True;director.retry()
            elif key==pygame.K_r:director.retry()
        director.tick(dt)
        if WEB:
            window.__nightmanAudio=json.dumps(dict(scene=director.scene,playing=director.playing,
                paused=director.paused,muted=director.muted,remaining=director.remaining,
                error=director.error,unlocked=director.unlocked,python=sys.version,pygame=pygame.version.ver,**mixer.state()))
        draw()
        await asyncio.sleep(0)

asyncio.run(main())
