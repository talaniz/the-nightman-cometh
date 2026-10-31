const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),path=require('node:path');
const state=async p=>JSON.parse(await p.evaluate(()=>window.__nightmanGame));
async function boot(p){await p.goto('/');await expect(p.locator('#boot-action')).toBeEnabled({timeout:120000});await p.locator('#boot-action').click();await p.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await p.locator('#canvas').focus();}
let fixtureId=0;
async function fixture(p,name){const id=++fixtureId;await p.evaluate(req=>window.__nightmanFixture=JSON.stringify(req),{name:'act2-'+name,id});await p.waitForFunction(id=>JSON.parse(window.__nightmanGame).fixture_id===id,id,{timeout:30000});}
async function capture(p,name){const dir=process.env.NIGHTMAN_EVIDENCE;if(!dir)return;fs.mkdirSync(dir,{recursive:true});await p.screenshot({path:path.join(dir,name+'.png')});fs.writeFileSync(path.join(dir,name+'.json'),JSON.stringify({viewport:p.viewportSize(),state:await state(p),build:process.env.NIGHTMAN_BUILD},null,2));}
function errors(p){const list=[];p.on('pageerror',e=>list.push(String(e)));p.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))list.push(m.text());});p.on('requestfailed',r=>list.push(r.url()));return list;}

test('ACT2_APPROACH bridge platforms signs pickups pause and retry',async({page})=>{
 const faults=errors(page);await boot(page);
 await fixture(page,'approach');expect((await state(page)).world.act).toBe('act2');expect((await state(page)).audio.playing).toBe('troll-toll');await capture(page,'bridge-entrance');
 for(const start of ['first','second']){
  await fixture(page,'platform-'+start);const x=start==='first'?560:1740;
  await page.keyboard.press('Space');await expect.poll(async()=>{const p=(await state(page)).world.player;return p.grounded&&p.y===316;},{timeout:10000}).toBe(true);await capture(page,'bridge-platform-'+start);
  for(let n=0;n<40;n++){
   const p=(await state(page)).world.player,dx=x+130-p.x;
   if(Math.abs(dx)<10)break;
   await page.keyboard.press(dx>0?'ArrowRight':'ArrowLeft',{delay:Math.min(100,Math.abs(dx)/220*1000)});
  }
  // Re-establish footing if slow key release walked off the lower ledge.
  await page.keyboard.press('Space');
  await expect.poll(async()=>{const p=(await state(page)).world.player;return p.grounded&&p.y===316;},{timeout:10000}).toBe(true);
  await Promise.all([page.keyboard.down('ArrowRight'),page.keyboard.press('Space')]);
  try{await expect.poll(async()=>(await state(page)).world.player.x,{timeout:10000,intervals:[50]}).toBeGreaterThanOrEqual(x+220);}
  finally{await page.keyboard.up('ArrowRight');}
  await expect.poll(async()=>{const p=(await state(page)).world.player;return p.grounded&&p.y===256;},{timeout:10000}).toBe(true);await capture(page,'bridge-upper-'+start);

 }
 for(const name of ['crew','gun','meal','mid','preboss','death']){
  await fixture(page,name);
  if(['meal','mid','preboss'].includes(name)){await page.keyboard.press('ArrowRight',{delay:230});}
  if(name==='meal')expect((await state(page)).world.player.dayman).toBeGreaterThan(0);
  if(['mid','preboss'].includes(name))expect((await state(page)).world.player.hearts).toBe(2);
  await capture(page,'bridge-'+name);
  if(name==='death'){await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).world.player.hearts).toBe(3);await capture(page,'bridge-retry');}
 }
 await fixture(page,'crew');await page.keyboard.press('Escape');await expect.poll(async()=>(await state(page)).screen).toBe('pause');const before=(await state(page)).world;await page.waitForTimeout(250);expect((await state(page)).world).toEqual(before);await capture(page,'bridge-pause');
 await page.keyboard.press('Escape');await page.setViewportSize({width:1920,height:1080});await capture(page,'bridge-1920');await page.setViewportSize({width:390,height:844});await capture(page,'bridge-narrow');expect(faults).toEqual([]);
});

