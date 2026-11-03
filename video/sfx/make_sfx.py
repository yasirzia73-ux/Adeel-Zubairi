"""Procedurally synthesized SFX (no third-party samples) + event-timed mix for both flat videos."""
import json, math, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)

def t_(d): return np.arange(int(d * SR)) / SR
def env_exp(d, tau): return np.exp(-t_(d) / tau)
def lp(x, fc):
    """one-pole low-pass; fc may be scalar or per-sample array"""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y
def hp(x, fc): return x - lp(x, fc)
def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1; return x / m * peak
def fade(x, fi=0.003, fo=0.01):
    n1, n2 = int(fi * SR), int(fo * SR); x = x.copy()
    if n1: x[:n1] *= np.linspace(0, 1, n1)
    if n2: x[-n2:] *= np.linspace(1, 0, n2)
    return x
def sweep(f0, f1, d, shape='exp'):
    t = t_(d); f = f0 * (f1 / f0) ** (t / d) if shape == 'exp' else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def bell(f, d=1.2, tau=0.35, partials=((1, 1), (2.01, .45), (3.02, .25), (4.17, .12))):
    t = t_(d); y = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (tau / (1 + 0.6 * k)))
                       for k, (m, a) in enumerate(partials))
    return fade(norm(y), 0.002, 0.05)

def pop(pitch=1.0):
    d = 0.16; y = sweep(950 * pitch, 260 * pitch, d) * env_exp(d, 0.045)
    y += 0.25 * hp(rng.standard_normal(len(y)), 2000) * env_exp(d, 0.006)
    return fade(norm(y))
def tick():
    d = 0.05; y = np.sin(2 * np.pi * 1700 * t_(d)) * env_exp(d, 0.008)
    return fade(norm(y))
def whoosh(d=0.55, up=True):
    n = rng.standard_normal(int(d * SR)); t = t_(d)
    shape = np.sin(np.pi * (t / d) ** (0.6 if up else 1.6)) ** 2
    fc = 300 + 3500 * shape
    y = hp(lp(n, fc), 150) * shape
    return fade(norm(y), 0.01, 0.05)
def coin():
    d = 0.45; t = t_(d)
    y = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((2093, 1), (3136, .7), (4186, .45), (5274, .3))) * np.exp(-t / 0.09)
    y2 = np.zeros_like(y); off = int(0.055 * SR)
    y2[off:] = (sum(a * np.sin(2 * np.pi * f * t) for f, a in ((2637, 1), (3951, .6), (5274, .35))) * np.exp(-t / 0.12))[:-off]
    return fade(norm(y + 0.8 * y2))
def ding(f=1318.5): return bell(f, 1.0, 0.3)
def chime():
    out = np.zeros(int(1.6 * SR))
    for i, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
        b = bell(f, 1.1, 0.32); s = int(i * 0.085 * SR); out[s:s + len(b)] += b[:len(out) - s] * (0.8 + 0.1 * i)
    return fade(norm(out), 0.002, 0.1)
def cash():
    out = np.zeros(int(1.4 * SR))
    for i in range(4):
        c = coin(); s = int(i * 0.06 * SR); out[s:s + len(c)] += c * (1 - 0.15 * i)
    b = bell(2093, 1.2, 0.4); s = int(0.18 * SR); out[s:s + len(b)] += 0.9 * b[:len(out) - s]
    return fade(norm(out), 0.002, 0.1)
def thud():
    d = 0.4; t = t_(d)
    y = np.sin(2 * np.pi * np.cumsum(110 * np.exp(-t / 0.08) + 45) / SR) * np.exp(-t / 0.12)
    y += 0.5 * lp(rng.standard_normal(len(t)), 900) * np.exp(-t / 0.03)
    return fade(norm(y))
def stamp():
    y = thud(); k = 0.35 * hp(rng.standard_normal(int(0.08 * SR)), 1500) * env_exp(0.08, 0.012)
    y[:len(k)] += k; return norm(y)
