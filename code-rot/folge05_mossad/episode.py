"""CODE ROT – Folge 5: MOSSAD (Israel). Die Ergreifung Adolf Eichmanns, Buenos Aires, Mai 1960.
Belegte Fakten (siehe SKRIPT.md): Eichmann lebte als „Ricardo Klement“ in San Fernando bei Buenos Aires und arbeitete
bei Mercedes-Benz; am 11. Mai 1960 auf dem Heimweg von der Bushaltestelle an der Garibaldi-Straße ergriffen; er kam an
diesem Abend mit einem späteren Bus; Peter Malkin sprach ihn mit „Un momentito, señor“ an; nach rund neun Tagen in einem
Versteck betäubt und als El-Al-Besatzungsmitglied verkleidet ausgeflogen; Prozess 1961 in Jerusalem. Den entscheidenden
Hinweis gab Lothar Hermann (fast blind), dessen Tochter mit Eichmanns Sohn Klaus ausging – der Sohn trug weiter den
Namen Eichmann; über den hessischen Generalstaatsanwalt Fritz Bauer gelangte der Hinweis nach Israel.
Dramatisiert: Uhrzeiten, Dialog des Teamleiters, die Ich-Perspektive. Alle Figuren sind erfunden; Eichmann erscheint
nur als Silhouette.
"""

STIMME = "JH302OKVzGGJc47f08ex"  # Manuel
MODELL = "eleven_multilingual_v2"
ATMO = "atmo_nacht"
STIMM_EINSTELLUNG = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.15}

MITTE = dict(x=150, y=560, w=780)
LINKS = dict(x=-80, y=600, w=780)
NAH = dict(x=40, y=380, w=1000)
GANZ = dict(x=290, y=330, w=500)
SILH = dict(x=330, y=520, w=420)
UNSCHARF = "blur(10px) brightness(.55)"
SCHWARZ = "brightness(0) drop-shadow(0 0 18px rgba(255,190,120,.35))"
HINWEIS = "NACH WAHREN EREIGNISSEN · DRAMATISIERT"
ERSATZ = "SAT=MOSSAD|ISRAEL|mossad"  # Mossad-Zelle im Spind-Intro (ersetzt SAT in dieser Folge)
ZELLE = 13


def fig(name, pos=MITTE, **kw):
    d = dict(src=name, **pos); d.update(kw); return d


def S(text, bg, figuren=(), move="zoom_in", **extra):
    return dict(text=text, bg=bg, figuren=list(figuren), move=move, **extra)


BEFEHLE = ["Kein Schuss", "!Er muss leben", "Keine Spuren", "!Kein zweiter Versuch"]
KALTSTART = dict(shot=32, dauer=1.5, text="15 Jahre versteckt.|Dann: *ein* Bus.")
MANN_SILH = fig("mann_ganz.svg", SILH, filter=SCHWARZ, aktion="gehen")

