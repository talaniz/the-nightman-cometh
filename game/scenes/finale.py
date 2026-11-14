"""Player-paced proposal lyrics and the approved closing exchange."""
from game.scenes.opening import Still

# Each supplied line is a separate readable page, including repeated vocalizations.
# Only the approved instrumental plays; these are never synthesized vocals.
PROPOSAL_LYRICS = (
    'ah ah ah ah ah ah ah ah',
    'ah ah ah ah ah ah ah ah',
    'ah ah ah ah ah ah ah ooh',
    'oo oo oo oooh',
    'I was that little boy that little',
    'baby boy was meee',
    'I once was a boy but',
    'now I am a Man',
    'I fought the nightman lived as dayman',
    "Now I'm here to ask for your hand",
    'so if you want to marry man,',
    'will you marry me?',
    "Won't you come on stage and join me?",
    'In this thing called matrimony?',
    'Please say yes and do not bone me',
    'please just marry',
    'Me!',
)

FINALE = (
    Still('DENNIS', 'I was a boy, now I am…', 'transformation', 0, 'ending'),
    Still('DENNIS', '', 'transformation', 0, 'ending', effect='dayman'),
    Still('DENNIS', 'The Dayman!', 'transformation', 1, 'ending'),
    *(Still('CHARLIE', line, 'transformation' if i<9 else 'finale',
            2 if i<9 else 1, 'proposal') for i,line in enumerate(PROPOSAL_LYRICS)),
    Still('WAITRESS', 'You said if I came to the show, you’d leave me alone. So, no….',
          'finale', 2, 'dialogue-silence'),
    Still('CHARLIE', 'Well, technically I didn’t sign anything', 'transformation', 3, 'dialogue-silence'),
    Still('CHARLIE', 'So, I guess I’ll see you tomorrow?…', 'finale', 3, 'dialogue-silence'),
    Still('DEE', 'I told you no one writes a musical for no reason!', 'finale', 4, 'dialogue-silence'),
    Still('CHARLIE', 'Dee, I’m right here right now…', 'finale', 5, 'dialogue-silence'),
    Still('CHARLIE', '…but I’m about to go here!', 'finale', 6, 'dialogue-silence'),
)
