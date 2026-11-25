"""Automatischer Schnitt für CODE ROT.

python cut.py <folge>/episode.py [--nur-plates] [--von N --bis M]
Voraussetzungen: <folge>/audio/timing.json (vo.py), <folge>/bg/*.png (Blender), assets/sfx (sfx.py)
Ergebnis: <folge>/export/<folge>.mp4
"""
import json, hashlib, pathlib, subprocess, sys, importlib.util, math, re, os
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose
import animator

ROOT = pathlib.Path(__file__).resolve().parent.parent
FPS = 30
W, H = 1080, 1920
ROT_ASS, GELB_ASS = "&H002A2AFF&", "&H001ED2FF&"  # BGR
SFX_PEGEL = {"whoosh": -9, "impact": -10, "tick": -12, "heartbeat": -11, "static": -16, "funk": -12, "atem": -8,
             "stimmen": -12, "feuer": -11, "tuer": -12, "schuesse": -10, "alarm": -14, "drone_hit": -14, "schrei": -10,
             "feuerwerk": -9}


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError(" ".join(map(str, cmd))[:400] + "\n" + r.stderr[-2000:])
    return r


# ---------------------------------------------------------------- Intro-Streifen
class Streifen:
    """Spind-Streifen (orthografisch). Zelle i hat Mitte bei (1.2 + 2i) Einheiten, Bildhöhe = 4.6 Einheiten."""

    def __init__(self, png):
        self.png = png
        w, h = map(int, sh(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(png)])
                   .stdout.strip().split(","))
        self.scale = H / h
        self.w = int(round(w * self.scale)); self.h = H

    def mitte_px(self, i):
        return (1.2 + 2 * i) * self.h / 4.6

    def crop_x(self, i):
        return max(0, min(self.w - W, self.mitte_px(i) - W / 2))

    def zelle_png(self, i, out):
        if not out.exists():
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(self.png), "-vf",
                f"scale={self.w}:{self.h},crop={W}:{H}:{self.crop_x(i):.0f}:0", str(out)])
        return out


# ---------------------------------------------------------------- Plates
def plate_spec(shot, folge, streifen, tmp):
    bg = shot["bg"]
    spec = {k: shot[k] for k in ("tint", "titel", "untertitel", "ringe", "bgfilter") if shot.get(k)}
    figs = []
    for f in shot["figuren"]:
        f = dict(f); f["src"] = str(folge / "svg" / f["src"]); figs.append(f)
    if bg.startswith("svg:"):
        spec["bg"] = str(folge / "svg" / (bg[4:] + ".svg"))
    elif bg.startswith("intro_zelle:"):
        spec["bg"] = str(streifen.zelle_png(int(bg.split(":")[1]), tmp / f"zelle_{bg.split(':')[1]}.png"))
    else:
        p = folge / "bg" / f"{bg}.png"
        if not p.exists():
            raise FileNotFoundError(p)
        spec["bg"] = str(p)
        if not bg.startswith("kabine"):
            spec["himmel"] = True
    spec["figuren"] = figs
    return spec


def overlay_spec(shot):
    spec = {"overlay": True}
    if shot.get("logo"):
        spec["logo"] = "CODE ROT"
    if shot.get("uhr"):
        spec["uhr"] = shot["uhr"]
    if shot.get("regeln") is not None and shot.get("regeln") is not False:
        n = shot["regeln"]
        spec["regeln"] = {"kopf": "Deine Befehle", "zeilen": shot["_befehle"][:n] or [" "]}
    if shot["bg"] == "intro":
        spec["linie"] = True
    return spec if len(spec) > 1 else None


def render_cached(spec, out):
    key = hashlib.md5(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:10]
    stamp = out.with_suffix(".key")
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return out
    compose.render(spec, str(out)); stamp.write_text(key)
    return out


# ---------------------------------------------------------------- Bewegung
def zoompan_expr(move, n):
    N = max(n, 1)
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if move == "zoom_in":
        return f"1+0.08*on/{N}", cx, cy
    if move == "zoom_schnell":
        return f"1+0.22*on/{N}", cx, cy
    if move == "zoom_out":
        return f"1.14-0.12*on/{N}", cx, cy
    if move == "pan_r":
        return "1.14", f"(iw-iw/zoom)*on/{N}", cy
    if move == "pan_l":
        return "1.14", f"(iw-iw/zoom)*(1-on/{N})", cy
    if move == "pan_hoch":
        return "1.14", cx, f"(ih-ih/zoom)*(1-on/{N})"
    if move == "shake":
        return (f"1.07+0.03*on/{N}", f"{cx}+22*sin(on*1.9)+14*sin(on*3.7)", f"{cy}+18*cos(on*2.3)+10*sin(on*5.1)")
    if move == "shake_stark":
        return (f"1.12", f"{cx}+70*exp(-on/9)*sin(on*2.7)+12*sin(on*1.3)", f"{cy}+60*exp(-on/9)*cos(on*3.1)+10*sin(on*1.7)")
    return "1.02", cx, cy  # statisch


