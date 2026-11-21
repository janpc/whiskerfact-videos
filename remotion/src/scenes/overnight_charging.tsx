import React from 'react';
import meta from '../../public/meta.json';
import {FPS, TEXT, ACC, GOLD, INK, GREEN, RED, clamp, eo, eio, lerp, useFonts, Grad, Stars, Skyline, Dunes, Pines, Card, Rays, Grain,
  Title, Label, Item, Battery, HeatWaves, BI, LW} from '../common';

export const DUR = meta.frames / FPS;
export const SC: [string, number, number][] = [
  ['hook', 0, 3.1], ['myth', 3.1, 5.7], ['nickel', 5.7, 13.7], ['lith', 13.7, 18.1], ['full', 18.1, 23.3], ['learn', 23.3, 28.6],
  ['enemy', 28.6, 31.4], ['heat', 31.4, 37.8], ['combo', 37.8, 43.6], ['verdict', 43.6, 49.0], ['ask', 49.0, 52.3], ['loop', 52.3, DUR],
];
export const CATS = new Set(['hook', 'myth', 'verdict', 'ask', 'loop']);
const sceneOf = (T: number) => SC.find(([, a, b]) => T >= a && T < b) ?? SC[SC.length - 1];

export const Bg: React.FC<{id: string; T: number}> = ({id, T}) => {
  switch (id) {
    case 'hook': case 'loop': return <><Grad top="rgb(34,28,78)" bot="rgb(232,112,72)" /><Stars T={T} /><Rays angle={T * 0.12} /></>;
    case 'myth': return <><Grad top="rgb(250,204,21)" bot="rgb(240,150,40)" /><Rays angle={-T * 0.1} /></>;
    case 'nickel': return <><Grad top="rgb(96,92,84)" bot="rgb(52,48,44)" /><Card /></>;
    case 'lith': return <><Grad top="rgb(30,120,150)" bot="rgb(14,52,80)" /><Card /></>;
    case 'full': return <><Grad top="rgb(18,24,64)" bot="rgb(44,30,92)" /><Stars T={T} seed={9} /><Skyline y={1500} color="rgb(16,14,40)" seed={3} T={T} /></>;
    case 'learn': return <><Grad top="rgb(26,44,84)" bot="rgb(70,52,110)" /><Stars T={T} seed={21} n={40} /><Pines y={1560} color="rgb(18,24,52)" seed={7} /></>;
    case 'enemy': return <><Grad top="rgb(255,168,64)" bot="rgb(214,60,40)" /><Dunes y={1250} colors={['rgb(190,70,40)', 'rgb(150,48,36)']} /></>;
    case 'heat': return <><Grad top="rgb(246,150,60)" bot="rgb(200,70,44)" /><Dunes y={1400} colors={['rgb(170,60,38)', 'rgb(128,40,32)']} /></>;
    case 'combo': return <><Grad top="rgb(60,20,40)" bot="rgb(150,36,40)" /><Card /></>;
    case 'verdict': return <><Grad top="rgb(36,40,96)" bot="rgb(20,20,56)" /><Stars T={T} seed={33} /><Rays angle={T * 0.08} /></>;
    default: return <Grad top="rgb(34,28,78)" bot="rgb(180,90,90)" />;
  }
};

const Big: React.FC<{text: string; y: number; size: number; t: number; at?: number}> = ({text, y, size, t, at = 0}) => (
  <div style={{position: 'absolute', left: 540, top: y, translate: '-50% 0', fontFamily: 'Londrina', fontSize: size, color: TEXT, whiteSpace: 'nowrap', opacity: clamp((t - at) / 0.1),
    scale: `${0.65 + 0.35 * eo((t - at) / 0.28)}`, WebkitTextStroke: '12px rgb(44,32,30)', paintOrder: 'stroke fill'}}>{text}</div>
);

