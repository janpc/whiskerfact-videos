import React from 'react';
import {delayRender, continueRender, getInputProps} from 'remotion';
import {FLOOR} from './common';

// Comprobador de diseño (equivalente al QA de Python para texto/solapes/zona de botones).
// Solo actúa cuando se renderiza con inputProps {probe: true} (lo hace remotion/check.mjs); en el render normal no existe.
// Mide las cajas REALES en el navegador (fuente y sprites ya cargados), con el recorte visible de cada sprite (canal alfa).
export const probeOn = () => !!(getInputProps() as {probe?: boolean}).probe;

// mismas constantes que factory/brand.py
const RAIL_TOP = 900, SAFE_RIGHT_LOW = 900, SAFE_TOP = 220, SAFE_BOTTOM = 1540, EDGE = 24, W = 1080, GAP_WARN = 20;
const TOL = 15;           // px de tolerancia en la zona de botones (como qa.py)
const OVERLAP_PX = 200;   // px² de solape visible que ya cuenta como fallo

type Mask = {data: Uint8ClampedArray; w: number; h: number} | null;
type Box = {kind: string; name: string; x0: number; y0: number; x1: number; y1: number; mask: Mask; rect: DOMRect; solid: boolean; air?: boolean};
// personajes y objetos que tienen que apoyar en el suelo (si no están saltando)
const GROUNDED = /^(dog|scientist|young_man|child_boy|child_girl|pilgrim_man|wampanoag_man|ancient_person|ancient_youth|early_human|astronaut|cow|mouse|monkey|woolly_mammoth)\/|\/(man_dog_nose|dog_sniffing|human_crawl_trail|lamp_post)$/;
export type Issue = {sev: 'FAIL' | 'WARN'; rule: string; a: string; b?: string; box?: number[]; box2?: number[]};

const maskCache = new Map<string, Mask>();
const getMask = (img: HTMLImageElement): Mask => {
  const key = img.currentSrc || img.src;
  if (maskCache.has(key)) return maskCache.get(key)!;
  const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
  const g = c.getContext('2d', {willReadFrequently: true});
  let m: Mask = null;
  if (g && c.width && c.height) { g.drawImage(img, 0, 0); m = {data: g.getImageData(0, 0, c.width, c.height).data, w: c.width, h: c.height}; }
  maskCache.set(key, m); return m;
};
const alphaAt = (b: Box, x: number, y: number) => {
  if (x < b.x0 || x >= b.x1 || y < b.y0 || y >= b.y1) return false;
  if (b.solid || !b.mask) return true;
  const u = Math.floor(((x - b.rect.left) / b.rect.width) * b.mask.w), v = Math.floor(((y - b.rect.top) / b.rect.height) * b.mask.h);
  if (u < 0 || v < 0 || u >= b.mask.w || v >= b.mask.h) return false;
  return b.mask.data[(v * b.mask.w + u) * 4 + 3] > 40;
};
const tight = (img: HTMLImageElement, r: DOMRect): [number, number, number, number, Mask] => {
  const m = getMask(img); if (!m) return [r.left, r.top, r.right, r.bottom, null];
  let x0 = m.w, y0 = m.h, x1 = -1, y1 = -1;
  for (let y = 0; y < m.h; y += 2) for (let x = 0; x < m.w; x += 2) if (m.data[(y * m.w + x) * 4 + 3] > 40) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  if (x1 < 0) return [r.left, r.top, r.left, r.top, m];
  return [r.left + (x0 / m.w) * r.width, r.top + (y0 / m.h) * r.height, r.left + ((x1 + 1) / m.w) * r.width, r.top + ((y1 + 1) / m.h) * r.height, m];
};
const opacityOf = (el: Element) => { let o = 1; for (let e: Element | null = el; e && e !== document.body; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity || '1'); return o; };

const collect = (): Box[] => {
  const out: Box[] = [];
  document.querySelectorAll('[data-box]').forEach((el) => {
    const kind = el.getAttribute('data-box')!, name = el.getAttribute('data-name') ?? kind;
    if (kind !== 'cat' && opacityOf(el) < 0.6) return;                      // todavía no se ve (entrando o saliendo)
    const r = el.getBoundingClientRect();
    if (kind === 'sub') {                                                    // caja ajustada al texto real (unión de palabras visibles)
      const spans = [...el.querySelectorAll('span')].filter((s) => parseFloat(getComputedStyle(s).opacity) > 0.5).map((s) => s.getBoundingClientRect());
      if (!spans.length) return;
      out.push({kind, name, x0: Math.min(...spans.map((s) => s.left)), y0: Math.min(...spans.map((s) => s.top)), x1: Math.max(...spans.map((s) => s.right)), y1: Math.max(...spans.map((s) => s.bottom)), mask: null, rect: r, solid: true});
      return;
    }
    if (kind === 'item' && el instanceof HTMLImageElement) {
      // el sprite puede girar (sol): se mide su caja SIN girar (centro = left/top por el translate -50%), que es la silueta real de un disco
      const he = el as HTMLElement, w = he.offsetWidth, h = he.offsetHeight, cx = he.offsetLeft, cy = he.offsetTop;
      const top = el.getAttribute('data-anchor') === 'bottom' ? cy - h : cy - h / 2;
      const r0 = {left: cx - w / 2, top, width: w, height: h, right: cx + w / 2, bottom: top + h} as DOMRect;
      const [x0, y0, x1, y1, mask] = tight(el, r0);
      out.push({kind, name, x0, y0, x1, y1, mask, rect: r0, solid: false, air: el.getAttribute('data-air') === '1'});
      return;
    }
    out.push({kind, name, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom, mask: null, rect: r, solid: true});
  });
  return out;
};

