"""Besetzung Folge 3 (BOPE): erzeugt die SVG-Figuren in ./svg"""
import sys, pathlib
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "pipeline"))
import figuren as F, inserts as I

DU = F.Figur("du", haut="mittel", haar="#2A1C12", frisur="kurz", jacke="#141516", jacke_schatten="#0D0E0F",
             weste="#222426", kopf="visier", kopf_farbe="#18191B")
TRUPPFUEHRER = F.Figur("truppfuehrer", haut="mittel", haar="#1A120D", frisur="kurz", bart="schnurrbart", jacke="#141516",
                       jacke_schatten="#0D0E0F", weste="#222426", kopf="barett", kopf_farbe="#0A0A0A")
KOLLEGE = F.Figur("kollege", haut="dunkel", haar="#120C09", jacke="#141516", jacke_schatten="#0D0E0F", weste="#222426",
                  kopf="visier", kopf_farbe="#18191B", bart="stoppeln")
JUNGE = F.Figur("junge", haut="dunkel", haar="#120C09", frisur="kurz", jacke="#D9541E", jacke_schatten="#B8461A",
                zivil=True, funk=False)

if __name__ == "__main__":
    out = HIER / "svg"; out.mkdir(exist_ok=True)
    for fig in (DU, TRUPPFUEHRER, KOLLEGE, JUNGE):
        for e in ("neutral", "angst", "entschlossen", "erleichtert", "schreien", "seitenblick"):
            (out / f"{fig.name}_{e}.svg").write_text(F.svg(fig, e))
    (out / "truppfuehrer_entschlossen_zeigen.svg").write_text(F.svg(TRUPPFUEHRER, "entschlossen", arm="zeigen"))
    for name, fig in F.EINHEITEN_FIGUREN.items():
        (out / f"einheit_{fig.name}.svg").write_text(F.svg_ganz(fig, "entschlossen"))
    for k, fn in I.ALLE.items():
        (out / f"{k}.svg").write_text(fn())
    print("ok", len(list(out.glob("*.svg"))))