export const Content: React.FC<{id: string; t: number; T: number}> = ({id, t, T}) => {
  const k = (a: number, d = 0.35) => eo((t - a) / d);
  switch (id) {
    case 'hook': {
      const f = 0.15 + 0.85 * ((0.9 * T + 1e-6) % 1.0);
      return <>
        <Title k={k(0.1)} text="Charging overnight" y={300} /><Title k={k(0.5)} text="kills your" y={400} /><Title k={k(0.9)} text="battery?" y={500} color={ACC} />
        <Item lib={LW} name="charging_phone_big" x={640} y={1000 + 6 * Math.sin(T * 2.4)} h={390} a={k(0.2)} />
        <Battery cx={250} cy={930} w={210} f={f} a={k(0.4)} bolt />
      </>;
    }
    case 'myth': return <>
      <Big text="MYTH" y={420} size={250} t={t} />
      <Label text="…but not completely" y={730} col="rgb(255,250,235)" a={k(1.4)} />
    </>;
    case 'nickel': {
      const f = clamp(1 - ((t - 2.2) / 5.2) * 0.45);
      return <>
        <Title k={k(0.1)} text="Old nickel batteries" y={290} />
        <Item lib={BI} name="nicd_battery" x={290} y={1040} h={310} a={k(0.3)} />
        <Item lib={BI} name="old_phone" x={790} y={1040} h={380} a={k(0.5)} />
        <Label text={'the "memory effect"'} y={752} col={INK} a={k(2.2)} />
        <Battery cx={540} cy={1215} w={340} f={f} a={k(2.4)} />
        <Label text={t > 4.5 ? 'seems to lose capacity' : 'recharged before empty…'} y={1300} col={INK} a={k(2.8)} />
      </>;
    }
    case 'lith': return <>
      <Title k={k(0.1)} text="Your phone: lithium-ion" y={290} />
      <Item lib={BI} name="li_battery" x={540} y={930} h={360} a={k(0.3)} />
      <Battery cx={540} cy={1230} w={360} f={0.92} a={k(0.9)} />
      <Label text="practically no memory effect" y={1310} col={GREEN} a={k(2.3)} />
    </>;
    case 'full': {
      const f = clamp(t / 2.2), hold = t > 2.4;
      return <>
        <Title k={k(0.1)} text="1. It stops when full" y={290} />
        <Battery cx={540} cy={680} w={380} f={f} a={k(0.2)} bolt={!hold} />
        <Item lib={BI} name="wall_socket" x={200} y={1080} h={230} a={k(0.3)} />
        <Item lib={BI} name="charging_cable" x={430} y={1100} h={150} a={k(0.4)} />
        <Item lib={BI} name="phone_charging" x={800} y={1080} h={380} a={k(0.5)} />
        <Label text={hold ? '100% · tiny top-ups' : `${Math.round(f * 100)}%`} y={780} col={TEXT} a={k(0.5)} />
      </>;
    }
    case 'learn': return <>
      <Title k={k(0.1)} text="It learns your routine" y={290} />
      <Item lib={LW} name="bedroom_night" x={540} y={1000} h={540} a={k(0.3)} />
      <Battery cx={540} cy={620} w={420} f={0.8} capLine={0.8} a={k(1.4)} />
      <Label text="holds around 80%" y={700} col={TEXT} a={k(2.4)} />
    </>;
    case 'enemy': return <>
      <Title k={k(0.1)} text="2. The real enemy" y={300} />
      <Big text="HEAT" y={470} size={290} t={t} at={1.2} />
      <Item lib={BI} name="thermometer" x={540} y={1080} h={420} a={k(0.3)} />
      <HeatWaves cx={540} y0={800} y1={900} T={t} a={k(1.2)} />
    </>;
    case 'heat': {
      const f = lerp(0.95, 0.62, eio((t - 1.2) / 4.5));
      return <>
        <Title k={k(0.1)} text="Heat + full charge" y={290} />
        <Item lib={LW} name="sun_cutaway" x={290} y={960} h={340} a={k(0.3)} />
        <HeatWaves cx={290} y0={760} y1={820} T={t} a={k(0.6)} n={2} spread={70} />
        <Battery cx={720} cy={960} w={380} f={f} a={k(0.5)} plate />
        <Label text="capacity lost for good" y={1130} col={TEXT} a={k(2.2)} />
      </>;
    }
    case 'combo': return <>
      <Title k={k(0.1)} text="Worst combo?" y={290} />
      <Item lib={LW} name="phone_under_pillow" x={540} y={1090} h={460} a={k(0.3)} />
      <HeatWaves cx={540} y0={640} y1={790} T={t} a={k(2.0)} />
      <Label text="full + hot" y={770} col={RED} a={k(1.1)} />
    </>;
    case 'verdict': return <>
      <Title k={k(0.1)} text="The verdict" y={310} color={ACC} />
      <Big text="NOT THE NIGHT" y={450} size={130} t={t} at={1.0} />
      <Big text="HEAT + 100%" y={620} size={150} t={t} at={2.6} />
    </>;
    case 'ask': return <>
      <Title k={k(0.1)} text="Be honest…" y={310} />
      <Label text="tell me below" y={460} col={ACC} a={k(1.9)} />
      <Item lib={BI} name="phone_charging" x={800} y={1000} h={330} a={k(0.4)} />
    </>;
    default: return <>
      <Title k={1} text="Charging overnight" y={300} /><Title k={1} text="kills your" y={400} /><Title k={1} text="battery?" y={500} color={ACC} />
      <Item lib={LW} name="charging_phone_big" x={640} y={1000} h={390} a={1} />
    </>;
  }
};

// efectos de sonido [segundo, nombre, volumen] (tap, whoosh, pop, click, sparkle)
export const SFX: [number, string, number][] = [...SC.slice(1, -1).map(([, a]): [number, string, number] => [a, 'whoosh', 0.5]), [0.9, 'pop', 0.5], [9.1, 'click', 0.5], [33.5, 'tap', 0.5], [51.0, 'sparkle', 0.4]];
export const SWAP_AT = 2.6; // segundo en que el gato pasa de stand_front a explain (en la primera escena)
export const CURIOUS = new Set(['ask']); // escenas con ojos curiosos
