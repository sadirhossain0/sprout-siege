# Sprout Siege: Zombies in the Garden

A lane-defense game: plant a garden and hold off waves of cartoon zombies before they reach the greenhouse.

**Play it:** https://sadirhossain0.github.io/sprot-seige/

**Download:** [Android APK](https://sadirhossain0.github.io/sprot-seige/downloads/SproutSiege-2.0-Android.apk) · [Windows, Mac and all platforms (Releases)](https://github.com/sadirhossain0/sprot-seige/releases) · [What's new](CHANGELOG.md)

- 14 plants and 12 kinds of zombies
- 5 worlds with 10 levels each (Backyard, Autumn Orchard, Moonlit Garden, Frosty Garden, Sunny Beach), plus Endless Horde
- Guided tutorial, How to Play book, Watch Demo mode, Field Guide
- Music and sound effects, all generated in code
- Works offline once it has been opened

## Put it on your iPhone

1. Open https://sadirhossain0.github.io/sprot-seige/ in **Safari**.
2. Tap the **Share** button, then **Add to Home Screen**, then **Add**.
3. Open it once from the home screen while online. After that it works without internet.

Hold your phone sideways to play. Progress is saved on the device.

## Controls

- Tap a seed card, then tap a lawn square to plant (or drag the card onto the lawn).
- Hold a finger on a seed card to read what the plant does.
- Tap dew drops (and apples) to collect them.
- Keyboard: `1`–`0` pick cards, `S` trowel, `F` fast-forward, `M` mute, `Esc`/`P` pause.

## Project layout

| Path | What it is |
|---|---|
| `index.html`, `sw.js`, `manifest.webmanifest`, `icons/` | The playable web app served by GitHub Pages |
| `source/web/src/` | Game source (JavaScript, all art and audio drawn/synthesized in code) |
| `source/web/build.py` | Builds the single-file game: `python3 build.py fonts-embed.css` |
| `source/android/` | Android wrapper (`build-apk.sh`, needs Android SDK build-tools 35 + platform 34) |
| `source/desktop/` | Windows/Mac wrapper (Electron; `package-all.sh`) |
| `source/tools/` | Tutorial-video recorder and a Mac `.dmg` helper |

Fonts: Lilita One and Fredoka, used under the SIL Open Font License 1.1.
