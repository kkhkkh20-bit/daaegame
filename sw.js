// 다람 탐정 사무소 service worker
// Bump VERSION whenever game.html changes so installed apps pick up the new build.
const VERSION = "v205";
const CORE = "daae-core-" + VERSION;
const FONTS = "daae-fonts";
const FILES = ["./", "index.html", "game.html", "manifest.webmanifest",
  "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "icons/apple-180.png",
  "art/ui/wood-tile.png", "art/ui/books-stack.png", "art/ui/cat-sleeping.png", "art/ui/ink-quill.png", "art/ui/ivy-left.png", "art/ui/ivy-right.png", "art/ui/lantern-lit.png", "art/ui/magnifier.png", "art/ui/masking-tape.png", "art/ui/memo-white.png", "art/ui/memo-yellow.png", "art/ui/pin-blue.png", "art/ui/pin-green.png", "art/ui/pin-red.png", "art/ui/pin-yellow.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CORE).then((c) => c.addAll(FILES.map((u) => new Request(u, { cache: "reload" })))).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("daae-core-") && k !== CORE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // Google Fonts: serve from cache, refresh in the background
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.open(FONTS).then((c) => c.match(req).then((hit) => {
      const net = fetch(req).then((res) => { if (res.ok || res.type === "opaque") c.put(req, res.clone()); return res; }).catch(() => hit);
      return hit || net;
    })));
    return;
  }

  if (url.origin !== self.location.origin) return;

  // Pages: network first so a new build shows up right away; cache when offline
  if (req.mode === "navigate" || url.pathname.endsWith(".html") || url.pathname.endsWith("/")) {
    e.respondWith(
      fetch(req.url, { cache: "no-cache", credentials: "same-origin" }).then((res) => { if (res.ok) { const copy = res.clone(); caches.open(CORE).then((c) => c.put(url.origin + url.pathname, copy)); } return res; })
        .catch(() => caches.match(req, { ignoreSearch: true }).then((hit) => hit || caches.match("index.html")))
    );
    return;
  }

  // Everything else: cache first
  e.respondWith(caches.match(req).then((hit) => hit || fetch(req)));
});
