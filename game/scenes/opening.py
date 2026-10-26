"""Approved opening, rendered as illustrations with exact game-owned dialogue."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Still:
    speaker: str
    text: str
    atlas: str
    panel: int
    music: str

OPENING=(
 Still('CHARLIE','Come ye of good faith one and all. So I may tell ye a tale of intrigue, and villainy. For ye see—','opening',0,'narration'),
 Still('DEE',"'For ye see'? Come on, Charlie, what's going on here?",'opening',1,'narration'),
 Still('CHARLIE','Absolutely nothing, Dee. Just a man trying to produce a musical.','opening',2,'narration'),
 Still('DEE','Whatever. Nobody writes a musical for no reason.','opening',1,'narration'),
 Still('CHARLIE','As I was saying, once a boy, then a Dayman, now complete with music and words I present: The Nightman Cometh','opening',3,'narration'),
 Still('THE NIGHTMAN COMETH','A musical by Charlie Kelly','opening',5,'title'),
 Still('DENNIS & DEE',"We're actors in Charlie's musical, what could go wrong?",'opening',4,'level1'),
 Still('CRICKET','Oooowoooooo','kidnapping',0,'level1'),
 Still('DEE','Den—er, Charlie! Cricket got into the dumpster behind Sherwin William again! Save me!','kidnapping',1,'level1'),
 Still('DENNIS',"Alright bird—I mean, Waitress. I'll save you!\nIf I have to…",'kidnapping',2,'level1'),
)
FRANK=(
 Still('DEE','Finally. Can we leave?','kidnapping',3,'frank-kidnap'),
 Still('FRANK','Not so fast. You gotta pay the troll toll.','kidnapping',4,'frank-kidnap'),
 Still('DENNIS','Seriously? We just did this.','kidnapping',5,'frank-kidnap'),
)
