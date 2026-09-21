const CACHE = "scheda-v4";
const ASSETS = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "fonts/Barlow-Regular.woff2", "fonts/Barlow-SemiBold.woff2", "fonts/BarlowCondensed-Bold.woff2", "fonts/BarlowCondensed-SemiBold.woff2", "anim/abductor.webp", "anim/bike.webp", "anim/cable_crunch.webp", "anim/chest.webp", "anim/chest_db.webp", "anim/chest_inc.webp", "anim/chest_inc_db.webp", "anim/crunch.webp", "anim/deadbug.webp", "anim/farmer.webp", "anim/fly_db.webp", "anim/glute_bridge.webp", "anim/glute_bridge_1.webp", "anim/goblet.webp", "anim/high_row.webp", "anim/hip.webp", "anim/lat.webp", "anim/lat_under.webp", "anim/lat_v.webp", "anim/lateral.webp", "anim/leg_curl.webp", "anim/leg_curl_seat.webp", "anim/leg_curl_stand.webp", "anim/leg_ext.webp", "anim/leg_press.webp", "anim/pallof.webp", "anim/pec.webp", "anim/plank.webp", "anim/pulley.webp", "anim/pushdown.webp", "anim/pushdown_rope.webp", "anim/row_db.webp", "anim/row_machine.webp", "anim/shoulder.webp", "anim/shoulder_db.webp", "anim/side_plank.webp", "anim/treadmill.webp"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request, {ignoreSearch: true}).then(hit => hit || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy));
      return res;
    }).catch(() => caches.match("index.html")))
  );
});
