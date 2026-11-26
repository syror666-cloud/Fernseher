"""Figurenstimmen für CODE ROT: ersetzt einzelne Zeilen der Erzählerspur durch andere ElevenLabs-Stimmen.

python stimmen.py <folge>/episode.py
- Einstellungen mit  stimme="<rolle>"  werden mit der Stimme der Rolle neu gesprochen. Aufeinanderfolgende
  Einstellungen derselben Rolle werden als ein Satz gesprochen (natürlicher Fluss) und danach wieder aufgeteilt.
- stimme_ab="<Wort>": nur ab diesem Wort ersetzen (z. B. Erzähler sagt „Im Funk:“, die Figur sagt „Bereit?“).
- Die Erzählerspur selbst bleibt unverändert (audio/vo_erzaehler.wav); alles nach einer ersetzten Zeile rückt
  um die Längendifferenz nach. Ergebnis: audio/vo.wav + audio/timing.json (wie vo.py).
Der API-Schlüssel wird vom Proxy der Umgebung eingesetzt (Header-Platzhalter).
"""
import json, re, base64, pathlib, subprocess, hashlib, shutil, sys, importlib.util, urllib.request
import numpy as np

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128"
SR = 44100
MODELL = "eleven_multilingual_v2"

# Rollen der Serie (Stimmen aus der ElevenLabs-Bibliothek, deutschsprachig)
ROLLEN = {
    # die unheimliche Stimme aus dem Spind (Intro + Teaser jeder Folge)
    "spind": dict(id="DUAKkudcC2PI6KEqJ60K", name="Haunting Hector",
                  einstellung={"stability": 0.5, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.0},
                  effekt="asetrate=44100*0.94,aresample=44100,atempo=1.0638,aecho=0.8:0.45:55|110:0.22|0.1", pegel=1.0),
    # Truppführer / Oberst: rau, ruhig, gefährlich
    "chef": dict(id="3SS1Mem5uFQXQc0kb54t", name="Gottfried",
                 einstellung={"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.05},
                 effekt="", pegel=0.0),
    # Befehl über Funk (gleiche Stimme, Funkfilter)
    "funk": dict(id="3SS1Mem5uFQXQc0kb54t", name="Gottfried (Funk)",
                 einstellung={"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.05},
                 effekt="highpass=f=350,lowpass=f=3200,acrusher=bits=9:mix=0.25,volume=2", pegel=0.0),
    # gebrüllter Befehl
    "schrei": dict(id="U2swAVvmpE98PJAkPUMP", name="Willy Lübke",
                   einstellung={"stability": 0.3, "similarity_boost": 0.8, "style": 0.8, "use_speaker_boost": True, "speed": 1.1},
                   effekt="", pegel=2.0),
    # junger Mann, laut und erleichtert (Befreiungsruf)
    "jubel": dict(id="1RqQZf1DSt04oYSqaxNK", name="Lucas (Jubel)",
                  einstellung={"stability": 0.3, "similarity_boost": 0.8, "style": 0.8, "use_speaker_boost": True, "speed": 1.05},
                  effekt="", pegel=2.5),
    # junger Mann
    "jung": dict(id="1RqQZf1DSt04oYSqaxNK", name="Lucas",
                 einstellung={"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.08},
                 effekt="", pegel=0.0),
}


# Rollenstimmen je Sprache (überschreiben ROLLEN; gleiche Effekte/Pegel, muttersprachliche Stimmen)
ROLLEN_SPRACHE = {
    "en": {"spind": "1BfrkuYXmEwp8AWqSLWk",   # Declan – Horror (alt, unheimlich)
           "chef": "3YzGaTGef0x5PLEK9yGq",    # Atlas – tief, rau
           "funk": "3YzGaTGef0x5PLEK9yGq",
           "schrei": "3YzGaTGef0x5PLEK9yGq",
           "jung": "nHHVbJ6p0mXRxkGrWZI2",    # Jeff
           "jubel": "nHHVbJ6p0mXRxkGrWZI2"},
    "es": {"spind": "DWrVftdnFieVgzNH3uzf",   # Jesús – tief, cineastisch (+ Effekt)
           "chef": "vT7H1Y5jYNGFl82cyN9E",    # Krade – tief, mexikanisch
           "funk": "vT7H1Y5jYNGFl82cyN9E",
           "schrei": "vT7H1Y5jYNGFl82cyN9E",
           "jung": "MFczlrjgpEos5t8Rwlto",    # Orozco – jung, kolumbianisch
           "jubel": "MFczlrjgpEos5t8Rwlto"},
}


def rolle(name, sprache):
    r = dict(ROLLEN[name])
    if sprache in ROLLEN_SPRACHE:
        r["id"] = ROLLEN_SPRACHE[sprache][name]
    return r


def plain(t):
    return re.sub(r"[*_„“”\"]", "", t)


def lade_wav(p):
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()


def schreibe_wav(y, p):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", str(p)], input=np.clip(y, -1, 1).astype(np.float32).tobytes(), check=True)


def tts(text, rolle_name, cache, sprache="de", override=None):
    rolle = rolle_name
    r = globals()["rolle"](rolle_name, sprache) if not override else dict(override, effekt="", pegel=0.0)
    key = hashlib.md5(json.dumps([text, r["id"], r["einstellung"]] + ([r["modell"]] if r.get("modell") else []),
                                 sort_keys=True).encode()).hexdigest()[:12]
    mp3, js = cache / f"{rolle}_{key}.mp3", cache / f"{rolle}_{key}.json"
    if not (mp3.exists() and js.exists()):
        body = json.dumps({"text": text, "model_id": r.get("modell", MODELL), "voice_settings": r["einstellung"],
                           "language_code": sprache}).encode()
        req = urllib.request.Request(API.format(voice=r["id"]), data=body, method="POST",
                                     headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as resp:
            d = json.loads(resp.read())
        al_ = d["alignment"]
        if "[" in text:  # eleven_v3-Regieanweisungen nicht als Wörter zählen
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import vo as _vo
            al_ = _vo.ohne_tags(al_)
        mp3.write_bytes(base64.b64decode(d["audio_base64"])); js.write_text(json.dumps(al_, ensure_ascii=False))
    y = lade_wav(mp3)
    if r["effekt"]:
        wav = cache / f"{rolle}_{key}_fx.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-af", r["effekt"], "-ac", "2", "-ar", str(SR),
                        str(wav)], check=True)
        y = lade_wav(wav)
    return y, json.loads(js.read_text())


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-9)


def anwenden(ep, folge):
    audio = folge / "audio"
    t_akt, w_akt = audio / "timing.json", audio / "vo.wav"
    t_basis, w_basis = audio / "timing_erzaehler.json", audio / "vo_erzaehler.wav"
    akt = json.loads(t_akt.read_text())
    if not akt.get("stimmen") or not t_basis.exists():  # vo.py hat neu gesprochen -> das ist die Erzählerspur
        shutil.copy(t_akt, t_basis); shutil.copy(w_akt, w_basis)
    basis = json.loads(t_basis.read_text())
    shots = basis["shots"]
    # Blöcke: aufeinanderfolgende Einstellungen derselben Rolle
    bloecke, cur = [], None
    for k, s in enumerate(ep.SHOTS):
        r = s.get("stimme")
        if r and shots[k]["words"]:
            ab = 0
            if s.get("stimme_ab"):
                toks = [w["w"] for w in shots[k]["words"]]
                ab = next(i for i, w in enumerate(toks) if s["stimme_ab"] in w)
            if cur and cur["rolle"] == r and cur["shots"][-1][0] == k - 1 and ab == 0:
                cur["shots"].append((k, 0))
            else:
                cur = {"rolle": r, "shots": [(k, ab)]}; bloecke.append(cur)
        else:
            cur = None
    # Titelkarte: der Erzähler spricht den Namen der Einheit in die stumme Pause (Nutzerwunsch)
    for k, s_ in enumerate(ep.SHOTS):
        if s_.get("titel") and not shots[k]["words"]:
            bloecke.append({"rolle": "erzaehler", "titel_k": k})
    bloecke.sort(key=lambda b_: shots[b_["titel_k"] if "titel_k" in b_ else b_["shots"][0][0]]["schnitt"])
    if not bloecke:
        shutil.copy(t_basis, t_akt); shutil.copy(w_basis, w_akt); return 0
    y = lade_wav(w_basis)
    cache = audio / "stimmen"; cache.mkdir(exist_ok=True)
    teile, cursor, verschiebung = [], 0.0, []  # verschiebung: (b_basis, delta) kumulativ
    neu_words = {}
    kum = 0.0
    titel_words = {}
    for bl in bloecke:
        if "titel_k" in bl:
            k = bl["titel_k"]; s_ = ep.SHOTS[k]
            name = s_.get("titel_sprich") or re.sub(r"[*_]", "", s_["titel"]).strip()
            if name.isupper() and not re.search(r"\d", name):
                name = " ".join(w.capitalize() if len(w) > 2 else w.lower() for w in name.split())
            text = name if name.rstrip()[-1:] in ".!?" else name + "."
            ov = {"id": ep.STIMME, "einstellung": getattr(ep, "TITEL_EINSTELLUNG", ep.STIMM_EINSTELLUNG)}
            if getattr(ep, "TITEL_MODELL", None):
                ov["modell"] = ep.TITEL_MODELL
            clip, al = tts(text, "erzaehler", cache, getattr(ep, "SPRACHE", "de"), override=ov)
            chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
            spans = [(m.start(), m.end() - 1) for m in re.finditer(r"\S+", "".join(chars))]
            t0 = max(0.0, st[spans[0][0]] - 0.03); t1 = min(len(clip) / SR, en[spans[-1][1]] + 0.12)
            # gerufene Namen (eleven_v3): die Zeichen-Zeitstempel sind teils viel zu kurz -> hörbaren Bereich mitnehmen
            e_ = np.sqrt(np.convolve((clip ** 2).mean(axis=1), np.ones(441) / 441, mode="same"))
            laut_ = np.where(e_ > 10 ** (-40 / 20))[0]
            if len(laut_):
                t0 = max(0.0, min(t0, laut_[0] / SR - 0.03)); t1 = min(len(clip) / SR, max(t1, laut_[-1] / SR + 0.12))
            c = clip[int(t0 * SR):int(t1 * SR)]
            ref = y[int(shots[k + 1]["words"][0]["start"] * SR):int(shots[k + 1]["words"][-1]["ende"] * SR)] \
                if k + 1 < len(shots) and shots[k + 1]["words"] else c
            c = c * (rms(ref) / rms(c)) * 10 ** (getattr(ep, "TITEL_PEGEL", 0.0) / 20)  # lauter gerufener Name
            if np.abs(c).max() > 0.9:
                c = 0.9 * np.tanh(c / 0.9)
            a = max(cursor, shots[k]["schnitt"] + 0.05); b = max(a, shots[k]["ende"] - 0.05)
            teile.append(y[int(cursor * SR):int(a * SR)]); teile.append(c)
            neu_a = a + kum
            toks = re.sub(r"[*_]", "", s_["titel"]).split() if len(s_["titel"].split()) == len(spans) \
                else re.sub(r"\[[^\]]*\]\s*", "", name).split()
            titel_words[k] = [{"w": tok, "start": neu_a + st[sa] - t0, "ende": neu_a + en[sb] - t0}
                              for tok, (sa, sb) in zip(toks, spans)]
            delta = (t1 - t0) - (b - a)
            kum += delta; verschiebung.append((b, kum)); cursor = b
            continue
        ws = [(k, i, w) for k, ab in bl["shots"] for i, w in enumerate(shots[k]["words"]) if i >= ab]
        a = max(cursor, ws[0][2]["start"] - 0.04); b = ws[-1][2]["ende"] + 0.08
        text = " ".join(plain(w["w"]) for _, _, w in ws)
        text = re.sub(r"\s+", " ", text).strip()
        clip, al = tts(text, bl["rolle"], cache, getattr(ep, "SPRACHE", "de"))
        chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
        joined = "".join(chars)
        spans = [(m.start(), m.end() - 1) for m in re.finditer(r"\S+", joined)]
        t0 = max(0.0, st[spans[0][0]] - 0.03)
        tail = 0.35 if ROLLEN[bl["rolle"]]["effekt"].count("aecho") else 0.08
        t1 = min(len(clip) / SR, en[spans[-1][1]] + tail)
        c = clip[int(t0 * SR):int(t1 * SR)]
        # Lautstärke an den Erzähler angleichen
        ref = y[int(ws[0][2]["start"] * SR):int(ws[-1][2]["ende"] * SR)]
        c = c * (rms(ref) / rms(c)) * 10 ** (ROLLEN[bl["rolle"]]["pegel"] / 20)
        if np.abs(c).max() > 0.9:  # weich begrenzen statt hart zu clippen (laute Rufe)
            c = 0.9 * np.tanh(c / 0.9)
        teile.append(y[int(cursor * SR):int(a * SR)]); teile.append(c)
        neu_a = a + kum
        for (k, i, w), (sa, sb) in zip(ws, spans):
            neu_words[(k, i)] = (neu_a + st[sa] - t0, neu_a + en[sb] - t0)
        delta = (t1 - t0) - (b - a)
        kum += delta; verschiebung.append((b, kum)); cursor = b
    teile.append(y[int(cursor * SR):])
    schreibe_wav(np.concatenate(teile), w_akt)

    def sh(t):  # Basiszeit -> neue Zeit (nach den Blöcken verschoben)
        d = 0.0
        for b, kk in verschiebung:
            if t >= b - 1e-6:
                d = kk
        return t + d
    neu = {"gesamt": basis["gesamt"] + kum, "stimmen": True, "shots": []}
    for k, s in enumerate(shots):
        n = json.loads(json.dumps(s))
        for i, w in enumerate(n["words"]):
            if (k, i) in neu_words:
                w["start"], w["ende"] = neu_words[(k, i)]
            else:
                w["start"], w["ende"] = sh(w["start"]), sh(w["ende"])
        if k in titel_words:
            n["words"] = titel_words[k]
        if n["words"]:
            n["start"], n["sprech_ende"] = n["words"][0]["start"], n["words"][-1]["ende"]
        else:
            n["start"] = sh(n["start"]); n["sprech_ende"] = sh(n["sprech_ende"])
        neu["shots"].append(n)
    for k, n in enumerate(neu["shots"]):
        n["schnitt"] = 0.0 if k == 0 else max(neu["shots"][k - 1]["sprech_ende"], n["start"] - 0.06)
    for k, n in enumerate(neu["shots"]):
        n["ende"] = neu["shots"][k + 1]["schnitt"] if k + 1 < len(neu["shots"]) else neu["gesamt"]
    t_akt.write_text(json.dumps(neu, ensure_ascii=False, indent=1))
    return len(bloecke)


if __name__ == "__main__":
    ep_path = pathlib.Path(sys.argv[1]).resolve()
    spec = importlib.util.spec_from_file_location("episode", ep_path); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep)
    n = anwenden(ep, ep_path.parent)
    t = json.loads((ep_path.parent / "audio/timing.json").read_text())
    print(f"{n} Zeilen mit Figurenstimmen, Dauer {t['gesamt']:.2f} s")
