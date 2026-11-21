import React from 'react';
import {Composition} from 'remotion';
import {Reel} from './Reel';
import {CatTest} from './CatTest';
import meta from '../public/meta.json';
export const Root: React.FC = () => <>
  <Composition id="Reel" component={Reel} durationInFrames={meta.frames} fps={30} width={1080} height={1920} />
  <Composition id="CatTest" component={CatTest} durationInFrames={1} fps={30} width={1080} height={800} />
</>;
