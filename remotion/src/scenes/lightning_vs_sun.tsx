import React from 'react';
import meta from '../../public/meta.json';
import {FPS, TEXT, ACC, INK, GREEN, RED, clamp, eo, eio, Grad, Stars, Dunes, Pines, Card, Rays, Title, Label, Item, Svg} from '../common';

export const DUR = meta.frames / FPS;
const LI = 'lightning_items', SC_ = 'scientist', CG = 'child_girl';
export const SC: [string, number, number][] = [
  ['hook', 0, 3.4], ['rounds', 3.4, 5.6], ['heat', 5.6, 12.5], ['surf', 12.5, 15.5], ['five', 15.5, 19.6], ['fulg', 19.6, 25.2], ['flash', 25.2, 30.1],
  ['years', 30.1, 34.4], ['final', 34.4, 36.9], ['core', 36.9, 40.8], ['cant', 40.8, 43.5], ['score', 43.5, 45.8], ['beats', 45.8, 48.9], ['nap', 48.9, 51.6], ['loop', 51.6, DUR],
];
export const CATS = new Set(['hook', 'nap', 'loop']);
export const SWAP_AT = 2.4;
export const CURIOUS = new Set(['hook']);
export const SFX: [number, string, number][] = [...SC.slice(1, -1).map(([, a]): [number, string, number] => [a, 'whoosh', 0.5]),
  [9.6, 'sparkle', 0.4], [18.2, 'pop', 0.5], [22.7, 'click', 0.4], [28.0, 'click', 0.4], [33.2, 'pop', 0.5], [42.4, 'tap', 0.5], [44.6, 'pop', 0.5]];

export const Bg: React.FC<{id: string; T: number}> = ({id, T}) => {
  switch (id) {
    case 'hook': case 'loop': return <><Grad top="rgb(40,40,96)" bot="rgb(232,120,50)" /><Rays angle={(id === 'loop' ? T - DUR : T) * 0.1} /></>;
    case 'rounds': return <><Grad top="rgb(60,34,96)" bot="rgb(30,22,64)" /><Stars T={T} seed={7} n={40} /></>;
    case 'heat': return <><Grad top="rgb(34,30,58)" bot="rgb(176,60,40)" /><Pines y={1560} color="rgb(26,20,34)" seed={5} /></>;
    case 'surf': return <><Grad top="rgb(250,214,70)" bot="rgb(240,130,40)" /><Rays angle={-T * 0.12} /></>;
    case 'five': return <><Grad top="rgb(30,50,96)" bot="rgb(20,28,66)" /><Card /></>;
    case 'fulg': return <><Grad top="rgb(236,190,120)" bot="rgb(200,140,80)" /><Dunes y={1400} colors={['rgb(214,160,92)', 'rgb(190,130,70)']} /></>;
    case 'flash': return <><Grad top="rgb(20,90,100)" bot="rgb(12,44,70)" /><Card /></>;
    case 'years': return <><Grad top="rgb(10,14,40)" bot="rgb(40,26,80)" /><Stars T={T} seed={21} n={90} /></>;
    case 'final': return <><Grad top="rgb(110,30,70)" bot="rgb(50,16,50)" /><Rays angle={T * 0.15} /></>;
    case 'core': return <><Grad top="rgb(130,30,30)" bot="rgb(240,120,40)" /><Stars T={T} seed={13} n={30} /></>;
    case 'cant': return <><Grad top="rgb(70,86,130)" bot="rgb(40,50,90)" /><Card /></>;
    case 'score': return <><Grad top="rgb(30,100,70)" bot="rgb(14,56,50)" /><Stars T={T} seed={2} n={40} /></>;
    case 'beats': return <><Grad top="rgb(96,60,110)" bot="rgb(190,100,80)" /><Card /></>;
    case 'nap': return <><Grad top="rgb(255,220,120)" bot="rgb(240,150,70)" /><Rays angle={T * 0.08} /></>;
    default: return <Grad top="rgb(40,30,70)" bot="rgb(180,90,70)" />;
  }
};

