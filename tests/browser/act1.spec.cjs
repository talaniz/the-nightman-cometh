const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),path=require('node:path');
const evidence=process.env.NIGHTMAN_EVIDENCE;
const state=async p=>JSON.parse(await p.evaluate(()=>window.__nightmanGame));
async function press(p,key,ms=120){await p.keyboard.press(key);await p.waitForTimeout(ms);}
async function boot(p){await p.goto('/');await expect(p.locator('#boot-action')).toBeEnabled({timeout:120000});await p.locator('#boot-action').click();await p.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await p.locator('#canvas').focus();}
async function choose(p,label){let s=await state(p);let i=s.menu.indexOf(label);expect(i).toBeGreaterThanOrEqual(0);for(let n=0;n<(i-s.selection+s.menu.length)%s.menu.length;n++)await press(p,'ArrowDown',30);await press(p,'Enter');}
async function capture(p,name){if(!evidence)return;fs.mkdirSync(evidence,{recursive:true});await p.screenshot({path:path.join(evidence,name+'.png')});fs.writeFileSync(path.join(evidence,name+'.json'),JSON.stringify({viewport:p.viewportSize(),browser:p.context().browser().version(),project:test.info().project.name,test:test.info().title,build:process.env.NIGHTMAN_BUILD,state_after_capture:true,state:await state(p)},null,2));}
async function fixture(p,name){await p.evaluate(name=>window.__nightmanFixture=JSON.stringify({name}),name);await p.waitForTimeout(160);}
function errors(p){const list=[];p.on('pageerror',e=>list.push(String(e)));p.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))list.push(m.text())});p.on('requestfailed',r=>list.push(r.url()));return list;}

test('STORY ACT1 exact sequence art audio and skip replay',async({page})=>{
 const faults=errors(page);await boot(page);await choose(page,'Start Act 1');
 const speakers=['CHARLIE','DEE','CHARLIE','DEE','CHARLIE','THE NIGHTMAN COMETH','DENNIS & DEE','CRICKET','DEE','DENNIS'];
 for(let i=0;i<speakers.length;i++){
  const s=await state(page);expect(s.story.speaker).toBe(speakers[i]);expect(s.dialogue).toBe(i);
  expect(s.audio.playing).toBe(i<5?'proposal':i===5?'dayman':'little-boy');
  await capture(page,'opening-'+i);await press(page,'Enter');
 }
 expect((await state(page)).world.act).toBe('act1');expect((await state(page)).screen).toBe('training');
 const save=await page.evaluate(()=>localStorage.getItem('nightman.progress.v1'));
 await press(page,'Escape');await choose(page,'Replay dialogue');await press(page,'Escape');
 expect((await state(page)).screen).toBe('pause');expect(await page.evaluate(()=>localStorage.getItem('nightman.progress.v1'))).toBe(save);
 expect(faults).toEqual([]);
});

