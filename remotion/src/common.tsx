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
  a <= 0.003 ? null : <Img src={staticFile(`spr/${lib}__${name}.png`)} style={{position: 'absolute', left: x, top: y, height: h, translate: '-50% -50%', rotate: `${-rot}deg`, opacity: a}} />;
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

// ---------- texto ----------
export const Title: React.FC<{k: number; text: string; color?: string; y?: number}> = ({k, text, color = TEXT, y = 360}) => (
  <div style={{position: 'absolute', left: 540, top: y + (1 - eo(k)) * 30, translate: '-50% 0', fontFamily: 'Londrina', fontSize: 94, lineHeight: 1.15, color, opacity: k, whiteSpace: 'nowrap', ...stroke(3)}}>{text}</div>
);
export const Label: React.FC<{text: string; y: number; col: string; a: number; x?: number}> = ({text, y, col, a, x = 540}) => {
  if (a <= 0.003) return null;
  const light = (/rgb\((\d+),(\d+),(\d+)\)/.exec(col)?.slice(1).reduce((p, v) => p + +v, 0) ?? 0) > 380;
  return (
    <div style={{position: 'absolute', left: x, top: y + (1 - eo(a)) * 30, translate: '-50% 0', fontFamily: 'Londrina', fontSize: 52, lineHeight: 1.1, color: col, opacity: a, whiteSpace: 'nowrap',
      padding: light ? '4px 18px 6px' : 0, borderRadius: 999, background: light ? 'rgba(30,22,22,0.67)' : 'none'}}>{text}</div>
  );
};

// ---------- fondos propios ----------
export const Grad: React.FC<{top: string; bot: string}> = ({top, bot}) => <div style={{position: 'absolute', inset: 0, background: `linear-gradient(${top}, ${bot})`}} />;
export const Stars: React.FC<{T: number; n?: number; seed?: number}> = ({T, n = 70, seed = 5}) => {
  const r = rng(seed);
  return <Svg>{Array.from({length: n}).map((_, i) => <circle key={i} cx={r() * W} cy={r() * 1500} r={1.5 + r() * 2.4} fill="#fff" opacity={0.35 + 0.5 * Math.abs(Math.sin(T * (0.6 + r()) + i))} />)}</Svg>;
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
export const Card: React.FC = () => <div style={{position: 'absolute', left: 56, top: 742, width: 968, height: 642, boxSizing: 'border-box', borderRadius: 36, background: CREAM, border: `4px solid ${INK}`}} />;
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
