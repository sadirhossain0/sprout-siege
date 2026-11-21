import { packager } from '@electron/packager';
import fs from 'node:fs';
const ELECTRON = '44.10.2';
fs.copyFileSync('../web/dist/index.html', 'app/game/index.html');
const common = {
  dir: 'app', name: 'Sprout Siege', executableName: 'Sprout Siege', electronVersion: ELECTRON, out: 'out', overwrite: true, asar: true,
  appVersion: '1.1.0', buildVersion: '1.1.0', appCopyright: 'Sprout Siege', appBundleId: 'com.sproutsiege.game',
  appCategoryType: 'public.app-category.games', quiet: true
};
const targets = (process.argv[2] || 'win32-x64,darwin-arm64,darwin-x64').split(',');
for (const t of targets) {
  const [platform, arch] = t.split('-');
  const icon = platform === 'win32' ? '../icons/icon.ico' : '../icons/icon.icns';
  const extra = platform === 'win32' ? { win32metadata: { CompanyName: 'Sprout Siege', FileDescription: 'Sprout Siege', ProductName: 'Sprout Siege', InternalName: 'SproutSiege', OriginalFilename: 'Sprout Siege.exe' } } : {};
  const paths = await packager({ ...common, platform, arch, icon, ...extra });
  console.log('built', t, '->', paths.join(', '));
}
