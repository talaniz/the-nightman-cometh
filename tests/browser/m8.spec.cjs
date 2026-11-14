const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),path=require('node:path');
const state=async page=>JSON.parse(await page.evaluate(()=>window.__nightmanGame));
async function boot(page){
 await page.goto('/');await expect(page.locator('#boot-action')).toBeEnabled({timeout:120000});
 await page.locator('#boot-action').click();await page.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});
 await page.locator('#canvas').focus();
}
let sequence=19000;
async function fixture(page,name){const id=++sequence;await page.evaluate(request=>window.__nightmanFixture=JSON.stringify(request),{name,id});await page.waitForFunction(id=>JSON.parse(window.__nightmanGame).fixture_id===id,id);}
async function capture(page,name){
 const dir=process.env.NIGHTMAN_EVIDENCE;if(!dir)return;fs.mkdirSync(dir,{recursive:true});
 await page.screenshot({path:path.join(dir,'m8-'+name+'.png')});
 fs.writeFileSync(path.join(dir,'m8-'+name+'.json'),JSON.stringify({viewport:page.viewportSize(),state:await state(page)},null,2));
}

// Observe transient states in the browser, without IPC/screenshot delays between them.
// This reads game state and canvas pixels only; it never changes the simulation.
async function observe(page,kind){
 await page.evaluate(kind=>{
  const observation=window.__m8Observation={frames:{},active:true,start:null};
  function tick(){
   if(!observation.active)return;
   const state=JSON.parse(window.__nightmanGame),b=state.world.targets.find(t=>t.kind==='cricket');
   let key;
   if(kind==='cricket'&&state.screen==='training'&&b){
    if(b.state==='brake')key='cricket-braking';
    else if(observation.frames['cricket-braking']&&b.state==='charge'&&b.direction===1)key='cricket-reversed';
    else if(observation.frames['cricket-reversed']&&b.state==='stunned')key='dumpster-crash';
   }else if(kind==='transformation'&&state.screen==='dialogue'&&state.dialogue===1){
    observation.start??=performance.now();
    key=performance.now()-observation.start<100?'first-flash':performance.now()-observation.start>1100?'color-wash':null;
   }
   if(key&&!observation.frames[key])observation.frames[key]={state,png:document.querySelector('#canvas').toDataURL('image/png')};
   requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
 },kind);
}
async function observedFrames(page){
 const frames=await page.evaluate(()=>{window.__m8Observation.active=false;return window.__m8Observation.frames;});
 const dir=process.env.NIGHTMAN_EVIDENCE;
 if(dir){fs.mkdirSync(dir,{recursive:true});for(const [name,frame] of Object.entries(frames)){
  fs.writeFileSync(path.join(dir,'m8-'+name+'.png'),Buffer.from(frame.png.split(',')[1],'base64'));
  fs.writeFileSync(path.join(dir,'m8-'+name+'.json'),JSON.stringify({viewport:page.viewportSize(),kind:'actual browser canvas',state:frame.state},null,2));
 }}
 return frames;
}

test('M8 Cricket brakes reverses and crashes into the dumpster',async({page})=>{
 await boot(page);await capture(page,'title-1280');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'title-1920');
 await page.setViewportSize({width:390,height:844});await capture(page,'title-narrow');
 await page.setViewportSize({width:1280,height:720});await fixture(page,'act1-boss-warning');
 await observe(page,'cricket');
 await page.waitForFunction(()=>!!window.__m8Observation.frames['dumpster-crash'],{},{timeout:15000});
 const frames=await observedFrames(page);
 expect(frames['cricket-braking'].state.world.targets[0].direction).toBe(-1);
 expect(frames['cricket-reversed'].state.world.targets[0].direction).toBe(1);
 expect(frames['dumpster-crash'].state.world.targets[0].x).toBe(4950);
 await page.setViewportSize({width:1920,height:1080});await capture(page,'dumpster-1920');
});

test('M8 transformation is automatic and proposal advances by click only once',async({page})=>{
 await boot(page);await fixture(page,'act3-finale-0');await capture(page,'dennis-before');
 await observe(page,'transformation');
 await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).dialogue).toBe(1);
 await page.keyboard.press('Enter');expect((await state(page)).dialogue).toBe(1);
 await expect.poll(async()=>(await state(page)).dialogue,{timeout:7000}).toBe(2);
 const frames=await observedFrames(page);expect(Object.keys(frames)).toEqual(['first-flash','color-wash']);
 expect((await state(page)).story.text).toBe('The Dayman!');await capture(page,'dayman-revealed');
 await page.locator('#canvas').click();await expect.poll(async()=>(await state(page)).dialogue).toBe(3);
 expect((await state(page)).audio.playing).toBe('proposal');await capture(page,'proposal-sunburst');
 await page.waitForTimeout(500);expect((await state(page)).dialogue).toBe(3);
 await page.locator('#canvas').click();await expect.poll(async()=>(await state(page)).dialogue).toBe(4);
 await page.setViewportSize({width:1920,height:1080});await capture(page,'proposal-1920');
 await page.setViewportSize({width:390,height:844});await capture(page,'story-narrow');
});

