"""CODE ROT Animator: baut pro Einstellung eine animierte HTML-Szene und rendert sie Frame für Frame."""
import html as _html, json, pathlib, re, subprocess, os

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parent.parent
FONT_BLACK = ROOT / "assets/fonts/Montserrat-Black.ttf"
FONT_XB = ROOT / "assets/fonts/Montserrat-ExtraBold.ttf"
ROT, GELB = "#FF2A2A", "#FFD21E"
FPS = 30

CSS = f"""
@font-face {{ font-family: MB; src: url('file://{FONT_BLACK}'); }}
@font-face {{ font-family: MXB; src: url('file://{FONT_XB}'); }}
html,body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#000; }}
.ebene, .tiefe {{ position:absolute; inset:0; transform-origin:540px 960px; }}
#bgimg, .bgsvg {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
.figwrap {{ position:absolute; transform-origin:50% 100%; }}
.figwrap svg {{ width:100%; height:auto; display:block; overflow:visible; }}
#fx {{ position:absolute; left:0; top:0; }}
.vignette {{ background:radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,.72) 100%); }}
#blitz, #schwarz {{ position:absolute; inset:0; opacity:0; }}
#schwarz {{ background:#000; }}
#uhr {{ position:absolute; top:150px; right:60px; font-family:MB; font-size:64px; color:#fff; transform-origin:100% 0;
  background:rgba(0,0,0,.72); border:3px solid {ROT}; border-radius:14px; padding:8px 26px 8px 62px; letter-spacing:3px; }}
#uhr .dot {{ position:absolute; left:24px; top:50%; width:22px; height:22px; margin-top:-11px; border-radius:50%;
  background:{ROT}; box-shadow:0 0 18px {ROT}; }}
.regeln {{ position:absolute; top:110px; left:50%; transform:translateX(-50%); width:760px; font-family:MB;
  text-transform:uppercase; text-align:center; transform-origin:50% 0; }}
.regeln .kopf {{ background:{ROT}; color:#fff; font-size:34px; padding:10px; border-radius:12px 12px 0 0; letter-spacing:3px; }}
.regeln .body {{ background:rgba(8,8,10,.9); border:3px solid {ROT}; border-top:none; border-radius:0 0 12px 12px; padding:16px 20px; min-height:10px; }}
.regeln .zeile {{ color:#fff; font-size:34px; margin:8px 0; }}
.regeln .zeile.r {{ color:{ROT}; }}
.logo {{ position:absolute; top:34px; left:0; right:0; text-align:center; font-family:MB; font-size:78px;
  color:{ROT}; letter-spacing:6px; -webkit-text-stroke:6px #000; paint-order:stroke fill; }}
.titel {{ position:absolute; left:0; right:0; top:1200px; text-align:center; font-family:MB; font-size:190px;
  color:#fff; -webkit-text-stroke:16px #000; paint-order:stroke fill; text-shadow:0 10px 30px rgba(0,0,0,.8); line-height:1; }}
.titel .r {{ color:{ROT}; }}
.untertitel {{ position:absolute; left:0; right:0; top:1420px; text-align:center; font-family:MXB; font-size:40px;
  color:#fff; letter-spacing:10px; text-shadow:0 3px 10px #000; }}
.umriss svg {{ filter:url(#umrissf); }}
.umriss .rig-arm-l>path:first-child, .umriss .rig-arm-r>path:first-child, .umriss .rig-kopf>circle:first-of-type,
.umriss .rig-bein-l>path:first-child, .umriss .rig-bein-r>path:first-child, .umriss .rig-koerper>path:first-child {{
  stroke:#1c130e; stroke-width:9; stroke-linejoin:round; }}
.schatten {{ position:absolute; left:8%; right:8%; bottom:-1.5%; height:5%;
  background:radial-gradient(ellipse at center, rgba(25,10,5,.6) 0%, rgba(25,10,5,.3) 45%, rgba(0,0,0,0) 72%); }}
.ringe {{ position:absolute; left:540px; top:820px; transform:translate(-50%,-50%); }}
"""

FX_STANDARD = {
    "rollfeld": [dict(typ="staub", n=45, alpha=0.6, seed=1)],
    "feuer": [dict(typ="flimmern", x=900, y=1300, r=900, alpha=0.22, seed=2), dict(typ="rauch", x=850, y=1500, breite=500, hoehe=1400, n=10, seed=3),
              dict(typ="glut", x=850, y=1450, breite=450, hoehe=1100, n=70, seed=4)],
    "kabine": [dict(typ="staub", n=70, alpha=0.9, seed=5)],
    "kabine_zugriff": [dict(typ="staub", n=90, alpha=1.0, seed=6), dict(typ="rauch", x=540, y=1300, breite=900, hoehe=900, n=8, farbe="90,90,100", alpha=0.6, seed=7)],
    "intro": [dict(typ="staub", n=60, alpha=0.7, seed=8), dict(typ="flimmern", x=540, y=300, r=1200, alpha=0.18, farbe="255,30,30", seed=9)],
    "tv": [dict(typ="scanlines", seed=10)],
    "meer": [dict(typ="staub", n=30, alpha=0.4, seed=13)],
    "favela": [dict(typ="staub", n=50, alpha=0.6, seed=14)],
    "feuerwerk": [dict(typ="feuerwerk", n=7, seed=15), dict(typ="staub", n=40, alpha=0.5, seed=16)],
    "titel": [dict(typ="glut", x=540, y=1900, breite=1000, hoehe=1700, n=60, seed=11), dict(typ="flimmern", x=540, y=800, r=1000, alpha=0.25, farbe="255,40,40", seed=12)],
}


