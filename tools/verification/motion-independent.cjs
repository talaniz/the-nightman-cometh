const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
assert(process.env.E2E_URL,'E2E_URL required');
const out=process.env.E2E_OUTPUT||process.env.E2E_DIR||'/tmp/nightman-m8-independent-e2e';fs.mkdirSync(out,{recursive:true});
const observations=[];let browser;
const log=(name,data={})=>{const row={time:new Date().toISOString(),name,...data};observations.push(row);fs.appendFileSync(path.join(out,'observations.jsonl'),JSON.stringify(row)+'\n');console.log(name,JSON.stringify(data));};
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH||chromium.executablePath(),args:['--no-sandbox','--disable-gpu']});
 const context=await browser.newContext({viewport:{width:1280,height:720}});const page=await context.newPage();const faults=[];
 page.on('pageerror',e=>faults.push(String(e)));page.on('requestfailed',r=>faults.push(r.url()+': '+r.failure()?.errorText));
 page.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))faults.push(m.text());});
 const state=async()=>JSON.parse(await page.evaluate(()=>window.__nightmanGame));
 const wait=async pred=>{const end=Date.now()+40000;while(Date.now()<end){const s=await state();if(pred(s))return s;await page.waitForTimeout(80);}throw Error('Expected state not reached');};
 const capture=async name=>{await page.screenshot({path:path.join(out,name+'.png')});fs.writeFileSync(path.join(out,name+'.json'),JSON.stringify(await state(),null,2));};
 await page.goto(process.env.E2E_URL);await page.locator('#boot-action').waitFor({state:'visible',timeout:120000});await page.waitForFunction(()=>!document.querySelector('#boot-action').disabled,{},{timeout:120000});await page.locator('#boot-action').click();await page.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await page.locator('#canvas').focus();
 let s=await state();assert.equal(s.test_build,true);let fid=90000;
 const fixture=async name=>{const id=++fid;await page.evaluate(r=>window.__nightmanFixture=JSON.stringify(r),{name,id});await wait(s=>s.fixture_id===id);};
 for(const label of ['dennis','dayman']){
 await fixture(label==='dennis'?'act1-platform-first':'motion-run-dayman');
 await page.evaluate(()=>{window.motion={active:true,frames:{}};function tick(){const o=window.motion;if(!o.active)return;const s=JSON.parse(window.__nightmanGame),p=s.world.player;if(p.grounded&&p.moving&&!p.swing){const k=(p.facing>0?'right':'left')+'-'+Math.floor(s.world.steps/6)%4;if(!o.frames[k]){const c=document.querySelector('#canvas'),crop=document.createElement('canvas');crop.width=140;crop.height=100;const camera=Math.max(0,Math.min(4140,p.x-350));crop.getContext('2d').drawImage(c,(p.x-camera-60)*c.width/960,(p.y-30)*c.height/540,140*c.width/960,100*c.height/540,0,0,140,100);o.frames[k]={state:s,png:crop.toDataURL()};}}requestAnimationFrame(tick);}requestAnimationFrame(tick);});
 for(let i=0;i<2;i++)for(const k of ['ArrowRight','ArrowLeft'])await page.keyboard.press(k,{delay:850});
 const f=await page.evaluate(()=>{window.motion.active=false;return window.motion.frames;});for(const side of ['left','right'])for(let i=0;i<4;i++)assert(f[side+'-'+i]);for(const[k,v]of Object.entries(f))fs.writeFileSync(path.join(out,label+'-'+k+'.png'),Buffer.from(v.png.split(',')[1],'base64'));await page.keyboard.press('j');await page.waitForTimeout(400);assert.equal((await state()).world.player.swing,0);log('four authored running poses and attack recovery',{label,keys:Object.keys(f)});
 }
 for(const boss of ['cricket','frank','nightman']){
 await fixture('motion-boss-'+boss);
 await page.evaluate(()=>{window.defeat={active:true,rows:[],frames:{}};function tick(){const o=window.defeat;if(!o.active)return;const s=JSON.parse(window.__nightmanGame),b=s.world.targets.find(t=>t.state==='defeated');if(b){const t=b.defeat_elapsed||0,k=s.screen==='dialogue'?'story':t<.35?'recoil':t<.9?'fall':Math.floor((t-.9)/.2)%2?'blink':'grounded';if(!o.frames[k]){o.rows.push({key:k,ms:performance.now(),state:s});o.frames[k]=document.querySelector('#canvas').toDataURL();}}requestAnimationFrame(tick);}requestAnimationFrame(tick);});
 await page.keyboard.press('j');await wait(s=>s.world.targets.some(t=>t.state==='defeated'));
 await page.keyboard.press('Escape');await wait(s=>s.screen==='pause');const paused=await state();await page.waitForTimeout(500);const later=await state();assert.deepEqual(later.world,paused.world);await page.keyboard.press('Escape');await wait(s=>s.screen==='training');
 if(boss==='frank') {await page.evaluate(()=>window.dispatchEvent(new Event('blur')));await wait(s=>s.screen==='pause');const a=await state();await page.waitForTimeout(500);assert.deepEqual((await state()).world,a.world);await page.locator('#canvas').focus();await page.keyboard.press('Escape');await wait(s=>s.screen==='training');log('focus-loss event froze defeat');}
 const held=await state();await page.keyboard.press('ArrowRight',{delay:250});await page.keyboard.press('j');const frozen=await state();if(frozen.screen==='training'){assert.equal(frozen.world.player.x,held.world.player.x);assert.equal(frozen.world.player.hearts,held.world.player.hearts);assert.equal(frozen.world.shots.length,0);}
 await wait(s=>s.screen==='dialogue');const d=await page.evaluate(()=>{window.defeat.active=false;return window.defeat;});for(const k of ['recoil','fall','grounded','blink','story'])assert(d.frames[k],boss+' '+k);for(const[k,v]of Object.entries(d.frames))fs.writeFileSync(path.join(out,boss+'-'+k+'.png'),Buffer.from(v.split(',')[1],'base64'));delete d.frames;fs.writeFileSync(path.join(out,boss+'-trace.json'),JSON.stringify(d));log('real final hit delayed frozen defeat then story',{boss,storyElapsed:d.rows.find(r=>r.key==='story').state.world.targets.find(t=>t.state==='defeated').defeat_elapsed});
 }
 for(const [fixtureName,kind]of [['act2-gun','alcohol'],['act3-boss-summons','crucifix'],['act3-boss-summons','chimichanga']]){await fixture(fixtureName);const s=await wait(s=>s.world.shots.some(t=>t.kind===kind));const shot=s.world.shots.find(t=>t.kind===kind);log('live projectile observed',{kind,dx:shot.dx});await capture(kind);}
 assert.deepEqual(faults,[]);log('PASSED',{browser:browser.version(),faults});
})().catch(e=>{log('FAILED',{error:String(e),stack:e.stack});process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
