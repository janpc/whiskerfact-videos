// Control final del mp4 antes de publicar: formato, duración, volumen, picos, fotogramas negros y bucle.
//   cd remotion && node final_check.mjs <fichero.mp4> [--length standard|short]     Sale con código 1 si hay FALLOS.
import {spawnSync} from 'node:child_process';
const file = process.argv[2];
const short = process.argv.includes('short');
const [MIN, WARN] = short ? [42, 62] : [61, 85];            // factory/brand.py LENGTH_PROFILES
const run = (cmd, args, opts = {}) => { const r = spawnSync(cmd, args, {maxBuffer: 1 << 28, ...opts}); if (r.status !== 0) { console.error(String(r.stderr)); process.exit(2); } return r; };
const fails = [], warns = [];
const info = JSON.parse(run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', file]).stdout);
const dur = +info.format.duration, v = info.streams.find((s) => s.codec_type === 'video');
if (!v || v.width !== 1080 || v.height !== 1920) fails.push('el vídeo no es 1080x1920');
if (!info.streams.some((s) => s.codec_type === 'audio')) fails.push('sin audio');
if (dur < MIN) fails.push(`dura ${dur.toFixed(1)} s (mínimo ${MIN})`); else if (dur > WARN) warns.push(`dura ${dur.toFixed(1)} s (aviso por encima de ${WARN})`);
const log = String(run('ffmpeg', ['-nostats', '-i', file, '-af', 'ebur128=peak=true', '-vf', 'blackdetect=d=0.3:pic_th=0.97', '-f', 'null', '-']).stderr);
const last = (re) => [...log.matchAll(re)].pop()?.[1];
const I = +last(/I:\s+(-?[\d.]+) LUFS/g), peak = +last(/Peak:\s+(-?[\d.]+) dBFS/g);
if (!(I >= -19 && I <= -13)) fails.push(`volumen ${I} LUFS (debe estar entre -19 y -13)`);
if (peak > -0.5) warns.push(`pico de audio ${peak} dBFS`);
for (const m of log.matchAll(/black_start:([\d.]+) black_end:([\d.]+)/g)) fails.push(`fotogramas negros ${m[1]}-${m[2]} s`);
const frame = (args) => run('ffmpeg', ['-v', 'error', ...args, '-i', file, '-frames:v', '1', '-vf', 'scale=270:480', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']).stdout;
const a = frame([]);
const all = run('ffmpeg', ['-v', 'error', '-sseof', '-0.2', '-i', file, '-vf', 'scale=270:480', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']).stdout;
const b = all.subarray(all.length - a.length);
let d = 0; for (let i = 0; i < a.length; i++) d += Math.abs(a[i] - b[i]); d /= a.length;
if (d > 3) fails.push(`bucle: primer y último fotograma distintos (diferencia ${d.toFixed(1)}/255)`);
console.log(`Control final: ${fails.length} FALLOS, ${warns.length} AVISOS · ${dur.toFixed(1)} s · ${I} LUFS · bucle ${d.toFixed(2)}`);
fails.forEach((x) => console.log('FAIL ' + x)); warns.forEach((x) => console.log('WARN ' + x));
process.exit(fails.length ? 1 : 0);