def clip(k, shot, t0, t1, plate, ov, streifen, out):
    f0, f1 = round(t0 * FPS), round(t1 * FPS)
    n = max(f1 - f0, 1); dur = n / FPS
    move = shot["move"]
    filt, inputs = [], []
    if move.startswith("whip:"):
        a, b = map(int, move.split(":")[1:])
        xa, xb = streifen.crop_x(a), streifen.crop_x(b)
        inputs = ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", str(streifen.png)]
        # schneller Schwenk in den ersten 60 % mit Ease-out, dann leichtes Nachdriften
        ex = f"{xa}+({xb}-{xa})*(1-pow(1-min(t/({dur}*0.6)\\,1)\\,3))"
        filt.append(f"[0:v]scale={streifen.w}:{streifen.h},crop={W}:{H}:x='{ex}':y=0,tmix=frames=4:weights='1 1 1 1',"
                    f"eq=brightness='0.04*sin(t*18)':eval=frame[v0]")
    else:
        inputs = ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", str(plate)]
        z, x, y = zoompan_expr(move, n)
        filt.append(f"[0:v]scale={W*2}:{H*2},zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},"
                    f"trim=end_frame={n}[v0]")
    cur = "v0"
    if shot.get("blitz"):
        farbe = "0xFF8A2A" if shot["blitz"] == "orange" else "white"
        filt.append(f"[{cur}]fade=t=in:st=0:d=0.18:color={farbe}[vb]"); cur = "vb"
    if shot.get("ende_blitz"):
        filt.append(f"[{cur}]fade=t=out:st={max(0, dur-0.15):.3f}:d=0.15:color=white[ve]"); cur = "ve"
    if shot.get("ende_schwarz"):
        filt.append(f"[{cur}]fade=t=out:st={max(0, dur-0.5):.3f}:d=0.5:color=black[vs]"); cur = "vs"
    if ov:
        inputs += ["-i", str(ov)]
        filt.append(f"[{cur}][1:v]overlay=0:0:format=auto[vo]"); cur = "vo"
    filt.append(f"[{cur}]format=yuv420p,setsar=1[vout]")
    sh(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[vout]",
        "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "17", str(out)])
    return out


# ---------------------------------------------------------------- Untertitel (ASS)
def ass_zeit(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_text(chunk):
    out = []
    for w in chunk:
        txt = w.upper().replace("{", "(").replace("}", ")")
        def farbe(m, c):
            return "{\\c" + c + "}" + m.group(1) + "{\\c&H00FFFFFF&}"
        txt = re.sub(r"\*(.+?)\*", lambda m: farbe(m, ROT_ASS), txt)
        txt = re.sub(r"_(.+?)_", lambda m: farbe(m, GELB_ASS), txt)
        out.append(txt)
    return " ".join(out)


def chunks(words, max_w=3, max_c=15):
    out, cur = [], []
    for w in words:
        plain = re.sub(r"[*_]", "", w["w"])
        if cur and (len(cur) >= max_w or len(" ".join(re.sub(r"[*_]", "", x["w"]) for x in cur + [w])) > max_c):
            out.append(cur); cur = []
        cur.append(w)
        if plain.rstrip("“\"").endswith((".", ",", ":", "?", "!")):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def ass_datei(ep, timing, out):
    kopf = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat Black,100,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    zeilen = []
    shots = timing["shots"]
    # offene Markierungen über mehrere Wörter auflösen: pro Shot Markup auf Wortebene normalisieren
    for k, s in enumerate(shots):
        words = s["words"]
        if not words:
            continue
        # Markierungen über mehrere Wörter (*Köpfe runter!*) auf jedes Wort einzeln verteilen
        txt = ep.SHOTS[k]["text"]
        for mk in ("*", "_"):
            txt = re.sub(re.escape(mk) + r"(.+?)" + re.escape(mk),
                         lambda m: " ".join(f"{mk}{w}{mk}" for w in m.group(1).split()), txt)
        toks = txt.split()
        norm = [dict(w, w=t) for w, t in zip(words, toks)] if len(toks) == len(words) else words
        shot_ende = s["ende"]
        cs = chunks(norm, 2, 12) if AGGR else chunks(norm)
        for j, c in enumerate(cs):
            a = c[0]["start"]
            b = cs[j + 1][0]["start"] if j + 1 < len(cs) else min(shot_ende + 0.25, c[-1]["ende"] + 0.45)
            if j + 1 >= len(cs) and k + 1 < len(shots) and shots[k + 1]["words"]:
                b = min(b, shots[k + 1]["words"][0]["start"])
            if j + 1 >= len(cs) and k + 1 < len(shots) and ep.SHOTS[k + 1].get("titel"):
                b = min(b, shots[k + 1]["schnitt"])  # Titelkarte frei halten
            pop = "{\\an5\\pos(540,1330)\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)}"
            if AGGR:
                rot = any("*" in x["w"] for x in c)
                pop = ("{\\an5\\pos(540,1330)\\fscx55\\fscy55\\t(0,70,\\fscx125\\fscy125)\\t(70,150,\\fscx112\\fscy112)"
                       + ("\\frz-4" if rot else "") + "}")
            zeilen.append(f"Dialogue: 0,{ass_zeit(a)},{ass_zeit(b)},Cap,,0,0,0,,{pop}{ass_text([x['w'] for x in c])}")
    if AGGR:
        kopf = kopf.replace("Montserrat Black,100,", "Montserrat Black,112,")
    out.write_text(kopf + "\n".join(zeilen) + "\n", encoding="utf-8")
    return out


# ---------------------------------------------------------------- Audio
ATMO_PEGEL = {"atmo_meer": -25, "atmo_stadt": -25, "atmo_nacht": -17}  # breitbandiges Meeresrauschen deckt Sprache stärker zu


def mix(ep, timing, folge, out_wav, ohne_vo=False, norm=True, vo=None):
    sfx_dir = ROOT / "assets/sfx"; real = ROOT / "assets/sfx_real"
    def sfx(name):  # echte Aufnahme bevorzugen, sonst synthetisch
        return real / f"{name}.wav" if (real / f"{name}.wav").exists() else sfx_dir / f"{name}.wav"
    shots = timing["shots"]; total = timing["gesamt"]
    atmo_name = getattr(ep, "ATMO", "atmo_nacht")
    atmo = real / f"{atmo_name}.wav" if (real / f"{atmo_name}.wav").exists() else sfx_dir / "atmo.wav"
    inputs = ["-i", str(vo or folge / "audio/vo.wav"), "-stream_loop", "-1", "-i", str(atmo)]
    filt = [f"[1:a]atrim=0:{total:.2f},volume={ATMO_PEGEL.get(atmo_name, -17) if atmo.parent == real else -20}dB"]
    # Atmo-Loch bei "Stille"
    stille = [(sh_["schnitt"], sh_["ende"]) for sh_, sp in zip(shots, ep.SHOTS) if sp.get("stille")]
    vol_expr = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in stille) or "0"
    filt[0] += f",volume='if({vol_expr},0.08,1)':eval=frame[atmo]"
    labels = ["[0:a]", "[atmo]"]
    n = 2
    for sh_, sp in zip(shots, ep.SHOTS):
        s = sp.get("sfx")
        if not s:
            continue
        inputs += ["-i", str(sfx(s))]
        d = max(0, int((sh_["schnitt"] - (0.25 if s == "whoosh" else 0)) * 1000))
        cap = min(6.0 if s == "feuerwerk" else 4.0, (sh_["ende"] - sh_["schnitt"]) + 1.2)
        filt.append(f"[{n}:a]atrim=0:{cap:.2f},afade=t=out:st={max(0, cap - 0.4):.2f}:d=0.4,"
                    f"volume={SFX_PEGEL.get(s, -10) - (6 if sfx(s).parent == real else 0)}dB,adelay={d}|{d}[s{n}]")
        labels.append(f"[s{n}]"); n += 1
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,"
                f"atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    # VO ist [0:a] und bestimmt mit duration=first die Länge -> VO vorher auf Gesamtlänge auffüllen
    # Stimme als Schlüssel für Ducking: Hintergrund + Geräusche werden leiser, sobald gesprochen wird
    filt.insert(0, f"[0:a]apad=whole_dur={total:.2f},asplit=2[vo0][key]")
    filt.insert(1, f"[vo0]{'volume=0' if ohne_vo else 'anull'}[vo]")
    ln = ",loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false" if norm else ""  # Limiter: keine Übersteuerung
    bett = labels[1:]
    # zwei Busse: Atmosphäre (sanft geduckt) und Effekte (stark geduckt, damit Akzente kein Wort verdecken)
    fx = bett[1:]
    filt[0] = filt[0].replace("asplit=2[vo0][key]", "asplit=3[vo0][key][key2]")
    if fx:
        filt[-1] = (f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0,apad=whole_dur={total:.2f},atrim=0:{total:.2f}[fxb];"
                    f"[fxb][key2]sidechaincompress=threshold=0.01:ratio=12:attack=4:release=250:makeup=1[fxd];")
    else:
        filt[-1] = f"anullsrc=r=44100:cl=stereo,atrim=0:{total:.2f}[fxd];[key2]anullsink;"
    filt[-1] += (f"{bett[0]}[key]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350:makeup=1[atd];"
                 f"[vo][atd][fxd]amix=inputs=3:normalize=0:duration=first,atrim=0:{total:.2f}{ln}[aout]")
    sh(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[aout]",
        "-ar", "48000", "-ac", "2", str(out_wav)])
    return out_wav


