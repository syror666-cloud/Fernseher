"""Rendert alle 3D-Animationen einer Folge (Blender/EEVEE) als Bildsequenzen.

python anim_render.py <folge>/episode.py [--res 540x960] [--samples 8] [--nur name1,name2]
Ausgabe: <folge>/anim/<name>/f_####.png  und  <folge>/anim/<name>/info.json (Frames je Einstellung)
"""
import json, pathlib, subprocess, sys, importlib.util, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLENDER = "/home/user/tools/blender-4.2.3-linux-x64/blender"
SZENEN = {"rollfeld": "scene_rollfeld.py", "kabine": "scene_kabine.py", "spinde": "scene_spinde.py"}
FPS = 30


def lade(ep_path):
    spec = importlib.util.spec_from_file_location("episode", ep_path); ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep); return ep


def gruppen(ep, timing):
    """Pro Animation: Liste der Einstellungen + Frames. Fortlaufende Gruppen oder Schleifen."""
    shots = timing["shots"]; out = {}
    for name, cfg in ep.ANIM.items():
        idx = sorted(k for k, v in ep.ANIM_SHOTS.items() if v == name)
        if not idx:
            continue
        if cfg.get("loop"):
            n = int(cfg["loop"] * FPS)
            zuordnung = {}
            pos = 0
            for k in idx:  # jede Einstellung bekommt einen anderen Startpunkt in der Schleife
                d = round(shots[k]["ende"] * FPS) - round(shots[k]["schnitt"] * FPS)
                zuordnung[k] = pos % n; pos += d + 17
            out[name] = dict(frames=n, start={k: v for k, v in zuordnung.items()}, loop=True)
        else:
            f0 = round(shots[idx[0]]["schnitt"] * FPS)
            f1 = round(shots[idx[-1]]["ende"] * FPS)
            out[name] = dict(frames=f1 - f0 + 2, start={k: round(shots[k]["schnitt"] * FPS) - f0 for k in idx}, loop=False)
    return out


def job(ep, folge, name, g, res, samples):
    cfg = ep.ANIM[name]
    ziel = folge / "anim" / name; ziel.mkdir(parents=True, exist_ok=True)
    n = g["frames"]
    fertig = len(list(ziel.glob("f_*.png")))
    if fertig >= n:
        return "schon fertig"
    halb = cfg["szene"] != "spinde"  # halbe Bildrate + Bewegungsinterpolation
    nr = (n + 1) // 2 + 1 if halb else n
    keys = [{"f": round(t * (nr - 1)), "loc": list(loc), "ziel": list(z), "lens": lens} for t, loc, z, lens in cfg["keys"]]
    pfad = {"frames": nr, "offset": 0, "keys": keys, "shake": cfg.get("shake", 0)}
    pf = ziel / "pfad.json"; pf.write_text(json.dumps(pfad))
    args = list(cfg.get("args", []))
    fk = 0.5 if halb else 1.0
    if cfg.get("zuendung_shot") is not None:
        args += ["--zuendung", str(int(g["start"][cfg["zuendung_shot"]] * fk) + 1)]
    if cfg.get("schuesse_shot") is not None:
        s0 = int(g["start"][cfg["schuesse_shot"]] * fk) + 1
        args += ["--schuesse", ",".join(str(s0 + d) for d in ((0, 2, 5) if halb else (0, 1, 4, 5, 9, 10)))]
    if cfg["szene"] == "spinde":
        args += ["--font", str(ROOT / "assets/fonts/Montserrat-Black.ttf"),
                 "--figuren", str(folge / "test/figuren/png")]
    cmd = [BLENDER, "-b", "-P", str(ROOT / "pipeline/blender" / SZENEN[cfg["szene"]]), "--",
           "--engine", "eevee", "--samples", str(samples), "--res", res, "--pfad", str(pf),
           "--out", str(ziel / ("h_####" if halb else "f_####")), *args]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    if "FERTIG_ANIM" not in r.stdout:
        return "FEHLER " + (r.stdout[-1500:] + r.stderr[-1500:])
    if halb:
        r2 = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "15", "-start_number", "1",
                             "-i", str(ziel / "h_%04d.png"), "-vf",
                             "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                             "-start_number", "1", str(ziel / "f_%04d.png")], capture_output=True, text=True)
        if r2.returncode:
            return "FEHLER Interpolation " + r2.stderr[-800:]
    return f"ok {n} Frames in {time.time() - t:.0f}s"


if __name__ == "__main__":
    ep_path = pathlib.Path(sys.argv[1]).resolve(); folge = ep_path.parent
    ep = lade(ep_path)
    timing = json.loads((folge / "audio/timing.json").read_text())
    res = sys.argv[sys.argv.index("--res") + 1] if "--res" in sys.argv else "540x960"
    samples = int(sys.argv[sys.argv.index("--samples") + 1]) if "--samples" in sys.argv else 8
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    G = gruppen(ep, timing)
    (folge / "anim").mkdir(exist_ok=True)
    (folge / "anim/gruppen.json").write_text(json.dumps(G, indent=1))
    print("Animationen:", len(G), "Frames gesamt:", sum(g["frames"] for g in G.values()), flush=True)
    reihen = sorted(G, key=lambda k: (ep.ANIM[k]["szene"] != "spinde", ep.ANIM[k]["szene"] == "kabine"))
    for name in reihen:
        g = G[name]
        if nur and name not in nur:
            continue
        print(name, g["frames"], "->", job(ep, folge, name, g, res, samples), flush=True)
    print("ALLE_ANIM_FERTIG", flush=True)