test('M8 live projectile shapes and both charged Nightman bursts',async({page})=>{
 await boot(page);
 await fixture(page,'act2-boss');
 await expect.poll(async()=>(await state(page)).world.targets.some(t=>t.ingredient==='cheese'),{timeout:10000,intervals:[50]}).toBe(true);
 await capture(page,'frank-ingredients');
 await fixture(page,'act2-crew');
 await expect.poll(async()=>(await state(page)).world.shots.some(s=>s.kind==='egg'),{timeout:10000,intervals:[50]}).toBe(true);
 await capture(page,'crew-egg');
 await fixture(page,'act2-gun');
 await expect.poll(async()=>(await state(page)).world.shots.some(s=>s.kind==='alcohol'),{timeout:10000,intervals:[50]}).toBe(true);
 await capture(page,'gun-alcohol');
 // This focused visual fixture uses invincibility; it is never a qualifying run.
 await fixture(page,'act3-boss-summons');
 await expect.poll(async()=>(await state(page)).world.targets[0].state,{timeout:20000,intervals:[50]}).toBe('charge');
 await capture(page,'nightman-charge');
 for(const kind of ['crucifix','chimichanga']){
  await expect.poll(async()=>(await state(page)).world.shots.some(s=>s.kind===kind),{timeout:30000,intervals:[50]}).toBe(true);
  await capture(page,'nightman-'+kind);
 }
});


test('POLISH ingredient readability and revised closing lines at supported viewport sizes',async({page})=>{
 await boot(page);
 for(const [width,height] of [[1280,720],[1920,1080],[390,844]]){
  await page.setViewportSize({width,height});
  await fixture(page,'act2-boss');
  await expect.poll(async()=>(await state(page)).world.targets.some(t=>t.ingredient==='lettuce'),{timeout:10000,intervals:[50]}).toBe(true);
  const shots=(await state(page)).world.targets.filter(t=>t.kind==='sandwich');
  expect(shots.length).toBeGreaterThan(0);
  expect(shots.every(t=>[366,382,398].includes(t.y))).toBe(true);
  await capture(page,'polish-ingredients-'+width);
  for(const [index,text] of [[21,'Well, technically I didn’t sign anything'],[22,'So, I guess I’ll see you tomorrow?…']]){
   await fixture(page,'act3-finale-'+index);
   expect((await state(page)).story.text).toBe(text);
   await capture(page,'polish-finale-'+index+'-'+width);
   await page.keyboard.press('Enter');
   await expect.poll(async()=>(await state(page)).dialogue).toBe(index+1);
  }
 }
});


test('CAT_FOOD can appearance and unchanged collection',async({page})=>{
 await boot(page);
 for(const [width,height] of [[1280,720],[1920,1080],[390,844]]){
  await page.setViewportSize({width,height});await fixture(page,'act1-platform-first');
  await capture(page,'cat-food-can-'+width);
 }
 await page.setViewportSize({width:1280,height:720});await fixture(page,'act1-platform-first');
 for(let i=0;i<20 && (await state(page)).world.player.x<920;i++){
  await page.keyboard.press('ArrowRight',{delay:100});
 }
 const collected=await state(page);expect(collected.world.player.x).toBeGreaterThanOrEqual(920);
 expect(collected.screen).toBe('training');expect(collected.world.player.hearts).toBe(3);
 await capture(page,'cat-food-collected');
 expect((await state(page)).screen).toBe('training');
});

test('BAT_GRIP running handle follows Dennis in both directions',async({page})=>{
 await boot(page);await fixture(page,'act1-platform-first');
 await page.evaluate(()=>{
  window.__batFrames={};
  function observe(){
   const s=JSON.parse(window.__nightmanGame),p=s.world.player;
   if(s.screen==='training'&&p.moving&&p.grounded&&!p.swing){
    const key=(p.facing>0?'right':'left')+'-'+Math.floor(s.world.steps/8)%2;
    if(!window.__batFrames[key])window.__batFrames[key]={state:s,png:document.querySelector('#canvas').toDataURL('image/png')};
   }
   if(window.__batObserving)requestAnimationFrame(observe);
  }
  window.__batObserving=true;requestAnimationFrame(observe);
 });
 for(const key of ['ArrowRight','ArrowLeft'])await page.keyboard.press(key,{delay:1000});
 const frames=await page.evaluate(()=>{window.__batObserving=false;return window.__batFrames;});
 expect(Object.keys(frames).sort()).toEqual(['left-0','left-1','right-0','right-1']);
 const dir=process.env.NIGHTMAN_EVIDENCE;
 if(dir){fs.mkdirSync(dir,{recursive:true});for(const [name,f] of Object.entries(frames)){
  fs.writeFileSync(path.join(dir,'bat-grip-'+name+'.png'),Buffer.from(f.png.split(',')[1],'base64'));
  fs.writeFileSync(path.join(dir,'bat-grip-'+name+'.json'),JSON.stringify({viewport:page.viewportSize(),kind:'actual browser canvas',state:f.state},null,2));
 }}
 for(const [width,height] of [[1280,720],[1920,1080],[390,844]]){
  await page.setViewportSize({width,height});await capture(page,'bat-grip-idle-'+width);
 }
 await page.setViewportSize({width:1280,height:720});await page.keyboard.press('Space',{delay:80});await capture(page,'bat-grip-jump');
 await page.keyboard.press('j');
 expect((await state(page)).screen).toBe('training');
});
