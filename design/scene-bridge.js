/* Call inside the original game's closure, after its patches finish. */
(() => {
  'use strict';
  async function install({ cases, scenes, hots, zooms, zoomArt, portraitSetter, portraitFallback, refresh }) {
    const m = await DaramArtKit.ready, source = m.sceneData;
    let count = 0;
    for (const key of source.locationOrder) {
      const record = source.locations[key], c = cases.find(c => c.id === record.caseId), l = c?.locations.find(l => l.id === record.locationId);
      if (!l || !m.backgrounds[key]) continue;
      scenes[key] = () => DaramArtKit.sceneMarkup(key);
      for (const e of record.evidence) {
        const live = l.spots.find(s => s.id === e.spotId && s.ev.id === e.evidenceId);
        if (!live) throw Error('Evidence ID mismatch: ' + key + '/' + e.spotId);
        hots[e.spotId] = e.point.slice();
      }
      for (const o of record.observations) {
        const live = l.obs?.find(i => i.id === o.id);
        if (live) { live.x = o.point[0]; live.y = o.point[1]; }
      }
      if (zooms) for (const [zk, z] of Object.entries(record.zooms)) {
        const live = zooms[zk];
        if (!live) continue;
        for (const it of z.items) {
          const item = live.items.find(i => i.id === it.id);
          if (item) { item.x = it.x; item.y = it.y; }
        }
      }
      count++;
    }
    if (zoomArt && zooms) for (const [zk, id] of Object.entries(m.zoomBackgrounds || {})) {
      if (zooms[zk] && m.backgrounds[id]) {
        const artKey = 'daram-art-' + zk;
        zooms[zk].art = artKey;
        zoomArt[artKey] = () => DaramArtKit.sceneMarkup(id);
      }
    }
    if (portraitSetter && portraitFallback) portraitSetter((id, mood) => {
      if (!m.characters[id] || id === 'daram') return portraitFallback(id, mood);
      const expression = /think|doubt|confused/.test(mood || '') ? 1 : /nervous|shy|sad|cry|angry|shock|panic/.test(mood || '') ? 2 : 0;
      // Testimony icons reuse pf's inner content in a 100×101 viewport.
      // Normalize with a group, so the game's generic SVG CSS cannot resize a nested viewport.
      const frame = m.characters[id].frames[expression] || m.characters[id].frames[0];
      const scale = Math.min(100 / frame[2], 101 / frame[3]);
      const tx = (100 - frame[2] * scale) / 2 - frame[0] * scale;
      const ty = 101 - frame[3] * scale - frame[1] * scale;
      const content = DaramArtKit.characterMarkup(id, expression).replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
      const marker = 'daram-npc-' + content.match(/id="([^"]+)"/)[1];
      // The original dot converter skips groups with IDs; these PNGs are already authored pixel art.
      return '<svg viewBox="0 0 100 101" aria-hidden="true" data-daram-art="' + id + '"><g id="' + marker + '" class="nodot" transform="matrix(' + scale + ' 0 0 ' + scale + ' ' + tx + ' ' + ty + ')">' + content + '</g></svg>';
    });
    if (refresh) refresh();
    return { locations: count, evidence: source.evidenceCount };
  }
  window.DaramSceneBridge = { install };
})();
