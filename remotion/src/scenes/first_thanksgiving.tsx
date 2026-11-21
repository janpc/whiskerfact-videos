import React from 'react';
import meta from '../../public/meta.json';
import {FPS, TEXT, ACC, GOLD, INK, GREEN, RED, clamp, eo, eio, useFonts, Grad, Stars, Pines, Dunes, Card, Rays, Title, Label, Item, Svg, stroke} from '../common';

export const DUR = meta.frames / FPS;
const TI = 'thanksgiving_items', LT = 'large_thanksgiving', PM = 'pilgrim_man', WM = 'wampanoag_man';
export const SC: [string, number, number][] = [
  ['hook', 0, 3.9], ['opts', 3.9, 12.5], ['reveal', 12.5, 15.8], ['plym', 15.8, 24.7], ['feast', 24.7, 27.3], ['deer', 27.3, 32.5], ['birds', 32.5, 37.9],
  ['turkey', 37.9, 40.5], ['pie', 40.5, 46.6], ['sugar', 46.6, 48.8], ['pump', 48.8, 52.8], ['foot', 52.8, 58.3], ['letter', 58.3, 64.3], ['bonus', 64.3, 68.0], ['loop', 68.0, DUR],
];
export const CATS = new Set(['hook', 'reveal', 'loop', 'sugar']);
export const SWAP_AT = 2.6;
export const CURIOUS = new Set(['hook', 'turkey']);
export const SFX: [number, string, number][] = [...SC.slice(1, -1).map(([, a]): [number, string, number] => [a, 'whoosh', 0.5]),
  [3.9, 'pop', 0.5], [5.3, 'pop', 0.5], [7.1, 'pop', 0.5], [13.6, 'sparkle', 0.4], [28.3, 'tap', 0.5], [33.5, 'tap', 0.5], [21.4, 'click', 0.4], [41.7, 'click', 0.4]];