# ---------------------------------------------------------------- Ablauf
def main():
    ep_path = pathlib.Path(sys.argv[1]).resolve(); folge = ep_path.parent
    spec = importlib.util.spec_from_file_location("episode", ep_path); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep)
    timing = json.loads((folge / "audio/timing.json").read_text())
    tmp = folge / "build"; tmp.mkdir(exist_ok=True)
    (folge / "export").mkdir(exist_ok=True)
    sp = folge / "bg/spinde_streifen.png"
    streifen = Streifen(sp if sp.exists() else folge / "test/spinde_streifen.png")
    shots = timing["shots"]
    assert len(shots) == len(ep.SHOTS)
    von = int(sys.argv[sys.argv.index("--von") + 1]) if "--von" in sys.argv else 0
    bis = int(sys.argv[sys.argv.index("--bis") + 1]) if "--bis" in sys.argv else len(shots) - 1

    # 1) Plates + Overlays (parallel, Chromium)
    def mach(k):
        s = dict(ep.SHOTS[k]); s["_befehle"] = getattr(ep, "BEFEHLE", [])
        plate = None
        if s["bg"] != "intro":
            plate = render_cached(plate_spec(s, folge, streifen, tmp), tmp / f"plate_{k:03d}.png")
        ov = overlay_spec(s)
        ovp = render_cached(ov, tmp / f"ov_{k:03d}.png") if ov else None
        return k, plate, ovp
    with ThreadPoolExecutor(4) as ex:
        res = dict((k, (p, o)) for k, p, o in ex.map(mach, range(von, bis + 1)))
    print("Plates fertig:", len(res))
    if "--nur-plates" in sys.argv:
        return

    # 2) Clips
    def mach_clip(k):
        s = ep.SHOTS[k]; t = shots[k]
        return clip(k, s, t["schnitt"], t["ende"], res[k][0], res[k][1], streifen, tmp / f"clip_{k:03d}.mp4")
    with ThreadPoolExecutor(3) as ex:
        clips = list(ex.map(mach_clip, range(von, bis + 1)))
    print("Clips fertig:", len(clips))

    # 3) Zusammenfügen, Untertitel, Ton
    liste = tmp / "liste.txt"
    liste.write_text("".join(f"file '{c}'\n" for c in clips))
    roh = tmp / "roh.mp4"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(roh)])
    ass = ass_datei(ep, timing, tmp / "untertitel.ass")
    audio = mix(ep, timing, folge, tmp / "mix.wav")
    out = folge / "export" / f"{folge.name}.mp4"
    fonts = ROOT / "assets/fonts"
    t_von = shots[von]["schnitt"]
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(roh), "-ss", f"{t_von:.3f}", "-i", str(audio),
        "-vf", f"setpts=PTS-STARTPTS+{t_von:.3f}/TB,ass={ass}:fontsdir={fonts},setpts=PTS-STARTPTS",
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    print("FERTIG", out)

