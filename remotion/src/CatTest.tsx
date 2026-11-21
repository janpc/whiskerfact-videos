import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Cat} from './Cat';
import {useFonts} from './common';
const N = ['smile', 'm', 'a', 'ah', 'oo', 'f', 'slight', 'e', 'ee', 'o'];
export const CatTest: React.FC = () => { useFonts(); return (
  <AbsoluteFill style={{background: '#ddd'}}>
    {N.map((n, i) => <div key={n} style={{position: 'absolute', left: (i % 5) * 216, top: Math.floor(i / 5) * 400}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: 216, height: 340, overflow: 'hidden'}}>
        <Cat T={0} x={-(188 + 420)} y={-600} k={1} mouthOverride={n} />
      </div>
      <div style={{position: 'absolute', top: 360, fontSize: 28}}>{n}</div>
    </div>)}
  </AbsoluteFill>); };
