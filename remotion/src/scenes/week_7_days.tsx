import React from 'react';
import {Img, staticFile} from 'remotion';
import meta from '../../public/meta.json';
import {FPS, W, H, TEXT, ACC, GOLD, INK, CREAM, RED, clamp, eo, eio, Svg, Grad, Stars, Card, Rays, Landscape, Ground, GROUND_Y, FLOOR, Stand, Title, Label, Item, Big, Tick, Cross} from '../common';

export const DUR = meta.frames / FPS;
const WK = 'week_w48', AP = 'ancient_person', AY = 'ancient_youth', YM = 'young_man', SCI = 'scientist', CG = 'child_girl', MI = 'moon_items';
export const SC: [string, number, number][] = [
  ['hook', 0, 2.55], ['sky', 2.55, 8.3], ['nothing', 8.3, 13.6], ['babylon', 13.6, 16.9], ['lights', 16.9, 23.9], ['moon', 23.9, 28.65],
  ['sabbath', 28.65, 32.5], ['rome', 32.5, 39.05], ['coin', 39.05, 45.15], ['names', 45.15, 52.15], ['spanish', 52.15, 56.8], ['twist', 56.8, 58.7],
  ['france', 58.7, 64.45], ['tired', 64.45, 67.25], ['ended', 67.25, 72.25], ['habit', 72.25, 76.9], ['loop', 76.9, DUR],
];
export const CATS = new Set(['hook', 'twist', 'loop']);
export const SWAP_AT = 1.7;
export const CURIOUS = new Set(['hook']);
export const SFX: [number, string, number][] = [...SC.slice(1, -1).map(([, a]): [number, string, number] => [a, 'whoosh', 0.4]),
  [3.0, 'pop', 0.3], [4.55, 'pop', 0.3], [6.4, 'pop', 0.3], [37.35, 'click', 0.45], [40.9, 'tap', 0.4], [47.3, 'pop', 0.3], [49.15, 'pop', 0.3], [50.65, 'pop', 0.3],
  [57.7, 'click', 0.45], [70.0, 'tap', 0.45], [76.9, 'sparkle', 0.35]];

const hookBg = (a: number) => <><Grad top="rgb(214,128,40)" bot="rgb(110,52,24)" /><Rays angle={a} /></>;

// ---------- fondos propios de este reel ----------
const Sea: React.FC<{T: number}> = ({T}) => (<>
  <Grad top="rgb(10,16,48)" bot="rgb(40,62,110)" /><Stars T={T} seed={31} n={70} maxY={950} />
  <Svg>{[0, 1, 2, 3].map((i) => { const y = 1070 + i * 85; const pts = Array.from({length: 60}).map((_, k) => `${k * 19},${y + 16 * Math.sin(k * 0.45 + T * (0.8 + i * 0.25) + i * 2)}`).join(' ');
    return <polygon key={i} points={`0,${H} ${pts} ${W},${H}`} fill={['rgb(30,80,112)', 'rgb(24,66,96)', 'rgb(18,52,80)', 'rgb(12,38,62)'][i]} />; })}</Svg>
  <Ground color="rgb(70,54,40)" />
</>);
const Room: React.FC<{T: number}> = ({T}) => (<>
  <Grad top="rgb(96,52,56)" bot="rgb(150,92,62)" />
  <Svg>
    {[150, 930].map((x) => <g key={x}><path d={`M${x - 80} 560 V420 A80 80 0 0 1 ${x + 80} 420 V560 Z`} fill="rgb(38,40,96)" stroke="rgb(60,32,28)" strokeWidth={14} />
      <circle cx={x - 20} cy={440 + 3 * Math.sin(T)} r={6} fill="#fff" /><circle cx={x + 30} cy={500} r={4} fill="#fff" /></g>)}
    <rect x={0} y={1170} width={W} height={18} fill="rgb(96,56,40)" />
  </Svg>
  <Ground color="rgb(82,48,32)" />
</>);
const Forum: React.FC = () => (<>
  <Grad top="rgb(86,36,96)" bot="rgb(190,104,96)" />
  <Svg>{[-10, 140, 830, 980].map((x, i) => <g key={i} fill="rgba(240,222,196,0.32)"><rect x={x + 12} y={600} width={86} height={720} /><rect x={x} y={560} width={110} height={44} rx={8} />
    {[34, 56, 78].map((d) => <rect key={d} x={x + d} y={620} width={6} height={680} fill="rgba(90,50,80,0.3)" />)}</g>)}</Svg>
  <Ground color="rgb(92,58,60)" />
</>);
const Paris: React.FC<{T: number}> = ({T}) => (<>
  <Grad top="rgb(36,62,128)" bot="rgb(120,140,190)" />
  <Svg>{Array.from({length: 9}).map((_, i) => { const x = i * 130 - 20, h = 190 + ((i * 73) % 130); return <g key={i}><rect x={x} y={GROUND_Y - h} width={118} height={h} fill="rgb(58,56,96)" />
    <polygon points={`${x - 6},${GROUND_Y - h} ${x + 20},${GROUND_Y - h - 56} ${x + 98},${GROUND_Y - h - 56} ${x + 124},${GROUND_Y - h}`} fill="rgb(40,38,70)" /></g>; })}
    {[0, 1, 2].map((i) => <ellipse key={i} cx={((i * 430 + T * 14) % 1400) - 160} cy={330 + i * 190} rx={170} ry={40} fill="rgba(255,255,255,0.13)" />)}</Svg>
  <Ground />
</>);

