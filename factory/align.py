"""Tiempos por palabra GRATIS: alineación forzada local del guion con el audio (pocketsphinx).
  python3 align.py voice/<slug>_brad.mp3 script.txt voice/<slug>_brad_words.json
Sustituye a la transcripción de ElevenLabs (ahorra ~400 créditos por vídeo).
Palabras fuera del diccionario: se añaden en EXTRA_PHONES o se deletrean con g2p sencillo."""
import json, re, subprocess, sys
import numpy as np

EXTRA_PHONES = {   # pronunciaciones de nombres propios que no están en cmudict
    "khufu": "K UW F UW", "menkaure": "M EH N K AW R EY", "giza": "G IY Z AH",
    "whiskerfact": "W IH S K ER F AE K T",
    "goosebumps": "G UW S B AH M P S", "arrector": "AH R EH K T ER", "pili": "P IH L AY",
    "fluffing": "F L AH F IH NG", "hairier": "HH EH R IY ER",
}
LETTER = {"a": "AE", "b": "B", "c": "K", "d": "D", "e": "EH", "f": "F", "g": "G", "h": "HH", "i": "IH", "j": "JH", "k": "K",
          "l": "L", "m": "M", "n": "N", "o": "AA", "p": "P", "q": "K", "r": "R", "s": "S", "t": "T", "u": "AH", "v": "V",
          "w": "W", "x": "K S", "y": "Y", "z": "Z"}

def norm(w):
    return re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))

def align(mp3, text):
    from pocketsphinx import Decoder
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    tokens = text.split()                                  # palabras tal cual (con puntuación) para los subtítulos
    keys = [norm(t) for t in tokens]
    dec = Decoder(samprate=16000, bestpath=False, loglevel="FATAL")
    for k in set(keys):
        if k and dec.lookup_word(k) is None:
            ph = EXTRA_PHONES.get(k) or " ".join(LETTER.get(c, "") for c in k if c in LETTER)
            dec.add_word(k, ph, True)
    dec.set_align_text(" ".join(k for k in keys if k))
    dec.start_utt(); dec.process_raw(pcm, full_utt=True); dec.end_utt()
    segs = [(s.word, s.start_frame / 100, (s.end_frame + 1) / 100) for s in dec.seg() if s.word not in ("<s>", "</s>", "<sil>", "(NULL)")]
    segs = [(re.sub(r"\(\d+\)$", "", w), a, b) for w, a, b in segs]
    out, j = [], 0
    for tok, k in zip(tokens, keys):
        while j < len(segs) and segs[j][0] != k: j += 1
        if j >= len(segs): raise SystemExit(f"alineación incompleta en '{tok}'")
        out.append([tok, round(segs[j][1], 3), round(segs[j][2], 3)]); j += 1
    return out

if __name__ == "__main__":
    mp3, txt, dst = sys.argv[1:4]
    words = align(mp3, open(txt).read())
    json.dump(words, open(dst, "w"))
    print(len(words), "palabras;", words[:3], "...", words[-2:])