def _cap(text):
    t = _html.escape(text)
    t = re.sub(r"\*(.+?)\*", r'<span class="r">\1</span>', t)
    return re.sub(r"_(.+?)_", r'<span class="g">\1</span>', t)


def _svg_inline(pfad):
    s = pathlib.Path(pfad).read_text()
    return re.sub(r'<svg([^>]*?) width="\d+" height="\d+"', r"<svg\1", s, count=1)


def _ausdruck_aktion(name):
    n = pathlib.Path(name).stem
    for e in ("angst", "schock", "entschlossen", "erleichtert", "schreien", "seitenblick", "neutral"):
        if f"_{e}" in n:
            return e, ""
    return "neutral", {"hand_funk": "funk", "hand_leiter": "klettern", "trage": "trage", "fenster1": "silhouetten",
                       "fenster2": "silhouetten", "tv_1972": "tv", "tv_rauschen": "tv", "zielfernrohr": "scope", "pirat_silhouette": "silhouetten"}.get(n, "pop" if n.startswith("einheit_") else "")


def baue(shot, k, dauer, folge, bg, hud, fx, vorher=None):
    """shot: Eintrag aus episode.SHOTS; bg: {"typ":"seq","muster","start","n","loop"} | {"typ":"bild","src"} | {"typ":"svg","src"}"""
    teile, figdaten = [], []
    # --- Hintergrund-Ebene
    bgf = f'filter:{shot["bgfilter"]};' if shot.get("bgfilter") else ""
    if bg["typ"] == "seq":
        teile.append(f'<div class="tiefe" data-tiefe="1"><img id="bgimg" style="{bgf}"></div>')
    elif bg["typ"] == "bild":
        teile.append(f'<div class="tiefe" data-tiefe="1"><img id="bgimg" src="file://{bg["src"]}" style="{bgf}"></div>')
    else:  # SVG-Hintergrund als animierbare Figur (Silhouetten, TV-Rauschen ...)
        e, a = _ausdruck_aktion(bg["src"])
        teile.append(f'<div class="tiefe" data-tiefe="1"><img id="bgimg" style="display:none">'
                     f'<div class="figwrap" style="left:0;top:0;width:1080px;{bgf}">{_svg_inline(bg["src"])}</div></div>')
        figdaten.append(dict(ausdruck=e, aktion=shot.get("bg_aktion", a), seed=k * 7 + 1))
    if bg.get("himmel"):
        teile.append('<div class="ebene" style="mix-blend-mode:screen;background:linear-gradient(to bottom, '
                     'rgba(38,62,130,.75) 0%, rgba(30,50,110,.45) 35%, rgba(20,35,80,.12) 60%, rgba(0,0,0,0) 75%)"></div>')
        teile.append('<div class="ebene" style="mix-blend-mode:soft-light;background:rgba(40,70,160,.35)"></div>')
    # --- Figuren
    for i, f in enumerate(shot.get("figuren", [])):
        e, a = _ausdruck_aktion(f["src"])
        style = f'left:{f["x"]}px;top:{f["y"]}px;width:{f["w"]}px;'
        klasse = "figwrap umriss" if shot.get("umriss") else "figwrap"
        schatten = '<div class="schatten"></div>' if f.get("boden") else ""
        if f.get("filter"):
            style += f'filter:{f["filter"]};'
        flip = ' style="transform:scaleX(-1)"' if f.get("flip") else ""
        teile.append(f'<div class="tiefe" data-tiefe="{f.get("tiefe", 1.15)}"><div class="{klasse}" style="{style}">{schatten}<div{flip}>'
                     f'{_svg_inline(folge / "svg" / f["src"])}</div></div></div>')
        figdaten.append(dict(ausdruck=e, aktion=f.get("aktion", a), seed=k * 13 + i * 5 + 3,
                             richtung=f.get("richtung", 1), tempo=f.get("tempo", 260), ab=f.get("ab", 0.5),
                             spricht=bool(f.get("spricht")), ganz=bool(f.get("boden")), von=f.get("von", 0)))
    teile.append('<div class="tiefe" data-tiefe="1.3"><canvas id="fx" width="1080" height="1920"></canvas></div>')
    if shot.get("tint"):
        teile.append(f'<div class="ebene" id="tint" style="background:{shot["tint"]};mix-blend-mode:multiply"></div>')
    teile.append('<div class="ebene vignette"></div>')
    # --- HUD (nicht von der Kamera bewegt)
    if hud.get("ringe"):
        teile.append('<svg class="ringe" width="1100" height="1100" viewBox="0 0 1100 1100">' +
                     "".join(f'<circle cx="550" cy="550" r="200" fill="none" stroke="{ROT}" stroke-width="9"/>' for _ in range(4)) + "</svg>")
    if hud.get("linie"):
        teile.append('<div id="linie" style="position:absolute;left:534px;top:250px;width:12px;height:1250px;background:#F4C21A;'
                     'box-shadow:0 0 24px #F4C21A;border-radius:6px"></div>'
                     '<div style="position:absolute;left:510px;top:240px;width:60px;height:14px;background:#F4C21A;border-radius:7px"></div>'
                     '<div style="position:absolute;left:510px;top:1494px;width:60px;height:14px;background:#F4C21A;border-radius:7px"></div>')
    if hud.get("logo"):
        # dunkles Band hinter dem Logo, damit Namensschilder der Spinde beim Zoom nicht mit dem Logo kollidieren
        teile.append('<div style="position:absolute;top:0;left:0;right:0;height:290px;'
                     'background:linear-gradient(#000 0%,#000 62%,rgba(0,0,0,0) 100%)"></div>'
                     '<div class="logo">CODE ROT</div>')
    if hud.get("titel"):
        # Schriftgröße nach dem längsten Wort (Montserrat Black, Großbuchstaben ~0,8 em breit); data-fit schaltet
        # die Messung im Laufzeitskript ab
        laengstes = max(len(w) for w in re.sub(r"[*_]", "", hud["titel"]).split())
        fs = int(min(190, 1000 / (0.8 * laengstes)))
        teile.append(f'<div class="titel" data-fit="1" style="font-size:{fs}px">{_cap(hud["titel"])}</div>'
                     f'<div class="untertitel">{_html.escape(hud.get("untertitel", ""))}</div>')
    if hud.get("uhr") and not hud.get("regeln"):
        teile.append(f'<div id="uhr"><span class="dot"></span>{_html.escape(hud["uhr"])}</div>')
    if hud.get("regeln"):
        z = hud["regeln"]["zeilen"]; neu = hud["regeln"].get("neu", False)
        zeilen = "".join(f'<div class="zeile {"r" if x.startswith("!") else ""} {"neu" if neu and i == len(z) - 1 else ""}">'
                         f'{_html.escape(x.lstrip("!"))}</div>' for i, x in enumerate(z))
        teile.append(f'<div class="regeln"><div class="kopf">{_html.escape(hud["regeln"].get("kopf", "Deine Befehle"))}</div><div class="body">{zeilen}</div></div>')
    if shot.get("hinweis") and not hud.get("titel"):
        teile.append(f'<div style="position:absolute;left:40px;bottom:60px;font-family:MXB;font-size:26px;letter-spacing:4px;'
                     f'color:rgba(255,255,255,.55);text-shadow:0 2px 6px #000">{_html.escape(shot["hinweis"])}</div>')
    if shot.get("umriss"):  # Umriss-Filter (dunkle Kontur wie im Comic-Look) + warme Lichtstimmung
        teile.append('<svg width="0" height="0" style="position:absolute"><filter id="umrissf" x="-5%" y="-5%" width="110%" height="110%">'
                     '<feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/><feFlood flood-color="#1c130e"/>'
                     '<feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/>'
                     '</feMerge></filter></svg>')
    teile.append('<div id="blitz"></div><div id="schwarz"></div>')
    shotjs = dict(dauer=dauer, fps=FPS, move=shot.get("move_2d", "drift" if bg["typ"] == "seq" else shot["move"]),
                  bg=bg if bg["typ"] == "seq" else None, figuren=figdaten, fx=fx, hud=hud,
                  blitz=shot.get("blitz", False), ende_blitz=shot.get("ende_blitz", False),
                  ende_schwarz=shot.get("ende_schwarz", False), stille=shot.get("stille", False),
                  tint_puls=bool(shot.get("tint_puls")), punches=shot.get("punches", []),
                  stoesse=shot.get("stoesse", []), blitz_kurz=shot.get("blitz_kurz", False))
    runtime = (HIER / "runtime.js").read_text()
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(teile)}'
            f'<script>window.SHOT={json.dumps(shotjs)};</script><script>{runtime}</script></body></html>')


def render(html_text, out_mp4, frames):
    out = pathlib.Path(out_mp4)
    h = out.with_suffix(".html"); h.write_text(html_text, encoding="utf-8")
    env = dict(os.environ)
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    r = subprocess.run(["node", str(HIER / "render_clip.js"), str(h), str(out), str(frames), str(FPS)],
                       capture_output=True, text=True, env=env)
    if r.returncode or "SEITENFEHLER" in r.stderr:
        raise RuntimeError(f"Animator-Fehler {out.name}: {r.stderr[-1500:]}")
    return out
