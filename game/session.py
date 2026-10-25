"""Keyboard menu and progress coordination; explicit QA/normal state separation."""
from game.world import World
from game.progress import Progress

CODES={'PAINTDOG':'Coffee-shop rehearsal','TROLLTOLL':'Bridge rehearsal','NIGHTMAN':'Rooftop rehearsal'}
DIALOGUE=(('CHARLIE','Welcome to rehearsal. Tonight: a tale of intrigue and villainy.'),
          ('DEE','These are practice props, Charlie. Where is the coffee shop?'),
          ('CHARLIE','Next act. First, learn the Rat Bat. Then we make theatre history.'))

class Session:
    def __init__(self,storage):
        self.progress=Progress(storage);self.progress.load();self.world=World();self.progress.restore(self.world)
        self.screen='title';self.selection=0;self.return_screen='title';self.qa=False;self.qa_label=''
        self.normal_world=None;self.password='';self.message='';self.dialogue=0;self.replaying=False
    def menu(self):
        if self.screen=='title':return ['Start new rehearsal']+(['Continue rehearsal'] if self.progress.saved else [])+['Options','Password','Replay dialogue']
        if self.screen=='pause':return ['Resume','Options','Replay dialogue']+(['QA Dayman','QA invincibility','QA checkpoint','Exit QA'] if self.qa else [])+['Title']
        if self.screen=='options':return ['Music','Effects','Back']
        if self.screen=='confirm':return ['Keep current progress','Start fresh']
        if self.screen=='dead':return ['Retry checkpoint','Title']
        return []
    def enter_screen(self,screen):self.screen=screen;self.selection=0;self.world.paused=screen!='training'
    def select(self,direction):
        options=self.menu()
        if options:self.selection=(self.selection+direction)%len(options)
    def start(self,fresh=True):
        if fresh:
            self.world=World();self.qa=False;self.qa_label='';self.normal_world=None
            self.progress.save(self.world)
        self.dialogue=0;self.replaying=False;self.enter_screen('dialogue')
    def activate(self):
        if self.screen=='dialogue':self.next_dialogue();return
        if self.screen=='password':self.submit_password();return
        options=self.menu()
        if not options:return
        choice=options[self.selection]
        if choice=='Start new rehearsal':
            self.enter_screen('confirm') if self.progress.saved else self.start()
        elif choice=='Start fresh':self.start()
        elif choice=='Keep current progress':self.enter_screen('title')
        elif choice=='Continue rehearsal':self.enter_screen('training')
        elif choice=='Resume':self.enter_screen('training')
        elif choice=='Options':self.return_screen=self.screen;self.enter_screen('options')
        elif choice=='Back':self.enter_screen(self.return_screen)
        elif choice=='Password':self.password='';self.message='';self.enter_screen('password')
        elif choice=='Replay dialogue':
            self.return_screen=self.screen;self.dialogue=0;self.replaying=True;self.enter_screen('dialogue')
        elif choice=='Retry checkpoint':self.world.retry();self.enter_screen('training')
        elif choice=='Title':self.enter_screen('title')
        elif choice=='QA Dayman':self.world.meal();self.enter_screen('training')
        elif choice=='QA invincibility':self.world.invincible=not self.world.invincible;self.enter_screen('training')
        elif choice=='QA checkpoint':self.world.flag('preboss',1400);self.world.retry();self.enter_screen('training')
        elif choice=='Exit QA':
            self.world=self.normal_world or World();self.normal_world=None;self.qa=False;self.qa_label='';self.enter_screen('title')
    def adjust(self,direction):
        if self.screen=='options' and self.selection<2:
            name=['music','effects'][self.selection]
            self.progress.settings[name]=round(max(0,min(1,self.progress.settings[name]+direction*.1)),1)
            self.progress.save(self.world,qa=self.qa)
    def submit_password(self):
        code=self.password.strip().upper()
        if code not in CODES:self.message='Unknown password. Try again or press Esc.';return
        if not self.qa:self.normal_world=self.world
        self.world=World();self.qa=True;self.qa_label=CODES[code];self.message='';self.enter_screen('training')
    def next_dialogue(self,skip=False):
        self.dialogue+=1
        if skip or self.dialogue>=len(DIALOGUE):self.enter_screen(self.return_screen if self.replaying else 'training')
    def back(self):
        if self.screen=='training':self.enter_screen('pause')
        elif self.screen=='pause':self.enter_screen('training')
        elif self.screen=='dialogue':self.next_dialogue(skip=True)
        elif self.screen=='options':self.enter_screen(self.return_screen)
        elif self.screen in ('password','confirm'):self.enter_screen('title')
    def blur(self):
        if self.screen=='training':self.enter_screen('pause')
    def update(self,dt,controls):
        if self.screen!='training':return
        self.world.advance(dt,controls)
        if 'checkpoint' in self.world.events:self.progress.save(self.world,qa=self.qa)
        if self.world.dead:self.enter_screen('dead')