test('ACT1 CRICKET state fixtures attacks recovery and evidence',async({page})=>{
 const faults=errors(page);await boot(page);expect((await state(page)).test_build).toBe(true);
 for(const name of ['approach','chicken','meal','mid','preboss','death']){
  await fixture(page,'act1-'+name);await capture(page,'act1-'+name);
  if(name==='approach'){
   await page.keyboard.down('ArrowRight');await page.waitForTimeout(180);await capture(page,'act1-running');await page.keyboard.up('ArrowRight');
   await fixture(page,'act1-pose-jump');await capture(page,'act1-jump-pose');await fixture(page,'act1-pose-bat');await capture(page,'act1-bat-pose');await fixture(page,'act1-pose-hurt');await capture(page,'act1-damage-pose');
  }
  if(name==='mid'){
   await page.keyboard.down('ArrowRight');await page.waitForTimeout(220);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.hearts).toBe(2);await capture(page,'act1-flag-first');
   await page.keyboard.down('ArrowLeft');await page.waitForTimeout(220);await page.keyboard.up('ArrowLeft');await page.keyboard.down('ArrowRight');await page.waitForTimeout(220);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.hearts).toBe(2);await capture(page,'act1-flag-repeat');
   await page.keyboard.down('ArrowLeft');await page.waitForTimeout(650);await page.keyboard.up('ArrowLeft');await capture(page,'wolf-cola');}
  if(name==='death'){await press(page,'Enter');expect((await state(page)).world.checkpoint).toBe(3350);await capture(page,'act1-retry');}
 }
 await fixture(page,'act1-pose-boss-warning');let s=await state(page);expect(s.world.targets.map(t=>t.kind)).toEqual(['cricket']);expect(s.audio.playing).toBe('cricket-boss');await capture(page,'cricket-warning');
 await fixture(page,'act1-pose-boss-charge');await capture(page,'cricket-charge');
 await fixture(page,'act1-pose-boss-stunned');await capture(page,'cricket-stunned');await fixture(page,'act1-boss-stunned');await press(page,'j');
 expect((await state(page)).world.targets[0].hp).toBe(2);await capture(page,'cricket-hit');
 await fixture(page,'act1-boss-stunned');await page.keyboard.press('k');expect((await state(page)).world.beams).toEqual([]);
 await fixture(page,'act1-pose-boss-defeated');await capture(page,'cricket-defeated');
 for(let i=0;i<3;i++){await fixture(page,'act1-frank-'+i);expect((await state(page)).audio.playing).toBe('frank-kidnap');await capture(page,'frank-'+i);}
 await press(page,'Escape');expect((await state(page)).screen).toBe('complete');await capture(page,'act1-complete');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'act1-complete-1920');await page.setViewportSize({width:390,height:844});await capture(page,'act1-narrow');
 expect(faults).toEqual([]);
});

test('ACT1 BEAM transformed sprite and horizontal shot',async({page})=>{
 const faults=errors(page);await boot(page);await fixture(page,'act1-preboss');await press(page,'Escape');await choose(page,'QA Dayman');await press(page,'k',40);
 const beams=(await state(page)).world.beams;expect(beams.length).toBe(1);expect(beams[0].dy).toBe(0);
 await capture(page,'act1-beam');
 await fixture(page,'act1-preboss');await page.keyboard.down('ArrowLeft');await page.waitForTimeout(1800);await page.keyboard.up('ArrowLeft');
 expect((await state(page)).screen).toBe('training');await capture(page,'act1-shadynastys');expect(faults).toEqual([]);
});

test('SAVE ACT1 legacy migration keeps volumes and resets coordinates',async({page})=>{
 await page.addInitScript(()=>localStorage.setItem('nightman.progress.v1',JSON.stringify({v:1,checkpoint:1400,flags:['preboss'],settings:{music:.3,effects:.6}})));
 await boot(page);let s=await state(page);expect(s.settings).toEqual({music:.3,effects:.6});expect(s.world.checkpoint).toBe(80);expect(s.world.flags).toEqual([]);expect(s.message).toContain('Rehearsal');await capture(page,'save-migrated');
});