# ---------------------------------------------------------------- Animator (bewegte Fassung)
FEUER_BG = {"boden_feuer", "nase_feuer"}


AGGR = "--aggressiv" in sys.argv   # Schnitt für sehr kurze Aufmerksamkeitsspanne
TEMPO = float(os.environ.get("TEMPO", "1.1"))  # Beschleunigung der Erzählung im aggressiven Modus
PUNCH_STUFEN = [1.0, 1.12, 1.0, 1.18]  # dezenter (Nutzerwunsch: nicht zu oft rein und raus)
PUNCH_ABSTAND = 1.6  # mindestens so viele Sekunden zwischen zwei Zoomsprüngen, höchstens einer je Einstellung


def aggressiv_extras(k, s, t, dauer, prev_s):
    """Punch-ins (harte Bildsprünge) höchstens jede zweite Einstellung an einer Wortgrenze, Stöße auf roten Wörtern,
    kurzer Blitz bei Ortswechsel."""
    ex = {}
    if s.get("titel") or s.get("stille"):
        return ex
    rel = [(w["start"] - t["schnitt"], w) for w in t["words"]]
    punches, letzte, stufe = [], 0.0, 1 + 2 * ((k // 2) % 2)  # 1.12 oder 1.18 im Wechsel
    kandidaten = [r for r, _ in rel[1:]] or ([dauer / 2] if dauer >= 1.2 else [])
    for c in kandidaten:
        if punches:
            break
        if c - letzte >= PUNCH_ABSTAND * 0.5 and dauer - c >= 0.5 and dauer >= 1.3 and k % 2 == 0:
            z = PUNCH_STUFEN[stufe % len(PUNCH_STUFEN)]; stufe += 1
            dx = ((k * 37 + stufe * 53) % 61 - 30) * (z - 1) * 4
            punches.append([round(c, 3), z, round(dx, 1), 0]); letzte = c
    if dauer >= 2.2 and not punches:
        punches.append([round(min(dauer * 0.5, dauer - 0.4), 3), PUNCH_STUFEN[stufe % 4], 0, 0])
    ex["punches"] = punches
    ex["stoesse"] = [[round(max(r, 0), 3), 0.28] for r, w in rel if "*" in w["w"]]
    ort = (s.get("anim") or s["bg"]); ort_vorher = (prev_s.get("anim") or prev_s["bg"]) if prev_s else None
    if ort != ort_vorher and not s.get("blitz"):
        ex["blitz_kurz"] = True
    return ex


STILLE_MAX = 0.7    # stumme Einstellungen (z. B. Titelkarte) höchstens so lang
LUECKE_MAX = 0.22   # Sprechpause zwischen zwei Einstellungen höchstens so lang
ENDE_NACH = 0.3     # nach dem letzten Wort: sofort zurück zum Anfang (Loop)


def stille_kuerzen(timing, vo_in, vo_out):
    """Tote Luft raus: lange stumme Einstellungen und Pausen zwischen Einstellungen kürzen, Ende direkt nach dem
    letzten Wort (nahtloser Loop). Schneidet die Stimme mit und verschiebt alle Zeiten."""
    shots = timing["shots"]; schnitte = []
    for k, sh_ in enumerate(shots):
        if not sh_["words"] and sh_["ende"] - sh_["schnitt"] > STILLE_MAX:
            schnitte.append((sh_["schnitt"] + STILLE_MAX, sh_["ende"]))
        if k + 1 < len(shots) and sh_["words"] and shots[k + 1]["words"]:
            a, b = sh_["words"][-1]["ende"], shots[k + 1]["words"][0]["start"]
            if b - a > LUECKE_MAX + 0.05:
                schnitte.append((a + LUECKE_MAX * 0.6, b - LUECKE_MAX * 0.4))
    letztes = max(w["ende"] for sh_ in shots for w in sh_["words"])
    if timing["gesamt"] - letztes > ENDE_NACH:
        schnitte.append((letztes + ENDE_NACH, timing["gesamt"]))
    schnitte = sorted((a, b) for a, b in schnitte if b > a + 0.02)

    def neu(t):
        d = 0.0
        for a, b in schnitte:
            if t >= b:
                d += b - a
            elif t > a:
                d += t - a
        return t - d
    import numpy as np
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(vo_in), "-ac", "2", "-ar", "44100", "-f", "f32le", "-"],
                       capture_output=True, check=True)
    y = np.frombuffer(r.stdout, np.float32).reshape(-1, 2)
    teile, cur = [], 0
    for a, b in schnitte:
        ia, ib = int(a * 44100), int(b * 44100)
        teile.append(y[cur:ia]); cur = ib
    teile.append(y[cur:])
    z = np.concatenate(teile)
    n = int(0.004 * 44100)  # winzige Blenden gegen Knackser an den Schnittstellen
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", str(vo_out)], input=z.astype(np.float32).tobytes(), check=True)
    out = dict(timing, gesamt=neu(timing["gesamt"]), shots=[])
    for sh_ in shots:
        out["shots"].append(dict(sh_, schnitt=neu(sh_["schnitt"]), ende=neu(sh_["ende"]), start=neu(sh_["start"]),
                                 sprech_ende=neu(sh_["sprech_ende"]),
                                 words=[dict(w, start=neu(w["start"]), ende=neu(w["ende"])) for w in sh_["words"]]))
    print(f"Stille gekürzt: {sum(b - a for a, b in schnitte):.1f} s an {len(schnitte)} Stellen", flush=True)
    return out


