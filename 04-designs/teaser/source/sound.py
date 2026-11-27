"""Original sound design for the teaser, synthesised from scratch (no samples, nothing to license).

  python sound.py teaser|reveal   -> _build/sound-<variant>.wav (48 kHz stereo)

Waves at Mahdia -> a boom on «لوين؟» -> wind while the map scrolls -> a darbouka groove in 6/8
with an oud-like pluck (Karplus-Strong) in the Hijaz mode on every clue -> a riser, then a
clock ticking under «عرفتوها؟» -> the end card, and the waves come back so the Reel loops.
Event times match teaser.js.
"""
import sys, wave
from pathlib import Path
import numpy as np
from scipy import signal

SR = 48000
HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(12)

def tt(d): return np.arange(int(d * SR)) / SR
def env_exp(d, tau): return np.exp(-tt(d) / tau)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)

class Mix:
    def __init__(self, dur):
        self.L = np.zeros(int(dur * SR) + SR); self.R = np.zeros_like(self.L); self.dur = dur
    def add(self, t0, x, g=1.0, pan=0.0):
        i = int(t0 * SR)
        if i < 0: x = x[-i:]; i = 0
        n = min(len(x), len(self.L) - i)
        if n <= 0: return
        gl, gr = g * np.sqrt((1 - pan) / 2) * 1.414, g * np.sqrt((1 + pan) / 2) * 1.414
        self.L[i:i+n] += x[:n] * gl; self.R[i:i+n] += x[:n] * gr
    def add_st(self, t0, l, r, g=1.0):
        self.add(t0, l, g, -1); self.add(t0, r, g, 1)

# ---------------------------------------------------------------- instruments

def ocean(d):
    out = []
    for _ in range(2):
        n = np.cumsum(rng.standard_normal(int(d*SR))); n = hp(n, 30); n /= np.abs(n).max()
        n = lp(n, 900)
        sw = 0.55 + 0.45 * np.sin(2*np.pi*tt(d)/3.4 + rng.uniform(0, 6))**2
        hiss = bp(rng.standard_normal(int(d*SR)), 1500, 5000) * 0.25 * sw**3
        out.append((n * sw + hiss) * 0.9)
    return out

def boom(d=1.4, f0=92, f1=36, g=1.0):
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / .12)
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t / .42)
    click = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t / .012) * .6
    return np.tanh((s + click) * 1.6) * g

def whoosh(d, f0=300, f1=4000, g=1.0):
    n = rng.standard_normal(int(d*SR)); t = tt(d)
    out = np.zeros_like(n); seg = 2048
    for k in range(0, len(n), seg):
        c = f0 * (f1/f0) ** (k/len(n))
        out[k:k+seg] = bp(n[max(0,k-4096):k+seg], c*.7, min(c*1.4, 20000))[-len(n[k:k+seg]):]
    e = np.sin(np.pi * np.clip(t/d, 0, 1)) ** 1.5
    return out * e * g

def wind(d):
    n = rng.standard_normal(int(d*SR)); t = tt(d)
    m = 0.6 + 0.4*np.sin(2*np.pi*t/2.3) * np.sin(2*np.pi*t/0.9 + 1)
    return bp(n, 250, 1400) * m * 0.5

def doum(g=1.0):
    t = tt(.5); f = 70 + 40*np.exp(-t/.03)
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/.17)
    s += lp(rng.standard_normal(len(t)), 900) * np.exp(-t/.01) * .4
    return s * g

def tek(g=1.0, bright=1.0):
    t = tt(.18)
    n = hp(rng.standard_normal(len(t)), 1800) * np.exp(-t/.018)
    ring = np.sin(2*np.pi*(2600*bright)*t) * np.exp(-t/.03) * .5
    return (n + ring) * g

