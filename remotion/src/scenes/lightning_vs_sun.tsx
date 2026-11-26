import React from 'react';
import meta from '../../public/meta.json';
import {FPS, TEXT, ACC, INK, GREEN, RED, clamp, eo, eio, Grad, Stars, Dunes, Pines, Card, Rays, Title, Label, Item, Big, Tick, Cross} from '../common';

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
    case 'hook': case 'loop': return <><Grad top="rgb(40,40,96)" bot="rgb(232,120,50)" /><Rays angle={T * 0.1} /></>;
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


export const Content: React.FC<{id: string; t: number; T: number}> = ({id, t, T}) => {
  const k = (a: number, d = 0.35) => eo((t - a) / d);
  const bob = Math.sin(T * 2.2) * 6;
  // Zona segura (igual que factory/brand.py): por debajo de y=900 nada pasa de x=900 (botones de la app); centro óptico ≈ x=485.
  switch (id) {
    case 'hook': return <>
      <Title k={1} text="Lightning vs the Sun" y={330} />
      <Title k={1} text="Which is hotter?" y={440} color={ACC} />
      <Item lib={LI} name="lightning_bolt" x={250} y={880 + bob} h={330} a={1} />
      <Big text="VS" y={730} size={150} t={9} col={ACC} x={470} />
      <Item lib={LI} name="sun_disc" x={740} y={830 - bob} h={290} a={1} />
      <Item lib={SC_} name="think" x={760} y={1150} h={250} a={1} />
    </>;
    case 'rounds': return <>
      <Big text="3 ROUNDS" y={290} size={190} t={t} at={0.1} col={ACC} />
      {[['thermometer', 'heat', 180], ['stopwatch', 'time', 470], ['sun_core_glow', 'core', 760]].map(([n, l, x], i) => <React.Fragment key={n as string}>
        <Item lib={LI} name={n as string} x={x as number} y={850} h={230} a={k(0.4 + i * 0.4)} />
        <Label text={`${i + 1} · ${l}`} y={1000} col={TEXT} a={k(0.5 + i * 0.4)} x={x as number} />
      </React.Fragment>)}
      <Item lib={SC_} name="talk" x={470} y={1250} h={240} a={k(0.3)} />
    </>;
    case 'heat': return <>
      <Title k={k(0.1)} text="Round 1 · Heat" y={300} />
      <Item lib={LI} name="storm_cloud" x={240} y={640} h={170} a={k(0.5)} />
      <Item lib={LI} name="lightning_bolt" x={220} y={940} h={320} a={k(0.9)} />
      <Item lib={LI} name="thermometer" x={700} y={860} h={300} a={k(2.8)} />
      <Big text="50,000°F" y={1130} size={120} t={t} at={3.6} col={ACC} x={460} />
      <Item lib={CG} name="surprised" x={800} y={1190} h={230} a={k(4.8)} />
    </>;
    case 'surf': return <>
      <Title k={k(0.1)} text="The Sun's surface" y={300} />
      <Item lib={LI} name="sun_disc" x={500} y={820} h={380} rot={T * 6} a={k(0.3)} />
      <Big text="10,000°F" y={1060} size={150} t={t} at={1.5} col={TEXT} x={500} />
      <Item lib={SC_} name="think" x={800} y={800} h={270} a={k(0.8)} />
    </>;
    case 'five': return <>
      <Big text="5 times hotter" y={280} size={170} t={t} at={0.3} col={ACC} />
      <Item lib={SC_} name="happy" x={130} y={1090} h={230} a={k(1.0)} />
      <Item lib={LI} name="lightning_bolt" x={340} y={1030} h={330} a={k(0.3)} />
      <Item lib={LI} name="sun_disc" x={740} y={1050} h={190} a={k(0.6)} />
      <Tick x={540} y={1030} a={clamp((t - 2.5) / 0.2)} r={56} />
      <Label text="Point · lightning" y={1235} col={INK} a={k(2.6)} x={485} />
    </>;
    case 'fulg': return <>
      <Title k={k(0.1)} text="Sand into glass" y={300} />
      <Item lib={LI} name="lightning_bolt" x={500} y={650} h={260} a={k(0.5)} />
      <Item lib={LI} name="fulgurite" x={500} y={1000} h={330} a={k(3.8)} />
      <Item lib={LI} name="beach_pail" x={790} y={1120} h={210} a={k(1.0)} />
      <Item lib={CG} name="surprised" x={190} y={1130} h={300} a={k(1.6)} />
      <Label text="fulgurite" y={1230} col={TEXT} a={k(4.3)} x={500} />
    </>;
    case 'flash': return <>
      <Title k={k(0.1)} text="Round 2 · Time" y={300} />
      <Item lib={LI} name="lightning_bolt" x={230} y={1010} h={300} a={clamp(Math.sin(T * 30) * 3 + 1.2)} />
      <Item lib={LI} name="stopwatch" x={520} y={940} h={340} a={k(0.3)} />
      <Big text="< 1 s" y={540} size={170} t={t} at={3.3} col={ACC} x={500} />
      <Item lib={SC_} name="think" x={800} y={1080} h={280} a={k(1.0)} />
    </>;
    case 'years': return <>
      <Title k={k(0.1)} text="Billions of years" y={300} />
      <Item lib={LI} name="sun_disc" x={500} y={800} h={320} rot={T * 6} a={k(0.3)} />
      <Item lib={LI} name="hourglass_space" x={200} y={1000} h={270} a={k(0.8)} />
      <Item lib={CG} name="talk" x={790} y={1120} h={260} a={k(1.2)} />
      <Tick x={800} y={700} a={clamp((t - 2.8) / 0.2)} r={50} />
      <Label text="Point · Sun" y={1230} col={TEXT} a={k(2.9)} x={470} />
    </>;
    case 'final': return <>
      <Big text="ROUND 3" y={330} size={230} t={t} at={0.2} col={ACC} />
      <Item lib={LI} name="sun_core_glow" x={480} y={900} h={380} a={k(0.5)} />
      <Item lib={SC_} name="point" x={780} y={1130} h={270} a={k(1.2)} />
      <Label text="deep inside" y={1180} col={TEXT} a={k(1.0)} x={260} />
    </>;
    case 'core': return <>
      <Title k={k(0.1)} text="The Sun's core" y={300} />
      <Item lib={LI} name="sun_core_glow" x={480} y={720} h={270} a={k(0.3)} />
      <Big text="27,000,000°F" y={880} size={105} t={t} at={2.2} col={ACC} x={540} />
      <Item lib={LI} name="thermometer" x={150} y={1090} h={300} a={k(0.8)} />
      <Item lib={SC_} name="surprised" x={780} y={1190} h={250} a={k(2.8)} />
    </>;
    case 'cant': return <>
      <Title k={k(0.1)} text="Out of reach" y={300} />
      <Item lib={LI} name="lightning_bolt" x={200} y={1020} h={290} a={k(0.3)} />
      <Item lib={LI} name="sun_core_glow" x={700} y={1020} h={250} a={k(0.5)} />
      <Cross x={450} y={1020} a={clamp((t - 0.8) / 0.2)} r={64} />
      <Label text="Point · Sun" y={1230} col={INK} a={k(1.5)} x={450} />
    </>;
    case 'score': return <>
      <Title k={k(0.1)} text="Final score" y={300} />
      <Item lib={LI} name="sun_disc" x={240} y={1040} h={230} a={k(0.2)} />
      <Item lib={LI} name="lightning_bolt" x={740} y={1030} h={280} a={k(0.2)} />
      <Big text="2" y={560} size={260} t={t} at={0.5} col={ACC} x={240} />
      <Big text="1" y={560} size={260} t={t} at={1.0} col={TEXT} x={740} />
      <Item lib={CG} name="happy" x={480} y={1230} h={260} a={k(1.2)} />
    </>;
    case 'beats': return <>
      <Title k={k(0.1)} text="Surface vs heart" y={300} />
      <Item lib={LI} name="sun_disc" x={270} y={960} h={230} a={k(0.2)} />
      <Item lib={LI} name="lightning_bolt" x={520} y={1000} h={300} a={k(0.2)} />
      <Item lib={LI} name="sun_core_glow" x={760} y={960} h={230} a={k(0.2)} />
      <Tick x={270} y={740} a={clamp((t - 0.9) / 0.2)} r={50} />
      <Cross x={760} y={740} a={clamp((t - 2.0) / 0.2)} r={50} />
      <Label text="surface" y={1130} col={INK} a={k(0.5)} x={270} />
      <Label text="core" y={1130} col={INK} a={k(1.6)} x={760} />
    </>;
    case 'nap': return <>
      <Title k={k(0.1)} text="Sunbeam nap" y={300} color={INK} />
      <Item lib={LI} name="sun_disc" x={640} y={760} h={280} rot={T * 6} a={k(0.3)} />
      <Big text="z z z" y={1000} size={110} t={t} at={1.2} col={TEXT} x={470} />
      <Item lib={CG} name="shrug" x={770} y={1070} h={240} a={k(0.8)} />
    </>;
    default: return <>
      <Big text="?" y={330} size={260} t={t} at={0.2} col={ACC} />
      <Item lib={LI} name="lightning_bolt" x={430} y={820} h={320} a={k(0.3)} />
      <Item lib={LI} name="sun_disc" x={740} y={800} h={280} a={k(0.5)} />
      <Item lib={SC_} name="shrug" x={720} y={1150} h={260} a={k(1.0)} />
    </>;
  }
};
