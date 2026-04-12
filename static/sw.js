/* PinguPlay v2.1 — Service Worker */
const CACHE = 'pinguplay-v9';

/* Shell precached on install */
const SHELL = [
  '/',
  '/manifest.json',
  '/icon.svg',
  '/privacy.html',
  '/terms.html',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);

  /* Cross-origin (fonts, analytics): stale-while-revalidate */
  if (url.origin !== self.location.origin) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        const net = fetch(e.request).then(res => {
          if (res.ok) { const clone = res.clone(); caches.open(CACHE).then(c => c.put(e.request, clone)); }
          return res;
        }).catch(() => cached);
        return cached || net;
      })
    );
    return;
  }

  /* Immutable hashed assets (_app/immutable/): cache-first forever */
  if (url.pathname.startsWith('/_app/immutable/')) {
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
        if (res.ok) { const clone = res.clone(); caches.open(CACHE).then(c => c.put(e.request, clone)); }
        return res;
      }))
    );
    return;
  }

  /* HTML navigation: network-first (always fresh), fallback to cache or shell */
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          if (res.ok) { const clone = res.clone(); caches.open(CACHE).then(c => c.put(e.request, clone)); }
          return res;
        })
        .catch(() =>
          caches.match(e.request)
            .then(cached => cached || caches.match('/'))
        )
    );
    return;
  }

  /* Everything else: stale-while-revalidate */
  e.respondWith(
    caches.match(e.request).then(cached => {
      const net = fetch(e.request).then(res => {
        if (res.ok) { const clone = res.clone(); caches.open(CACHE).then(c => c.put(e.request, clone)); }
        return res;
      }).catch(() => cached);
      return cached || net;
    })
  );
});