def pluck(freq, d=1.6, g=1.0, bright=.5):
    """Karplus-Strong: a plucked string, oud-ish."""
    N = int(SR / freq); buf = rng.uniform(-1, 1, N); buf = lp(np.concatenate([buf, buf]), 4000)[N:]
    out = np.zeros(int(d*SR)); idx = 0; dec = .996
    for i in range(len(out)):
        j = i % N; nxt = (i+1) % N
        v = dec * (bright*buf[j] + (1-bright)*buf[nxt])
        out[i] = buf[j]; buf[j] = v
    att = np.minimum(1, tt(d)/.004)
    return lp(out * att, 5200) * g

def woodblock(g=1.0):
    t = tt(.12); return (np.sin(2*np.pi*1350*t) + .5*np.sin(2*np.pi*2210*t)) * np.exp(-t/.022) * g

def paper(g=1.0):
    t = tt(.22); return lp(hp(rng.standard_normal(len(t)), 300), 3500) * np.exp(-t/.04) * g

def tape(g=1.0):
    t = tt(.16); n = bp(rng.standard_normal(len(t)), 1800, 7000)
    return n * (0.5 + 0.5*np.sign(np.sin(2*np.pi*90*t))) * np.exp(-t/.07) * g

def scribble(d=.5, g=1.0):
    t = tt(d); n = bp(rng.standard_normal(len(t)), 2500, 7000)
    am = (0.5 + 0.5*np.sin(2*np.pi*13*t + 3*np.sin(2*np.pi*3*t))) ** 2
    return n * am * np.sin(np.pi*np.clip(t/d, 0, 1)) * g

def drone(d, g=1.0):
    t = tt(d)
    s = sum(signal.sawtooth(2*np.pi*f*t + p) for f, p in [(73.42, 0), (110.0, 1), (146.83, 2), (73.6, 3)])
    s = lp(s, 700, 2) * .25
    e = np.minimum(1, t/1.2) * np.minimum(1, (d - t)/1.0)
    return s * e * g

def riser(d, g=1.0):
    t = tt(d); f = 180 * (6 ** (t/d))
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * .3 + whoosh(d, 400, 9000) * .8
    return s * (t/d) ** 2 * g

# Hijaz on D: D Eb F# G A Bb C D
HJ = {'D3': 146.83, 'Eb3': 155.56, 'F#3': 185.0, 'G3': 196.0, 'A3': 220.0, 'Bb3': 233.08, 'C4': 261.63, 'D4': 293.66, 'Eb4': 311.13, 'F#4': 369.99, 'A2': 110.0, 'D2': 73.42}
PHRASES = [['D3', 'Eb3', 'F#3'], ['F#3', 'G3', 'A3'], ['A3', 'Bb3', 'C4'], ['C4', 'Bb3', 'A3', 'D4']]

# ---------------------------------------------------------------- score