test('FRANK actual bat stomp beam and straight sandwiches',async({page})=>{
 const faults=errors(page);await boot(page);await fixture(page,'boss-close');
 await page.keyboard.press('j');await expect.poll(async()=>(await state(page)).world.targets[0].hp).toBe(4);await capture(page,'frank-bat');
 await fixture(page,'boss-stomp');await expect.poll(async()=>(await state(page)).world.targets[0].hp).toBe(4);await capture(page,'frank-stomp');
 await fixture(page,'boss-beam');await page.keyboard.press('k');await expect.poll(async()=>(await state(page)).world.targets[0].hp).toBe(4);await capture(page,'frank-beam');
 await fixture(page,'boss');expect((await state(page)).audio.playing).toBe('frank-boss');
 await expect.poll(async()=>(await state(page)).world.targets.some(t=>t.kind==='sandwich'),{timeout:15000}).toBe(true);
 const shot=(await state(page)).world.targets.find(t=>t.kind==='sandwich');expect(shot.y).toBe(398);await capture(page,'frank-sandwich');
 await page.waitForTimeout(180);const later=(await state(page)).world.targets.find(t=>t.id===shot.id);if(later){expect(later.y).toBe(shot.y);expect(later.x).toBeLessThan(shot.x);}
 expect((await state(page)).world.targets.every(t=>['frank','sandwich'].includes(t.kind))).toBe(true);expect(faults).toEqual([]);
});

test('ACT2_STORY exact extra kidnapping screen abduction and endpoint',async({page})=>{
 const faults=errors(page);await boot(page);await fixture(page,'frank-story-3');
 expect((await state(page)).story.speaker).toBe('DENNIS');
 expect((await state(page)).story.text).toBe('Dee—er—Waitress! Stop getting kidnapped, you bird!');await capture(page,'frank-extra-kidnapping');
 await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).screen).toBe('training');expect((await state(page)).world.act).toBe('act2');
 for(let i=0;i<2;i++){await fixture(page,'nightman-story-'+i);await capture(page,'nightman-abduction-'+i);}
 await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).screen).toBe('complete');await capture(page,'act2-preview-end');
 expect((await state(page)).menu).toContain('Replay QA Act 2');expect(faults).toEqual([]);
});

test('ACT2_MOTION live crew gun and Frank pose evidence',async({page})=>{
 const faults=errors(page);await boot(page);
 for(const name of ['crew','gun','boss']){
  await fixture(page,name);
  await page.evaluate(()=>{
   window.__motion={frames:{},active:true};
   const sample=()=>{
    const log=window.__motion;if(!log.active)return;
    const s=JSON.parse(window.__nightmanGame),w=s.world,c=document.querySelector('#canvas');
    const camera=Math.max(0,Math.min(3600-960,w.player.x-350));
    for(const t of w.targets){
     if(!t.alive||!['duncan','z','gun','frank'].includes(t.kind))continue;
     const x=t.x-camera;if(x<60||x>850)continue;
     const frame=Math.floor(t.animation_step/(t.kind==='frank'?10:9))%2;
     const key=t.kind+'-'+t.state+(t.state==='patrol'||t.state==='shuffle'?'-'+frame:'');
     if(log.frames[key])continue;
     const crop=document.createElement('canvas');crop.width=120;crop.height=110;
     crop.getContext('2d').drawImage(c,(x-40)*c.width/960,(t.y-45)*c.height/540,120*c.width/960,110*c.height/540,0,0,120,110);
     log.frames[key]={png:crop.toDataURL('image/png'),state:t};
    }
    requestAnimationFrame(sample);
   };requestAnimationFrame(sample);
  });
  // Real keyboard input exercises scene motion; observer reads pixels only.
  await page.keyboard.press('j');if(name==='crew')await page.keyboard.press('ArrowRight',{delay:200});await page.waitForTimeout(name==='boss'?3500:2800);
  const frames=await page.evaluate(()=>{window.__motion.active=false;return window.__motion.frames;});
  const kind=name==='crew'?'z':name==='gun'?'gun':'frank';
  expect(Object.keys(frames).filter(k=>k.startsWith(kind)).length).toBeGreaterThanOrEqual(2);
  const dir=process.env.NIGHTMAN_EVIDENCE;
  if(dir)for(const [key,value]of Object.entries(frames)){
   fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'motion-'+name+'-'+key+'.png'),Buffer.from(value.png.split(',')[1],'base64'));
   fs.writeFileSync(path.join(dir,'motion-'+name+'-'+key+'.json'),JSON.stringify({viewport:page.viewportSize(),state:value.state,kind:'live browser canvas crop',build:process.env.NIGHTMAN_BUILD},null,2));
  }
 }
 expect(faults).toEqual([]);
});
