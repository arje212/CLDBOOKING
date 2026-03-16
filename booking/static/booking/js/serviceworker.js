const CACHE_NAME = 'trainroom-v2';

// Only cache truly static assets — never cache login or any POST pages
const STATIC_ASSETS = [
  '/static/booking/js/app.js',
];

// Pages that should NEVER be cached (CSRF-sensitive)
const NEVER_CACHE = [
  '/login/',
  '/register/',
  '/logout/',
  '/custom-reset-password/',
];

// Install — cache only static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch — network first for HTML pages, cache first for static assets
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Skip non-GET requests entirely
  if (event.request.method !== 'GET') return;

  // Never cache login/register/csrf-sensitive pages
  if (NEVER_CACHE.some(path => url.pathname.startsWith(path))) {
    event.respondWith(fetch(event.request));
    return;
  }

  // For static files — cache first
  if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // For everything else — network first, fallback to cache
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});

// Push Notifications
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'TrainRoom';
  const options = {
    body: data.body || 'You have a new notification.',
    icon: '/static/booking/img/icon-192.png',
    badge: '/static/booking/img/icon-192.png',
    data: { url: data.url || '/' },
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

// Notification click
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url));
});
