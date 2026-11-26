import React from 'react';
import {Img, staticFile} from 'remotion';
import {FPS, clamp} from './common';
import mouthTL from '../public/mouth.json';
// fonemas de mouth.json; cada imagen cat/mouth_<fonema>.png viene ya ajustada de export_raw.py (no escalar ni mover aquí)
const PHONES = new Set(['smile', 'm', 'a', 'ah', 'oo', 'f', 'slight', 'e', 'ee', 'o']);
const BLINKS = Array.from({length: 17}).map((_, i) => 1.1 + i * 3.3);
const OUT = 'drop-shadow(9px 0 0 rgb(58,36,30)) drop-shadow(-9px 0 0 rgb(58,36,30)) drop-shadow(0 9px 0 rgb(58,36,30)) drop-shadow(0 -9px 0 rgb(58,36,30))';

export const Cat: React.FC<{T: number; x: number; y: number; k?: number; pose?: string; curious?: boolean; mouthOverride?: string; o?: number}> =
  ({T, x, y, k = 0.36, pose = 'stand_front', curious = false, mouthOverride, o = 1}) => {
    const fi = Math.min(Math.floor(T * FPS), (mouthTL as string[]).length - 1);
    const ph = mouthOverride ?? (mouthTL as string[])[fi] ?? 'smile';
    const img = PHONES.has(ph) ? ph : 'smile';
    const blink = BLINKS.some((b) => T - b >= 0 && T - b < 0.1);
    const eyes = blink ? 'closed' : curious ? 'curious' : null;
    const br = 1 + 0.006 * Math.sin((2 * Math.PI * T) / 3.2);
    // lienzo 1400x1900; cabeza 1024x1024 en (188,0)
    const head = (
      <div style={{position: 'absolute', left: 188, top: 0, width: 1024, height: 1024}}>
        {/* la máscara del cuello es obligatoria: sin ella la base tapa la ropa del cuerpo */}
        <div style={{position: 'absolute', inset: 0, WebkitMaskImage: 'linear-gradient(to bottom, #000 0, #000 790px, transparent 835px)'}}>
          <Img src={staticFile('cat/base.png')} style={{position: 'absolute', inset: 0, width: 1024, height: 1024}} />
        </div>
        {eyes && <Img src={staticFile(`cat/eyes_${eyes}.png`)} style={{position: 'absolute', inset: 0, width: 1024, height: 1024}} />}
        <div style={{position: 'absolute', inset: 0}}>
          <Img src={staticFile(`cat/mouth_${img}.png`)} style={{position: 'absolute', inset: 0, width: 1024, height: 1024}} />
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
