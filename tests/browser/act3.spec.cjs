const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),path=require('node:path');
const state=async p=>JSON.parse(await p.evaluate(()=>window.__nightmanGame));
async function boot(p){await p.goto('/');await expect(p.locator('#boot-action')).toBeEnabled({timeout:120000});await p.locator('#boot-action').click();await p.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await p.locator('#canvas').focus();}
let fixtureId=1000;
async function fixture(p,name){const id=++fixtureId;await p.evaluate(req=>window.__nightmanFixture=JSON.stringify(req),{name:'act3-'+name,id});await p.waitForFunction(id=>JSON.parse(window.__nightmanGame).fixture_id===id,id,{timeout:30000});}
async function capture(p,name){const dir=process.env.NIGHTMAN_EVIDENCE;if(!dir)return;fs.mkdirSync(dir,{recursive:true});await p.screenshot({path:path.join(dir,name+'.png')});fs.writeFileSync(path.join(dir,name+'.json'),JSON.stringify({viewport:p.viewportSize(),state:await state(p),build:process.env.NIGHTMAN_BUILD},null,2));}
function errors(p){const list=[];p.on('pageerror',e=>list.push(String(e)));p.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))list.push(m.text());});p.on('requestfailed',r=>list.push(r.url()));return list;}
async function pressUntil(p,key,check){await p.keyboard.down(key);try{await expect.poll(check,{timeout:15000,intervals:[50]}).toBe(true);}finally{await p.keyboard.up(key);}}

// Release movement before each browser round trip near a platform edge.
async function walkTo(p,x){
 const deadline=Date.now()+15000;
 while(Date.now()<deadline){
  const current=(await state(p)).world.player.x;
  if(current>=x)return;
  await p.keyboard.press('ArrowRight',{delay:Math.min(60,Math.max(16,(x-current)/220*1000))});
 }
 expect((await state(p)).world.player.x).toBeGreaterThanOrEqual(x);
}

test('ACT3_APPROACH platforms ads meal flags pause retry',async({page})=>{
 const faults=errors(page);await boot(page);await fixture(page,'approach');
 expect((await state(page)).audio.playing).toBe('rooftop');await capture(page,'rooftop-entrance');
 for(const start of ['first','second']){
  await fixture(page,'platform-'+start);const x=start==='first'?650:1850;
  await page.keyboard.press('Space');await expect.poll(async()=>{const p=(await state(page)).world.player;return p.grounded&&p.y===316;},{timeout:10000}).toBe(true);await capture(page,'rooftop-lower-'+start);
  await walkTo(page,x+110);
  await Promise.all([page.keyboard.down('Space'),page.keyboard.down('ArrowRight')]);
  try{await page.waitForTimeout(400);}
  finally{await Promise.all([page.keyboard.up('ArrowRight'),page.keyboard.up('Space')]);}
  await expect.poll(async()=>{const p=(await state(page)).world.player;return p.grounded&&p.y===256;},{timeout:10000}).toBe(true);await capture(page,'rooftop-upper-'+start);
 }
 for(const name of ['poster','mid','preboss','meal','death']){
  await fixture(page,name);
  if(['mid','preboss','meal'].includes(name))await pressUntil(page,'ArrowRight',async()=>{const w=(await state(page)).world;return name==='meal'?w.player.dayman>0:w.flags.includes(name);});
  if(['mid','preboss'].includes(name))expect((await state(page)).world.player.hearts).toBe(2);
  if(name==='meal')expect((await state(page)).audio.playing).toBe('dayman-fast');
  await capture(page,'rooftop-'+name);
  if(name==='death'){await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).world.player.hearts).toBe(3);await capture(page,'rooftop-retry');}
 }
 await fixture(page,'poster');await page.keyboard.press('Escape');await expect.poll(async()=>(await state(page)).screen).toBe('pause');
 const before=(await state(page)).world;await page.waitForTimeout(200);expect((await state(page)).world).toEqual(before);await capture(page,'rooftop-pause');
 await page.keyboard.press('Escape');await page.setViewportSize({width:1920,height:1080});await capture(page,'rooftop-1920');await page.setViewportSize({width:390,height:844});await capture(page,'rooftop-narrow');expect(faults).toEqual([]);
});

test('NIGHTMAN_BOSS collision attacks expiry and arena exclusion',async({page})=>{
 const faults=errors(page);await boot(page);
 for(const [name,key] of [['close','j'],['stomp',null],['beam','k']]){
  await fixture(page,'boss-'+name);if(key)await page.keyboard.press(key);
  await expect.poll(async()=>(await state(page)).world.targets[0].hp).toBe(7);await capture(page,'nightman-'+name);
 }
 await fixture(page,'boss-expiry');await expect.poll(async()=>(await state(page)).audio.playing,{timeout:10000}).toBe('nightman-boss');
 expect((await state(page)).world.player.dayman).toBe(0);await capture(page,'nightman-expiry');
 expect((await state(page)).world.targets.every(t=>t.kind==='nightman'||t.summoned)).toBe(true);expect(faults).toEqual([]);
});

