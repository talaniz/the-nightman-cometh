const {test} = require('node:test');
const assert = require('node:assert/strict');
const {BootState} = require('../../game/web/boot-state.js');
test('stalled boot gives recoverable error',()=>{
 const state=new BootState();state.tick(61);assert.equal(state.state,'error');
 state.retry();assert.equal(state.state,'loading');assert.equal(state.elapsed,0);
});
test('failure and idempotent ready',()=>{
 const state=new BootState();state.fail();assert.equal(state.state,'error');
 state.retry();state.ready();state.ready();assert.equal(state.starts,1);
});
