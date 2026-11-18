# Builds the installable phone app (app/) from the artifact page (index.html).
import re, time, pathlib
src = pathlib.Path("src/artifact.html").read_text()
body = src.replace("const STANDALONE = false;", "const STANDALONE = true;")
assert "const STANDALONE = true;" in body
title = re.search(r"<title>.*?</title>", body).group(0)
body = body.replace(title, "", 1)
head = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{title}
<meta name="theme-color" content="#2c6e4f">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font-size:14px;font-family:system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head><body>
"""
out = pathlib.Path("."); out.mkdir(exist_ok=True)
(out/"index.html").write_text(head + body + "\n</body></html>\n")
(out/"manifest.webmanifest").write_text("""{
  "name": "Piring Calorie Tracker",
  "short_name": "Piring",
  "description": "Log food, drinks, workouts and weight.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#f3f6f2",
  "theme_color": "#2c6e4f",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
""")
ver = time.strftime("%Y%m%d%H%M%S")
(out/"sw.js").write_text("""// Offline support. Network first for the app page so updates arrive; cache as fallback.
const CACHE = "piring-%s";
const CORE = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-180.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(m => m || caches.match("index.html"))));
});
""" % ver)
print("built", ver)
