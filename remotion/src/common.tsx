import React from 'react';
import {Img, staticFile, delayRender, continueRender} from 'remotion';

export const W = 1080, H = 1920, FPS = 30;
export const TEXT = 'rgb(246,244,238)', GOLD = 'rgb(255,199,74)', ACC = 'rgb(250,204,21)', ACC_T = 'rgb(252,227,126)';
export const INK = 'rgb(44,32,30)', RED_T = 'rgb(176,40,58)', GREEN = 'rgb(70,178,84)', YELLOW = 'rgb(246,196,60)', RED = 'rgb(222,64,60)', CREAM = 'rgb(233,226,190)';
export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const eo = (x: number) => 1 - (1 - clamp(x)) ** 3;
export const eio = (x: number) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const rng = (seed: number) => () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };

export const useFonts = () => {
  const [h] = React.useState(() => delayRender('fonts'));
  React.useEffect(() => {
    const list: [string, string][] = [['Londrina', 'fonts/Londrina.ttf'], ['InterBlack', 'fonts/Inter-Black.otf'], ['InterXB', 'fonts/Inter-ExtraBold.otf']];
    Promise.all(list.map(([n, f]) => new FontFace(n, `url(${staticFile(f)})`).load().then((ff) => document.fonts.add(ff)))).then(() => continueRender(h));
  }, [h]);
};

export const stroke = (px: number, col = INK): React.CSSProperties => ({WebkitTextStroke: `${px * 2}px ${col}`, paintOrder: 'stroke fill'} as React.CSSProperties);

export const Svg: React.FC<{a?: number; children: React.ReactNode}> = ({a = 1, children}) =>
  a <= 0.003 ? null : <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, opacity: a}}>{children}</svg>;

export const Item: React.FC<{lib: string; name: string; x: number; y: number; h: number; a?: number; rot?: number}> = ({lib, name, x, y, h, a = 1, rot = 0}) =>
  a <= 0.003 ? null : <Img data-box="item" data-name={`${lib}/${name}`} src={staticFile(`spr/${lib}__${name}.png`)} style={{position: 'absolute', left: x, top: y, height: h, translate: '-50% -50%', rotate: `${-rot}deg`, opacity: a}} />;

// ---------- suelo ----------
export const GROUND_Y = 1300;   // horizonte: aquí empieza la franja de suelo
export const FLOOR = 1345;      // línea donde apoyan los pies (dentro de la franja)
// Personaje u objeto APOYADO: su borde inferior (los sprites vienen recortados al ras) queda en FLOOR, con sombra de contacto.
// `lift` > 0 solo para saltos: lo marca como "en el aire" para el comprobador; la sombra se queda en el suelo.
export const Stand: React.FC<{lib: string; name: string; x: number; h: number; a?: number; lift?: number}> = ({lib, name, x, h, a = 1, lift = 0}) =>
  a <= 0.003 ? null : <>
    <div style={{position: 'absolute', left: x, top: FLOOR, width: h * 0.55, height: 26, translate: '-50% -50%', borderRadius: '50%', background: 'rgba(0,0,0,0.4)', filter: 'blur(5px)', opacity: a * (1 - clamp(lift / 80, 0, 0.6))}} />
    <Img data-box="item" data-anchor="bottom" data-air={lift > 0 ? '1' : undefined} data-name={`${lib}/${name}`} src={staticFile(`spr/${lib}__${name}.png`)} style={{position: 'absolute', left: x, top: FLOOR - lift, height: h, translate: '-50% -100%', opacity: a}} />
  </>;
export const BI = 'battery_items', LW = 'large_w47';

