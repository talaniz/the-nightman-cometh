(() => {
  const boot = new BootState();
  window.nightmanBoot=boot;
  let message='Loading the stage…', engaged=false;
  const fail=()=>{boot.fail();message='The stage could not load. Check your connection, then retry.';render();};
  const nativeFetch=window.fetch.bind(window);
  window.fetch=async (...args)=>{
    try {
      const response=await nativeFetch(...args);
      if(!response.ok && response.status!==304) fail();
      else boot.progress();
      return response;
    } catch(error){fail();throw error;}
  };
  window.addEventListener('error', event=>{
    if(event.target?.tagName==='SCRIPT' || event.error)fail();
  },true);
  window.addEventListener('unhandledrejection',fail);
  function render(){
    const panel=document.getElementById('loader');if(!panel)return;
    const button=document.getElementById('boot-action');
    document.getElementById('boot-status').textContent=message;
    panel.hidden=boot.state==='ready';
    button.textContent=boot.state==='error'?'Retry':(window.MM?'Enter the theatre':'Loading runtime…');
    button.disabled=boot.state!=='error' && !window.MM;
  }
  window.addEventListener('DOMContentLoaded',()=>{
    document.getElementById('boot-action').addEventListener('click',()=>{
      if(boot.state==='error'){
        window.onbeforeunload=null;location.reload();return;
      }
      engaged=true;boot.progress();message='Opening the curtains…';render();
    });
    render();
  });
  setInterval(()=>{
    if(window.__nightmanGame){boot.ready();document.getElementById('canvas')?.setAttribute('aria-label','Nightman game. Arrow keys move, Space jumps, Escape pauses.');}
    else if(!window.MM || engaged)boot.tick(.25);
    if(boot.state==='error')message='The stage could not load. Check your connection, then retry.';
    else if(window.MM && !engaged)message='The stage is ready. Enter the theatre to begin.';
    render();
  },250);
})();
