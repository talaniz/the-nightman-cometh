const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),path=require('node:path');
let id=22000;
async function fixture(page,name){const n=++id;await page.evaluate(v=>window.__nightmanFixture=JSON.stringify(v),{name,id:n});await page.waitForFunction(n=>JSON.parse(window.__nightmanGame).fixture_id===n,n);}
async function saveFrames(page){
 const frames=await page.evaluate(()=>{window.__motionObserve=false;return window.__motionFrames;});
 if(process.env.NIGHTMAN_EVIDENCE){fs.mkdirSync(process.env.NIGHTMAN_EVIDENCE,{recursive:true});for(const [name,f] of Object.entries(frames)){
  const base=path.join(process.env.NIGHTMAN_EVIDENCE,name);
  fs.writeFileSync(base+'.png',Buffer.from(f.png.split(',')[1],'base64'));
  fs.writeFileSync(base+'.json',JSON.stringify({viewport:page.viewportSize(),kind:'synchronized browser canvas/state',state:f.state},null,2));
 }}return frames;
}
async function observe(page,mode){await page.evaluate(mode=>{
 window.__motionFrames={};window.__motionObserve=true;
 function tick(){if(!window.__motionObserve)return;
  const s=JSON.parse(window.__nightmanGame),p=s.world.player,b=s.world.targets.find(t=>t.state==='defeated');let key;
  if(mode==='run'&&s.screen==='training'&&p.moving&&p.grounded&&!p.swing)
   key=(p.dayman?'dayman':'dennis')+'-'+(p.facing>0?'right':'left')+'-'+Math.floor(s.world.steps/6)%4;
  if(mode!=='run'&&b&&s.screen==='training'){
   const t=b.defeat_elapsed||0;
   key=t<.35?'recoil':t<.9?'fall':Math.floor((t-.9)/.2)%2?'blink':'grounded';key=mode+'-'+key;
  }
  if(key&&!window.__motionFrames[key])window.__motionFrames[key]={state:s,png:document.querySelector('#canvas').toDataURL('image/png')};
  requestAnimationFrame(tick);
 }requestAnimationFrame(tick);
},mode);}
test('MOTION authored run cycle defeats and directional shots',async({page})=>{
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('/');await expect(page.locator('#boot-action')).toBeEnabled({timeout:120000});await page.locator('#boot-action').click();await page.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await page.locator('#canvas').focus();
 await fixture(page,'act1-platform-first');await observe(page,'run');
 for(let i=0;i<2;i++)for(const key of ['ArrowRight','ArrowLeft'])await page.keyboard.press(key,{delay:850});
 const run=await saveFrames(page);for(const direction of ['left','right'])for(let pose=0;pose<4;pose++)expect(run['dennis-'+direction+'-'+pose]).toBeTruthy();
 await fixture(page,'motion-run-dayman');await observe(page,'run');
 for(let i=0;i<2;i++)for(const key of ['ArrowRight','ArrowLeft'])await page.keyboard.press(key,{delay:850});
 const day=await saveFrames(page);for(const direction of ['left','right'])for(let pose=0;pose<4;pose++)expect(day['dayman-'+direction+'-'+pose]).toBeTruthy();
 for(const boss of ['cricket','frank','nightman']){
  await fixture(page,'motion-boss-'+boss);await observe(page,boss);await page.keyboard.press('j');
  await page.waitForFunction(()=>JSON.parse(window.__nightmanGame).screen==='dialogue',{},{timeout:12000});
  const frames=await saveFrames(page);for(const stage of ['recoil','fall','grounded','blink'])expect(frames[boss+'-'+stage]).toBeTruthy();
  expect(frames[boss+'-grounded'].state.world.complete).toBe(true);
 }
 await fixture(page,'motion-shots');
 for(const [width,height] of [[1280,720],[1920,1080],[390,844]]){
  await page.setViewportSize({width,height});
  if(process.env.NIGHTMAN_EVIDENCE){const base=path.join(process.env.NIGHTMAN_EVIDENCE,'projectiles-'+width);await page.screenshot({path:base+'.png'});fs.writeFileSync(base+'.json',JSON.stringify({viewport:page.viewportSize(),state:JSON.parse(await page.evaluate(()=>window.__nightmanGame))},null,2));}
 }
 expect(errors).toEqual([]);
});
