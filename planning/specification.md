# Agreed game specification

## Outcome and runtime

A short three-level single-player side-scrolling browser game, Python with pygame-ce packaged by pygbag. Runs on desktop keyboard; a separately planned USB-controller milestone completes supported input. Philadelphia rendered as homemade stage scenery, retro Capcom NES gameplay readability with richer pixel portraits from the supplied title reference. No strict NES hardware restriction. Initial target play length 10–15 minutes is provisional and must be measured.

The user authorized proceeding with the plan on 2026-10-11. All four M1 preview melodies have user listening approval; integration/review is in progress and no executable game exists. The title image and generated mockups are concepts, not production sprites, collision geometry, frame budgets or evidence of a functioning game.

## Cast and visual contract

- Dennis plays Charlie: green shirt/dark pants, clean-shaven; white-and-gold Dayman when transformed.
- Actual Charlie is the director in gray suit/top hat, scruffy beard and natural eyes without eyeliner.
- Dee plays the Waitress in blouse/apron/blue skirt. The actual Waitress appears separately in the ending.
- Cricket wears a dog costume, with spray paint on his face after emerging from a dumpster behind Sherwin-Williams.
- Frank's Troll: pointier hooked nose inspired by DeVito's Penguin, round cheeks, wispy hair, squat hunched silhouette; warm skin, brown/moss robe, no monochrome/noir makeover.
- Mac's Nightman: black costume, pronounced black eye makeup.
- Ghouls: little green imp-like creatures, our interpretation of Charlie's description; not verified literal screen designs.
- Ground rats; occasional cooked chicken in denim shorts with wings for a telegraphed swoop; Duncan and Z/bridge crew; cartoon guns with legs that walk, pause and fire.
- Curtains open at stage beginning and close at stage end, not permanent gameplay borders. Painted brick flats, skyline, moon wire, stage supports and lighting maintain theatrical Philadelphia.
- Comic impact stars, brief neutral white damage flash, enemy tumble/puff; no gore. Foot stomps, not bat-pogo.
- Prominent detailed top HUD bat portrait labeled RAT BAT. Bat stays attached to hands through normal idle/run/jump/swing.
- Milksteak WITH jellybeans on ONE plate, one pickup/icon; never separate ingredient collection. Cat food is separate.
- In-world ads: Kitten Mittens with actual Charlie and mittened cat; Wolf Cola; Shadynasty's (jazz club, no invented bikes/boats subtitle); Fight Milk with Mac/Charlie and requested copy "THE ONLY DRINK BY BODYGUARDS FOR BODYGUARDS"; The Shotgun Shot; Dennis portrait with "REYNOLDS FOR COMPTROLLER", "SOUTH PHILLY", "ZONE 2", "DISTRICT 37". Distribute ads without hiding enemies/platforms or confusing pickups.

## Combat, health and progression

Move, jump, Rat Bat attack; descending onto ordinary enemies kills them and bounces Dennis. Side contact damages him. Dayman shoots ONE straight horizontal beam per shot from current firing height, never a fan/spread. Transform immediately on one combined meal; start at 10 seconds then tune against actual level length, damage does not cancel it. Timer pauses with game; retain default bat capability or reliable fallback so every boss is beatable without transformation.

Three hearts maximum. Cat food restores one heart. Mid-level and pre-boss FLAGS activate respawn checkpoints and restore ONE heart on first activation, capped at three. No repeated healing from recrossing. No automatic meal, stat upgrade or level-up at flags.

Unlimited retries accepted as planning default. Proposed deterministic respawn rule: restore three hearts, clear transient attacks/Dayman, return to last flag and reset encounter enemies; preserve activated flag IDs so re-crossing cannot farm health. Pause freezes simulation/timers/audio as appropriate; blur clears held inputs and pauses. Proposed jump assistance and damage-invulnerability timings are tuning details, not user commitments.

QA passwords PAINTDOG, TROLLTOLL, NIGHTMAN load respective level with standard health/bat. Explicit separate QA Dayman/invincibility/boss-checkpoint controls show QA status and do not mutate ordinary saved progress. Passwords are convenience tools, not security boundaries. Three final qualifying playthroughs cannot use them.

## Three acts

### Level 1 — coffee-shop rescue

Charlie is on his way to pick up the Waitress; Cricket kidnaps her and keeps her at the coffee shop. Approach contains rats, ghouls, occasional denim chicken and pickups. Boss arena contains Cricket only as hostile entity, player, Dee and props. Cricket charges back/forth; dodge until he hits a garbage can, becomes stunned, then hit or stomp him (Dayman beams also work in the stun window). No regular enemies in Cricket's boss arena.

After rescue, Frank kidnaps Dee in still-image dialogue, leading under the bridge. Exact short dialogue for this transition remains a phase-level script draft within the agreed plot.

### Level 2 — The Troll Toll

