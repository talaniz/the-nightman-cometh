"""Rooftop traversal and bounded, telegraphed Nightman encounter."""
import math
from game.world import World, DT

class Act3(World):
    act='act3'
    launcher=False
    width=4850
    flag_positions={'mid':1600,'preboss':3850}
    platforms=((0,430,1100,110),(1172,430,1178,110),(2422,430,878,110),
               (650,360,160,18),(850,300,160,18),(1850,360,160,18),(2050,300,160,18),(2850,360,160,18),(3050,300,160,18),
               (3372,430,1478,110))
    arena_left=4010
    arena_right=4750

    def reset_encounter(self):
        self.complete=False;self.boss_active=False;self.next_id=1000;self.summon_clock=6.
        self.targets=[]
        for i,(kind,x,y) in enumerate((('rat',460,398),('ghoul',720,328),('rat',1320,398),
                                      ('ghoul',1790,398),('ghoul',2110,268),('rat',2690,398),('chicken',2210,150),('ghoul',3120,268),('rat',3600,398),('ghoul',3780,398))):
            self.targets.append(dict(id=i,kind=kind,x=float(x),y=float(y),home=float(x),alive=True,
                                     direction=1,state='waiting' if kind=='chicken' else 'patrol',timer=0.,animation_step=0))
        self.pickups=[dict(id='food1',kind='cat-food',x=960,y=412,taken=False),
                      dict(id='meal',kind='meal',x=1660,y=412,taken=False),
                      dict(id='food2',kind='cat-food',x=2870,y=412,taken=False)]
        self.beams=[];self.shots=[];self.shot_clock=0;self.impacts=[]

    def enter_boss(self):
        self.boss_active=True;self.beams=[];self.shots=[];self.swing_hits.clear();self.summon_clock=6.
        self.targets=[dict(id=100,kind='nightman',x=4530.,y=374.,alive=True,hp=6,immune=0.,
                           direction=-1,state='idle',timer=1.,turn=0,burst=0,remaining=0,vy=0.,animation_step=0)]
        self.events.append('boss-start')

    def summon(self):
        if not self.boss_active or self.complete or self.dead:return False
        living=[t for t in self.targets if t.get('summoned') and t['alive']]
        if len(living)>=2:return False
        # Only stable floor positions inside the arena; occupied/unsafe slots defer.
        candidates=[x for x in (4050,4220,4390,4560,4700)
                    if any(px<=x and x+30<=px+width and py==430 for px,py,width,height in self.platforms)
                    and abs(x-self.player.x)>=96 and all(abs(x-t['x'])>=40 for t in living)]
        if not candidates:return False
        x=max(candidates,key=lambda x:abs(x-self.player.x))
        self.targets.append(dict(id=self.next_id,kind='ghoul',x=float(x),y=398.,alive=True,
                                 home=float(x),direction=1,state='patrol',timer=0.,summoned=True,animation_step=0))
        self.next_id+=1
        return True

    def target_rect(self,target):
        return (target['x'],target['y'],32,56) if target['kind']=='nightman' else super().target_rect(target)

    def target_active(self,target):
        return target['alive'] and not (target['kind']=='chicken' and target['state'] in ('waiting','warning'))

    def contact_hurts(self,target):
        return target['kind']!='nightman' or target['state'] not in ('recover','summon')

    def hit_target(self,target,event):
        if target['kind']!='nightman':return super().hit_target(target,event)
        if not target['alive'] or target['immune']>0:return False
        target['hp']-=1;target['immune']=.75;self.events.append(event)
        self.impacts.append(dict(x=target['x']+16,y=target['y']+25,life=.25))
        if target['hp']==0:
            self.complete=True;target['state']='defeated'
            for other in self.targets:other['alive']=False
            self.shots=[];self.beams=[];self.events.append('defeat')
        return True

    def update_boss(self,b):
        b['immune']=max(0,b['immune']-DT);b['timer']-=DT
        state=b['state']
        if state in ('idle','recover') and b['timer']<=0:
            b['direction']=1 if self.player.x>b['x'] else -1
            if self.summon_clock<=0:
                b['state']='summon';b['timer']=.6
            else:
                b['state']='windup';b['timer']=.7
        elif state=='summon' and b['timer']<=0:
            self.summon();self.summon_clock=6.;b['state']='recover';b['timer']=.8
        elif state=='windup' and b['timer']<=0:
            b['turn']+=1
            b['state']='charge' if b['turn']%3==0 else 'leap' if b['turn']%3==2 else 'dash'
            b['timer']=.9 if b['state']=='charge' else .65
            if b['state']=='leap':b['vy']=-380.
        elif state in ('dash','leap'):
            b['x']=max(self.arena_left+30,min(self.arena_right-45,b['x']+b['direction']*210*DT))
            if state=='leap':
                b['vy']+=1100*DT;b['y']=min(374.,b['y']+b['vy']*DT)
            if b['timer']<=0 and b['y']>=374:
                b['state']='karate';b['timer']=.35;b['vy']=0
        elif state=='karate' and b['timer']<=0:
            b['state']='recover';b['timer']=.9
        elif state=='charge' and b['timer']<=0:
            # Direction is locked after the visible charge, never tracks mid-burst.
            b['direction']=1 if self.player.x>b['x'] else -1
            b['burst']+=1;b['remaining']=3 if b['burst']%2 else 2
            b['state']='fire';b['timer']=0.
        elif state=='fire' and b['timer']<=0:
            kind='crucifix' if b['burst']%2 else 'chimichanga'
            self.shots.append(dict(kind=kind,x=b['x']+16+b['direction']*38,
                                   y=405.,dx=b['direction']*230,life=3.))
            self.events.append('hoagie');b['remaining']-=1;b['timer']=.2
            if not b['remaining']:b['state']='recover';b['timer']=1.

    def update_approach(self,t):
        if t['kind']=='chicken':
            if t['state']=='waiting' and 1900<self.player.x<2500:
                t['state']='warning';t['timer']=1.2;t['x']=self.player.x+420
            elif t['state']=='warning':
                t['timer']-=DT
                if t['timer']<=0:t['state']='swoop';t['timer']=0
            elif t['state']=='swoop':
                t['timer']+=DT;t['x']-=210*DT;t['y']=150+240*math.sin(min(1,t['timer']/2.4)*math.pi)
                if t['timer']>=2.4:t['alive']=False
        else:
            if t.get('summoned'):
                t['direction']=1 if self.player.x>t['x'] else -1
                t['x']=max(self.arena_left,min(self.arena_right-30,t['x']+t['direction']*32*DT))
            else:
                t['x']+=t['direction']*(45 if t['kind']=='rat' else 27)*DT
                if abs(t['x']-t['home'])>40:t['direction']*=-1

    def step(self,inputs=None):
        if self.paused or self.dead or self.complete:return
        if self.player.x>=4000 and not self.boss_active:self.enter_boss()
        self.summon_clock=max(0,self.summon_clock-DT)
        for t in list(self.targets):
            if not t['alive']:continue
            t['animation_step']=self.steps
            if t['kind']=='nightman':self.update_boss(t)
            else:self.update_approach(t)
        super().step(inputs)
        if self.boss_active:self.player.x=max(self.arena_left,min(self.arena_right,self.player.x))
        if self.dead:
            for t in self.targets:
                if t.get('summoned'):t['alive']=False
            self.shots=[];self.beams=[]
        self.targets=[t for t in self.targets if not t.get('summoned') or t['alive']]

    def snapshot(self):
        result=super().snapshot();result.update(act=self.act,boss_active=self.boss_active,complete=self.complete)
        return result
