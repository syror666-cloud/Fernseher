"""Setzt einen Einzelframe aus Ebenen zusammen (HTML -> PNG über Playwright).

Ebenen: Hintergrund (Blender-Render), Figuren (SVG), Untertitel mit Farbcode,
Einsatzuhr, Regel-Box, Titelkarte, Serienlogo.
Untertitel-Markup: *rot*  _gelb_
"""
import html, re, json, pathlib, subprocess, os

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_BLACK = ROOT / "assets/fonts/Montserrat-Black.ttf"
FONT_XB = ROOT / "assets/fonts/Montserrat-ExtraBold.ttf"
ROT, GELB = "#FF2A2A", "#FFD21E"

CSS = f"""
@font-face {{ font-family: MB; src: url('file://{FONT_BLACK}'); }}
@font-face {{ font-family: MXB; src: url('file://{FONT_XB}'); }}
html,body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#000; }}
.ebene {{ position:absolute; inset:0; }}
.bg {{ width:1080px; height:1920px; object-fit:cover; }}
.fig {{ position:absolute; }}
.cap {{ position:absolute; left:0; right:0; top:{int(1920*0.68)}px; text-align:center;
  font-family:MB; font-size:84px; letter-spacing:1px; color:#fff; text-transform:uppercase;
  -webkit-text-stroke:14px #000; paint-order:stroke fill;
  text-shadow: 0 6px 14px rgba(0,0,0,.65); line-height:1.05; padding:0 60px; }}
.cap .r {{ color:{ROT}; }} .cap .g {{ color:{GELB}; }}
.uhr {{ position:absolute; top:150px; right:60px; font-family:MB; font-size:64px; color:#fff;
  background:rgba(0,0,0,.72); border:3px solid {ROT}; border-radius:14px; padding:8px 26px 8px 62px;
  letter-spacing:3px; }}
.uhr:before {{ content:''; position:absolute; left:24px; top:50%; width:22px; height:22px; margin-top:-11px;
  border-radius:50%; background:{ROT}; box-shadow:0 0 18px {ROT}; }}
.regeln {{ position:absolute; top:110px; left:50%; transform:translateX(-50%); width:760px; font-family:MB;
  text-transform:uppercase; text-align:center; }}
.regeln .kopf {{ background:{ROT}; color:#fff; font-size:34px; padding:10px; border-radius:12px 12px 0 0; letter-spacing:3px; }}
.regeln .body {{ background:rgba(8,8,10,.9); border:3px solid {ROT}; border-top:none; border-radius:0 0 12px 12px; padding:16px 20px; }}
.regeln .zeile {{ color:#fff; font-size:34px; margin:8px 0; }}
.regeln .zeile.r {{ color:{ROT}; }}
.logo {{ position:absolute; top:120px; left:0; right:0; text-align:center; font-family:MB; font-size:96px;
  color:{ROT}; letter-spacing:6px; -webkit-text-stroke:6px #000; paint-order:stroke fill;
  text-shadow:0 0 30px rgba(255,30,30,.55); }}
.titel {{ position:absolute; left:0; right:0; top:1200px; text-align:center; font-family:MB; font-size:190px;
  color:#fff; -webkit-text-stroke:16px #000; paint-order:stroke fill; text-shadow:0 10px 30px rgba(0,0,0,.8);
  line-height:1; }}
.titel .r {{ color:{ROT}; }}
.untertitel {{ position:absolute; left:0; right:0; top:1420px; text-align:center; font-family:MXB; font-size:40px;
  color:#fff; letter-spacing:10px; text-shadow:0 3px 10px #000; }}
.ringe {{ position:absolute; left:50%; top:820px; transform:translate(-50%,-50%); }}
.vignette {{ background:radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,.75) 100%); }}
.tint {{ mix-blend-mode:multiply; }}
"""


def caption_html(text: str) -> str:
    t = html.escape(text)
    t = re.sub(r"\*(.+?)\*", r'<span class="r">\1</span>', t)
    t = re.sub(r"_(.+?)_", r'<span class="g">\1</span>', t)
    return t


def ringe_svg(n=4, farbe=ROT):
    kreise = "".join(f'<circle cx="500" cy="500" r="{150 + i*95}" fill="none" stroke="{farbe}" '
                     f'stroke-width="{10 - i*1.5}" opacity="{0.95 - i*0.18}"/>' for i in range(n))
    return f'<svg class="ringe" width="1000" height="1000" viewBox="0 0 1000 1000">{kreise}</svg>'


def frame_html(spec: dict) -> str:
    teile = []
    if spec.get("bg"):
        teile.append(f'<img class="ebene bg" src="file://{spec["bg"]}">')
    if spec.get("ringe"):
        teile.append(ringe_svg())
    for fig in spec.get("figuren", []):
        style = f'left:{fig["x"]}px; top:{fig["y"]}px; width:{fig["w"]}px;'
        if fig.get("flip"):
            style += "transform:scaleX(-1);"
        if fig.get("filter"):
            style += f'filter:{fig["filter"]};'
        teile.append(f'<img class="fig" style="{style}" src="file://{fig["src"]}">')
    if spec.get("tint"):
        teile.append(f'<div class="ebene tint" style="background:{spec["tint"]}"></div>')
    teile.append('<div class="ebene vignette"></div>')
    if spec.get("logo"):
        teile.append(f'<div class="logo">{html.escape(spec["logo"])}</div>')
    if spec.get("titel"):
        teile.append(f'<div class="titel">{caption_html(spec["titel"])}</div>')
        teile.append(f'<div class="untertitel">{html.escape(spec.get("untertitel", ""))}</div>')
    if spec.get("uhr") and not spec.get("regeln"):
        teile.append(f'<div class="uhr">{html.escape(spec["uhr"])}</div>')
    if spec.get("regeln"):
        zeilen = "".join(f'<div class="zeile {"r" if z.startswith("!") else ""}">{html.escape(z.lstrip("!"))}</div>'
                         for z in spec["regeln"]["zeilen"])
        teile.append(f'<div class="regeln"><div class="kopf">{html.escape(spec["regeln"]["kopf"])}</div>'
                     f'<div class="body">{zeilen}</div></div>')
    if spec.get("cap"):
        teile.append(f'<div class="cap">{caption_html(spec["cap"])}</div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(teile)}</body></html>'


def render(spec: dict, out_png: str):
    out = pathlib.Path(out_png)
    h = out.with_suffix(".html")
    h.write_text(frame_html(spec), encoding="utf-8")
    env = dict(os.environ)
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(ROOT / "pipeline/render_html.js"), str(h), str(out), "1080", "1920", "1"], check=True, env=env)
    h.unlink()
    return out


if __name__ == "__main__":
    import sys
    render(json.loads(pathlib.Path(sys.argv[1]).read_text()), sys.argv[2])
