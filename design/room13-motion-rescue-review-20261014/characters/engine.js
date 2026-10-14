/* Declarative motion math, independent of the DOM. */
(function (root, factory) {
  const engine = factory();
  if (typeof module === 'object' && module.exports) module.exports = engine;
  else root.DaramMotion = engine;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const defaults = { x: 0, y: 0, rotation: 0, scaleX: 1, scaleY: 1, opacity: 1 };
  const clamp = (x, lo, hi) => Math.min(hi, Math.max(lo, x));
  const frameImage = f => f.image || { src: f.src, crop: f.sourceRect };
  const frameKey = f => JSON.stringify([frameImage(f).src, f.sourceRect || frameImage(f).crop, f.rect]);
  function hasMotion(state) {
    const frames = state.frames || [];
    if (frames.length > 1 && new Set(frames.map(frameKey)).size > 1) return true;
    return [...(state.layers || []), ...(state.bodyMotion ? [state.bodyMotion] : [])].some(l => l.keyframes?.length > 1 &&
      Object.keys(defaults).some(k => new Set(l.keyframes.map(f => f[k] ?? defaults[k])).size > 1));
  }
  function status(state) {
    if (!state || (!state.pose && !(state.frames?.length))) return 'pending';
    if (!hasMotion(state)) return 'pose_only';
    return state.status === 'ready' && state.quality?.poseReviewed && state.quality?.motionReviewed ? 'ready' : 'motion_draft';
  }
  function duration(state) {
    if (state.frames?.length) return state.frames.reduce((sum, f) => sum + Math.max(1, f.durationMs || 100), 0);
    return Math.max(1, state.timing?.durationMs || 3200);
  }
  function phase(ms, timing, fallback = 3200) {
    const d = Math.max(1, timing?.durationMs || fallback);
    return timing?.loop === false ? clamp(ms / d, 0, 1) : ((Math.max(0, ms) % d) / d);
  }
  function frameAt(state, ms, reduced = false) {
    const frames = state.frames || [];
    if (!frames.length) return null;
    if (reduced) return frames[state.reducedMotionFrame ?? (frames.length - 1)] || frames[frames.length - 1];
    const d = duration(state); let time = state.timing?.loop === false ? Math.min(Math.max(ms, 0), d - .001) : (Math.max(ms, 0) % d);
    for (const frame of frames) { const span = Math.max(1, frame.durationMs || 100); if (time < span) return frame; time -= span; }
    return frames[frames.length - 1];
  }
  function transformAt(keyframes, progress) {
    if (!keyframes?.length) return {...defaults};
    const frames = [...keyframes].sort((a,b) => a.at - b.at); const p=clamp(progress,0,1);
    let a=frames[0], b=frames[frames.length-1];
    if (p <= a.at) return {...defaults,...a};
    if (p >= b.at) return {...defaults,...b};
    for (let i=1;i<frames.length;i++) if(p<=frames[i].at){a=frames[i-1];b=frames[i];break;}
    const t=(p-a.at)/(b.at-a.at || 1); const out={};
    for(const k of Object.keys(defaults)) out[k]=(a[k]??defaults[k])+((b[k]??defaults[k])-(a[k]??defaults[k]))*t;
    return out;
  }
  function layerTransform(layer,state,ms,reduced) {
    const p = reduced ? (layer.reducedMotionAt ?? 0) : phase(ms,layer.timing||state.timing,duration(state));
    return transformAt(layer.keyframes,p);
  }
  return {clamp,hasMotion,status,duration,phase,frameAt,frameImage,transformAt,layerTransform};
});
