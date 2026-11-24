"""Lädt echte, gemeinfreie (CC0) Geräusche von Freesound und legt sie als WAV in assets/sfx_real/ ab.
Der API-Schlüssel wird vom Netzwerk-Proxy eingesetzt. Fehlt er, bleibt alles bei den synthetischen Sounds.
Quellen werden in assets/sfx_real/QUELLEN.md protokolliert.
"""
import json, pathlib, subprocess, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/sfx_real"
API = "https://freesound.org/apiv2/search/text/"

SUCHE = {  # Name -> (Suchbegriff, min/max Dauer)
    "whoosh": ("swoosh whoosh fast", 0.3, 1.6),
    "impact": ("cinematic impact boom", 0.5, 4),
    "tick": ("clock ticking", 0.5, 3),
    "heartbeat": ("heartbeat", 1, 6),
    "static": ("radio static noise", 0.5, 4),
    "funk": ("walkie talkie radio squelch", 0.2, 3),
    "feuer": ("fire ignite", 0.8, 8),
    "tuer": ("door slam metal", 0.3, 3),
    "schuesse": ("distant gunshots", 0.5, 4),
    "alarm": ("alarm siren short", 0.5, 4),
    "drone_hit": ("cinematic braam", 1, 8),
    "feuerwerk": ("fireworks", 2, 15),
    "wellen": ("ocean waves", 3, 60),
    "atmo_nacht": ("night ambience crickets wind", 20, 300),
    "atmo_meer": ("ocean waves ambience night", 20, 300),
    "atmo_stadt": ("city night ambience dogs barking distant", 20, 400),
}


def suche(q, dmin, dmax):
    p = {"query": q, "filter": f'license:"Creative Commons 0" duration:[{dmin} TO {dmax}]',
         "fields": "id,name,username,duration,previews,avg_rating,num_downloads", "sort": "downloads_desc", "page_size": 8}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers={"Authorization": "Token proxy-injected"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["results"]


def main():
    try:
        suche("test", 0, 5)
    except Exception as e:
        print("Freesound nicht erreichbar/kein Schlüssel:", e); sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    quellen = ["# Geräusch-Quellen (Freesound, CC0)\n"]
    for name, (q, a, b) in SUCHE.items():
        ziel = OUT / f"{name}.wav"
        if ziel.exists():
            continue
        try:
            res = suche(q, a, b)
            if not res:
                print("nichts gefunden:", name); continue
            r = res[0]
            url = r["previews"]["preview-hq-mp3"]
            tmp = OUT / f"{name}.mp3"
            urllib.request.urlretrieve(url, tmp)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-ac", "2", "-ar", "44100",
                            "-af", "loudnorm=I=-16:TP=-1.5", str(ziel)], check=True)
            tmp.unlink()
            quellen.append(f"- {name}: \"{r['name']}\" von {r['username']} (freesound.org/s/{r['id']}), CC0")
            print("ok", name, r["name"])
        except Exception as e:
            print("Fehler", name, e)
    with open(OUT / "QUELLEN.md", "a") as f:
        f.write("\n".join(quellen[1:]) + "\n")


if __name__ == "__main__":
    main()
