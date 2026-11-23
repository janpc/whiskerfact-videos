import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import words from '../public/words.json';
import {FPS, clamp, useFonts, Grain} from './common';
import {Cat} from './Cat';
import {Subs} from './Subs';
import {Probe, probeOn} from './Probe';
import {SC, CATS, Bg, Content, SFX, SWAP_AT, CURIOUS, DUR} from './scenes/current';

const sceneOf = (T: number) => SC.find(([, a, b]) => T >= a && T < b) ?? SC[SC.length - 1];

export const Reel: React.FC = () => {
  useFonts();
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  // el ÚLTIMO fotograma es exactamente el primero (bucle): se dibuja con T=0, sin ninguna animación en curso
  const isLastFrame = frame >= durationInFrames - 1;
  const T = isLastFrame ? 0 : frame / FPS;
  const [id, s0] = sceneOf(T);
  const t = T - s0;
  const last = id === SC[SC.length - 1][0];
  const hasCat = CATS.has(id);
  const wList = words as [string, number, number][];
  const speaking = (tt: number) => wList.some(([, a, b]) => tt >= a + 0.18 && tt <= b + 0.5);
  const vol = (f: number) => (speaking(f / FPS) ? 0.1 : 0.22) * clamp((DUR - f / FPS) / 1.2);
  // la última escena (cierre en bucle) acaba como empieza la primera: contenido fuera, gato en la pose inicial
  const fadeEnd = last ? 1 - clamp((T - (DUR - 0.35)) / 0.3) : 1;
  const swap = id === SC[0][0] ? clamp((T - SWAP_AT) / 0.2) : last ? fadeEnd : 1;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Bg id={id} T={last ? T - DUR : T} />
      <div style={{position: 'absolute', inset: 0, opacity: fadeEnd}}><Content id={id} t={t} T={T} /></div>
      {last && <div style={{position: 'absolute', inset: 0, opacity: 1 - fadeEnd}}><Content id={SC[0][0]} t={0} T={0} /></div>}
      {hasCat && <>
        <div data-box="cat" data-name="cat" style={{position: 'absolute', left: 40, top: 1236, width: 420, height: 684, visibility: 'hidden'}} />
        <Cat T={T} x={-20} y={1236} pose="stand_front" o={1 - swap} curious={CURIOUS.has(id) || (last && T > DUR - 0.35)} />
        <Cat T={T} x={-20} y={1236} pose="explain" o={swap} curious={CURIOUS.has(id) || (last && T > DUR - 0.35)} />
      </>}
      <Subs T={T} narrow={hasCat} />
      <Grain frame={isLastFrame ? 0 : frame} />
      {probeOn() && <Probe id={id} />}
      <Sequence from={9}><Audio src={staticFile('voice.mp3')} volume={1} /></Sequence>
      <Audio src={staticFile('music.mp3')} volume={vol} />
      {SFX.map(([tt, n, v], i) => <Sequence key={i} from={Math.round(tt * FPS)} durationInFrames={30}><Audio src={staticFile(`sfx/${n}.wav`)} volume={v} /></Sequence>)}
    </AbsoluteFill>
  );
};
