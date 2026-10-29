"""Efectos de sonido sintetizados para Mr. Whiskerfact (sin librerías externas de audio).
Cada efecto es una función que devuelve un array mono float32 a 44,1 kHz.
"""
import math, os, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(1)

def t_(dur): return np.arange(int(SR * dur)) / SR
def env(n, attack=0.005, decay=0.2):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)
def lowpass(x, k=0.08):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y

def whoosh(dur=0.5):
    """subida: ruido filtrado que se abre y se cierra"""
    n = int(SR * dur); noise = rng.normal(0, 1, n).astype(np.float32)
    out = np.zeros(n, np.float32); acc = 0.0
    for i in range(n):
        p = i / n; k = 0.02 + 0.25 * math.sin(math.pi * p)
        acc += k * (noise[i] - acc); out[i] = acc
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5 * 0.9

def pop(f0=620, f1=260, dur=0.16):
    """rebote al aterrizar"""
    t = t_(dur); f = f1 + (f0 - f1) * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.05)

def click(f=3200, dur=0.03):
    t = t_(dur); return np.sin(2 * np.pi * f * t) * env(len(t), 0.0005, 0.006) * 0.6

def clink(dur=0.35):
    """gafas que suben: tintineo metálico corto"""
    t = t_(dur); s = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((2490, 1), (3720, 0.5), (5210, 0.25)))
    return s * env(len(t), 0.001, 0.06) * 0.35

def sparkle(dur=0.7):
    """guiño: dos notas brillantes con destello"""
    t = t_(dur); out = np.zeros(len(t))
    for start, f in ((0.0, 1318.5), (0.07, 1760.0), (0.14, 2637.0)):
        i = int(start * SR); tt = t[: len(t) - i]
        out[i:] += np.sin(2 * np.pi * f * tt) * env(len(tt), 0.002, 0.18) * 0.35
    shimmer = rng.normal(0, 1, len(t)) * env(len(t), 0.01, 0.12) * 0.04
    return out + shimmer

def tap(f=523.25, dur=0.22):
    """aparición de palabra: nota suave tipo marimba"""
    t = t_(dur); s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t)
    return s * env(len(t), 0.002, 0.07) * 0.45

def mix(events, total):
    out = np.zeros(int(SR * total), np.float32)
    for at, snd, gain in events:
        i = int(at * SR); snd = snd[: max(0, len(out) - i)]
        out[i:i + len(snd)] += snd * gain
    peak = np.max(np.abs(out)) or 1
    return out / peak * 0.8

def write_wav(path, x):
    x16 = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    st = np.stack([x16, x16], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

# guion de sonido del cierre "gafas" (mismos tiempos que outro4.frame_a)
OUTRO_GAFAS = lambda: [
    (0.00, whoosh(0.5), 0.6),
    (0.42, pop(), 0.9),
    (0.70, tap(523.25), 0.6), (1.00, tap(659.25), 0.6),
    (0.86, click(), 0.4),
    (1.60, clink(), 0.9),
    (3.25, sparkle(), 0.8),
    (2.60, tap(587.33), 0.6), (2.90, tap(783.99), 0.6),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    wav = os.path.join(here, "out", "outro_gafas_sfx.wav")
    write_wav(wav, mix(OUTRO_GAFAS(), 4.8))
    print(wav)