const Big: React.FC<{text: string; y: number; size: number; t: number; at?: number; col?: string; x?: number}> = ({text, y, size, t, at = 0, col = TEXT, x = 540}) => (
  <div style={{position: 'absolute', left: x, top: y, translate: '-50% 0', fontFamily: 'Londrina', fontSize: size, color: col, whiteSpace: 'nowrap', opacity: clamp((t - at) / 0.1),
    scale: `${0.65 + 0.35 * eo((t - at) / 0.28)}`, WebkitTextStroke: '12px rgb(44,32,30)', paintOrder: 'stroke fill'}}>{text}</div>
);
const Tick: React.FC<{x: number; y: number; a: number; r?: number}> = ({x, y, a, r = 46}) => (
  <Svg a={a}><circle cx={x} cy={y} r={r} fill={GREEN} stroke={INK} strokeWidth={6} /><polyline points={`${x - r * 0.45},${y} ${x - r * 0.1},${y + r * 0.38} ${x + r * 0.5},${y - r * 0.38}`} fill="none" stroke="#fff" strokeWidth={r * 0.2} strokeLinecap="round" strokeLinejoin="round" /></Svg>
);
const Cross: React.FC<{x: number; y: number; a: number; r?: number}> = ({x, y, a, r = 46}) => (
  <Svg a={a}><circle cx={x} cy={y} r={r} fill={RED} stroke={INK} strokeWidth={6} /><path d={`M${x - r * 0.38},${y - r * 0.38} L${x + r * 0.38},${y + r * 0.38} M${x + r * 0.38},${y - r * 0.38} L${x - r * 0.38},${y + r * 0.38}`} stroke="#fff" strokeWidth={r * 0.2} strokeLinecap="round" /></Svg>
);

