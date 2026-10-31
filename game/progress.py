"""Validated local progress; old rehearsal coordinates never become story progress."""
import json
import math
from game.world import FLAGS
from game.levels.act1 import Act1
from game.levels.act2 import Act2

class Progress:
    def __init__(self,storage):
        self.storage=storage;self.message='';self.saved=None
        self.settings={'music':.7,'effects':.7}

    def load(self):
        try:
            raw=self.storage.read()
            if not raw:return None
            if not isinstance(raw,str) or len(raw)>16384:raise ValueError('oversized save')
            data=json.loads(raw)
            if not isinstance(data,dict) or type(data.get('v'))!=int or data['v'] not in (1,2):raise ValueError('save version')
            settings=data.get('settings')
            if not isinstance(settings,dict) or set(settings)!={'music','effects'}:raise ValueError('settings')
            for value in settings.values():
                if type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<=1:raise ValueError('volume')
            stage=data.get('stage','rehearsal') if data['v']==2 else 'rehearsal'
            if stage not in ('act1','act2','rehearsal'):raise ValueError('unknown stage')
            positions={'act1':Act1.flag_positions,'act2':Act2.flag_positions,'rehearsal':FLAGS}[stage]
            checkpoint=data.get('checkpoint');flags=data.get('flags')
            if type(checkpoint)!=int or checkpoint not in (80,*positions.values()):raise ValueError('checkpoint')
            if not isinstance(flags,list) or len(flags)>2 or any(not isinstance(f,str) or f not in positions for f in flags) or len(set(flags))!=len(flags):raise ValueError('flags')
            if checkpoint!=80 and checkpoint not in [positions[f] for f in flags]:raise ValueError('unactivated checkpoint')
            complete=data.get('complete',False)
            if type(complete)!=bool or (complete and stage not in ('act1','act2')):raise ValueError('completion')
            self.settings=dict(settings)
            if data['v']==1:
                data=dict(v=2,stage='act1',checkpoint=80,flags=[],complete=False,settings=dict(settings))
                self.message='Rehearsal settings kept. Your Act 1 adventure starts here.'
                # Persist the migration once; storage failure still permits in-memory play.
                try:self.storage.write(json.dumps(data))
                except Exception:self.message+=' Saving unavailable.'
            self.saved=data
        except Exception:
            self.saved=None;self.message='Save unavailable. You can play; progress stays in this session.'
        return self.saved

    def save(self,world,qa=False):
        if qa:return False
        completed=bool(getattr(world,'complete',False)) or bool(self.saved and self.saved.get('stage')==world.act and self.saved.get('complete'))
        self.saved=dict(v=2,stage=world.act,checkpoint=world.checkpoint,flags=sorted(world.flags),
                        complete=completed,settings=dict(self.settings))
        try:self.storage.write(json.dumps(self.saved));return True
        except Exception:
            self.message='Saving unavailable. Progress stays in this session.';return False

    def restore(self,world):
        if self.saved and self.saved.get('stage')==world.act:
            world.checkpoint=self.saved['checkpoint'];world.flags=set(self.saved['flags']);world.retry()
            if world.act in ('act1','act2'):world.complete=self.saved.get('complete',False)
