"""Hörprüfung für CODE ROT: maschinelles "Anhören" einer fertigen Folge.

python hoerpruefung.py <folge>/episode.py [--fix]
 A) Geräusch-Erkennung (CLAP): klingt jedes eingesetzte Geräusch wie das, was die Szene braucht?
 B) Atmosphäre passend zum Schauplatz?
 C) Pegel je Einstellung: Stimme vs. Hintergrund/Geräusche (Verständlichkeit), Übersteuerung
 D) Sprachverständlichkeit: Whisper hört den fertigen Mix ab und vergleicht mit dem Skript
 E) Gesamtlautheit
--fix: echte Aufnahmen, die in A/B durchfallen, werden aussortiert (assets/sfx_real/abgelehnt/), damit beim
       nächsten Schnitt die synthetische Version greift. Exit-Code 3 = es wurde etwas aussortiert (neu schneiden).
Bericht: <folge>/export/HOERPRUEFUNG.md
"""
import json, pathlib, re, subprocess, sys, importlib.util, difflib, shutil, os
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

ERWARTET = {  # Geräusch -> was es sein soll
    "whoosh": "a fast whoosh swoosh sound effect", "impact": "a deep cinematic impact boom",
    "tick": "a ticking clock", "heartbeat": "a heartbeat", "static": "white noise static hiss",
    "funk": "a walkie talkie radio squelch beep", "atem": "a man breathing heavily", "stimmen": "people talking indistinctly",
    "feuer": "fire igniting and burning", "tuer": "a heavy door slamming", "schuesse": "gunshots",
    "alarm": "an alarm siren", "drone_hit": "a deep dark cinematic drone hit", "schrei": "a man shouting",
    "feuerwerk": "fireworks exploding", "wellen": "ocean waves",
    "atmo_nacht": "quiet night ambience with wind and crickets", "atmo_meer": "ocean waves at night",
    "atmo_stadt": "city at night ambience with distant dogs and traffic", "atmo": "dark wind ambience drone",
}
ABLENKER = ["music", "a woman speaking", "applause", "birds singing", "a car engine", "rain",
            "a dog barking", "silence", "electronic beeps", "laughter", "a crowd cheering", "footsteps"]


def lade(ep_path):
    spec = importlib.util.spec_from_file_location("episode", ep_path); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep); return ep


def wav(path, sr=48000, dauer=None, start=0.0):
    import librosa
    y, _ = librosa.load(str(path), sr=sr, mono=True, offset=start, duration=dauer)
    return y


