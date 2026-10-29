"""Música de fondo de Mr. Whiskerfact, generada por código (propia, sin licencias).
Una base lo-fi suave: acordes de pad, arpegio pulsado, bajo y un shaker muy discreto.
Cada categoría cambia de tonalidad para que los vídeos no suenen todos iguales.
"""
import math
import numpy as np

SR = 44100
BPM = 88
BEAT = 60 / BPM
KEYS = {"science": 0, "nature": 2, "history": -3, "body": 5, "space": -5, "tech": 4}   # semitonos sobre Do
PROG = [[0, 4, 7, 11], [9, 12, 16, 19], [5, 9, 12, 16], [7, 11, 14, 17]]           # Cmaj7 - Am7 - Fmaj7 - G6

def hz(semi, octave=4): return 261.63 * 2 ** ((semi + 12 * (octave - 4)) / 12)

def _env(n, a, d):
    t = np.arange(n) / SR
    return np.clip(t / a, 0, 1) * np.exp(-t / d)

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2.003 * f * t) for f in freqs) / len(freqs)
    env = np.clip(t / 0.6, 0, 1) * np.clip((dur - t) / 0.8, 0, 1)
    return x * env * (0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * t))

def pluck(f, dur=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 18)) * _env(n, 0.003, 0.22)

def bass(f, dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * _env(n, 0.01, 0.35)

def shaker(dur=0.08, rng=np.random.default_rng(3)):
    n = int(dur * SR); x = np.diff(rng.normal(0, 1, n + 1))
    return x * _env(n, 0.002, 0.02)

def bed(seconds, category="science", end_on_tonic=True):
    """base musical de `seconds` segundos; termina en el acorde de tónica"""
    key = KEYS.get(category, 0)
    bar = 4 * BEAT
    n = int(seconds * SR) + SR
    out = np.zeros(n)
    def add(at, sig, g):
        i = int(at * SR); sig = sig[: max(0, n - i)]; out[i:i + len(sig)] += sig * g
    nb = int(math.ceil(seconds / bar))
    for b in range(nb):
        t0 = b * bar
        chord = PROG[b % 4] if not (end_on_tonic and b == nb - 1) else PROG[0]
        add(t0, pad([hz(key + c, 3) for c in chord], bar + 0.6), 0.22)
        add(t0, bass(hz(key + chord[0], 2)), 0.30); add(t0 + 2 * BEAT, bass(hz(key + chord[0], 2)), 0.22)
        arp = [chord[0], chord[1], chord[2], chord[3], chord[2], chord[1], chord[2], chord[3]]
        for k, c in enumerate(arp):
            add(t0 + k * BEAT / 2, pluck(hz(key + c, 5)), 0.10 if k % 2 == 0 else 0.07)
        for k in range(4):
            add(t0 + k * BEAT + BEAT / 2, shaker(), 0.05)
    out = out[: int(seconds * SR)]
    t = np.arange(len(out)) / SR
    out *= np.clip(t / 0.8, 0, 1) * np.clip((seconds - t) / 1.5, 0, 1)    # entra y sale en fundido
    return (out / (np.max(np.abs(out)) or 1)).astype(np.float32)

def duck(music, voice_env, depth_db=-8.0):
    """baja la música donde hay voz (voice_env: 0..1 por muestra)"""
    g = 10 ** (depth_db / 20)
    return music * (1 - (1 - g) * voice_env)


# ---------- estilo documental ----------
DOC_BPM = 68
DOC_PROG = [[9, 12, 16], [5, 9, 12], [0, 4, 7], [7, 11, 14]]     # Am - F - C - G: asombro, tono de documental

def _lowpass(x, cutoff):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, cutoff, fs=SR, output="sos"), x)

def strings(freqs, dur, swell=1.0):
    """cuerdas: dientes de sierra ligeramente desafinados, filtrados y con ataque lento"""
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            for h in range(1, 7):
                x += np.sin(2 * np.pi * ff * h * t + h * 0.7) / h
    x = _lowpass(x / (len(freqs) * 3), 1800)
    env = np.clip(t / 1.4, 0, 1) * np.clip((dur - t) / 1.2, 0, 1)
    vib = 1 + 0.04 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.8) / 1, 0, 1)
    return x * env * vib * swell

def piano(f, dur=2.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (1.6 + 1.4 * h)) for h, a in ((1, 1), (2, 0.45), (3, 0.2), (4, 0.08)))
    return x * np.clip(t / 0.004, 0, 1)

def soft_pulse(f, dur=0.4):
    n = int(dur * SR); t = np.arange(n) / SR
    return _lowpass(np.sin(2 * np.pi * f * t) + 0.5 * np.sign(np.sin(2 * np.pi * f * t)) * 0.3, 900) * _env(n, 0.01, 0.12)

