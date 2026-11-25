"""Voiceover über ElevenLabs (mit Zeitstempeln) und Wort-Timing pro Einstellung.

Der API-Schlüssel wird vom Proxy der Umgebung eingesetzt (Header-Platzhalter).
Ergebnis: vo.mp3 + timing.json (Start/Ende jeder Einstellung und jedes Wortes, inkl. Pausen).
"""
import json, re, base64, pathlib, subprocess, urllib.request

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128"


def plain(t: str) -> str:
    return re.sub(r"[*_]", "", t)


def tts(text, voice, model, settings, out_mp3: pathlib.Path, sprache="de"):
    body = json.dumps({"text": text, "model_id": model, "voice_settings": settings, "language_code": sprache}).encode()
    req = urllib.request.Request(API.format(voice=voice), data=body, method="POST",
                                 headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    out_mp3.write_bytes(base64.b64decode(d["audio_base64"]))
    return d["alignment"]


def build(episode, outdir: pathlib.Path, force=False):
    outdir.mkdir(parents=True, exist_ok=True)
    raw_mp3, align_f = outdir / "vo_raw.mp3", outdir / "alignment.json"
    # Volltext und Zeichen-Offsets je Einstellung
    teile, offs, pos = [], [], 0
    for s in episode.SHOTS:
        t = (s.get("sprich") or plain(s["text"])).strip()
        offs.append((pos, pos + len(t)) if t else None)
        if t:
            teile.append(t); pos += len(t) + 1
    text = " ".join(teile)
    if force or not raw_mp3.exists():
        align = tts(text, episode.STIMME, episode.MODELL, episode.STIMM_EINSTELLUNG, raw_mp3, getattr(episode, "SPRACHE", "de"))
        align_f.write_text(json.dumps(align, ensure_ascii=False))
    align = json.loads(align_f.read_text())
    chars, st, en = align["characters"], align["character_start_times_seconds"], align["character_end_times_seconds"]
    assert "".join(chars) == text, "Alignment passt nicht zum Text"

    # Pausen einfügen: verschiebt alles ab der Einstellung um 'pause' Sekunden
    shots, shift, pausen = [], 0.0, []
    for i, s in enumerate(episode.SHOTS):
        p = s.get("pause", 0.0)
        if p:
            # Pause beginnt am Ende des vorherigen gesprochenen Zeichens
            prev = max((o[1] - 1 for o in offs[:i] if o), default=-1)
            t0 = en[prev] if prev >= 0 else 0.0
            pausen.append((t0, p)); shift += p
        o = offs[i]
        if o:
            words = []
            if s.get("sprich"):
                # Untertitelwörter gleichmäßig (nach Länge) über die gesprochene Spanne verteilen
                t0, t1 = st[o[0]] + shift, en[o[1] - 1] + shift
                mws = s["text"].split(); tot = sum(len(w) for w in mws); acc = 0
                for mw in mws:
                    a = t0 + (t1 - t0) * acc / tot; acc += len(mw)
                    words.append({"w": mw, "start": a, "ende": t0 + (t1 - t0) * acc / tot})
            else:
                pt = plain(s["text"]).strip()
                for mw, pm in zip(s["text"].split(), re.finditer(r"\S+", pt)):
                    a = o[0] + pm.start(); b = o[0] + pm.end() - 1
                    words.append({"w": mw, "start": st[a] + shift, "ende": en[b] + shift})
            shots.append({"i": i, "start": words[0]["start"], "sprech_ende": words[-1]["ende"], "words": words})
        else:
            shots.append({"i": i, "start": None, "words": []})
    total_raw = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                      str(raw_mp3)], capture_output=True, text=True).stdout)
    # Stumme Einstellungen: beginnen am Sprechende der vorherigen + 0.05
    for k, sh in enumerate(shots):
        if sh["start"] is None:
            prev = shots[k - 1]
            sh["start"] = prev["sprech_ende"] + 0.05
            sh["sprech_ende"] = sh["start"]
    # Schnittzeitpunkte: Einstellung startet kurz vor ihrem ersten Wort (Schnitt auf dem Wort)
    for k, sh in enumerate(shots):
        sh["schnitt"] = 0.0 if k == 0 else max(shots[k - 1]["sprech_ende"] - 0.0, sh["start"] - 0.06)
    total = total_raw + shift + 0.8
    for k, sh in enumerate(shots):
        sh["ende"] = shots[k + 1]["schnitt"] if k + 1 < len(shots) else total
    # Audio mit Pausen zusammensetzen
    vo = outdir / "vo.wav"
    if pausen:
        filt, inputs, last, segs = [], [], 0.0, []
        for n, (t0, p) in enumerate(pausen):
            segs.append(f"[0:a]atrim={last}:{t0},asetpts=PTS-STARTPTS[s{n}]")
            segs.append(f"aevalsrc=0:d={p}:s=44100:c=stereo[p{n}]")
            last = t0
        segs.append(f"[0:a]atrim={last},asetpts=PTS-STARTPTS[s{len(pausen)}]")
        order = "".join(f"[s{n}][p{n}]" for n in range(len(pausen))) + f"[s{len(pausen)}]"
        segs.append(f"{order}concat=n={2*len(pausen)+1}:v=0:a=1[out]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw_mp3), "-filter_complex", ";".join(segs),
                        "-map", "[out]", "-ac", "2", "-ar", "44100", str(vo)], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw_mp3), "-ac", "2", "-ar", "44100", str(vo)], check=True)
    timing = {"gesamt": total, "shots": shots}
    (outdir / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
    return timing


if __name__ == "__main__":
    import sys, importlib.util
    ep_path = pathlib.Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location("episode", ep_path); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep)
    t = build(ep, ep_path.parent / "audio", force="--neu" in sys.argv)
    print("Dauer", round(t["gesamt"], 2), "s,", len(t["shots"]), "Einstellungen")
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import stimmen  # Figurenstimmen einsetzen (Einstellungen mit stimme="...")
    n = stimmen.anwenden(ep, ep_path.parent.resolve())
    if n:
        print(n, "Zeilen mit Figurenstimmen, Dauer", round(json.loads((ep_path.parent / "audio/timing.json").read_text())["gesamt"], 2), "s")