const battColor = (f: number) => (f > 0.55 ? GREEN : f > 0.25 ? YELLOW : RED);
export const Battery: React.FC<{cx: number; cy: number; w: number; f: number; a?: number; bolt?: boolean; capLine?: number | null; plate?: boolean}> =
  ({cx, cy, w, f, a = 1, bolt = false, capLine = null, plate = false}) => {
    const h = w * 0.5, x0 = cx - w / 2, y0 = cy - h / 2, x1 = cx + w / 2, y1 = cy + h / 2, pad = w * 0.06, k = h * 0.36;
    const pts = [[cx + 0.15 * k, cy - k], [cx - 0.45 * k, cy + 0.12 * k], [cx - 0.02 * k, cy + 0.12 * k], [cx - 0.18 * k, cy + k], [cx + 0.45 * k, cy - 0.15 * k], [cx + 0.02 * k, cy - 0.15 * k]];
    return (
      <Svg a={a}>
        {plate && <rect x={x0 - w * 0.16} y={y0 - h * 0.34} width={w * 1.39} height={h * 1.68} rx={h * 0.3} fill="rgb(236,226,196)" stroke={INK} strokeWidth={6} />}
        <rect x={x1} y={cy - h * 0.18} width={w * 0.07} height={h * 0.36} rx={6} fill={INK} />
        <rect x={x0} y={y0} width={w} height={h} rx={h * 0.18} fill="rgb(250,248,240)" stroke={INK} strokeWidth={7} />
        {f > 0.01 && <rect x={x0 + pad} y={y0 + pad} width={(w - 2 * pad) * clamp(f)} height={h - 2 * pad} rx={8} fill={battColor(f)} />}
        {capLine !== null && <line x1={x0 + pad + (w - 2 * pad) * capLine} x2={x0 + pad + (w - 2 * pad) * capLine} y1={y0 - 12} y2={y1 + 12} stroke={RED} strokeWidth={8} />}
        {bolt && <polygon points={pts.map((p) => p.join(',')).join(' ')} fill="rgb(255,236,90)" stroke={INK} strokeWidth={5} strokeLinejoin="round" />}
      </Svg>
    );
  };

export const HeatWaves: React.FC<{cx: number; y0: number; y1: number; T: number; a: number; n?: number; spread?: number}> = ({cx, y0, y1, T, a, n = 3, spread = 90}) => (
  <Svg a={a}>
    {Array.from({length: n}).map((_, i) => {
      const x = cx + (i - (n - 1) / 2) * spread;
      const pts = Array.from({length: 30}).map((__, k) => `${x + 14 * Math.sin(k * 0.55 - T * 6 + i)},${y1 - ((y1 - y0) * k) / 29}`).join(' ');
      return <polyline key={i} points={pts} fill="none" stroke="rgb(240,110,50)" strokeWidth={10} strokeLinejoin="round" strokeLinecap="round" />;
    })}
  </Svg>
);

// Busto (dibujo cortado por la cintura) dentro de un círculo: el corte queda tapado por el borde y se lee como retrato.
export const Medallion: React.FC<{lib: string; name: string; x: number; y: number; d: number}> = ({lib, name, x, y, d}) => (
  <div data-box="item" data-name={`medallion:${lib}/${name}`} style={{position: 'absolute', left: x - d / 2, top: y - d / 2, width: d, height: d, boxSizing: 'border-box', borderRadius: '50%', overflow: 'hidden', background: CREAM, border: `8px solid ${INK}`, boxShadow: '0 14px 0 rgba(0,0,0,0.25)'}}>
    <Img src={staticFile(`spr/${lib}__${name}.png`)} style={{position: 'absolute', left: '50%', bottom: -14, height: d * 0.94, translate: '-50% 0'}} />
  </div>
);

// ---------- texto ----------
export const Title: React.FC<{k: number; text: string; color?: string; y?: number}> = ({k, text, color = TEXT, y = 360}) => (
  <div data-box="text" data-name={text} style={{position: 'absolute', left: 540, top: y + (1 - eo(k)) * 30, translate: '-50% 0', fontFamily: 'Londrina', fontSize: 94, lineHeight: 1.15, color, opacity: k, whiteSpace: 'nowrap', ...stroke(3)}}>{text}</div>
);
export const Label: React.FC<{text: string; y: number; col: string; a: number; x?: number}> = ({text, y, col, a, x = 540}) => {
  if (a <= 0.003) return null;
  const light = (/rgb\((\d+),(\d+),(\d+)\)/.exec(col)?.slice(1).reduce((p, v) => p + +v, 0) ?? 0) > 380;
  return (
    <div data-box="text" data-name={text} style={{position: 'absolute', left: x, top: y + (1 - eo(a)) * 30, translate: '-50% 0', fontFamily: 'Londrina', fontSize: 52, lineHeight: 1.1, color: col, opacity: a, whiteSpace: 'nowrap',
      padding: light ? '4px 18px 6px' : 0, borderRadius: 999, background: light ? 'rgba(30,22,22,0.67)' : 'none'}}>{text}</div>
  );
};