// Ordinary full route uses only keyboard actions and read-only observations.
// No test fixtures, passwords, invincibility or skipped story states.
for(const recovery of [false,true])test('ACT1_NORMAL '+(recovery?'death checkpoint reload recovery':'full keyboard rescue and safe end of preview'),async({page})=>{
 test.setTimeout(420000);const faults=errors(page);await boot(page);expect((await state(page)).test_build).toBe(false);await choose(page,'Start Act 1');
 while((await state(page)).screen==='dialogue')await press(page,'Enter',70);
 let held='';let deaths=0;let forcedRecovery=false;
 // A read-count cap runs out sooner on faster hosts despite ongoing gameplay.
 // Bound elapsed route time instead; success still requires the full rescue.
 const routeDeadline=Date.now()+180000;
 while(Date.now()<routeDeadline){
  let s=await state(page),w=s.world,p=w.player;
  if(s.screen==='dialogue'||s.screen==='complete')break;
  if(recovery&&!forcedRecovery&&w.boss_active){
   if(held)await page.keyboard.up(held);held='';
   await page.keyboard.down('ArrowRight');await page.waitForTimeout(650);await page.keyboard.up('ArrowRight');
   await expect.poll(async()=>(await state(page)).screen,{timeout:45000}).toBe('dead');
   await capture(page,'normal-death');await press(page,'Enter');
   let retry=await state(page);expect(retry.world.player.hearts).toBe(3);expect(retry.world.player.dayman).toBe(0);expect(retry.world.checkpoint).toBe(3350);await capture(page,'normal-retry');
   await page.evaluate(()=>window.onbeforeunload=null);await page.goto('about:blank');await boot(page);await choose(page,'Continue Act 1');
   let restored=await state(page);expect(restored.world.checkpoint).toBe(3350);expect(restored.world.flags).toContain('preboss');forcedRecovery=true;continue;
  }
  if(s.screen==='dead'){deaths++;expect(deaths).toBeLessThan(5);await page.keyboard.up('ArrowLeft');await page.keyboard.up('ArrowRight');await press(page,'Enter');held='';continue;}
  // Stop before approaching a pit: driver round trips on the Pi can exceed400ms.
  // Keyboard pulses and a stationary read avoid walking off while awaiting observations.
  const edge=[1050,2500].find(edge=>edge-p.x>0&&edge-p.x<300);
  if(!w.boss_active&&edge&&p.grounded){
   if(held){await page.keyboard.up(held);held='';}
   p=(await state(page)).world.player;
   if(edge-p.x<85){
    await Promise.all([page.keyboard.down('ArrowRight'),page.keyboard.press('Space')]);
    await page.waitForTimeout(750);await page.keyboard.up('ArrowRight');
   }else await page.keyboard.press('ArrowRight',{delay:60});
   continue;
  }
  if(w.boss_active){
   // Camp beside the left can. Chasing the opposite stun window takes longer
   // than the window itself; release movement before IPC/readback can overshoot.
   if(held){await page.keyboard.up(held);held='';continue;}
   const b=w.targets[0],distance=p.x-3598;
   if(Math.abs(distance)>14){
    await page.keyboard.press(distance>0?'ArrowLeft':'ArrowRight',{delay:Math.min(180,Math.abs(distance)/220*1000)});continue;
   }
   // Jump within the flight window, rather than early enough to land before contact.
   const incoming=b.state==='charge'&&b.direction<0&&b.x-p.x>0&&b.x-p.x<140;
   const leaving=b.state==='warning'&&b.direction>0&&b.x<3600&&b.timer<.45;
   if(p.grounded&&(incoming||leaving))await page.keyboard.press('Space');
   if(b.state==='stunned'&&b.x<3600){
    if(p.facing>0)await page.keyboard.press('ArrowLeft',{delay:25});
    await page.keyboard.press('j');
   }
   await page.waitForTimeout(50);continue;
  }
  const direction='ArrowRight',bat=true;
  const jump=p.grounded&&([1050,2500].some(edge=>edge-p.x>0&&edge-p.x<70)||w.targets.some(t=>t.alive&&t.x-p.x>0&&t.x-p.x<110&&Math.abs(t.y-p.y)<65));
  if(direction!==held){if(held)await page.keyboard.up(held);if(direction)await page.keyboard.down(direction);held=direction;}
  if(jump)await page.keyboard.press('Space');if(bat)await page.keyboard.press('j');
  await page.waitForTimeout(50);
 }
 if(held)await page.keyboard.up(held);
 expect((await state(page)).screen).toBe('dialogue');expect((await state(page)).world.complete).toBe(true);
 for(let i=0;i<3;i++)await press(page,'Enter');
 expect((await state(page)).screen).toBe('complete');await capture(page,'normal-complete');
 const saved=JSON.parse(await page.evaluate(()=>localStorage.getItem('nightman.progress.v1')));expect(saved.complete).toBe(true);expect(saved.flags).toContain('preboss');if(recovery)expect(forcedRecovery).toBe(true);expect(faults).toEqual([]);
 await page.evaluate(()=>window.onbeforeunload=null);await page.goto('about:blank');await boot(page);await choose(page,'Continue Act 1');expect((await state(page)).screen).toBe('complete');
});
