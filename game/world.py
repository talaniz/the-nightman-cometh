"""Fixed-step training simulation. No pygame, storage, wall clock or audio dependency."""
from dataclasses import dataclass, asdict

DT=1/60
WIDTH=1800
FLOOR=430
FLAGS={'mid':400,'preboss':1400}
PLATFORMS=((0,430,1050,110),(1190,430,610,110),(690,340,130,18),(880,280,130,18),(1260,350,110,18))

def overlap(a,b):
    return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]

@dataclass
class Player:
    x:float=80
    y:float=386
    hearts:int=3
    dayman:float=0
    invulnerable:float=0
    facing:int=1
    vy:float=0
    grounded:bool=True
    swing:float=0
    beam_cooldown:float=0
    @property
    def rect(self):return (self.x,self.y,24,44)

class World:
    def __init__(self):
        self.player=Player();self.flags=set();self.checkpoint=80
        self.paused=False;self.dead=False;self.events=[];self.beams=[]
        self.invincible=False;self.accumulator=0;self.steps=0;self.swing_hits=set()
        self.reset_encounter()
    def reset_encounter(self):
        self.targets=[{'id':i,'x':x,'y':y,'alive':True} for i,(x,y) in enumerate(((520,398),(750,308),(930,248),(1520,398)))]
        self.pickups=[{'id':'food','kind':'cat-food','x':250,'y':412,'taken':False},
                      {'id':'meal','kind':'meal','x':640,'y':412,'taken':False}]
        self.beams=[];self.shots=[];self.shot_clock=0
    def flag(self,name,x):
        if name not in FLAGS or FLAGS[name]!=x:raise ValueError('Unknown checkpoint')
        # Activation and its heal are one-shot across death and save/reload.
        if name in self.flags:return
        self.flags.add(name);self.checkpoint=x
        self.player.hearts=min(3,self.player.hearts+1);self.events.append('checkpoint')
    def meal(self):self.player.dayman=10;self.events.append('meal')
    def food(self):self.player.hearts=min(3,self.player.hearts+1);self.events.append('cat-food')
    def hurt(self):
        p=self.player
        if self.dead or self.invincible or p.invulnerable>0:return
        p.hearts=max(0,p.hearts-1);p.invulnerable=1;self.events.append('hurt')
        if not p.hearts:self.dead=True
    def retry(self):
        self.player=Player(x=self.checkpoint);self.dead=False;self.paused=False
        self.events=[];self.accumulator=0;self.swing_hits=set();self.reset_encounter()
    def shoot(self):
        p=self.player
        if p.dayman<=0 or p.beam_cooldown>0 or self.paused or self.dead:return
        self.beams.append({'x':p.x+12+p.facing*18,'y':p.y+19,'dx':p.facing*600,'dy':0,'life':1.8})
        p.beam_cooldown=.25;self.events.append('beam')
    def contact(self,old_bottom,target_top,descending):
        return 'stomp' if descending and old_bottom<=target_top+1 else 'hurt'
    def attack(self):
        if self.paused or self.dead or self.player.swing>0:return
        self.player.swing=.22;self.swing_hits.clear();self.events.append('bat-swing')
    def advance(self,elapsed,inputs=None):
        if elapsed<0 or elapsed!=elapsed:raise ValueError('Invalid elapsed time')
        if self.paused or self.dead:self.accumulator=0;return
        # At most six simulation steps per frame. Hidden tabs pause instead of catching up.
        self.accumulator+=min(.1,elapsed)
        first=True
        while self.accumulator+1e-9>=DT:
            controls=dict(inputs or {})
            if not first:
                for action in ('jump','bat','beam'):controls[action]=False
            self.step(controls);self.accumulator=max(0,self.accumulator-DT);first=False
    def step(self,inputs=None):
        if self.paused or self.dead:return
        self.steps+=1;p=self.player;controls=inputs or {}
        for attr in ('dayman','invulnerable','swing','beam_cooldown'):setattr(p,attr,max(0,getattr(p,attr)-DT))
        direction=int(bool(controls.get('right')))-int(bool(controls.get('left')))
        if direction:p.facing=direction
        p.x=max(0,min(WIDTH-24,p.x+direction*220*DT))
        if controls.get('jump') and p.grounded:p.vy=-490;p.grounded=False;self.events.append('jump')
        if controls.get('bat'):self.attack()
        if controls.get('beam'):self.shoot()
        old_bottom=p.y+44;p.vy=min(800,p.vy+1300*DT);p.y+=p.vy*DT;p.grounded=False
        for x,y,w,h in PLATFORMS:
            if p.vy>=0 and p.x+24>x and p.x<x+w and old_bottom<=y+.01 and p.y+44>=y:
                p.y=y-44;p.vy=0;p.grounded=True;break
        if p.y>600:
            p.hearts=0;self.dead=True;self.events.append('hurt');return
        for name,x in FLAGS.items():
            if abs(p.x-x)<25 and p.y+44>=FLOOR-5:self.flag(name,x)
        for pickup in self.pickups:
            if not pickup['taken'] and overlap(p.rect,(pickup['x']-15,pickup['y']-13,30,26)):
                pickup['taken']=True
                self.meal() if pickup['kind']=='meal' else self.food()
        for target in self.targets:
            if not target['alive']:continue
            rect=(target['x'],target['y'],30,32)
            hitbox=(p.x+24 if p.facing>0 else p.x-42,p.y+7,42,27)
            if .04<p.swing<.18 and target['id'] not in self.swing_hits and overlap(hitbox,rect):
                self.swing_hits.add(target['id']);target['alive']=False;self.events.append('bat-hit');continue
            if overlap(p.rect,rect):
                if self.contact(old_bottom,target['y'],p.vy>0)=='stomp':
                    target['alive']=False;p.y=target['y']-44;p.vy=-350;self.events.append('stomp')
                else:self.hurt()
        self.shot_clock+=DT
        if self.shot_clock>=2:
            self.shot_clock=0
            if self.targets[-1]['alive']:self.shots.append({'x':1500.0,'y':410.0,'life':5.0})
        for shot in self.shots:
            shot['x']-=120*DT;shot['life']-=DT
            rect=(shot['x']-7,shot['y']-7,14,14)
            hitbox=(p.x+24 if p.facing>0 else p.x-42,p.y+7,42,27)
            if .04<p.swing<.18 and overlap(hitbox,rect):shot['life']=0;self.events.append('bat-hit')
            elif overlap(p.rect,rect):
                if self.contact(old_bottom,shot['y']-7,p.vy>0)=='stomp':p.vy=-350;self.events.append('stomp')
                else:self.hurt()
                shot['life']=0
            for beam in self.beams:
                if overlap((beam['x']-10,beam['y']-3,20,6),rect):shot['life']=0;beam['life']=0;self.events.append('bat-hit')
        self.shots=[shot for shot in self.shots if shot['life']>0]
        for beam in self.beams:
            beam['x']+=beam['dx']*DT;beam['life']-=DT
            for target in self.targets:
                if target['alive'] and overlap((beam['x']-10,beam['y']-3,20,6),(target['x'],target['y'],30,32)):
                    target['alive']=False;beam['life']=0;self.events.append('bat-hit');break
        self.beams=[b for b in self.beams if b['life']>0]
    def snapshot(self):
        return {'player':asdict(self.player),'flags':sorted(self.flags),'checkpoint':self.checkpoint,
                'dead':self.dead,'paused':self.paused,'targets':[dict(t) for t in self.targets],
                'beams':[dict(b) for b in self.beams],'shots':[dict(b) for b in self.shots],'steps':self.steps}
