import React from 'react';
import meta from '../../public/meta.json';
import {FPS, TEXT, ACC, INK, clamp, eo, eio, Svg, Grad, Stars, Card, Rays, Landscape, Ground, Stand, Title, Label, Item, Big, Tick, Cross, HeatWaves} from '../common';

export const DUR = meta.frames / FPS;
const NS = 'nose_w48', D = 'dog', SCI = 'scientist', YM = 'young_man';
export const SC: [string, number, number][] = [
  ['hook', 0, 2.95], ['wake', 2.95, 6.35], ['food', 6.35, 9.15], ['dogm', 9.15, 13.8], ['six', 13.8, 15.75], ['pools', 15.75, 21.35],
  ['map', 21.35, 24.95], ['detour', 24.95, 30.9], ['prints', 30.9, 33.5], ['time', 33.5, 39.65], ['brain', 39.65, 44.6], ['news', 44.6, 49.45],
  ['twist', 49.45, 52.95], ['crawl', 52.95, 58.9], ['thirds', 58.9, 60.35], ['coffee', 60.35, 63.2], ['loop', 63.2, DUR],
];
export const CATS = new Set(['hook', 'twist', 'loop']);
export const SWAP_AT = 1.9;
export const CURIOUS = new Set(['hook']);
export const SFX: [number, string, number][] = [...SC.slice(1, -1).map(([, a]): [number, string, number] => [a, 'whoosh', 0.45]),
  [6.52, 'pop', 0.35], [6.98, 'pop', 0.35], [7.67, 'pop', 0.35], [8.31, 'pop', 0.35], [11.2, 'sparkle', 0.4], [42.7, 'tap', 0.4], [59.3, 'click', 0.4]];

export const Bg: React.FC<{id: string; T: number}> = ({id, T}) => {
  const rays = (angle: number) => <><Grad top="rgb(30,180,86)" bot="rgb(12,80,40)" /><Rays angle={angle} /><Ground /></>;
  switch (id) {
    case 'hook': case 'loop': return rays((id === 'loop' ? T - DUR : T) * 0.1);
    case 'wake': return <Landscape sky="dawn" terrain="hills" T={T} seed={4} />;
    case 'food': return <><Grad top="rgb(30,150,80)" bot="rgb(14,76,44)" /><Card y={430} h={860} /></>;
    case 'dogm': return <Landscape sky="night" terrain="pines" T={T} seed={2} />;
    case 'six': return <Landscape sky="sunset" terrain="dunes" T={T} seed={1} />;
    case 'pools': return <Landscape sky="day" terrain="hills" T={T} seed={8} />;
    case 'map': return <Landscape sky="day" terrain="city" T={T} seed={5} />;
    case 'detour': return <><Grad top="rgb(112,40,70)" bot="rgb(56,20,48)" /><Card /></>;
    case 'prints': return <Landscape sky="storm" terrain="forest" T={T} seed={6} />;
    case 'time': return <Landscape sky="dusk" terrain="pines" T={T} seed={3} />;
    case 'brain': return <><Grad top="rgb(18,24,58)" bot="rgb(44,30,80)" /><Stars T={T} seed={14} n={80} /><Card /></>;
    case 'news': return <Landscape sky="day" terrain="autumn" T={T} seed={7} />;
    case 'twist': return rays(-T * 0.14);
    case 'crawl': return <Landscape sky="sunset" terrain="forest" T={T} seed={9} />;
    case 'thirds': return <Landscape sky="dawn" terrain="city" T={T} seed={11} />;
    default: return <Landscape sky="dusk" terrain="hills" T={T} seed={12} />;
  }
};

const Dots: React.FC<{t: number}> = ({t}) => {
  const n = Math.round(300 * eio((t - 0.5) / 2.0));
  return <Svg>{Array.from({length: n}).map((_, i) => <circle key={i} cx={125 + (i % 20) * 38} cy={540 + Math.floor(i / 20) * 33} r={11} fill={ACC} stroke={INK} strokeWidth={3} />)}</Svg>;
};
const StreetMap: React.FC<{t: number}> = ({t}) => {
  const trails: [string, string, number][] = [
    ['M120 560 C 300 600, 250 800, 480 790 S 720 700, 860 760', 'rgb(222,64,60)', 0.2],
    ['M160 980 C 330 860, 520 1010, 600 860 S 700 560, 830 540', 'rgb(104,62,180)', 0.7],
    ['M480 480 C 380 640, 620 660, 560 800 S 300 900, 330 1010', 'rgb(240,140,30)', 1.2],
  ];
  return <Svg>
    <rect x={70} y={430} width={830} height={640} rx={36} fill="rgb(233,226,190)" stroke={INK} strokeWidth={6} />
    <path d="M70 690 L900 640 M70 900 L900 940 M330 430 L300 1070 M650 430 L700 1070" stroke="rgb(190,180,150)" strokeWidth={40} />
    {trails.map(([d, c, at], i) => <g key={i}><mask id={`m${i}`}><path d={d} fill="none" stroke="#fff" strokeWidth={30} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - eio((t - at) / 1.6)} /></mask>
      <path d={d} mask={`url(#m${i})`} fill="none" stroke={c} strokeWidth={14} strokeLinecap="round" strokeDasharray="2 30" /></g>)}
  </Svg>;
};
const Arrow: React.FC<{x: number; y0: number; y1: number; k: number}> = ({x, y0, y1, k}) => {
  const y = y0 + (y1 - y0) * k;
  return <Svg a={clamp(k * 5)}><path d={`M${x} ${y0} L${x} ${y} M${x - 60} ${y + 70} L${x} ${y} L${x + 60} ${y + 70}`} fill="none" stroke={INK} strokeWidth={46} strokeLinecap="round" strokeLinejoin="round" />
    <path d={`M${x} ${y0} L${x} ${y} M${x - 60} ${y + 70} L${x} ${y} L${x + 60} ${y + 70}`} fill="none" stroke={ACC} strokeWidth={24} strokeLinecap="round" strokeLinejoin="round" /></Svg>;
};
const Trail: React.FC<{d: string; t: number}> = ({d, t}) => <Svg a={clamp(t / 0.4)}><path d={d} fill="none" stroke="rgb(96,56,36)" strokeWidth={14} strokeLinecap="round" strokeDasharray="6 30" strokeDashoffset={-t * 40} /></Svg>;

