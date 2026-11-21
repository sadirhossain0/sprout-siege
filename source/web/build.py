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
.ss-modal { position: fixed; inset: 0; z-index: 50; display: flex; align-items: center; justify-content: center; padding: 16px; background: rgba(15,20,10,.62); font-family: Fredoka, "Trebuchet MS", system-ui, sans-serif; -webkit-user-select: text; user-select: text; }
.ss-card { position: relative; width: min(560px, 100%); max-height: 100%; overflow-y: auto; box-sizing: border-box; padding: 20px 24px; border-radius: 22px; background: #fff7e2; color: #3b2a14; border: 6px solid #8b5426; box-shadow: 0 8px 0 rgba(0,0,0,.25); }
.ss-card h2 { margin: 0 0 6px; font-family: "Lilita One", "Trebuchet MS", sans-serif; font-weight: 400; font-size: 30px; color: #2f7a2c; }
.ss-card h3 { margin: 18px 0 4px; font-family: "Lilita One", "Trebuchet MS", sans-serif; font-weight: 400; font-size: 22px; color: #a8503a; }
.ss-card p { margin: 6px 0 10px; font-size: 16px; line-height: 1.4; }
.ss-card label { display: block; margin: 8px 0; font-weight: 600; font-size: 15px; }
.ss-card input { display: block; width: 100%; box-sizing: border-box; margin-top: 4px; padding: 10px 12px; font: 600 17px Fredoka, system-ui, sans-serif; color: #3b2a14; background: #fff; border: 2px solid #b89a6a; border-radius: 10px; }
.ss-card input:focus { outline: 3px solid #7fd458; border-color: #4fa83a; }
.ss-card input[hidden] { display: none; }
.ss-row { display: flex; gap: 10px; align-items: center; margin: 8px 0; }
.ss-row input { margin-top: 0; flex: 1; min-width: 0; font-family: ui-monospace, Menlo, monospace; font-size: 15px; }
.ss-btn { flex: none; padding: 10px 16px; font: 400 18px "Lilita One", "Trebuchet MS", sans-serif; color: #fff8e0; background: #b8783d; border: 3px solid #24180c; border-radius: 12px; box-shadow: 0 4px 0 rgba(0,0,0,.25); cursor: pointer; }
.ss-btn.go { background: #5aa83a; }
.ss-btn:active { transform: translateY(3px); box-shadow: 0 1px 0 rgba(0,0,0,.25); }
.ss-btn:disabled { opacity: .55; }
.ss-btn:focus-visible, .ss-link:focus-visible, .ss-x:focus-visible { outline: 3px solid #ffe14a; outline-offset: 2px; }
.ss-link { background: none; border: none; padding: 4px 0; color: #2f6aa8; font: 600 15px Fredoka, system-ui, sans-serif; text-decoration: underline; cursor: pointer; }
.ss-x { position: absolute; top: 10px; right: 12px; width: 40px; height: 40px; border-radius: 50%; border: 3px solid #24180c; background: #b8783d; color: #fff8e0; font-size: 18px; cursor: pointer; }
.ss-msg { min-height: 22px; margin: 6px 0; font-weight: 600; font-size: 15px; color: #2f7a2c; }
.ss-msg.bad { color: #b13a2a; }
@media (max-height: 500px) { .ss-card { padding: 14px 18px; } .ss-card h3 { margin-top: 10px; } .ss-card p { margin: 4px 0 6px; } }
"""
cfg_path = os.path.join(ROOT, 'cloud-config.json')
cfg = open(cfg_path).read().strip() if os.path.exists(cfg_path) else 'null'
body = f'<canvas id="game" aria-label="Sprout Siege game"></canvas>\n<script>window.SPROUT_CLOUD_CONFIG = {cfg} || window.SPROUT_CLOUD_CONFIG || null;</script>\n<script>\n{js}\n</script>\n'
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
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('sprout-siege-') && !k.startsWith('sprout-siege-retro-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
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
