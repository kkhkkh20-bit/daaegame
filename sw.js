// 2026-10-17: the 1장 HTML 테스트판 moved to the archive/ch1-html-test branch.
// This worker only removes itself and the caches the old one left, so browsers that installed it
// stop serving the old page and stop intercepting /preview/room13-dev/.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k.startsWith("daae-")).map((k) => caches.delete(k)));
    await self.registration.unregister();
    const clients = await self.clients.matchAll({ type: "window" });
    clients.forEach((c) => c.navigate(c.url));
  })());
});
