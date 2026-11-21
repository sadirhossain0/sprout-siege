#!/usr/bin/env bash
# Packages Windows + macOS builds, ad-hoc signs the Mac apps, and zips everything into ../dist
set -euo pipefail
cd "$(dirname "$0")"
RCODESIGN=${RCODESIGN:-rcodesign}
rm -rf out stage
node build.mjs win32-x64,darwin-arm64,darwin-x64
mkdir -p stage ../dist
for a in arm64 x64; do "$RCODESIGN" sign "out/Sprout Siege-darwin-$a/Sprout Siege.app" >/dev/null; done
mv "out/Sprout Siege-win32-x64" "stage/Sprout Siege"
(cd stage && rm -f ../../dist/SproutSiege-Windows.zip && zip -qry ../../dist/SproutSiege-Windows.zip "Sprout Siege")
(cd "out/Sprout Siege-darwin-arm64" && rm -f ../../../dist/SproutSiege-Mac-AppleSilicon.zip && zip -qry ../../../dist/SproutSiege-Mac-AppleSilicon.zip "Sprout Siege.app")
(cd "out/Sprout Siege-darwin-x64" && rm -f ../../../dist/SproutSiege-Mac-Intel.zip && zip -qry ../../../dist/SproutSiege-Mac-Intel.zip "Sprout Siege.app")
rm -rf out stage
ls -la ../dist
