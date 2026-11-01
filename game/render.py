"""Code-native pixel scenery and representative rehearsal sprites."""
import math
import pygame
from game.world import FLAGS, PLATFORMS, WIDTH
from game.art import Art

INK=(15,18,32);GOLD=(231,185,87);CREAM=(238,227,199);MUTED=(166,174,192)

class Renderer:
    def __init__(self,screen):
        self.screen=screen;self.art=Art()
        self.item_font=pygame.font.Font(None,16);self.font=pygame.font.Font(None,25);self.small=pygame.font.Font(None,21);self.large=pygame.font.Font(None,48)
    def text(self,text,x,y,color=CREAM,font=None):
        self.screen.blit((font or self.font).render(text,False,color),(int(x),int(y)))
    def dialogue_width(self,text):
        parts=text.split('—')
        dash_width=max(12,self.font.size('M')[0])+6
        return sum(self.font.size(part)[0] for part in parts)+(len(parts)-1)*dash_width
    def dialogue_image(self,text):
        # Web runtime fonts can give em dashes overhanging ink. Keep authored
        # punctuation, but reserve a separate cell and paint its pixel stroke.
        if '—' not in text:return self.font.render(text,False,INK)
        dash_width=max(12,self.font.size('M')[0])+6
        parts=text.split('—')
        runs=[self.font.render(part,False,INK) for part in parts]
        height=max(run.get_height() for run in runs)
        image=pygame.Surface((self.dialogue_width(text),height),pygame.SRCALPHA)
        x=0
        for index,(part,rendered) in enumerate(zip(parts,runs)):
            if index:
                pygame.draw.line(image,INK,(x+3,height//2),(x+dash_width-4,height//2),2)
                x+=dash_width
            image.blit(rendered,(x,0));x+=self.font.size(part)[0]
        return image
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
        w=session.world;p=w.player;camera=max(0,min(w.width-960,p.x-350));self.act_scenery(w,camera) if w.act in ("act1","act2") else self.scenery(camera)
        for name,x in w.flag_positions.items():
            color=(126,202,139) if name in w.flags else GOLD
            pygame.draw.polygon(self.screen,color,[(x-camera+2,362),(x-camera+35,371),(x-camera+2,382)])
        for t in w.targets:
            if t['alive']:
                x=t['x']-camera;y=t['y']
                if w.act in ('act1','act2'):
                    self.enemy(t,camera);continue
                self.rect((123,65,63),(x,y,30,32));self.rect((199,139,83),(x+4,y+4,22,24))
                pygame.draw.circle(self.screen,(91,43,44),(int(x)+15,int(y)+15),9,2);pygame.draw.circle(self.screen,CREAM,(int(x)+15,int(y)+15),3)
                self.rect((67,47,42),(x+11,y+29,8,4))
        for item in w.pickups:
            if item['taken']:continue
            x=item['x']-camera;y=item['y']
            if item['kind']=='meal' and w.act in ('act1','act2'):
                self.screen.blit(self.art.image('cast',15,(44,25)),(int(x-22),int(y-15)));continue
            if item['kind']=='meal':
                pygame.draw.ellipse(self.screen,CREAM,(x-18,y-6,38,12));pygame.draw.ellipse(self.screen,(142,75,64),(x-12,y-10,20,12))
                for dx,c in ((10,(177,211,117)),(15,GOLD),(6,(191,99,143))):pygame.draw.circle(self.screen,c,(int(x+dx),int(y-5)),3)
            else:
                self.rect((122,159,173),(x-14,y-15,28,22));self.rect(CREAM,(x-14,y-10,28,12));self.text('CAT',x-11,y-10,INK,self.item_font)
        if w.act in ('act1','act2') or not (p.invulnerable>0 and int(p.invulnerable*12)%2):self.actor(p,camera,w.steps) if w.act in ('act1','act2') else self.person(p.x-camera,p.y,p.dayman>0,p.facing,p.swing>0,w.steps*.22 if p.grounded else 0)
        for impact in w.impacts:
            x=int(impact['x']-camera);y=int(impact['y']);radius=int(5+impact['life']*30)
            for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
                pygame.draw.line(self.screen,CREAM,(x-dx*radius,y-dy*radius),(x+dx*radius,y+dy*radius),2)
        for shot in w.shots:
            pygame.draw.circle(self.screen,(207,98,76),(int(shot['x']-camera),int(shot['y'])),7)
            pygame.draw.circle(self.screen,GOLD,(int(shot['x']-camera)-2,int(shot['y'])-2),3)
        for b in w.beams:
            self.rect((255,242,164),(b['x']-camera-12,b['y']-3,26,6));self.rect(GOLD,(b['x']-camera-10,b['y']-1,23,2))
        self.rect((24,25,39),(0,0,960,70));self.rect(GOLD,(0,68,960,2));self.screen.blit(self.art.asset('sprites/nail-bat.png',(96,30),trim=True),(20,14)) if w.act in ('act1','act2') else self.bat(25,18,2);self.text('RAT BAT',130,18,GOLD);self.text('DENNIS AS CHARLIE',130,42,MUTED,self.small)
        for i in range(3):
            x=365+i*33;color=(205,83,86) if i<p.hearts else (60,53,65)
            pygame.draw.polygon(self.screen,color,[(x,24),(x+7,19),(x+14,24),(x+21,19),(x+28,24),(x+28,32),(x+14,46),(x,32)])
        self.text(('DAYMAN  '+str(max(0,math.ceil(p.dayman)))+'s') if p.dayman else ({'act1':'COFFEE-SHOP RESCUE','act2':'THE TROLL TOLL'}.get(w.act,'REHEARSAL / RAT BAT')),520,27,GOLD)
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
            self.screen.blit(self.art.image('opening',5,(960,540)),(0,0));self.curtains()
            self.center('THE NIGHTMAN COMETH',82,GOLD,self.large)
            self.center('ACTS I–II  ·  A MUSICAL ADVENTURE',126,MUTED,self.small)
        if session.screen in ('title','pause','options','confirm','dead','complete'):
            headings={'title':'ENTER THE THEATRE','pause':'TAKE FIVE','options':'OPTIONS','confirm':'START A NEW RUN?','dead':'CURTAIN CALL','complete':'ACT 2 COMPLETE' if session.world.act=='act2' else 'ACT 1 COMPLETE'}
            self.panel(headings[session.screen])
            if session.screen=='complete':self.center('End of preview · Rooftops come next.' if session.world.act=='act2' else 'Under the bridge comes next.',195,MUTED,self.small)
            for i,choice in enumerate(session.menu()):
                y=220+i*(27 if len(session.menu())>6 else 38)
                if session.screen=='options' and i<2:choice+='   < '+str(round(session.progress.settings[['music','effects'][i]]*100))+'% >'
                if i==session.selection:self.rect((64,61,67),(238,y-4,484,30))
                self.text(('> ' if i==session.selection else '  ')+choice,255,y,GOLD if i==session.selection else CREAM)
            self.center('UP / DOWN choose · ENTER confirm · ESC back',480,MUTED,self.small)
        elif session.screen=='password':
            self.panel('PASSWORD');self.center('PAINTDOG: Act 1 · TROLLTOLL: Act 2',220,MUTED);self.center(session.password+'_',270,GOLD,self.large)
            self.center(session.message or 'Type a code. Enter confirms. Esc returns.',350,CREAM,self.small)
        elif session.screen=='dialogue':
            self.story(session)
        message=session.progress.message or session.message
        if audio.error:message='Audio unavailable · R retries · play can continue'
        elif audio.muted:message='MUTED · press M to restore audio'
        if message and session.screen!='password':
            self.rect((54,39,43),(10,478,940,26));self.text(message,20,482,(242,191,139),self.small)
        pygame.display.flip()

    def story(self,session):
        still=session.sequence[min(session.dialogue,len(session.sequence)-1)]
        self.screen.fill(INK)
        self.screen.blit(self.art.image(still.atlas,still.panel,(960,420)),(0,0))
        self.rect(CREAM,(24,368,912,140));self.rect(GOLD,(24,368,912,140),3)
        pygame.draw.polygon(self.screen,CREAM,[(110,370),(140,342),(157,370)])
        self.text(still.speaker,43,380,(104,58,28),self.small)
        body,_,whisper=still.text.partition('\n')
        words=body.split();lines=['']
        for word in words:
            candidate=(lines[-1]+' '+word).strip()
            if self.dialogue_width(candidate)>866:lines.append(word)
            else:lines[-1]=candidate
        for i,line in enumerate(lines):
            self.screen.blit(self.dialogue_image(line),(43,405+i*26))
            if 'and words' in line:
                left=43+self.font.size(line.split('and words')[0])[0]
                pygame.draw.line(self.screen,(130,78,28),(left,428+i*26),(left+self.font.size('and words')[0],428+i*26),2)
        if whisper:self.text(whisper,43,410+len(lines)*26,(87,80,69),self.small)
        self.center('ENTER next    ESC skip    Replay from the menu',519,MUTED,self.small)

    def actor(self,p,camera,steps):
        if p.swing:
            # Match existing .22s swing: windup >.18, active strike .18..04, recovery <.04.
            pose=0 if p.swing>=.18 else (1 if p.swing>.04 else 2)
            frame=pose+(3 if p.dayman else 0)
            sprite=self.art.sequence('sprites/bat-attack.png',frame,3,2,(92,92),p.facing<0)
            anchor=(48,40,40)[pose]
            if p.facing<0:anchor=92-anchor
            self.screen.blit(sprite,(int(p.x-camera+12-anchor),int(p.y+44-90)))
            return
        moving=getattr(p,'moving',False)
        frame=3 if not p.grounded else (1+(steps//8)%2 if moving else 0)
        if p.dayman:frame+=4
        sprite=self.art.image('cast',frame,(40,64),p.facing<0)
        if p.invulnerable and int(p.invulnerable*12)%2:
            sprite=sprite.copy();sprite.fill((180,180,180,0),special_flags=pygame.BLEND_RGB_ADD)
        self.screen.blit(sprite,(int(p.x-camera-8),int(p.y-20)))
        # Per-pose hand anchors keep the bat attached to the atlas animation.
        hand_x,hand_y=((23,17),(29,3),(29,3),(29,-8))[frame%4]
        bat_x=p.x-camera+hand_x if p.facing>0 else p.x-camera+24-hand_x-43
        bat=self.art.asset('sprites/nail-bat.png',(43,13),trim=True)
        if p.facing<0:bat=pygame.transform.flip(bat,True,False)
        self.screen.blit(bat,(int(bat_x),int(p.y+hand_y)))

    def enemy(self,t,camera):
        if t['kind'] in ('duncan','z','gun','frank','sandwich'):
            self.bridge_enemy(t,camera);return
        if t['kind'] in ('rat','ghoul'):
            row=0 if t['kind']=='rat' else 1
            frame=(t.get('animation_step',0)//8)%4+row*4
            size=(44,23) if row==0 else (38,42)
            sprite=self.art.sequence('sprites/enemy-walk.png',frame,4,2,size,t.get('direction',1)<0,trim_row=True)
            self.screen.blit(sprite,(int(t['x']-camera+(30-size[0])/2),int(t['y']+32-size[1])))
            return
        index={'rat':8,'ghoul':9,'chicken':10,'cricket':11}[t['kind']]
        if t['kind']=='cricket' and t['state'] in ('stunned','defeated'):index=12
        size=(44,48) if t['kind']=='cricket' else (38,36)
        if t['kind']=='chicken' and t['state']=='waiting':return
        if t['state']=='warning':self.text('!',t['x']-camera+12,t['y']-26,GOLD,self.large)
        if t['state']=='stunned':self.text('* * *',t['x']-camera-7,t['y']-30,GOLD)
        self.screen.blit(self.art.image('cast',index,size,(t.get('direction',1)>0 if t['kind']=='cricket' else t.get('direction',1)<0)),(int(t['x']-camera-5),int(t['y']+32-size[1])))
        if t['kind']=='cricket':
            self.text('CRICKET',675,83,GOLD)
            for i in range(t['hp']):self.rect((204,86,78),(790+i*27,84,20,12))

    def act_scenery(self,w,camera):
        if w.act=='act2':self.bridge_scenery(w,camera);return
        if not hasattr(self,'stage_backdrop'):
            source=pygame.image.load(str(self.art.root/'backgrounds/act1/street.png')).convert()
            self.stage_backdrop=pygame.transform.scale(source,(1350,450))
        self.screen.blit(self.stage_backdrop,(-int(camera*390/(w.width-960)),70))
        # Foreground brick flats and readable collision surfaces, independent of painted backdrop.
        for x,y,width,height in w.platforms:
            self.rect((82,51,43),(x-camera,y,width,height));self.rect((184,126,69),(x-camera,y,width,6))
            for yy in range(y+16,min(506,y+height),18):
                pygame.draw.line(self.screen,(47,35,36),(x-camera,yy),(x+width-camera,yy),2)
                for xx in range(x,x+width,44):self.rect((47,35,36),(xx-camera+(22 if yy%36 else 0),yy-16,2,16))
        for x,label in ((1700,'MIDPOINT'),(3350,'PRE-BOSS')):
            pygame.draw.line(self.screen,CREAM,(x-camera,430),(x-camera,360),3)
            self.text(label,x-camera-40,447,GOLD,self.small)
        # Storefront fascia shares the painted flat's parallax, not the camera/HUD layer.
        offset=int(camera*390/(w.width-960))
        self.screen.blit(self.art.asset('ui/sherwin-sign.png',(294,48)),(48-offset,244))
        # Ads are mounted above the playable lane; physical posts and braces locate them in the set.
        for x,top,asset in ((410,75,'kitten-billboard.png'),(1290,75,'wolf-billboard.png')):
            sx=x-camera;width=250;height=166
            for dx in (22,width-22):
                self.rect((37,33,33),(sx+dx,top+height,7,430-top-height))
                self.rect((109,85,57),(sx+dx,top+height,2,430-top-height))
            pygame.draw.line(self.screen,(64,51,40),(sx+22,top+height+35),(sx+width-22,top+height+65),4)
            self.screen.blit(self.art.asset('ui/'+asset,(width,height)),(int(sx),top))
        # Existing later-route venue remains an enamel mounted sign, not a floating HUD label.
        sx=2730-camera
        self.rect((58,38,35),(sx,220,220,105));self.rect((174,129,69),(sx+4,224,212,97),3)
        lettering=pygame.font.Font(None,31).render("SHADYNASTY'S",False,(232,205,151))
        self.screen.blit(lettering,(int(sx+(220-lettering.get_width())/2),240))
        self.text('JAZZ CLUB',sx+67,282,(190,160,107),self.small)
        if w.boss_active:
            for x in (3530,4090):
                self.rect((116,135,137),(x-camera,393,34,37))
                for rib in (5,12,20,27):self.rect((65,85,91),(x-camera+rib,397,2,29))
                pygame.draw.ellipse(self.screen,(184,193,185),(int(x-camera-3),388,40,10))
                self.rect((218,218,193),(x-camera+10,385,14,4))
            self.screen.blit(self.art.image('cast',13,(38,62)),(4140-camera,368))

    def bridge_enemy(self,t,camera):
        x=t['x']-camera;y=t['y'];kind=t['kind']
        if kind=='sandwich':
            pygame.draw.ellipse(self.screen,(231,176,91),(x,y,30,7))
            self.rect((99,145,62),(x+1,y+6,28,3));self.rect((170,66,48),(x+2,y+9,26,3))
            pygame.draw.ellipse(self.screen,(203,139,67),(x,y+11,30,5));return
        row={'duncan':0,'z':1,'gun':2,'frank':3}[kind]
        state=t['state'];step=t.get('animation_step',0)
        if kind=='frank':pose=2 if state=='windup' else 3 if state=='throw' else (step//10)%2 if state=='shuffle' else 0
        elif kind=='gun':pose=3 if state=='recover' and t['timer']>1.1 else 0 if state in ('windup','recover') else 1+(step//9)%2
        else:pose=3 if state=='lunge' else 0 if state in ('windup','recover') else 1+(step//9)%2
        size=(76,62) if kind=='frank' else (68,43) if kind=='gun' else (66,59)
        sprite=self.art.sequence('sprites/bridge.png',row*4+pose,4,4,size,t['direction']<0,trim_row=True)
        if t.get('immune',0)>0 and int(t['immune']*14)%2:
            sprite=sprite.copy();sprite.fill((100,100,100,0),special_flags=pygame.BLEND_RGB_ADD)
        height=48 if kind=='frank' else 32
        self.screen.blit(sprite,(int(x+15-size[0]/2),int(y+height-size[1])))
        if state=='windup':self.text('!',x+9,y-35,GOLD,self.large)
        if kind=='frank':
            self.text('FRANK / TROLL',640,83,GOLD)
            for i in range(t['hp']):self.rect((204,86,78),(805+i*25,84,18,12))

    def bridge_scenery(self,w,camera):
        self.screen.fill(INK)
        backdrop=self.art.asset('backgrounds/act2/bridge.png',(1320,440))
        self.screen.blit(backdrop,(-int(camera*360/(w.width-960)),70))
        # Solid collision geometry is foreground wood decking, distinct from scenery.
        for x,y,width,height in w.platforms:
            self.rect((68,53,43),(x-camera,y,width,height));self.rect((193,151,89),(x-camera,y,width,6))
            for xx in range(x,x+width,42):
                self.rect((32,31,33),(xx-camera,y+6,2,min(height-6,76)))
            if height<30:
                for xx in (x+14,x+width-20):
                    pygame.draw.line(self.screen,(78,80,75),(xx-camera,y+height),(xx-camera-12,y+height+22),4)
        for name,x in w.flag_positions.items():
            pygame.draw.line(self.screen,CREAM,(x-camera,430),(x-camera,360),3)
            self.text('MIDPOINT' if name=='mid' else 'PRE-BOSS',x-camera-40,447,GOLD,self.small)
        for x,ad in ((180,0),(1190,1),(2320,2)):
            sx=x-camera;top=98;width=246;height=164
            for dx in (16,width-20):
                self.rect((43,40,37),(sx+dx,top+height,6,430-top-height))
            pygame.draw.line(self.screen,(117,92,62),(sx+16,top+height+18),(sx+width-20,top+height+58),4)
            asset=self.art.asset('ui/wolf-billboard.png',(width,height)) if ad==2 else self.art.sequence('ui/bridge-ads.png',ad,2,1,(width,height))
            self.screen.blit(asset,(int(sx),top))
        if w.boss_active:
            self.text('TROLL CROSSING',3190-camera,250,GOLD,self.small)
            self.screen.blit(self.art.image('cast',13,(38,62)),(3540-camera,368))
