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
 let s=await state();assert.equal(s.test_build,false);assert.equal(s.qa,false);assert.equal(s.screen,'title');log('ordinary cold boot',{test_build:s.test_build,qa:s.qa});await capture('title');
 await choose('Options');await wait(s=>s.screen==='options');const volume=(await state()).settings.music;await key('ArrowLeft');assert.equal((await state()).settings.music,Math.max(0,Math.round((volume-.1)*10)/10));await capture('options');await key('ArrowRight');assert.equal((await state()).settings.music,volume);await key('Escape');await wait(s=>s.screen==='title');log('options adjust restore');
 await choose('Password');await wait(s=>s.screen==='password');await page.keyboard.type('NOTACODE',{delay:40});await key('Enter');assert.match((await state()).message,/Unknown/);assert.equal((await state()).qa,false);await capture('invalid-password');await key('Escape');await wait(s=>s.screen==='title');log('invalid password recover');
 await choose('Start Act 1');if((await state()).screen==='confirm')await choose('Start fresh');await wait(s=>s.screen==='dialogue');
 const speakers=['CHARLIE','DEE','CHARLIE','DEE','CHARLIE','THE NIGHTMAN COMETH','DENNIS & DEE','CRICKET','DEE','DENNIS'];
 for(let i=0;i<speakers.length;i++){s=await state();assert.equal(s.dialogue,i);assert.equal(s.story.speaker,speakers[i]);if(i===0||i===8)await capture('opening-'+i);if(i%2===0)await page.locator('#canvas').click();else await page.keyboard.press('Enter');await wait(v=>v.screen!=='dialogue'||v.dialogue!==i);}
 await wait(s=>s.screen==='training');log('all opening stills keyboard pointer one advance');
 s=await state();const x=s.world.player.x;await page.keyboard.press('ArrowRight',{delay:200});await wait(s=>s.world.player.x>x);await key('j');await capture('running-bat');
 await key('Escape');await wait(s=>s.screen==='pause');const before=JSON.stringify((await state()).world);await page.waitForTimeout(700);assert.equal(JSON.stringify((await state()).world),before);await capture('pause');await key('Escape');await wait(s=>s.screen==='training');log('movement bat and pause freeze');
 await key('m');assert.equal((await state()).audio.muted,true);await key('m');assert.equal((await state()).audio.muted,false);assert.equal((await state()).audio.playing,'little-boy');log('mute restore state only not listening');
 await Promise.all([page.keyboard.down('ArrowRight'),page.keyboard.press('Space')]);await page.waitForTimeout(300);await page.keyboard.up('ArrowRight');await capture('jump');
 const end=Date.now()+120000;while(Date.now()<end&&(await state()).screen!=='dead'){await page.keyboard.press('ArrowRight',{delay:200});await page.waitForTimeout(80);}
 s=await state();assert.equal(s.screen,'dead');const checkpoint=s.world.checkpoint;await capture('death');await key('Enter');s=await wait(s=>s.screen==='training');assert.equal(s.world.player.hearts,3);assert.equal(s.world.checkpoint,checkpoint);assert.equal(s.world.player.dayman,0);await capture('retry');log('ordinary death retry',{checkpoint,hearts:s.world.player.hearts});
 await key('Escape');await choose('Title');await wait(s=>s.screen==='title');await choose('Continue Act 1');await wait(s=>s.screen==='training');log('return title continue');
 assert.deepEqual(faults,[]);log('finished',{browser:browser.version(),url:process.env.E2E_URL,faults,limitations:['No full-game qualification','No physical USB or audible listening','Final story inspected from separate evidence']});
})().catch(e=>{log('FAILED',{error:String(e),stack:e.stack});process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