const bx = (b: Box) => [Math.round(b.x0), Math.round(b.y0), Math.round(b.x1), Math.round(b.y1)];
const inter = (a: Box, b: Box) => ({x0: Math.max(a.x0, b.x0), y0: Math.max(a.y0, b.y0), x1: Math.min(a.x1, b.x1), y1: Math.min(a.y1, b.y1)});
const overlapPx = (a: Box, b: Box) => {
  const i = inter(a, b); if (i.x1 <= i.x0 || i.y1 <= i.y0) return 0;
  let n = 0; const st = 4;
  for (let y = i.y0; y < i.y1; y += st) for (let x = i.x0; x < i.x1; x += st) if (alphaAt(a, x, y) && alphaAt(b, x, y)) n++;
  return n * st * st;
};
const gapOf = (a: Box, b: Box) => Math.hypot(Math.max(0, a.x0 - b.x1, b.x0 - a.x1), Math.max(0, a.y0 - b.y1, b.y0 - a.y1));

export const analyse = (boxes: Box[]): Issue[] => {
  const iss: Issue[] = []; const vis = boxes.filter((b) => b.kind !== 'cat');
  for (const b of vis) {
    {
      const w = Math.min(b.x1, W + 999) - Math.max(b.x0, SAFE_RIGHT_LOW), h = b.y1 - Math.max(b.y0, RAIL_TOP);
      if (w > TOL && h > TOL) iss.push({sev: 'FAIL', rule: 'botones', a: b.name, box: bx(b)});            // tapado por los botones de la app
    }
    if (b.kind === 'item' && !b.air && GROUNDED.test(b.name) && Math.abs(b.y1 - FLOOR) > 20)
      iss.push({sev: 'FAIL', rule: 'flota', a: b.name, box: bx(b)});                                       // sin apoyar en el suelo
    if (b.kind !== 'sub') {
      if (b.y0 < SAFE_TOP) iss.push({sev: 'FAIL', rule: 'arriba', a: b.name, box: bx(b)});               // bajo la interfaz superior
      if (b.y1 > SAFE_BOTTOM) iss.push({sev: 'FAIL', rule: 'abajo', a: b.name, box: bx(b)});              // bajo la descripción de la app
    }
    if (b.x0 < 0 || b.x1 > W) iss.push({sev: 'FAIL', rule: 'cortado', a: b.name, box: bx(b)});
    else if (b.x0 < EDGE || b.x1 > W - EDGE) iss.push({sev: 'WARN', rule: 'borde', a: b.name, box: bx(b)});
  }
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.kind === 'sub' && b.kind === 'sub') continue;
    if (a.kind === 'cat' && b.kind === 'cat') continue;
    const px = overlapPx(a, b);
    if (px > OVERLAP_PX) iss.push({sev: 'FAIL', rule: ['item', 'cat', 'mark'].includes(a.kind) && ['item', 'cat', 'mark'].includes(b.kind) ? 'solape' : 'solape_texto', a: a.name, b: b.name, box: bx(a), box2: bx(b)});
    else if (px === 0 && a.kind !== 'cat' && b.kind !== 'cat' && gapOf(a, b) < GAP_WARN && (a.kind === 'item' || b.kind === 'item'))
      iss.push({sev: 'WARN', rule: 'pegados', a: a.name, b: b.name, box: bx(a), box2: bx(b)});
  }
  return iss;
};

export const Probe: React.FC<{id: string}> = ({id}) => {
  const [iss, setIss] = React.useState<Issue[] | null>(null);
  const overlay = !!(getInputProps() as {overlay?: boolean}).overlay;
  React.useEffect(() => {
    const h = delayRender('probe');
    (async () => {
      await document.fonts.ready;
      for (let i = 0; i < 60 && !document.fonts.check('50px Londrina'); i++) await new Promise((r) => setTimeout(r, 50));
      await Promise.all([...document.images].map((im) => im.decode().catch(() => undefined)));
      await new Promise((r) => setTimeout(r, 120));
      const res = analyse(collect());
      console.log('PROBE ' + JSON.stringify({id, issues: res}));
      setIss(res);
      setTimeout(() => continueRender(h), 60);
    })();
  }, [id]);
  if (!overlay || !iss) return null;
  return (
    <div style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: SAFE_RIGHT_LOW, top: RAIL_TOP, width: W - SAFE_RIGHT_LOW, height: 800, border: '4px dashed rgb(255,200,0)', background: 'rgba(255,200,0,0.18)'}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: SAFE_TOP, background: 'rgba(255,200,0,0.12)'}} />
      {iss.flatMap((s, k) => [s.box, s.box2].filter(Boolean).map((b, m) => {
        const [x0, y0, x1, y1] = b as number[];
        return <div key={`${k}-${m}`} style={{position: 'absolute', left: x0, top: y0, width: x1 - x0, height: y1 - y0, border: `5px solid ${s.sev === 'FAIL' ? 'rgb(255,30,30)' : 'rgb(255,140,0)'}`, boxSizing: 'border-box'}} />;
      }))}
    </div>
  );
};
