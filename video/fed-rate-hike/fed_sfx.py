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
HITS = [s[i] for i in [16, 22, 32, 39, 47, 51, 61, 73, 81]] + [fr(67, .3)]
# ---- HOOK (paragraphs 0-6): cinematic, louder than the rest ----
a(0.0, 'impact', 0.9); a(0.0, 'sub', 0.8); a(0.02, 'glitch', 0.45)
a(s[0] + 0.6, 'stamp', 0.75)                                   # DEC 9 calendar slam
for k in range(12): a(s[0] + 2.2 + k * 0.08, 'poppro', 0.32, -0.6 + k * 0.1)   # 12 people pop in
for k in range(3): a(s[1] + k * 0.9, 'poppro', 0.5, (k - 1) * 0.5); a(s[1] + k * 0.9 + 0.02, 'shutter', 0.25)
for k in range(16): a(s[2] + 0.4 + k * 0.1, 'tickhi', 0.16 + k * 0.012)        # gauge climbing
a(s[2] + 2.0, 'impact', 0.7); a(s[2] + 2.05, 'heart', 0.5); a(s[2] + 2.9, 'heart', 0.45)
a(s[3] + 0.45, 'whooshD', 0.5); a(s[3] + 0.55, 'shutter', 0.45)               # strike through "NOT CHEAPER"
a(s[3] + 0.7, 'rewind', 0.55); a(s[3] + 0.9, 'impact', 0.95); a(s[3] + 0.92, 'glitch', 0.4)  # record scratch -> MORE EXPENSIVE
a(s[4] + 0.3, 'buzzer', 0.35); a(fr(4, .3), 'dingpro', 0.45); a(fr(4, .55) - 0.8, 'swell', 0.4); a(fr(4, .55), 'sub', 0.55)
for k in range(3): a(s[5] + 0.2 + k * 0.4, 'poppro', 0.4, (k - 1) * 0.5)
a(fr(5, .45), 'whooshD', 0.4); a(fr(5, .6), 'dingpro', 0.4)
a(s[6] - 1.4, 'swell', 0.6); a(s[6] + 0.05, 'impact', 1.0); a(s[6] + 0.4, 'cashpro', 0.45)  # "AGAIN." -> beat drop
for i in range(1, len(s)):
    if i in CHAP or i <= 6: continue
    a(s[i] - 0.12, 'whooshD', 0.16, (-1) ** i * 0.3)
for t in HITS: a(t - 1.1, 'swell', 0.22); a(t, 'impact', 0.42)
for i in CHAP: a(s[i] - 0.35, 'whooshD', 0.3, 0.4)
for i in range(len(s)):  # card/chip pops
    if i in CHAP or i <= 6 or i in (81, 86): continue
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
