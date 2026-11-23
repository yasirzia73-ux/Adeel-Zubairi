"""SFX track for the Thanksgiving cost Short. Usage: python3 sales_sfx.py sync.json out.wav"""
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
a(0.0, 'impact', 0.85); a(0.0, 'sub', 0.7); a(0.05, 'poppro', 0.4)
for k in range(5): a(s[0] + 0.3 + k * 0.12, 'poppro', 0.25, (k - 2) * 0.3)
for k in range(20): a(s[0] + 0.35 + k * 0.12, 'tickhi', 0.12 + k * 0.01)
a(s[0] + 2.7, 'impact', 0.7); a(s[0] + 2.75, 'cashpro', 0.45); a(fr(0, .5), 'poppro', 0.3)
for i in range(1, len(s)): a(s[i] - 0.12, 'whooshD', 0.22, (-1) ** i * 0.3)
a(fr(1, .4) - 0.9, 'swell', 0.3); a(fr(1, .4), 'impact', 0.6)
a(fr(2, .05), 'stamp', 0.6); a(fr(2, .07), 'heart', 0.45); a(fr(2, .3), 'poppro', 0.3)
for k in range(13): a(fr(2, .4) + k * 0.12, 'tickhi', 0.1)
a(fr(2, .8), 'buzzer', 0.3)
a(fr(3, .1), 'poppro', 0.25); a(fr(3, .35), 'poppro', 0.25); a(fr(3, .7), 'dingpro', 0.4); a(fr(3, .7), 'impact', 0.4)
a(fr(4, .25), 'poppro', 0.3); a(fr(4, .6), 'poppro', 0.3)
for k in range(3): a(fr(5, .05 + k * .12), 'poppro', 0.3, (k - 1) * 0.4)
for k in range(12): a(fr(5, .55) + k * 0.12, 'tickhi', 0.1)
a(fr(5, .55) + 1.45, 'buzzer', 0.25)
a(fr(6, .02), 'poppro', 0.3); a(fr(6, .3), 'rewind', 0.3); a(fr(6, .3), 'stamp', 0.35); a(fr(6, .62) - 0.8, 'swell', 0.3); a(fr(6, .62), 'stamp', 0.6); a(fr(6, .64), 'cashpro', 0.4)
a(fr(7, .02), 'stamp', 0.5)
for f in (.1, .25, .4): a(fr(7, f), 'poppro', 0.3)
for k in range(5): a(fr(7, .55) + k * 0.1, 'cashpro', 0.15, (k - 2) * 0.3)
a(s[8] + 0.1, 'dingpro', 0.35); a(fr(8, .45), 'dingpro', 0.35)
a(fr(9, .02), 'poppro', 0.35); a(fr(9, .4), 'poppro', 0.3); a(fr(9, .6), 'dingpro', 0.35)
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
