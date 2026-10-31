const {test,expect}=require('@playwright/test');
test.use({video:process.env.NIGHTMAN_VIDEO==='1'?'on':'off'});
const fs=require('node:fs'),path=require('node:path');
const state=async p=>JSON.parse(await p.evaluate(()=>window.__nightmanGame));
async function boot(p){await p.goto('/');await expect(p.locator('#boot-action')).toBeEnabled({timeout:120000});await p.locator('#boot-action').click();await p.waitForFunction(()=>!!window.__nightmanGame,{},{timeout:120000});await p.locator('#canvas').focus();}
async function shot(p,name){if(!process.env.NIGHTMAN_EVIDENCE)return;const d=process.env.NIGHTMAN_EVIDENCE;fs.mkdirSync(d,{recursive:true});await p.screenshot({path:path.join(d,name+'.png')});fs.writeFileSync(path.join(d,name+'.json'),JSON.stringify({viewport:p.viewportSize(),browser:p.context().browser().version(),test:test.info().title,build:process.env.NIGHTMAN_BUILD,state:await state(p)},null,2));}
async function move(p,x){for(let i=0;i<70;i++){const w=(await state(p)).world;if(w.dead)throw Error('Player died while travelling to '+x);const dx=x-w.player.x;if(Math.abs(dx)<12)return;await p.keyboard.press(dx>0?'ArrowRight':'ArrowLeft',{delay:Math.min(140,Math.abs(dx)/220*1000)});await p.keyboard.press('j');}throw Error('Failed to reach '+x);}
async function land(p,x,top){await move(p,x);await p.keyboard.press('Space');await expect.poll(async()=>{const a=(await state(p)).world.player;return a.grounded&&Math.abs(a.y+44-top)<1;},{timeout:6000}).toBe(true);}
async function transfer(p,label,top,direction,target){
 await expect.poll(async()=>(await state(p)).world.player.grounded).toBe(true);
 await Promise.all([p.keyboard.down(direction),p.keyboard.press('Space')]);
 try {await expect.poll(async()=>{const a=(await state(p)).world.player;return direction==='ArrowRight'?a.x>=target:a.x<=target;},{timeout:10000,intervals:[50]}).toBe(true);}
 finally {await p.keyboard.up(direction);}
 await expect.poll(async()=>{const a=(await state(p)).world.player;return a.grounded&&Math.abs(a.y+44-top)<1;},{timeout:6000}).toBe(true);
 await shot(p,'platform-'+label);
}
function monitor(p){const errors=[];p.on('pageerror',e=>errors.push(String(e)));p.on('requestfailed',r=>errors.push(r.url()+' '+r.failure()?.errorText));p.on('console',m=>{if(m.type()==='error'&&!m.text().includes('MEDIA USER ACTION REQUIRED'))errors.push(m.text());});return errors;}


test('POLISH real keyboard raised route and mounted art',async({page})=>{
 test.setTimeout(600000);const errors=monitor(page);await boot(page);await page.keyboard.press('Enter');await page.waitForTimeout(100);await page.keyboard.press('Escape');
 await move(page,420);await shot(page,'billboard-and-sign');
 // Fixtures isolate geometry from combat; all landings still require real keyboard jumps.
 await page.evaluate(()=>window.__nightmanFixture=JSON.stringify({name:'act1-platform-first'}));await page.waitForTimeout(150);
 await land(page,720,360);await shot(page,'first-platform-landed');await land(page,805,360);await shot(page,'first-platform-launch');
 await transfer(page,'upper',300,'ArrowRight',910);
 await transfer(page,'return',360,'ArrowLeft',805);
 await page.evaluate(()=>window.__nightmanFixture=JSON.stringify({name:'act1-platform-second'}));await page.waitForTimeout(150);
 await land(page,2080,360);await land(page,2184,360);await transfer(page,'second-upper',300,'ArrowRight',2310);
 await transfer(page,'second-return',360,'ArrowLeft',2180);
 await page.evaluate(()=>window.__nightmanFixture=JSON.stringify({name:'act1-platform-third'}));await page.waitForTimeout(150);
 await land(page,2860,350);await shot(page,'third-platform-landed');
 await page.setViewportSize({width:1920,height:1080});await shot(page,'platforms-1920');
 await page.setViewportSize({width:390,height:844});await shot(page,'narrow-guidance');expect(errors).toEqual([]);
});

test('POLISH live weapon and creature motion plus pause',async({page})=>{
 const errors=monitor(page);await boot(page);expect((await state(page)).test_build).toBe(true);
 await page.evaluate(()=>window.__nightmanFixture=JSON.stringify({name:'act1-approach'}));await page.waitForTimeout(150);
 await move(page,420);await page.keyboard.press('j');await shot(page,'swing-live');
 await page.keyboard.press('ArrowLeft',{delay:35});await page.keyboard.press('j');await page.waitForTimeout(70);await shot(page,'swing-left-live');
 await page.keyboard.press('Space');await page.keyboard.press('j');await shot(page,'swing-jump-live');
 await page.keyboard.press('Escape');const before=(await state(page)).world;await page.waitForTimeout(400);expect((await state(page)).world).toEqual(before);await shot(page,'paused-animation');
 await page.keyboard.press('Escape');
 // Existing midpoint fixture is diagnostic only; then actual keyboard travel shows the Wolf ad.
 await page.evaluate(()=>window.__nightmanFixture=JSON.stringify({name:'act1-mid'}));await page.waitForTimeout(150);
 await move(page,1560);await shot(page,'wolf-billboard');
 await page.evaluate(()=>window.__nightmanFixture=JSON.stringify({name:'act1-pose-bat'}));await page.waitForTimeout(150);await shot(page,'bat-strike-browser-pose');
 expect(errors).toEqual([]);
});
