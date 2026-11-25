"""SFX track for the GTA 6 vs minimum wage Short. Usage: python3 sales_sfx.py sync.json out.wav"""
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
a(0.0, 'impact', 0.9); a(0.0, 'sub', 0.8); a(0.05, 'poppro', 0.4)
for k in range(12): a(0.3 + k * 0.1, 'tickhi', 0.14 + k * 0.015)
a(1.55, 'cashpro', 0.5); a(1.6, 'impact', 0.6)
for i in range(1, len(s)): a(s[i] - 0.15, 'whooshD', 0.45, (-1) ** i * 0.4); a(s[i], 'impact', 0.5)
for k in range(11): a(s[1] + 0.25 + k * 0.1, 'tickhi', 0.11)
a(s[1] + 1.25, 'cashpro', 0.45); a(s[1] + 1.2, 'stamp', 0.35)
for k, t in enumerate((0, 0.5, 1.0)): a(s[2] + t, 'poppro', 0.35, (k - 1) * 0.4)
a(s[2] + 0.4, 'impact', 0.4); a(s[2] + 1.4, 'buzzer', 0.3)
for k in range(13): a(s[3] + 0.9 + k * 0.1, 'tickhi', 0.11)
a(s[3] + 2.2, 'dingpro', 0.4)
for k in range(12): a(s[4] + 1.2 + k * 0.1, 'tickhi', 0.11)
a(s[4] + 2.4, 'buzzer', 0.3)
a(s[5] + 0.1, 'poppro', 0.35); a(s[5] + 0.0 + 0.8 - 0.9, 'swell', 0.35); a(s[5] + 0.8, 'impact', 0.75); a(s[5] + 0.85, 'cashpro', 0.45)
a(s[6] + 0.3, 'cashpro', 0.45); a(s[6] + 1.4, 'dingpro', 0.45)
for k in range(8): a(s[6] + 2.0 + k * 0.5, 'cashpro', 0.12)
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
