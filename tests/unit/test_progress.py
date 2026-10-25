from game.progress import Progress
from game.world import World
class Memory:
    def __init__(self,raw=None,broken=False):self.raw=raw;self.broken=broken;self.writes=0
    def read(self):
        if self.broken:raise OSError('storage disabled')
        return self.raw
    def write(self,value):
        if self.broken:raise OSError('quota')
        self.raw=value;self.writes+=1

def test_corrupt_and_unavailable_storage_are_recoverable():
    for store in (Memory('{bad'),Memory(broken=True),Memory('"wrong type"')):
        p=Progress(store);assert p.load() is None;assert p.message
        p.save(World());assert p.saved is not None

def test_qa_cannot_write_ordinary_progress():
    store=Memory();p=Progress(store);p.save(World());before=store.raw
    w=World();w.flag('preboss',1400);p.save(w,qa=True)
    assert store.raw==before and store.writes==1

def test_roundtrip_preserves_flags_and_settings():
    store=Memory();p=Progress(store);w=World();w.flag('mid',400);p.settings['music']=.3;p.save(w)
    q=Progress(store);q.load();assert q.settings['music']==.3 and q.saved['flags']==['mid']

def test_invalid_save_does_not_create_bogus_progress():
    for raw in ('{"v":99}', '{"v":1,"checkpoint":"elsewhere","flags":[]}', 'x'*17000):
        assert Progress(Memory(raw)).load() is None
