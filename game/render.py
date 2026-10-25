"""Code-native pixel scenery and representative rehearsal sprites."""
import math
import pygame
from game.world import FLAGS, PLATFORMS, WIDTH
from game.session import DIALOGUE

INK=(15,18,32);GOLD=(231,185,87);CREAM=(238,227,199);MUTED=(166,174,192)

class Renderer:
    def __init__(self,screen):
        self.screen=screen
        self.font=pygame.font.Font(None,25);self.small=pygame.font.Font(None,21);self.large=pygame.font.Font(None,48)
    def text(self,text,x,y,color=CREAM,font=None):
        self.screen.blit((font or self.font).render(text,False,color),(int(x),int(y)))
    def center(self,text,y,color=CREAM,font=None):
        image=(font or self.font).render(text,False,color);self.screen.blit(image,((960-image.get_width())//2,y))
    def rect(self,color,rect,width=0):pygame.draw.rect(self.screen,color,tuple(int(v) for v in rect),width)
    def bat(self,x,y,scale=1,flip=False):
        sprite=pygame.Surface((46,20),pygame.SRCALPHA)
        pygame.draw.polygon(sprite,(49,29,23),[(0,14),(9,9),(41,2),(45,5),(43,10),(10,16),(1,18)])
        pygame.draw.line(sprite,(164,111,65),(5,13),(42,6),5)
        for px in (20,29,36):
            pygame.draw.line(sprite,(218,215,195),(px,8),(px-3,2),2)
            pygame.draw.circle(sprite,(100,102,111),(px,11),3)
            pygame.draw.line(sprite,(149,139,142),(px+2,12),(px+7,17),1)
        if flip:sprite=pygame.transform.flip(sprite,True,False)
        self.screen.blit(pygame.transform.scale(sprite,(int(46*scale),int(20*scale))),(int(x),int(y)))
    def person(self,x,y,dayman=False,facing=1,swing=False,walk=0,portrait=False):
        s=pygame.Surface((28,48),pygame.SRCALPHA)
        def r(c,b):pygame.draw.rect(s,c,b)
        skin=(224,169,115);dark=(38,34,39);shirt=(63,112,72) if not dayman else (239,229,201)
        r(dark,(7,0,15,9));r(skin,(8,6,13,13));r((112,70,42),(8,5,5,4));r(dark,(17 if facing>0 else 9,10,2,2))
        r((188,131,84),(10,16,10,3));r(shirt,(5,20,19,16));r((35,69,48) if not dayman else GOLD,(7,34,17,3))
        r(skin,(2,23,4,13));r(shirt,(1,20,5,7));r(skin,(23,23,4,11))
        offset=int(math.sin(walk)*3)
        pants=(44,48,62) if not dayman else CREAM
        r(pants,(7,37,6,8+offset));r(pants,(17,37,6,8-offset));r(dark,(5,44+offset,9,3));r(dark,(17,44-offset,9,3))
        if dayman:
            pygame.draw.circle(s,GOLD,(15,26),4,1)
            for a in range(0,360,45):
                dx=math.cos(math.radians(a));dy=math.sin(math.radians(a));pygame.draw.line(s,GOLD,(15+dx*5,26+dy*5),(15+dx*7,26+dy*7))
        self.screen.blit(s,(int(x)-2,int(y)-4))
        if swing:
            self.bat(x+18 if facing>0 else x-44,y+10,1,flip=facing<0)
            pygame.draw.arc(self.screen,GOLD,(int(x)-28,int(y)-10,80,60),-.6,.6,2)
        else:self.bat(x+12 if facing>0 else x-28,y+23,.7,flip=facing<0)
    def portrait(self,name,x,y):
        # Rehearsal portraits: director Charlie and Dee, distinct from Dennis.
        self.rect((38,43,59),(x-8,y-8,72,110));skin=(224,169,115)
        if name=='CHARLIE':
            self.rect((85,88,99),(x+9,y-8,32,27));self.rect((156,157,164),(x+5,y+16,42,6))
            self.rect(skin,(x+13,y+23,29,31));self.rect((93,65,49),(x+13,y+43,29,13))
            self.rect((128,128,141),(x+3,y+57,49,40));self.rect(CREAM,(x+23,y+57,12,30))
            self.rect(GOLD,(x+20,y+60,18,7))
        else:
            self.rect((216,179,88),(x+5,y+9,44,58));self.rect(skin,(x+14,y+19,27,32))
            self.rect((113,158,192),(x+3,y+57,49,40));self.rect(CREAM,(x+16,y+57,25,40))
        self.rect(INK,(x+20,y+29,3,3));self.rect(INK,(x+33,y+29,3,3))
    def scenery(self,camera):
        self.screen.fill(INK)
        pygame.draw.circle(self.screen,(194,200,208),(790-int(camera*.07),135),26)
        pygame.draw.circle(self.screen,(157,164,181),(783-int(camera*.07),130),6)
        for i in range(24):
            x=i*95-int(camera*.2);height=90+(i*37%140)
            self.rect((28,35,55),(x,430-height,72,height))
            for yy in range(440-height,420,28):
                for xx in (12,38):self.rect((114,98,62),(x+xx,yy,8,11))
        # Painted City Hall tower, suspended moon and visible stage braces.
        x=450-int(camera*.12);self.rect((49,56,75),(x,205,58,225));self.rect((62,70,88),(x+13,165,30,80))
        pygame.draw.polygon(self.screen,(69,77,96),[(x+13,165),(x+28,115),(x+43,165)])
        pygame.draw.circle(self.screen,GOLD,(x+28,206),10,2);pygame.draw.line(self.screen,GOLD,(x+28,206),(x+28,199),2)
        pygame.draw.line(self.screen,(71,73,85),(790-int(camera*.07),65),(790-int(camera*.07),109))
        for bx in range(0,2100,320):
            xx=bx-camera;pygame.draw.line(self.screen,(53,43,44),(xx,430),(xx+100,300),6)
        for x,y,w,h in PLATFORMS:
            self.rect((94,61,47),(x-camera,y,w,h));self.rect((167,115,66),(x-camera,y,w,6))
            for yy in range(y+15,y+h,20):pygame.draw.line(self.screen,(59,42,39),(x-camera,yy),(x+w-camera,yy),1)
        for name,x in FLAGS.items():
            sx=x-camera;pygame.draw.line(self.screen,(193,184,158),(sx,430),(sx,360),3)
            self.text('MIDPOINT' if name=='mid' else 'PRE-BOSS PROP',sx-35,445,MUTED,self.small)
        self.text('BAT PRACTICE',490-camera,350,GOLD,self.small)
        self.text('MIND THE GAP',1050-camera,472,MUTED,self.small)
        self.text('END OF REHEARSAL',1510-camera,355,GOLD,self.small)
    def training(self,session):
        w=session.world;p=w.player;camera=max(0,min(WIDTH-960,p.x-350));self.scenery(camera)
        for name,x in FLAGS.items():
            color=(126,202,139) if name in w.flags else GOLD
            pygame.draw.polygon(self.screen,color,[(x-camera+2,362),(x-camera+35,371),(x-camera+2,382)])
        for t in w.targets:
            if t['alive']:
                x=t['x']-camera;y=t['y'];self.rect((123,65,63),(x,y,30,32));self.rect((199,139,83),(x+4,y+4,22,24))
                pygame.draw.circle(self.screen,(91,43,44),(int(x)+15,int(y)+15),9,2);pygame.draw.circle(self.screen,CREAM,(int(x)+15,int(y)+15),3)
                self.rect((67,47,42),(x+11,y+29,8,4))
        for item in w.pickups:
            if item['taken']:continue
            x=item['x']-camera;y=item['y']
            if item['kind']=='meal':
                pygame.draw.ellipse(self.screen,CREAM,(x-18,y-6,38,12));pygame.draw.ellipse(self.screen,(142,75,64),(x-12,y-10,20,12))
                for dx,c in ((10,(177,211,117)),(15,GOLD),(6,(191,99,143))):pygame.draw.circle(self.screen,c,(int(x+dx),int(y-5)),3)
            else:
                self.rect((122,159,173),(x-9,y-15,18,22));self.rect(CREAM,(x-9,y-10,18,10));self.text('CAT',x-8,y-10,INK,self.small)
        if not (p.invulnerable>0 and int(p.invulnerable*12)%2):self.person(p.x-camera,p.y,p.dayman>0,p.facing,p.swing>0,w.steps*.22 if p.grounded else 0)
        for shot in w.shots:
            pygame.draw.circle(self.screen,(207,98,76),(int(shot['x']-camera),int(shot['y'])),7)
            pygame.draw.circle(self.screen,GOLD,(int(shot['x']-camera)-2,int(shot['y'])-2),3)
        for b in w.beams:
            self.rect((255,242,164),(b['x']-camera-12,b['y']-3,26,6));self.rect(GOLD,(b['x']-camera-10,b['y']-1,23,2))
        self.rect((24,25,39),(0,0,960,70));self.rect(GOLD,(0,68,960,2));self.bat(25,18,2);self.text('RAT BAT',130,18,GOLD);self.text('DENNIS AS CHARLIE',130,42,MUTED,self.small)
        for i in range(3):
            x=365+i*33;color=(205,83,86) if i<p.hearts else (60,53,65)
            pygame.draw.polygon(self.screen,color,[(x,24),(x+7,19),(x+14,24),(x+21,19),(x+28,24),(x+28,32),(x+14,46),(x,32)])
        self.text(('DAYMAN  '+str(max(0,math.ceil(p.dayman)))+'s') if p.dayman else 'REHEARSAL  /  RAT BAT',520,27,GOLD)
        self.text('ESC PAUSE',810,28,MUTED,self.small)
        self.rect((24,25,39),(0,506,960,34));self.text('SPACE jump    J bat    K sunbeam    M mute    R retry audio',24,515,MUTED,self.small)
        if session.qa:self.text('QA · '+session.qa_label+(' · INVINCIBLE' if w.invincible else ''),22,79,(245,160,112),self.small)
    def curtains(self):
        for side in (0,840):
            for i in range(6):self.rect((88+i%2*22,29,43),(side+i*20,0,20,540))
        for x in range(0,960,80):pygame.draw.ellipse(self.screen,(115,37,50),(x-20,-60,120,120))
        pygame.draw.line(self.screen,GOLD,(0,56),(960,56),3)
    def panel(self,title):
        self.rect((20,23,38),(210,140,540,330));self.rect(GOLD,(210,140,540,330),2);self.center(title,160,GOLD,self.large)
    def draw(self,session,audio):
        if session.screen in ('training','pause','dead'):self.training(session)
        else:
            self.scenery(0);self.curtains()
            self.center('THE NIGHTMAN COMETH',82,GOLD,self.large)
            self.center('A MUSICAL PLATFORMER  ·  REHEARSAL',126,MUTED,self.small)
        if session.screen in ('title','pause','options','confirm','dead'):
            headings={'title':'ENTER THE THEATRE','pause':'TAKE FIVE','options':'OPTIONS','confirm':'START A NEW RUN?','dead':'CURTAIN CALL'}
            self.panel(headings[session.screen])
            for i,choice in enumerate(session.menu()):
                y=220+i*(27 if len(session.menu())>6 else 38)
                if session.screen=='options' and i<2:choice+='   < '+str(round(session.progress.settings[['music','effects'][i]]*100))+'% >'
                if i==session.selection:self.rect((64,61,67),(238,y-4,484,30))
                self.text(('> ' if i==session.selection else '  ')+choice,255,y,GOLD if i==session.selection else CREAM)
            self.center('UP / DOWN choose · ENTER confirm · ESC back',480,MUTED,self.small)
        elif session.screen=='password':
            self.panel('PASSWORD');self.center('QA destinations use rehearsal props.',220,MUTED);self.center(session.password+'_',270,GOLD,self.large)
            self.center(session.message or 'Type a code. Enter confirms. Esc returns.',350,CREAM,self.small)
        elif session.screen=='dialogue':
            self.panel(DIALOGUE[min(session.dialogue,2)][0]);self.portrait(DIALOGUE[min(session.dialogue,2)][0],245,235)
            words=DIALOGUE[min(session.dialogue,2)][1].split();lines=['']
            for word in words:
                if len(lines[-1])+len(word)>40:lines.append('')
                lines[-1]+=word+' '
            for i,line in enumerate(lines):self.text(line,315,240+i*30)
            self.center('ENTER next · ESC skip · Replay from the menu',430,MUTED,self.small)
        message=session.progress.message or session.message
        if audio.error:message='Audio unavailable · R retries · play can continue'
        elif audio.muted:message='MUTED · press M to restore audio'
        if message and session.screen!='password':
            self.rect((54,39,43),(10,478,940,26));self.text(message,20,482,(242,191,139),self.small)
        pygame.display.flip()
