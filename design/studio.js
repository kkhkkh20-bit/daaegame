(() => {
  'use strict';
  const $ = id => document.getElementById(id), kit = window.DaramArtKit;
  let manifest, selected, costume, expression = 0, scene = 'cake-kitchen', activeEvidence;
  const found = new Set(), regions = {forest:'숲속 마을',silver:'은빛 마을',mine:'광산 마을',city:'도시'};
  const lazy = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      kit.character(entry.target, entry.target.dataset.character, 0);
      lazy.unobserve(entry.target);
    }
  }, {rootMargin:'160px'});
  function cast() {
    lazy.disconnect();
    const query = $('search').value.trim().toLowerCase(), region = $('region').value;
    const items = manifest.order.map(id => manifest.characters[id]).filter(c =>
      (region === 'all' || c.region === region) && (!query || [c.name,c.species,c.kind,c.role,c.bio,c.design].join(' ').toLowerCase().includes(query)));
    $('cast-count').textContent = items.length; $('cast-grid').replaceChildren();
    for (const c of items) {
      const button = document.createElement('button'), portrait = document.createElement('div'), name = document.createElement('h3'), meta = document.createElement('p');
      button.className = 'cast-card'; button.setAttribute('aria-label', c.name + ' 캐릭터 보기');
      portrait.className = 'cast-portrait'; portrait.dataset.character = c.id;
      name.textContent = c.name; meta.textContent = c.species + ' · ' + regions[c.region];
      button.append(portrait,name,meta); button.onclick = () => showCharacter(c.id);
      $('cast-grid').append(button); lazy.observe(portrait);
    }
    $('no-results').hidden = items.length > 0;
  }
  function paintCharacter() {
    const id = costume || selected, c = manifest.characters[id];
    kit.character($('character-large'), id, expression);
    $('character-download').href = kit.url(c.src); $('character-download').download = c.src.split('/').pop();
    $('expression-buttons').replaceChildren();
    ['기본','생각·의심','감정'].forEach((label,i) => {
      const b = document.createElement('button'); b.textContent = label; b.setAttribute('aria-pressed', i === expression);
      b.onclick = () => { expression = i; paintCharacter(); }; $('expression-buttons').append(b);
    });
    $('costumes').replaceChildren(); $('costumes').hidden = selected !== 'nero';
    if (selected === 'nero') for (const [id,label] of [['nero','네로'],['luka','루카 변장'],['shadow','검은 망토']]) {
      const b = document.createElement('button'); b.textContent = label; b.setAttribute('aria-pressed', id === (costume || selected));
      b.onclick = () => { costume = id; paintCharacter(); }; $('costumes').append(b);
    }
  }
  function showCharacter(id) {
    selected = id; costume = null; expression = 0;
    const c = manifest.characters[id]; $('character-name').textContent = c.name;
    $('character-kind').textContent = c.species + ' · ' + (c.role || c.kind);
    $('character-bio').textContent = c.bio; $('character-design').textContent = c.design;
    paintCharacter(); $('character-dialog').showModal(); $('dialog-close').focus();
  }
  function pointButton(name, point, kind, handler, id) {
    const b = document.createElement('button'); b.className = 'scene-point ' + kind;
    b.style.left = point[0] / 360 * 100 + '%'; b.style.top = point[1] / 200 * 100 + '%';
    b.setAttribute('aria-label', name); b.dataset.point = id;
    const label = document.createElement('span'); label.textContent = name; b.append(label);
    if (point[0] < 80) b.classList.add('edge-left');
    if (point[0] > 280) b.classList.add('edge-right');
    if (point[1] < 50) b.classList.add('edge-top');
    b.onclick = handler; return b;
  }
  function paintPoints() {
    const record = manifest.sceneData.locations[scene], host = $('scene-hotspots'); host.replaceChildren();
    const uv = $('uv-mode').checked;
    host.classList.toggle('points-hidden', !$('show-points').checked);
    host.parentElement.classList.toggle('is-uv', uv && !!record?.evidence.some(e => e.uv));
    if (!record) return;
    for (const e of record.evidence) {
      if (e.inZoom || (e.uv && !uv)) continue;
      const done = found.has(record.caseId + ':' + e.evidenceId);
      host.append(pointButton(e.name, e.point, 'evidence-point' + (e.uv ? ' uv-point' : '') + (done ? ' done' : ''), () => inspectEvidence(e), e.spotId));
    }
    for (const o of record.observations) {
      host.append(pointButton(o.name, o.point, 'observation-point' + (o.zoom ? ' zoom-point' : ''), () => {
        if (o.zoom) openZoom(record, o.zoom); else {
          activeEvidence = null; $('evidence-inspector').dataset.kind = 'observation';
          $('evidence-name').textContent = o.name; $('evidence-desc').textContent = o.text || '';
          $('evidence-check').hidden = true;
        }
      }, o.id));
    }
  }
  function inspectEvidence(e) {
    activeEvidence = e; const record = manifest.sceneData.locations[scene];
    found.add(record.caseId + ':' + e.evidenceId);
    $('evidence-inspector').dataset.kind = 'evidence'; $('evidence-name').textContent = e.evidence.name;
    $('evidence-desc').textContent = e.evidence.desc;
    $('evidence-check').hidden = !e.evidence.check;
    if (e.evidence.check) $('evidence-check').textContent = e.evidence.check.label;
    paintPoints();
  }
  function locationOptions(cid) {
    $('location-select').replaceChildren();
    const c = manifest.cases.find(c => c.id === cid);
    $('location-select').disabled = !c;
    if (!c) { $('location-select').add(new Option(cid === 'main' ? '탐정 사무소' : '마을을 잇는 숲길', cid)); return; }
    for (const id of c.locations) $('location-select').add(new Option(manifest.locations[id].name, id));
  }
  function showScene(id) {
    scene = id; activeEvidence = null;
    const c = manifest.backgrounds[id], record = manifest.sceneData.locations[id];
    kit.background($('scene-preview'), id);
    $('scene-name').textContent = record ? record.name + ' · 증거 ' + record.evidence.length + '개' : c.name;
    $('scene-download').href = kit.url(c.src); $('scene-download').download = c.src.split('/').pop();
    $('uv-control').hidden = !record?.evidence.some(e => e.uv);
    const cid = record?.caseId || id;
    if ($('case-select').value !== cid) { $('case-select').value = cid; locationOptions(cid); }
    $('location-select').value = id;
    $('evidence-inspector').dataset.kind = 'idle'; $('evidence-name').textContent = record ? '수상한 물건을 눌러 보세요.' : '배경 전체를 둘러보세요.';
    $('evidence-desc').textContent = record ? '노란 표시는 증거, 파란 표시는 관찰과 확대 조사입니다.' : '이 장면에는 원작의 조사 증거를 배치하지 않았습니다.';
    $('evidence-check').hidden = true; paintPoints();
  }
  function openZoom(record, key) {
    const z = record.zooms[key]; if (!z) return;
    $('zoom-title').textContent = z.title; $('zoom-hotspots').replaceChildren();
    const id = manifest.zoomBackgrounds[key];
    if (id && manifest.backgrounds[id]) kit.background($('zoom-background'), id);
    else {
      kit.background($('zoom-background'), scene);
      $('zoom-background').querySelector('svg').style.filter = 'brightness(.6)';
    }
    $('zoom-evidence-name').textContent = '안쪽 물건을 눌러 보세요.'; $('zoom-evidence-desc').textContent = '';
    for (const it of z.items) {
      const b = pointButton(it.name, [it.x,it.y], it.ev ? 'evidence-point' : 'observation-point', () => {
        $('zoom-evidence-name').textContent = it.ev?.name || it.name;
        $('zoom-evidence-desc').textContent = it.ev?.desc || it.text || '';
        if (it.ev) {
          found.add(record.caseId + ':' + it.ev.id); b.classList.add('done');
          const e = record.evidence.find(e => e.evidenceId === it.ev.id); if (e) inspectEvidence(e);
        }
      }, it.id);
      $('zoom-hotspots').append(b);
    }
    $('zoom-dialog').showModal(); $('zoom-close').focus();
  }
  $('dialog-close').onclick = () => $('character-dialog').close();
  $('zoom-close').onclick = () => $('zoom-dialog').close();
  $('search').oninput = cast; $('region').onchange = cast;
  $('case-select').onchange = () => { locationOptions($('case-select').value); showScene($('location-select').value); };
  $('location-select').onchange = () => showScene($('location-select').value);
  $('show-points').onchange = paintPoints; $('uv-mode').onchange = paintPoints;
  $('show-actor').onchange = () => { $('scene-actor').hidden = !$('show-actor').checked; };
  $('evidence-check').onclick = () => {
    if (!activeEvidence?.evidence.check) return;
    $('evidence-desc').textContent = activeEvidence.evidence.check.text;
    $('evidence-check').hidden = true;
  };
  $('scene-fullscreen').onclick = async () => {
    if (document.fullscreenElement) await document.exitFullscreen();
    else if ($('scene-workbench').requestFullscreen) {
      try { await $('scene-workbench').requestFullscreen(); } catch (_) { $('scene-workbench').classList.toggle('expanded'); }
    } else $('scene-workbench').classList.toggle('expanded');
  };
  kit.ready.then(m => {
    manifest = m;
    kit.background($('hero-bg'), 'main').setAttribute('preserveAspectRatio', 'xMidYMid slice');
    kit.character($('hero-daram'), 'daram'); kit.character($('scene-actor'), 'daram'); cast();
    m.cases.forEach((c,i) => $('case-select').add(new Option(String(i + 1).padStart(2,'0') + ' · ' + c.title,c.id)));
    $('case-select').add(new Option('메인 화면','main')); $('case-select').add(new Option('이동 · 숲길','forest-path'));
    const initial = new URLSearchParams(location.search).get('scene');
    if (initial && m.backgrounds[initial]) scene = initial;
    const cid = m.locations[scene]?.caseId || scene;
    $('case-select').value = cid; locationOptions(cid); showScene(scene);
  }).catch(error => { console.error(error); $('cast-grid').textContent = '그림 목록을 불러오지 못했습니다. 새로고침해 주세요.'; });
})();
