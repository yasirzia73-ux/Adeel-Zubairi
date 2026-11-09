"""Original, royalty-free background music, synthesized in code (no samples).
Usage: python3 music_gen.py <sync.json> <out.wav> [bpm]
- Intro (until the 'drop' line): dark tension: sub drone, ticking clock, heartbeat pulse.
- After the drop: upbeat groove (kick, clap, hats, bass, plucked chords, pad), Am-F-C-G.
- At each chapter start: 2-bar filtered build then full groove again."""
import json, sys, math, wave
import numpy as np
SR = 48000
rng = np.random.default_rng(7)

def t_(d): return np.arange(int(d * SR)) / SR
def lp(x, fc):  # one-pole low-pass
    a = math.exp(-2 * math.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y
def kick():
    t = t_(0.45); f = 48 + 110 * np.exp(-t / 0.035)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16))
def clap():
    t = t_(0.25); n = rng.standard_normal(len(t)); env = np.exp(-t / 0.06)
    for o in (0.0, 0.012, 0.024): env += 0.6 * np.exp(-np.maximum(t - o, 0) / 0.008) * (t >= o)
    x = n * env; return x - lp(x, 900)
def hat(open_=False):
    t = t_(0.18 if open_ else 0.05); n = rng.standard_normal(len(t)); x = n - lp(n, 6000)
    return x * np.exp(-t / (0.06 if open_ else 0.012)) * 0.6
def note(f, d, kind='pluck'):
    t = t_(d)
    if kind == 'pluck':
        x = sum(a * np.sin(2 * np.pi * f * m * t) for m, a in ((1, 1), (2, .45), (3, .2), (4, .1)))
        return x * np.exp(-t / 0.35) * (1 - np.exp(-t / 0.003))
    if kind == 'bass':
        x = np.tanh(2.2 * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)))
        return x * np.minimum(1, t / 0.005) * np.exp(-t / 0.6)
    if kind == 'pad':
        x = sum(np.sin(2 * np.pi * f * dt * t + p) for dt, p in ((1, 0), (1.004, 1), (0.996, 2), (2.002, .5))) / 4
        env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
        return x * env
def tick():
    t = t_(0.03); return np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.004)
def heart():
    t = t_(0.7); y = np.zeros(len(t))
    for off, a in ((0, 1), (0.2, .7)):
        o = int(off * SR); tt = t[:len(t) - o]; y[o:] += a * np.sin(2 * np.pi * (45 + 25 * np.exp(-tt / .03)) * tt) * np.exp(-tt / .1)
    return np.tanh(2 * y)
def riser(d):
    t = t_(d); n = rng.standard_normal(len(t)); env = (t / d) ** 2.5
    sw = np.sin(2 * np.pi * np.cumsum(200 * (8 ** (t / d))) / SR)
    return (n - lp(n, 1500)) * env * 0.5 + sw * env * 0.3

# A minor progression: Am, F, C, G (root Hz, triad Hz)
CH = [(110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]), (130.81, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]

def build(sync, out, bpm=104):
    s = [l['start'] for l in sync['lines']]; total = sync['total'] + 2
    drop = s[sync.get('drop', 6)] if len(s) > 6 else 8.0
    chapters = [s[i] for i in sync.get('chapters', []) if i < len(s)]
    beat = 60 / bpm; bar = 4 * beat
    mix = np.zeros(int(total * SR))
    def put(x, t, g):
        i = int(t * SR); x = x[:len(mix) - i]
        if i >= 0 and len(x) > 0: mix[i:i + len(x)] += x * g
    K, CL, HC, HO = kick(), clap(), hat(), hat(True)
    # ---- intro tension ----
    tt = t_(drop); drone = (np.sin(2 * np.pi * 55 * tt) + 0.5 * np.sin(2 * np.pi * 55.4 * tt)) * np.minimum(1, tt / 1.5) * 0.35
    mix[:len(drone)] += drone
    k = 0.0
    while k < drop - 0.1: put(tick(), k, 0.25); k += beat / 2
    k = 0.0
    while k < drop - 0.1: put(heart(), k, 0.55); k += 2 * beat
    put(riser(min(4.0, drop)), drop - min(4.0, drop), 0.8)
    # ---- groove after drop ----
    t0 = drop; nbars = int((total - t0) / bar) + 1
    def in_build(t):  # 2 bars before each chapter: thin out (no kick), riser
        return any(c - 2 * bar <= t < c for c in chapters)
    for b in range(nbars):
        tb = t0 + b * bar; root, tri = CH[b % 4]
        if tb > total - 2: break
        build_ = in_build(tb)
        for q in range(4):
            tq = tb + q * beat
            if not build_: put(K, tq, 0.9 if q in (0, 2) else 0.5 if q == 3 and b % 2 else 0)
            if q in (1, 3): put(CL, tq, 0.45)
            put(HC, tq, 0.25); put(HC, tq + beat / 2, 0.18)
        if b % 2 == 1: put(HO, tb + 3.5 * beat, 0.2)
        # bass: root on 1, octave pickup
        put(note(root, beat * 1.5, 'bass'), tb, 0.42); put(note(root, beat, 'bass'), tb + 2 * beat, 0.32); put(note(root * 2, beat / 2, 'bass'), tb + 3.5 * beat, 0.22)
        # plucked arpeggio (8ths)
        arp = tri + [tri[1] * 2]
        for e in range(8): put(note(arp[(e * 3 + b) % 4] * 2, beat * 0.6, 'pluck'), tb + e * beat / 2, 0.08 if not build_ else 0.05)
        put(sum(note(f, bar, 'pad') for f in tri) / 3, tb, 0.16)
    for c in chapters:  # riser + crash into each chapter
        put(riser(2 * bar), c - 2 * bar, 0.45)
        n = rng.standard_normal(int(1.6 * SR)); cr = (n - lp(n, 4000)) * np.exp(-t_(1.6) / 0.5)
        put(cr, c, 0.25); put(K, c, 1.0)
    # ending fade
    f = int(3 * SR); mix[-f:] *= np.linspace(1, 0, f)
    mix = np.tanh(mix * 0.9); mix /= max(1e-9, np.max(np.abs(mix))); mix *= 0.89
    st = np.stack([mix, np.roll(mix, int(0.012 * SR)) * 0.96], 1)  # slight stereo width
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())

if __name__ == '__main__':
    sync = json.load(open(sys.argv[1])); bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 104
    build(sync, sys.argv[2], bpm); print('ok')