// ---------- fondos propios ----------
export const Grad: React.FC<{top: string; bot: string}> = ({top, bot}) => <div style={{position: 'absolute', inset: 0, background: `linear-gradient(${top}, ${bot})`}} />;
export const Stars: React.FC<{T: number; n?: number; seed?: number; maxY?: number}> = ({T, n = 70, seed = 5, maxY = 1500}) => {
  const r = rng(seed);
  return <Svg>{Array.from({length: n}).map((_, i) => <circle key={i} cx={r() * W} cy={r() * maxY} r={1.5 + r() * 2.4} fill="#fff" opacity={0.35 + 0.5 * Math.abs(Math.sin(T * (0.6 + r()) + i))} />)}</Svg>;
};
export const Skyline: React.FC<{y: number; color: string; seed: number; T: number}> = ({y, color, seed}) => {
  const r = rng(seed); let x = -20; const bs: React.ReactNode[] = [];
  while (x < W) { const w = 60 + r() * 90, h = 120 + r() * 340; bs.push(<rect key={x} x={x} y={y - h} width={w} height={h + 400} fill={color} />);
    for (let wy = y - h + 24; wy < y - 20; wy += 38) for (let wx = x + 12; wx < x + w - 18; wx += 26) if (r() > 0.62) bs.push(<rect key={`${x}-${wx}-${wy}`} x={wx} y={wy} width={10} height={14} fill="rgba(255,214,120,0.8)" />);
    x += w + 4 + r() * 8; }
  return <Svg>{bs}</Svg>;
};
export const Dunes: React.FC<{y: number; colors: string[]}> = ({y, colors}) => (
  <Svg>{colors.map((c, i) => {
    const pts = Array.from({length: 54}).map((_, k) => `${(k / 53) * W},${y + i * 90 - 70 * Math.sin(k * 0.2 + i * 1.7) - 26 * Math.sin(k * 0.55 + i)}`).join(' ');
    return <polygon key={i} points={`0,${H} ${pts} ${W},${H}`} fill={c} />;
  })}</Svg>
);
export const Pines: React.FC<{y: number; color: string; seed: number}> = ({y, color, seed}) => {
  const r = rng(seed); const ps: React.ReactNode[] = [];
  for (let x = -30; x < W + 30; x += 58 + r() * 30) { const h = 170 + r() * 150, w = 80 + r() * 30; ps.push(<polygon key={x} points={`${x},${y} ${x + w / 2},${y - h} ${x + w},${y}`} fill={color} />); }
  return <Svg>{ps}<rect x={0} y={y - 4} width={W} height={H} fill={color} /></Svg>;
};
export const Card: React.FC<{y?: number; h?: number}> = ({y = 720, h = 600}) => <div style={{position: 'absolute', left: 56, top: y, width: 968, height: h, boxSizing: 'border-box', borderRadius: 36, background: CREAM, border: `4px solid ${INK}`, boxShadow: '10px 14px 0 rgba(0,0,0,0.28)'}} />;

