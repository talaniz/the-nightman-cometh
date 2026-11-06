const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm'),fs=require('node:fs');
function fixture(getGamepads){
 const handlers={};
 const listen=(name,fn)=>(handlers[name] ||= []).push(fn);
 const context={window:{addEventListener:listen},navigator:{getGamepads},document:{hidden:false,hasFocus:()=>true,addEventListener:listen}};
 vm.runInNewContext(fs.readFileSync('game/web/gamepad.js','utf8'),context);
 const read=()=>JSON.parse(context.window.nightmanReadPad());
 read.emit=name=>(handlers[name]||[]).forEach(fn=>fn());
 return read;
}
function pad(mapping='standard'){return {connected:true,mapping,axes:[0,0],buttons:Array.from({length:17},()=>({pressed:false}))};}
test('bounded snapshot no identifiers, dead slot before replacement',()=>{
 const a=pad(),b=pad();a.id='private device name';let list=[a,b];const read=fixture(()=>list);
 assert.equal(read().slot,0);list=[null,b];assert.equal(read().status,'absent');assert.equal(read().slot,1);
 assert.equal(JSON.stringify(read()).includes('private'),false);
});
test('unsupported, missing and denied API fail safely',()=>{
 assert.equal(fixture(()=>[pad('')])().status,'unsupported');
 assert.equal(fixture(undefined)().status,'unavailable');
 assert.equal(fixture(()=>{throw new Error('denied')})().status,'unavailable');
 assert.equal(fixture(()=>[])().status,'absent');
});
test('nonfinite axes and large lists are bounded',()=>{
 const bad=pad();bad.axes[0]=NaN;assert.equal(fixture(()=>[bad])().status,'unavailable');
 const list=Array(16).fill(null).concat([pad()]);assert.equal(fixture(()=>list)().status,'absent');
});

test('brief blur is latched until the game samples it',()=>{
 const read=fixture(()=>[pad()]);read();read.emit('blur');
 assert.equal(read().interrupted,true);assert.equal(read().interrupted,false);
});
