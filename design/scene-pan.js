/* Horizontal investigation camera. Artwork and its targets share one canvas. */
(() => {
  'use strict';
  const controllers = new WeakMap(), positions = new Map();
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  function attach({viewport, canvas, left, right, progress, key = ''}) {
    if (controllers.has(viewport)) return controllers.get(viewport);
    viewport.classList.add('pan-scroll'); canvas.classList.add('pan-canvas');
    viewport.tabIndex = 0;
    viewport.setAttribute('role', 'region');
    viewport.setAttribute('aria-label', '좌우로 이동하며 현장 조사. 방향키 또는 드래그로 이동');
    let activeKey = key, max = -1, ratio = positions.get(key) ?? .5;
    let drag = null, suppressClickUntil = 0;
    const limit = () => Math.max(0, viewport.scrollWidth - viewport.clientWidth);
    function paint() {
      const end = limit(), x = viewport.scrollLeft;
      for (const [button, available] of [[left, x > 2], [right, x < end - 2]]) {
        if (!button) continue;
        button.hidden = !available; button.disabled = !available;
        button.classList.toggle('on', available);
      }
      if (progress) {
        progress.hidden = end <= 2;
        const thumb = progress.firstElementChild;
        thumb.style.width = viewport.clientWidth / viewport.scrollWidth * 100 + '%';
        thumb.style.left = x / viewport.scrollWidth * 100 + '%';
      }
      viewport.classList.toggle('can-pan', end > 2);
    }
    function layout() {
      if (!viewport.isConnected) { observer.disconnect(); return; }
      const end = limit();
      if (end !== max) { max = end; viewport.scrollLeft = ratio * end; }
      paint();
    }
    viewport.addEventListener('scroll', () => {
      const end = limit();
      if (end > 2) { ratio = viewport.scrollLeft / end; if (activeKey) positions.set(activeKey, ratio); }
      paint();
    }, {passive:true});
    function move(distance) {
      viewport._user = Date.now();
      viewport.scrollBy({left:distance, behavior:reduced() ? 'auto' : 'smooth'});
      paint();
    }
    for (const [button, sign] of [[left,-1],[right,1]]) if (button) {
      // Capture replaces, rather than duplicates, the source game's arrow handler.
      button.addEventListener('click', e => { e.preventDefault(); e.stopImmediatePropagation(); move(sign * viewport.clientWidth * .65); }, true);
    }
    viewport.addEventListener('keydown', e => {
      if (e.target !== viewport || limit() <= 2) return;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); move((e.key === 'ArrowLeft' ? -1 : 1) * viewport.clientWidth * .5); }
      if (e.key === 'Home' || e.key === 'End') { e.preventDefault(); move(e.key === 'Home' ? -viewport.scrollWidth : viewport.scrollWidth); }
    });
    viewport.addEventListener('wheel', e => {
      viewport._user = Date.now();
      if (e.shiftKey && Math.abs(e.deltaY) > Math.abs(e.deltaX) && limit() > 2) { e.preventDefault(); viewport.scrollLeft += e.deltaY; }
    }, {passive:false});
    viewport.addEventListener('pointerdown', e => {
      suppressClickUntil = 0;
      viewport._user = Date.now();
      // Touch uses browser scrolling, including swipes that begin on an item.
      if (e.pointerType === 'touch' || e.button !== 0 || limit() <= 2 || e.target.closest('button,a,input,select')) return;
      drag = {id:e.pointerId, x:e.clientX, y:e.clientY, scroll:viewport.scrollLeft, moved:false};
      e.stopPropagation();
    }, true);
    viewport.addEventListener('pointermove', e => {
      if (!drag || drag.id !== e.pointerId) return;
      if (!e.buttons) { drag = null; viewport.classList.remove('dragging'); return; }
      const dx = e.clientX - drag.x;
      if (!drag.moved && Math.abs(dx) <= 6) return;
      if (!drag.moved && Math.abs(dx) < Math.abs(e.clientY - drag.y)) { drag = null; return; }
      drag.moved = true; viewport.classList.add('dragging');
      viewport.setPointerCapture(e.pointerId); e.preventDefault();
      viewport.scrollLeft = drag.scroll - dx;
    });
    function finish(e) {
      if (!drag || drag.id !== e.pointerId) return;
      if (drag.moved) suppressClickUntil = Date.now() + 400;
      drag = null; viewport.classList.remove('dragging');
      if (viewport.hasPointerCapture(e.pointerId)) viewport.releasePointerCapture(e.pointerId);
    }
    for (const event of ['pointerup','pointercancel','lostpointercapture']) viewport.addEventListener(event, finish);
    viewport.addEventListener('click', e => {
      if (Date.now() < suppressClickUntil) { e.preventDefault(); e.stopImmediatePropagation(); }
    }, true);
    const observer = new ResizeObserver(layout); observer.observe(viewport); observer.observe(canvas);
    const control = {setKey(next) { activeKey = next; ratio = positions.get(next) ?? .5; max = limit(); viewport.scrollLeft = ratio * max; paint(); }};
    controllers.set(viewport, control); requestAnimationFrame(layout); return control;
  }
  let watching = false;
  function watchGame() {
    if (watching) return; watching = true;
    let last = null, queued = false;
    function scan() {
      queued = false;
      const viewport = document.getElementById('fsscroll'), canvas = document.getElementById('bigscene');
      if (!viewport || !canvas || viewport === last) return;
      last = viewport;
      attach({viewport,canvas,left:document.getElementById('fsal'),right:document.getElementById('fsar'),key:'game:' + canvas.querySelector('svg[data-daram-art]')?.dataset.daramArt});
    }
    new MutationObserver(() => { if (!queued) { queued = true; requestAnimationFrame(scan); } }).observe(document.body, {childList:true,subtree:true});
    scan();
  }
  window.DaramScenePan = {attach, watchGame};
})();
