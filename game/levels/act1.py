"""Coffee-shop route. Shared combat remains in the deterministic world model."""
from game.world import World

class Act1(World):
    act='act1'
    width=5100
    flag_positions={'mid':1700,'preboss':4250}
    platforms=((0,430,1050,110),(1122,430,1378,110),(2572,430,1028,110),
               (690,360,150,18),(890,300,150,18),(2050,360,170,18),(2290,300,170,18),
               (2820,350,160,18),(3230,360,160,18),(3430,300,160,18),
               (3672,430,1428,110))
    launcher=False

    def reset_encounter(self):
        self.boss_active=False;self.complete=False;self.chicken_clock=0
        self.targets=[]
        for i,(kind,x,y) in enumerate((('rat',580,398),('ghoul',780,328),('rat',1440,398),
                    ('ghoul',1990,398),('ghoul',2340,268),('rat',2860,318),('chicken',2200,160),('rat',3310,328),('ghoul',3820,398),('rat',4030,398))):
            self.targets.append(dict(id=i,kind=kind,x=float(x),y=float(y),home=x,alive=True,
                                     direction=1,state='waiting' if kind=='chicken' else 'patrol',timer=0))
        self.pickups=[dict(id='food1',kind='cat-food',x=900,y=412,taken=False),
                      dict(id='meal',kind='meal',x=1810,y=412,taken=False),
                      dict(id='food2',kind='cat-food',x=3080,y=412,taken=False)]
        self.beams=[];self.shots=[];self.shot_clock=0;self.impacts=[]

    def enter_boss(self):
        self.boss_active=True;self.beams=[];self.shots=[];self.swing_hits.clear()
        self.targets=[dict(id=100,kind='cricket',x=4800.,y=398.,alive=True,hp=3,
                           state='warning',timer=.75,direction=-1,charge_count=0,
                           charge_elapsed=0.,feinted=False)]
        self.events.append('boss-start')

    def contact_hurts(self,target):
        return target["kind"]!="cricket" or target["state"] not in ("stunned","recover","brake")

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
        if self.player.x>=4400 and not self.boss_active:self.enter_boss()
        for target in self.targets:
            if not target['alive']:continue
            target['animation_step']=self.steps
            kind=target['kind']
            if kind=='cricket':
                target['timer']-=DT
                if target['state'] in ('warning','recover') and target['timer']<=0:
                    if target['state']=='recover':target['state']='warning';target['timer']=.75
                    else:
                        target['state']='charge'
                        target['charge_count']+=1
                        target['charge_elapsed']=0.
                        target['feinted']=False
                elif target['state']=='charge':
                    target['x']+=target['direction']*300*DT
                    target['charge_elapsed']+=DT
                    if target['x']<=4440 or target['x']>=4950:
                        target['x']=max(4440,min(4950,target['x']))
                        target['state']='stunned';target['timer']=1.5
                        target['direction']*=-1;self.events.append('bat-hit')
                    elif (target['charge_count']%2==1 and not target['feinted']
                          and target['charge_elapsed']>=.55):
                        # One stationary, harmless tell on alternating charges.
                        # Never track/reverse continuously: every cycle has a crash.
                        target['state']='brake';target['timer']=.4
                        target['feinted']=True
                elif target['state']=='brake' and target['timer']<=0:
                    target['direction']*=-1;target['state']='charge'
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
        if self.boss_active:self.player.x=max(4440,min(4956,self.player.x))

    def snapshot(self):
        result=super().snapshot()
        result.update(act=self.act,boss_active=self.boss_active,complete=self.complete)
        return result
