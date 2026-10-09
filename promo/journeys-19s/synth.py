# Music + SFX for stash · journeys (19 s). 120 BPM, D major, calm and clean.
# Usage: python3 synth.py <spot.json> <out.wav>
# Scene cuts (3, 7.5, 12, 16.5 s) fall on beats. Ticks follow the on-screen
# beats in compose.html: issues landing, terminal lines, flow nodes, the close.
import json
import sys
import wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SPOT = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
SR = 44100
DUR = float(SPOT['duration'])
N = int(SR * DUR)
rng = np.random.default_rng(11)
BEAT = 0.5


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)


def place(buf, sig, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    s = sig[: len(buf) - i]
    buf[i:i + len(s)] += s * g


def tone(f, dur, decay, harm=3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * t) * 0.5 ** (k - 1) for k in range(1, harm + 1))
    return s * np.exp(-t * decay) * np.minimum(1, t / 0.004)


def pad(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for d in (-0.003, 0.003):
            s += np.sin(2 * np.pi * hz(m) * (1 + d) * t) + 0.3 * np.sin(4 * np.pi * hz(m) * (1 + d) * t)
    env = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return lp(s * env, 1800)


def kick():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (48 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 14)


def hat():
    n = int(0.06 * SR)
    return hp(rng.standard_normal(n), 7000) * np.exp(-np.arange(n) / SR * 70)


music = np.zeros(N)
# D  Bm  G  A, one chord per 2 s bar
CHORDS = [[62, 66, 69], [59, 62, 66], [55, 59, 62, 67], [57, 61, 64]]
ROOTS = [38, 35, 31, 33]
for bar in range(int(DUR // 2) + 1):
    t0 = bar * 2.0
    c = CHORDS[bar % 4]
    place(music, pad(c, 2.2), t0, 0.05)
    place(music, tone(hz(ROOTS[bar % 4]), 1.9, 2.0, 2), t0, 0.22)
    for i, m in enumerate([c[0] + 12, c[1] + 12, c[2] + 12, c[1] + 12]):
        place(music, tone(hz(m), 0.4, 9), t0 + i * 0.5 + 0.25, 0.05)

drums = np.zeros(N)
end_drums = 16.5  # outro drops to pad and chime
for b in np.arange(0, end_drums, BEAT):
    if b >= 1.0:
        place(drums, kick(), b, 0.35 if (b / BEAT) % 2 == 0 else 0.18)
    place(drums, hat(), b + 0.25, 0.05)

sfx = np.zeros(N)
blip = lambda m, g: (tone(hz(m), 0.18, 28, 2), g)
# review: 4 issues land, then the count
for i in range(4):
    s, g = blip(81 + [0, 2, 4, 7][i], 0.08)
    place(sfx, s, 3 + 0.5 + i * 0.45, g)
place(sfx, tone(hz(86), 0.4, 10), 3 + 2.5, 0.08)
# nightly: soft key ticks per terminal line
for i in range(9):
    place(sfx, hp(rng.standard_normal(int(0.03 * SR)), 3000) * np.exp(-np.arange(int(0.03 * SR)) / SR * 120), 7.5 + 0.3 + i * 0.25, 0.05)
# lifecycle: nodes, then three green chimes and the close
for i in range(5):
    place(sfx, tone(hz(74 + [0, 2, 4, 7, 9][i]), 0.25, 18), 12 + 0.3 + i * 0.45, 0.06)
for i in range(3):
    place(sfx, tone(hz(86 + [0, 4, 7][i]), 0.5, 7), 12 + 2.25 + i * 0.25, 0.07)
# outro chime
for m in (74, 78, 81, 86):
    place(sfx, tone(hz(m), 2.0, 1.6), 16.5, 0.06)

mix = music + drums + sfx
# Small room so the effects sit in the same space as the music
ir = rng.standard_normal(int(0.6 * SR)) * np.exp(-np.arange(int(0.6 * SR)) / SR * 7)
wet = fftconvolve(mix, lp(ir, 5000))[:N]
mix = mix + 0.12 * wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(mix))
fade = np.ones(N)
fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
mix = hp(mix * fade, 30)
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.8
st = np.stack([mix, mix], axis=1)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
