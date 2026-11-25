"""Besetzung Folge 5 (Mossad, Buenos Aires 1960): erzeugt die SVG-Figuren in ./svg.
Alle Figuren sind erfunden; reale Personen erscheinen nur als Silhouette ohne Gesicht."""
import sys, pathlib
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "pipeline"))
import figuren as F, inserts as I

DU = F.Figur("du", haut="hell", haar="#3A2A1C", frisur="seitenscheitel", jacke="#3B3A36", jacke_schatten="#2E2D2A",
             zivil=True, funk=False)
TEAMLEITER = F.Figur("teamleiter", haut="mittel", haar="#1E1712", frisur="kurz", bart="schnurrbart", jacke="#2B2F36",
                     jacke_schatten="#21252B", zivil=True, funk=False)
KOLLEGE = F.Figur("kollege", haut="hell", haar="#5A4632", frisur="kurz", jacke="#4A3F33", jacke_schatten="#3A3128",
                  zivil=True, funk=False, bart="stoppeln")
MOSSAD = F.Figur("mossad", haut="mittel", haar="#1E1410", frisur="seitenscheitel", jacke="#23262B", jacke_schatten="#1A1C20",
                 zivil=True, funk=False, hose="#1E2024")
MANN = F.Figur("mann", haut="hell", haar="#2A2520", frisur="seitenscheitel", jacke="#4A4238", jacke_schatten="#3A342C",
               zivil=True, funk=False, hose="#2E2A26")

if __name__ == "__main__":
    out = HIER / "svg"; out.mkdir(exist_ok=True)
    for fig in (DU, TEAMLEITER, KOLLEGE):
        for e in ("neutral", "angst", "entschlossen", "erleichtert", "schreien", "seitenblick"):
            (out / f"{fig.name}_{e}.svg").write_text(F.svg(fig, e))
    (out / "teamleiter_entschlossen_zeigen.svg").write_text(F.svg(TEAMLEITER, "entschlossen", arm="zeigen"))
    (out / "mann_ganz.svg").write_text(F.svg_ganz(MANN, "neutral"))  # nur als schwarze Silhouette verwendet
    for name, fig in F.EINHEITEN_FIGUREN.items():
        (out / f"einheit_{fig.name}.svg").write_text(F.svg_ganz(fig, "entschlossen"))
    (out / "einheit_mossad.svg").write_text(F.svg_ganz(MOSSAD, "entschlossen"))
    for k, fn in I.ALLE.items():
        (out / f"{k}.svg").write_text(fn())
    (out / "tv_prozess.svg").write_text(I.tv("JERUSALEM · 1961", "DER PROZESS", False))
    print("ok", len(list(out.glob("*.svg"))))