def poof():
    d = 0.6; t = t_(d); n = rng.standard_normal(len(t))
    e = (1 - np.exp(-t / 0.02)) * np.exp(-t / 0.16)
    y = lp(n, 2500 * np.exp(-t / 0.25) + 200) * e
    y += 0.3 * sweep(900, 300, d) * np.exp(-t / 0.1)
    return fade(norm(y), 0.002, 0.05)
def sparkle():
    out = np.zeros(int(1.0 * SR))
    for i, f in enumerate((2637, 3136, 3520, 4186, 4699)):
        b = bell(f, 0.6, 0.12); s = int(i * 0.05 * SR); out[s:s + len(b)] += b[:len(out) - s] * 0.7
    return fade(norm(out), 0.002, 0.1)
def riser(d=2.6):
    t = t_(d); n = rng.standard_normal(len(t)); sh = (t / d) ** 1.8
    y = hp(lp(n, 400 + 5000 * sh), 200) * sh * 0.7 + 0.35 * sweep(180, 720, d) * sh
    return fade(norm(y), 0.05, 0.03)
def buzzer():
    d = 0.42; t = t_(d); sq = np.sign(np.sin(2 * np.pi * 155 * t)) + 0.6 * np.sign(np.sin(2 * np.pi * 160 * t))
    y = lp(sq, 1400) * (np.minimum(1, t / 0.01)) * np.exp(-t / 0.35)
    return fade(norm(y), 0.003, 0.04)
def alarm(d=2.4):
    t = t_(d); car = np.sin(2 * np.pi * 2350 * t) + 0.5 * np.sin(2 * np.pi * 3520 * t)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 22 * t); bursts = lp(((t % 0.5) < 0.36).astype(float), 30)
    y = lp(car * am * bursts, 6000)
    return fade(norm(y), 0.005, 0.05)
def step():
    d = 0.12; t = t_(d); y = lp(rng.standard_normal(len(t)), 500) * np.exp(-t / 0.025) + 0.6 * np.sin(2 * np.pi * 80 * t) * np.exp(-t / 0.03)
    return fade(norm(y))
def flip():
    d = 0.3; t = t_(d); y = hp(lp(rng.standard_normal(len(t)), 5000), 800) * np.sin(np.pi * t / d) ** 3
    return fade(norm(y))
def firework():
    d = 1.2; t = t_(d); boom = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-t / 0.2) + 40) / SR) * np.exp(-t / 0.25)
    cr = rng.standard_normal(len(t)) * (rng.random(len(t)) < 0.004) * np.exp(-t / 0.5)
    y = 0.8 * boom + 2.5 * hp(cr, 1500)
    return fade(norm(y), 0.002, 0.1)
def rewind():
    w = whoosh(0.7, up=True)[::-1].copy(); t = t_(0.7)
    w += 0.4 * sweep(1500, 300, 0.7) * np.sin(np.pi * t / 0.7)
    return fade(norm(w), 0.01, 0.05)
def slide(): return whoosh(0.35, up=True)

LIB = {k: f() for k, f in dict(pop=pop, pophi=lambda: pop(1.35), poplo=lambda: pop(0.75), tick=tick, whoosh=whoosh,
       whooshS=slide, coin=coin, ding=ding, dinghi=lambda: ding(1760), chime=chime, cash=cash, thud=thud, stamp=stamp,
       poof=poof, sparkle=sparkle, buzzer=buzzer, step=step, flip=flip, firework=firework, rewind=rewind).items()}

