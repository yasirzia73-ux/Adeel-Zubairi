"""SFX track for the Black Friday BNPL Short. Usage: python3 sales_sfx.py sync.json out.wav"""
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
a(0.0, 'impact', 0.85); a(0.0, 'sub', 0.75); a(0.05, 'poppro', 0.4)
for k in range(20): a(s[0] + 0.4 + k * 0.11, 'tickhi', 0.13 + k * 0.01)
a(s[0] + 2.65, 'impact', 0.75); a(s[0] + 2.7, 'cashpro', 0.5); a(fr(0, .55), 'poppro', 0.4)
for i in range(1, len(s)): a(s[i] - 0.12, 'whooshD', 0.22, (-1) ** i * 0.3)
for k in range(12): a(s[1] + 0.1 + k * 0.12, 'tickhi', 0.1)
a(fr(1, .65), 'stamp', 0.6); a(fr(1, .67), 'heart', 0.4)
a(fr(2, .02), 'poppro', 0.35)
for k in range(4): a(fr(2, .3 + k * .07), 'poppro', 0.3, (k - 1.5) * 0.3)
a(fr(2, .6), 'dingpro', 0.35); a(fr(2, .82), 'swell', 0.25)
a(fr(3, .02), 'stamp', 0.5); a(fr(3, .42), 'rewind', 0.3); a(fr(3, .42), 'impact', 0.45)
for k in range(4): a(fr(3, .45) + k * 0.08, 'cashpro', 0.18, (k - 1.5) * 0.3)
a(fr(3, .72), 'dingpro', 0.35)
for f in (.05, .15, .25, .55, .63, .71): a(fr(4, f), 'poppro', 0.22)
a(fr(4, .82), 'buzzer', 0.3)
a(st(5) if False else s[5] + 0.05, 'impact', 0.7); a(fr(5, .05), 'stamp', 0.55); a(fr(5, .55), 'buzzer', 0.25)
a(s[6] + 0.05, 'dingpro', 0.35); a(fr(6, .1), 'poppro', 0.3); a(fr(6, .5) - 0.9, 'swell', 0.3); a(fr(6, .5), 'impact', 0.6)
for k in range(10): a(fr(7, .3) + k * 0.13, 'tickhi', 0.1)
a(fr(7, .5), 'dingpro', 0.4); a(fr(8, .02), 'poppro', 0.35); a(fr(8, .45), 'poppro', 0.3); a(fr(8, .65), 'dingpro', 0.35)
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
