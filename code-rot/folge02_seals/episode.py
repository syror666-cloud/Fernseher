"""CODE ROT – Folge 2: NAVY SEALS. Rettung von Kapitän Phillips, Indischer Ozean, April 2009 (echter Einsatz).
Format wie Folge 1: Text (*rot* _gelb_), Hintergrund, Figuren, Bewegung, Extras, 3D-Animation (anim=...).
"""

STIMME = "JH302OKVzGGJc47f08ex"  # Manuel
MODELL = "eleven_multilingual_v2"
ATMO = "atmo_meer"
STIMM_EINSTELLUNG = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.15}

MITTE = dict(x=150, y=560, w=780)
LINKS = dict(x=-80, y=600, w=780)
RECHTS = dict(x=380, y=600, w=780)
NAH = dict(x=40, y=380, w=1000)
TIEF = dict(x=150, y=1150, w=780)
GANZ = dict(x=290, y=330, w=500)
VOLL = dict(x=0, y=0, w=1080)
UNSCHARF = "blur(10px) brightness(.55)"
FOKUS_ZELLE = 0  # NAVY SEALS im Spind-Streifen


def fig(name, pos=MITTE, **kw):
    d = dict(src=name, **pos); d.update(kw); return d


def S(text, bg, figuren=(), move="zoom_in", **extra):
    return dict(text=text, bg=bg, figuren=list(figuren), move=move, **extra)


BEFEHLE = ["Nur wenn sein Leben bedroht ist", "!Alle Ziele gleichzeitig", "Ein Schuss pro Ziel", "!Kein zweiter Versuch"]
# Hook für den aggressiven Schnitt (cut.py --aggressiv): Höhepunkt vorweg
KALTSTART = dict(shot=49, dauer=1.5, text="3 Piraten.|*3* Schüsse.|Eine Sekunde.")