export const Bg: React.FC<{id: string; T: number}> = ({id, T}) => {
  switch (id) {
    case 'hook': case 'loop': return hookBg(T * 0.1);
    case 'sky': return <><Grad top="rgb(22,96,128)" bot="rgb(10,52,76)" /><Card y={330} h={980} /></>;
    case 'nothing': return <Landscape sky="night" terrain="hills" T={T} seed={21} />;
    case 'babylon': return <Landscape sky="sunset" terrain="dunes" T={T} seed={17} />;
    case 'lights': return <><Grad top="rgb(8,10,34)" bot="rgb(62,40,96)" /><Stars T={T} seed={23} n={110} /><Ground color="rgb(60,44,50)" /></>;
    case 'moon': return <Sea T={T} />;
    case 'sabbath': return <Room T={T} />;
    case 'rome': return <Landscape sky="day" terrain="dunes" T={T} seed={27} />;
    case 'coin': return <Forum />;
    case 'names': return <><Grad top="rgb(40,30,92)" bot="rgb(18,14,50)" /><Stars T={T} seed={41} n={80} /><Card y={290} h={1030} /></>;
    case 'spanish': return <Landscape sky="dusk" terrain="city" T={T} seed={19} />;
    case 'twist': return <><Grad top="rgb(190,50,60)" bot="rgb(96,18,38)" /><Rays angle={-T * 0.14} /><Ground color="rgb(66,14,28)" /></>;
    case 'france': return <Paris T={T} />;
    case 'tired': return <Landscape sky="storm" terrain="hills" T={T} seed={33} />;
    case 'ended': return <Landscape sky="dawn" terrain="autumn" T={T} seed={29} />;
    default: return <Landscape sky="day" terrain="forest" T={T} seed={37} />;
  }
};

