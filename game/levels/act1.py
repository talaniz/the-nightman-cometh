"""Coffee-shop route. Shared combat remains in the deterministic world model."""
from game.world import World

class Act1(World):
    act='act1'
    width=4200
    flag_positions={'mid':1700,'preboss':3350}
    platforms=((0,430,1050,110),(1122,430,1378,110),(2572,430,1628,110),
               (690,360,150,18),(890,300,150,18),(2050,360,170,18),(2290,300,170,18),
               (2820,350,160,18))
    launcher=False

    def reset_encounter(self):
        self.boss_active=False;self.complete=False;self.chicken_clock=0
        self.targets=[]
        for i,(kind,x,y) in enumerate((('rat',580,398),('ghoul',780,328),('rat',1440,398),
                    ('ghoul',1990,398),('ghoul',2340,268),('rat',2860,318),('chicken',2200,160))):
            self.targets.append(dict(id=i,kind=kind,x=float(x),y=float(y),home=x,alive=True,
                                     direction=1,state='waiting' if kind=='chicken' else 'patrol',timer=0))
        self.pickups=[dict(id='food1',kind='cat-food',x=900,y=412,taken=False),
                      dict(id='meal',kind='meal',x=1810,y=412,taken=False),
                      dict(id='food2',kind='cat-food',x=3080,y=412,taken=False)]
        self.beams=[];self.shots=[];self.shot_clock=0;self.impacts=[]

    def enter_boss(self):
        self.boss_active=True;self.beams=[];self.shots=[];self.swing_hits.clear()
        self.targets=[dict(id=100,kind='cricket',x=3900.,y=398.,alive=True,hp=3,
                           state='warning',timer=.75,direction=-1)]
        self.events.append('boss-start')

    def contact_hurts(self,target):
        return target["kind"]!="cricket" or target["state"] not in ("stunned","recover")

    def target_active(self,target):
        return target["alive"] and not (target["kind"]=="chicken" and target["state"] in ("waiting","warning"))

    def hit_target(self,target,event):
        if target['kind']!='cricket':return super().hit_target(target,event)
        if target['state']!='stunned':return False
        target['hp']-=1;self.events.append(event)
        self.impacts.append(dict(x=target['x']+15,y=target['y']+16,life=.25))
        if target['hp']<=0:
            target['alive']=False;target['state']='defeated';self.complete=True
            self.events.append('defeat')
        else:target['state']='recover';target['timer']=.65
        return True

    def step(self,inputs=None):
        from game.world import DT
        if self.paused or self.dead or self.complete:return
        if self.player.x>=3500 and not self.boss_active:self.enter_boss()
        for target in self.targets:
            if not target['alive']:continue
            target['animation_step']=self.steps
            kind=target['kind']
            if kind=='cricket':
                target['timer']-=DT
                if target['state'] in ('warning','recover') and target['timer']<=0:
                    if target['state']=='recover':target['state']='warning';target['timer']=.75
                    else:target['state']='charge'
                elif target['state']=='charge':
                    target['x']+=target['direction']*300*DT
                    if target['x']<=3540 or target['x']>=4050:
                        target['x']=max(3540,min(4050,target['x']))
                        target['state']='stunned';target['timer']=1.5
                        target['direction']*=-1;self.events.append('bat-hit')
                elif target['state']=='stunned' and target['timer']<=0:
                    target['state']='warning';target['timer']=.75
            elif kind=='chicken':
                if target['state']=='waiting' and 1800<self.player.x<2500:
                    target['state']='warning';target['timer']=1.2;target['x']=self.player.x+480
                elif target['state']=='warning':
                    target['timer']-=DT
                    if target['timer']<=0:target['state']='swoop';target['timer']=0
                elif target['state']=='swoop':
                    import math
                    target['timer']+=DT;target['x']-=210*DT
                    target['y']=160+230*math.sin(min(1,target['timer']/2.4)*math.pi)
                    if target['timer']>=2.4:target['alive']=False
            else:
                target['x']+=target['direction']*(45 if kind=='rat' else 27)*DT
                if abs(target['x']-target['home'])>45:target['direction']*=-1
        super().step(inputs)
        if self.boss_active:self.player.x=max(3510,min(4110,self.player.x))

    def snapshot(self):
        result=super().snapshot()
        result.update(act=self.act,boss_active=self.boss_active,complete=self.complete)
        return result
