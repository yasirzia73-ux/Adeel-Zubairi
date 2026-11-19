"""SFX track for the GTA 6 long video. Usage: python3 gta_sfx.py sync.json out.wav"""
import json, math, sys, wave
import numpy as np
sys.path.insert(0, '/home/user/Adeel-Zubairi/video/sfx')
import sfx_pro as P
src = open('/home/user/Adeel-Zubairi/video/sfx/make_sfx.py').read()
exec(src[:src.index('# ---------- events ----------')])
SR = P.SR
ALL = dict(LIB); ALL.update({k: f() for k, f in P.LIB_FN.items()})
sync = json.load(open(sys.argv[1])); out = sys.argv[2]
s = [l['start'] for l in sync['lines']]; e = [l['end'] for l in sync['lines']]; total = sync['total']
du = lambda i: max(1, e[i] - s[i]); fr = lambda i, f: s[i] + du(i) * f
ev = []
def a(t, n, g=0.4, pan=0.0): ev.append((t, n, g, pan))
CHAP = [4, 8, 13, 17, 22, 27, 33, 39, 43]
CHS = [8, 17, 22, 27, 39]   # full chapter title cards
HITS = [s[1] + 1.75, fr(20, .55)] + [s[i] for i in CHS] + [s[i] for i in (4, 13, 33, 43)]
# ---- hook ----
a(0.0, 'impact', 0.9); a(0.0, 'sub', 0.8); a(0.02, 'glitch', 0.4)
a(0.2, 'poppro', 0.4); a(0.5, 'whooshD', 0.45); a(fr(0, .35), 'impact', 0.6); a(fr(0, .62), 'poppro', 0.35)
for k in range(17): a(s[1] + 0.05 + k * 0.1, 'tickhi', 0.14 + k * 0.012)
a(s[1] + 1.75, 'impact', 0.85); a(s[1] + 1.8, 'cashpro', 0.5)
for k in range(7): a(fr(1, .5) + k * 0.08, 'poppro', 0.3, -0.6 + k * 0.2)
a(fr(2, .05), 'poppro', 0.35); a(fr(2, .45), 'poppro', 0.35); a(fr(2, .5), 'stamp', 0.55)
for k in range(4): a(fr(3, .05 + k * .14), 'poppro', 0.3, (k - 1.5) * 0.3)
a(fr(3, .78) - 0.9, 'swell', 0.35); a(fr(3, .78), 'stamp', 0.6); a(fr(3, .78) + 0.05, 'heart', 0.45)
# ---- generic per-paragraph whoosh + pops ----
for i in range(4, len(s)):
    if i in CHAP: continue
    a(s[i] - 0.12, 'whooshD', 0.16, (-1) ** i * 0.3)
    if i not in (46,): a(s[i] + 0.35, 'poppro', 0.14, 0.2 * math.sin(i)); a(fr(i, .45), 'poppro', 0.11, -0.2 * math.sin(i))
for t in HITS: a(t - 1.1, 'swell', 0.22); a(t, 'impact', 0.45)
for i in CHAP: a(s[i] - 0.35, 'whooshD', 0.32, 0.4)
# ---- specific moments ----
a(fr(5, .18), 'stamp', 0.4); a(fr(5, .4), 'stamp', 0.4); a(fr(5, .6), 'dingpro', 0.4)
for i, o, d in ((6, .45, 2.2), (9, .35, 1.6), (18, .05, 1.6), (21, .1, 1.5), (26, .25, 2.0), (35, .1, 1.4), (40, .25, 2.5)):
    t0 = s[i] + (du(i) * o if o > .2 else 0.3)
    for k in range(int(d / 0.12)): a(t0 + k * 0.12, 'tickhi', 0.07)
a(fr(7, .45), 'heart', 0.4); a(fr(10, .7), 'stamp', 0.4); a(fr(12, .3), 'buzzer', 0.2); a(fr(12, .65), 'dingpro', 0.3)
for k in range(6): a(s[14] + 0.1 + k * 0.12, 'buzzer', 0.06, (k - 2.5) * 0.3)
a(fr(15, .85), 'dingpro', 0.35); a(fr(18, .72), 'stamp', 0.55); a(fr(18, .74), 'cashpro', 0.35)
a(fr(20, .55), 'stamp', 0.6); a(fr(21, .8), 'dingpro', 0.35); a(fr(23, .6), 'dingpro', 0.3)
a(fr(26, .82), 'stamp', 0.5); a(fr(26, .84), 'cashpro', 0.4)
for k in range(6): a(s[30] + du(30) * 0.4 + k * 0.5, 'cashpro', 0.12)
a(fr(31, .7), 'cashpro', 0.3); a(fr(34, .8), 'dingpro', 0.3)
a(fr(36, .05), 'stamp', 0.55); a(fr(36, .3), 'heart', 0.45); a(fr(36, .7), 'buzzer', 0.18)
a(fr(37, .55), 'rewind', 0.35); a(fr(37, .58), 'impact', 0.4)
a(fr(38, .1), 'buzzer', 0.15); a(fr(38, .8), 'dingpro', 0.3); a(fr(40, .8), 'dingpro', 0.35)
for k in range(5): a(fr(41, .04 + k * .07), 'cashpro', 0.14)
a(fr(41, .6), 'dingpro', 0.35); a(fr(45, .1), 'poppro', 0.35); a(fr(46, .2), 'poppro', 0.3); a(fr(46, .3), 'dingpro', 0.3)
mix = np.zeros((int((total + 2) * SR), 2))
for t, n, g, pan in ev:
    x = ALL[n] * g; s0 = int(max(0, t) * SR); x = x[:len(mix) - s0]
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    mix[s0:s0 + len(x), 0] += x * l * 1.4; mix[s0:s0 + len(x), 1] += x * r * 1.4
mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.89
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
bed = P.bed(total + 2); f = int(2 * SR); bed[-f:] *= np.linspace(1, 0, f); bed[:f] *= np.linspace(0, 1, f)
with wave.open(out.replace('.wav', '_bed.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((bed * 0.89 * 32767).astype('<i2').tobytes())
print(len(ev), 'events')