// ---------- paisajes en capas (ver refs/fondos/) ----------
export const SKIES = {
  sunset: ['rgb(70,52,120)', 'rgb(196,96,130)', 'rgb(246,176,96)', 'rgb(250,214,120)'],
  dawn: ['rgb(64,84,150)', 'rgb(150,140,190)', 'rgb(240,180,170)', 'rgb(252,222,170)'],
  dusk: ['rgb(30,36,90)', 'rgb(96,60,130)', 'rgb(200,100,120)', 'rgb(236,150,110)'],
  day: ['rgb(70,140,210)', 'rgb(120,180,230)', 'rgb(180,216,240)', 'rgb(220,236,246)'],
  storm: ['rgb(40,44,60)', 'rgb(70,76,96)', 'rgb(110,116,130)', 'rgb(150,150,160)'],
  night: ['rgb(24,22,70)', 'rgb(44,42,120)'],
};
const TERRAINS = {
  forest: ['rgb(30,70,52)', 'rgb(24,60,44)', 'rgb(18,48,36)'],
  pines: ['rgb(36,76,70)', 'rgb(28,62,58)', 'rgb(20,48,46)'],
  autumn: ['rgb(150,80,50)', 'rgb(120,60,40)', 'rgb(90,44,30)'],
  hills: ['rgb(80,110,70)', 'rgb(60,90,56)', 'rgb(44,70,42)'],
  dunes: ['rgb(214,160,100)', 'rgb(196,140,84)', 'rgb(170,116,66)'],
  city: ['rgb(70,64,100)', 'rgb(54,50,84)', 'rgb(40,36,66)'],
};
export const Ground: React.FC<{color?: string}> = ({color = 'rgb(40,44,30)'}) => <div style={{position: 'absolute', left: 0, top: GROUND_Y, width: W, height: H - GROUND_Y, background: color}} />;
const PERIOD = W + 400;
const Layer: React.FC<{terrain: keyof typeof TERRAINS; i: number; color: string; T: number; seed: number}> = ({terrain, i, color, T, seed}) => {
  const r = rng(seed * 7919 + i * 104729 + 17); for (let n = 0; n < 4; n++) r();
  const base = GROUND_Y - 120 + i * 60, hh = [300, 240, 190][i], shift = T * [6, 12, 22][i];
  const wrap = (x: number) => ((((x - shift) % PERIOD) + PERIOD) % PERIOD) - 200;
  const els: React.ReactNode[] = [];
  if (terrain === 'hills' || terrain === 'dunes') {
    const ph = r() * 6.3, f = 180 + r() * 120, amp = hh * 0.5;
    const pts = Array.from({length: 96}).map((_, k) => { const x = -20 + k * 12; return `${x},${base - amp * (0.5 + 0.5 * Math.sin((x + shift) / f + ph)) - amp * 0.25 * Math.sin((x + shift) / (f * 0.45) + ph * 2)}`; }).join(' ');
    els.push(<polygon key="d" points={`-20,${H} ${pts} ${W + 140},${H}`} fill={color} />);
  } else if (terrain === 'city') {
    for (let x = 0; x < PERIOD;) { const w = 50 + r() * 80, h = (0.35 + r() * 0.65) * hh * 1.3; els.push(<rect key={x} x={wrap(x)} y={base - h} width={w - 6} height={h + 400} fill={color} />); x += w; }
  } else {
    const th = terrain === 'pines' ? hh * 1.2 : hh, n = terrain === 'pines' ? 28 : 18;
    els.push(<rect key="b" x={0} y={base - th * 0.35} width={W} height={400} fill={color} />);
    for (let j = 0; j < n; j++) {
      const x0 = ((j + r() * 0.8) / n) * PERIOD, h = (0.75 + r() * 0.25) * th, R = h * 0.32 * (0.8 + r() * 0.4), x = wrap(x0), cy = base - h * 0.55;
      for (let k = 0; k < 7; k++) { const g = (k / 7) * Math.PI; els.push(<circle key={`${j}-${k}`} cx={x + Math.cos(g) * R * 0.9 + r() * 16 - 8} cy={cy - Math.sin(g) * R * 0.7 + r() * 16 - 8} r={R * (0.55 + r() * 0.25)} fill={color} />); }
      els.push(<ellipse key={`e${j}`} cx={x} cy={cy + R * 0.3} rx={R} ry={R * 0.9} fill={color} />);
    }
  }
  return <Svg>{els}</Svg>;
};
export const Landscape: React.FC<{sky: keyof typeof SKIES; terrain: keyof typeof TERRAINS; T: number; seed?: number}> = ({sky, terrain, T, seed = 1}) => (
  <>
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: GROUND_Y, background: `linear-gradient(${SKIES[sky].join(', ')})`}} />
    {sky === 'night' && <Stars T={T} seed={seed + 3} n={60} maxY={1000} />}
    {TERRAINS[terrain].map((c, i) => <Layer key={i} terrain={terrain} i={i} color={c} T={T} seed={seed} />)}
    <Ground />
  </>
);
export const Rays: React.FC<{angle: number}> = ({angle}) => (
  <Svg>{Array.from({length: 14}).map((_, i) => {
    const a0 = angle + (i * Math.PI * 2) / 14, a1 = a0 + Math.PI / 14, R = 1800;
    return <polygon key={i} points={`540,1080 ${540 + R * Math.cos(a0)},${1080 + R * Math.sin(a0)} ${540 + R * Math.cos(a1)},${1080 + R * Math.sin(a1)}`} fill="rgba(255,255,255,0.1)" />;
  })}</Svg>
);
export const Grain: React.FC<{frame: number}> = ({frame}) => (
  <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, opacity: 0.1, mixBlendMode: 'overlay', pointerEvents: 'none'}}>
    <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed={frame % 4} stitchTiles="stitch" /><feColorMatrix type="saturate" values="0" /></filter>
    <rect width={W} height={H} filter="url(#g)" />
  </svg>
);