// fila de n días; `gold` resalta uno
const Days: React.FC<{n: number; y: number; t: number; gold?: number; goldA?: number; at?: number; step?: number}> = ({n, y, t, gold = -1, goldA = 1, at = 0, step = 0.1}) => {
  const x0 = 76, tw = 818, gap = 14, w = (tw - gap * (n - 1)) / n;
  return <Svg>{Array.from({length: n}).map((_, i) => { const a = eo((t - at - i * step) / 0.25), g = i === gold && goldA > 0.5;
    return <g key={i} opacity={a} transform={`translate(0 ${(1 - a) * 30})`}><rect x={x0 + i * (w + gap)} y={y} width={w} height={130} rx={16} fill={g ? ACC : CREAM} stroke={INK} strokeWidth={6} />
      <text x={x0 + i * (w + gap) + w / 2} y={y + 87} textAnchor="middle" fontFamily="Londrina" fontSize={64} fill={INK}>{i + 1}</text></g>; })}</Svg>;
};
const Candle: React.FC<{x: number; T: number; i: number; a: number}> = ({x, T, i, a}) => {
  const f = 1 + 0.12 * Math.sin(T * 11 + i * 2) * Math.sin(T * 7 + i);
  return <Svg a={a}><ellipse cx={x} cy={900} rx={70} ry={90} fill="rgba(255,200,90,0.22)" /><path d={`M${x} ${940} C ${x - 40} ${915} ${x - 8} ${880} ${x + 3} ${940 - 95 * f} C ${x + 10} ${885} ${x + 40} ${915} ${x} ${940} Z`} fill="rgb(255,184,50)" stroke={INK} strokeWidth={5} />
    <rect x={x - 24} y={945} width={48} height={170} rx={8} fill="rgb(250,246,232)" stroke={INK} strokeWidth={6} /><path d={`M${x - 60} 1115 H${x + 60} L${x + 38} 1150 H${x - 38} Z`} fill={GOLD} stroke={INK} strokeWidth={6} /></Svg>;
};
// moneda: se recorta al retrato (la inscripción del sprite es texto inventado)
const Coin: React.FC<{x: number; y: number; d: number; k: number}> = ({x, y, d, k}) => k <= 0.003 ? null : (
  <div data-box="item" data-name="coin" style={{position: 'absolute', left: x - d / 2, top: y - d / 2, width: d, height: d, boxSizing: 'border-box', borderRadius: '50%', background: 'rgb(180,112,64)', border: `10px solid ${INK}`, overflow: 'hidden', opacity: k, scale: `${0.8 + 0.2 * k}`, boxShadow: '0 16px 0 rgba(0,0,0,0.28)'}}>
    <Img src={staticFile(`spr/${WK}__roman_coin.png`)} style={{position: 'absolute', left: '50%', top: '50%', width: d * 1.28, translate: '-50% -50%', clipPath: 'ellipse(25.5% 37% at 50% 50%)'}} />
    <svg width={d - 20} height={d - 20} style={{position: 'absolute', left: 0, top: 0}}><circle cx={(d - 20) / 2} cy={(d - 20) / 2} r={d * 0.41} fill="none" stroke="rgb(120,70,40)" strokeWidth={12} strokeDasharray="4 22" strokeLinecap="round" /></svg>
  </div>
);
const Chevron: React.FC<{x: number; y: number; a: number}> = ({x, y, a}) => <Svg a={a}><path d={`M${x - 16} ${y - 30} L${x + 18} ${y} L${x - 16} ${y + 30}`} fill="none" stroke={INK} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" /></Svg>;

