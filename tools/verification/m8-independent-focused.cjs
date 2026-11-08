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
 const wait=async pred=>{const end=Date.now()+15000;while(Date.now()<end){const s=await state();if(pred(s))return s;await page.waitForTimeout(80);}throw Error('Expected state not reached');};
 const key=async k=>{await page.keyboard.press(k);await page.waitForTimeout(160);};
 const choose=async label=>{let s=await state();assert(s.menu.includes(label),JSON.stringify(s.menu));while(s.menu[s.selection]!==label){const old=s.selection;await key('ArrowDown');s=await wait(v=>v.selection!==old);}await key('Enter');};
 const capture=async name=>{await page.screenshot({path:path.join(out,name+'.png')});fs.writeFileSync(path.join(out,name+'.json'),JSON.stringify(await state(),null,2));};
 await page.goto(process.env.E2E_URL);await page.locator('#boot-action').waitFor({state:'visible',timeout:120000});await page.waitForFunction(()=>!document.querySelector('#boot-action').disabled,{},{timeout:120000});await page.locator('#boot-action').click();await page.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await page.locator('#canvas').focus();
 let s=await state();assert.equal(s.test_build,true);let fid=90000;
 const fixture=async name=>{const id=++fid;await page.evaluate(r=>window.__nightmanFixture=JSON.stringify(r),{name,id});await wait(s=>s.fixture_id===id);};
 const watch=async kind=>page.evaluate(kind=>{
  const o=window.__independent={active:true,rows:[],frames:{},seen:{},removed:[]};let prev={};
  function tick(){if(!o.active)return;const s=JSON.parse(window.__nightmanGame),w=s.world,b=w.targets.find(t=>['cricket','frank','nightman'].includes(t.kind));
   const row={ms:performance.now(),screen:s.screen,dialogue:s.dialogue,player:w.player,boss:b,shots:w.shots,targets:w.targets};
   if(!o.rows.length||o.lastKey!==JSON.stringify([b?.state,b?.remaining,b?.burst,s.dialogue,w.shots.length,w.targets.length])){row.steps=w.steps;o.rows.push(row);o.lastKey=JSON.stringify([b?.state,b?.remaining,b?.burst,s.dialogue,w.shots.length,w.targets.length]);}
   let key=b?.kind+'-'+b?.state+(kind==='cricket'&&b?.state==='charge'?'-'+b.direction:'');if(kind==='finale'){if(s.dialogue===1){o.effectStart??=performance.now();key=performance.now()-o.effectStart>1100?'color-wash':'first-flash';}else key=s.dialogue===2?'dayman-revealed':null;}
   if(key&&!o.frames[key]&&Object.keys(o.frames).length<5)o.frames[key]=document.querySelector('#canvas').toDataURL();
   for(const t of w.targets.filter(t=>t.kind==='sandwich'))if(!o.seen[t.id])o.seen[t.id]=t;
   const now=Object.fromEntries(w.targets.filter(t=>t.kind==='sandwich').map(t=>[t.id,t]));for(const [id,t]of Object.entries(prev))if(!now[id])o.removed.push({target:t,player:w.player,ms:performance.now()});prev=now;
   requestAnimationFrame(tick);
  }requestAnimationFrame(tick);
 },kind);
 const stop=async name=>{const o=await page.evaluate(()=>{window.__independent.active=false;const o=window.__independent;window.__independent=null;return o;});for(const [key,png]of Object.entries(o.frames))fs.writeFileSync(path.join(out,name+'-'+key+'.png'),Buffer.from(png.split(',')[1],'base64'));delete o.frames;fs.writeFileSync(path.join(out,name+'-trace.json'),JSON.stringify(o));return o;};
 let o;
 await fixture('act1-boss-warning');await watch('cricket');await page.waitForFunction(()=>window.__independent.rows.some(r=>r.boss?.state==='stunned'),{},{timeout:15000});o=await stop('cricket');
 const brake=o.rows.find(r=>r.boss?.state==='brake'),reversed=o.rows.find(r=>r.ms>brake?.ms&&r.boss?.state==='charge'&&r.boss.direction===1),crash=o.rows.find(r=>r.boss?.state==='stunned');assert(brake&&reversed&&crash);assert.equal(crash.boss.x,4950);log('Cricket tell reversal bounded dumpster crash',{brakeX:brake.boss.x,crashX:crash.boss.x,elapsedMs:crash.ms-brake.ms});
 await fixture('act1-boss-stunned');await key('j');assert.equal((await state()).world.targets[0].hp,2);log('Cricket stunned punish');
 await fixture('act2-boss');await key('Escape');await choose('QA invincibility');await wait(s=>s.screen==='training');await watch('frank');await page.waitForTimeout(4300);o=await stop('frank');const pieces=Object.values(o.seen).slice(0,5);assert.deepEqual(pieces.map(t=>t.ingredient),['whole','meat','cheese','bread','lettuce']);assert(pieces.every(t=>t.y===398&&t.direction===-1));log('Frank whole plus four straight ingredients',{pieces:pieces.map(t=>t.ingredient)});
 await fixture('act2-boss');await key('Escape');await choose('QA invincibility');await watch('frank');for(let i=0;i<20;i++){await key('j');}o=await stop('frank-interception');const intercepted=o.removed.filter(r=>r.target.x>r.player.x&&r.target.x-r.player.x<110&&r.player.swing>0);assert(intercepted.length>0);log('Frank bat interception',{count:intercepted.length});
 await fixture('act3-boss-summons');await watch('nightman');await page.waitForFunction(()=>{const rows=window.__independent.rows;return rows.some(r=>r.shots.some(s=>s.kind==='chimichanga'))&&rows.some(r=>r.shots.some(s=>s.kind==='crucifix'));},{},{timeout:30000});await page.waitForTimeout(800);o=await stop('nightman');assert(o.rows.some(r=>r.boss?.state==='charge'));assert(o.rows.every(r=>r.targets.filter(t=>t.kind==='ghoul'&&t.alive).length<=2));const bursts={};for(const r of o.rows){if(r.boss?.burst){const kind=r.boss.burst%2?'crucifix':'chimichanga';bursts[r.boss.burst]=Math.max(bursts[r.boss.burst]||0,r.shots.filter(s=>s.kind===kind).length);}}assert.equal(bursts[1],3);assert.equal(bursts[2],2);log('Nightman charged alternate bursts capped ghouls',{bursts});
 await fixture('act3-finale-0');await capture('dennis-before');await watch('finale');await key('Enter');await wait(s=>s.dialogue===1);await key('Enter');assert.equal((await state()).dialogue,1);await wait(s=>s.dialogue===2);o=await stop('finale');const effect=o.rows.find(r=>r.dialogue===1),revealed=o.rows.find(r=>r.dialogue===2);assert(effect&&revealed);const elapsed= revealed.ms-effect.ms;assert(elapsed>=4100&&elapsed<=10000);log('automatic transformation Enter cannot skip',{observedMs:elapsed});assert.equal((await state()).story.text,'The Dayman!');await capture('dayman-revealed');
 await page.locator('#canvas').click();await wait(s=>s.dialogue===3);await page.waitForTimeout(500);assert.equal((await state()).dialogue,3);assert.equal((await state()).audio.playing,'proposal');await capture('charlie-sunburst');
 for(let i=3;i<26;i++){s=await state();assert.equal(s.dialogue,i);if([17,20,21,22,23,24,25].includes(i))await capture('finale-'+i);log('finale page',{index:i,speaker:s.story.speaker,text:s.story.text,music:s.audio.playing});await key('Enter');await wait(v=>v.screen!=='dialogue'||v.dialogue!==i);}
 assert.equal((await state()).screen,'credits');assert.equal((await state()).audio.playing,'sunny-credits');await capture('credits');log('direct Sunny credits after retained exchange');
 assert.deepEqual(faults,[]);log('finished',{browser:browser.version(),url:process.env.E2E_URL,faults,limitations:['Focused fixtures include invincibility and are not full-game qualification','No physical USB or audible listening']});
})().catch(e=>{log('FAILED',{error:String(e),stack:e.stack});process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
