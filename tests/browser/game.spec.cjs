const {test,expect}=require('@playwright/test');
const fs=require('node:fs');const path=require('node:path');
const evidence=process.env.NIGHTMAN_EVIDENCE;
if(evidence)fs.mkdirSync(evidence,{recursive:true});
const port=process.env.NIGHTMAN_PORT||'8773';
async function state(page){return JSON.parse(await page.evaluate(()=>window.__nightmanGame));}
async function capture(page,name){
 if(!evidence)return;fs.mkdirSync(evidence,{recursive:true});
 await page.screenshot({path:path.join(evidence,name+'.png')});
 fs.writeFileSync(path.join(evidence,name+'.json'),JSON.stringify({viewport:page.viewportSize(),state:await state(page)},null,2));
}
async function boot(page){
 await page.goto('/');await expect(page.locator('#boot-action')).toBeEnabled({timeout:120000});
 await page.locator('#boot-action').click();await page.waitForFunction(()=>Boolean(window.__nightmanGame),{},{timeout:120000});
 await expect(page.locator('#loader')).toBeHidden({timeout:10000});await page.locator('#canvas').focus();
}
async function press(page,key,ms=160){await page.keyboard.press(key);await page.waitForTimeout(ms);}
async function menu(page,label){
 const s=await state(page);const index=s.menu.indexOf(label);expect(index).toBeGreaterThanOrEqual(0);
 for(let n=0;n<(index-s.selection+s.menu.length)%s.menu.length;n++)await press(page,'ArrowDown',30);
 await press(page,'Enter');
}
async function fixture(page,name){await page.evaluate(n=>window.__nightmanFixture=JSON.stringify({name:n}),name);await page.waitForTimeout(200);}
function monitor(page){
 const errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 page.on('requestfailed',r=>errors.push(r.url()+' '+r.failure()?.errorText));
 page.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))errors.push(m.text());});
 return errors;
}
test('BOOT SMOKE cold load menus movement and pause',async({page})=>{
 const errors=monitor(page);await boot(page);
 const box=await page.locator('#canvas').boundingBox();expect(box.width/box.height).toBeCloseTo(16/9,1);
 await capture(page,'title-1280');
 await menu(page,'Start new rehearsal');expect((await state(page)).screen).toBe('dialogue');await capture(page,'dialogue-1280');
 await press(page,'Escape');expect((await state(page)).screen).toBe('training');
 const start=(await state(page)).world.player.x;
 await page.keyboard.down('ArrowRight');await page.waitForTimeout(500);await page.keyboard.up('ArrowRight');
 expect((await state(page)).world.player.x).toBeGreaterThan(start);await capture(page,'training-1280');
 await press(page,'Space');await capture(page,'jump-1280');
 await press(page,'Escape');expect((await state(page)).screen).toBe('pause');await capture(page,'pause-1280');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'desktop-1920');
 await page.setViewportSize({width:390,height:844});await expect(page.locator('#narrow')).toBeVisible();await capture(page,'narrow-390');
 expect((await state(page)).loops).toBe(1);expect(errors).toEqual([]);
});
test('BOOT blocked runtime shows error and retry recovers',async({page})=>{
 await page.route('**/pythons.js',r=>r.abort());await page.goto('/');
 await expect(page.locator('#boot-action')).toHaveText('Retry',{timeout:10000});
 if(evidence){fs.mkdirSync(evidence,{recursive:true});await page.screenshot({path:path.join(evidence,'boot-error-1280.png')});}
 await page.unroute('**/pythons.js');await page.locator('#boot-action').click();
 await expect(page.locator('#boot-action')).toHaveText('Enter the theatre',{timeout:120000});
 await page.locator('#boot-action').click();await page.waitForFunction(()=>Boolean(window.__nightmanGame),{},{timeout:120000});
 expect((await state(page)).loops).toBe(1);
});
test('BOOT localhost canonicalizes before dependency startup',async({page})=>{
 const bad=[];page.on('request',r=>{if(r.url().includes('localhost:8000'))bad.push(r.url());});
 await page.goto(`http://localhost:${port}`);await expect(page).toHaveURL(`http://127.0.0.1:${port}/`);
 await expect(page.locator('#boot-action')).toBeEnabled({timeout:120000});await page.locator('#boot-action').click();
 await page.waitForFunction(()=>Boolean(window.__nightmanGame),{},{timeout:120000});expect(bad).toEqual([]);
});
test('CORE bat stomp food flags death transformation and blur',async({page})=>{
 const errors=monitor(page);await boot(page);expect((await state(page)).test_build).toBe(true);
 await fixture(page,'bat');await capture(page,'bat-idle-1280');await press(page,'j',100);await capture(page,'bat-swing-1280');
 expect((await state(page)).world.targets[0].alive).toBe(false);
 await fixture(page,'stomp');await page.waitForTimeout(300);expect((await state(page)).world.targets[0].alive).toBe(false);await capture(page,'stomp-1280');
 await fixture(page,'side');expect((await state(page)).world.player.hearts).toBe(2);await capture(page,'damage-1280');
 await fixture(page,'food');await page.keyboard.down('ArrowRight');await page.waitForTimeout(160);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.hearts).toBe(3);await capture(page,'food-1280');
 await fixture(page,'full-food');await page.keyboard.down('ArrowRight');await page.waitForTimeout(160);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.hearts).toBe(3);await capture(page,'full-food-1280');
 await fixture(page,'flag');await page.keyboard.down('ArrowRight');await page.waitForTimeout(200);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.hearts).toBe(2);await capture(page,'flag-first-1280');
 await fixture(page,'repeat-flag');await page.keyboard.down('ArrowRight');await page.waitForTimeout(200);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.hearts).toBe(1);await capture(page,'flag-repeat-1280');
 await fixture(page,'death');expect((await state(page)).screen).toBe('dead');await capture(page,'death-1280');await press(page,'Enter');
 expect((await state(page)).world.player.hearts).toBe(3);expect((await state(page)).world.checkpoint).toBe(400);await capture(page,'retry-1280');
 await fixture(page,'meal');await page.keyboard.down('ArrowRight');await page.waitForTimeout(160);await page.keyboard.up('ArrowRight');
 expect((await state(page)).world.player.dayman).toBeGreaterThan(9);await capture(page,'meal-dayman-1280');
 await press(page,'k',80);const beams=(await state(page)).world.beams;expect(beams.length).toBe(1);expect(beams[0].dy).toBe(0);await capture(page,'beam-1280');
 await page.keyboard.down('ArrowRight');await page.evaluate(()=>window.dispatchEvent(new Event('blur')));await page.waitForTimeout(150);
 expect((await state(page)).screen).toBe('pause');const timer=(await state(page)).world.player.dayman;await page.waitForTimeout(400);expect((await state(page)).world.player.dayman).toBe(timer);
 await page.keyboard.up('ArrowRight');await page.evaluate(()=>window.dispatchEvent(new Event('focus')));await press(page,'Escape');const x=(await state(page)).world.player.x;await page.waitForTimeout(300);expect((await state(page)).world.player.x).toBe(x);
 await page.waitForTimeout(11000);expect((await state(page)).world.player.dayman).toBe(0);expect((await state(page)).audio.playing).toBe('little-boy');await capture(page,'expired-1280');expect(errors).toEqual([]);
});
test('SHELL keyboard settings QA isolation dialogue replay and reload',async({page})=>{
 const errors=monitor(page);await boot(page);await menu(page,'Options');await press(page,'ArrowLeft');expect((await state(page)).settings.music).toBe(.6);await capture(page,'options-1280');await press(page,'Escape');
 await menu(page,'Password');await page.keyboard.type('BAD');await press(page,'Enter');expect((await state(page)).message).toContain('Unknown');await capture(page,'invalid-password-1280');
 await page.keyboard.press('Backspace');await page.keyboard.press('Backspace');await page.keyboard.press('Backspace');await page.keyboard.type('TROLLTOLL');await press(page,'Enter');expect((await state(page)).qa).toBe(true);await capture(page,'qa-1280');
 const before=await page.evaluate(()=>localStorage.getItem('nightman.progress.v1'));
 await press(page,'Escape');await menu(page,'QA checkpoint');await press(page,'Escape');await menu(page,'Exit QA');expect((await state(page)).qa).toBe(false);
 expect(await page.evaluate(()=>localStorage.getItem('nightman.progress.v1'))).toBe(before);
 await menu(page,'Replay dialogue');await press(page,'Escape');expect((await state(page)).screen).toBe('title');
 await menu(page,'Start new rehearsal');expect((await state(page)).screen).toBe('confirm');await capture(page,'new-game-confirm-1280');await menu(page,'Start fresh');await press(page,'Escape');
 // Save a real normal checkpoint by ordinary keyboard movement.
 await page.keyboard.down('ArrowRight');await page.waitForTimeout(1550);await page.keyboard.up('ArrowRight');expect((await state(page)).world.flags).toContain('mid');
 await page.evaluate(()=>window.onbeforeunload=null);await page.goto('about:blank');await boot(page);await menu(page,'Continue rehearsal');expect((await state(page)).world.checkpoint).toBe(400);expect((await state(page)).world.flags).toContain('mid');expect(errors).toEqual([]);
});
test('SHELL corrupt and disabled storage keep game usable',async({page})=>{
 await page.addInitScript(()=>localStorage.setItem('nightman.progress.v1','{broken'));
 await boot(page);expect((await state(page)).message).toContain('Save unavailable');await capture(page,'save-error-1280');await menu(page,'Start new rehearsal');await press(page,'Escape');expect((await state(page)).screen).toBe('training');
});
test('SHELL storage disabled and audio failure remain recoverable',async({page})=>{
 await page.addInitScript(()=>{
  Storage.prototype.getItem=function(){throw new Error('disabled storage fixture');};
  Storage.prototype.setItem=function(){throw new Error('disabled storage fixture');};
 });
 await boot(page);expect((await state(page)).message).toContain('Save unavailable');
 await menu(page,'Start new rehearsal');await press(page,'Escape');expect((await state(page)).screen).toBe('training');
 await capture(page,'storage-disabled-1280');
 await fixture(page,'audio-error');expect((await state(page)).audio.error).not.toBe('');await capture(page,'audio-error-1280');
 const x=(await state(page)).world.player.x;await page.keyboard.down('ArrowRight');await page.waitForTimeout(200);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.x).toBeGreaterThan(x);
 await press(page,'r',400);expect((await state(page)).audio.error).toBe('');await capture(page,'audio-recovered-1280');
});
test('BOOT missing package and stalled runtime expose retry',async({page})=>{
 await page.route('**/nightman.tar.gz',r=>r.fulfill({status:404,body:'fixture missing'}));await page.goto('/');
 await expect(page.locator('#boot-action')).toBeEnabled({timeout:120000});await page.locator('#boot-action').click();
 await expect(page.locator('#boot-action')).toHaveText('Retry',{timeout:120000});
 if(evidence)await page.screenshot({path:path.join(evidence,'asset-load-error-1280.png')});
 // Actual stalled script request; loader's own 60-second timer must recover.
 await page.evaluate(()=>window.onbeforeunload=null);await page.unroute('**/nightman.tar.gz');
 await page.route('**/pythons.js',async r=>{await new Promise(resolve=>setTimeout(resolve,70000));await r.abort().catch(()=>{});});
 await page.goto('/',{waitUntil:'commit'});
 await expect(page.locator('#boot-action')).toHaveText('Retry',{timeout:80000});
 if(evidence)await page.screenshot({path:path.join(evidence,'startup-timeout-1280.png')});
});

test('AUDIO SMOKE mute restores playback without restarting gameplay',async({page})=>{
 const errors=monitor(page);await boot(page);await menu(page,'Start new rehearsal');await press(page,'Escape');
 await press(page,'m');expect((await state(page)).audio.muted).toBe(true);await capture(page,'muted-1280');
 const x=(await state(page)).world.player.x;await page.keyboard.down('ArrowRight');await page.waitForTimeout(200);await page.keyboard.up('ArrowRight');expect((await state(page)).world.player.x).toBeGreaterThan(x);
 await press(page,'m');expect((await state(page)).audio.muted).toBe(false);expect((await state(page)).audio.playing).toBe('little-boy');expect(errors).toEqual([]);
});
