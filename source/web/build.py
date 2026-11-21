#!/usr/bin/env python3
"""Assemble the game into single-file HTML builds."""
import glob, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
fonts = open(sys.argv[1]).read() if len(sys.argv) > 1 else ''
js = '\n'.join(open(f).read() for f in sorted(glob.glob(os.path.join(ROOT, 'src', '*.js'))))
css = fonts + """
:root { --bg: #1c2a12; color-scheme: dark; }
html { box-sizing: border-box; height: 100%; background: var(--bg); }
body { height: 100%; margin: 0; background: var(--bg); overflow: hidden; overscroll-behavior: none;
  -webkit-user-select: none; user-select: none; -webkit-tap-highlight-color: transparent; -webkit-touch-callout: none; }
canvas#game { display: block; width: 100%; height: 100%; touch-action: none; outline: none; }
"""
body = f'<canvas id="game" aria-label="Sprout Siege game"></canvas>\n<script>\n{js}\n</script>\n'
fragment = f'<title>Sprout Siege</title>\n<style>{css}</style>\n{body}'
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">\n'
        '<meta name="theme-color" content="#1c2a12">\n'
        f'<title>Sprout Siege</title>\n<style>{css}</style>\n</head>\n<body>\n{body}</body>\n</html>\n')
out = os.path.join(ROOT, 'dist'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w').write(full)
open(os.path.join(out, 'sprout-siege.html'), 'w').write(fragment)
# Installable offline web app (GitHub Pages / iPhone home screen)
import time, shutil, json
pwa = os.path.join(ROOT, 'dist-pwa'); os.makedirs(os.path.join(pwa, 'icons'), exist_ok=True)
head_extra = ('<link rel="manifest" href="manifest.webmanifest">\n'
  '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
  '<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">\n'
  '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="Sprout Siege">\n')
sw_reg = ("<script>if ('serviceWorker' in navigator && location.protocol === 'https:') "
  "window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));</script>\n")
page = full.replace('<title>Sprout Siege</title>', head_extra + '<title>Sprout Siege</title>').replace('</body>', sw_reg + '</body>')
open(os.path.join(pwa, 'index.html'), 'w').write(page)
icons = os.path.join(ROOT, '..', 'icons')
for src, dst in [('apple-touch-icon.png', 'apple-touch-icon.png'), ('icon-192.png', 'icon-192.png'), ('icon-square-512.png', 'icon-512.png')]:
    shutil.copy(os.path.join(icons, src), os.path.join(pwa, 'icons', dst))
manifest = { 'name': 'Sprout Siege', 'short_name': 'Sprout Siege', 'description': 'Plant a garden and hold off waves of cartoon zombies.',
  'start_url': './', 'scope': './', 'display': 'fullscreen', 'orientation': 'landscape', 'background_color': '#1c2a12', 'theme_color': '#1c2a12',
  'icons': [{ 'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable' },
            { 'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable' }] }
open(os.path.join(pwa, 'manifest.webmanifest'), 'w').write(json.dumps(manifest, indent=2))
version = time.strftime('%Y%m%d%H%M%S')
sw = '''// Offline support: serve the game from the cache, refresh it whenever the network is available.
const CACHE = 'sprout-siege-%s';
const FILES = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
      .catch(() => caches.match(e.request, { ignoreSearch: true }).then(m => m || caches.match('./index.html')))
  );
});
''' % version
open(os.path.join(pwa, 'sw.js'), 'w').write(sw)
open(os.path.join(pwa, '.nojekyll'), 'w').write('')
print('pwa built', version)
print('built', len(full), 'bytes')
