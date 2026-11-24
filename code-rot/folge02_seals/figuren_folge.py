"""Besetzung Folge 2 (SEALs): erzeugt die SVG-Figuren in ./svg"""
import sys, pathlib
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "pipeline"))
import figuren as F, inserts as I

DU = F.Figur("du", haut="hell", haar="#8A6A3A", frisur="kurz", bart="stoppeln", jacke="#2F3A2E", jacke_schatten="#252E24",
             weste="#3A3A30", kopf="kappe", kopf_farbe="#2B2B25")
TEAMLEADER = F.Figur("teamleader", haut="mittel", haar="#2A1E16", frisur="kurz", bart="stoppeln", jacke="#2A3328",
                     jacke_schatten="#20281F", weste="#34342B", kopf="kappe", kopf_farbe="#3A3A30")
SNIPER2 = F.Figur("sniper2", haut="dunkel", haar="#140E0B", jacke="#2F3A2E", jacke_schatten="#252E24", weste="#3A3A30",
                  kopf="nachtsicht", kopf_farbe="#2E3229")
SNIPER3 = F.Figur("sniper3", haut="hell", haar="#3A2A1C", jacke="#2F3A2E", jacke_schatten="#252E24", weste="#3A3A30",
                  kopf="kappe", kopf_farbe="#20231E", bart="stoppeln")
KAPITAEN = F.Figur("kapitaen", haut="hell", haar="#B9B6AE", frisur="seitenscheitel", bart="stoppeln", jacke="#C8C2B4",
                   jacke_schatten="#ABA597", zivil=True, funk=False)

if __name__ == "__main__":
    out = HIER / "svg"; out.mkdir(exist_ok=True)
    for fig in (DU, TEAMLEADER, SNIPER2, SNIPER3, KAPITAEN):
        for e in ("neutral", "angst", "entschlossen", "erleichtert", "schreien", "seitenblick"):
            (out / f"{fig.name}_{e}.svg").write_text(F.svg(fig, e))
    (out / "teamleader_entschlossen_zeigen.svg").write_text(F.svg(TEAMLEADER, "entschlossen", arm="zeigen"))
    for name, fig in F.EINHEITEN_FIGUREN.items():
        (out / f"einheit_{fig.name}.svg").write_text(F.svg_ganz(fig, "entschlossen"))
    for k, fn in I.ALLE.items():
        (out / f"{k}.svg").write_text(fn())
    print("ok", len(list(out.glob("*.svg"))))