SHOTS = [
    # ---------- HOOK ----------
    S("Eine dieser *Einheiten*", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("holt dich heute Nacht.", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("Mal sehen,", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("ob du *zurückkommst*.", "intro", logo=True, sfx="alarm", ende_blitz=True, anim="intro"),
    S("", "intro_zelle:0", [fig("einheit_seals.svg", GANZ, filter="drop-shadow(0 0 30px rgba(255,40,40,.6))")],
      move="zoom_schnell", titel="NAVY *SEALS*", untertitel="US NAVY · SEIT 1962", ringe=True, logo=True,
      tint="rgba(255,60,60,.35)", pause=1.5, sfx="impact"),
    # ---------- SETUP ----------
    S("Indischer Ozean.", "meer", anim="anflug", sfx="whoosh", blitz=True),
    S("April _2009_.", "meer", anim="anflug", sprich="April zweitausendneun."),
    S("Vor der Küste _Somalias_.", "meer", anim="anflug"),
    S("Vier *Piraten* entern ein amerikanisches Frachtschiff.", "meer", anim="frachter", sfx="drone_hit"),
    S("Die _Maersk Alabama_.", "meer", anim="frachter", sprich="Die Märsk Alabama."),
    S("Der Kapitän bietet sich selbst als Geisel an.", "meer", [fig("kapitaen_entschlossen.svg", MITTE)],
      bgfilter=UNSCHARF, anim="loop_frachter"),
    S("Damit seine Crew frei kommt.", "meer", [fig("kapitaen_neutral.svg", NAH)], bgfilter=UNSCHARF, anim="loop_frachter"),
    S("Jetzt sitzt er in einem *Rettungsboot*.", "meer", anim="boot_nah"),
    S("Mit vier Piraten.", "meer", anim="boot_nah", sfx="impact"),
    S("Und du?", "meer", [fig("du_neutral.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_heck"),
    S("Du liegst auf dem Heck eines Zerstörers.", "meer", anim="schiff_seite"),
    S("Der _USS Bainbridge_.", "meer", anim="schiff_seite", sprich="Der U S S Bainbridge."),
    S("Dein Gewehr zeigt auf das Boot.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope", uhr="17:52"),
    S("Dein Befehl:", "meer", [fig("teamleader_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_heck", uhr="17:52"),
    S("Geschossen wird nur,", "meer", [fig("teamleader_entschlossen_zeigen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_heck", uhr="17:52"),
    S("wenn sein Leben in *Gefahr* ist.", "meer", [fig("du_angst.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_heck",
      uhr="17:52", sfx="heartbeat"),
    # ---------- LAGE ----------
    S("Das Boot ist geschlossen.", "meer", anim="boot_nah2", uhr="17:53"),
    S("Kleine Fenster. Eine Luke.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope2", uhr="17:53"),
    S("Die See schaukelt.", "meer", anim="boot_nah2", move_2d="shake", uhr="17:53"),
    S("Dein *Fadenkreuz* schaukelt mit.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope2", uhr="17:54"),
    S("Und du siehst nie alle *gleichzeitig*.", "meer", [fig("du_seitenblick.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_heck", uhr="17:54"),
    S("Zwei Tage vorher ist der Kapitän ins Wasser gesprungen.", "meer", anim="sprung", sfx="whoosh"),
    S("*Schüsse*.", "meer", anim="sprung", move_2d="shake_stark", blitz=True, sfx="schuesse"),
    S("Sie haben ihn zurückgeholt.", "meer", [fig("kapitaen_angst.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_frachter"),
    # ---------- BEFEHLE ----------
    S("Deine Befehle:", "meer", [fig("teamleader_entschlossen_zeigen.svg", LINKS)], bgfilter=UNSCHARF, anim="loop_heck",
      regeln=0),
    S("Nur wenn sein Leben bedroht ist.", "meer", [fig("du_entschlossen.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_heck", regeln=1),
    S("Alle Ziele *gleichzeitig*.", "meer", [fig("sniper2_entschlossen.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_heck", regeln=2),
    S("Ein Schuss pro Ziel.", "meer", [fig("sniper3_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_heck",
      regeln=3),
    S("Und: Es gibt *keinen* zweiten Versuch.", "meer", [fig("teamleader_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_heck", move_2d="zoom_schnell", regeln=4, sfx="impact"),
    # ---------- BELAGERUNG ----------
    S("Achtzehn Uhr vierzig.", "meer", anim="daemmerung", uhr="18:40", sfx="tick"),
    S("Die Sonne ist weg.", "meer", anim="daemmerung", uhr="18:40"),
    S("Stunden im Liegen.", "meer", [fig("du_neutral.svg", TIEF)], anim="heck_pov", uhr="18:52"),
    S("Dein Ellbogen ist taub.", "meer", [fig("du_angst.svg", TIEF)], anim="heck_pov", uhr="18:58"),
    S("Ein Kopf in der Luke.", "meer", [fig("zielfernrohr.svg", VOLL)],
      anim="scope3", uhr="19:04"),
    S("Ein zweiter am Fenster.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope3", uhr="19:07", sfx="tick"),
    S("Der *dritte* fehlt.", "meer", [fig("du_seitenblick.svg", NAH)], bgfilter=UNSCHARF, anim="loop_heck",
      uhr="19:09", sfx="heartbeat"),
    S("Im Funk: „Bereit?“", "meer", [fig("hand_funk.svg", VOLL)], bgfilter=UNSCHARF, anim="loop_heck", uhr="19:12",
      sfx="funk"),
    S("Durch das Fenster siehst du:", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope4", uhr="19:15"),
    S("Ein Gewehr.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope4", uhr="19:16", tint="rgba(200,0,0,.25)"),
    S("Es zeigt auf den Rücken des Kapitäns.", "meer", [fig("kapitaen_angst.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_frachter", uhr="19:17", sfx="drone_hit"),
    S("Neunzehn Uhr neunzehn.", "meer", anim="boot_nah3", uhr="19:19", sfx="tick"),
    S("Alle drei.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope5", uhr="19:19"),
    S("Im selben Moment. *Sichtbar*.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope5", uhr="19:19"),
    S("*Jetzt*.", "meer", [fig("du_schreien.svg", NAH)], bgfilter=UNSCHARF, anim="loop_heck", move_2d="shake_stark",
      uhr="19:19", blitz=True, sfx="impact"),
    # ---------- ZUGRIFF ----------
    S("Drei Schüsse.", "meer", anim="schuss", move_2d="shake_stark", blitz=True, uhr="19:19", sfx="schuesse"),
    S("Fast *gleichzeitig*.", "meer", anim="schuss", move_2d="shake", uhr="19:19"),
    S("Dann: nur noch Wellen.", "meer", anim="boot_nah3", move_2d="statisch", uhr="19:20", pause=0.6, stille=True),
    # ---------- FALSCHE ERLÖSUNG ----------
    S("Ein Schlauchboot legt ab.", "meer", anim="rhib", sfx="whoosh"),
    S("Sie öffnen die Luke.", "meer", anim="boot_nah4"),
    S("Der Kapitän lebt.", "meer", [fig("kapitaen_erleichtert.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_frachter"),
    S("_Unverletzt_.", "meer", [fig("kapitaen_erleichtert.svg", NAH)], bgfilter=UNSCHARF, anim="loop_frachter"),
    S("Nach vier Tagen.", "meer", anim="drohne_ende1"),
    S("Du hast es geschafft.", "meer", [fig("du_erleichtert.svg", MITTE)], bgfilter="blur(10px) brightness(.75)",
      anim="loop_heck"),
    # ---------- TWIST ----------
    S("Aber Moment.", "meer", [fig("du_seitenblick.svg", NAH)], bgfilter=UNSCHARF, anim="loop_heck", sfx="drone_hit"),
    S("Es waren *vier* Piraten.", "meer", anim="boot_nah2", tint="rgba(150,0,0,.3)"),
    S("Im Boot waren nur *drei*.", "meer", [fig("zielfernrohr.svg", VOLL)], anim="scope2", tint="rgba(150,0,0,.3)"),
    S("Der vierte?", "meer", [fig("du_angst.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_heck", sfx="heartbeat"),
    S("Der saß die ganze Zeit *hinter dir*.", "meer", anim="schiff_innen", tint="rgba(150,0,0,.25)", sfx="impact"),
    S("An Bord deines Schiffs.", "meer", anim="schiff_innen", tint="rgba(150,0,0,.25)"),
    S("Er war zum Verhandeln rübergekommen.", "meer", [fig("pirat_silhouette.svg", VOLL)], anim="schiff_innen",
      bgfilter="brightness(.6)"),
    S("Und wurde festgenommen.", "meer", [fig("pirat_silhouette.svg", VOLL)], anim="schiff_innen",
      bgfilter="brightness(.6)", move_2d="zoom_schnell"),
    S("Später: _33_ Jahre Haft.", "svg:gericht", move="zoom_in", sprich="Später: dreiunddreißig Jahre Haft."),
    # ---------- LOOP-ENDE ----------
    S("Ein Rettungsboot.", "meer", anim="drohne_ende2"),
    S("Vier Piraten.", "meer", anim="drohne_ende2"),
    S("Drei Schüsse.", "meer", anim="drohne_ende2", sfx="impact"),
    S("Und ein Kapitän, der _freiwillig_ mitgegangen ist.", "intro_zelle:0", [fig("einheit_seals.svg", GANZ)],
      move="zoom_in", tint="rgba(255,60,60,.25)", ringe=True, logo=True),
    # ---------- TEASER ----------
    S("Und morgen?", "intro", logo=True, sfx="whoosh", anim="outro"),
    S("Holt dich eine *andere*.", "intro", logo=True, sfx="alarm", ende_schwarz=True, anim="outro"),
]



# Figurenstimmen (pipeline/stimmen.py): Einstellung -> Rolle
FIGURENSTIMMEN = {0: 'spind', 1: 'spind', 2: 'spind', 3: 'spind', 71: 'spind', 72: 'spind', 41: 'funk'}
STIMME_AB = {41: 'Bereit'}
for _k, _r in FIGURENSTIMMEN.items():
    SHOTS[_k]["stimme"] = _r
for _k, _w in STIMME_AB.items():
    SHOTS[_k]["stimme_ab"] = _w

# =====================================================================================
# 3D-ANIMATION
# =====================================================================================
def _c(i):
    return -13 + 2 * i


Z, ZZ = 2.0, 2.05
ANIM = {
    "intro": dict(szene="spinde", keys=[
        (0.00, (_c(5) + 0.8, -2.4, Z), (_c(5) + 0.8, 0.5, ZZ), 21),
        (0.20, (_c(9), -2.4, Z), (_c(9), 0.5, ZZ), 21),
        (0.26, (_c(9) - 0.15, -2.3, Z), (_c(9) - 0.15, 0.5, ZZ), 21),
        (0.52, (_c(2), -2.4, Z), (_c(2), 0.5, ZZ), 21),
        (0.58, (_c(2) + 0.15, -2.3, Z), (_c(2) + 0.15, 0.5, ZZ), 21),
        (0.70, (_c(4), -2.4, Z), (_c(4), 0.5, ZZ), 21),
        (0.84, (_c(0), -2.3, Z), (_c(0), 0.5, ZZ), 21),
        (1.00, (_c(0), -1.5, 1.95), (_c(0), 0.5, 1.95), 21)]),
    "outro": dict(szene="spinde", keys=[
        (0.00, (_c(0), -1.8, Z), (_c(0), 0.5, ZZ), 21),
        (0.25, (_c(0) + 0.2, -2.4, Z), (_c(0) + 0.2, 0.5, ZZ), 21),
        (0.45, (_c(8), -2.4, Z), (_c(8), 0.5, ZZ), 21),
        (0.70, (_c(3), -2.4, Z), (_c(3), 0.5, ZZ), 21),
        (1.00, (_c(3), -1.4, 1.95), (_c(3), 0.5, 1.95), 21)]),
    # Meer: Zerstörer-Heck bei x=0, Bug bei +x. Rettungsboot bei (-32, 0). Frachter weit weg bei (-420, 260).
    "anflug": dict(szene="meer", keys=[(0, (-160, -140, 90), (-15, 0, 0), 28), (1, (-90, -95, 45), (-10, 0, 2), 30)]),
    "frachter": dict(szene="meer", args=["--zeit", "tag"], keys=[
        (0, (-330, 150, 30), (-420, 260, 12), 30), (1, (-345, 175, 22), (-420, 260, 12), 32)]),
    "loop_frachter": dict(szene="meer", args=["--zeit", "tag"], loop=4.0, shake=0.1, keys=[
        (0, (-380, 230, 18), (-420, 260, 16), 30), (1, (-379, 231, 18.3), (-420, 260, 16), 30)]),
    "boot_nah": dict(szene="meer", keys=[(0, (-44, -14, 1.2), (-32, 0, 1.2), 26), (1, (-40, -10, 1.0), (-32, 0, 1.3), 28)]),
    "boot_nah2": dict(szene="meer", keys=[(0, (-24, -9, 1.0), (-32, 0, 1.4), 30), (1, (-25, -7, 1.1), (-32, 0, 1.4), 32)]),
    "boot_nah3": dict(szene="meer", keys=[(0, (-46, 10, 0.8), (-32, 0, 1.3), 30), (1, (-44, 8, 0.9), (-32, 0, 1.3), 34)]),
    "boot_nah4": dict(szene="meer", args=["--rhib", "nah"], keys=[(0, (-38, -9, 1.6), (-32, 0, 1.6), 30),
                                                                (1, (-36, -7, 1.7), (-32, 0, 1.8), 32)]),
    "loop_heck": dict(szene="meer", loop=4.0, shake=0.12, keys=[
        (0, (9, -3.5, 8.2), (-32, 0, 1.0), 30), (1, (9.2, -3.1, 8.3), (-32, 0, 1.0), 30)]),
    "schiff_seite": dict(szene="meer", keys=[(0, (-30, -40, 9), (10, 0, 6), 26), (1, (-18, -36, 8), (10, 0, 6), 28)]),
    "scope": dict(szene="meer", shake=0.05, keys=[(0, (1.5, 0.5, 7.0), (-32, 0, 1.6), 230), (1, (1.5, 0.5, 7.0), (-32, 0, 1.6), 260)]),
    "scope2": dict(szene="meer", shake=0.06, keys=[(0, (1.5, 0.5, 7.0), (-31, 0, 1.7), 320), (1, (1.5, 0.5, 7.0), (-32.5, 0, 1.7), 320)]),
    "scope3": dict(szene="meer", shake=0.05, keys=[(0, (1.5, -0.5, 7.0), (-30, 0, 2.3), 300), (1, (1.5, -0.5, 7.0), (-31.5, 0, 2.0), 330)]),
    "scope4": dict(szene="meer", shake=0.04, keys=[(0, (1.5, 0.5, 7.0), (-33, 0, 1.6), 380), (1, (1.5, 0.5, 7.0), (-33, 0, 1.6), 420)]),
    "scope5": dict(szene="meer", shake=0.03, keys=[(0, (1.5, 0.5, 7.0), (-32, 0, 1.7), 200), (1, (1.5, 0.5, 7.0), (-32, 0, 1.7), 200)]),
    "sprung": dict(szene="meer", args=["--zeit", "tag", "--spritzer"], shake=0.15, keys=[
        (0, (-48, -12, 2.0), (-32, 0, 0.6), 28), (1, (-46, -10, 1.6), (-32, -2, 0.4), 30)]),
    "daemmerung": dict(szene="meer", args=["--zeit", "daemmerung"], keys=[
        (0, (-120, -60, 25), (-20, 0, 3), 28), (1, (-100, -50, 18), (-20, 0, 3), 28)]),
    "heck_pov": dict(szene="meer", shake=0.08, keys=[(0, (6, 1.5, 7.2), (-32, 0, 1.2), 34), (1, (5.6, 1.3, 7.2), (-32, 0, 1.2), 38)]),
    "schuss": dict(szene="meer", args=["--muendung", "1"], shake=0.25, keys=[
        (0, (5, -2.5, 7.4), (-32, 0, 1.4), 30), (1, (5.4, -2.3, 7.5), (-32, 0, 1.4), 32)]),
    "rhib": dict(szene="meer", args=["--rhib", "fahrt"], keys=[(0, (-10, -25, 6), (-25, 0, 0.5), 28), (1, (-18, -22, 4), (-30, 0, 0.8), 30)]),
    "schiff_innen": dict(szene="meer", keys=[(0, (40, -16, 9), (0, 0, 6), 24), (1, (36, -14, 8.5), (0, 0, 6), 26)]),
    "drohne_ende1": dict(szene="meer", args=["--rhib", "nah"], keys=[(0, (-60, -40, 25), (-25, 0, 0), 26), (1, (-90, -70, 45), (-15, 0, 0), 26)]),
    "drohne_ende2": dict(szene="meer", keys=[(0, (-70, -50, 30), (-20, 0, 0), 26), (1, (-200, -170, 130), (0, 0, 0), 26)]),
}
ANIM_SHOTS = {i: s["anim"] for i, s in enumerate(SHOTS) if s.get("anim")}