SHOTS = [
    # ---------- HOOK ----------
    S("Eine dieser *Einheiten*", "intro", logo=True, sfx="whoosh", anim="intro", stimme="spind"),
    S("holt dich heute Nacht.", "intro", logo=True, sfx="whoosh", anim="intro", stimme="spind"),
    S("Mal sehen,", "intro", logo=True, sfx="whoosh", anim="intro", stimme="spind"),
    S("ob du *zurückkommst*.", "intro", logo=True, sfx="alarm", ende_blitz=True, anim="intro", stimme="spind"),
    S("", f"intro_zelle:{ZELLE}", [fig("einheit_mossad.svg", GANZ, filter="drop-shadow(0 0 30px rgba(255,40,40,.6))")],
      move="zoom_schnell", titel="*MOSSAD*", untertitel="ISRAEL · SEIT 1949", ringe=True, logo=True,
      tint="rgba(255,60,60,.35)", pause=1.5, sfx="impact"),
    # ---------- SETUP ----------
    S("_Buenos Aires_.", "strasse", anim="anflug", sfx="whoosh", blitz=True),
    S("Mai 1960.", "strasse", anim="anflug", sprich="Mai neunzehnhundertsechzig."),
    S("Du bist Agent des *Mossad*.", "strasse", [fig("du_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_auto"),
    S("Seit Wochen beobachtet ihr einen Mann.", "strasse", anim="strasse"),
    S("Er arbeitet in einer Autofabrik.", "strasse", [MANN_SILH], bgfilter="brightness(.8)", anim="loop_strasse"),
    S("Er nennt sich _Ricardo Klement_.", "svg:fenster1", move="zoom_in"),
    S("Aber sein echter Name ist ein anderer.", "svg:fenster1", move="zoom_schnell", sfx="drone_hit"),
    S("_Adolf Eichmann_.", "svg:fenster1", move="statisch", bgfilter="grayscale(1) brightness(.7)", sfx="impact"),
    S("Einer der Organisatoren des *Holocaust*.", "strasse", anim="huegel_nacht", tint="rgba(120,0,0,.25)"),
    S("Seit fünfzehn Jahren auf der Flucht.", "strasse", anim="huegel_nacht"),
    # ---------- LAGE ----------
    S("Jeden Abend nimmt er denselben Bus.", "strasse", anim="bus_fahrt", sfx="whoosh"),
    S("Steigt an derselben Haltestelle aus.", "strasse", anim="bus_steht"),
    S("Läuft dieselbe dunkle Straße entlang.", "strasse", [MANN_SILH], bgfilter="brightness(.8)", anim="loop_strasse"),
    S("Bis zu seinem Haus.", "strasse", anim="haus"),
    S("Dein Teamleiter sagt nur:", "strasse", [fig("teamleiter_entschlossen.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_auto"),
    S("„Er muss *lebend* nach Israel.“", "strasse", [fig("teamleiter_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_auto", stimme="chef", sfx="heartbeat"),
    # ---------- BEFEHLE ----------
    S("Deine Befehle:", "strasse", [fig("teamleiter_entschlossen_zeigen.svg", LINKS)], bgfilter=UNSCHARF,
      anim="loop_auto", regeln=0),
    S("Kein Schuss.", "strasse", [fig("du_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_auto", regeln=1),
    S("Er muss *leben*.", "strasse", [fig("kollege_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_auto", regeln=2),
    S("Keine Spuren.", "strasse", anim="strasse", regeln=3),
    S("Und: Es gibt *keinen* zweiten Versuch.", "strasse", [fig("teamleiter_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_auto", move_2d="zoom_schnell", regeln=4, sfx="impact"),
    # ---------- ANNÄHERUNG ----------
    S("Elfter Mai.", "strasse", anim="strasse2", uhr="19:40", sprich="Elfter Mai."),
    S("Ihr wartet im Auto.", "strasse", [fig("du_angst.svg", NAH)], bgfilter=UNSCHARF, anim="loop_auto", uhr="19:40",
      sfx="tick"),
    S("Der Bus kommt.", "strasse", anim="bus_fahrt", uhr="19:41"),
    S("Er steigt *nicht* aus.", "strasse", anim="bus_steht", uhr="19:42", sfx="drone_hit"),
    S("Ihr überlegt abzubrechen.", "strasse", [fig("kollege_seitenblick.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_auto", uhr="19:58"),
    S("Dann: noch ein Bus.", "strasse", anim="bus_fahrt", uhr="20:05", sfx="whoosh"),
    S("Ein Mann steigt aus.", "strasse", [MANN_SILH], bgfilter="brightness(.8)", anim="loop_strasse", uhr="20:05",
      sfx="heartbeat"),
    S("Eine Hand in der Manteltasche.", "strasse", [MANN_SILH], bgfilter="brightness(.7)", anim="loop_strasse",
      move_2d="zoom_schnell", uhr="20:05"),
    S("Dein Kollege geht auf ihn zu.", "strasse", [fig("kollege_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_strasse", uhr="20:05"),
    S("„*Un momentito, señor*.“", "strasse", [fig("kollege_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_strasse", uhr="20:05", stimme="jung"),
    S("Dann geht alles schnell.", "strasse", anim="zugriff", move_2d="shake_stark", blitz=True, uhr="20:05", sfx="impact"),
    S("Ins Auto. Eine Decke drüber.", "strasse", anim="zugriff", move_2d="shake", uhr="20:06", sfx="tuer"),
    S("Kein Schuss.", "strasse", anim="auto_weg", uhr="20:06"),
    S("Niemand hat etwas gesehen.", "strasse", anim="auto_weg", move_2d="statisch", stille=True, uhr="20:06"),
    # ---------- FALSCHE ERLÖSUNG ----------
    S("Neun Tage später.", "rollfeld", anim="flughafen", sfx="whoosh", blitz=True),
    S("Ein Flugzeug der El Al.", "rollfeld", anim="flughafen"),
    S("An Bord: ein Mann in Crew-Uniform.", "rollfeld", anim="flugzeug_nah"),
    S("Er schläft. Betäubt.", "rollfeld", anim="flugzeug_nah"),
    S("Du hast es geschafft.", "strasse", [fig("du_erleichtert.svg", MITTE)], bgfilter="blur(10px) brightness(.7)",
      anim="loop_auto"),
    S("Ein Jahr später: der Prozess in Jerusalem.", "svg:tv_prozess", move="zoom_in", sfx="static"),
    # ---------- TWIST ----------
    S("Aber weißt du, wer ihn *wirklich* gefunden hat?", "strasse", anim="huegel_nacht", sfx="drone_hit"),
    S("Kein Agent.", "strasse", [fig("teamleiter_seitenblick.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_auto"),
    S("Ein Mann, der fast *blind* war.", "svg:fenster1", move="zoom_in", bgfilter="blur(3px) brightness(.8)"),
    S("Seine Tochter ging mit einem jungen Mann aus.", "strasse", anim="strasse"),
    S("Der redete gern über seinen Vater.", "strasse", anim="strasse2"),
    S("Der Vater nannte sich _Klement_.", "svg:fenster1", move="zoom_in"),
    S("Der Sohn hieß immer noch *Eichmann*.", "svg:fenster1", move="zoom_schnell", tint="rgba(150,0,0,.25)",
      sfx="impact"),
    S("Fünfzehn Jahre Versteck.", "strasse", anim="haus"),
    S("Verraten von seinem *eigenen* Namen.", f"intro_zelle:{ZELLE}", [fig("einheit_mossad.svg", GANZ)], move="zoom_in",
      tint="rgba(255,60,60,.25)", ringe=True, logo=True, sfx="drone_hit"),
    # ---------- TEASER ----------
    S("Und morgen?", "intro", logo=True, sfx="whoosh", anim="outro", stimme="spind"),
    S("Holt dich eine *andere*.", "intro", logo=True, sfx="alarm", ende_schwarz=True, anim="outro", stimme="spind"),
]
for _s in SHOTS:
    _s.setdefault("hinweis", HINWEIS)


# =====================================================================================
# 3D-ANIMATION: Straße bei Nacht (Favela-Szene, Straße unten bei y≈-10) + Flughafen (Rollfeld-Szene ohne Zusätze)
# =====================================================================================
def _c(i):
    return -13 + 2 * i


Z, ZZ = 2.0, 2.05
SP = ["--ersatz", ERSATZ, "--fokus", "MOSSAD"]
AU = ["--auto", "steht"]
ANIM = {
    "intro": dict(szene="spinde", args=SP, keys=[
        (0.00, (_c(3) + 0.8, -2.4, Z), (_c(3) + 0.8, 0.5, ZZ), 21),
        (0.20, (_c(8), -2.4, Z), (_c(8), 0.5, ZZ), 21),
        (0.26, (_c(8) - 0.15, -2.3, Z), (_c(8) - 0.15, 0.5, ZZ), 21),
        (0.52, (_c(1), -2.4, Z), (_c(1), 0.5, ZZ), 21),
        (0.58, (_c(1) + 0.15, -2.3, Z), (_c(1) + 0.15, 0.5, ZZ), 21),
        (0.70, (_c(10), -2.4, Z), (_c(10), 0.5, ZZ), 21),
        (0.84, (_c(ZELLE), -2.3, Z), (_c(ZELLE), 0.5, ZZ), 21),
        (1.00, (_c(ZELLE), -1.5, 1.95), (_c(ZELLE), 0.5, 1.95), 21)]),
    "outro": dict(szene="spinde", args=SP, keys=[
        (0.00, (_c(ZELLE), -1.8, Z), (_c(ZELLE), 0.5, ZZ), 21),
        (0.25, (_c(ZELLE) - 0.2, -2.4, Z), (_c(ZELLE) - 0.2, 0.5, ZZ), 21),
        (0.45, (_c(4), -2.4, Z), (_c(4), 0.5, ZZ), 21),
        (0.70, (_c(9), -2.4, Z), (_c(9), 0.5, ZZ), 21),
        (1.00, (_c(9), -1.4, 1.95), (_c(9), 0.5, 1.95), 21)]),
    "anflug": dict(szene="favela", args=AU, keys=[(0, (-90, -120, 80), (0, 0, 6), 26), (1, (-50, -80, 40), (0, -6, 4), 28)]),
    "huegel_nacht": dict(szene="favela", keys=[(0, (0, -30, 4), (0, 30, 16), 24), (1, (0, -25, 4.6), (0, 30, 17), 26)]),
    "strasse": dict(szene="favela", args=AU, shake=0.08, keys=[(0, (-20, -13.5, 1.7), (10, -10, 1.6), 22),
                                                             (1, (-16, -13.5, 1.7), (14, -10, 1.6), 22)]),
    "strasse2": dict(szene="favela", args=AU, shake=0.06, keys=[(0, (14, -14, 2.2), (-10, -9, 1.8), 24),
                                                              (1, (11, -14, 2.0), (-12, -9, 1.8), 26)]),
    "loop_strasse": dict(szene="favela", args=AU, loop=4.0, shake=0.1, keys=[(0, (-10, -14, 1.6), (6, -9, 1.7), 26),
                                                                            (1, (-9.7, -13.8, 1.62), (6, -9, 1.7), 26)]),
    "loop_auto": dict(szene="favela", args=AU, loop=4.0, shake=0.12, keys=[(0, (10.5, -7.0, 2.1), (-10, -9, 1.3), 26),
                                                                          (1, (10.2, -7.1, 2.12), (-10, -9, 1.3), 26)]),
    "bus_fahrt": dict(szene="favela", args=AU + ["--bus", "fahrt"], keys=[(0, (2, -15.5, 1.6), (-20, -10, 1.8), 34),
                                                                         (1, (2, -15.5, 1.6), (-6, -10, 1.8), 34)]),
    "bus_steht": dict(szene="favela", args=AU + ["--bus", "steht"], shake=0.05, keys=[(0, (8, -15, 1.7), (-2, -10, 1.8), 28),
                                                                                     (1, (7.5, -15, 1.7), (-2, -10, 1.8), 32)]),
    "haus": dict(szene="favela", shake=0.08, keys=[(0, (6, 29, 15.8), (6, 37, 18.6), 22), (1, (6, 31, 16.4), (6, 37, 18.6), 24)]),
    "zugriff": dict(szene="favela", args=AU, shake=0.35, keys=[(0, (10, -12, 1.5), (6, -7.6, 1.0), 22),
                                                             (1, (8.5, -11, 1.4), (6, -7.6, 1.0), 20)]),
    "auto_weg": dict(szene="favela", keys=[(0, (6, -14, 1.6), (-20, -9, 1.6), 26), (1, (6, -14, 1.6), (-24, -9, 1.6), 28)]),
    "flughafen": dict(szene="rollfeld", args=["--leer", "--fire", "0"], keys=[(0, (-70, -80, 70), (0, 0, 0), 28),
                                                                            (1, (-40, -52, 38), (4, 0, 2), 30)]),
    "flugzeug_nah": dict(szene="rollfeld", args=["--leer", "--fire", "0"], keys=[(0, (8, -8.5, 3.1), (0, -1.9, 3.5), 30),
                                                                               (1, (3, -8.0, 3.2), (-5, -1.9, 3.5), 30)]),
}
ANIM_SHOTS = {i: s["anim"] for i, s in enumerate(SHOTS) if s.get("anim")}
