"""Synthetische Geräusche für CODE ROT (kein externer Sound nötig, frei von Rechten).

python sfx.py <ausgabeordner>  -> erzeugt alle WAVs (44.1 kHz, Stereo)
"""
import numpy as np, pathlib, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(42)


def t(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d))
def lp(x, f, o=4): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b, o=4): return sosfilt(butter(o, [a, b], "band", fs=SR, output="sos"), x)
def env(d, a, r):
    n = int(SR * d); e = np.ones(n); na = max(1, int(SR * a)); nr = max(1, int(SR * r))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def decay(d, k): return np.exp(-t(d) * k)
def norm(x, peak=0.9): return x / (np.max(np.abs(x)) + 1e-9) * peak
def stereo(x, breite=0.0):
    if breite:
        d = int(SR * 0.012 * breite); r = np.concatenate([np.zeros(d), x[:-d]]) if d else x
        return np.stack([x, r], 1)
    return np.stack([x, x], 1)


def whoosh(d=0.7):
    n = noise(d); out = np.zeros_like(n); seg = 512
    for i in range(0, len(n) - seg, seg):
        f = 300 + 4000 * np.sin(np.pi * i / len(n)) ** 2
        out[i:i + seg] = bp(n[i:i + seg + 0], max(80, f * 0.5), min(18000, f * 1.6), 2)[:seg]
    return norm(lp(out, 6000) * np.sin(np.pi * t(d) / d) ** 1.5, 0.7)


def impact(d=1.6):
    boom = np.sin(2 * np.pi * (48 * t(d) + 30 * (1 - decay(d, 6)) / 6)) * decay(d, 3.2)
    knall = lp(noise(d), 1800) * decay(d, 25)
    return norm(boom * 1.0 + knall * 0.6, 0.95)


def tick(d=0.35):
    klick = hp(noise(d), 3000) * decay(d, 160)
    piep = np.sin(2 * np.pi * 1760 * t(d)) * env(d, 0.005, 0.05) * (t(d) > 0.06) * (t(d) < 0.16)
    return norm(klick * 0.8 + piep * 0.35, 0.6)


def heartbeat(d=1.6):
    x = np.zeros(int(SR * d))
    for s0, a in ((0.0, 1.0), (0.24, 0.7), (0.85, 1.0), (1.09, 0.7)):
        dd = 0.25; seg = np.sin(2 * np.pi * 52 * t(dd)) * decay(dd, 18) * a
        i = int(SR * s0); x[i:i + len(seg)] += seg[: len(x) - i]
    return norm(lp(x, 160), 0.95)


def static(d=0.9):
    n = bp(noise(d), 800, 6000)
    crack = (rng.random(len(n)) > 0.997) * rng.standard_normal(len(n)) * 6
    return norm((n * 0.5 + crack) * env(d, 0.01, 0.15), 0.55)


def funk(d=0.6):
    klick = hp(noise(d), 2000) * decay(d, 200)
    rausch = bp(noise(d), 1200, 3500) * (t(d) > 0.03) * (t(d) < 0.38) * 0.4
    piep = np.sin(2 * np.pi * 1350 * t(d)) * (t(d) > 0.4) * (t(d) < 0.52) * env(d, 0.01, 0.05) * 0.5
    return norm(klick + rausch + piep, 0.6)


def atem(d=2.4):
    def zug(dd, f1, f2):
        return bp(noise(dd), f1, f2, 2) * np.sin(np.pi * t(dd) / dd) ** 2
    x = np.concatenate([zug(0.9, 300, 2200), np.zeros(int(SR * 0.15)), zug(1.2, 200, 1600) * 0.8])
    x = np.pad(x, (0, max(0, int(SR * d) - len(x))))[: int(SR * d)]
    return norm(x, 0.5)


def stimmen(d=1.6):
    n = noise(d); out = np.zeros_like(n)
    for f0 in (180, 230, 140):
        mod = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(3, 6) * t(d) + rng.uniform(0, 6))
        out += bp(n, f0 * 2, f0 * 6, 2) * mod
    return norm(lp(out, 900) * env(d, 0.2, 0.4), 0.45)