def skaliere_timing(timing, f):
    def sk(x):
        return round(x / f, 4)
    neu = dict(timing, gesamt=sk(timing["gesamt"]), shots=[])
    for s in timing["shots"]:
        neu["shots"].append(dict(s, schnitt=sk(s["schnitt"]), ende=sk(s["ende"]),
                                 words=[dict(w, start=sk(w["start"]), ende=sk(w["ende"])) for w in s["words"]]))
    return neu


def gruppen_anpassen(ep, timing, folge, gruppen_alt):
    """Startbilder der 3D-Sequenzen aus der aktuellen Zeitachse neu bestimmen. Ist eine Gruppe jetzt länger als
    gerendert (z. B. durch eine langsamere Figurenstimme), läuft sie entsprechend langsamer statt einzufrieren."""
    spec = importlib.util.spec_from_file_location("anim_render", pathlib.Path(__file__).parent / "anim_render.py")
    ar = importlib.util.module_from_spec(spec); spec.loader.exec_module(ar)
    neu = ar.gruppen(ep, timing)
    for name, g in neu.items():
        d = folge / "anim" / name
        nf = len(list(d.glob("f_*.png"))) if d.exists() else 0
        if g["loop"] or nf == 0:
            continue
        s = min(1.0, (nf - 1) / max(g["frames"] - 2, 1))
        g["tempo"] = s
        g["start"] = {k: int(round(v * s)) for k, v in g["start"].items()}
    return neu


