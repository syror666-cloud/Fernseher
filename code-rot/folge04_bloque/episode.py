"""CODE ROT – Folge 4: BLOQUE DE BÚSQUEDA (Kolumbien). Die Jagd auf Pablo Escobar, Medellín, 2. Dezember 1993.
Belegte Fakten (siehe SKRIPT.md): Flucht aus dem selbst gebauten Gefängnis „La Catedral“ im Juli 1992; Suchblock der
Nationalpolizei unter Oberst Hugo Martínez; dessen Sohn leitete die Funkpeilung; Escobar wurde am 2.12.1993 (einen Tag
nach seinem 44. Geburtstag) über ein Telefonat mit seinem Sohn in einem zweistöckigen Haus in Los Olivos geortet, floh
über die Dächer und wurde erschossen. Wer den tödlichen Schuss abgab, ist bis heute umstritten.
Dramatisiert: Uhrzeiten/Gesprächsdauer im Bild, Dialoge, die Ich-Perspektive. Alle Figuren sind erfunden;
Escobar erscheint nur als Silhouette.
"""

STIMME = "JH302OKVzGGJc47f08ex"  # Manuel
MODELL = "eleven_multilingual_v2"
ATMO = "atmo_stadt"
STIMM_EINSTELLUNG = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.15}

MITTE = dict(x=150, y=560, w=780)
LINKS = dict(x=-80, y=600, w=780)
NAH = dict(x=40, y=380, w=1000)
GANZ = dict(x=290, y=330, w=500)
UNSCHARF = "blur(4px) brightness(.9) saturate(1.1)"  # neuer Look: nur leichte Tiefenunschärfe
VORNE = dict(x=300, y=640, w=480, boden=True)   # Ganzkörper im Bild (Füße ~1780 px)
RUECK = dict(x=330, y=770, w=420, boden=True)   # Rückansicht, läuft ins Bild
HINWEIS = "NACH WAHREN EREIGNISSEN · DRAMATISIERT"
ERSATZ = "SEK=BLOQUE DE BÚSQUEDA|KOLUMBIEN|bloque"  # Kolumbien-Zelle im Spind-Intro (ersetzt SEK in dieser Folge)
ZELLE = 9


def fig(name, pos=MITTE, **kw):
    d = dict(src=name, **pos); d.update(kw); return d


def S(text, bg, figuren=(), move="zoom_in", **extra):
    return dict(text=text, bg=bg, figuren=list(figuren), move=move, **extra)


BEFEHLE = ["Bleib unsichtbar", "!Warte auf das Signal", "Keine Zivilisten", "!Er darf nicht entkommen"]
# Hook für den aggressiven Schnitt (cut.py --aggressiv): Höhepunkt vorweg
KALTSTART = dict(shot=43, dauer=1.5, text="Ein Anruf.|Zu *lang*.", sprich="Er ist der gefährlichste Mann der Welt. Und ein *Anruf* verrät ihn.")

