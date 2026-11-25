"""folge03_bope – Sprachfassung es (automatisch erzeugt von pipeline/sprache.py; Texte: ../folge03_bope/sprachen/es.py)"""
import importlib.util as _ilu, pathlib as _pl, copy as _copy

_B = _pl.Path(__file__).resolve().parent.parent / "folge03_bope"
def _lade(name, pfad):
    s = _ilu.spec_from_file_location(name, pfad); m = _ilu.module_from_spec(s); s.loader.exec_module(m); return m
_basis = _lade("basis_folge03_bope", _B / "episode.py")
_T = _lade("text_folge03_bope_es", _B / "sprachen" / "es.py")
globals().update({k: v for k, v in vars(_basis).items() if not k.startswith("_")})

SPRACHE = "es"
STIMME = "mfQB4jp20XcYgvNoJxXN"
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
for _k, _w in getattr(_T, "STIMME_AB", {}).items():
    SHOTS[_k]["stimme_ab"] = _w
BEFEHLE = _T.BEFEHLE
BEFEHLE_KOPF = _T.BEFEHLE_KOPF
KALTSTART = dict(_basis.KALTSTART, text=_T.HOOK)
ANIM = _copy.deepcopy(_basis.ANIM)
for _a in ANIM.values():
    if _a["szene"] == "spinde":
        _a["args"] = list(_a.get("args", [])) + ["--sprache", SPRACHE]
ANIM_SHOTS = {i: s["anim"] for i, s in enumerate(SHOTS) if s.get("anim")}
