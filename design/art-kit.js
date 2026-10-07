/* Daram Detective artwork: unmodified PNG atlases, clipped to their authored frames. */
(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src), ns = 'http://www.w3.org/2000/svg';
  let manifest, serial = 0;
  const read = path => fetch(new URL(path, base)).then(r => {
    if (!r.ok) throw Error('Art data could not load: ' + path);
    return r.json();
  });
  const ready = read('manifest.json?v=3').then(async m => {
    if (m.sceneMap) m.sceneData = await read(m.sceneMap + '?v=3');
    manifest = m;
    return m;
  });
  function frame(kind, id, expression = 0) {
    const item = manifest[kind][id];
    if (!item) throw Error('Unknown art id: ' + id);
    return { item, rect: item.frames[expression] || item.frames[0] };
  }
  function render(target, kind, id, expression = 0) {
    const { item, rect } = frame(kind, id, expression), svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', rect.join(' '));
    svg.setAttribute('preserveAspectRatio', kind === 'backgrounds' ? 'xMidYMid meet' : 'xMidYMax meet');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', item.name + (kind === 'characters' ? ' · ' + (item.labels?.[expression] || '기본 표정') : ''));
    svg.classList.add('daram-art');
    const defs = document.createElementNS(ns, 'defs'), clip = document.createElementNS(ns, 'clipPath'), clipRect = document.createElementNS(ns, 'rect'), clipId = 'daram-frame-' + (++serial);
    clip.id = clipId;
    ['x', 'y', 'width', 'height'].forEach((key, i) => clipRect.setAttribute(key, rect[i]));
    clip.append(clipRect); defs.append(clip); svg.append(defs);
    const image = document.createElementNS(ns, 'image');
    image.setAttribute('href', new URL(item.src, base).href);
    image.setAttribute('width', item.width); image.setAttribute('height', item.height);
    image.setAttribute('clip-path', 'url(#' + clipId + ')'); svg.append(image);
    target.replaceChildren(svg); target.dataset.artId = id; target.dataset.expression = expression;
    return svg;
  }
  function markup(kind, id, expression = 0) {
    const { item, rect } = frame(kind, id, expression), clipId = 'daram-markup-' + (++serial);
    const href = new URL(item.src, base).href.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
    return '<svg class="nodot" viewBox="' + rect.join(' ') + '" preserveAspectRatio="' + (kind === 'backgrounds' ? 'none' : 'xMidYMax meet') + '" aria-hidden="true" data-daram-art="' + id + '"><defs><clipPath id="' + clipId + '"><rect x="' + rect[0] + '" y="' + rect[1] + '" width="' + rect[2] + '" height="' + rect[3] + '"/></clipPath></defs><image href="' + href + '" width="' + item.width + '" height="' + item.height + '" clip-path="url(#' + clipId + ')"/></svg>';
  }
  window.DaramArtKit = {
    ready, base, get manifest() { return manifest; },
    character: (target, id, expression = 0) => render(target, 'characters', id, expression),
    background: (target, id) => render(target, 'backgrounds', id),
    characterMarkup: (id, expression = 0) => markup('characters', id, expression),
    sceneMarkup: id => markup('backgrounds', id),
    url: src => new URL(src, base).href
  };
})();
