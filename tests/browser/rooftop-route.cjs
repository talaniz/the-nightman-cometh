// Actual keyboard only. No passwords, fixture writes or invincibility.
const {expect}=require('@playwright/test');
const state=async p=>JSON.parse(await p.evaluate(()=>window.__nightmanGame));
async function driveRooftop(page,{recovery=false,restart,choose,capture=async()=>{}}={}){
 const deadline=Date.now()+Number(process.env.NIGHTMAN_ROUTE_MS||240000);
 let forced=false,deaths=0;
 while(Date.now()<deadline){
  const s=await state(page),w=s.world,p=w.player;
  expect(s.qa).toBe(false);
  if(s.screen==='dialogue')break;
  if(s.screen==='dead'){
   deaths++;expect(deaths).toBeLessThan(5);await page.keyboard.press('Enter');
   await expect.poll(async()=>(await state(page)).screen).toBe('training');continue;
  }
  if(recovery&&!forced&&w.boss_active){
   // Stand in the boss lane without attacking; accept real damage until death.
   await expect.poll(async()=>(await state(page)).screen,{timeout:90000}).toBe('dead');
   await capture(page,'act3-normal-death');await page.keyboard.press('Enter');
   await expect.poll(async()=>(await state(page)).screen).toBe('training');
   const retry=(await state(page)).world;expect(retry.player.hearts).toBe(3);expect(retry.player.dayman).toBe(0);
   expect(retry.checkpoint).toBe(3000);await capture(page,'act3-normal-retry');
   await restart(page);await choose(page,'Continue Act 3');expect((await state(page)).world.checkpoint).toBe(3000);
   forced=true;continue;
  }
  if(w.boss_active){
   expect(p.dayman).toBe(0);expect(w.beams).toEqual([]);
   const b=w.targets.find(t=>t.kind==='nightman'),dx=b.x-p.x;
   if(p.grounded&&Math.abs(dx)<190)await page.keyboard.press('Space');
   await page.keyboard.press('j');
   if(Math.abs(dx)>42)await page.keyboard.press(dx>0?'ArrowRight':'ArrowLeft',{delay:Math.min(85,(Math.abs(dx)-35)/220*1000)});
   else if((p.facing>0)!==(dx>0))await page.keyboard.press(dx>0?'ArrowRight':'ArrowLeft',{delay:10});
   else await page.waitForTimeout(45);
  }else{
   const edge=[1100,2350].find(x=>x-p.x>0&&x-p.x<180);
   if(edge&&p.grounded&&edge-p.x<85){
    await Promise.all([page.keyboard.down('ArrowRight'),page.keyboard.press('Space')]);
    await page.waitForTimeout(650);await page.keyboard.up('ArrowRight');
   }else{
    const nearby=w.targets.some(t=>t.alive&&t.x-p.x>0&&t.x-p.x<115&&Math.abs(t.y-p.y)<70);
    if(p.grounded&&(nearby||Math.abs(1660-p.x)<80))await page.keyboard.press('Space');
    await page.keyboard.press('j');await page.keyboard.press('ArrowRight',{delay:edge?50:150});
   }
  }
 }
 const end=await state(page);expect(end.screen).toBe('dialogue');expect(end.world.act).toBe('act3');expect(end.world.complete).toBe(true);
 if(recovery)expect(forced).toBe(true);
 return {deaths,forced};
}
module.exports={driveRooftop};
