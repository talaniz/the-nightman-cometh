"""Bridge simulation; implemented against the milestone's behavior contracts."""
from game.world import World

class Act2(World):
    act='act2'
    launcher=False
    width=3600
    flag_positions={'mid':1500,'preboss':2800}
    platforms=((0,430,1000,110),(1072,430,1128,110),(2272,430,1328,110),
               (560,360,160,18),(760,300,160,18),(1740,360,160,18),(1940,300,160,18))

    def reset_encounter(self):
        self.complete=False;self.boss_active=False;self.next_id=1000
        self.targets=[]
        for i,(kind,x) in enumerate((('duncan',450),('gun',850),('z',1290),('gun',1810),('duncan',2420),('z',2630))):
            self.targets.append(dict(id=i,kind=kind,x=float(x),y=398.,home=float(x),alive=True,
                                     direction=-1,state='patrol',timer=1.,animation_step=0))
        self.pickups=[dict(id='food1',kind='cat-food',x=950,y=412,taken=False),
                      dict(id='meal',kind='meal',x=1560,y=412,taken=False),
                      dict(id='food2',kind='cat-food',x=2710,y=412,taken=False)]
        self.beams=[];self.shots=[];self.shot_clock=0;self.impacts=[]

    def enter_boss(self):
        self.boss_active=True;self.beams=[];self.shots=[];self.swing_hits.clear()
        self.targets=[dict(id=100,kind='frank',x=3310.,y=382.,alive=True,hp=5,
                           direction=-1,state='shuffle',timer=1.,immune=0.,animation_step=0)]
        self.events.append('boss-start')

    def target_rect(self,target):
        if target['kind']=='frank':return (target['x'],target['y'],38,48)
        if target['kind']=='sandwich':return (target['x'],target['y'],30,16)
        return super().target_rect(target)

    def hit_target(self,target,event):
        if target['kind']!='frank':return super().hit_target(target,event)
        if not target['alive'] or target['immune']>0:return False
        target['hp']-=1;target['immune']=.75;self.events.append(event)
        self.impacts.append(dict(x=target['x']+19,y=target['y']+20,life=.25))
        if target['hp']<=0:
            target['alive']=False;target['state']='defeated';self.complete=True
            for other in self.targets:
                if other['kind']=='sandwich':other['alive']=False
            self.shots=[];self.beams=[];self.events.append('defeat')
        return True

    def update_frank(self,target):
        from game.world import DT
        target['immune']=max(0,target['immune']-DT)
        target['direction']=1 if self.player.x>target['x'] else -1
        if target['state']=='shuffle':
            # Two short steps, forward then backward, before the readable windup.
            target['x']+=target['direction']*(22 if target['timer']>.55 else -22)*DT
            target['x']=max(3070,min(3430,target['x']))
            if target['timer']<=0:target['state']='windup';target['timer']=.85
        elif target['state']=='windup' and target['timer']<=0:
            target['state']='throw';target['timer']=.3
            self.targets.append(dict(id=self.next_id,kind='sandwich',x=target['x']+19+target['direction']*34,
                                     y=398.,alive=True,direction=target['direction'],state='flight',timer=3.,animation_step=0))
            self.next_id+=1;self.events.append('hoagie')
        elif target['state']=='throw' and target['timer']<=0:target['state']='recover';target['timer']=.6
        elif target['state']=='recover' and target['timer']<=0:target['state']='shuffle';target['timer']=1.1

    def step(self,inputs=None):
        from game.world import DT
        if self.paused or self.dead or self.complete:return
        if self.player.x>=2950 and not self.boss_active:self.enter_boss()
        for target in list(self.targets):
            if not target['alive']:continue
            target['animation_step']=self.steps
            target['timer']-=DT
            near=abs(self.player.x-target['x'])<380
            if target['kind']=='frank':self.update_frank(target)
            elif target['kind']=='sandwich':
                target['x']+=target['direction']*170*DT
                if target['timer']<=0 or not 2930<target['x']<3550:target['alive']=False
            elif target['kind']=='gun':
                if target['state']=='patrol':
                    target['x']+=target['direction']*24*DT
                    if abs(target['x']-target['home'])>35:target['direction']*=-1
                    if near and target['timer']<=0:
                        target['state']='windup';target['timer']=.9
                        target['direction']=1 if self.player.x>target['x'] else -1
                elif target['state']=='windup' and target['timer']<=0:
                    target['state']='recover';target['timer']=1.2
                    self.shots.append(dict(x=target['x']+15+target['direction']*24,y=410.,dx=target['direction']*150,life=2.8))
                elif target['state']=='recover' and target['timer']<=0:
                    target['state']='patrol';target['timer']=1.0
            else:
                if target['state']=='patrol':
                    target['x']+=target['direction']*32*DT
                    if abs(target['x']-target['home'])>42:target['direction']*=-1
                    if abs(self.player.x-target['x'])<90 and target['timer']<=0:
                        target['direction']=1 if self.player.x>target['x'] else -1
                        target['state']='windup';target['timer']=.65
                elif target['state']=='windup' and target['timer']<=0:
                    target['state']='lunge';target['timer']=.3
                elif target['state']=='lunge':
                    target['x']+=target['direction']*80*DT
                    if target['timer']<=0:target['state']='recover';target['timer']=.7
                elif target['state']=='recover' and target['timer']<=0:
                    target['state']='patrol';target['timer']=1.2
                target['x']=max(target['home']-70,min(target['home']+70,target['x']))
        super().step(inputs)
        if self.boss_active:self.player.x=max(2960,min(3520,self.player.x))
        self.targets=[t for t in self.targets if t['kind']!='sandwich' or t['alive']]

    def snapshot(self):
        result=super().snapshot()
        result.update(act=self.act,boss_active=self.boss_active,complete=self.complete)
        return result
