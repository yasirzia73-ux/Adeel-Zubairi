"""SFX tracks for the 3 Shorts, reusing the synth library from video/sfx/make_sfx.py."""
import math, sys, wave
import numpy as np
src = open('/home/user/Adeel-Zubairi/video/sfx/make_sfx.py').read()
exec(src[:src.index('# ---------- events ----------')])   # SR, LIB, riser, alarm, resample...

def resample(x, r):
    if r == 1: return x
    idx = np.arange(0, len(x) - 1, r); return np.interp(idx, np.arange(len(x)), x)

SEGS = {
 1: [0, 1.86, 3.39, 6.68, 7.86, 10.06, 11.88, 13.80, 15.75, 16.71, 18.04, 20.24, 21.79, 23.87, 25.40, 29.19, 30.11, 32.84, 35.27, 36.85, 37.98, 39.22, 42.58, 43.81, 45.11],
 2: [0, 3.39, 4.74, 7.17, 8.40, 11.93, 14.67, 16.43, 19.02, 20.29, 24.44, 26.63, 28.99, 30.84],
 3: [0, 3.19, 4.92, 7.38, 11.00, 13.36, 15.18, 17.92, 19.15, 22.21, 22.91, 29.62, 32.24, 33.72, 35.83],
}
SEGS[4] = [0.07, 2.6, 5.74, 10.04, 11.42, 12.78, 17.77, 18.69, 20.13, 21.81, 23.18, 26.11, 28.48, 32.78, 34.89, 37.41, 42.79]
ENDS = {1: 46.60, 2: 33.41, 3: 37.56, 4: 46.13}