def animierter_clip(k, ep, folge, shots, gruppen, streifen, tmp, prev):
    s = dict(ep.SHOTS[k]); t = shots[k]
    f0, f1 = round(t["schnitt"] * FPS), round(t["ende"] * FPS)
    n = max(f1 - f0, 1); dauer = n / FPS
    bgname = s["bg"]; anim = getattr(ep, "ANIM_SHOTS", {}).get(k)
    bg = None
    if anim and (folge / "anim" / anim / "f_0001.png").exists():
        g = gruppen[anim]
        nf = len(list((folge / "anim" / anim).glob("f_*.png")))
        st = g["start"].get(k, g["start"].get(str(k)))
        bg = {"typ": "seq", "muster": f"file://{folge}/anim/{anim}/f_####.png", "start": st,
              "n": nf, "loop": g["loop"], "tempo": g.get("tempo", 1.0)}
        szene = ep.ANIM[anim]["szene"]
        bg["himmel"] = szene == "rollfeld"
    elif bgname.startswith("svg:"):
        bg = {"typ": "svg", "src": str(folge / "svg" / (bgname[4:] + ".svg"))}; szene = "svg"
    elif bgname.startswith("intro_zelle:"):
        bg = {"typ": "bild", "src": str(streifen.zelle_png(int(bgname.split(":")[1]), tmp / f"zelle_{bgname.split(':')[1]}.png"))}
        szene = "titel"
    elif bgname == "intro":
        bg = {"typ": "bild", "src": str(streifen.zelle_png(6, tmp / "zelle_6.png"))}; szene = "intro"
    else:
        bg = {"typ": "bild", "src": str(folge / "bg" / f"{bgname}.png"), "himmel": not bgname.startswith("kabine")}
        szene = "kabine" if bgname.startswith("kabine") else "rollfeld"
    # Partikel
    if "fx" in s:
        fx = s["fx"]
    elif bgname.startswith("svg:tv"):
        fx = animator.FX_STANDARD["tv"]
    elif bgname in FEUER_BG and not (anim == "nase_feuer" and k < 41):
        fx = animator.FX_STANDARD["feuer"]
    elif szene == "kabine":
        fx = animator.FX_STANDARD["kabine_zugriff" if "zugriff" in bgname or "ausstieg" in bgname else "kabine"]
    elif szene in animator.FX_STANDARD:
        fx = animator.FX_STANDARD[szene]
    else:
        fx = animator.FX_STANDARD["rollfeld"] if szene != "svg" else []
    # HUD
    hud = {"logo": bool(s.get("logo")), "linie": bgname == "intro", "ringe": bool(s.get("ringe")),
           "titel": s.get("titel"), "untertitel": s.get("untertitel", "")}
    if s.get("uhr"):
        hud["uhr"] = s["uhr"]; hud["uhr_neu"] = (prev or {}).get("uhr") != s["uhr"]
    if s.get("regeln") is not None and s.get("regeln") is not False:
        nr = s["regeln"]; pr = (prev or {}).get("regeln")
        hud["regeln"] = {"zeilen": ep.BEFEHLE[:nr] or [], "neu": isinstance(pr, int) and nr > pr}
        if getattr(ep, "BEFEHLE_KOPF", None):
            hud["regeln"]["kopf"] = ep.BEFEHLE_KOPF
        hud["regeln_neu_box"] = not isinstance(pr, int)
    if AGGR:
        s.update(aggressiv_extras(k, s, t, dauer, prev))
        s["ende_schwarz"] = False  # Loop: letztes Bild geht direkt in den Kaltstart über
    out = tmp / f"anim_{k:03d}.mp4"
    html = animator.baue(s, k, dauer, folge, bg, hud, fx)
    key = hashlib.md5((html + str(n)).encode()).hexdigest()[:12]
    stamp = out.with_suffix(".key")
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return out
    animator.render(html, out, n)
    stamp.write_text(key)
    return out


def main_animiert():
    ep_path = pathlib.Path(sys.argv[1]).resolve(); folge = ep_path.parent
    spec = importlib.util.spec_from_file_location("episode", ep_path); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep)
    timing = json.loads((folge / "audio/timing.json").read_text())
    gruppen = json.loads((folge / "anim/gruppen.json").read_text())
    tmp = folge / ("build_aggr" if AGGR else "build"); tmp.mkdir(exist_ok=True); (folge / "export").mkdir(exist_ok=True)
    vo = None
    if AGGR:  # tote Luft raus, Erzählung beschleunigen (Tonhöhe bleibt), Timing mitskalieren
        timing = stille_kuerzen(timing, folge / "audio/vo.wav", tmp / "vo_kurz.wav")
        timing = skaliere_timing(timing, TEMPO)
        vo = tmp / "vo_schnell.wav"
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "vo_kurz.wav"), "-af", f"atempo={TEMPO}", str(vo)])
    gruppen = gruppen_anpassen(ep, timing, folge, gruppen)
    sp = folge / "bg/spinde_streifen.png"
    streifen = Streifen(sp)
    shots = timing["shots"]
    von = int(sys.argv[sys.argv.index("--von") + 1]) if "--von" in sys.argv else 0
    bis = int(sys.argv[sys.argv.index("--bis") + 1]) if "--bis" in sys.argv else len(shots) - 1
    def mach(k):
        return animierter_clip(k, ep, folge, shots, gruppen, streifen, tmp, ep.SHOTS[k - 1] if k > 0 else None)
    with ThreadPoolExecutor(int(os.environ.get("ANIM_JOBS", "3"))) as ex:
        clips = list(ex.map(mach, range(von, bis + 1)))
    print("Animierte Clips fertig:", len(clips), flush=True)
    liste = tmp / "liste_anim.txt"
    liste.write_text("".join(f"file '{c}'\n" for c in clips))
    roh = tmp / "roh_anim.mp4"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(roh)])
    ass = ass_datei(ep, timing, tmp / "untertitel.ass")
    audio = mix(ep, timing, folge, tmp / "mix.wav", vo=vo)
    name = folge.name + ("_aggressiv" if AGGR else "")
    out = folge / "export" / (f"{name}.mp4" if von == 0 and bis == len(shots) - 1 else f"{name}_teil_{von}-{bis}.mp4")
    if AGGR:
        out_final, out = out, tmp / "haupt.mp4"
    fonts = ROOT / "assets/fonts"
    t_von = shots[von]["schnitt"]
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(roh), "-ss", f"{t_von:.3f}", "-i", str(audio),
        "-vf", f"setpts=PTS-STARTPTS+{t_von:.3f}/TB,ass={ass}:fontsdir={fonts},setpts=PTS-STARTPTS",
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    if AGGR:
        ks = getattr(ep, "KALTSTART", None)
        hook_clips = []
        if ks and von == 0:  # Clips des Höhepunkts (auch bei Teil-Vorschau) bereitstellen
            with ThreadPoolExecutor(int(os.environ.get("ANIM_JOBS", "3"))) as ex:
                hook_clips = list(ex.map(mach, range(ks["shot"], min(ks["shot"] + 4, len(shots)))))
        kaltstart(ep, folge, timing, hook_clips, out, tmp, out_final, von, vo)
        out = out_final
    print("FERTIG", out)


