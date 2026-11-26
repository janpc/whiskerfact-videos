import React from 'react';
import meta from '../../public/meta.json';
import {FPS, TEXT, ACC, INK, clamp, eo, eio, Svg, Grad, Stars, Dunes, Pines, Card, Rays, Skyline, Title, Label, Item, Big, Tick, Cross, HeatWaves} from '../common';

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
  switch (id) {
    case 'hook': case 'loop': return <><Grad top="rgb(24,66,104)" bot="rgb(226,128,52)" /><Rays angle={(id === 'loop' ? T - DUR : T) * 0.1} /></>;
    case 'wake': return <><Grad top="rgb(250,176,90)" bot="rgb(190,82,80)" /><Dunes y={1500} colors={['rgb(140,56,66)']} /></>;
    case 'food': return <Grad top="rgb(24,104,104)" bot="rgb(12,56,68)" />;
    case 'dogm': return <><Grad top="rgb(40,26,80)" bot="rgb(18,14,44)" /></>;
    case 'six': return <Grad top="rgb(238,226,196)" bot="rgb(206,176,134)" />;
    case 'pools': return <><Grad top="rgb(40,120,180)" bot="rgb(14,54,104)" /><Dunes y={1520} colors={['rgb(12,46,90)']} /></>;
    case 'map': return <><Grad top="rgb(118,170,110)" bot="rgb(58,112,78)" /></>;
    case 'detour': return <><Grad top="rgb(112,40,70)" bot="rgb(56,20,48)" /><Card /></>;
    case 'prints': return <><Grad top="rgb(190,150,104)" bot="rgb(132,96,68)" /></>;
    case 'time': return <><Grad top="rgb(14,16,48)" bot="rgb(52,32,90)" /><Stars T={T} seed={21} n={80} /></>;
    case 'brain': return <><Grad top="rgb(30,96,76)" bot="rgb(14,52,48)" /><Card /></>;
    case 'news': return <><Grad top="rgb(250,210,80)" bot="rgb(234,134,50)" /><Skyline y={1620} color="rgb(104,58,52)" seed={9} T={T} /></>;
    case 'twist': return <><Grad top="rgb(150,36,90)" bot="rgb(60,18,64)" /><Rays angle={-T * 0.14} /></>;
    case 'crawl': return <><Grad top="rgb(140,196,224)" bot="rgb(96,160,180)" /><Pines y={1500} color="rgb(40,98,66)" seed={6} /></>;
    case 'thirds': return <><Grad top="rgb(52,52,66)" bot="rgb(26,26,36)" /></>;
    default: return <><Grad top="rgb(124,80,54)" bot="rgb(58,34,30)" /><Stars T={T} seed={3} n={24} /></>;
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
      <Item lib={NS} name="man_dog_nose" x={350} y={920 + bob * 0.6} h={560} />
      <Item lib={D} name="curious" x={725} y={1080 - bob} h={280} />
    </>;
    case 'wake': return <>
      <Title k={k(0.05)} text="Good morning" y={290} />
      <HeatWaves cx={520} y0={470} y1={690} T={T} a={k(0.8)} spread={130} />
      <Item lib={NS} name="breakfast_plate" x={560} y={920} h={390} a={k(0.5)} />
      <Item lib={YM} name="surprised" x={160} y={1160} h={340} a={k(0.2)} />
      <Item lib={D} name="happy" x={730} y={1265 - (1 - k(1.4)) * 40} h={190} a={k(1.4)} />
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
      <Item lib={D} name="happy" x={290} y={1195} h={270} a={k(0.3)} />
      <Item lib={SCI} name="point" x={720} y={1185} h={300} a={k(1.0)} />
    </>;
    case 'six': return <>
      <Title k={k(0)} text="You" y={270} color={INK} />
      <Big text="6 MILLION" y={390} size={180} t={t} at={0.5} col={ACC} />
      <Svg>{Array.from({length: 6}).map((_, i) => <circle key={i} cx={230 + i * 124} cy={700} r={30 * eo((t - 0.2 - i * 0.12) / 0.2)} fill="rgb(222,64,60)" stroke={INK} strokeWidth={6} />)}</Svg>
      <Item lib={YM} name="shrug" x={560} y={1040} h={400} a={k(0.15)} />
      <Item lib={D} name="look_back" x={210} y={1140} h={240} a={k(0.5)} />
    </>;
    case 'pools': return <>
      <Title k={k(0.05)} text="1 teaspoon of sugar" y={270} />
      <Item lib={NS} name="sugar_spoon" x={480} y={540 + bob} h={220} a={k(0.4)} />
      <Item lib={NS} name="swimming_pool" x={270} y={890} h={260} a={k(3.7)} />
      <Item lib={NS} name="swimming_pool" x={690} y={890} h={260} a={k(4.1)} />
      <Item lib={D} name="curious" x={280} y={1190} h={260} a={k(1.5)} />
      <Item lib={SCI} name="think" x={700} y={1190} h={290} a={k(0.2)} />
    </>;
    case 'map': return <>
      <Title k={k(0.05)} text="The scent map" y={270} />
      <StreetMap t={t} />
      <Item lib={NS} name="lamp_post" x={170} y={1225} h={270} a={k(0.2)} />
      <Item lib={D} name="walk1" x={430 + 130 * eio(t / 3.4)} y={1200} h={240} a={k(0.1)} />
    </>;
    case 'detour': return <>
      <Big text="≈ 12%" y={250} size={220} t={t} at={1.4} col={ACC} x={430} />
      <Title k={k(0.1)} text="of each sniff takes a detour" y={560} />
      <Item lib={NS} name="nose_cutaway" x={480} y={960} h={420} a={k(0.3)} />
      <Label text="smell area · back of the nose" y={1220} col={INK} a={k(3.9)} x={500} />
    </>;
    case 'prints': return <>
      <Title k={k(0)} text="Which way did they go?" y={270} color={INK} />
      <Item lib={NS} name="shoe_prints" x={330} y={790} h={540} a={k(0.1)} />
      <Arrow x={700} y0={900} y1={520} k={eio((t - 1.0) / 1.0)} />
      <Item lib={D} name="run2" x={640} y={1215 - (1 - k(0.5)) * 60} h={220} a={k(0.5)} />
    </>;
    case 'time': return <>
      <Title k={k(0.05)} text="Can dogs smell time?" y={270} />
      <HeatWaves cx={260} y0={760} y1={920} T={T * 0.4} a={0.28 * k(3.4)} spread={80} />
      <HeatWaves cx={710} y0={470} y1={920} T={T} a={k(4.5)} spread={100} />
      <Item lib={NS} name="shoe_prints" x={260} y={1070} h={230} a={0.4 * k(1.0) + 0} />
      <Item lib={NS} name="shoe_prints" x={710} y={1070} h={230} a={k(1.3)} />
      <Item lib={SCI} name="think" x={485} y={720} h={320} a={k(0.2)} />
      <Label text="hours ago" y={1235} col={TEXT} a={k(3.6)} x={260} />
      <Label text="just now" y={1235} col={TEXT} a={k(4.7)} x={710} />
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
      <Title k={k(0.05)} text="Today's walk" y={270} color={INK} />
      <Item lib={NS} name="newspaper" x={500} y={690} h={500} rot={6 * (1 - k(0.2, 0.6)) - 3} a={k(0.2)} />
      <Item lib={NS} name="lamp_post" x={160} y={1130} h={320} a={k(0.6)} />
      <Item lib={NS} name="dog_sniffing" x={540} y={1170} h={290} a={k(1.0)} />
    </>;
    case 'twist': return <>
      <Big text="PLOT TWIST" y={270} size={180} t={t} at={0.1} col={ACC} />
      <Title k={k(1.4)} text="Your nose isn't bad" y={500} />
      <Item lib={SCI} name="surprised" x={270} y={950} h={400} a={k(0.4)} />
      <Item lib={YM} name="jump" x={690} y={950 - Math.abs(Math.sin(t * 3)) * 16} h={390} a={k(1.2)} />
    </>;
    case 'crawl': return <>
      <Title k={k(0.05)} text="The chocolate trail" y={270} color={INK} />
      <Item lib={NS} name="human_crawl_trail" x={470} y={700} h={430} a={k(0.2)} />
      <Trail d="M470 980 C 620 1040, 540 1150, 390 1170" t={t - 2.6} />
      <Item lib={NS} name="chocolate_bar" x={230} y={1160} h={280} a={k(3.8)} />
      <Item lib={SCI} name="point" x={730} y={1160} h={310} a={k(0.8)} />
    </>;
    case 'thirds': return <>
      <Big text="2 of 3" y={270} size={230} t={t} at={0.05} col={ACC} x={500} />
      <Tick x={225} y={660} a={pop(0.35)} r={62} />
      <Tick x={480} y={660} a={pop(0.55)} r={62} />
      <Cross x={730} y={660} a={pop(0.75)} r={62} />
      <Item lib={YM} name="happy" x={225} y={980} h={390} />
      <Item lib={YM} name="jump" x={470} y={980} h={340} />
      <Item lib={YM} name="shrug" x={735} y={980} h={390} />
    </>;
    case 'coffee': return <>
      <Title k={k(0.05)} text="Tomorrow's homework" y={270} />
      <HeatWaves cx={440} y0={440} y1={680} T={T} a={k(0.5)} spread={110} />
      <Item lib={NS} name="coffee_mug" x={440} y={930} h={380} a={k(0.15)} />
      <Item lib={YM} name="think" x={770} y={1120} h={360} a={k(0.5)} />
    </>;
    default: return <>
      <Big text="WHAT IF...?" y={270} size={180} t={t} at={1.5} col={ACC} />
      <Item lib={D} name="sit" x={290} y={880} h={380} a={k(0.2)} />
      <Item lib={YM} name="think" x={690} y={900} h={400} a={k(0.5)} />
    </>;
  }
};
