// Comprobador de diseño de la versión Remotion (equivale a la parte de texto/solapes/botones de factory/qa.py).
//   cd remotion && node check.mjs [--step 0.5] [--overlay out/check]   (usa /usr/bin/google-chrome si existe)
// Renderiza fotogramas sueltos con inputProps {probe:true}; src/Probe.tsx mide las cajas reales en el navegador y las
// reglas son las de factory/brand.py (RAIL_TOP/SAFE_RIGHT_LOW = 900, SAFE_TOP). Sale con código 1 si hay algún FALLO.
import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition, renderStill} from '@remotion/renderer';

const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const step = parseFloat(arg('--step', '0.5'));
const overlayDir = arg('--overlay', null);
const meta = JSON.parse(fs.readFileSync('public/meta.json', 'utf8'));
const FPS = meta.fps ?? 30, N = meta.frames;
const scenesSrc = fs.readFileSync('src/scenes/current.ts', 'utf8');

const chrome = fs.existsSync('/usr/bin/google-chrome') ? {browserExecutable: '/usr/bin/google-chrome', chromeMode: 'chrome-for-testing'} : {};
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const browser = await openBrowser('chrome', {...chrome, chromiumOptions: {}});
const comp = await selectComposition({serveUrl, id: 'Reel', inputProps: {probe: true}, puppeteerInstance: browser});
if (overlayDir) fs.mkdirSync(overlayDir, {recursive: true});

const found = new Map();   // clave -> {sev, rule, a, b, scene, t0, t1}
const frames = []; for (let t = 0.2; t < N / FPS - 0.5; t += step) frames.push(Math.round(t * FPS));
let done = 0;
for (const f of frames) {
  let got = null;
  await renderStill({composition: comp, serveUrl, frame: f, output: overlayDir ? null : null, inputProps: {probe: true}, puppeteerInstance: browser, imageFormat: 'jpeg', scale: 0.2,
    onBrowserLog: (l) => { if (l.text.startsWith('PROBE ')) got = JSON.parse(l.text.slice(6)); }});
  if (!got) { console.error(`sin datos del comprobador en el fotograma ${f}`); process.exit(2); }
  for (const s of got.issues) {
    const k = `${got.id}|${s.rule}|${s.a}|${s.b ?? ''}`;
    const cur = found.get(k) ?? {...s, scene: got.id, t0: f / FPS, t1: f / FPS, frame: f}; cur.t1 = f / FPS;
    if (s.sev === 'FAIL') cur.sev = 'FAIL';
    found.set(k, cur);
  }
  if (overlayDir && got.issues.length) {
    await renderStill({composition: comp, serveUrl, frame: f, output: path.join(overlayDir, `f${String(f).padStart(4, '0')}_${got.id}.png`), inputProps: {probe: true, overlay: true}, puppeteerInstance: browser, scale: 0.5});
  }
  if (++done % 20 === 0) console.error(`  ${done}/${frames.length}`);
}
// bucle: el primer fotograma y los últimos tienen que ser idénticos (se comparan los PNG renderizados)
const still = async (frame) => (await renderStill({composition: comp, serveUrl, frame, output: null, inputProps: {probe: false}, puppeteerInstance: browser, imageFormat: 'png', scale: 0.25})).buffer;
const first = await still(0);
for (const f of [N - 6, N - 1]) if (!first.equals(await still(f)))
  found.set(`bucle|${f}`, {sev: 'FAIL', rule: 'bucle', a: `fotograma ${f}`, scene: 'loop', t0: f / FPS, t1: f / FPS, frame: f});
await browser.close({silent: true});

const RULES = {bucle: 'no es igual al primer fotograma', flota: 'personaje sin apoyar en el suelo', botones: 'bajo los botones de la app (x>900, y>900)', arriba: 'bajo la interfaz superior', abajo: 'bajo la descripción de la app', cortado: 'cortado por el borde', borde: 'pegado al borde',
  solape: 'dibujos que se superponen', solape_texto: 'texto tapado o tapando un dibujo', pegados: 'dibujos casi pegados (<20 px)'};
const list = [...found.values()].sort((a, b) => a.t0 - b.t0 || (a.sev < b.sev ? -1 : 1));
const fails = list.filter((x) => x.sev === 'FAIL');
console.log(`Comprobador de diseño: ${frames.length} fotogramas, ${fails.length} FALLOS, ${list.length - fails.length} AVISOS`);
for (const x of list) console.log(`${x.sev.padEnd(5)} ${x.t0.toFixed(1)}-${x.t1.toFixed(1)}s [${x.scene}] ${RULES[x.rule] ?? x.rule}: ${x.a}${x.b ? ' ↔ ' + x.b : ''}`);
fs.mkdirSync('out', {recursive: true});
fs.writeFileSync('out/check.json', JSON.stringify({fails: fails.length, warns: list.length - fails.length, issues: list}, null, 1));
process.exit(fails.length ? 1 : 0);
