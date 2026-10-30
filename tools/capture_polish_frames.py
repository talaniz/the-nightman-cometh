"""Supplemental rendered pose sheets. Browser workflows remain acceptance evidence."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pygame
from game.render import Renderer
from game.levels.act1 import Act1

def capture(directory):
    directory.mkdir(parents=True,exist_ok=True)
    pygame.init();pygame.display.set_mode((960,540))
    sheet=pygame.Surface((960,540));sheet.fill((24,25,39));r=Renderer(sheet)
    r.text('ACTUAL RENDERER · BAT WINDUP / STRIKE / RECOVERY',15,10)
    for row,(dayman,facing) in enumerate(((0,1),(0,-1),(10,1),(10,-1))):
        r.text(('DAYMAN' if dayman else 'DENNIS')+(' LEFT' if facing<0 else ' RIGHT'),10,65+row*115)
        for col,remaining in enumerate((.21,.12,.02)):
            p=Act1().player;p.x=250+col*250;p.y=65+row*115;p.swing=remaining;p.facing=facing;p.dayman=dayman
            r.actor(p,0,0)
            r.text(('WINDUP','STRIKE','RECOVERY')[col],p.x-25,p.y+53,font=r.small)
    pygame.image.save(sheet,str(directory/'bat-motion-sheet.png'))
    sheet.fill((24,25,39));r.text('ACTUAL RENDERER · FOUR DISTINCT SIMULATION-TIMED POSES',15,10)
    for row,kind in enumerate(('rat','ghoul')):
        for col,step in enumerate((0,8,16,24)):
            t=dict(kind=kind,x=140+col*220,y=130+row*210,alive=True,state='patrol',direction=1,animation_step=step)
            # Enlarged through the same atlas path for inspection; game uses native sprite size.
            sprite=r.art.sequence('sprites/enemy-walk.png',col+row*4,4,2,(132,69) if row==0 else (114,126),trim_row=True)
            sheet.blit(sprite,(t['x']-40,t['y']-30));r.text(kind.upper()+' '+str(col+1),t['x']-25,t['y']+110,font=r.small)
    pygame.image.save(sheet,str(directory/'enemy-motion-sheet.png'))
    pygame.quit()

if __name__=='__main__':capture(Path(sys.argv[1]))
