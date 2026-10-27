// HTML owns the music until the first Ren'Py interaction hands it over.
(function () {
    const audio = new Audio('game/assets/bgm-title.mp3?v=__MUSIC_HASH__');
    audio.id = 'r13-loading-music';
    audio.loop = true;
    audio.volume = .75;
    audio.preload = 'auto';
    document.body.appendChild(audio);
    let finished = false;
    // 소유자(2026-10-27): "배경음은 로딩 나올때부터 나와야한다고". 브라우저는 사용자가 한 번 누르기 전에는
    // 소리를 거부하므로 코드로 더 당길 수 없다. 대신 거부된 동안만 "누르면 켜진다"는 줄을 편다.
    function audioHint() {
        return (typeof document.querySelector === 'function') ? document.querySelector('#loading-brand .loading-audio-hint') : null;
    }
    function showHint(show) {
        const hint = audioHint();
        if (hint) hint.hidden = !show;
    }
    function start() {
        if (finished || !audio.paused) return;
        // Call synchronously inside the gesture, including on iOS Safari.
        audio.play().then(() => { if (finished) audio.pause(); else showHint(false); })
            .catch(() => { if (!finished) showHint(true); });
    }
    function stop() {
        if (finished) return 0;
        finished = true;
        showHint(false);
        const position = audio.currentTime || 0;
        audio.pause();
        audio.removeAttribute('src');
        audio.load();
        for (const event of ['pointerdown', 'touchstart', 'keydown']) {
            document.removeEventListener(event, start, true);
        }
        return position;
    }
    function handoff() {
        const context = window.renpyAudio && window.renpyAudio.context;
        if (!context || context.state === 'running' || audio.paused) return stop();
        // Safari may create the engine context after the loading-screen gesture.
        // Keep HTML audible until that context can actually take ownership.
        const position = audio.currentTime || 0;
        const ready = () => {
            if (context.state !== 'running') return;
            stop();
            context.removeEventListener('statechange', ready);
        };
        context.addEventListener('statechange', ready);
        context.resume().then(ready).catch(() => {});
        return position;
    }
    window.r13LoadingAudio = {audio, handoff};
    for (const event of ['pointerdown', 'touchstart', 'keydown']) {
        document.addEventListener(event, start, {capture: true, passive: true});
    }
    window.addEventListener('pagehide', stop, {once: true});
    start(); // Allowed on returning/engaged sites; rejection stays silent.
})();
