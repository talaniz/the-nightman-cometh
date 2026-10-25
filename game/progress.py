"""Bounded, versioned local progress with in-memory fallback and QA isolation."""
import json
import math
from game.world import FLAGS

class Progress:
    def __init__(self,storage):
        self.storage=storage;self.message='';self.saved=None;self.settings={'music':.7,'effects':.7}
    def load(self):
        try:
            raw=self.storage.read()
            if not raw:return None
            if not isinstance(raw,str) or len(raw)>16384:raise ValueError('oversized save')
            data=json.loads(raw)
            if not isinstance(data,dict) or type(data.get('v'))!=int or data.get('v')!=1:raise ValueError('save version')
            checkpoint=data.get('checkpoint');flags=data.get('flags');settings=data.get('settings')
            if type(checkpoint)!=int or checkpoint not in (80,*FLAGS.values()):raise ValueError('checkpoint')
            if not isinstance(flags,list) or len(flags)>2 or any(not isinstance(f,str) or f not in FLAGS for f in flags) or len(set(flags))!=len(flags):raise ValueError('flags')
            if checkpoint!=80 and checkpoint not in [FLAGS[f] for f in flags]:raise ValueError('unactivated checkpoint')
            if not isinstance(settings,dict) or set(settings)!={'music','effects'}:raise ValueError('settings')
            for value in settings.values():
                if type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<=1:raise ValueError('volume')
            self.saved=data;self.settings=dict(settings)
        except Exception:
            # Storage/browser bridges can raise platform-specific exceptions at this boundary.
            self.saved=None;self.message='Save unavailable. You can play; progress stays in this session.'
        return self.saved
    def save(self,world,qa=False):
        if qa:return False
        self.saved={'v':1,'checkpoint':world.checkpoint,'flags':sorted(world.flags),'settings':dict(self.settings)}
        try:self.storage.write(json.dumps(self.saved));return True
        except Exception:
            self.message='Saving unavailable. Progress stays in this session.';return False
    def restore(self,world):
        if self.saved:
            world.checkpoint=self.saved['checkpoint'];world.flags=set(self.saved['flags']);world.retry()
