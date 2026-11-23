// Hoja de contactos de la versión Remotion: un fotograma por escena (cuando ya está todo en pantalla) con la zona de botones en amarillo.
//   node sheet.mjs [out/sheet.jpg]   (necesita Python con Pillow para pegarlos)
import path from 'node:path'; import fs from 'node:fs'; import {execFileSync} from 'node:child_process';
import {bundle} from '@remotion/bundler'; import {openBrowser, selectComposition, renderStill} from '@remotion/renderer';
const out = process.argv[2] ?? 'out/sheet.jpg'; const meta = JSON.parse(fs.readFileSync('public/meta.json', 'utf8'));
const src = fs.readFileSync('src/scenes/lightning_vs_sun.tsx', 'utf8');
const chrome = fs.existsSync('/usr/bin/google-chrome') ? {browserExecutable: '/usr/bin/google-chrome', chromeMode: 'chrome-for-testing'} : {};
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')}); const browser = await openBrowser('chrome', chrome);
const comp = await selectComposition({serveUrl, id: 'Reel', inputProps: {probe: true}, puppeteerInstance: browser});
const times = JSON.parse(process.env.TIMES ?? '[]'); fs.mkdirSync('out/sheet', {recursive: true});
for (const [i, t] of times.entries()) await renderStill({composition: comp, serveUrl, frame: Math.round(t * 30), output: `out/sheet/s${String(i).padStart(2, '0')}.png`, inputProps: {probe: true, overlay: true}, puppeteerInstance: browser, scale: 0.35});
await browser.close({silent: true});
execFileSync('python3', ['-c', `
from PIL import Image; import glob
fs=sorted(glob.glob('out/sheet/s*.png')); ims=[Image.open(f).convert('RGB') for f in fs]; w,h=ims[0].size; cols=5; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(w*cols,h*rows),(20,20,20))
for i,im in enumerate(ims): sh.paste(im,((i%cols)*w,(i//cols)*h))
sh.save('${out}', quality=88); print(sh.size)`], {stdio: 'inherit'});
