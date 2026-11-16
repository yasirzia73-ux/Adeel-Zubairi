"""SFX for the text-only viral Shorts. Usage: python3 viral_sfx.py <id> <out.wav>"""
import sys, math, wave, json
import numpy as np
sys.path.insert(0, '/home/user/Adeel-Zubairi/video/sfx')
import sfx_pro as P
src = open('/home/user/Adeel-Zubairi/video/sfx/make_sfx.py').read()
exec(src[:src.index('# ---------- events ----------')])
SR = P.SR; ALL = dict(LIB); ALL.update({k: f() for k, f in P.LIB_FN.items()})
def resample(x, r): idx = np.arange(0, len(x) - 1, r); return np.interp(idx, np.arange(len(x)), x)
rid, out = sys.argv[1], sys.argv[2]; ev = []
def a(t, n, g=0.5, pan=0.0, pitch=1.0): ev.append((t, n, g, pan, pitch))
if rid == 'mrbeast':
    total = 19.5
    a(0.0, 'impact', 0.7); a(0.05, 'shutter', 0.45)
    for k in range(14): a(0.1 + k * 0.1, 'tickhi', 0.2, 0, 1 + k * 0.03)
    a(1.6, 'impact', 0.8); a(1.65, 'cashpro', 0.6); a(2.2, 'dingpro', 0.4)
    for k in range(4): a(3.3 + k * 1.4, 'poppro', 0.5, (k % 2) * 0.6 - 0.3, 1 + k * 0.1); a(3.35 + k * 1.4, 'coin', 0.3)
    a(9.0, 'swell', 0.45); a(9.4, 'impact', 0.7)
    t = 9.5
    while t < 19.3: a(t, 'coin', 0.18, ((int(t * 10) % 5) - 2) * 0.25); t += 0.42
    a(16.2, 'poppro', 0.5); a(16.25, 'dingpro', 0.4)
elif rid == 'top5':
    total = 24.5
    a(0.0, 'impact', 0.7); a(0.05, 'whooshD', 0.4); a(0.5, 'stamp', 0.5); a(1.3, 'poppro', 0.5); a(2.4, 'swell', 0.4)
    for k, t0 in enumerate([3.0, 6.2, 9.4, 12.6]):
        a(t0 - 0.1, 'whooshD', 0.4); a(t0, 'shutter', 0.45); a(t0 + 0.15, 'stamp', 0.45)
        for j in range(8): a(t0 + 0.1 + j * 0.1, 'tickhi', 0.15)
        a(t0 + 0.95, 'cashpro', 0.35)
    a(15.0, 'heart', 0.5); a(15.4, 'swell', 0.5); a(15.8, 'impact', 0.95); a(15.85, 'glitch', 0.35)
    for j in range(16): a(15.9 + j * 0.1, 'tickhi', 0.15 + j * 0.01)
    a(17.4, 'impact', 0.7); a(17.45, 'confetti', 0.6); a(17.5, 'cashpro', 0.6)
    a(20.0, 'whooshD', 0.45); a(20.2, 'impact', 0.6); a(21.4, 'dingpro', 0.45)
elif rid == 'ytpay':
    total = 17.5
    a(0.0, 'impact', 0.6); a(0.05, 'poppro', 0.5)
    for k in range(16): a(0.1 + k * 0.1, 'tickhi', 0.2, 0, 1 + k * 0.03)
    a(1.5, 'impact', 0.7); a(1.55, 'glitch', 0.35); a(2.0, 'heart', 0.5); a(2.6, 'swell', 0.4)
    a(3.0, 'whooshD', 0.4); a(3.05, 'poppro', 0.5); a(3.2, 'coin', 0.4)
    a(5.6, 'whooshD', 0.4); a(5.65, 'poppro', 0.5); a(5.8, 'cashpro', 0.55)
    a(8.0, 'swell', 0.45); a(8.6, 'impact', 0.85); a(8.65, 'rewind', 0.45); a(9.4, 'stamp', 0.6); a(9.45, 'buzzer', 0.3)
    a(12.2, 'poppro', 0.45); a(14.4, 'poppro', 0.5); a(14.45, 'dingpro', 0.4)
elif rid == 'penny':
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
if len(sys.argv) > 3:   # optional warp file: map visual-time events onto the voiceover timeline
    W = json.load(open(sys.argv[3]))[rid]; vo = [a for a, b in W]; vis = [b for a, b in W]
    ev = [(float(np.interp(t, vis, vo)), n, g, pan, pitch) for t, n, g, pan, pitch in ev]; total = vo[-1]
mix = np.zeros((int((total + 1) * SR), 2))
for t, n, g, pan, pitch in ev:
    x = ALL[n]; x = resample(x, pitch) if pitch != 1.0 else x; x = x * g; s0 = int(max(0, t) * SR); x = x[:len(mix) - s0]
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    mix[s0:s0 + len(x), 0] += x * l * 1.4; mix[s0:s0 + len(x), 1] += x * r * 1.4
mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.89
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print(rid, len(ev), 'events')
