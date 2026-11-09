"""Low-level SFX + music bed for the Fed long video. Usage: python3 fed_sfx.py sync.json out.wav"""
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
CHAP = [16, 22, 31, 32, 39, 47, 51, 61, 67, 73, 81]
HITS = [fr(3, .15), s[6] + .05] + [s[i] for i in [16, 22, 32, 39, 47, 51, 61, 73, 81]] + [fr(67, .3)]
a(0.0, 'sub', 0.5); a(0.05, 'shutter', 0.3)
for i in range(1, len(s)):
    if i in CHAP: continue
    a(s[i] - 0.12, 'whooshD', 0.16, (-1) ** i * 0.3)
for t in HITS: a(t - 1.1, 'swell', 0.22); a(t, 'impact', 0.42)
for i in range(len(s)):  # card/chip pops
    if i in CHAP or i in (0, 3, 6, 81, 86): continue
    a(s[i] + 0.35, 'poppro', 0.16, 0.2 * math.sin(i)); a(fr(i, .45), 'poppro', 0.12, -0.2 * math.sin(i))
for i in (2, 14, 34, 41, 43, 55, 56, 23):  # counters
    for k in range(10): a(s[i] + 0.4 + k * 0.12, 'tickhi', 0.07)
for i in (51, 52, 55, 59): a(fr(i, .5), 'cashpro', 0.22)
for i in range(74, 81): a(s[i] + 0.1, 'dingpro', 0.18)
a(fr(38, .1), 'buzzer', 0.15); a(fr(78, .2), 'dingpro', 0.25)
a(fr(84, .3), 'poppro', 0.3); a(fr(85, .3), 'dingpro', 0.3)
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
