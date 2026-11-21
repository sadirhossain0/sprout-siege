#!/bin/bash
# Builds "Sprout Siege.dmg": a disk image with the app and an Applications shortcut,
# so people can install by dragging the app onto Applications.
# Run this on a Mac, in the same folder as "Sprout Siege.app".
set -e
cd "$(dirname "$0")"
APP="Sprout Siege.app"
if [ ! -d "$APP" ]; then
  echo "Put this file next to \"$APP\" and run it again."
  exit 1
fi
STAGE=$(mktemp -d)
cp -R "$APP" "$STAGE/"
ln -s /Applications "$STAGE/Applications"
hdiutil create -volname "Sprout Siege" -srcfolder "$STAGE" -ov -format UDZO "Sprout Siege.dmg"
rm -rf "$STAGE"
echo "Created: $(pwd)/Sprout Siege.dmg"