SHOTS = [
    # ---------- HOOK ----------
    S("Eine dieser *Einheiten*", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("holt dich heute.", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("Mal sehen,", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("ob du *zurückkommst*.", "intro", logo=True, sfx="alarm", ende_blitz=True, anim="intro"),
    S("", f"intro_zelle:{ZELLE}", [fig("einheit_bloque.svg", GANZ, filter="drop-shadow(0 0 30px rgba(255,40,40,.6))")],
      move="zoom_schnell", titel="BLOQUE DE *BÚSQUEDA*", untertitel="POLICÍA NACIONAL · KOLUMBIEN", ringe=True,
      logo=True, tint="rgba(255,60,60,.35)", pause=1.5, sfx="impact"),
    # ---------- SETUP ----------
    S("_Medellín_, Kolumbien.", "favela", anim="anflug", sfx="whoosh", blitz=True),
    S("Dezember 1993.", "favela", anim="anflug", sprich="Dezember neunzehnhundertdreiundneunzig."),
    S("Du gehörst zum *Suchblock*.", "favela", [fig("du_entschlossen_waffe_ganz.svg", VORNE, aktion="zielen")], anim="huegel"),
    S("Euer Ziel: ein einziger Mann.", "favela", anim="huegel"),
    S("Der gefährlichste Drogenboss der Welt.", "svg:fenster1", move="zoom_in", sfx="drone_hit"),
    S("_Pablo Escobar_.", "svg:fenster1", move="zoom_schnell", bgfilter="brightness(.8)", sfx="impact"),
    S("Vor anderthalb Jahren ist er geflohen.", "favela", anim="gasse"),
    S("Aus einem Gefängnis, das er *selbst* gebaut hat.", "favela", [fig("kollege_seitenblick.svg", MITTE)],
      bgfilter=UNSCHARF, anim="loop_wagen"),
    S("Seitdem wechselt er ständig das Versteck.", "favela", anim="huegel2"),
    S("Aber er hat eine *Schwäche*.", "favela", [fig("du_seitenblick.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen",
      sfx="heartbeat"),
    S("Seine Familie.", "favela", anim="gasse_tief"),
    S("Er ruft sie an. Immer wieder.", "svg:hand_funk", move="zoom_in", sfx="funk"),
    # ---------- LAGE ----------
    S("Dein Oberst hat einen Plan.", "favela", [fig("oberst_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_wagen"),
    S("Sein eigener *Sohn*", "favela", [fig("sohn_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_wagen"),
    S("sitzt in einem Wagen voller Antennen.", "favela", anim="peil_nah"),
    S("Jeder Anruf verrät eine *Richtung*.", "favela", anim="peil_nah", sfx="static"),
    S("Ein paar Minuten reichen.", "favela", [fig("sohn_seitenblick.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen", sfx="tick"),
    # ---------- BEFEHLE ----------
    S("Deine Befehle:", "favela", [fig("oberst_entschlossen_zeigen.svg", LINKS)], bgfilter=UNSCHARF, anim="loop_wagen",
      regeln=0),
    S("Bleib unsichtbar.", "favela", [fig("du_ruecken.svg", RUECK, aktion="laufen_weg")], anim="gasse", regeln=1),
    S("Warte auf das *Signal*.", "favela", [fig("du_neutral_fernglas_ganz.svg", dict(x=-30, y=700, w=450, boden=True), aktion="umsehen")],
      anim="peil_nah", regeln=2),
    S("Keine Zivilisten.", "favela", [fig("du_ruecken.svg", RUECK, aktion="laufen_weg")], anim="gasse", regeln=3),
    S("Und: Er darf *nicht* entkommen.", "favela", [fig("oberst_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_wagen", move_2d="zoom_schnell", regeln=4, sfx="impact"),
    # ---------- ANNÄHERUNG ----------
    S("Zweiter Dezember.", "favela", anim="anflug2", sprich="Zweiter Dezember."),
    S("Einen Tag nach seinem *Geburtstag*.", "favela", anim="anflug2"),
    S("Dann: ein Signal.", "svg:hand_funk", move="shake", uhr="00:00", sfx="funk"),
    S("Er telefoniert.", "favela", [fig("sohn_angst.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen", uhr="00:04"),
    S("Mit seinem *Sohn*.", "favela", [fig("oberst_seitenblick.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_wagen",
      uhr="00:09", sfx="heartbeat"),
    S("Der Wagen fährt los.", "favela", anim="peil_fahrt", uhr="00:31"),
    S("Langsam. Durch die Straßen.", "favela", anim="peil_fahrt", uhr="01:12"),
    S("Das Signal wird *stärker*.", "favela", anim="peil_nah", uhr="02:40", sfx="static"),
    S("„Er ist ganz *nah*.“", "favela", [fig("sohn_angst.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen", uhr="02:55",
      stimme="jung"),
    S("Er redet. Und redet.", "svg:hand_funk", move="zoom_in", uhr="03:30", sfx="tick"),
    S("Ein Haus. Zwei Stockwerke.", "favela", anim="haus", uhr="04:15"),
    S("Am Fenster: ein Mann mit Bart.", "svg:fenster1", move="zoom_schnell", uhr="04:40", sfx="drone_hit"),
    S("Er telefoniert *immer noch*.", "svg:fenster1", move="zoom_in", uhr="05:02"),
    S("Dein Oberst nickt.", "favela", [fig("oberst_entschlossen.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen",
      uhr="05:05"),
    S("„*Jetzt*.“", "favela", [fig("du_entschlossen.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen", move_2d="zoom_schnell",
      sfx="impact"),
    S("Ihr stürmt die Tür.", "favela", [fig("kollege_ruecken.svg", dict(x=560, y=820, w=400, boden=True), aktion="rennen_hin"),
                                        fig("du_ruecken.svg", dict(x=150, y=760, w=440, boden=True), aktion="rennen_hin")],
      anim="tuer2", move_2d="shake_stark", blitz=True, sfx="tuer"),
    S("Er flieht. Über die *Dächer*.", "favela", anim="dach_flucht", move_2d="shake", sfx="whoosh"),
    S("Ziegel splittern.", "favela", anim="dach_flucht", move_2d="shake"),
    S("*Schüsse*.", "favela", anim="dach_weit", move_2d="shake_stark", blitz=True, sfx="schuesse"),
    S("Dann: Stille.", "favela", anim="dach_weit", move_2d="statisch", stille=True),
    # ---------- FALSCHE ERLÖSUNG ----------
    S("Es ist vorbei.", "favela", [fig("kollege_erleichtert_ganz.svg", VORNE)], anim="loop_abend"),
    S("Nach anderthalb Jahren Jagd.", "favela", anim="abend"),
    S("Im ganzen Land: Eilmeldung.", "svg:tv_eilmeldung", move="zoom_in", sfx="static"),
    S("Du hast es geschafft.", "favela", [fig("du_erleichtert_ganz.svg", VORNE)], anim="loop_abend"),
    # ---------- TWIST ----------
    S("Aber weißt du, wer ihn *gefunden* hat?", "favela", anim="dach_weit2", sfx="drone_hit"),
    S("Kein Spion. Kein Verräter.", "favela", anim="peil_nah2"),
    S("Ein junger Mann im Wagen.", "favela", [fig("sohn_neutral.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_abend"),
    S("Der *Sohn* deines Obersts.", "favela", [fig("sohn_entschlossen.svg", NAH)], bgfilter=UNSCHARF, anim="loop_abend",
      sfx="impact"),
    S("Und verraten hat Escobar:", "svg:hand_funk", move="zoom_in"),
    S("ein Anruf bei *seinem* Sohn.", "svg:fenster1", move="zoom_schnell", tint="rgba(150,0,0,.25)", sfx="impact"),
    S("Er konnte nicht *auflegen*.", "svg:fenster1", move="statisch", bgfilter="grayscale(1) brightness(.6)"),
    S("Zwei Väter. Zwei Söhne.", "favela", [fig("oberst_neutral.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_abend"),
    S("Und wer den letzten Schuss abgab?", "favela", anim="dach_weit2"),
    S("Weiß bis heute *niemand*.", f"intro_zelle:{ZELLE}", [fig("einheit_bloque.svg", GANZ)], move="zoom_in",
      tint="rgba(255,60,60,.25)", ringe=True, logo=True, sfx="drone_hit"),
    # ---------- TEASER ----------
    S("Und morgen?", "intro", logo=True, sfx="whoosh", anim="outro"),
    S("Holt dich eine *andere*.", "intro", logo=True, sfx="alarm", ende_schwarz=True, anim="outro"),
]
for _s in SHOTS:
    _s.setdefault("hinweis", HINWEIS)
    _s["umriss"] = True  # Comic-Kontur um alle Figuren
# Figurenstimmen (pipeline/stimmen.py): Spind-Stimme für Intro und Teaser, Oberst für den Zugriffsbefehl
for _k in (len(SHOTS) - 2, len(SHOTS) - 1):  # Intro spricht der normale Erzähler (Nutzer-Feedback)
    SHOTS[_k]["stimme"] = "spind"
for _s in SHOTS:
    if _s["text"].startswith("„*Jetzt*"):
        _s["stimme"] = "chef"


# =====================================================================================
# 3D-ANIMATION (Favela-Szene als Medellín bei Tag; Haus mit Tür bei (6, 38, 14); Peilwagen an der Straße y≈-10)
# =====================================================================================
def _c(i):
    return -13 + 2 * i


Z, ZZ = 2.0, 2.05
SP = ["--ersatz", ERSATZ, "--fokus", "BLOQUE DE BÚSQUEDA"]
T = ["--zeit", "gold"]  # neuer Look: goldene Stunde (warmes Streiflicht, Dunst, Berge)
A = ["--zeit", "daemmerung"]
ANIM = {
    "intro": dict(szene="spinde", args=SP, keys=[
        (0.00, (_c(2) + 0.8, -2.4, Z), (_c(2) + 0.8, 0.5, ZZ), 21),
        (0.20, (_c(6), -2.4, Z), (_c(6), 0.5, ZZ), 21),
        (0.26, (_c(6) - 0.15, -2.3, Z), (_c(6) - 0.15, 0.5, ZZ), 21),
        (0.52, (_c(12), -2.4, Z), (_c(12), 0.5, ZZ), 21),
        (0.58, (_c(12) + 0.15, -2.3, Z), (_c(12) + 0.15, 0.5, ZZ), 21),
        (0.70, (_c(4), -2.4, Z), (_c(4), 0.5, ZZ), 21),
        (0.84, (_c(ZELLE), -2.3, Z), (_c(ZELLE), 0.5, ZZ), 21),
        (1.00, (_c(ZELLE), -1.5, 1.95), (_c(ZELLE), 0.5, 1.95), 21)]),
    "outro": dict(szene="spinde", args=SP, keys=[
        (0.00, (_c(ZELLE), -1.8, Z), (_c(ZELLE), 0.5, ZZ), 21),
        (0.25, (_c(ZELLE) + 0.2, -2.4, Z), (_c(ZELLE) + 0.2, 0.5, ZZ), 21),
        (0.45, (_c(1), -2.4, Z), (_c(1), 0.5, ZZ), 21),
        (0.70, (_c(11), -2.4, Z), (_c(11), 0.5, ZZ), 21),
        (1.00, (_c(11), -1.4, 1.95), (_c(11), 0.5, 1.95), 21)]),
    # tief über die Dächer auf den Hang zu, Berge dahinter – kein sichtbarer Weltrand (Vorbild: Horror Roulette)
    "anflug": dict(szene="favela", args=T + ["--berge"], keys=[(0, (-30, -70, 22), (0, 35, 20), 30), (1, (-15, -48, 15), (0, 35, 20), 30)]),
    "anflug2": dict(szene="favela", args=T + ["--berge"], keys=[(0, (45, -62, 18), (0, 35, 18), 32), (1, (28, -45, 13), (0, 35, 18), 32)]),
    "huegel": dict(szene="favela", args=T + ["--berge"], keys=[(0, (0, -30, 4), (0, 30, 16), 24), (1, (0, -24, 5), (0, 30, 18), 26)]),
    "huegel2": dict(szene="favela", args=T + ["--berge"], keys=[(0, (-10, -32, 3), (0, 30, 22), 22), (1, (-8, -30, 3.5), (0, 30, 24), 22)]),
    "gasse": dict(szene="favela", args=T, shake=0.1, keys=[(0, (1, 8, 6.7), (1, 30, 10), 20), (1, (1, 12, 7.6), (1, 30, 11), 20)]),
    "gasse_tief": dict(szene="favela", args=T, keys=[(0, (1, 6, 6.2), (1, 30, 9), 22), (1, (1, 9, 6.6), (1, 30, 10), 22)]),
    "loop_wagen": dict(szene="favela", args=T + ["--peilwagen", "steht"], loop=4.0, shake=0.12,
                       keys=[(0, (-12, -16, 1.8), (2, 10, 5), 26), (1, (-11.7, -15.8, 1.85), (2, 10, 5), 26)]),
    "peil_nah": dict(szene="favela", args=T + ["--peilwagen", "steht"], keys=[(0, (-9, -15.5, 4.2), (-4, -10, 2.6), 26),
                                                                             (1, (-8, -15.5, 4.6), (-4, -10, 2.8), 28)]),
    "peil_nah2": dict(szene="favela", args=A + ["--peilwagen", "steht"], keys=[(0, (-9, -15.5, 4.2), (-4, -10, 2.6), 26),
                                                                              (1, (-8.5, -15.5, 4.4), (-4, -10, 2.7), 30)]),
    "peil_fahrt": dict(szene="favela", args=T + ["--peilwagen", "fahrt"], keys=[(0, (-30, -18, 2.5), (-24, -10, 1.6), 24),
                                                                               (1, (-12, -18, 2.4), (-6, -10, 1.6), 24)]),
    "haus": dict(szene="favela", args=T, shake=0.08, keys=[(0, (6, 29, 15.8), (6, 37, 18.6), 22), (1, (6, 31, 16.4), (6, 37, 18.6), 24)]),
    "tuer2": dict(szene="favela", args=T + ["--tuer", "offen"], shake=0.3, keys=[(0, (6, 34.0, 17.6), (6, 40, 18.6), 20),
                                                                                (1, (6, 36.2, 18.6), (6, 41, 18.4), 20)]),
    "dach_flucht": dict(szene="favela", args=T, shake=0.35, keys=[(0, (-5, 9, 17.5), (4.6, 22, 18.0), 26),
                                                                 (1, (1, 16, 18.4), (8, 30, 18.6), 26)]),
    "dach_weit": dict(szene="favela", args=T, shake=0.1, keys=[(0, (-12, 4, 22), (4, 26, 17), 30), (1, (-10, 6, 22.5), (4, 26, 17), 34)]),
    "dach_weit2": dict(szene="favela", args=A, keys=[(0, (-12, 4, 22), (4, 26, 17), 30), (1, (-11, 5, 22.2), (4, 26, 17), 36)]),
    "abend": dict(szene="favela", args=A, keys=[(0, (-40, -60, 30), (0, 30, 12), 26), (1, (-30, -48, 24), (0, 30, 12), 28)]),
    "loop_abend": dict(szene="favela", args=A + ["--peilwagen", "steht"], loop=4.0, shake=0.1,
                       keys=[(0, (-12, -16, 1.8), (2, 10, 6), 26), (1, (-11.7, -15.8, 1.85), (2, 10, 6), 26)]),
}
ANIM_SHOTS = {i: s["anim"] for i, s in enumerate(SHOTS) if s.get("anim")}
