// Renders a tutorial video from the game itself: steps the game frame by frame,
// captures each frame, renders the matching game audio offline, and encodes an MP4.
// Usage: node record-video.js <script: start|demo|guide> <out.mp4> <ffmpeg path>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const [, , script, out, ffmpeg] = process.argv;
const FPS = 30;
(async () => {
  const tmp = fs.mkdtempSync(path.join(path.dirname(out), '.frames-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + path.resolve(__dirname, '../web/dist/index.html') + '?rec=' + script);
  await page.waitForFunction(() => App.fontsReady === true);
  await page.evaluate(s => window.recStart(s), script);
  let n = 0, done = false, time = 0;
  while (!done && time < 240) {
    const r = await page.evaluate(([k, dt]) => window.recFrames(k, dt), [45, 1 / FPS]);
    for (const f of r.frames) fs.writeFileSync(path.join(tmp, String(n++).padStart(6, '0') + '.jpg'), Buffer.from(f.split(',')[1], 'base64'));
    done = r.done; time = r.time;
    if (n % 900 < 45) process.stdout.write(`  ${script}: ${time.toFixed(1)}s\n`);
  }
  const wav = await page.evaluate(() => window.recAudio());
  fs.writeFileSync(path.join(tmp, 'audio.wav'), Buffer.from(wav, 'base64'));
  await browser.close();
  execFileSync(ffmpeg, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, '%06d.jpg'), '-i', path.join(tmp, 'audio.wav'),
    '-vf', 'scale=in_range=pc:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-color_range', 'tv', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`${out}: ${n} frames, ${time.toFixed(1)}s, errors: ${JSON.stringify(errs)}`);
})();
