import React from 'react';
import words from '../public/words.json';
import {ACC_T, TEXT, clamp, eo, stroke} from './common';

const OFF = 0.3;
type Wd = {w: string; s: number; e: number};
const all: Wd[] = (words as [string, number, number][]).map(([w, s, e]) => ({w, s: s + OFF, e: e + OFF}));
const blocks: Wd[][] = [];
{ let cur: Wd[] = [];
  all.forEach((w, i) => { cur.push(w);
    const end = /[.?:!]$/.test(w.w) || (/[,]$/.test(w.w) && cur.length >= 3) || cur.length >= 6;
    const gap = i + 1 < all.length ? all[i + 1].s - w.e : 9;
    if (end || gap > 0.5) { blocks.push(cur); cur = []; } });
  if (cur.length) blocks.push(cur); }

export const Subs: React.FC<{T: number; narrow: boolean; y?: number}> = ({T, narrow, y}) => {
  const b = blocks.find((bl, i) => { const t0 = bl[0].s, t1 = (blocks[i + 1]?.[0].s ?? 99) - 0.02; return T >= t0 && T < Math.min(t1, bl[bl.length - 1].e + 0.35); });
  if (!b) return null;
  const outA = 1 - clamp((T - (b[b.length - 1].e + 0.12)) / 0.2);
  const size = narrow ? 58 : 70;
  return (
    <div style={{position: 'absolute', left: narrow ? 545 : 60, width: narrow ? 480 : 960, top: y ?? (narrow ? 1450 : 1390), display: 'flex', flexWrap: 'wrap', justifyContent: narrow ? 'flex-start' : 'center',
      columnGap: size * 0.28, rowGap: 2, fontFamily: 'Londrina', fontSize: size, lineHeight: 1.1, opacity: outA}}>
      {b.map((w, i) => {
        const a = clamp((T - w.s) / 0.08), hot = T >= w.s && T < w.e + 0.05;
        return <span key={i} style={{opacity: a, translate: `0 ${(1 - eo(a)) * 8}px`, color: hot ? ACC_T : TEXT, ...stroke(4)}}>{w.w}</span>;
      })}
    </div>
  );
};