def reverb(x, secs=2.2, mix=0.35):
    from scipy.signal import fftconvolve
    n = int(secs * SR); t = np.arange(n) / SR
    ir = np.random.default_rng(9).normal(0, 1, n) * np.exp(-t * 3.2)
    ir = _lowpass(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(x, ir)[: len(x)]
    return (1 - mix) * x + mix * wet * 0.6

def doc_bed(seconds, category="science", swell_at=None):
    """base de documental: cuerdas, piano disperso, pulso suave que crece y un grave sostenido"""
    key = KEYS.get(category, 0)
    beat = 60 / DOC_BPM; bar = 4 * beat
    n = int(seconds * SR) + 3 * SR
    out = np.zeros(n)
    def add(at, sig, g):
        i = int(at * SR); sig = sig[: max(0, n - i)]; out[i:i + len(sig)] += sig * g
    nb = int(math.ceil(seconds / bar))
    swell_at = swell_at or seconds * 0.75
    mel = [4, 2, 0, 2, 4, 7, 4, 2]   # grados de la melodía de piano (sobre la escala del acorde)
    for b in range(nb):
        t0 = b * bar
        last = b == nb - 1
        chord = [0, 4, 7] if last else DOC_PROG[b % 4]
        grow = 0.6 + 0.4 * min(1, t0 / swell_at)           # va creciendo hasta el dato final
        add(t0, strings([hz(key + c, 3) for c in chord], bar + 1.4, grow), 0.20)
        add(t0, strings([hz(key + chord[0], 2)], bar + 1.4), 0.16)                 # grave sostenido
        # piano: una nota cada dos tiempos, pocas y espaciadas
        for k in (0, 2):
            c = chord[(b + k) % 3] + (12 if (b + k) % 2 else 0)
            add(t0 + k * beat, piano(hz(key + c, 4)), 0.14)
        # pulso de corcheas muy suave, solo cuando el vídeo ya ha arrancado
        if t0 >= bar and not last:
            for k in range(8):
                add(t0 + k * beat / 2, soft_pulse(hz(key + chord[0], 3)), 0.05 * grow)
    out = reverb(out)[: int(seconds * SR)]
    t = np.arange(len(out)) / SR
    out *= np.clip(t / 1.2, 0, 1) * np.clip((seconds - t) / 2.0, 0, 1)
    return (out / (np.max(np.abs(out)) or 1)).astype(np.float32)


# ---------- documental animado ----------
UP_BPM = 100
UP_PROG = [[5, 9, 12], [0, 4, 7], [7, 11, 14], [9, 12, 16]]      # F - C - G - Am: optimista, de descubrimiento

def spiccato(f, dur=0.16):
    """cuerda corta y picada para el ostinato"""
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * h * t + h) / h for h in range(1, 6))
    return _lowpass(x, 2600) * _env(n, 0.004, 0.05)

def kick(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.12)

def tick(dur=0.05, rng=np.random.default_rng(4)):
    n = int(dur * SR); x = np.diff(rng.normal(0, 1, n + 1))
    return _lowpass(x, 7000) * _env(n, 0.001, 0.012)

def upbeat_doc_bed(seconds, category="science", swell_at=None):
    """documental con ritmo: ostinato de cuerdas picadas, piano en motivo, bombo suave y cuerdas largas"""
    key = KEYS.get(category, 0)
    beat = 60 / UP_BPM; bar = 4 * beat
    n = int(seconds * SR) + 3 * SR
    out = np.zeros(n)
    def add(at, sig, g):
        i = int(at * SR); sig = sig[: max(0, n - i)]; out[i:i + len(sig)] += sig * g
    nb = int(math.ceil(seconds / bar))
    swell_at = swell_at or seconds * 0.75
    motif = [2, 1, 0, 1, 2, 2, 1, 0]                 # índices de nota del acorde para el piano
    for b in range(nb):
        t0 = b * bar
        last = b == nb - 1
        chord = [0, 4, 7] if last else UP_PROG[b % 4]
        grow = 0.65 + 0.35 * min(1, t0 / swell_at)
        add(t0, strings([hz(key + c, 3) for c in chord], bar + 1.0, grow), 0.13)
        add(t0, strings([hz(key + chord[0], 2)], bar + 1.0), 0.10)
        if last:
            add(t0, piano(hz(key + 12, 4), 3.0), 0.16)
            continue
        # ostinato de semicorcheas: raíz y quinta, acento en cada tiempo
        for k in range(16):
            c = chord[0] if k % 4 in (0, 3) else chord[2]
            add(t0 + k * beat / 4, spiccato(hz(key + c, 4)), (0.11 if k % 4 == 0 else 0.07) * grow)
        # piano en corcheas con el motivo, a partir del segundo compás
        if b >= 1:
            for k, m in enumerate(motif):
                add(t0 + k * beat / 2, piano(hz(key + chord[m] + 12, 4), 1.2), 0.07)
        # pulso: bombo en 1 y 3, tick en contratiempos (entra tras dos compases)
        if b >= 2:
            add(t0, kick(), 0.30 * grow); add(t0 + 2 * beat, kick(), 0.24 * grow)
            for k in range(4): add(t0 + k * beat + beat / 2, tick(), 0.05)
    out = reverb(out, secs=1.6, mix=0.25)[: int(seconds * SR)]
    t = np.arange(len(out)) / SR
    out *= np.clip(t / 0.6, 0, 1) * np.clip((seconds - t) / 1.8, 0, 1)
    return (out / (np.max(np.abs(out)) or 1)).astype(np.float32)