export const Content: React.FC<{id: string; t: number; T: number}> = ({id, t, T}) => {
  const k = (a: number, d = 0.35) => eo((t - a) / d);
  const bob = Math.sin(T * 2.2) * 6;
  switch (id) {
    case 'hook': return <>
      <Title k={1} text="Lightning vs the Sun" y={330} />
      <Title k={1} text="Which is hotter?" y={440} color={ACC} />
      <Item lib={LI} name="lightning_bolt" x={420} y={900 + bob} h={330} a={1} />
      <Item lib={LI} name="sun_disc" x={800} y={870 - bob} h={300} a={1} />
      <Big text="VS" y={650} size={150} t={9} col={ACC} x={610} />
      <Item lib={SC_} name="think" x={930} y={1170} h={290} a={1} />
    </>;
    case 'rounds': return <>
      <Big text="3 ROUNDS" y={290} size={190} t={t} at={0.1} col={ACC} />
      {[['thermometer', 'heat', 200], ['stopwatch', 'time', 540], ['sun_core_glow', 'core', 880]].map(([n, l, x], i) => <React.Fragment key={n as string}>
        <Item lib={LI} name={n as string} x={x as number} y={850} h={230} a={k(0.4 + i * 0.4)} />
        <Label text={`${i + 1} · ${l}`} y={1000} col={TEXT} a={k(0.5 + i * 0.4)} x={x as number} />
      </React.Fragment>)}
      <Item lib={SC_} name="talk" x={300} y={1200} h={280} a={k(0.3)} />
    </>;
    case 'heat': return <>
      <Title k={k(0.1)} text="Round 1 · Heat" y={300} />
      <Item lib={LI} name="storm_cloud" x={300} y={650} h={190} a={k(0.5)} />
      <Item lib={LI} name="lightning_bolt" x={300} y={960} h={340} a={k(0.9)} />
      <Item lib={LI} name="thermometer" x={780} y={900} h={330} a={k(2.8)} />
      <Big text="50,000°F" y={1100} size={140} t={t} at={3.6} col={ACC} x={680} />
      <Item lib={CG} name="surprised" x={540} y={1160} h={260} a={k(4.8)} />
    </>;
    case 'surf': return <>
      <Title k={k(0.1)} text="The Sun's surface" y={300} />
      <Item lib={LI} name="sun_disc" x={540} y={820} h={380} rot={T * 6} a={k(0.3)} />
      <Big text="10,000°F" y={1060} size={150} t={t} at={1.5} col={TEXT} />
      <Item lib={SC_} name="think" x={900} y={1000} h={280} a={k(0.8)} />
    </>;
    case 'five': return <>
      <Big text="5 times hotter" y={280} size={170} t={t} at={0.3} col={ACC} />
      <Item lib={SC_} name="happy" x={150} y={1090} h={230} a={k(1.0)} />
      <Item lib={LI} name="lightning_bolt" x={380} y={1030} h={330} a={k(0.3)} />
      <Item lib={LI} name="sun_disc" x={800} y={1050} h={190} a={k(0.6)} />
      <Tick x={590} y={1030} a={clamp((t - 2.5) / 0.2)} r={56} />
      <Label text="Point · lightning" y={1235} col={INK} a={k(2.6)} />
    </>;
    case 'fulg': return <>
      <Title k={k(0.1)} text="Sand into glass" y={300} />
      <Item lib={LI} name="lightning_bolt" x={540} y={650} h={260} a={k(0.5)} />
      <Item lib={LI} name="fulgurite" x={540} y={1000} h={330} a={k(3.8)} />
      <Item lib={LI} name="beach_pail" x={850} y={1130} h={220} a={k(1.0)} />
      <Item lib={CG} name="surprised" x={200} y={1130} h={300} a={k(1.6)} />
      <Label text="fulgurite" y={1230} col={TEXT} a={k(4.3)} />
    </>;
    case 'flash': return <>
      <Title k={k(0.1)} text="Round 2 · Time" y={300} />
      <Item lib={LI} name="lightning_bolt" x={230} y={1010} h={300} a={clamp(Math.sin(T * 30) * 3 + 1.2)} />
      <Item lib={LI} name="stopwatch" x={560} y={940} h={340} a={k(0.3)} />
      <Big text="< 1 s" y={540} size={170} t={t} at={3.3} col={ACC} />
      <Item lib={SC_} name="think" x={880} y={1080} h={280} a={k(1.0)} />
    </>;
    case 'years': return <>
      <Title k={k(0.1)} text="Billions of years" y={300} />
      <Item lib={LI} name="sun_disc" x={540} y={800} h={320} rot={T * 6} a={k(0.3)} />
      <Item lib={LI} name="hourglass_space" x={220} y={1000} h={270} a={k(0.8)} />
      <Item lib={CG} name="talk" x={860} y={1100} h={290} a={k(1.2)} />
      <Tick x={760} y={640} a={clamp((t - 2.8) / 0.2)} r={50} />
      <Label text="Point · Sun" y={1230} col={TEXT} a={k(2.9)} />
    </>;
    case 'final': return <>
      <Big text="ROUND 3" y={330} size={230} t={t} at={0.2} col={ACC} />
      <Item lib={LI} name="sun_core_glow" x={540} y={900} h={380} a={k(0.5)} />
      <Item lib={SC_} name="point" x={880} y={1130} h={270} a={k(1.2)} />
      <Label text="deep inside" y={1180} col={TEXT} a={k(1.0)} x={300} />
    </>;
    case 'core': return <>
      <Title k={k(0.1)} text="The Sun's core" y={300} />
      <Item lib={LI} name="sun_core_glow" x={560} y={720} h={270} a={k(0.3)} />
      <Item lib={LI} name="thermometer" x={220} y={1000} h={330} a={k(0.8)} />
      <Big text="27,000,000°F" y={930} size={130} t={t} at={2.2} col={ACC} x={640} />
      <Item lib={SC_} name="surprised" x={880} y={1250} h={220} a={k(2.8)} />
    </>;
    case 'cant': return <>
      <Title k={k(0.1)} text="Out of reach" y={300} />
      <Item lib={LI} name="lightning_bolt" x={230} y={1020} h={290} a={k(0.3)} />
      <Item lib={LI} name="sun_core_glow" x={820} y={1020} h={250} a={k(0.5)} />
      <Cross x={540} y={1020} a={clamp((t - 0.8) / 0.2)} r={64} />
      <Label text="Point · Sun" y={1230} col={INK} a={k(1.5)} />
    </>;
    case 'score': return <>
      <Title k={k(0.1)} text="Final score" y={300} />
      <Item lib={LI} name="sun_disc" x={300} y={1010} h={230} a={k(0.2)} />
      <Item lib={LI} name="lightning_bolt" x={780} y={1010} h={280} a={k(0.2)} />
      <Big text="2" y={640} size={260} t={t} at={0.5} col={ACC} x={300} />
      <Big text="1" y={640} size={260} t={t} at={1.0} col={TEXT} x={780} />
      <Item lib={CG} name="happy" x={540} y={1230} h={260} a={k(1.2)} />
    </>;
    case 'beats': return <>
      <Title k={k(0.1)} text="Surface vs heart" y={300} />
      <Item lib={LI} name="sun_disc" x={290} y={960} h={230} a={k(0.2)} />
      <Item lib={LI} name="lightning_bolt" x={540} y={1000} h={300} a={k(0.2)} />
      <Item lib={LI} name="sun_core_glow" x={790} y={960} h={230} a={k(0.2)} />
      <Tick x={290} y={800} a={clamp((t - 0.9) / 0.2)} r={50} />
      <Cross x={790} y={800} a={clamp((t - 2.0) / 0.2)} r={50} />
      <Label text="surface" y={1130} col={INK} a={k(0.5)} x={290} />
      <Label text="core" y={1130} col={INK} a={k(1.6)} x={790} />
    </>;
    case 'nap': return <>
      <Title k={k(0.1)} text="Sunbeam nap" y={300} color={INK} />
      <Item lib={LI} name="sun_disc" x={800} y={800} h={300} rot={T * 6} a={k(0.3)} />
      <Big text="z z z" y={1000} size={140} t={t} at={1.2} col={TEXT} x={700} />
      <Item lib={CG} name="shrug" x={920} y={1170} h={250} a={k(0.8)} />
    </>;
    default: return <>
      <Big text="?" y={330} size={260} t={t} at={0.2} col={ACC} />
      <Item lib={LI} name="lightning_bolt" x={470} y={820} h={320} a={k(0.3)} />
      <Item lib={LI} name="sun_disc" x={800} y={800} h={280} a={k(0.5)} />
      <Item lib={SC_} name="shrug" x={930} y={1210} h={260} a={k(1.0)} />
    </>;
  }
};
