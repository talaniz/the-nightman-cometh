// Ordinary keyboard driver: reads state, never writes game objects or uses QA.
const {expect}=require('@playwright/test');
const state=async page=>JSON.parse(await page.evaluate(()=>window.__nightmanGame));
async function driveBridge(page,{recovery=false,restart,choose,capture=async()=>{}}={}){
 const deadline=Date.now()+Number(process.env.NIGHTMAN_ROUTE_MS||240000);
 let forced=false,deaths=0;
 while(Date.now()<deadline){
  const s=await state(page),w=s.world,p=w.player;
  if(s.screen==='dialogue')break;
  if(s.screen==='dead'){
   deaths++;expect(deaths).toBeLessThan(5);await page.keyboard.press('Enter');continue;
  }
  if(recovery&&!forced&&w.boss_active){
   await page.keyboard.press('ArrowRight',{delay:650});
   await expect.poll(async()=>(await state(page)).screen,{timeout:60000}).toBe('dead');
   await capture(page,'act2-normal-death');await page.keyboard.press('Enter');
   await expect.poll(async()=>(await state(page)).world.player.hearts).toBe(3);
   expect((await state(page)).world.player.dayman).toBe(0);await capture(page,'act2-normal-retry');
   await restart(page);await choose(page,'Continue Act 2');
   expect((await state(page)).world.checkpoint).toBe(2800);expect((await state(page)).world.flags).toContain('preboss');forced=true;continue;
  }
  if(w.boss_active){
   const b=w.targets.find(t=>t.kind==='frank'),dx=b.x-p.x;
   // Short pulses avoid uncontrolled movement across slow browser IPC round trips.
   if(dx>60)await page.keyboard.press('ArrowRight',{delay:Math.min(100,(dx-52)/220*1000)});
   else if(dx<36){await page.keyboard.press('ArrowLeft',{delay:60});await page.keyboard.press('ArrowRight',{delay:10});}
   else {
    if(p.facing<0)await page.keyboard.press('ArrowRight',{delay:10});
    await page.keyboard.press('j');
    if(p.grounded&&w.targets.some(t=>t.kind==='sandwich'&&t.x-p.x>0&&t.x-p.x<110))await page.keyboard.press('Space');
   }
  }else{
   const edge=[1000,2200].find(edge=>edge-p.x>0&&edge-p.x<180);
   if(edge&&p.grounded&&edge-p.x<85){
    await Promise.all([page.keyboard.down('ArrowRight'),page.keyboard.press('Space')]);await page.waitForTimeout(650);await page.keyboard.up('ArrowRight');
   }else{
    const nearby=w.targets.some(t=>t.alive&&t.x-p.x>0&&t.x-p.x<115);
    if(p.grounded&&(nearby||Math.abs(1560-p.x)<70))await page.keyboard.press('Space');
    await page.keyboard.press('j');await page.keyboard.press('ArrowRight',{delay:edge?50:170});
   }
  }
 }
 const end=await state(page);expect(end.screen).toBe('dialogue');expect(end.world.complete).toBe(true);
 if(recovery)expect(forced).toBe(true);
 return {deaths,forced};
}
module.exports={driveBridge};
