"""Second-generation SFX for Reels: deeper impacts, reverb, risers, glitches.
All sounds are synthesized in code (no samples, no licensing)."""
import numpy as np
SR = 48000
rng = np.random.default_rng(11)

def t_(d): return np.arange(int(d * SR)) / SR
def norm(x, p=1.0):
    m = np.max(np.abs(x)) or 1.0
    return x / m * p
def fade(x, a=0.002, b=0.02):
    x = x.copy(); n1, n2 = int(a * SR), int(b * SR)
    if n1: x[:n1] *= np.linspace(0, 1, n1)
    if n2: x[-n2:] *= np.linspace(1, 0, n2)
    return x
def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))
def reverb(x, decay=1.2, mix=0.25, bright=6000):
    n = int(decay * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 5.5 / decay)
    ir = fft_filter(ir, lo=150, hi=bright); ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + n; y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)
    out = np.zeros(L); out[:len(x)] += x
    return out * (1 - mix) + norm(y, np.max(np.abs(x))) * mix
def sweep(f0, f1, d):
    t = t_(d); f = f0 * (f1 / f0) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

def sub_boom(d=1.6):
    t = t_(d); f = 34 + 70 * np.exp(-t / 0.09)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.55)
    y = np.tanh(y * 2.2)
    click = fft_filter(rng.standard_normal(len(t)), lo=1500) * np.exp(-t / 0.006) * 0.5
    return fade(norm(y + click), 0.001, 0.2)
def impact(d=2.2):
    t = t_(d); boom = sub_boom(d)
    crack = fft_filter(rng.standard_normal(len(t)), lo=800, hi=9000) * np.exp(-t / 0.05)
    y = norm(boom * 1.0 + crack * 0.6)
    return norm(reverb(y, 1.8, 0.3))[:int(d * SR)]
def swell(d=1.8):
    """reverse cymbal / riser into a hit"""
    t = t_(d); n = rng.standard_normal(len(t))
    env = (t / d) ** 3
    y = fft_filter(n, lo=2500) * env + 0.25 * sweep(200, 1400, d) * env
    return fade(norm(y), 0.05, 0.004)
def whoosh_deep(d=0.7):
    t = t_(d); n = rng.standard_normal(len(t)); env = np.sin(np.pi * t / d) ** 2
    y = fft_filter(n, lo=120, hi=2500) * env + 0.4 * sweep(90, 45, d) * env
    return fade(norm(y), 0.01, 0.05)
def glitch(d=0.35):
    t = t_(d); y = np.zeros(len(t)); seg = int(0.03 * SR)
    for i in range(0, len(t), seg):
        f = rng.choice([220, 440, 880, 1760, 3520]) * (1 + rng.random() * 0.1)
        s = np.sign(np.sin(2 * np.pi * f * t[i:i + seg]))
        y[i:i + seg] = s * (rng.random() > 0.25)
    y = np.round(y * 4) / 4
    return fade(norm(fft_filter(y, hi=7000)) * 0.8)
def shutter():
    d = 0.18; t = t_(d)
    a = fft_filter(rng.standard_normal(len(t)), lo=2000) * np.exp(-t / 0.008)
    b = np.zeros(len(t)); o = int(0.07 * SR); b[o:] = a[:len(t) - o] * 0.7
    return fade(norm(a + b))
def heartbeat():
    d = 0.9; t = t_(d); y = np.zeros(len(t))
    for off, amp in ((0.0, 1.0), (0.22, 0.7)):
        o = int(off * SR); tt = t[:len(t) - o]
        y[o:] += amp * np.sin(2 * np.pi * (48 + 30 * np.exp(-tt / 0.03)) * tt) * np.exp(-tt / 0.09)
    return fade(norm(np.tanh(y * 2)))
def tick_hi():
    d = 0.04; t = t_(d); return fade(norm(np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.006)))
def cash_pro():
    d = 1.2; t = t_(d); out = np.zeros(len(t))
    for i in range(5):
        o = int(i * 0.05 * SR); f = 2100 + i * 380
        c = sum(a * np.sin(2 * np.pi * f * m * t) for m, a in ((1, 1), (1.5, .6), (2.0, .35))) * np.exp(-t / 0.12)
        out[o:] += c[:len(t) - o] * (1 - i * 0.12)
    bell = sum(a * np.sin(2 * np.pi * 2093 * m * t) for m, a in ((1, 1), (2.01, .5), (3.0, .25))) * np.exp(-t / 0.35)
    return fade(norm(reverb(norm(out + bell), 0.8, 0.2))[:len(t)], 0.001, 0.08)
def pop_pro(pitch=1.0):
    d = 0.2; t = t_(d); y = sweep(1100 * pitch, 240 * pitch, d) * np.exp(-t / 0.05)
    y += 0.3 * fft_filter(rng.standard_normal(len(t)), lo=2500) * np.exp(-t / 0.005)
    return fade(norm(y))
def ding_pro(f=1318.5):
    d = 1.4; t = t_(d)
    y = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (0.5 / (1 + k))) for k, (m, a) in enumerate(((1, 1), (2.0, .4), (3.01, .2), (4.2, .1))))
    return fade(norm(reverb(norm(y), 1.0, 0.2))[:len(t)], 0.001, 0.1)
def confetti():
    d = 1.4; t = t_(d); out = np.zeros(len(t))
    for i in range(40):
        o = int(rng.random() * 0.9 * SR); dd = int(0.03 * SR); f = 3000 + rng.random() * 5000
        seg = np.sin(2 * np.pi * f * t[:dd]) * np.exp(-t[:dd] / 0.006) * (0.4 + rng.random() * 0.6)
        out[o:o + dd] += seg[:len(out[o:o + dd])]
    pop = fft_filter(rng.standard_normal(len(t)), lo=600, hi=5000) * np.exp(-t / 0.04)
    return fade(norm(out + pop * 0.8), 0.001, 0.1)
def bed(d, bpm=100):
    """very subtle tension bed: sub pulse + filtered hats (synthesized, royalty-free)"""
    t = t_(d); beat = 60 / bpm; y = np.zeros(len(t))
    for k in range(int(d / beat) + 1):
        o = int(k * beat * SR); L = min(int(0.5 * SR), len(t) - o)
        if L <= 0: break
        tt = t[:L]; y[o:o + L] += 0.8 * np.sin(2 * np.pi * (45 + 25 * np.exp(-tt / 0.04)) * tt) * np.exp(-tt / 0.18)
        oh = int((k + 0.5) * beat * SR); Lh = min(int(0.05 * SR), len(t) - oh)
        if Lh > 0: y[oh:oh + Lh] += 0.15 * fft_filter(rng.standard_normal(Lh), lo=7000) * np.exp(-t[:Lh] / 0.01)
    pad = sum(np.sin(2 * np.pi * f * t + p) for f, p in ((55, 0), (82.4, 1), (110, 2))) * 0.12
    pad *= 0.6 + 0.4 * np.sin(2 * np.pi * t / 8)
    return norm(np.tanh(y + pad))

LIB_FN = dict(sub=sub_boom, impact=impact, swell=swell, whooshD=whoosh_deep, glitch=glitch, shutter=shutter,
              heart=heartbeat, tickhi=tick_hi, cashpro=cash_pro, poppro=pop_pro, dingpro=ding_pro, confetti=confetti)
