"""Da ritmo a la voz antes de alinear: acorta las pausas largas y acelera un poco sin cambiar el tono.
  python3 tighten.py voice/<slug>_brad.mp3
Guarda el original como voice/<slug>_brad_raw.mp3 y deja la versión ajustada en voice/<slug>_brad.mp3.
Reglas: las pausas se acortan en proporción (ver pause_target), ninguna supera MAX_PAUSE, y la voz sale a VOICE_TEMPO veces su velocidad.
Siempre se ejecuta ANTES de align.py, para que los tiempos de cada palabra correspondan al audio final."""
import os, shutil, subprocess, sys
import numpy as np
import brand as B

SR = 44100
THRESH_DB = -40          # por debajo de esto se considera silencio
MIN_GAP = 0.05           # s, huecos menores no cuentan como pausa

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def pause_target(gap):
    """acorta en proporción: las pausas cortas casi no se tocan y las largas (fin de frase) conservan aire.
    0,20 s -> 0,18 · 0,30 -> 0,24 · 0,45 -> 0,33 · 0,60 -> 0,42 · nunca más de 0,45"""
    return min(gap, 0.15 + 0.6 * (gap - 0.15), 0.45) if gap > 0.15 else gap

def shorten_pauses(x):
    win = int(0.01 * SR)
    n = len(x) // win
    rms = np.sqrt(np.mean(x[: n * win].reshape(n, win) ** 2, axis=1) + 1e-12)
    silent = 20 * np.log10(rms) < THRESH_DB
    out, i, fade = [], 0, int(0.01 * SR)
    k = 0
    while k < n:
        if silent[k]:
            j = k
            while j < n and silent[j]: j += 1
            gap = (j - k) * win / SR
            inside = k > 0 and j < n                    # no tocar el silencio inicial ni el final
            target = pause_target(gap)
            if inside and gap > target + 0.02:
                a, b = k * win, j * win
                half = int(target * SR / 2)
                out.append(x[i:a + half])
                tail = x[b - half:b].copy()
                tail[:fade] *= np.linspace(0, 1, fade)  # unión sin clic
                out[-1] = out[-1].copy(); out[-1][-fade:] *= np.linspace(1, 0, fade)
                out.append(tail)
                i = b
            k = j
        else:
            k += 1
    out.append(x[i:])
    return np.concatenate(out)

if __name__ == "__main__":
    mp3 = sys.argv[1]
    raw = mp3.replace(".mp3", "_raw.mp3")
    if not os.path.exists(raw): shutil.copy(mp3, raw)       # nunca se pierde el original
    x = load(raw)
    y = shorten_pauses(x)
    tmp = mp3 + ".wav.f32"
    y.astype(np.float32).tofile(tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
                    "-af", f"atempo={B.VOICE_TEMPO}", "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
    os.remove(tmp)
    d0, d1 = len(x) / SR, len(y) / SR / B.VOICE_TEMPO
    print(f"{d0:.1f} s -> {d1:.1f} s ({(1 - d1 / d0) * 100:.0f}% más corto)")
