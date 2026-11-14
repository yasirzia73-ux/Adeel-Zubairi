"""SFX for the text-only viral Shorts. Usage: python3 viral_sfx.py <id> <out.wav>"""
import sys, math, wave
import numpy as np
sys.path.insert(0, '/home/user/Adeel-Zubairi/video/sfx')
import sfx_pro as P
src = open('/home/user/Adeel-Zubairi/video/sfx/make_sfx.py').read()
exec(src[:src.index('# ---------- events ----------')])
SR = P.SR; ALL = dict(LIB); ALL.update({k: f() for k, f in P.LIB_FN.items()})
def resample(x, r): idx = np.arange(0, len(x) - 1, r); return np.interp(idx, np.arange(len(x)), x)
rid, out = sys.argv[1], sys.argv[2]; ev = []
def a(t, n, g=0.5, pan=0.0, pitch=1.0): ev.append((t, n, g, pan, pitch))
if rid == 'penny':
    total = 19.5
    a(0.0, 'impact', 0.6); a(0.05, 'whooshD', 0.4); a(0.45, 'poppro', 0.5, -0.4); a(0.95, 'poppro', 0.5, 0.4, 1.2); a(1.0, 'glitch', 0.25)
    a(1.4, 'heart', 0.5); a(2.0, 'heart', 0.45); a(2.5, 'swell', 0.35)
    a(2.8, 'impact', 0.55)
    for d in range(2, 21): a(2.6 + 5 * (d - 1) / 19, 'tickhi', 0.25, 0, 1 + d * 0.03)        # days 1-20 fast ticks
    for d in range(21, 31):                                                                     # days 21-30: a hit each, rising pitch
        t = 7.6 + (d - 20) * 0.8 - 0.8 + 0.8 - 0.8
        a(t, 'poppro', 0.45 + (d - 21) * 0.03, 0, 0.8 + (d - 21) * 0.06); a(t, 'coin', 0.25 + (d - 21) * 0.03)
    a(7.6 + 8 * 0.8, 'impact', 0.8); a(7.6 + 8 * 0.8 + 0.05, 'cashpro', 0.6)                   # passes $1M
    a(15.0, 'swell', 0.45); a(15.6, 'impact', 0.9); a(15.62, 'confetti', 0.6); a(15.7, 'cashpro', 0.6); a(15.9, 'dingpro', 0.5)
else:
    total = 15.5
    a(0.0, 'impact', 0.6); a(0.05, 'shutter', 0.45); a(0.15, 'stamp', 0.55); a(1.0, 'whooshD', 0.4); a(1.0, 'poppro', 0.4)
    a(1.6, 'heart', 0.5); a(2.3, 'heart', 0.45); a(2.8, 'swell', 0.4); a(3.4, 'impact', 0.6)
    k, t = 0, 3.4
    while t < 11.6: a(t, 'tickhi', 0.22 + 0.15 * (t - 3.4) / 8.2, 0, 1 + 0.4 * (t - 3.4) / 8.2); t += max(0.07, 0.22 - 0.02 * k); k += 1
    a(3.4 + 8.2 * 0.08, 'buzzer', 0.25)
    a(10.6, 'swell', 0.5); a(11.6, 'impact', 0.9); a(11.62, 'glitch', 0.35); a(12.0, 'stamp', 0.6); a(12.05, 'buzzer', 0.3); a(13.0, 'poppro', 0.5); a(13.05, 'dingpro', 0.4)
mix = np.zeros((int((total + 1) * SR), 2))
for t, n, g, pan, pitch in ev:
    x = ALL[n]; x = resample(x, pitch) if pitch != 1.0 else x; x = x * g; s0 = int(max(0, t) * SR); x = x[:len(mix) - s0]
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    mix[s0:s0 + len(x), 0] += x * l * 1.4; mix[s0:s0 + len(x), 1] += x * r * 1.4
mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.89
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print(rid, len(ev), 'events')