# ---------- events ----------
TM = json.load(open('/tmp/sfx/timing.json'))
def mk(vid):
    d = TM[vid]; C = {c['key']: c['start'] for c in d['cues']}; E = {c['key']: c['end'] for c in d['cues']}
    D = {k: E[k] - C[k] for k in C}; SC = d['scenes']; ev = []
    def a(t, name, g=0.5, pan=0.0, **kw): ev.append((t, name, g, pan, kw))
    for i, s in enumerate(d['order']):
        if i: a(SC[s]['start'] - 0.15, 'whoosh', 0.22)
    if vid == 'v1':
        for i in range(10): a(C['h1'] + i * 0.08, 'coin', 0.10, -0.4)
        for i in range(12): a(C['h2'] + i * 0.08, 'coin', 0.10, 0.4)
        a(C['h3'], 'pop', 0.3); a(C['h4'], 'riser', 0.28, dur=1.6); a(C['h4'] + 0.8, 'chime', 0.45)
        for i in range(5): a(C['m1'] + 0.1 + i * 0.27, 'step', 0.25, -0.3 if i % 2 else 0.3)
        a(C['m3'], 'pop', 0.35, -0.3); a(C['m3'] + 0.12, 'pop', 0.3, 0.3); a(C['m4'], 'pophi', 0.3); a(C['m5'], 'whooshS', 0.25)
        t = C['m6'] + 0.9
        while t < E['m7']: a(t, 'coin', 0.3, -0.1); t += 0.9
        a(C['m8'], 'pop', 0.35, 0.3); a(C['m9'], 'pophi', 0.25, 0.3); a(C['m10'], 'thud', 0.45)
        a(C['s1'], 'tick', 0.2); a(C['s2'], 'coin', 0.3, -0.3); a(C['s3'], 'pop', 0.4, -0.5); a(C['s3'] + 0.15, 'pophi', 0.3, -0.5)
        a(C['s4'], 'stamp', 0.55, -0.2); a(C['s5'], 'pophi', 0.4, 0.4)
        for i in range(3): a(C['s6'] + 0.3 + i * 0.6, 'coin', 0.22, 0.5)
        a(C['s8'], 'coin', 0.3, 0.5); a(C['s9'], 'thud', 0.4)
        a(C['r1'] - 0.2, 'riser', 0.22, dur=C['r2'] - C['r1'] + 0.2); a(C['r4'], 'riser', 0.2, dur=2.2)
        a(C['r5'], 'riser', 0.3, dur=E['r5'] - C['r5'] + 0.8); a(E['r5'] + 0.8, 'ding', 0.45)
        a(C['r6'], 'cash', 0.35); a(C['r7'], 'buzzer', 0.22); a(C['r8'], 'thud', 0.55)
        a(C['w1'], 'sparkle', 0.35)
        for i in range(4): a(C['w2'] + i * 0.8, 'coin', 0.25 + 0.04 * i)
        a(C['w3'], 'whoosh', 0.3, dur=1.0); a(C['w4'] + 1.0, 'whoosh', 0.3); a(C['w5'], 'whoosh', 0.35)
        for i in range(6): a(C['w6'] + 0.5 + i * 0.55, 'pop', 0.3, -0.6 + i * 0.24, pitch=1 + i * 0.12)
        a(C['w8'], 'chime', 0.4); a(C['w9'], 'whooshS', 0.3); a(C['w10'], 'whooshS', 0.3)
        a(C['w11'] + 2.2, 'ding', 0.35); a(C['w13'], 'pop', 0.3); a(C['w15'], 'thud', 0.4); a(C['w15'] + 0.05, 'chime', 0.4)
        a(C['b1'], 'rewind', 0.45); a(C['b2'], 'riser', 0.28, dur=E['b3'] - C['b2']); a(C['b3'] + 0.3, 'cash', 0.45)
        a(C['b4'], 'whooshS', 0.3); a(C['b4'] + 1.2, 'pop', 0.35, 0.3); a(C['b5'], 'buzzer', 0.25)
        a(C['t1'], 'poplo', 0.25); a(C['t2'] + 0.6, 'sparkle', 0.4); a(C['t3'], 'pop', 0.35)
        for k in ('t4', 't6', 't7', 't8', 't9'): a(C[k], 'whooshS', 0.2, 0.3); a(C[k] + 0.25, 'tick', 0.3, 0.3)
        a(C['e1'], 'whoosh', 0.2); a(C['e3'], 'chime', 0.35); a(C['e4'], 'pop', 0.4); a(C['e4'] + 0.3, 'ding', 0.3)
    elif vid == 'v2':
        a(C['h1'], 'pop', 0.4); a(C['h1'] + 0.6, 'pophi', 0.35, 0.3); a(C['h1'] + 1.0, 'alarm', 0.12, 0.3, dur=2.6)
        a(C['h1'] + 1.1, 'coin', 0.2); a(C['h2'] + 0.3, 'poof', 0.45); a(C['h2'] + 1.3, 'thud', 0.3)
        a(C['h3'], 'whoosh', 0.3); a(C['h3'] + 0.35, 'pop', 0.35, 0.3); a(C['h4'], 'pop', 0.35, 0.4); a(C['h4'] + 0.1, 'sparkle', 0.3, 0.4)
        for i in range(6): a(C['i1'] - 0.2 + i * 0.25, 'step', 0.25, -0.5 + i * 0.1)
        a(C['i1'] + 0.8, 'pop', 0.4, 0.3)
        for i in range(5): a(C['i1'] + 1.3 + i * 0.25, 'tick', 0.22, 0.4)
        a(C['i2'], 'thud', 0.35)
        firsts = ['f1', 'k1', 'l1', 'd1', 'o1']
        for n, s in enumerate(['fsa', 'k401', 'loss', 'give', 'next']):
            a(SC[s]['start'] + 0.25, 'pop', 0.45, 0, pitch=0.9 + n * 0.06)
            a(SC[s]['end'] - 1.5, 'tick', 0.35, 0.7); a(SC[s]['end'] - 1.45, 'dinghi', 0.35, 0.7)
        a(C['f2'], 'pop', 0.4, -0.4); a(C['f2'] + 1.6, 'pophi', 0.25, -0.4)
        a(C['f3'], 'pop', 0.3, 0.4); a(C['f3'] + 0.3, 'stamp', 0.5, 0.3)
        a(C['f4'], 'whooshS', 0.3, 0.4); a(C['f4'] + 0.42 * D['f4'], 'tick', 0.3, 0.3); a(C['f4'] + 0.74 * D['f4'], 'buzzer', 0.15, 0.3)
        a(C['f5'] + 0.2, 'poof', 0.45, 0.5); a(C['f5'] + 0.8, 'thud', 0.4, 0.3)
        a(C['f6'] + 0.2, 'pophi', 0.25, -0.4)
        for i in range(4): a(C['f6'] + 1.3 + i * 0.9, 'pop', 0.3, 0.3, pitch=1 + i * 0.08)
        a(C['k2'] + 0.3, 'riser', 0.25, dur=2.6); a(C['k2'] + 2.9, 'ding', 0.4)
        for i in range(4): a(C['k3'] + 0.2 + i * 0.3, 'pop', 0.25, -0.5 + i * 0.33, pitch=1 + i * 0.07)
        for i in range(4): a(C['k3'] + 0.6 + 1.3 + i * 0.3, 'coin', 0.15, -0.5 + i * 0.33)
        a(C['k3'] + 2.0, 'tick', 0.3, 0.6)
        a(C['k4'], 'pop', 0.35, -0.3); a(C['k4'] + 2.2, 'cash', 0.45, 0.3); a(C['k5'] + 0.3, 'pop', 0.35); a(C['k5'] + 0.4, 'sparkle', 0.3)
        a(C['l2'], 'pop', 0.35); a(C['l3'] + 0.3, 'stamp', 0.5, 0.2); a(C['l4'], 'whooshS', 0.3); a(C['l4'] + 0.05, 'pop', 0.3, -0.4)
        a(C['l4'] + 0.8, 'ding', 0.3); a(C['l4'] + 0.55 * D['l4'], 'pophi', 0.3)
        a(C['l5'], 'pop', 0.3)
        for i in range(30): a(C['l5'] + 0.3 + i * 0.06, 'tick', 0.09, -0.5 + (i % 10) * 0.11)
        a(C['l5'] + 2.6, 'buzzer', 0.3)
        a(C['l6'] + 0.2, 'buzzer', 0.22, -0.4); a(C['l6'] + 1.2, 'ding', 0.4, 0.4)
        for i in range(5): a(C['d1'] - 0.1 + i * 0.26, 'step', 0.22, -0.6)
        a(C['d2'], 'pop', 0.3, 0.4)
        for i in range(3):
            t = C['d2'] + i * 0.45 + 1.2
            while t < C['d3']: a(t, 'coin', 0.22, 0.4); t += 1.35
        a(C['d3'], 'whooshS', 0.25); a(C['d3'] + 1.0, 'pop', 0.4, 0.3); a(C['d3'] + 1.05, 'cash', 0.35, 0.3)
        a(C['d4'], 'pophi', 0.35, 0.3); a(C['d5'], 'flip', 0.35); a(C['d5'] + 0.3, 'tick', 0.25, 0.4); a(C['d5'] + 1.6, 'ding', 0.3, 0.4)
        a(C['o2'], 'pop', 0.35)
        for i in range(3): a(C['o2'] + 1.2 + i * 0.7, 'tick', 0.35); a(C['o2'] + 1.22 + i * 0.7, 'dinghi', 0.12)
        a(C['o3'] + 0.2, 'pop', 0.35, 0.3); a(C['o4'], 'pop', 0.3, -0.3); a(C['o4'] + 0.8, 'poof', 0.25, -0.3)
        for i in range(3): a(C['o4'] + 1.4 + i * 0.9, 'coin', 0.3, 0.5)
        a(C['o5'], 'pop', 0.3); a(C['o5'] + 1.2, 'whooshS', 0.3); a(C['o5'] + 2.0, 'pop', 0.35); a(C['o5'] + 2.05, 'sparkle', 0.3)
        a(C['x1'], 'pop', 0.4, -0.3); a(C['x1'] + 1.0, 'buzzer', 0.3, -0.3); a(C['x2'], 'flip', 0.5, -0.3)
        a(C['x2'] + 0.8, 'pop', 0.4, 0.3)
        t = C['x2'] + 1.2 + 1.0
        while t < SC['bonus']['end']: a(t, 'coin', 0.25, 0.3); t += 1.2
        a(C['x3'], 'cash', 0.4, 0.3)
        for i in range(5): a(C['r2'] + 0.2 + i * D['r2'] / 5, 'tick', 0.35); a(C['r2'] + 0.22 + i * D['r2'] / 5, 'ding', 0.18, 0, pitch=1 + i * 0.12)
        a(C['r3'], 'pop', 0.3)
        for off, pan in ((0, 0.3), (0.55, 0.7), (1.1, 0.1), (0.8, 0.5)):
            t = C['e1'] + off
            while t < C['e2']: a(t, 'firework', 0.25, pan); t += 1.7
        a(C['e1'], 'chime', 0.4); a(C['e2'], 'pop', 0.4); a(C['e2'] + 0.3, 'ding', 0.3)
    elif vid == 'v3':
        a(C['h1'], 'pop', 0.4); a(C['h1'] + 0.7, 'whooshS', 0.3); a(C['h1'] + 0.9, 'sparkle', 0.4)
        for i in range(9): a(C['h1'] + 0.95 + i * 0.06, 'coin', 0.08, -0.6 + i * 0.15)
        a(C['h2'] + 0.2, 'stamp', 0.55); a(C['h3'], 'whoosh', 0.3); a(C['h3'] + 0.35, 'pop', 0.35, 0.3)
        for i in range(5): a(C['w1'] - 0.15 + i * 0.27, 'step', 0.25, 0.5 - i * 0.12)
        a(C['w1'] + 1.8, 'whooshS', 0.25); a(C['w1'] + 2.9, 'thud', 0.2); a(C['w2'], 'whoosh', 0.3, 0.4); a(C['w2'] + 0.5, 'pop', 0.4, 0.4)
        a(C['w3'], 'pop', 0.3, -0.3); a(C['w4'], 'pophi', 0.3, -0.3)
        for i in range(4): a(C['w4'] + 0.9 + i * 1.2, 'coin', 0.15)
        a(C['w5'], 'whooshS', 0.25, 0.4)
        for i in range(12): a(C['w5'] + 0.3 + i * 0.12, 'pop', 0.12, 0.3 + (i % 4) * 0.1, pitch=1 + (i % 4) * 0.1)
        a(C['w6'], 'pop', 0.4); a(C['w6'] + 0.1, 'flip', 0.3)
        a(C['m1'] + 0.2, 'pop', 0.4); a(C['m1'] + 0.3, 'sparkle', 0.3); a(C['m2'], 'whooshS', 0.25); a(C['m3'], 'tick', 0.3)
        t = C['m4'] + 1.1
        while t < C['m7']: a(t, 'coin', 0.16, -0.4); t += 0.55
        t = C['m5'] + 1.1
        while t < C['m7']: a(t, 'coin', 0.16, 0.4); t += 1.1
        a(C['m4'] + 0.5, 'riser', 0.15, dur=1.5); a(C['m5'] + 0.3, 'cash', 0.4, 0.4); a(C['m6'], 'pop', 0.4); a(C['m6'] + 0.1, 'chime', 0.4)
        a(C['m7'] + 0.3, 'poof', 0.4); a(C['m7'] + 0.4, 'buzzer', 0.3)
        a(C['c1'], 'thud', 0.4); a(C['c2'], 'pop', 0.35); a(C['c3'] + 0.4, 'riser', 0.28, dur=D['c3'] - 0.2); a(E['c3'] + 0.2, 'cash', 0.45)
        a(C['c4'], 'pop', 0.35, -0.3); a(C['c4'] + 0.5, 'ding', 0.35, 0.3)
        a(C['t2'] + 1.2, 'whooshS', 0.3); a(C['t2'] + 1.9, 'tick', 0.3); a(C['t3'] + 0.6, 'cash', 0.4, 0.3)
        a(C['t4'], 'whoosh', 0.25); a(C['t5'] + 0.1, 'pop', 0.35, -0.4); a(C['t5'] + 1.6, 'pop', 0.35, 0.4, pitch=1.15)
        a(C['t6'], 'pop', 0.35); a(C['t6'] + 0.1, 'sparkle', 0.3)
        for i in range(4): a(C['r1'] + 0.2 + i * 0.15, 'pop', 0.3, -0.5 + i * 0.33, pitch=1 + i * 0.1)
        for k in ('r2', 'r3', 'r4', 'r5'): a(C[k], 'whooshS', 0.25); a(C[k] + 0.1, 'pop', 0.3, -0.4)
        a(C['r3'] + 1.0, 'stamp', 0.25, -0.4); a(C['r5'] + 1.2, 'whooshS', 0.25, -0.4)
        for k in ('s2', 's3', 's4', 's5'): a(C[k] + 0.6, 'tick', 0.35, 0.3); a(C[k] + 0.62, 'dinghi', 0.2, 0.3)
        a(C['s6'] + 0.2, 'pop', 0.35, 0.3); a(C['s6'] + 0.3, 'buzzer', 0.15, 0.3)
        a(C['e1'], 'chime', 0.4)
        for i in range(10): a(C['e1'] + 0.3 + i * 0.5, 'coin', 0.1, -0.7 + (i * 0.37) % 1.4)
        a(C['e2'], 'pop', 0.4); a(C['e2'] + 0.3, 'ding', 0.3)
    elif vid == 'v4':
        a(C['h1'], 'thud', 0.4)
        for i in range(12): a(C['h1'] + i * 0.08, 'tick', 0.12)
        a(C['h1'] + 1.0, 'pop', 0.35); a(C['h2'], 'whoosh', 0.3)
        t = C['h2'] + 0.6
        while t < C['h4b']: a(t, 'coin', 0.10, 0.5); t += 0.35 if t > C['h3'] else 0.7
        a(C['h3'], 'riser', 0.3, dur=E['h4'] - C['h3']); a(E['h4'], 'thud', 0.5)
        for i in range(3): a(C['h4b'] + i * 0.55, 'whooshS', 0.25)
        a(C['h4b'] + 1.8, 'thud', 0.45); a(C['h5'], 'pop', 0.4); a(C['h5'] + 1.6, 'cash', 0.35)
        a(C['h6'], 'whoosh', 0.3); a(C['h6'] + 2.0, 'stamp', 0.55); a(C['h7'], 'pop', 0.4); a(C['h7'] + 0.9, 'buzzer', 0.3)
        a(C['h8'], 'thud', 0.5); a(C['h8'] + 0.05, 'sparkle', 0.3)
        for i in range(5): a(C['j1'] - 0.1 + i * 0.27, 'step', 0.22, -0.4)
        a(C['j1'] + 1.0, 'pop', 0.4, 0.4); a(C['j2'], 'tick', 0.3, 0.4); a(C['j3'], 'buzzer', 0.4, 0.4); a(C['j4'], 'stamp', 0.3, 0.4)
        for i in range(12): a(C['j5'] + i * 0.09, 'tick', 0.1, -0.6 + i * 0.1)
        a(C['b1'], 'pop', 0.4); a(C['b2'], 'whooshS', 0.3); a(C['b2'] + 1.5, 'cash', 0.3); a(C['b3'] + 0.2, 'thud', 0.35, -0.4)
        a(C['b4'] + 0.2, 'pop', 0.35, 0.4)
        for i in range(4): a(C['b5'] + 0.6 + i * 0.3, 'coin', 0.15, 0.6)
        a(C['b6'] + 1.2, 'buzzer', 0.3, 0.5)
        a(C['k1'], 'thud', 0.45); a(C['k2'], 'pop', 0.35); a(C['k3'] + 0.3, 'buzzer', 0.3, -0.3); a(C['k3'] + 0.5, 'riser', 0.2, dur=1.2); a(C['k3'] + 1.6, 'stamp', 0.3, 0.4)
        a(C['k4'], 'pop', 0.35); a(C['k4'] + 0.9, 'stamp', 0.45); a(C['k4'] + 2.4, 'tick', 0.3)
        a(C['k5'], 'flip', 0.4); a(C['k5'] + 1.0, 'whooshS', 0.2); a(C['k6'], 'whoosh', 0.25); a(C['k7'], 'pop', 0.35)
        for i in range(9): a(C['k8'] + 0.6 + i * 0.45, 'coin', 0.16, -0.8 + i * 0.2)
        a(C['k8'] + 0.5, 'riser', 0.25, dur=4.0); a(C['k9'], 'thud', 0.4); a(C['k9b'], 'whoosh', 0.25); a(C['k10'], 'stamp', 0.55)
        a(C['n1'], 'pop', 0.4); a(C['n1'] + 1.8, 'stamp', 0.55); a(C['n2'], 'thud', 0.45); a(C['n3'], 'pop', 0.35)
        a(C['n3b'], 'pop', 0.35); a(C['n3c'] + 0.5, 'tick', 0.45); a(C['n3c'] + 0.6, 'buzzer', 0.35)
        for k in ('n4', 'n5'): a(C[k] + 0.2, 'whooshS', 0.25); a(C[k] + 1.0, 'pop', 0.35)
        a(C['n6'] + 0.2, 'riser', 0.3, dur=0.9); a(C['n6'] + 1.1, 'thud', 0.55)
        a(C['n7'], 'pop', 0.35); a(C['n8'] + 0.8, 'stamp', 0.5)
        a(C['f1'], 'whoosh', 0.25); a(C['f1'] + 1.5, 'dinghi', 0.3); a(C['f1'] + 2.6, 'buzzer', 0.25)
        for i in range(6): a(C['f2'] + i * 0.4, 'tick', 0.2)
        a(C['f3'] + 1.5, 'poof', 0.25); a(C['f3'] + 2.1, 'poof', 0.25)
        for i in range(5): a(C['f4'] + i * 0.5, 'poof', 0.22, -0.6 + i * 0.3)
        a(C['f4'] + 2.7, 'cash', 0.35); a(C['f5'], 'whooshS', 0.25); a(C['f5'] + 0.5, 'whoosh', 0.3, 0.3); a(C['f6'], 'thud', 0.35); a(C['f6b'], 'whoosh', 0.25)
        a(C['r1'], 'thud', 0.4); a(C['r2'], 'pop', 0.35); a(C['r2'] + 3, 'ding', 0.35); a(C['r2b'], 'pop', 0.3, -0.4); a(C['r2b'] + 2.5, 'buzzer', 0.25, 0.4)
        a(C['r3'] + 0.5, 'riser', 0.25, dur=2.0); a(C['r3'] + 2.5, 'chime', 0.4); a(C['r4'], 'pop', 0.35, -0.4)
        for i in range(4): a(C['r4'] + 1.2 + i * 0.4, 'pop', 0.25, 0.4, pitch=1 + i * 0.1)
        for i in range(5): a(C['r5'] + i * 0.4, 'step', 0.18, 0.4)
        a(C['r5'] + 1.5, 'riser', 0.2, dur=2.0); a(C['r6'], 'whooshS', 0.25); a(C['r6'] + 1.4, 'thud', 0.4)
        a(C['r7'], 'pop', 0.35); a(C['r7'] + 0.1, 'dinghi', 0.3); a(C['r7'] + 1.6, 'stamp', 0.45)
        a(C['t1'], 'thud', 0.35); a(C['t2'] + 0.3, 'cash', 0.3); a(C['t3'] + 0.5, 'buzzer', 0.25); a(C['t4'] + 0.6, 'thud', 0.5); a(C['t4'] + 0.8, 'poof', 0.3)
        a(C['t4'] + 2.5, 'pop', 0.3); a(C['t5'], 'whoosh', 0.2); a(C['t6'], 'pop', 0.4); a(C['t6'] + 0.8, 'sparkle', 0.4)
        for k in ('l2', 'l3', 'l4', 'l5', 'l6'): a(C[k], 'whooshS', 0.2, 0.3); a(C[k] + 0.25, 'tick', 0.3, 0.3)
        a(C['e1'] + 1.2, 'thud', 0.4); a(C['e2'], 'whoosh', 0.2); a(C['e2b'], 'pop', 0.3); a(C['e3'], 'pop', 0.4); a(C['e3'] + 0.3, 'chime', 0.35)
    return ev, d['total']

def resample(x, r):
    if r == 1: return x
    idx = np.arange(0, len(x) - 1, r); return np.interp(idx, np.arange(len(x)), x)

def render(vid, out):
    ev, total = mk(vid)
    mix = np.zeros((int((total + 2) * SR), 2))
    for t, name, g, pan, kw in ev:
        if name == 'riser': x = riser(max(0.4, kw['dur']))
        elif name == 'alarm': x = alarm(kw['dur'])
        else:
            x = LIB[name]
            if 'pitch' in kw: x = resample(x, kw['pitch'])
            if 'dur' in kw and name == 'whoosh': x = resample(x, 0.55 / kw['dur'])
        s = int(max(0, t) * SR); x = x[:len(mix) - s] * g
        l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        mix[s:s + len(x), 0] += x * l * 1.4; mix[s:s + len(x), 1] += x * r * 1.4
    # gentle limiter
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.89
    pcm = (mix * 32767).astype('<i2')
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(vid, len(ev), 'events ->', out)

for v in (sys.argv[1:] or ['v1', 'v2']): render(v, f'/tmp/sfx/{v}.wav')
