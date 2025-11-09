async function includePartial(id, url) {
    const host = document.getElementById(id);
    if (!host) return;
    try {
        const res = await fetch(url, { cache: 'no-store' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        host.innerHTML = await res.text();
    } catch (e) {
        console.error(`Не удалось загрузить ${url}:`, e);
    }
}

function markActive() {
    const active = document.body.dataset.active; // 'home' | 'docs' | 'mo'
    if (!active) return;
    const map = { home: 'index.html', docs: 'documents.html', mo: 'mo.html' };
    const href = map[active];
    document.querySelectorAll('header .nav a.link').forEach(a => {
        const ends = (a.getAttribute('href') || '').endsWith(href);
        a.classList.toggle('active', ends);
    });
}

// --- запускаем сразу (без ожидания событий), плюс резерв на onload ---
(async function boot() {
    await includePartial('site-header', './partials/header.html');
    await includePartial('site-footer', './partials/footer.html');
    markActive();
})();

window.addEventListener('load', () => {
    // если по какой-то причине не успело — повторим
    if (!document.querySelector('header .nav')) {
        includePartial('site-header', './partials/header.html')
            .then(() => markActive());
    }
    if (!document.querySelector('footer > div')) {
        includePartial('site-footer', './partials/footer.html');
    }
});
