"""SFX + subtle music bed for the v2 Reels. Usage: python3 reel_sfx.py <id> <sync.json> <out.wav>
sync.json: {"lines":[{"start":..,"end":..},...], "total":..}"""
import json, math, sys, wave
import numpy as np
sys.path.insert(0, '/home/user/Adeel-Zubairi/video/sfx')
import sfx_pro as P
src = open('/home/user/Adeel-Zubairi/video/sfx/make_sfx.py').read()
exec(src[:src.index('# ---------- events ----------')])  # old LIB: pop, coin, stamp, buzzer, rewind, ...
SR = P.SR
def resample(x, r):
    if r == 1: return x
    idx = np.arange(0, len(x) - 1, r); return np.interp(idx, np.arange(len(x)), x)
ALL = dict(LIB); ALL.update({k: f() for k, f in P.LIB_FN.items()})

def events(rid, s, e):
    ev = []
    def a(t, n, g=0.5, pan=0.0, **kw): ev.append((t, n, g, pan, kw))
    if rid == 'trump':
        a(0.0, 'impact', 0.75); a(0.02, 'glitch', 0.35)
        a(s[0] + 0.9, 'stamp', 0.55, -0.3); a(s[0] + 1.7, 'stamp', 0.55, 0.3)
        a(s[1] - 0.1, 'whooshD', 0.4); a(s[1] + 0.9, 'confetti', 0.5); a(s[1] + 1.0, 'cashpro', 0.35)
        a(s[2] - 0.1, 'whooshD', 0.35); a(s[2], 'poppro', 0.4, -0.3); a(s[2] + 0.6, 'poppro', 0.4, 0.3, pitch=1.2)
        a(s[3] - 1.45, 'swell', 0.45); a(s[3] + 0.15, 'impact', 0.7)
        for i in range(16): a(s[3] + 0.2 + i * 0.1, 'tickhi', 0.18)
        a(s[4], 'poppro', 0.45); a(s[4] + 0.6, 'dingpro', 0.4)
        a(s[5] - 0.1, 'whooshD', 0.35)
        for i in range(14): a(s[5] + i * 0.16, 'tickhi', 0.16, (-1) ** i * 0.3)
        a(s[5] + 2.2, 'stamp', 0.6)
        a(s[6] - 0.1, 'whooshD', 0.35); a(s[6], 'shutter', 0.45, -0.4); a(s[6] + 0.15, 'shutter', 0.45, 0.4); a(s[6] + 2.0, 'poppro', 0.4)
        a(s[7], 'shutter', 0.5); a(s[7] + 1.0, 'poppro', 0.45); a(s[7] + 2.0, 'tickhi', 0.3)
        a(s[8] - 0.1, 'whooshD', 0.35); a(s[8] + 0.5, 'sub', 0.6); a(s[8] + 1.8, 'poppro', 0.4)
        a(s[9], 'heart', 0.5); a(s[9] + 0.95, 'heart', 0.4)
        for i in range(3): a(s[9] + 1.2 + i * 0.6, 'poppro', 0.4, 0, pitch=0.9 + i * 0.15)
        a(s[10] - 0.1, 'whooshD', 0.35); a(s[10] + 0.2, 'poppro', 0.55); a(s[10] + 0.5, 'dingpro', 0.45)
    if rid == 'musk':
        a(0.0, 'impact', 0.75)
        for i in range(18): a(0.3 + i * 0.11, 'tickhi', 0.15)
        for i in range(6): a(0.4 + i * 0.5, 'coin', 0.18, -0.6 + i * 0.25)
        a(s[1] + 0.1, 'glitch', 0.45); a(s[1] + 0.2, 'impact', 0.8); a(s[1] + 0.9, 'heart', 0.45)
        a(s[2], 'rewind', 0.45)
        for i in range(7): a(s[3] + 0.3 + i * 0.35, 'coin', 0.2, -0.3 + i * 0.1)
        a(s[4], 'shutter', 0.45); a(s[4] + 1.0, 'stamp', 0.6)
        a(s[5] - 0.1, 'whooshD', 0.35); a(s[5] + 1.2, 'poppro', 0.45, -0.4); a(s[5] + 1.6, 'poppro', 0.45, 0.4); a(s[5] + 1.7, 'buzzer', 0.25)
        a(s[6] + 0.9, 'swell', 0.3); a(s[6] + 2.6, 'sub', 0.55)
        for i in range(70): a(s[7] + 0.4 + i * 0.02, 'tickhi', 0.06, (i % 10 - 5) / 6)
        a(s[7] + 0.3, 'impact', 0.55)
        a(s[8] - 0.1, 'whooshD', 0.35); a(s[8] + 0.3, 'swell', 0.25); a(s[8] + 1.5, 'dingpro', 0.45)
        a(s[9], 'shutter', 0.45); a(s[9] + 0.8, 'poppro', 0.45)
        a(s[10] - 0.1, 'whooshD', 0.35); a(s[10] + 0.2, 'poppro', 0.55); a(s[10] + 0.5, 'dingpro', 0.45)
    if rid == 'crash':
        tc = s[0] + (e[0] - s[0] + 0.3) * 0.62
        a(0.0, 'swell', 0.4); a(tc - 1.6, 'swell', 0.45); a(tc, 'impact', 0.85); a(tc + 0.02, 'glitch', 0.4)
        a(s[1], 'shutter', 0.45); a(s[1] + 0.6, 'sub', 0.6)
        for i in range(6): a(s[2] + 0.3 + i * 0.25, 'tickhi', 0.2)
        a(s[2] + 1.2, 'poppro', 0.45)
        a(s[3] - 0.1, 'whooshD', 0.35); a(s[3] + 1.2, 'sub', 0.5)
        a(s[4], 'swell', 0.3); a(e[4] - 0.2, 'poppro', 0.6, 0, pitch=0.7); a(e[4] - 0.18, 'glitch', 0.3)
        for i in range(3): a(s[5] + 0.4 + i * 1.0, 'heart', 0.45)
        for i in range(12): a(s[6] + 1.2 + i * 0.11, 'tickhi', 0.16)
        a(s[6] + 2.6, 'dingpro', 0.45)
        for i in range(3): a(s[7] + i * 0.4, 'shutter', 0.4, -0.3 + i * 0.3)
        a(s[7] + 1.6, 'stamp', 0.6)
        a(s[8] - 0.1, 'whooshD', 0.35)
        for i in range(3): a(s[8] + 0.9 + i * 1.1, 'tickhi', 0.35); a(s[8] + 0.92 + i * 1.1, 'dingpro', 0.25, 0, pitch=1 + i * 0.12)
        a(s[9] - 0.1, 'whooshD', 0.35); a(s[9] + 0.2, 'poppro', 0.55); a(s[9] + 0.5, 'dingpro', 0.45)
    return ev

def build(rid, sync, out):
    s = [l['start'] for l in sync['lines']]; e = [l['end'] for l in sync['lines']]; total = sync['total']
    mix = np.zeros((int((total + 2) * SR), 2))
    for t, name, g, pan, kw in events(rid, s, e):
        x = ALL[name]
        if 'pitch' in kw: x = resample(x, kw['pitch'])
        s0 = int(max(0, t) * SR); x = x[:len(mix) - s0] * g
        l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        mix[s0:s0 + len(x), 0] += x * l * 1.4; mix[s0:s0 + len(x), 1] += x * r * 1.4
    mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.89
    bed = P.bed(total + 2)[:len(mix)]
    fade_n = int(1.5 * SR); bed[-fade_n:] *= np.linspace(1, 0, fade_n)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
    with wave.open(out.replace('.wav', '_bed.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((bed * 0.89 * 32767).astype('<i2').tobytes())
    print(rid, len(events(rid, s, e)), 'events')

if __name__ == '__main__':
    build(sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3])