Underbridge platforms with Duncan/Z crew and walking guns; reserved visual references keep them distinct, not duplicated generic enemies. Frank boss shuffles forward/back while facing Dennis, inspired by NES Birdo. Throws sandwiches/hoagies STRAIGHT HORIZONTALLY, not arcs; telegraph and spacing permit reaction. Player can stomp, shoot or bat BOTH sandwiches and Frank. No pause-only immunity rule. Short post-hit invulnerability may prevent multiple hits from one contact. No other enemies during this boss.

After Frank falls, Nightman jumps down yelling "Confound your lousy toll, troll", grabs Dee and runs off. Still of Dennis watching and Dee shouting "Not again!"

### Level 3 — rooftop showdown

Cross staged Philadelphia rooftops/fire escapes with ordinary hazards and enemy approach encounters. Nightman boss uses telegraphed dash/leap/recovery (provisional tuning) and can summon green ghouls. This is the ONLY exception to ordinary boss-arena enemy exclusion: no rats, chickens, bridge crew or walking guns during Nightman. Cap simultaneous summons and provide recoverable attack openings. All bosses beatable using bat/stomp alone.

## Script and sequence

Still pixel-art scenes with speech bubbles, player-advanced and skippable with a reliable replay path. No requirement for actor voice synthesis.

1. Actual Charlie: "Come ye of good faith one and all. So I may tell ye a tale of intrigue, and villainy. For ye see—"
2. Dee: "'For ye see'? Come on, Charlie, what's going on here?"
3. Charlie: "Absolutely nothing, Dee. Just a man trying to produce a musical."
4. Skeptical Dee: "Whatever. Nobody writes a musical for no reason."
5. Charlie: "As I was saying, once a boy, then a Dayman, now complete with music and words I present: The Nightman Cometh" (emphasize "and words").
6. Title splash.
7. Dennis and Dee: "We're actors in Charlie's musical, what could go wrong?" with Tiny Boy music cue.
8. Dog-costumed paint-faced Cricket bursts from dumpster behind Sherwin-Williams: "Oooowoooooo", grabs Dee and carries her away.
9. Dee: "Den—er, Charlie! Cricket got into the dumpster behind Sherwin William again! Save me!" Preserve user's spoken singular William; storefront spelling is Sherwin-Williams.
10. Dennis watches them flee: "Alright bird—I mean, Waitress. I'll save you!" Smaller whisper: "If I have to…"
11. Level 1, Frank kidnapping, Level 2, Nightman abduction, Level 3.
12. After final rescue Charlie interrupts for his proposal song.
13. ACTUAL Waitress: "I'm not going to marry you, Charlie."
14. Charlie: "Well, see you tomorrow."
15. Dee: "I told you no one writes a musical for no reason!"
16. Charlie, hand low: "Dee, I'm right here right now"; hand high: "but I'm about to go here!"
17. End, then credits with Dayman. Proposal music ducks/stops for the final exchange;
    exact fade timing is an M2 listening decision. Do not omit the see-you-tomorrow beat.

## Audio contract

Four user-approved short instrumental previews establish the melodic baseline:
Dayman v2, Proposal v1, Little Baby Boy v1 and Troll Toll v2. Preserve their approved
notes/timing/timbres when making production arrangements; deliberate changes need
new listening approval. Automated checks establish preservation, not hearing.
The uploaded MIDI and approved Online Sequencer/Songsterr arrangements supplied
explicit notes after the first audio-extraction probe failed recognition.

See [music cue map](music-cue-map.md) for every approved placement and original-cue
assignment. M2 adds original Cricket, Frank and Nightman boss tracks, a rooftop
level track, and two kidnapping transitions. Broad high-energy retro arcade/NES
inspiration is allowed; compose new melodies for these tracks. Boss themes should
be faster and more urgent than approach music, with distinct identities.

Dayman transformation briefly overrides current music, then restores the current
scene's appropriate cue when it expires. User requested a slightly faster version;
1.10x tempo with unchanged pitch is a proposed first audition, not an approved value.
M1 establishes recognition; M2 creates full cues/loops/transitions and original SFX.
NES DuckTales informs an original springy stomp effect. Distinct jump/stomp/bat
hit/player damage/meal/cat food/checkpoint/sunbeam/sandwich/defeat sounds. Music and
SFX volumes separate; browser user gesture unlock; play remains possible muted or
if audio fails. User listening approval and actual browser audio evidence remain gates.

## Boundaries and acceptance

No mobile touch implementation, multiplayer, backend, database, accounts, analytics, paid mechanics, sprawling upgrade tree, actor voice cloning or production deployment in current plan execution. No invented extra game modes. Public release asset provenance/permissions are a release gate, not a reason to block planning.

Acceptance requires complete browser workflows including failure/recovery, actual-branch screenshots and headless inspections, per-commit independent code reviews, per-PR independent E2E, user-approved music, physical USB evidence, and three final complete playthroughs with no unresolved material user-visible defect. See verification.md.