def kaltstart(ep, folge, timing, hook_clips, haupt, tmp, out, von, vo):
    """Hook: ~1,5 s vom Höhepunkt (ohne Stimme) mit Hook-Text, Rückspul-Glitch, dann die Folge.
    Darüber ein Fortschrittsbalken über die ganze Länge."""
    ks = getattr(ep, "KALTSTART", None)
    fonts = ROOT / "assets/fonts"; shots = timing["shots"]
    teile = []
    if ks and von == 0:
        t_ton = shots[ks["shot"]]["schnitt"] + ks.get("versatz", 0.0); d = ks.get("dauer", 1.5)
        (tmp / "hook_liste.txt").write_text("".join(f"file '{c}'\n" for c in hook_clips))
        roh = tmp / "hook_roh.mp4"
        sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "hook_liste.txt"),
            "-c", "copy", str(roh)])
        t0 = ks.get("versatz", 0.0)
        bett = mix(ep, timing, folge, tmp / "bett.wav", ohne_vo=True, vo=vo)
        ev = []
        for i, z in enumerate(ks["text"].split("|")):
            a = i * 0.3
            txt = re.sub(r"\*(.+?)\*", lambda m: "{\\c" + ROT_ASS + "}" + m.group(1) + "{\\c&H00FFFFFF&}", z.upper())
            ev.append(f"Dialogue: 0,{ass_zeit(a)},{ass_zeit(d + 0.4)},Hook,,0,0,0,,"
                      "{\\an5\\pos(540," + str(1180 + i * 150) + ")\\fscx" + ("100" if i == 0 else "50") + "\\fscy" + ("100" if i == 0 else "50") + "\\t(0,80,\\fscx118\\fscy118)\\t(80,160,\\fscx105\\fscy105)}" + txt)
        ass = tmp / "hook.ass"
        ass.write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Montserrat Black,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,10,6,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n", encoding="utf-8")
        hook = tmp / "hook.mp4"; glitch = tmp / "glitch.mp4"
        whoosh = ROOT / "assets/sfx/whoosh.wav"
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", str(roh),
            "-ss", f"{t_ton:.3f}", "-t", f"{d:.3f}", "-i", str(bett),
            "-vf", f"eq=saturation=1.25:contrast=1.08,ass={ass}:fontsdir={fonts}",
            "-af", "volume=2dB", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-c:a", "aac", "-ar", "48000", "-ac", "2", str(hook)])
        # Rückspulen: Hook-Bilder rückwärts, 4x schnell, RGB-Versatz + Rauschen; Ton rückwärts + Whoosh
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(hook), "-i", str(whoosh), "-filter_complex",
            "[0:v]reverse,setpts=PTS/4,fps=30,rgbashift=rh=-18:bh=18,noise=alls=40:allf=t,eq=brightness=0.06[v];"
            "[0:a]areverse,atempo=2,atempo=2,volume=-6dB[r];[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:0.6,volume=-4dB[w];"
            "[r][w]amix=inputs=2:normalize=0:duration=longest,atrim=0:0.38[a]",
            "-map", "[v]", "-map", "[a]", "-t", "0.38", "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2", str(glitch)])
        teile = [hook, glitch]
    teile.append(haupt)
    gesamt = sum(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(x)], capture_output=True, text=True).stdout) for x in teile)
    ein = []
    for x in teile:
        ein += ["-i", str(x)]
    n = len(teile)
    fc = "".join(f"[{i}:v]fps=30,format=yuv420p,setsar=1[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];"
                 for i in range(n))
    fc += "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
    vorlauf = sum(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(x)], capture_output=True, text=True).stdout) for x in teile[:-1])
    ov = overlay_ass(ep, folge, tmp, vorlauf, gesamt)
    fc = fc.replace("concat=n=" + str(n) + ":v=1:a=1[cv][ca];", "concat=n=" + str(n) + ":v=1:a=1[cv0][ca];"
                    + f"[cv0]ass={ov}:fontsdir={fonts}[cv];")
    fc += (f"color=c=0xFF2A2A:s=1080x12:r=30[bar];[cv][bar]overlay=x='-W+W*t/{gesamt:.3f}':y=0:eval=frame:shortest=1[vout];"
           "[ca]alimiter=limit=0.84:level=false[aout]")
    sh(["ffmpeg", "-y", "-loglevel", "error", *ein, "-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(out)])
    if gesamt < 62:
        print(f"WARNUNG: nur {gesamt:.0f} s – für das TikTok-Creator-Rewards-Programm muss ein Video über 60 s lang sein",
              flush=True)
    posting(ep, folge, out, gesamt)


SERIE_TEXT = {
    "de": dict(teil="TEIL {n}", frage="Welche Einheit als Nächstes?", folgen="Folg für Teil {m}",
               versprechen="Das Ende sieht keiner kommen."),
    "en": dict(teil="PART {n}", frage="Which unit should be next?", folgen="Follow for part {m}",
               versprechen="Nobody sees the ending coming."),
    "es": dict(teil="PARTE {n}", frage="¿Qué unidad sigue?", folgen="Sígueme para la parte {m}",
               versprechen="Nadie ve venir el final."),
}


def folgen_nummer(folge):
    m = re.match(r"folge(\d+)", folge.name)
    return int(m.group(1)) if m else 0


def overlay_ass(ep, folge, tmp, vorlauf, gesamt):
    """„TEIL n“ direkt nach dem Kaltstart (Serie -> Profil -> weitere Folgen) und am Ende eine Frage an die Zuschauer
    (Kommentare) plus „Folg für Teil n+1“."""
    sp = getattr(ep, "SPRACHE", "de"); T = SERIE_TEXT.get(sp, SERIE_TEXT["de"]); n = folgen_nummer(folge)
    kopf = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Teil,Montserrat Black,54,&H00FFFFFF,&H00FFFFFF,&H002A2AFF,&H00000000,0,0,0,0,100,100,6,0,3,14,0,5,40,40,0,1
Style: Frage,Montserrat Black,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,8,5,5,60,60,0,1
Style: Versprechen,Montserrat ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,5,3,5,40,40,0,1
Style: Folgen,Montserrat Black,46,&H00FFFFFF,&H00FFFFFF,&H002A2AFF,&H00000000,0,0,0,0,100,100,4,0,3,12,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    if n:
        a = vorlauf + 0.15
        ev.append(f"Dialogue: 0,{ass_zeit(a)},{ass_zeit(a + 3.0)},Teil,,0,0,0,,{{\\an5\\pos(540,175)\\fad(120,200)}}"
                  + T["teil"].format(n=n, m=n + 1))
    # offene Schleife: Versprechen einer Wende -> Zuschauer bleiben bis zum Ende (Abschlussrate)
    ev.append(f"Dialogue: 0,{ass_zeit(vorlauf + 0.4)},{ass_zeit(vorlauf + 4.2)},Versprechen,,0,0,0,,"
              f"{{\\an5\\pos(540,262)\\fad(150,250)}}" + T["versprechen"])
    b = max(vorlauf, gesamt - 3.0)
    ev.append(f"Dialogue: 0,{ass_zeit(b)},{ass_zeit(gesamt)},Frage,,0,0,0,,{{\\an5\\pos(540,640)\\fscx70\\fscy70"
              f"\\t(0,140,\\fscx104\\fscy104)\\t(140,240,\\fscx100\\fscy100)}}" + T["frage"])
    if n:
        ev.append(f"Dialogue: 0,{ass_zeit(b + 0.5)},{ass_zeit(gesamt)},Folgen,,0,0,0,,{{\\an5\\pos(540,780)\\fad(150,0)}}"
                  + T["folgen"].format(n=n, m=n + 1))
    out = tmp / "overlay.ass"; out.write_text(kopf + "\n".join(ev) + "\n", encoding="utf-8")
    return out


HASHTAGS = {
    "de": "#coderot #spezialeinheit #wahregeschichte #geschichte #fürdich #fyp",
    "en": "#coderot #specialforces #truestory #history #fyp #foryou",
    "es": "#coderot #fuerzasespeciales #historiareal #historia #parati #fyp",
}
POST_TEXT = {
    "de": "Würdest du zurückkommen? 👀 Teil {n} von CODE ROT.",
    "en": "Would you make it back? 👀 Part {n} of CODE ROT.",
    "es": "¿Regresarías? 👀 Parte {n} de CODE ROT.",
}


def posting(ep, folge, mp4, dauer):
    """Begleittext zum Hochladen: Beschreibung, Hashtags, Vorschaubild, erster Kommentar."""
    sp = getattr(ep, "SPRACHE", "de"); n = folgen_nummer(folge)
    titel = next((s_["titel"] for s_ in ep.SHOTS if s_.get("titel")), "")
    einheit = re.sub(r"[*_]", "", titel).strip()
    import unicodedata
    tag = "#" + re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", einheit).encode("ascii", "ignore").decode().lower())
    hook = re.sub(r"[*_]", "", getattr(ep, "KALTSTART", {}).get("text", "")).replace("|", " ")
    T = SERIE_TEXT.get(sp, SERIE_TEXT["de"])
    txt = f"""# Posting – {folge.name} ({sp.upper()})

**Datei:** {mp4.name} · {dauer:.0f} s · 1080×1920

**Beschreibung (kopieren):**
{hook} {POST_TEXT.get(sp, POST_TEXT["de"]).format(n=n)} {tag} {HASHTAGS.get(sp, HASHTAGS["de"])}

**Vorschaubild:** Sekunde 0 (Kaltstart mit Hook-Text) – in TikTok als Cover wählen.

**Erster Kommentar (anpinnen):** {T["frage"]}

**Hinweise:** Video als Teil der Playlist „CODE ROT“ speichern · in den ersten 60 Minuten auf Kommentare antworten ·
optional einen Trend-Sound sehr leise (5–10 %) unterlegen.
"""
    (folge / "export" / f"POSTING_{sp}.md").write_text(txt, encoding="utf-8")



if __name__ == "__main__":
    main_animiert() if "--statisch" not in sys.argv else main()