export const Content: React.FC<{id: string; t: number; T: number}> = ({id, t, T}) => {
  const k = (a: number, d = 0.35) => eo((t - a) / d);
  const pop = (a: number) => clamp((t - a) / 0.15);
  const bob = Math.sin(T * 2.4) * 6;
  // Zona segura: bajo y=900 nada pasa de x=900; centro óptico ≈ x=485; subtítulos en y=1390.
  switch (id) {
    case 'hook': return <>
      <Big text="A DOG'S NOSE" y={250} size={165} t={9} col={ACC} />
      <Big text="for one day?" y={455} size={125} t={9} />
      <Stand lib={NS} name="man_dog_nose" x={595} h={500} />
      <Stand lib={D} name="curious" x={825} h={160} />
    </>;
    case 'wake': return <>
      <Title k={k(0.05)} text="Good morning" y={290} />
      <HeatWaves cx={520} y0={470} y1={690} T={T} a={k(0.8)} spread={130} />
      <Item lib={NS} name="breakfast_plate" x={560} y={920} h={390} a={k(0.5)} />
      <Stand lib={YM} name="surprised" x={160} h={340} a={k(0.2)} />
      <Stand lib={D} name="happy" x={730} h={190} a={k(1.4)} />
    </>;
    case 'food': return <>
      <Title k={k(0)} text="One breakfast, four smells" y={290} />
      <Item lib={NS} name="fried_eggs" x={275} y={650} h={270} a={pop(0.15)} />
      <Item lib={NS} name="bacon" x={715} y={650} h={290} a={pop(0.62)} />
      <Item lib={NS} name="toast" x={275} y={1080} h={290} a={pop(1.3)} />
      <Item lib={NS} name="coffee_mug" x={705} y={1080} h={290} a={pop(1.95)} />
    </>;
    case 'dogm': return <>
      <Title k={k(0.05)} text="Dog · up to" y={260} />
      <Big text="300 MILLION" y={375} size={150} t={t} at={2.0} col={ACC} />
      <Dots t={t} />
      <Stand lib={D} name="happy" x={290} h={270} a={k(0.3)} />
      <Stand lib={SCI} name="point" x={720} h={300} a={k(1.0)} />
    </>;
    case 'six': return <>
      <Title k={k(0)} text="You" y={270} />
      <Big text="6 MILLION" y={390} size={180} t={t} at={0.5} col={ACC} />
      <Svg>{Array.from({length: 6}).map((_, i) => <circle key={i} cx={230 + i * 124} cy={700} r={30 * eo((t - 0.2 - i * 0.12) / 0.2)} fill="rgb(222,64,60)" stroke={INK} strokeWidth={6} />)}</Svg>
      <Stand lib={YM} name="shrug" x={560} h={400} a={k(0.15)} />
      <Stand lib={D} name="look_back" x={210} h={240} a={k(0.5)} />
    </>;
    case 'pools': return <>
      <Title k={k(0.05)} text="1 teaspoon of sugar" y={270} />
      <Item lib={NS} name="sugar_spoon" x={480} y={540 + bob} h={220} a={k(0.4)} />
      <Item lib={NS} name="swimming_pool" x={270} y={890} h={260} a={k(3.7)} />
      <Item lib={NS} name="swimming_pool" x={690} y={890} h={260} a={k(4.1)} />
      <Stand lib={D} name="curious" x={280} h={260} a={k(1.5)} />
      <Stand lib={SCI} name="think" x={700} h={290} a={k(0.2)} />
    </>;
    case 'map': return <>
      <Title k={k(0.05)} text="The scent map" y={270} />
      <StreetMap t={t} />
      <Stand lib={NS} name="lamp_post" x={170} h={240} a={k(0.2)} />
      <Stand lib={D} name="curious" x={520} h={220} a={k(0.1)} />
    </>;
    case 'detour': return <>
      <Big text="≈ 12%" y={250} size={220} t={t} at={1.4} col={ACC} x={430} />
      <Title k={k(0.1)} text="of each sniff takes a detour" y={560} />
      <Item lib={NS} name="nose_cutaway" x={480} y={960} h={420} a={k(0.3)} />
      <Label text="smell area · back of the nose" y={1220} col={INK} a={k(3.9)} x={500} />
    </>;
    case 'prints': return <>
      <Title k={k(0)} text="Which way did they go?" y={270} />
      <Item lib={NS} name="shoe_prints" x={330} y={790} h={540} a={k(0.1)} />
      <Arrow x={700} y0={900} y1={520} k={eio((t - 1.0) / 1.0)} />
      <Stand lib={D} name="run2" x={640} h={220} a={k(0.5)} />
    </>;
    case 'time': return <>
      <Title k={k(0.05)} text="Can dogs smell time?" y={270} />
      <Label text="hours ago" y={450} col={TEXT} a={k(3.6)} x={260} />
      <Label text="just now" y={450} col={TEXT} a={k(4.7)} x={710} />
      <HeatWaves cx={260} y0={540} y1={660} T={T * 0.4} a={0.28 * k(3.4)} spread={80} />
      <HeatWaves cx={710} y0={540} y1={660} T={T} a={k(4.5)} spread={100} />
      <Item lib={NS} name="shoe_prints" x={260} y={810} h={230} a={0.4 * k(1.0)} />
      <Item lib={NS} name="shoe_prints" x={710} y={810} h={230} a={k(1.3)} />
      <Stand lib={SCI} name="think" x={485} h={360} a={k(0.2)} />
    </>;
    case 'brain': return <>
      <Title k={k(0.05)} text="Smell center" y={270} />
      <Big text="≈ 40x" y={390} size={220} t={t} at={3.0} col={ACC} x={500} />
      <Label text="for its brain size" y={745} col={INK} a={k(0.5)} x={500} />
      <Item lib={NS} name="brain_compare" x={500} y={990} h={290} a={k(0.3)} />
      <Label text="dog" y={1180} col={INK} a={k(1.5)} x={320} />
      <Label text="human" y={1180} col={INK} a={k(2.0)} x={700} />
    </>;
    case 'news': return <>
      <Title k={k(0.05)} text="Today's walk" y={270} />
      <Item lib={NS} name="newspaper" x={500} y={690} h={500} rot={6 * (1 - k(0.2, 0.6)) - 3} a={k(0.2)} />
      <Stand lib={NS} name="lamp_post" x={160} h={320} a={k(0.6)} />
      <Stand lib={NS} name="dog_sniffing" x={540} h={290} a={k(1.0)} />
    </>;
    case 'twist': return <>
      <Big text="PLOT TWIST" y={270} size={180} t={t} at={0.1} col={ACC} />
      <Title k={k(1.4)} text="Your nose isn't bad" y={500} />
      <Stand lib={SCI} name="surprised" x={560} h={400} a={k(0.4)} />
      <Stand lib={YM} name="jump" x={770} h={370} a={k(1.2)} lift={Math.abs(Math.sin(t * 3)) * 16} />
    </>;
    case 'crawl': return <>
      <Title k={k(0.05)} text="The chocolate trail" y={270} />
      <Stand lib={NS} name="human_crawl_trail" x={300} h={340} a={k(0.2)} />
      <Trail d="M545 1335 C 580 1270, 620 1380, 650 1335" t={t - 2.6} />
      <Stand lib={NS} name="chocolate_bar" x={660} h={180} a={k(3.8)} />
      <Stand lib={SCI} name="point" x={825} h={320} a={k(0.8)} />
    </>;
    case 'thirds': return <>
      <Big text="2 of 3" y={270} size={230} t={t} at={0.05} col={ACC} x={500} />
      <Tick x={225} y={660} a={pop(0.35)} r={62} />
      <Tick x={480} y={660} a={pop(0.55)} r={62} />
      <Cross x={730} y={660} a={pop(0.75)} r={62} />
      <Stand lib={YM} name="happy" x={225} h={390} />
      <Stand lib={YM} name="jump" x={470} h={340} />
      <Stand lib={YM} name="shrug" x={735} h={390} />
    </>;
    case 'coffee': return <>
      <Title k={k(0.05)} text="Tomorrow's homework" y={270} />
      <HeatWaves cx={400} y0={700} y1={930} T={T} a={k(0.5)} spread={110} />
      <Stand lib={NS} name="coffee_mug" x={400} h={360} a={k(0.15)} />
      <Stand lib={YM} name="think" x={760} h={380} a={k(0.5)} />
    </>;
    default: return <>
      <Big text="WHAT IF...?" y={270} size={180} t={t} at={1.5} col={ACC} />
      <Stand lib={D} name="sit" x={580} h={330} a={k(0.2)} />
      <Stand lib={YM} name="think" x={790} h={420} a={k(0.5)} />
    </>;
  }
};
