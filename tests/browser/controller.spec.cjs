const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),path=require('node:path');
const state=async p=>JSON.parse(await p.evaluate(()=>window.__nightmanGame));
async function boot(p){
 await p.addInitScript(()=>{
  window.testPad={connected:true,mapping:'standard',axes:[0,0],buttons:Array.from({length:17},()=>({pressed:false}))};
  window.padMode='normal';
  Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>{
   if(window.padMode==='denied')throw new DOMException('Denied','SecurityError');
   return window.padMode==='absent'?[]:[window.testPad];
  }});
 });
 await p.goto('/');await expect(p.locator('#boot-action')).toBeEnabled({timeout:120000});await p.locator('#boot-action').click();
 await p.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await p.locator('#canvas').focus();
 await expect.poll(async()=>(await state(p)).input.connected).toBe(true);
 await p.waitForTimeout(100);
}
async function buttons(p,list){await p.evaluate(list=>window.testPad.buttons.forEach((b,i)=>b.pressed=list.includes(i)),list);await p.waitForTimeout(100);}
async function tap(p,b){await buttons(p,[b]);await buttons(p,[]);}
let id=8000;
async function fixture(p,name){await buttons(p,[]);const n=++id;await p.evaluate(req=>window.__nightmanFixture=JSON.stringify(req),{name,id:n});await p.waitForFunction(n=>JSON.parse(window.__nightmanGame).fixture_id===n,n);await p.waitForTimeout(100);}
async function capture(p,name){const dir=process.env.NIGHTMAN_EVIDENCE;if(!dir)return;fs.mkdirSync(dir,{recursive:true});await p.screenshot({path:path.join(dir,'controller-'+name+'.png')});fs.writeFileSync(path.join(dir,'controller-'+name+'.json'),JSON.stringify({viewport:p.viewportSize(),state:await state(p),build:process.env.NIGHTMAN_BUILD,simulated_pad:true},null,2));}
function errors(p){const list=[];p.on('pageerror',e=>list.push(String(e)));p.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))list.push(m.text());});p.on('requestfailed',r=>list.push(r.url()));return list;}
async function selectCharacter(p,target){
 const start=(await state(p)).input.password_index;
 const queue=[[start,[]]],seen=new Set([start]);let route=[];
 while(queue.length){const [i,r]=queue.shift();if(i===target){route=r;break;}
  for(const [button,delta] of [[14,-1],[15,1],[12,-10],[13,10]]){const j=(i+delta+38)%38;if(!seen.has(j)){seen.add(j);queue.push([j,[...r,button]]);}}
 }
 for(const b of route)await tap(p,b);
 await expect.poll(async()=>(await state(p)).input.password_index).toBe(target);await tap(p,0);
}

test('CONTROLLER menus password dialogue options and credits',async({page})=>{
 const faults=errors(page);await boot(page);await capture(page,'connected-title');
 await buttons(page,[0]);await expect.poll(async()=>(await state(page)).screen).toBe('dialogue');
 await page.waitForTimeout(400);expect((await state(page)).dialogue).toBe(0);await capture(page,'dialogue');await buttons(page,[]);
 await tap(page,1);await expect.poll(async()=>(await state(page)).screen).toBe('training');
 await tap(page,9);await expect.poll(async()=>(await state(page)).screen).toBe('pause');await capture(page,'pause');
 await tap(page,13);await tap(page,0);await expect.poll(async()=>(await state(page)).screen).toBe('options');
 const volume=(await state(page)).settings.music;await tap(page,14);expect((await state(page)).settings.music).toBeCloseTo(volume-.1);
 await capture(page,'options');await tap(page,1);await expect.poll(async()=>(await state(page)).screen).toBe('pause');
 await tap(page,12);await tap(page,0);await expect.poll(async()=>(await state(page)).screen).toBe('title');
 // Existing save inserts Continue, so select the Password menu entry by actual labels.
 while((await state(page)).menu[(await state(page)).selection]!=='Password')await tap(page,13);
 await tap(page,0);await expect.poll(async()=>(await state(page)).screen).toBe('password');
 await selectCharacter(page,0);await selectCharacter(page,37);expect((await state(page)).message).toContain('Unknown');await capture(page,'password-invalid');
 await selectCharacter(page,36);expect((await state(page)).password).toBe('');
 for(const ch of 'NIGHTMAN')await selectCharacter(page,'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.indexOf(ch));
 await capture(page,'password');await selectCharacter(page,37);expect((await state(page)).world.act).toBe('act3');expect((await state(page)).qa).toBe(true);
 await fixture(page,'act3-finale-6');await tap(page,0);expect((await state(page)).screen).toBe('ending');await capture(page,'ending');
 await tap(page,0);expect((await state(page)).screen).toBe('credits');await capture(page,'credits');
 await tap(page,4);expect((await state(page)).audio.muted).toBe(true);await capture(page,'muted');await tap(page,4);
 await fixture(page,'audio-error');expect((await state(page)).audio.error).toContain('Audio unavailable');await capture(page,'audio-error');await tap(page,5);
 await expect.poll(async()=>(await state(page)).audio.error).toBe('');await capture(page,'audio-recovered');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'credits-1920');await page.setViewportSize({width:390,height:844});await capture(page,'narrow');
 await page.setViewportSize({width:1280,height:720});await tap(page,0);expect((await state(page)).screen).toBe('dialogue');await tap(page,1);expect((await state(page)).screen).toBe('ending');expect(faults).toEqual([]);
});