// ---------- elementos compartidos por las escenas (antes copiados en cada escena) ----------
export const Big: React.FC<{text: string; y: number; size: number; t: number; at?: number; col?: string; x?: number}> = ({text, y, size, t, at = 0, col = TEXT, x = 540}) => (
  <div data-box="text" data-name={text} style={{position: 'absolute', left: x, top: y, translate: '-50% 0', fontFamily: 'Londrina', fontSize: size, color: col, whiteSpace: 'nowrap', opacity: clamp((t - at) / 0.1),
    scale: `${0.65 + 0.35 * eo((t - at) / 0.28)}`, WebkitTextStroke: '12px rgb(44,32,30)', paintOrder: 'stroke fill'}}>{text}</div>
);
export const Tick: React.FC<{x: number; y: number; a: number; r?: number}> = ({x, y, a, r = 46}) => (
  <Svg a={a}><circle data-box="mark" data-name="tick" cx={x} cy={y} r={r} fill={GREEN} stroke={INK} strokeWidth={6} /><polyline points={`${x - r * 0.45},${y} ${x - r * 0.1},${y + r * 0.38} ${x + r * 0.5},${y - r * 0.38}`} fill="none" stroke="#fff" strokeWidth={r * 0.2} strokeLinecap="round" strokeLinejoin="round" /></Svg>
);
export const Cross: React.FC<{x: number; y: number; a: number; r?: number}> = ({x, y, a, r = 46}) => (
  <Svg a={a}><circle data-box="mark" data-name="cross" cx={x} cy={y} r={r} fill={RED} stroke={INK} strokeWidth={6} /><path d={`M${x - r * 0.38},${y - r * 0.38} L${x + r * 0.38},${y + r * 0.38} M${x + r * 0.38},${y - r * 0.38} L${x - r * 0.38},${y + r * 0.38}`} stroke="#fff" strokeWidth={r * 0.2} strokeLinecap="round" /></Svg>
);

// ---------- portada del canal (plantilla A «rayos»): la escena del gancho de TODOS los reels; el fotograma 0 es la miniatura ----------
export const CATEGORIES = {
  science: ['SCIENCE', [59, 130, 246]], nature: ['NATURE', [34, 197, 94]], history: ['HISTORY', [249, 115, 22]],
  body: ['BODY', [239, 68, 68]], space: ['SPACE', [139, 92, 246]], tech: ['TECH', [250, 204, 21]],
} as const;
export type Category = keyof typeof CATEGORIES;
export const CoverBg: React.FC<{cat: Category; angle: number}> = ({cat, angle}) => {
  const c = CATEGORIES[cat][1], col = (k: number) => `rgb(${c.map((v) => Math.round(v * k)).join(',')})`;
  return <><Grad top={col(0.95)} bot={col(0.42)} /><div style={{position: 'absolute', inset: 0, background: 'radial-gradient(ellipse 470px 390px at 540px 1080px, rgba(255,255,255,0.28), transparent)'}} /><Rays angle={angle} /></>;
};
// line1/line2: título corto (máx. ≈9 caracteres por línea); sub: la pregunta del gancho. La ilustración va entre y=860 y 1300.
export const CoverTitle: React.FC<{cat: Category; line1: string; line2: string; sub?: string}> = ({cat, line1, line2, sub}) => {
  const big: React.CSSProperties = {fontFamily: 'InterBlack', fontSize: 150, lineHeight: '170px', textTransform: 'uppercase', ...stroke(6)};
  return <>
    <div data-box="text" data-name="brand" style={{position: 'absolute', left: 90, top: 266, lineHeight: '50px', fontFamily: 'InterXB', fontSize: 38, color: GOLD, whiteSpace: 'nowrap', ...stroke(2)}}>MR. WHISKERFACT</div>
    <div data-box="text" data-name="category" style={{position: 'absolute', right: 90, top: 266, lineHeight: '40px', padding: '0 22px', borderRadius: 25, background: '#fff', border: `5px solid ${INK}`, fontFamily: 'InterBlack', fontSize: 34, color: INK}}>{CATEGORIES[cat][0]}</div>
    <div data-box="text" data-name={`${line1} ${line2}`} style={{position: 'absolute', left: 540, top: 385, translate: '-50% 0', textAlign: 'center', whiteSpace: 'nowrap'}}>
      <div style={{...big, color: '#fff'}}>{line1}</div><div style={{...big, color: 'rgb(255,222,90)'}}>{line2}</div>
    </div>
    {sub && <div data-box="text" data-name={sub} style={{position: 'absolute', left: 540, top: 745, translate: '-50% 0', fontFamily: 'InterXB', fontSize: 66, lineHeight: '90px', color: '#fff', whiteSpace: 'nowrap', ...stroke(4)}}>{sub}</div>}
  </>;
};