export const Bg: React.FC<{id: string; T: number}> = ({id, T}) => {
  switch (id) {
    case 'hook': case 'loop': return <><Grad top="rgb(58,28,56)" bot="rgb(222,112,44)" /><Rays angle={(id === 'loop' ? T - DUR : T) * 0.1} /></>;
    case 'opts': return <><Grad top="rgb(50,34,30)" bot="rgb(120,70,36)" /></>;
    case 'reveal': return <><Grad top="rgb(250,204,21)" bot="rgb(236,128,36)" /><Rays angle={-T * 0.1} /></>;
    case 'plym': return <><Grad top="rgb(126,70,40)" bot="rgb(60,34,30)" /><Pines y={1520} color="rgb(34,26,30)" seed={11} /></>;
    case 'feast': return <><Grad top="rgb(240,164,60)" bot="rgb(176,76,40)" /><Dunes y={1500} colors={['rgb(130,56,34)']} /></>;
    case 'deer': return <><Grad top="rgb(30,70,70)" bot="rgb(18,38,50)" /><Card /></>;
    case 'birds': return <><Grad top="rgb(78,116,150)" bot="rgb(40,60,96)" /><Card /></>;
    case 'turkey': return <><Grad top="rgb(96,58,96)" bot="rgb(50,30,70)" /><Stars T={T} seed={4} n={30} /></>;
    case 'pie': return <><Grad top="rgb(80,24,40)" bot="rgb(150,40,44)" /><Card /></>;
    case 'sugar': return <><Grad top="rgb(224,200,160)" bot="rgb(176,128,84)" /></>;
    case 'pump': return <><Grad top="rgb(232,150,50)" bot="rgb(160,70,30)" /><Card /></>;
    case 'foot': return <><Grad top="rgb(36,44,80)" bot="rgb(20,24,52)" /><Stars T={T} seed={31} /></>;
    case 'letter': return <><Grad top="rgb(116,96,66)" bot="rgb(64,50,38)" /><Card /></>;
    case 'bonus': return <><Grad top="rgb(26,100,120)" bot="rgb(14,46,70)" /><Dunes y={1480} colors={['rgb(20,70,96)']} /></>;
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
const Opt: React.FC<{cx: number; letter: string; name: string; sprite: string; h: number; a: number; dim?: number; win?: boolean}> = ({cx, letter, name, sprite, h, a, dim = 1, win}) => (
  <div style={{opacity: a * dim}}>
    <div style={{position: 'absolute', left: cx - 150, top: 640 + (1 - eo(a)) * 24, width: 300, height: 560, boxSizing: 'border-box', borderRadius: 32, background: 'rgb(233,226,190)', border: `5px solid ${win ? ACC : INK}`}} />
    <Big text={letter} y={650} size={130} t={1} col={win ? ACC : TEXT} x={cx} />
    <Item lib={TI} name={sprite} x={cx} y={940} h={h} a={1} />
    <Label text={name} y={1090} col={INK} a={1} x={cx} />
  </div>
);

export const Content: React.FC<{id: string; t: number; T: number}> = ({id, t, T}) => {
  const k = (a: number, d = 0.35) => eo((t - a) / d);
  switch (id) {
    case 'hook': return <>
      <Big text="POP QUIZ" y={300} size={190} t={t} at={0.15} col={ACC} />
      <Title k={k(1.0)} text="What was NOT at the" y={560} /><Title k={k(1.3)} text="first Thanksgiving?" y={660} />
      <Item lib={LT} name="harvest_feast_1621" x={620} y={1010} h={560} a={k(1.9)} />
    </>;
    case 'opts': return <>
      <Title k={k(0.1)} text="Which one is missing?" y={330} />
      <Opt cx={200} letter="A" name="deer" sprite="deer" h={270} a={k(0.0)} />
      <Opt cx={540} letter="B" name="wildfowl" sprite="duck" h={230} a={k(1.4)} />
      <Opt cx={880} letter="C" name="pumpkin pie" sprite="pumpkin_pie" h={170} a={k(3.2)} />
      <Label text="comment your answer" y={1260} col={ACC} a={k(5.0)} />
    </>;
    case 'reveal': {
      const win = clamp((t - 1.0) / 0.3);
      return <>
        <Big text="IT'S C" y={330} size={220} t={t} at={0.8} />
        <Item lib={TI} name="pumpkin_pie" x={540} y={840} h={260} a={k(0.9)} rot={Math.sin(t * 5) * 3} />
        <Cross x={760} y={740} a={clamp((t - 1.6) / 0.2)} r={60} />
        <Label text="no pumpkin pie" y={1010} col={INK} a={k(1.8)} />
      </>;
    }
    case 'plym': return <>
      <Title k={k(0.1)} text="Plymouth · autumn 1621" y={300} />
      <Item lib={LT} name="plymouth_1621" x={540} y={820} h={640} a={k(0.3)} />
      <Item lib={PM} name="talk" x={230} y={1180} h={300} a={k(2.5)} />
      <Item lib={WM} name="front" x={850} y={1180} h={320} a={k(5.2)} />
      <Label text="Massasoit + ~90 men" y={1330} col={TEXT} a={k(5.8)} />
    </>;
    case 'feast': return <>
      <Big text="3 DAYS" y={330} size={240} t={t} at={0.5} />
      <Item lib={LT} name="harvest_feast_1621" x={540} y={1010} h={760} a={k(0.2)} />
    </>;
    case 'deer': return <>
      <Title k={k(0.1)} text="Deer?" y={320} />
      <Item lib={TI} name="deer" x={540} y={980} h={360} a={k(0.3)} />
      <Tick x={760} y={800} a={clamp((t - 0.9) / 0.2)} r={70} />
      <Label text="5 deer, as gifts" y={1225} col={TEXT} a={k(2.5)} />
    </>;
    case 'birds': return <>
      <Title k={k(0.1)} text="Birds?" y={320} />
      <Item lib={TI} name="duck" x={400} y={1000} h={300} a={k(0.3)} />
      <Item lib={TI} name="wild_turkey" x={720} y={1010} h={300} a={k(2.0)} />
      <Tick x={820} y={800} a={clamp((t - 0.9) / 0.2)} r={70} />
      <Label text="ducks and geese, probably" y={1225} col={INK} a={k(3.3)} />
    </>;
    case 'turkey': return <>
      <Title k={k(0.1)} text="Turkey?" y={320} />
      <Item lib={TI} name="roast_turkey" x={540} y={1000} h={280} a={k(0.3)} />
      <Big text="?" y={520} size={200} t={t} at={1.3} col={ACC} />
      <Label text="historians aren't sure" y={1250} col={TEXT} a={k(1.6)} />
    </>;
    case 'pie': return <>
      <Title k={k(0.1)} text="Why no pie?" y={300} />
      <Item lib={TI} name="pumpkin_pie" x={540} y={860} h={220} a={k(0.3)} />
      {[['no butter', 1.2], ['no wheat flour', 2.4], ['no oven (probably)', 4.0]].map(([s, at], i) => <React.Fragment key={s as string}>
        <Cross x={250} y={1040 + i * 85} a={clamp((t - (at as number)) / 0.2)} r={34} />
        <Label text={s as string} y={1008 + i * 85} col={TEXT} a={k(at as number)} x={620} />
      </React.Fragment>)}
    </>;
    case 'sugar': return <>
      <Title k={k(0.1)} text="Sugar?" y={320} color={INK} />
      <Item lib={TI} name="sugar_loaf" x={780} y={900} h={300} a={k(0.3)} />
      <Label text="running low, likely" y={1130} col={INK} a={k(0.9)} x={720} />
    </>;
    case 'pump': return <>
      <Title k={k(0.1)} text="Pumpkins + squash?" y={300} />
      <Item lib={TI} name="pumpkin" x={400} y={960} h={280} a={k(0.3)} />
      <Item lib={TI} name="cooking_pot" x={730} y={980} h={250} a={k(1.0)} />
      <Tick x={560} y={820} a={clamp((t - 1.6) / 0.2)} r={60} />
      <Label text="yes, just not in a crust" y={1225} col={INK} a={k(2.4)} />
    </>;
    case 'foot': {
      const x1 = 200, x2 = 880, p = eio((t - 1.0) / 2.5);
      return <>
        <Title k={k(0.1)} text="Footnote" y={310} color={ACC} />
        <Svg><line x1={x1} y1={820} x2={x1 + (x2 - x1) * p} y2={820} stroke={TEXT} strokeWidth={10} strokeLinecap="round" />
          <circle cx={x1} cy={820} r={22} fill={ACC} stroke={INK} strokeWidth={6} /><circle cx={x2} cy={820} r={22} fill={ACC} stroke={INK} strokeWidth={6} opacity={clamp((t - 3.3) / 0.2)} /></Svg>
        <Label text="1621" y={870} col={TEXT} a={k(0.5)} x={x1} />
        <Label text="the name" y={870} col={ACC} a={k(3.4)} x={x2} />
        <Label text="~200 years later" y={720} col={TEXT} a={k(3.6)} />
        <Item lib={TI} name="mayflower" x={x1} y={1100} h={210} a={k(0.6)} />
      </>;
    }
    case 'letter': return <>
      <Title k={k(0.1)} text="One eyewitness letter" y={300} />
      <Item lib={TI} name="old_letter" x={540} y={940} h={330} a={k(0.3)} />
      <Label text="Edward Winslow" y={1170} col={INK} a={k(3.9)} />
    </>;
    case 'bonus': return <>
      <Title k={k(0.1)} text="Bonus" y={300} color={ACC} />
      <Item lib={TI} name="mussels" x={330} y={920} h={260} a={k(0.9)} />
      <Item lib={TI} name="eel" x={750} y={940} h={240} a={k(2.5)} />
      <Label text="mussels and eels, maybe" y={1100} col={TEXT} a={k(3.0)} />
    </>;
    default: return <>
      <Item lib={LT} name="modern_table" x={540} y={900} h={600} a={k(0.2)} />
      <Label text="this year, at your table…" y={470} col={ACC} a={k(0.5)} />
    </>;
  }
};