def events(i):
    s = SEGS[i]; ev = []
    def a(t, n, g=0.5, pan=0.0, **kw): ev.append((t, n, g, pan, kw))
    if i == 1:
        a(0.05, 'pop', 0.5, -0.3)
        for k in range(5): a(0.25 + k * 0.12, 'coin', 0.12, -0.3)
        a(s[2], 'whooshS', 0.3, 0.3)
        for k in range(10): a(s[2] + 0.1 + k * 0.09, 'coin', 0.12, 0.3)
        a(s[3], 'whoosh', 0.3); a(s[3] + 0.05, 'pop', 0.45); a(s[4], 'pop', 0.4, 0, pitch=1.2); a(s[4] + 0.1, 'coin', 0.3)
        a(s[5], 'thud', 0.55); a(s[6], 'whoosh', 0.3); a(s[6] + 0.1, 'riser', 0.25, dur=3.0)
        a(s[8], 'stamp', 0.6); a(s[9], 'stamp', 0.5, 0, ); a(s[10], 'whoosh', 0.3); a(s[10] + 0.1, 'riser', 0.25, dur=4.6); a(s[12], 'stamp', 0.6)
        a(s[13] - 0.1, 'whoosh', 0.35); a(s[13], 'riser', 0.35, dur=s[15] - s[13] - 0.4); a(s[14] + 2.6, 'cash', 0.5); a(s[16], 'pop', 0.4)
        a(s[17] - 0.1, 'whoosh', 0.35); a(s[17], 'pop', 0.45); a(s[18], 'stamp', 0.6); a(s[18] + 0.1, 'chime', 0.5)
        a(s[19] - 0.1, 'whoosh', 0.3); a(s[20], 'thud', 0.5); a(s[20] + 0.05, 'sparkle', 0.45); a(s[21] + 0.5, 'ding', 0.4)
        a(s[22] - 0.1, 'whoosh', 0.3); a(s[22], 'pop', 0.4); a(s[24], 'pop', 0.55); a(s[24] + 0.3, 'dinghi', 0.4)
    if i == 2:
        a(0.05, 'pop', 0.5); a(0.2, 'alarm', 0.14, 0.3, dur=1.4); a(1.6, 'poof', 0.5)
        a(s[1] - 0.1, 'whoosh', 0.3); a(s[1], 'pop', 0.45); a(s[2] + 0.4, 'poof', 0.55); a(s[2] + 0.1, 'stamp', 0.55)
        a(s[3], 'pop', 0.45); a(s[3] + 0.1, 'ding', 0.4)
        a(s[4] - 0.1, 'whooshS', 0.3)
        for k in range(3): a(s[4] + k * 0.8, 'pop', 0.4, -0.4 + k * 0.4, pitch=1 + k * 0.1)
        a(s[5] - 0.1, 'whoosh', 0.3); a(s[5], 'pop', 0.4); a(s[5] + 0.4, 'buzzer', 0.2); a(s[6], 'stamp', 0.6); a(s[7], 'pop', 0.4); a(s[7] + 0.1, 'cash', 0.5)
        a(s[8] - 0.1, 'whoosh', 0.3); a(s[8], 'pop', 0.4)
        for k in range(3):
            t = s[8] + k * 0.4 + 1.0
            while t < s[10] - 0.2: a(t, 'coin', 0.22, -0.2); t += 1.2
        a(s[9], 'pop', 0.45, 0.4)
        a(s[10] - 0.1, 'whoosh', 0.3); a(s[10], 'pop', 0.45); a(s[11] - 0.1, 'riser', 0.3, dur=1.1); a(s[11] + 1.0, 'cash', 0.55); a(s[12], 'pop', 0.45); a(s[12] + 0.1, 'sparkle', 0.4)
        a(s[13] - 0.1, 'whoosh', 0.3)
        for k in range(3): a(s[13] + 0.1 + k * 0.15, 'tick', 0.4)
        a(s[13] + 1.0, 'pop', 0.55); a(s[13] + 1.3, 'dinghi', 0.4)
    if i == 3:
        a(0.05, 'pop', 0.5); a(0.6, 'whooshS', 0.35); a(0.8, 'sparkle', 0.5)
        for k in range(9): a(0.85 + k * 0.06, 'coin', 0.1, -0.6 + k * 0.15)
        a(s[1], 'stamp', 0.6); a(s[2] - 0.1, 'whoosh', 0.35); a(s[2], 'thud', 0.5)
        a(s[3] - 0.1, 'whoosh', 0.3); a(s[3], 'pop', 0.4)
        t = s[3] + 1.2
        while t < s[8]: a(t, 'coin', 0.16, -0.4); t += 0.8
        a(s[4], 'ding', 0.45, -0.4); a(s[5], 'pop', 0.4, 0.4); a(s[6], 'cash', 0.5, 0.4)
        t = s[6] + 0.8
        while t < s[8]: a(t, 'coin', 0.16, 0.4); t += 0.8
        a(s[7], 'sparkle', 0.45, 0.4); a(s[8] - 0.05, 'thud', 0.5); a(s[8], 'chime', 0.5)
        a(s[9] - 0.1, 'whoosh', 0.3); a(s[9], 'buzzer', 0.4); a(s[10] + 0.1, 'riser', 0.35, dur=s[11] - s[10] - 0.8); a(s[11] - 0.6, 'cash', 0.55)
        a(s[11] - 0.1, 'whoosh', 0.3); a(s[11], 'pop', 0.4); a(s[12], 'pop', 0.45, 0.3, pitch=1.2)
        a(s[13], 'tick', 0.5, 0.3); a(s[13] + 0.05, 'dinghi', 0.4, 0.3); a(s[13] + 0.1, 'sparkle', 0.4)
        a(s[14], 'pop', 0.55); a(s[14] + 0.3, 'dinghi', 0.4)
    if i == 4:
        for k in range(12): a(0.05 + k * 0.1, 'tick', 0.15)
        a(s[1], 'thud', 0.45); a(s[2] - 0.1, 'whoosh', 0.3)
        t = s[2] + 0.4
        while t < s[6]: a(t, 'coin', 0.12, 0.4); t += 0.6 if t < s[4] else 0.32
        a(s[3], 'riser', 0.3, dur=s[6] - s[3] - 0.2); a(s[5] + 2.5, 'stamp', 0.6)
        for k in range(3): a(s[6 + k], 'whooshS', 0.3)
        a(s[9], 'thud', 0.5); a(s[10], 'pop', 0.45); a(s[11], 'whooshS', 0.25); a(s[11] + 0.9, 'thud', 0.45); a(s[11] + 1.0, 'pop', 0.4)
        a(s[12] - 0.1, 'whoosh', 0.3); a(s[13], 'stamp', 0.6)
        a(s[14], 'pop', 0.45); a(s[14] + 0.7, 'buzzer', 0.4)
        a(s[15], 'thud', 0.55); a(s[16] - 0.1, 'whoosh', 0.3); a(s[16], 'pop', 0.45); a(s[16] + 1.0, 'pop', 0.55); a(s[16] + 1.3, 'dinghi', 0.4)
    return ev

for i in (int(sys.argv[1]),) if len(sys.argv) > 1 else (1, 2, 3):
    total = ENDS[i] + 1.2
    mix = np.zeros((int((total + 1) * SR), 2))
    for t, name, g, pan, kw in events(i):
        if name == 'riser': x = riser(max(0.4, kw['dur']))
        elif name == 'alarm': x = alarm(kw['dur'])
        else:
            x = LIB[name]
            if 'pitch' in kw: x = resample(x, kw['pitch'])
        s0 = int(max(0, t) * SR); x = x[:len(mix) - s0] * g
        l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        mix[s0:s0 + len(x), 0] += x * l * 1.4; mix[s0:s0 + len(x), 1] += x * r * 1.4
    mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.89
    with wave.open(f'/tmp/claude-0/-home-user-Adeel-Zubairi/a5d9cfe7-fb74-56f3-913e-57d93760c98f/scratchpad/shorts/sfx{i}.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
    print('short', i, len(events(i)), 'sfx events')