def build(variant):
    R = variant == 'reveal'
    DUR = 17.0 if R else 15.5
    m = Mix(DUR)
    # S1 waves, boom on «لوين؟»
    l, r = ocean(3.4); fade = np.minimum(1, (3.4 - tt(3.4)) / 1.0); m.add_st(0, l*fade, r*fade, .42)
    m.add(.74, boom(), .9); m.add(.72, whoosh(.25, 2000, 8000), .25)
    m.add(1.1, pluck(HJ['D3'], 2.2, bright=.45), .35, -.2)
    # S2 the camera tilts down the map
    m.add(1.95, whoosh(1.2, 250, 3000), .55)
    m.add(2.2, wind(2.6), .75)
    for k, tk in enumerate(np.arange(2.5, 4.4, .38)):     # footsteps on the trail
        m.add(tk, lp(paper(.7), 900), .5, -.3 if k % 2 else .3)
    m.add(2.95, boom(.9, 140, 60), .45)                    # «4 تلميحات» pops
    m.add(4.15, woodblock(), .35); m.add(4.32, woodblock(), .25)    # the pin drops
    m.add(4.45, whoosh(.45, 600, 6000), .5)                # page slides up
    # S3-S6 darbouka groove in 6/8, one bar per clue (1.6 s), pluck phrase on each landing
    bar = 1.6; e = bar / 6
    m.add(4.75, drone(6.6), .55)
    for i in range(4):
        t0 = 4.75 + 1.6*i + .3                              # the card lands
        m.add(t0 - .05, paper(1), .55); m.add(t0, doum(1), .85)
        m.add(t0 + .08, tape(1), .3)
        m.add(4.75 + 1.6*i + .45, scribble(.5), .16)
        for k, (kind, gg) in enumerate([('D', 1), (None, 0), ('T', .7), ('K', .45), ('D', .7), ('T', .6)]):
            if k == 0 or kind is None: continue
            tk = t0 + k*e
            if tk > 11.12: continue
            m.add(tk, doum(gg) if kind == 'D' else tek(gg, 1.0 if kind == 'T' else .8), .7, .15 if kind == 'K' else -.1)
        for j, nm in enumerate(PHRASES[i]):
            m.add(t0 + j*e*1.0, pluck(HJ[nm], 1.4, bright=.5), .32, .25)
    if not R:
        m.add(10.55, riser(.9), .55)
        m.add(11.45, boom(1.6, 110, 40), .9); m.add(11.45, pluck(HJ['D2'], 2.5, bright=.4), .4)
        m.add(11.47, pluck(HJ['A2'], 2.4, bright=.4), .3, .3)
        for k, tk in enumerate(np.arange(11.95, 13.1, .5)):  # thinking… the clock ticks
            m.add(tk, woodblock(1 if k % 2 == 0 else .7), .62, -.4 if k % 2 else .4)
        # end card
        m.add(13.1, whoosh(.5, 500, 5000), .4)
        m.add(13.35, boom(1.4, 100, 40), .75)
        for j, nm in enumerate(['D3', 'F#3', 'A3', 'D4']):
            m.add(13.45 + j*.22, pluck(HJ[nm], 2.0, bright=.5), .34, -.2 + .15*j)
        m.add(13.3, drone(2.4), .45)
    else:
        m.add(11.0, whoosh(.5, 3000, 300), .4)
        m.add(11.48, boom(1.6, 80, 34), 1.0); m.add(11.48, paper(1.4), .7)
        m.add(11.5, woodblock(.8), .5)
        m.add(12.25, riser(.62), .45)
        m.add(12.85, boom(1.2, 120, 45), .7)
        for j, nm in enumerate(['A3', 'C4', 'Bb3', 'A3', 'D4']):
            m.add(12.6 + j*.13, pluck(HJ[nm], 1.8, bright=.5), .33, .2)
        # the groove comes back for the end card
        m.add(13.6, whoosh(.5, 500, 5000), .35)
        m.add(13.6, drone(2.9), .5)
        for b in range(2):
            t0 = 13.9 + b*bar
            for k, (kind, gg) in enumerate([('D', 1), (None, 0), ('T', .7), ('K', .45), ('D', .7), ('T', .6)]):
                if kind is None: continue
                tk = t0 + k*e
                if tk > 16.4: continue
                m.add(tk, doum(gg) if kind == 'D' else tek(gg, 1.0 if kind == 'T' else .8), .6)
        for j, nm in enumerate(['D3', 'F#3', 'A3', 'D4']):
            m.add(14.6 + j*.22, pluck(HJ[nm], 2.0, bright=.5), .32, -.2 + .15*j)
    # the waves return so the end flows into the start
    l, r = ocean(1.4); fi = np.minimum(1, tt(1.4) / 1.1); m.add_st(DUR - 1.4, l*fi, r*fi, .42)
    L, Rr = m.L[:int(DUR*SR)], m.R[:int(DUR*SR)]
    st = np.stack([L, Rr], 1)
    st = np.tanh(st / (np.abs(st).max() * .62)) ; st /= np.abs(st).max(); st *= .89
    return st

def write(variant):
    st = build(variant)
    out = HERE / '_build' / f'sound-{variant}.wav'
    with wave.open(str(out), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())
    print('wrote', out.name, f'{len(st)/SR:.2f}s')

if __name__ == '__main__':
    for v in sys.argv[1:] or ['teaser', 'reveal']:
        write(v)
