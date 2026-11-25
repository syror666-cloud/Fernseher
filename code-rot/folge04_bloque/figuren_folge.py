"""Besetzung Folge 4 (Bloque de Búsqueda, Medellín 1993): erzeugt die SVG-Figuren in ./svg.
Alle Figuren sind erfunden; reale Personen erscheinen nur als Silhouette ohne Gesicht."""
import sys, pathlib
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "pipeline"))
import figuren as F, inserts as I

GRUEN, GRUEN_S, WESTE, KAPPE = "#3D5233", "#30422A", "#2A3524", "#2F4128"
DU = F.Figur("du", haut="mittel", haar="#2A1C12", frisur="kurz", jacke=GRUEN, jacke_schatten=GRUEN_S, weste=WESTE,
             kopf="kappe", kopf_farbe=KAPPE)
OBERST = F.Figur("oberst", haut="mittel", haar="#5A5048", frisur="kurz", bart="schnurrbart", jacke=GRUEN,
                 jacke_schatten=GRUEN_S, weste=WESTE, kopf="kappe", kopf_farbe=KAPPE)
SOHN = F.Figur("sohn", haut="mittel", haar="#1A120D", frisur="seitenscheitel", jacke="#5B6470", jacke_schatten="#4A525C",
               zivil=True)
KOLLEGE = F.Figur("kollege", haut="dunkel", haar="#120C09", jacke=GRUEN, jacke_schatten=GRUEN_S, weste=WESTE,
                  kopf="kappe", kopf_farbe=KAPPE, bart="stoppeln")
BLOQUE = F.Figur("bloque", haut="mittel", haar="#1E1410", jacke=GRUEN, jacke_schatten=GRUEN_S, weste=WESTE,
                 kopf="kappe", kopf_farbe=KAPPE, bart="stoppeln")

if __name__ == "__main__":
    out = HIER / "svg"; out.mkdir(exist_ok=True)
    for fig in (DU, OBERST, SOHN, KOLLEGE):
        for e in ("neutral", "angst", "entschlossen", "erleichtert", "schreien", "seitenblick"):
            (out / f"{fig.name}_{e}.svg").write_text(F.svg(fig, e))
    (out / "oberst_entschlossen_zeigen.svg").write_text(F.svg(OBERST, "entschlossen", arm="zeigen"))
    (out / "sohn_entschlossen_funk.svg").write_text(F.svg(SOHN, "entschlossen", arm="funk"))
    (out / "sohn_angst_funk.svg").write_text(F.svg(SOHN, "angst", arm="funk"))
    for name, fig in F.EINHEITEN_FIGUREN.items():
        (out / f"einheit_{fig.name}.svg").write_text(F.svg_ganz(fig, "entschlossen"))
    (out / "einheit_bloque.svg").write_text(F.svg_ganz(BLOQUE, "entschlossen"))
    # Neuer Look: Ganzkörper (kurze Beine) und Rückansicht für Aktionen im Bild
    (out / "du_ruecken.svg").write_text(F.svg_ruecken(DU))
    (out / "kollege_ruecken.svg").write_text(F.svg_ruecken(KOLLEGE))
    (out / "du_entschlossen_waffe_ganz.svg").write_text(F.svg_ganz(DU, "entschlossen", arm="waffe", kurz=True))
    (out / "du_neutral_fernglas_ganz.svg").write_text(F.svg_ganz(DU, "neutral", arm="fernglas", kurz=True))
    (out / "du_erleichtert_ganz.svg").write_text(F.svg_ganz(DU, "erleichtert", kurz=True))
    (out / "kollege_erleichtert_ganz.svg").write_text(F.svg_ganz(KOLLEGE, "erleichtert", kurz=True))
    (out / "oberst_entschlossen_zeigen_ganz.svg").write_text(F.svg_ganz(OBERST, "entschlossen", arm="zeigen", kurz=True))
    for k, fn in I.ALLE.items():
        (out / f"{k}.svg").write_text(fn())
    (out / "tv_eilmeldung.svg").write_text(I.tv("EILMELDUNG", "MEDELLÍN · 2.12.1993", False))
    print("ok", len(list(out.glob("*.svg"))))