test('CONTROLLER disconnect focus unsupported fallback and deadzone',async({page})=>{
 const faults=errors(page);await boot(page);await tap(page,0);await tap(page,1);
 const start=(await state(page)).world.player.x;
 await page.evaluate(()=>window.testPad.axes=[.2,0]);await page.waitForTimeout(300);expect((await state(page)).world.player.x).toBe(start);
 await page.evaluate(()=>window.testPad.axes=[1,0]);await expect.poll(async()=>(await state(page)).world.player.x).toBeGreaterThan(start+10);
 await page.evaluate(()=>window.padMode='absent');await expect.poll(async()=>(await state(page)).screen).toBe('pause');await capture(page,'disconnected');
 const paused=(await state(page)).world.player.x;await page.waitForTimeout(300);expect((await state(page)).world.player.x).toBe(paused);
 await page.evaluate(()=>{window.padMode='normal';window.testPad.buttons[9].pressed=true;});await page.waitForTimeout(300);expect((await state(page)).screen).toBe('pause');await capture(page,'release-required');
 await page.evaluate(()=>window.testPad.axes=[0,0]);await buttons(page,[]);await tap(page,9);expect((await state(page)).screen).toBe('training');
 // Real browser focus change, rather than merely dispatching a synthetic blur event.
 const other=await page.context().newPage();await other.goto('about:blank');await other.bringToFront();await expect.poll(async()=>(await state(page)).screen).toBe('pause');
 await page.evaluate(()=>window.testPad.buttons[9].pressed=true);await other.close();await page.bringToFront();await page.locator('#canvas').focus();
 await page.waitForTimeout(300);expect((await state(page)).screen).toBe('pause');await capture(page,'focus-return');await buttons(page,[]);await tap(page,9);
 await page.evaluate(()=>window.testPad.mapping='');await expect.poll(async()=>(await state(page)).input.status).toBe('unsupported');expect((await state(page)).screen).toBe('pause');await capture(page,'unsupported');
 await page.keyboard.press('Escape');expect((await state(page)).screen).toBe('training');
 const x=(await state(page)).world.player.x;await page.keyboard.down('ArrowRight');await expect.poll(async()=>(await state(page)).world.player.x).toBeGreaterThan(x+10);await page.keyboard.up('ArrowRight');
 await page.evaluate(()=>window.padMode='denied');await expect.poll(async()=>(await state(page)).input.status).toBe('unavailable');await capture(page,'unavailable');
 expect(faults).toEqual([]);
});

test('CONTROLLER gameplay all acts attacks death retry and mixed input',async({page})=>{
 const faults=errors(page);await boot(page);
 for(const act of [1,2,3]){
  await fixture(page,`act${act}-approach`);
  const x=(await state(page)).world.player.x;
  await buttons(page,[15]);await expect.poll(async()=>(await state(page)).world.player.x).toBeGreaterThan(x+10);await buttons(page,[]);
  await tap(page,0);await expect.poll(async()=>(await state(page)).world.player.grounded).toBe(false);await capture(page,`act${act}-jump`);
  await fixture(page,`act${act}-death`);await capture(page,`act${act}-death`);await tap(page,0);expect((await state(page)).screen).toBe('training');expect((await state(page)).world.player.hearts).toBe(3);await capture(page,`act${act}-retry`);
 }
 for(const act of [2,3]){
  await fixture(page,`act${act}-boss-close`);const hp=(await state(page)).world.targets[0].hp;await tap(page,2);
  await expect.poll(async()=>(await state(page)).world.targets[0].hp).toBeLessThan(hp);await capture(page,`act${act}-bat`);
  await fixture(page,`act${act}-boss-beam`);const beamHp=(await state(page)).world.targets[0].hp;await tap(page,3);
  await expect.poll(async()=>(await state(page)).world.targets[0].hp).toBeLessThan(beamHp);await capture(page,`act${act}-beam`);
 }
 await fixture(page,'act1-approach');const x=(await state(page)).world.player.x;
 await page.keyboard.down('ArrowLeft');await buttons(page,[15]);const neutral=(await state(page)).world.player.x;await page.waitForTimeout(200);expect((await state(page)).world.player.x).toBe(neutral);
 await page.keyboard.up('ArrowLeft');await expect.poll(async()=>(await state(page)).world.player.x).toBeGreaterThan(neutral);await buttons(page,[]);expect(faults).toEqual([]);
});
