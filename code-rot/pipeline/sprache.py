"""Sprachfassung einer CODE-ROT-Folge anlegen.

python sprache.py <folge>/episode.py <en|es>
Legt <folge>_<sprache>/ an:
- episode.py: lädt die deutsche Folge und ersetzt Texte/Titel/Befehle/Hook/Hinweise aus <folge>/sprachen/<sprache>.py
- anim/: Verweise auf die deutschen 3D-Renders; nur die Spind-Animationen (Intro/Outro, Schilder) werden je Sprache neu gerendert
- bg/: Verweise; spinde_streifen.png -> code-rot/spinde/<sprache>_<variante>.png (eigener Render mit übersetzten Schildern)
- svg/: Verweise; TV-Einblendungen mit übersetztem Text neu erzeugt
Danach: vo.py (Stimme + Figurenstimmen), anim_render.py --nur intro,outro, cut.py --aggressiv.
"""
import sys, pathlib, os, importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

ERZAEHLER = {
    "en": dict(stimme="rg775DvkPkOmZPsaBnBg", name="Midnight – deep conversational documentary narrator"),
    "es": dict(stimme="mfQB4jp20XcYgvNoJxXN", name="Asv – deep documentary narrator (Latin American)"),
}

VORLAGE = '''"""{folge} – Sprachfassung {sprache} (automatisch erzeugt von pipeline/sprache.py; Texte: ../{folge}/sprachen/{sprache}.py)"""
import importlib.util as _ilu, pathlib as _pl, copy as _copy

_B = _pl.Path(__file__).resolve().parent.parent / "{folge}"
def _lade(name, pfad):
    s = _ilu.spec_from_file_location(name, pfad); m = _ilu.module_from_spec(s); s.loader.exec_module(m); return m
_basis = _lade("basis_{folge}", _B / "episode.py")
_T = _lade("text_{folge}_{sprache}", _B / "sprachen" / "{sprache}.py")
globals().update({{k: v for k, v in vars(_basis).items() if not k.startswith("_")}})

SPRACHE = "{sprache}"
STIMME = "{stimme}"
STIMM_EINSTELLUNG = dict(_basis.STIMM_EINSTELLUNG)
SHOTS = _copy.deepcopy(_basis.SHOTS)
assert len(_T.TEXTE) == len(SHOTS), "Übersetzung hat nicht gleich viele Einstellungen"
for _s, _t in zip(SHOTS, _T.TEXTE):
    _s.pop("sprich", None); _s.pop("stimme_ab", None)
    if isinstance(_t, tuple):
        _s["text"], _s["sprich"] = _t
    else:
        _s["text"] = _t
    if _s.get("untertitel"):
        _s["untertitel"] = _T.UNTERTITEL
    if _s.get("hinweis") and getattr(_T, "HINWEIS", None):
        _s["hinweis"] = _T.HINWEIS
for _k, _w in getattr(_T, "STIMME_AB", {{}}).items():
    SHOTS[_k]["stimme_ab"] = _w
BEFEHLE = _T.BEFEHLE
BEFEHLE_KOPF = _T.BEFEHLE_KOPF
KALTSTART = dict(_basis.KALTSTART, text=_T.HOOK, sprich=getattr(_T, "HOOK_SPRICH", None))
ANIM = _copy.deepcopy(_basis.ANIM)
for _a in ANIM.values():
    if _a["szene"] == "spinde":
        _a["args"] = list(_a.get("args", [])) + ["--sprache", SPRACHE]
ANIM_SHOTS = dict(_basis.ANIM_SHOTS)  # gleiche Einstellungen wie im Original (Folge 1 ordnet ohne "anim"-Feld zu)
'''


def link(ziel, quelle):
    if ziel.is_symlink() or ziel.exists():
        return
    ziel.symlink_to(os.path.relpath(quelle, ziel.parent))


def anlegen(ep_path, sprache):
    ep_path = pathlib.Path(ep_path).resolve(); basis = ep_path.parent; folge = basis.name
    neu = ROOT / f"{folge}_{sprache}"
    for d in ("audio", "anim", "bg", "svg", "export"):
        (neu / d).mkdir(parents=True, exist_ok=True)
    (neu / "episode.py").write_text(VORLAGE.format(folge=folge, sprache=sprache, stimme=ERZAEHLER[sprache]["stimme"]),
                                    encoding="utf-8")
    spec = importlib.util.spec_from_file_location("ep_" + sprache, neu / "episode.py")
    ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
    spinde = {n for n, a in ep.ANIM.items() if a["szene"] == "spinde"}
    for d in (basis / "anim").iterdir():
        if d.is_dir() and d.name not in spinde:
            link(neu / "anim" / d.name, d)
    for f in (basis / "bg").iterdir():
        if f.name != "spinde_streifen.png":
            link(neu / "bg" / f.name, f)
    variante = "bloque" if getattr(ep, "ERSATZ", "") else "standard"
    streifen = ROOT / "spinde" / f"{sprache}_{variante}.png"
    streifen.parent.mkdir(exist_ok=True)
    link(neu / "bg" / "spinde_streifen.png", streifen)
    for f in (basis / "svg").iterdir():
        link(neu / "svg" / f.name, f)
    link(neu / "test", basis / "test")
    import inserts
    t = ep._T
    for name, (oben, unten) in getattr(t, "SVG", {}).items():
        z = neu / "svg" / f"{name}.svg"
        if z.is_symlink():
            z.unlink()
        z.write_text(inserts.tv(oben, unten, name != "tv_eilmeldung"), encoding="utf-8")
    print(neu, "| Streifen:", streifen.name, "| Spind-Animationen:", sorted(spinde))
    return neu, streifen, getattr(ep, "ERSATZ", "")


if __name__ == "__main__":
    anlegen(sys.argv[1], sys.argv[2])
