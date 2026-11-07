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

test('M8 Cricket brakes reverses and crashes into the dumpster',async({page})=>{
 await boot(page);await capture(page,'title-1280');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'title-1920');
 await page.setViewportSize({width:390,height:844});await capture(page,'title-narrow');
 await page.setViewportSize({width:1280,height:720});await fixture(page,'act1-boss-warning');
 await expect.poll(async()=>(await state(page)).world.targets[0].state,{timeout:10000,intervals:[50]}).toBe('brake');
 const braking=(await state(page)).world.targets[0];expect(braking.direction).toBe(-1);
 await capture(page,'cricket-braking');
 await expect.poll(async()=>(await state(page)).world.targets[0].direction,{intervals:[50]}).toBe(1);
 await capture(page,'cricket-reversed');
 await expect.poll(async()=>(await state(page)).world.targets[0].state,{intervals:[50]}).toBe('stunned');
 expect((await state(page)).world.targets[0].x).toBe(4950);await capture(page,'dumpster-crash');
 await page.setViewportSize({width:1920,height:1080});await capture(page,'dumpster-1920');
});

test('M8 transformation is automatic and proposal advances by click only once',async({page})=>{
 await boot(page);await fixture(page,'act3-finale-0');await capture(page,'dennis-before');
 await page.keyboard.press('Enter');await expect.poll(async()=>(await state(page)).dialogue).toBe(1);
 await capture(page,'first-flash');await page.waitForTimeout(1100);await capture(page,'color-wash');
 await page.keyboard.press('Enter');expect((await state(page)).dialogue).toBe(1);
 await expect.poll(async()=>(await state(page)).dialogue,{timeout:7000}).toBe(2);
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
