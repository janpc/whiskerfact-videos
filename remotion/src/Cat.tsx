import React from 'react';
import {Img, staticFile} from 'remotion';
import {FPS, clamp} from './common';
import mouthTL from '../public/mouth.json';
import dyJ from '../public/cat/mouth_dy.json';

const dy = {...(dyJ as Record<string, number>), round: 14};
// nombre de fonema -> [imagen, sx, sy]
const MAP: Record<string, [string, number, number]> = {
  smile: ['closed', 1, 1], m: ['closed', 1, 1], a: ['mid', 1, 1], ah: ['wide', 1, 0.72], oo: ['round', 0.85, 0.85], f: ['teeth', 1, 1],
  slight: ['mid', 1, 0.45], e: ['mid', 1.15, 0.85], ee: ['teeth', 1.2, 0.75], o: ['round', 1.25, 1.25],
};
const BLINKS = Array.from({length: 17}).map((_, i) => 1.1 + i * 3.3);
const OUT = 'drop-shadow(9px 0 0 rgb(58,36,30)) drop-shadow(-9px 0 0 rgb(58,36,30)) drop-shadow(0 9px 0 rgb(58,36,30)) drop-shadow(0 -9px 0 rgb(58,36,30))';

export const Cat: React.FC<{T: number; x: number; y: number; k?: number; pose?: string; curious?: boolean; mouthOverride?: string; o?: number}> =
  ({T, x, y, k = 0.36, pose = 'stand_front', curious = false, mouthOverride, o = 1}) => {
    const fi = Math.min(Math.floor(T * FPS), (mouthTL as string[]).length - 1);
    const ph = mouthOverride ?? (mouthTL as string[])[fi] ?? 'smile';
    const [img, sx, sy] = MAP[ph] ?? MAP.smile;
    const blink = BLINKS.some((b) => T - b >= 0 && T - b < 0.1);
    const eyes = blink ? 'closed' : curious ? 'curious' : null;
    const br = 1 + 0.006 * Math.sin((2 * Math.PI * T) / 3.2);
    // lienzo 1400x1900; cabeza 1024x1024 en (188,0); boca alineada en y=687
    const d = dy[img] ?? 0;
    const head = (
      <div style={{position: 'absolute', left: 188, top: 0, width: 1024, height: 1024}}>
        <div style={{position: 'absolute', inset: 0, WebkitMaskImage: 'linear-gradient(to bottom, #000 0, #000 790px, transparent 835px)'}}>
          <Img src={staticFile('cat/base.png')} style={{position: 'absolute', inset: 0, width: 1024, height: 1024}} />
        </div>
        {eyes && <Img src={staticFile(`cat/eyes_${eyes}.png`)} style={{position: 'absolute', inset: 0, width: 1024, height: 1024}} />}
        <div style={{position: 'absolute', inset: 0, translate: `0 ${d}px`}}>
          <Img src={staticFile(`cat/mouth_${img}.png`)} style={{position: 'absolute', inset: 0, width: 1024, height: 1024, scale: `${sx} ${sy}`, transformOrigin: `528px ${687 - d}px`}} />
        </div>
      </div>
    );
    return (
      <div style={{position: 'absolute', left: x, top: y, width: 1400, height: 1900, scale: `${k * br}`, transformOrigin: '0 0', filter: OUT, opacity: o}}>
        <Img src={staticFile(`cat/body_${pose}.png`)} style={{position: 'absolute', left: 0, top: 0, width: 1400, height: 1900}} />
        {head}
      </div>
    );
  };
