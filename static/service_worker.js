const statCache = "brewzy-static-cache";
const dynaCache = "brewzy-dynamic-cache";
const assets = [
  "/","/static/images/icons/add.png","/static/images/icons/age.png","/static/images/icons/android-chrome-36x36.png","/static/images/icons/android-chrome-48x48.png","/static/images/icons/android-chrome-72x72.png","/static/images/icons/android-chrome-96x96.png","/static/images/icons/android-chrome-144x144.png","/static/images/icons/android-chrome-192x192.png","/static/images/icons/android-chrome-256x256.png","/static/images/icons/android-chrome-384x384.png","/static/images/icons/android-chrome-512x512.png","/static/images/icons/animation.png","/static/images/icons/apple-touch-icon.png","/static/images/icons/arrow_left.png","/static/images/icons/arrow_right.png","/static/images/icons/audio.png","/static/images/icons/brewzy_logo.png","/static/images/icons/close.png","/static/images/icons/delete.png","/static/images/icons/document.png","/static/images/icons/email.png","/static/images/icons/favicon-16x16.png","/static/images/icons/favicon-32x32.png","/static/images/icons/favicon-194x194.png","/static/images/icons/favicon.ico","/static/images/icons/image.png","/static/images/icons/login.png","/static/images/icons/logout.png","/static/images/icons/message_sent.png","/static/images/icons/mstile-150x150.png","/static/images/icons/no.png","/static/images/icons/options.png","/static/images/icons/password.png","/static/images/icons/person.png","/static/images/icons/prohibit.png","/static/images/icons/register.png","/static/images/icons/reset.png","/static/images/icons/safari-pinned-tab.svg","/static/images/icons/text.png","/static/images/icons/update.png","/static/images/icons/video.png","/static/images/icons/view.png","/static/images/icons/yes.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(statCache)
      .then(cache => {
        return cache.addAll(assets);
      })
      .catch(error => {
        console.error('Failed to cache assets: ', error);
      })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});

self.addEventListener("activate", event => {
  const cacheWhitelist = [statCache];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
