"""SFX track for the GTA 6 sales Short. Usage: python3 sales_sfx.py sync.json out.wav"""
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
a(0.0, 'impact', 0.9); a(0.0, 'sub', 0.8); a(0.02, 'glitch', 0.4)
for k in range(20): a(s[0] + 0.3 + k * 0.11, 'tickhi', 0.14 + k * 0.01)
a(s[0] + 2.5, 'impact', 0.8); a(s[0] + 2.55, 'cashpro', 0.5); a(fr(0, .62), 'poppro', 0.45)
for i in range(1, len(s)): a(s[i] - 0.12, 'whooshD', 0.22, (-1) ** i * 0.3)
a(fr(1, .15), 'stamp', 0.6); a(fr(1, .35), 'poppro', 0.3); a(fr(1, .78) - 1.0, 'swell', 0.3); a(fr(1, .78), 'impact', 0.6)
a(s[2] + 0.2, 'poppro', 0.3); a(fr(2, .45), 'swell', 0.25); a(fr(2, .8), 'impact', 0.5); a(fr(2, .8) + 0.05, 'cashpro', 0.35)
for k in range(18): a(s[3] + 0.2 + k * 0.12, 'tickhi', 0.09)
a(fr(3, .55), 'stamp', 0.5)
a(s[4] + 0.1, 'poppro', 0.3); a(fr(4, .3), 'swell', 0.35)
a(s[5] - 0.05, 'rewind', 0.5); a(s[5] + 0.05, 'impact', 0.85); a(s[5] + 0.1, 'stamp', 0.6); a(fr(5, .35), 'whooshD', 0.4); a(fr(5, .5), 'buzzer', 0.3)
a(fr(6, .25), 'poppro', 0.3); a(fr(6, .32), 'dingpro', 0.3); a(fr(6, .5), 'whooshD', 0.35); a(fr(6, .55), 'impact', 0.45); a(fr(6, .88), 'stamp', 0.55); a(fr(6, .88) + 0.05, 'heart', 0.4)
a(fr(7, .05), 'dingpro', 0.3); a(fr(7, .4), 'buzzer', 0.2); a(fr(7, .78), 'poppro', 0.3)
a(fr(8, .2), 'poppro', 0.4); a(fr(8, .3), 'poppro', 0.4); a(fr(8, .6), 'dingpro', 0.35)
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
