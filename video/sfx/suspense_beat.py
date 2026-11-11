"""Original suspense beat (beats only, no melody), synthesized in code. Royalty-free.
Usage: python3 suspense_beat.py <seconds> <out.wav> [bpm]
Low sub drone + heartbeat-style kick + ticking hats + soft rim clicks; a slow riser every 8 bars."""
import sys, math, wave
import numpy as np
SR = 48000; rng = np.random.default_rng(3)
def t_(d): return np.arange(int(d * SR)) / SR
def hp(x, k=0.97):  # simple high-pass (difference) for noise hats
    y = np.empty_like(x); p = 0.0; q = 0.0
    for i in range(len(x)): q = k * (q + x[i] - p); p = x[i]; y[i] = q
    return y
def kick():
    t = t_(0.5); f = 42 + 70 * np.exp(-t / 0.04)
    return np.tanh(1.3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22))
HAT = hp(rng.standard_normal(int(0.03 * SR))) * np.exp(-t_(0.03) / 0.006)
def rim():
    t = t_(0.06); return (np.sin(2 * np.pi * 1700 * t) * 0.6 + hp(rng.standard_normal(len(t))) * 0.4) * np.exp(-t / 0.012)
def build(dur, out, bpm=92):
    beat = 60 / bpm; bar = 4 * beat; N = int((dur + 1) * SR); mix = np.zeros(N)
    def put(x, t, g):
        i = int(t * SR); x = x[:N - i]
        if 0 <= i < N: mix[i:i + len(x)] += x * g
    K, R = kick(), rim()
    tt = t_(dur + 1)
    drone = (np.sin(2 * np.pi * 41.2 * tt) + 0.6 * np.sin(2 * np.pi * 41.6 * tt) + 0.25 * np.sin(2 * np.pi * 82.4 * tt)) * (0.75 + 0.25 * np.sin(2 * np.pi * tt / 8))
    mix += drone * 0.22
    b = 0
    while b * bar < dur:
        tb = b * bar
        put(K, tb, 0.9); put(K, tb + 0.22, 0.55)              # heartbeat double kick on 1
        put(K, tb + 2 * beat, 0.7); put(K, tb + 2 * beat + 0.22, 0.4)
        for e in range(8): put(HAT, tb + e * beat / 2, 0.18 if e % 2 else 0.1)   # ticking clock
        put(R, tb + 3 * beat + beat / 2, 0.22)
        if b % 8 == 6:                                          # slow riser into every 8th bar
            d = 2 * bar; n = hp(rng.standard_normal(int(d * SR))) * (t_(d) / d) ** 3
            put(n, tb, 0.35)
        b += 1
    f = int(2 * SR); mix[-f:] *= np.linspace(1, 0, f); mix[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    mix = np.tanh(mix); mix /= max(1e-9, np.max(np.abs(mix))); mix *= 0.89
    st = np.stack([mix, np.roll(mix, int(0.01 * SR))], 1)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
if __name__ == '__main__':
    build(float(sys.argv[1]), sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 92); print('ok')
