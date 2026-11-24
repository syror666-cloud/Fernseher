"""Automatischer Schnitt für CODE ROT.

python cut.py <folge>/episode.py [--nur-plates] [--von N --bis M]
Voraussetzungen: <folge>/audio/timing.json (vo.py), <folge>/bg/*.png (Blender), assets/sfx (sfx.py)
Ergebnis: <folge>/export/<folge>.mp4
"""
import json, hashlib, pathlib, subprocess, sys, importlib.util, math, re, os
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose

ROOT = pathlib.Path(__file__).resolve().parent.parent
FPS = 30
W, H = 1080, 1920
ROT_ASS, GELB_ASS = "&H002A2AFF&", "&H001ED2FF&"  # BGR
SFX_PEGEL = {"whoosh": -9, "impact": -6, "tick": -12, "heartbeat": -6, "static": -12, "funk": -9, "atem": -8,
             "stimmen": -10, "feuer": -8, "tuer": -5, "schuesse": -7, "alarm": -14, "drone_hit": -7, "schrei": -10}


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
        cs = chunks(norm)
        for j, c in enumerate(cs):
            a = c[0]["start"]
            b = cs[j + 1][0]["start"] if j + 1 < len(cs) else min(shot_ende + 0.25, c[-1]["ende"] + 0.45)
            if j + 1 >= len(cs) and k + 1 < len(shots) and shots[k + 1]["words"]:
                b = min(b, shots[k + 1]["words"][0]["start"])
            pop = "{\\an5\\pos(540,1330)\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)}"
            zeilen.append(f"Dialogue: 0,{ass_zeit(a)},{ass_zeit(b)},Cap,,0,0,0,,{pop}{ass_text([x['w'] for x in c])}")
    out.write_text(kopf + "\n".join(zeilen) + "\n", encoding="utf-8")
    return out


# ---------------------------------------------------------------- Audio
def mix(ep, timing, folge, out_wav):
    sfx_dir = ROOT / "assets/sfx"
    shots = timing["shots"]; total = timing["gesamt"]
    inputs = ["-i", str(folge / "audio/vo.wav"), "-i", str(sfx_dir / "atmo.wav")]
    filt = [f"[1:a]atrim=0:{total:.2f},volume=-20dB"]
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
        inputs += ["-i", str(sfx_dir / f"{s}.wav")]
        d = max(0, int((sh_["schnitt"] - (0.25 if s == "whoosh" else 0)) * 1000))
        filt.append(f"[{n}:a]volume={SFX_PEGEL.get(s, -10)}dB,adelay={d}|{d}[s{n}]")
        labels.append(f"[s{n}]"); n += 1
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,"
                f"atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    # VO ist [0:a] und bestimmt mit duration=first die Länge -> VO vorher auf Gesamtlänge auffüllen
    filt.insert(0, f"[0:a]apad=whole_dur={total:.2f}[vo]")
    labels[0] = "[vo]"
    filt[-1] = f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
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


if __name__ == "__main__":
    main()
