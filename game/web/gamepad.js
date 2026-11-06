/* One bounded snapshot per game frame. No device identifiers are persisted. */
(() => {
  let active = null, interrupted = false;
  window.addEventListener('blur', () => { interrupted = true; });
  document.addEventListener('visibilitychange', () => { if (document.hidden) interrupted = true; });
  function read() {
    const focused = !document.hidden && document.hasFocus();
    try {
      if (typeof navigator.getGamepads !== 'function') return {status: 'unavailable', focused};
      const pads = Array.from(navigator.getGamepads()).slice(0, 16);
      const supported = p => p && p.connected && p.mapping === 'standard' &&
        p.buttons && p.buttons.length >= 16 && p.axes && p.axes.length >= 2;
      // Keep the selected slot stable. A lost slot is reported before selecting another.
      if (active !== null && !supported(pads[active])) {
        active = null;
        return {status: 'absent', focused};
      }
      if (active === null) active = pads.findIndex(supported);
      if (active < 0) {
        active = null;
        return {status: pads.some(p => p && p.connected) ? 'unsupported' : 'absent', focused};
      }
      const pad = pads[active];
      const axes = Array.from(pad.axes).slice(0, 2);
      if (!axes.every(a => typeof a === 'number' && Number.isFinite(a) && Math.abs(a) <= 1))
        return {status: 'unavailable', focused};
      const buttons = Array.from({length: 17}, (_, i) => pad.buttons[i]?.pressed === true);
      return {status: 'connected', slot: active, axes, buttons, focused};
    } catch (_) {
      active = null;
      return {status: 'unavailable', focused};
    }
  }
  window.nightmanReadPad = () => {
    const snapshot = read();
    snapshot.interrupted = interrupted;
    interrupted = false;
    return JSON.stringify(snapshot);
  };
})();