class Clap:
    def __init__(self):
        from transformers import ClapModel, ClapProcessor
        import torch
        self.torch = torch
        self.m = ClapModel.from_pretrained("laion/clap-htsat-unfused").eval()
        self.p = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")

    def ranking(self, audio, texte):
        with self.torch.no_grad():
            ein = self.p(text=texte, audio=[audio], sampling_rate=48000, return_tensors="pt", padding=True)
            out = self.m(**ein)
            pr = out.logits_per_audio.softmax(-1)[0].numpy()
        return sorted(zip(texte, pr), key=lambda x: -x[1])


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def main():
    ep_path = pathlib.Path(sys.argv[1]).resolve(); folge = ep_path.parent; ep = lade(ep_path)
    fix = "--fix" in sys.argv
    import cut
    timing = json.loads((folge / "audio/timing.json").read_text())
    shots = timing["shots"]
    real = ROOT / "assets/sfx_real"; synth = ROOT / "assets/sfx"
    benutzt = sorted({s["sfx"] for s in ep.SHOTS if s.get("sfx")})
    atmo_name = getattr(ep, "ATMO", "atmo_nacht")
    bericht = [f"# Hörprüfung {folge.name}\n"]
    probleme, aussortiert = [], []
    clap = Clap()

    # ---------- A/B: Geräusche ----------
    bericht.append("## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)\n")
    bericht.append("| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |\n|---|---|---|---|")
    pruef = [(n, real / f"{n}.wav" if (real / f"{n}.wav").exists() else synth / f"{n}.wav") for n in benutzt]
    pa = real / f"{atmo_name}.wav"
    pruef.append((atmo_name, pa if pa.exists() else synth / "atmo.wav"))
    for name, f in pruef:
        soll = ERWARTET.get(name, name)
        texte = [soll] + [ERWARTET[k] for k in ERWARTET if k != name and ERWARTET[k] != soll][:8] + ABLENKER
        rk = clap.ranking(wav(f, dauer=10), texte)
        platz = [t for t, _ in rk].index(soll) + 1
        ok = platz <= 3
        top = ", ".join(f"{t} ({p:.0%})" for t, p in rk[:3])
        art = "echt" if f.parent == real else "synthetisch"
        bericht.append(f"| {name} | {art} | {top} | {'✅' if ok else '❌ Platz ' + str(platz)} |")
        if not ok:
            probleme.append(f"Geräusch '{name}' ({art}) klingt nicht wie '{soll}' (Platz {platz})")
            if fix and f.parent == real:
                (real / "abgelehnt").mkdir(exist_ok=True); shutil.move(str(f), real / "abgelehnt" / f.name)
                aussortiert.append(name)

    # ---------- C: Pegel je Einstellung ----------
    bericht.append("\n## C) Pegel je Einstellung (Stimme vs. Hintergrund)\n")
    tmp = folge / "build"; tmp.mkdir(exist_ok=True)
    bett = cut.mix(ep, timing, folge, tmp / "pruef_bett.wav", ohne_vo=True, norm=False)
    voll = cut.mix(ep, timing, folge, tmp / "pruef_voll.wav", ohne_vo=False, norm=False)
    yb, yv = wav(bett, sr=16000), wav(voll, sr=16000)
    yvo = yv[:len(yb)] - yb[:len(yv)]
    schlecht = 0
    for k, s in enumerate(shots):
        if not s["words"]:
            continue
        a, b = int(s["words"][0]["start"] * 16000), int(s["words"][-1]["ende"] * 16000)
        if b - a < 1600:
            continue
        sv, sb = rms_db(yvo[a:b]), rms_db(yb[a:b])
        spitze = 20 * np.log10(np.max(np.abs(yb[a:b])) + 1e-9) - sv
        abst = sv - sb
        if abst < 8 or spitze > 12:
            schlecht += 1
            probleme.append(f"Einstellung {k} ('{ep.SHOTS[k]['text'][:30]}'): Stimme nur {abst:.1f} dB über Hintergrund"
                            f"{', Geräuschspitze ' + format(spitze, '.1f') + ' dB über Stimme' if spitze > 12 else ''}")
    bericht.append(f"{len(shots)} Einstellungen geprüft, {schlecht} mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).")

    if "--schnell" in sys.argv:
        print("\n".join(probleme) or "keine Probleme"); print(bericht[-1]); return
    # ---------- D: Verständlichkeit ----------
    bericht.append("\n## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)\n")
    mp4 = folge / "export" / f"{folge.name}.mp4"
    quelle = mp4 if mp4.exists() else voll
    w16 = tmp / "pruef_16k.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(quelle), "-ac", "1", "-ar", "16000", str(w16)], check=True)
    from faster_whisper import WhisperModel
    os.environ.setdefault("HF_HUB_OFFLINE", "0")
    wm = WhisperModel("small", device="cpu", compute_type="int8")
    import wave
    w = wave.open(str(w16)); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = wm.transcribe(a, language=getattr(ep, "SPRACHE", "de"))
    gehoert = " ".join(x.text for x in segs)
    norm_ = lambda t: re.sub(r"[^a-zäöüß0-9 ]", " ", t.lower()).split()
    soll = " ".join(re.sub(r"[*_]", "", s.get("sprich") or s["text"]) for s in ep.SHOTS)
    quote = difflib.SequenceMatcher(None, norm_(soll), norm_(gehoert)).ratio()
    bericht.append(f"Übereinstimmung Skript ↔ Gehörtes: **{quote:.0%}** (gut ab ~85 %).")
    if quote < 0.8:
        probleme.append(f"Sprachverständlichkeit nur {quote:.0%}")

    # ---------- E: Lautheit ----------
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(quelle), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    bericht.append(f"\n## E) Lautheit\nIntegriert: {lufs[-1] if lufs else '?'} LUFS (Ziel −14 … −16), True Peak: {tp[-1] if tp else '?'} dBFS")

    bericht.append("\n## Ergebnis\n" + ("Keine Auffälligkeiten. ✅" if not probleme else "\n".join(f"- {p}" for p in probleme)))
    if aussortiert:
        bericht.append("\nAussortiert (beim nächsten Schnitt synthetisch ersetzt): " + ", ".join(aussortiert))
    (folge / "export").mkdir(exist_ok=True)
    (folge / "export/HOERPRUEFUNG.md").write_text("\n".join(bericht) + "\n", encoding="utf-8")
    print("\n".join(bericht[-3:]))
    sys.exit(3 if aussortiert else 0)


if __name__ == "__main__":
    main()