def feuer(d=2.5):
    grund = lp(noise(d), 400) * 0.6
    knistern = (rng.random(int(SR * d)) > 0.9985) * rng.standard_normal(int(SR * d)) * 5
    knistern = hp(knistern, 1500)
    fauch = bp(noise(d), 500, 3000) * env(d, 0.05, 0.8) * 0.35
    return norm((grund + knistern + fauch) * env(d, 0.02, 0.7), 0.75)


def tuer(d=1.4):
    x = impact(d) * 0.8
    for f, k in ((420, 6), (1130, 9), (2310, 12), (3170, 15)):
        x += np.sin(2 * np.pi * f * t(d)) * decay(d, k) * 0.12
    return norm(x, 0.95)


def schuesse(d=0.9):
    x = np.zeros(int(SR * d))
    for s0 in (0.0, 0.16, 0.41):
        dd = 0.35
        shot = lp(noise(dd), 2500) * decay(dd, 40) + np.sin(2 * np.pi * 70 * t(dd)) * decay(dd, 14) * 0.8
        i = int(SR * s0); x[i:i + len(shot)] += shot[: len(x) - i]
    return norm(lp(x, 3500), 0.9)


def alarm(d=1.2):
    f = np.where((t(d) * 4).astype(int) % 2 == 0, 880, 660)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.3 + np.sin(ph) * 0.4
    return norm(lp(x, 3000) * env(d, 0.01, 0.2), 0.45)


def drone_hit(d=3.0):
    saw = sum(np.sin(2 * np.pi * 41 * k * t(d)) / k for k in range(1, 12))
    x = lp(saw, 500) * np.minimum(1, t(d) * 4) * decay(d, 1.1) + impact(d) * 0.5
    return norm(x, 0.9)


def schrei(d=0.6):
    return norm(impact(d) * 0.5 + whoosh(d) * 0.5, 0.6)


def feuerwerk(d=3.0):
    x = np.zeros(int(SR * d))
    for s0 in (0.0, 0.7, 1.5):
        aufstieg = hp(noise(0.5), 2500) * np.linspace(0.05, 0.4, int(SR * 0.5))
        knall = impact(0.9) * 0.9
        knistern = hp((rng.random(int(SR * 1.2)) > 0.996) * rng.standard_normal(int(SR * 1.2)) * 4, 2000) * decay(1.2, 2.5)
        i = int(SR * s0)
        for seg, off in ((aufstieg, 0), (knall, 0.5), (knistern, 0.6)):
            j = i + int(SR * off); x[j:j + len(seg)] += seg[: max(0, len(x) - j)]
    return norm(x, 0.9)


def atmo(d=150.0):
    """Nacht-Atmosphäre: Wind, tiefer Drone, ferne Grillen."""
    wind = lp(np.cumsum(noise(d)) * 0.02, 500)
    wind = wind - lp(wind, 20)
    wind *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t(d)) ** 2
    drone = (np.sin(2 * np.pi * 55 * t(d)) + 0.6 * np.sin(2 * np.pi * 55.4 * t(d)) + 0.3 * np.sin(2 * np.pi * 82.4 * t(d)))
    drone *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t(d)) ** 2
    grillen = np.sin(2 * np.pi * 4600 * t(d)) * (np.sin(2 * np.pi * 28 * t(d)) > 0.6) * (np.sin(2 * np.pi * 0.9 * t(d)) > 0.2)
    x = norm(wind) * 0.55 + norm(drone) * 0.35 + norm(lp(grillen, 6000)) * 0.04
    return norm(x, 0.5)


ALLE = dict(whoosh=whoosh, impact=impact, tick=tick, heartbeat=heartbeat, static=static, funk=funk, atem=atem,
            stimmen=stimmen, feuer=feuer, tuer=tuer, schuesse=schuesse, alarm=alarm, drone_hit=drone_hit, schrei=schrei, feuerwerk=feuerwerk)

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for k, fn in ALLE.items():
        wavfile.write(out / f"{k}.wav", SR, (stereo(fn(), 0.5) * 32767).astype(np.int16))
    wavfile.write(out / "atmo.wav", SR, (stereo(atmo(), 1.0) * 32767).astype(np.int16))
    print("ok", len(ALLE) + 1)
