// Own the title audio only while the HTML loading plate is present.
(function () {
    const audio = new Audio('game/assets/bgm-title.mp3?v=__MUSIC_HASH__');
    audio.loop = true;
    audio.volume = .45;
    audio.preload = 'auto';
    let finished = false;
    const hint = document.querySelector('#loading-brand .loading-hint');
    function start() {
        if (finished || !audio.paused) return;
        audio.play().then(() => {
            if (finished) audio.pause();
            else if (hint) hint.textContent = '마을의 문을 여는 중…';
        }).catch(() => {
            if (!finished && hint) hint.textContent = '화면을 누르면 배경음이 시작됩니다 · 로딩 중…';
        });
    }
    function stop() {
        if (finished) return;
        finished = true;
        audio.pause();
        audio.removeAttribute('src');
        audio.load();
        document.removeEventListener('pointerdown', start, true);
        document.removeEventListener('keydown', start, true);
        observer.disconnect();
    }
    document.addEventListener('pointerdown', start, true);
    document.addEventListener('keydown', start, true);
    window.addEventListener('pagehide', stop, {once:true});
    const observer = new MutationObserver(() => {
        const splash = document.getElementById('presplash');
        if (!splash || splash.classList.contains('hidden') || splash.style.display === 'none') stop();
    });
    observer.observe(document.body, {childList:true, subtree:true, attributes:true, attributeFilter:['class','style']});
    start();
})();