export const Content: React.FC<{id: string; t: number; T: number}> = ({id, t, T}) => {
  const k = (a: number, d = 0.35) => eo((t - a) / d);
  const pop = (a: number) => clamp((t - a) / 0.15);
  const bob = Math.sin(T * 2.4) * 6;
  // Zona segura: bajo y=900 nada pasa de x=900; centro óptico ≈ x=485; subtítulos en y=1390.
  switch (id) {
    case 'hook': return <>
      <Big text="WHY 7 DAYS?" y={265} size={185} t={9} col={ACC} />
      <Item lib={WK} name="wall_calendar" x={540} y={825} h={600} rot={Math.sin(T * 1.6) * 1.5} />
      <Item lib={MI} name="sun" x={140} y={640} h={150} rot={T * 8} />
      <Item lib={WK} name="saturn" x={940} y={590} h={110} />
    </>;
    case 'sky': {
      const rows: [string, string, string, number, number][] = [[MI, 'sun', '1 spin', 0.45, 495], [MI, 'moon_near', '1 moon cycle', 2.0, 815], [WK, 'seasons_wheel', '1 orbit', 3.85, 1140]];
      return <>{rows.map(([l, n, s, at, y], i) => <React.Fragment key={n}>
        <Item lib={l} name={n} x={260} y={y} h={250} a={k(at)} rot={i === 2 ? -T * 10 : 0} />
        <Big text={['DAY', 'MONTH', 'YEAR'][i]} y={y - 105} size={110} t={t} at={at + 0.15} col={ACC} x={650} />
        <Label text={s} y={y + 30} col={INK} a={k(at + 0.5)} x={650} />
      </React.Fragment>)}</>;
    }
    case 'nothing': return <>
      <Big text="7 DAYS?" y={280} size={200} t={t} at={1.6} col={ACC} />
      <Item lib={MI} name="moon_near" x={250} y={700 + bob} h={290} a={k(0.1)} />
      <Item lib={WK} name="saturn" x={745} y={700 - bob} h={170} a={k(0.5)} />
      <Cross x={485} y={700} a={pop(1.9)} r={62} />
      <Stand lib={YM} name={t < 3.2 ? 'shrug' : 'think'} x={300} h={400} a={k(0.2)} />
      <Stand lib={SCI} name="think" x={715} h={390} a={k(3.2)} />
    </>;
    case 'babylon': return <>
      <Title k={k(0.05)} text="Ancient Babylon" y={260} />
      <Item lib={WK} name="babylon_night_sky" x={485} y={710} h={580} a={k(0.1)} />
      <Stand lib={AP} name="point" x={250} h={300} a={k(0.5)} />
      <Item lib={WK} name="clay_tablet" x={660} y={1190} h={250} a={k(1.2)} rot={4} />
    </>;
    case 'lights': {
      const xs = [125, 246, 341, 437, 547, 662, 815];
      const at = [2.95, 3.7, 4.5, 4.8, 5.1, 5.4, 5.7];
      return <>
        <Big text="7 LIGHTS" y={270} size={170} t={t} at={1.7} col={ACC} x={485} />
        <Item lib={WK} name="seven_lights" x={485} y={610 + bob * 0.5} h={112} a={k(0.5)} />
        {xs.map((x, i) => <Label key={i} text={`${i + 1}`} y={720} col={TEXT} a={k(at[i], 0.2)} x={x} />)}
        <Item lib={WK} name="star_chart" x={485} y={990} h={310} a={k(0.2)} />
        <Stand lib={AP} name="surprised" x={170} h={300} a={k(0.2)} />
        <Stand lib={AY} name="front" x={780} h={270} a={k(0.9)} />
      </>;
    }
    case 'moon': return <>
      <Title k={k(0.05)} text="The Moon's main phases" y={280} />
      <Item lib={WK} name="moon_phases" x={540} y={560} h={185} a={k(0.2)} />
      {[330, 540, 750].map((x, i) => <Big key={x} text="≈7" y={685} size={90} t={t} at={2.0 + i * 0.35} col={ACC} x={x} />)}
      <Item lib={MI} name="moon_near" x={620} y={990 + bob} h={310} a={k(0.5)} />
      <Stand lib={SCI} name="point" x={240} h={390} a={k(0.3)} />
    </>;
    case 'sabbath': return <>
      <Title k={k(0.05)} text="The Sabbath" y={280} />
      <Days n={7} y={560} t={t} at={0.2} gold={6} goldA={k(1.0)} />
      <Candle x={400} T={T} i={0} a={k(0.8)} />
      <Candle x={570} T={T} i={1} a={k(1.0)} />
      <Stand lib={AP} name="happy" x={180} h={330} a={k(0.2)} />
      <Stand lib={AY} name="sit" x={775} h={220} a={k(0.5)} />
    </>;
    case 'rome': return <>
      <Title k={k(0)} text={t < 4.7 ? 'Rome: market week' : 'The planet week won'} y={270} />
      <Days n={8} y={450} t={t} at={0.3} step={0.12} />
      <Cross x={843} y={515} a={pop(4.85)} r={54} />
      <Item lib={WK} name="market_stall" x={585} y={1085} h={500} a={k(0.15)} />
      <Stand lib={AP} name={t < 4.7 ? 'talk' : 'shrug'} x={162} h={320} a={k(0.5)} />
    </>;
    case 'coin': return <>
      <Big text="321 AD" y={270} size={210} t={t} at={0.15} col={ACC} />
      <Coin x={485} y={760} d={440} k={k(0.9)} />
      <Label text="Sunday = day off" y={1004} col={TEXT} a={k(3.0)} x={485} />
      <Stand lib={AP} name="happy" x={290} h={222} a={k(2.6)} />
      <Stand lib={AY} name="jump" x={690} h={222} a={k(3.2)} lift={10 + Math.abs(Math.sin(t * 3.4)) * 18} />
    </>;
    case 'names': {
      const rows: [string, string, number, string, number, number][] = [[WK, 'saturn', 170, 'SATURDAY', 1.9, 475], [MI, 'sun', 240, 'SUNDAY', 3.75, 805], [MI, 'moon_near', 230, 'MONDAY', 5.25, 1135]];
      return <>{rows.map(([l, n, h, s, at, y]) => <React.Fragment key={s}>
        <Item lib={l} name={n} x={280} y={y} h={h} a={k(at - 1.4)} rot={n === 'sun' ? T * 8 : 0} />
        <Big text={s} y={y - 55} size={96} t={t} at={at} col={ACC} x={680} />
      </React.Fragment>)}</>;
    }
    case 'spanish': return <>
      <Title k={k(0.05)} text="In Spanish" y={280} />
      <Item lib={WK} name="mars" x={285} y={640 + bob} h={330} a={k(0.2)} />
      <Item lib={WK} name="venus" x={720} y={640 - bob} h={330} a={k(0.45)} />
      <Big text="MARTES" y={850} size={100} t={t} at={0.75} col={ACC} x={285} />
      <Big text="VIERNES" y={850} size={100} t={t} at={2.55} col={ACC} x={700} />
      <Stand lib={CG} name="point" x={280} h={300} a={k(0.5)} />
      <Stand lib={CG} name="happy" x={700} h={300} a={k(2.4)} />
    </>;
    case 'twist': return <>
      <Big text="7" y={235} size={520} t={t} at={0.05} col={ACC} />
      <Cross x={780} y={690} a={pop(0.9)} r={85} />
      <Stand lib={YM} name="surprised" x={640} h={400} a={k(0.3)} />
    </>;
    case 'france': return <>
      <Big text="1793" y={240} size={200} t={t} at={0.1} col={ACC} />
      <Item lib={WK} name="revolution_calendar" x={485} y={742} h={450} a={k(0.6)} />
      <Label text="10-day week" y={1000} col={TEXT} a={k(2.1)} x={320} />
      <Item lib={WK} name="decimal_clock" x={320} y={1210} h={240} a={k(3.8)} />
      <Stand lib={SCI} name="talk" x={730} h={320} a={k(0.5)} />
    </>;
    case 'tired': return <>
      <Title k={k(0)} text="Rest day: number 10" y={290} />
      <Days n={10} y={500} t={t} at={0.1} step={0.09} gold={9} goldA={k(1.3)} />
      <Stand lib={YM} name="think" x={250} h={440} a={k(0.1)} />
      <Stand lib={CG} name="shrug" x={640} h={340} a={k(0.4)} />
    </>;
    case 'ended': return <>
      <Big text="1806" y={250} size={220} t={t} at={2.1} col={ACC} />
      <Item lib={WK} name="revolution_calendar" x={485} y={760 + 50 * eio((t - 2.7) / 0.8)} h={390} rot={-14 * eio((t - 2.7) / 0.8)} a={k(0.1)} />
      <Cross x={815} y={590} a={pop(3.3)} r={75} />
      <Stand lib={SCI} name="shrug" x={230} h={260} a={k(0.5)} />
      <Stand lib={YM} name="happy" x={720} h={270} a={k(3.4)} />
    </>;
    case 'habit': return <>
      <Title k={k(0.05)} text="A very old habit" y={290} />
      <Item lib={WK} name="clay_tablet" x={220} y={660} h={220} a={k(0.2)} />
      <Chevron x={375} y={660} a={k(0.8)} />
      <Item lib={WK} name="ziggurat" x={540} y={660} h={200} a={k(1.2)} />
      <Chevron x={710} y={660} a={k(2.0)} />
      <Item lib={WK} name="wall_calendar" x={880} y={660} h={225} a={k(2.5)} />
      <Stand lib={SCI} name="happy" x={250} h={400} a={k(0.4)} />
      <Stand lib={CG} name="wave" x={660} h={320} a={k(2.4)} />
    </>;
    default: return <>
      <Big text="HAPPY WEEKEND" y={290} size={140} t={t} at={0.05} col={ACC} />
      <Item lib={WK} name="weekend_hammock" x={540} y={840} h={540} a={k(0)} />
    </>;
  }
};