test('ACT3_MOTION live boss telegraphs and capped summons',async({page})=>{
 const faults=errors(page);await boot(page);await fixture(page,'boss-summons');
 await page.evaluate(()=>{
  window.__nightmanMotion={frames:{},max:0,active:true};
  const sample=()=>{
   const log=window.__nightmanMotion;if(!log.active)return;
   const s=JSON.parse(window.__nightmanGame),w=s.world,b=w.targets.find(t=>t.kind==='nightman');
   log.max=Math.max(log.max,w.targets.filter(t=>t.summoned&&t.alive).length);
   const c=document.querySelector('#canvas'),camera=Math.max(0,Math.min(4850-960,w.player.x-350));
   if(b&&!log.frames[b.state]){
    const crop=document.createElement('canvas');crop.width=130;crop.height=140;
    crop.getContext('2d').drawImage(c,(b.x-camera-45)*c.width/960,(b.y-50)*c.height/540,130*c.width/960,140*c.height/540,0,0,130,140);
    log.frames[b.state]={png:crop.toDataURL('image/png'),state:b};
   }requestAnimationFrame(sample);
  };requestAnimationFrame(sample);
 });
 await expect.poll(async()=>Object.keys(await page.evaluate(()=>window.__nightmanMotion.frames)),{timeout:35000}).toEqual(expect.arrayContaining(['windup','dash','leap','recover','summon']));
 await expect.poll(async()=>await page.evaluate(()=>window.__nightmanMotion.max),{timeout:35000}).toBe(2);
 await page.waitForTimeout(7000);expect(await page.evaluate(()=>window.__nightmanMotion.max)).toBe(2);await capture(page,'nightman-summons');
 const frames=await page.evaluate(()=>{window.__nightmanMotion.active=false;return window.__nightmanMotion.frames;});
 const dir=process.env.NIGHTMAN_EVIDENCE;
 if(dir)for(const [key,value] of Object.entries(frames)){
  fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'nightman-motion-'+key+'.png'),Buffer.from(value.png.split(',')[1],'base64'));
  fs.writeFileSync(path.join(dir,'nightman-motion-'+key+'.json'),JSON.stringify({viewport:page.viewportSize(),state:value.state,kind:'live browser canvas crop',build:process.env.NIGHTMAN_BUILD},null,2));
 }
 expect(faults).toEqual([]);
});

test('FINALE exact dialogue and approved credits survive retry completion and replay',async({page})=>{
 const faults=errors(page);await boot(page);
 const lines=[
  'I was a boy, now I am…','','The Dayman!',
  'ah ah ah ah ah ah ah ah','ah ah ah ah ah ah ah ah','ah ah ah ah ah ah ah ooh','oo oo oo oooh',
  'I was that little boy that little','baby boy was meee','I once was a boy but','now I am a Man',
  'I fought the nightman lived as dayman',"Now I'm here to ask for your hand",'so if you want to marry man,',
  'will you marry me?',"Won't you come on stage and join me?",'In this thing called matrimony?',
  'Please say yes and do not bone me','please just marry','Me!',
  'You said if I came to the show, you’d leave me alone. So, no….','Well, technically I didn’t sign anything','So, I guess I’ll see you tomorrow?…',
  'I told you no one writes a musical for no reason!','Dee, I’m right here right now…','…but I’m about to go here!'];
 for(let i=0;i<lines.length;i++){
  await fixture(page,'finale-'+i);expect((await state(page)).story.text).toBe(lines[i]);
  expect((await state(page)).audio.playing).toBe(i<3?'dayman':i<20?'proposal':null);
  await capture(page,'finale-'+i);
 }
 await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).screen).toBe('credits');
 expect((await state(page)).audio.playing).toBe('sunny-credits');
 await expect.poll(async()=>(await state(page)).audio.music_busy).toBe(1);await capture(page,'musical-credits');
 await page.keyboard.press('m');await expect.poll(async()=>(await state(page)).audio.gains[0]).toBe(0);await capture(page,'credits-muted');
 await page.keyboard.press('m');await expect.poll(async()=>(await state(page)).audio.gains[0]).toBeGreaterThan(0);
 const errorId=++fixtureId;
 await page.evaluate(id=>window.__nightmanFixture=JSON.stringify({name:'audio-error',id}),errorId);
 await page.waitForFunction(id=>JSON.parse(window.__nightmanGame).fixture_id===id,errorId);
 expect((await state(page)).audio.error).toContain('Audio unavailable');await capture(page,'credits-audio-error');
 await page.keyboard.press('r');await expect.poll(async()=>(await state(page)).audio.error).toBe('');
 await expect.poll(async()=>(await state(page)).audio.music_busy).toBe(1);await capture(page,'credits-recovered');
 await expect.poll(async()=>(await state(page)).audio.music_busy,{timeout:70000,intervals:[500]}).toBe(0);
 expect((await state(page)).screen).toBe('credits');await capture(page,'credits-finished');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'credits-1920');
 await page.setViewportSize({width:390,height:844});await capture(page,'credits-narrow');
 await page.setViewportSize({width:1280,height:720});
 await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).screen).toBe('dialogue');await page.keyboard.press('Escape');await expect.poll(async()=>(await state(page)).screen).toBe('credits');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'ending-1920');await page.setViewportSize({width:390,height:844});await capture(page,'ending-narrow');expect(faults).toEqual([]);
});

test('ACT3_SAVE old completed bridge resumes rooftop with settings preserved',async({page})=>{
 await page.addInitScript(()=>localStorage.setItem('nightman.progress.v1',JSON.stringify({v:2,stage:'act2',checkpoint:2800,flags:['mid','preboss'],complete:true,settings:{music:.3,effects:.6}})));
 await boot(page);await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).screen).toBe('dialogue');
 await page.keyboard.press('Escape');await expect.poll(async()=>(await state(page)).world.act).toBe('act3');
 expect((await state(page)).qa).toBe(false);expect((await state(page)).settings).toEqual({music:.3,effects:.6});await capture(page,'act3-save-migrated');
});
