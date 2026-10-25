// Shared by the actual page loader and Node behavior tests.
class BootState {
  constructor(){ this.state='loading'; this.elapsed=0; this.starts=0; }
  tick(seconds){
    if (!Number.isFinite(seconds) || seconds < 0) throw new Error('Invalid elapsed time');
    if (this.state==='loading') { this.elapsed+=seconds; if(this.elapsed>=60)this.fail(); }
  }
  progress(){ if(this.state==='loading')this.elapsed=0; }
  fail(){ if(this.state!=='ready')this.state='error'; }
  ready(){ if(this.state==='loading'){ this.state='ready';this.starts+=1; } }
  retry(){ this.state='loading';this.elapsed=0; }
}
if (typeof module !== 'undefined') module.exports = {BootState};
else window.BootState = BootState;
