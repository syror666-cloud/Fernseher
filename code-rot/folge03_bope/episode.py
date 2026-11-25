"""CODE ROT – Folge 3: BOPE (Rio de Janeiro). Typischer Nachteinsatz – frei erzähltes Szenario, keine echte Operation.
Belegte Fakten: Gründung 1978, Panzerwagen „Caveirão“ (= großer Totenkopf), Feuerwerk der „Fogueteiros“ als Warnung
bei Polizeieinsätzen und als Feier. Alle Personen sind erfunden.
"""

STIMME = "JH302OKVzGGJc47f08ex"  # Manuel
MODELL = "eleven_multilingual_v2"
ATMO = "atmo_stadt"
STIMM_EINSTELLUNG = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.15}

MITTE = dict(x=150, y=560, w=780)
LINKS = dict(x=-80, y=600, w=780)
NAH = dict(x=40, y=380, w=1000)
TIEF = dict(x=150, y=1150, w=780)
GANZ = dict(x=290, y=330, w=500)
VOLL = dict(x=0, y=0, w=1080)
UNSCHARF = "blur(10px) brightness(.55)"
HINWEIS = "SZENARIO · FREI NACHERZÄHLT"


def fig(name, pos=MITTE, **kw):
    d = dict(src=name, **pos); d.update(kw); return d


def S(text, bg, figuren=(), move="zoom_in", **extra):
    return dict(text=text, bg=bg, figuren=list(figuren), move=move, **extra)


BEFEHLE = ["Bleib hinter dem Schild", "!Kein Fenster aus den Augen", "Hier wohnen Familien", "!Niemand bleibt zurück"]
# Hook für den aggressiven Schnitt (cut.py --aggressiv): Höhepunkt vorweg
KALTSTART = dict(shot=53, dauer=1.6, text="Wer hat dich|*verraten*?")
FW = [dict(typ="feuerwerk", n=7, seed=15), dict(typ="staub", n=40, alpha=0.5, seed=16)]
FW_VIEL = [dict(typ="feuerwerk", n=16, seed=21), dict(typ="staub", n=40, alpha=0.5, seed=22)]

SHOTS = [
    # ---------- HOOK ----------
    S("Eine dieser *Einheiten*", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("holt dich heute Nacht.", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("Mal sehen,", "intro", logo=True, sfx="whoosh", anim="intro"),
    S("ob du *zurückkommst*.", "intro", logo=True, sfx="alarm", ende_blitz=True, anim="intro"),
    S("", "intro_zelle:3", [fig("einheit_bope.svg", GANZ, filter="drop-shadow(0 0 30px rgba(255,40,40,.6))")],
      move="zoom_schnell", titel="*BOPE*", untertitel="RIO DE JANEIRO · SEIT 1978", ringe=True, logo=True,
      tint="rgba(255,60,60,.35)", pause=1.5, sfx="impact"),
    # ---------- SETUP ----------
    S("_Rio de Janeiro_.", "favela", anim="anflug", sfx="whoosh", blitz=True),
    S("Vier Uhr morgens.", "favela", anim="anflug", uhr="04:00", sprich="Vier Uhr morgens."),
    S("Du sitzt in einem schwarzen Panzerwagen.", "favela", anim="caveirao_fahrt", uhr="04:00"),
    S("Sie nennen ihn _Caveirão_.", "favela", anim="caveirao_nah", uhr="04:01", sprich="Sie nennen ihn Kaweiraung."),
    S("Den großen *Totenkopf*.", "favela", anim="caveirao_nah", uhr="04:01", sfx="drone_hit"),
    S("Neben dir: dein Truppführer.", "favela", [fig("truppfuehrer_neutral.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_wagen", uhr="04:01"),
    S("Seit zwanzig Jahren dabei.", "favela", [fig("truppfuehrer_seitenblick.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_wagen", uhr="04:01"),
    S("Vor euch: ein Hügel. Tausende Häuser.", "favela", anim="huegel", uhr="04:02"),
    S("Eine _Favela_.", "favela", anim="huegel", uhr="04:02"),
    S("Euer Ziel: ein Mann, den hier jeder kennt.", "favela", anim="gasse_tief", uhr="04:02"),
    S("Und *keiner* verrät.", "favela", anim="gasse_tief", uhr="04:03", sfx="impact"),
    S("Dein Truppführer sagt nur:", "favela", [fig("truppfuehrer_entschlossen.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_wagen", uhr="04:03"),
    S("„Wenn du *Feuerwerk* hörst,", "favela", [fig("truppfuehrer_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_wagen", uhr="04:03"),
    S("wissen sie, dass wir kommen.“", "favela", [fig("du_angst.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_wagen",
      uhr="04:03", sfx="heartbeat"),
    # ---------- LAGE ----------
    S("Gassen, so schmal wie ein Flur.", "favela", anim="gasse", uhr="04:04"),
    S("Treppen ohne Ende.", "favela", anim="treppe", uhr="04:04"),
    S("Stromkabel wie Spinnennetze.", "favela", anim="kabel", uhr="04:05"),
    S("Auf einem Dach: ein *Junge*.", "favela", anim="dach", uhr="04:05"),
    S("Er schaut euch an.", "favela", [fig("junge_neutral.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_dach", uhr="04:05"),
    S("Und verschwindet.", "favela", anim="dach_leer", uhr="04:05", move_2d="zoom_schnell"),
    S("Dann: ein Zischen.", "favela", anim="huegel2", uhr="04:06", sfx="whoosh"),
    S("*Feuerwerk*. Über dem ganzen Hügel.", "favela", anim="huegel2", fx=FW, uhr="04:06", blitz=True, sfx="feuerwerk"),
    S("Sie *wissen* es.", "favela", [fig("du_angst.svg", NAH)], bgfilter=UNSCHARF, anim="loop_wagen", fx=FW,
      move_2d="shake", uhr="04:06"),
    # ---------- BEFEHLE ----------
    S("Deine Befehle:", "favela", [fig("truppfuehrer_entschlossen_zeigen.svg", LINKS)], bgfilter=UNSCHARF,
      anim="loop_gasse", regeln=0),
    S("Bleib hinter dem Schild.", "favela", [fig("du_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, anim="loop_gasse", regeln=1),
    S("Kein Fenster aus den Augen.", "favela", [fig("kollege_entschlossen.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_gasse", regeln=2),
    S("Hier wohnen *Familien*.", "favela", anim="gasse", regeln=3),
    S("Und: *Niemand* bleibt zurück.", "favela", [fig("truppfuehrer_entschlossen.svg", NAH)], bgfilter=UNSCHARF,
      anim="loop_gasse", move_2d="zoom_schnell", regeln=4, sfx="impact"),
    # ---------- ANNÄHERUNG ----------
    S("Vier Uhr zwölf.", "favela", anim="aussteigen", uhr="04:12", sfx="tick"),
    S("Ihr steigt aus.", "favela", anim="aussteigen", uhr="04:12", sfx="tuer"),
    S("Hundert Stufen.", "favela", anim="treppe2", uhr="04:14"),
    S("Zweihundert.", "favela", [fig("du_angst.svg", NAH)], bgfilter=UNSCHARF, anim="loop_gasse", uhr="04:17", sfx="atem"),
    S("Ein Hund bellt.", "favela", anim="gasse2", uhr="04:18"),
    S("Dann *keiner* mehr.", "favela", anim="gasse2", uhr="04:18", move_2d="statisch", stille=True),
    S("Ein Fernseher läuft. Niemand schaut zu.", "svg:tv_rauschen", move="zoom_in", uhr="04:19", sfx="static"),
    S("Das Haus.", "favela", anim="tuer", uhr="04:20"),
    S("Blaue Tür.", "favela", anim="tuer", uhr="04:20"),
    S("Dein Truppführer zählt mit den Fingern.", "favela", [fig("truppfuehrer_entschlossen_zeigen.svg", NAH)],
      bgfilter=UNSCHARF, anim="loop_gasse", uhr="04:20"),
    S("Drei. Zwei. Eins.", "favela", [fig("du_entschlossen.svg", NAH)], bgfilter=UNSCHARF, anim="loop_gasse",
      uhr="04:21", sfx="heartbeat"),
    S("Die Tür fliegt auf.", "favela", anim="tuer2", move_2d="shake_stark", blitz=True, uhr="04:21", sfx="tuer"),
    S("*Leer*.", "favela", anim="raum", uhr="04:21", move_2d="statisch"),
    S("Auf dem Tisch: eine Tasse Kaffee.", "favela", anim="raum", uhr="04:22"),
    S("Noch *warm*.", "favela", [fig("du_seitenblick.svg", NAH)], bgfilter=UNSCHARF, anim="loop_gasse", uhr="04:22",
      sfx="drone_hit"),
    # ---------- FALSCHE ERLÖSUNG ----------
    S("Ihr kommt raus.", "favela", anim="treppe_runter", uhr="05:10"),
    S("Ohne Schuss. Niemand verletzt.", "favela", [fig("kollege_erleichtert.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_morgen", uhr="05:12"),
    S("Die Sonne geht auf über _Rio_.", "favela", anim="morgen", uhr="05:41"),
    S("Du hast es geschafft.", "favela", [fig("du_erleichtert.svg", MITTE)], bgfilter="blur(10px) brightness(.8)",
      anim="loop_morgen"),
    # ---------- TWIST ----------
    S("Dann knallt es wieder.", "favela", anim="morgen2", fx=FW, blitz=True, sfx="impact"),
    S("*Feuerwerk*. Mehr als vorhin.", "favela", anim="morgen2", fx=FW_VIEL, sfx="feuerwerk"),
    S("Viel mehr.", "favela", anim="morgen2", fx=FW_VIEL, move_2d="zoom_schnell"),
    S("Du greifst nach der Waffe.", "favela", [fig("du_angst.svg", NAH)], bgfilter=UNSCHARF, anim="loop_morgen", fx=FW_VIEL,
      move_2d="shake"),
    S("Dein Truppführer schüttelt den Kopf.", "favela", [fig("truppfuehrer_neutral.svg", MITTE)], bgfilter=UNSCHARF,
      anim="loop_morgen", fx=FW),
    S("„Das ist kein Alarm.", "favela", [fig("truppfuehrer_seitenblick.svg", NAH)], bgfilter=UNSCHARF, anim="loop_morgen", fx=FW),
    S("Das ist eine *Party*.“", "favela", anim="morgen2", fx=FW_VIEL),
    S("Sie *feiern*. Dass ihr wieder geht.", "favela", anim="morgen2", fx=FW_VIEL, sfx="drone_hit"),
    S("Auf dem Dach steht wieder der Junge.", "favela", anim="dach_morgen", fx=FW),
    S("Er *winkt*.", "favela", [fig("junge_erleichtert.svg", MITTE)], bgfilter="blur(8px) brightness(.8)", anim="loop_morgen", fx=FW),
    S("Er hat euch heute Nacht *angekündigt*.", "favela", anim="dach_morgen", fx=FW, tint="rgba(150,0,0,.2)"),
    S("Er ist _zwölf_.", "favela", [fig("junge_neutral.svg", NAH)], bgfilter="blur(8px) brightness(.7)", anim="loop_morgen",
      fx=FW, sfx="impact"),
    # ---------- LOOP-ENDE ----------
    S("Ihr habt die Tür gefunden.", "favela", anim="abfahrt"),
    S("Er hat *euch* gefunden.", "favela", anim="abfahrt", fx=FW),
    S("Lange bevor ihr ausgestiegen seid.", "intro_zelle:3", [fig("einheit_bope.svg", GANZ)], move="zoom_in",
      tint="rgba(255,60,60,.25)", ringe=True, logo=True),
    # ---------- TEASER ----------
    S("Und morgen?", "intro", logo=True, sfx="whoosh", anim="outro"),
    S("Holt dich eine *andere*.", "intro", logo=True, sfx="alarm", ende_schwarz=True, anim="outro"),
]
for _s in SHOTS:
    _s.setdefault("hinweis", HINWEIS)

# Figurenstimmen (pipeline/stimmen.py): Einstellung -> Rolle
FIGURENSTIMMEN = {0: 'spind', 1: 'spind', 2: 'spind', 3: 'spind', 67: 'spind', 68: 'spind', 17: 'chef', 18: 'chef', 57: 'chef', 58: 'chef'}
STIMME_AB = {}
for _k, _r in FIGURENSTIMMEN.items():
    SHOTS[_k]["stimme"] = _r
for _k, _w in STIMME_AB.items():
    SHOTS[_k]["stimme_ab"] = _w


# =====================================================================================
# 3D-ANIMATION (Favela: Hang steigt nach +y an; Straße unten bei y≈-10; Haus mit blauer Tür bei (6, 38, 14))
# =====================================================================================
def _c(i):
    return -13 + 2 * i


Z, ZZ = 2.0, 2.05
ANIM = {
    "intro": dict(szene="spinde", keys=[
        (0.00, (_c(8) + 0.8, -2.4, Z), (_c(8) + 0.8, 0.5, ZZ), 21),
        (0.20, (_c(12), -2.4, Z), (_c(12), 0.5, ZZ), 21),
        (0.26, (_c(12) - 0.15, -2.3, Z), (_c(12) - 0.15, 0.5, ZZ), 21),
        (0.52, (_c(5), -2.4, Z), (_c(5), 0.5, ZZ), 21),
        (0.58, (_c(5) + 0.15, -2.3, Z), (_c(5) + 0.15, 0.5, ZZ), 21),
        (0.70, (_c(1), -2.4, Z), (_c(1), 0.5, ZZ), 21),
        (0.84, (_c(3), -2.3, Z), (_c(3), 0.5, ZZ), 21),
        (1.00, (_c(3), -1.5, 1.95), (_c(3), 0.5, 1.95), 21)]),
    "outro": dict(szene="spinde", keys=[
        (0.00, (_c(3), -1.8, Z), (_c(3), 0.5, ZZ), 21),
        (0.25, (_c(3) + 0.2, -2.4, Z), (_c(3) + 0.2, 0.5, ZZ), 21),
        (0.45, (_c(10), -2.4, Z), (_c(10), 0.5, ZZ), 21),
        (0.70, (_c(7), -2.4, Z), (_c(7), 0.5, ZZ), 21),
        (1.00, (_c(7), -1.4, 1.95), (_c(7), 0.5, 1.95), 21)]),
    "anflug": dict(szene="favela", keys=[(0, (-90, -120, 80), (0, 30, 10), 26), (1, (-50, -80, 45), (0, 30, 12), 28)]),
    "caveirao_fahrt": dict(szene="favela", args=["--caveirao", "fahrt"], keys=[(0, (-14, -16, 2.5), (0, -10, 1.5), 24),
                                                                            (1, (-6, -17, 2.2), (6, -10, 1.5), 24)]),
    "caveirao_nah": dict(szene="favela", args=["--caveirao", "steht"], keys=[(0, (3, -15, 1.0), (0, -10, 1.6), 22),
                                                                          (1, (2, -14.5, 0.9), (0, -10, 1.8), 22)]),
    "loop_wagen": dict(szene="favela", args=["--caveirao", "steht"], loop=4.0, shake=0.12,
                       keys=[(0, (-4, -13, 1.8), (2, 10, 5), 26), (1, (-3.7, -12.8, 1.85), (2, 10, 5), 26)]),
    "huegel": dict(szene="favela", keys=[(0, (0, -30, 4), (0, 30, 16), 24), (1, (0, -24, 5), (0, 30, 18), 26)]),
    "huegel2": dict(szene="favela", keys=[(0, (-10, -32, 3), (0, 30, 22), 22), (1, (-8, -30, 3.5), (0, 30, 24), 22)]),
    "gasse_tief": dict(szene="favela", keys=[(0, (1, 6, 6.2), (1, 30, 9), 22), (1, (1, 9, 6.6), (1, 30, 10), 22)]),
    "gasse": dict(szene="favela", shake=0.1, keys=[(0, (1, 8, 6.7), (1, 30, 10), 20), (1, (1, 12, 7.6), (1, 30, 11), 20)]),
    "gasse2": dict(szene="favela", shake=0.08, keys=[(0, (1, 18, 9.8), (1, 40, 13), 20), (1, (1, 20, 10.4), (1, 40, 13), 20)]),
    "loop_gasse": dict(szene="favela", loop=4.0, shake=0.12, keys=[(0, (1, 14, 8.2), (1, 30, 11), 22), (1, (1.2, 14.4, 8.3), (1, 30, 11), 22)]),
    "treppe": dict(szene="favela", shake=0.1, keys=[(0, (-6, 10, 7.4), (-6, 30, 14), 20), (1, (-6, 14, 9.2), (-6, 30, 15), 20)]),
    "treppe2": dict(szene="favela", shake=0.15, keys=[(0, (-6, 16, 10), (-6, 32, 16), 20), (1, (-6, 22, 12.6), (-6, 34, 17), 20)]),
    "kabel": dict(szene="favela", keys=[(0, (1, 12, 7.5), (2, 20, 16), 18), (1, (1, 13, 7.8), (-1, 20, 16), 18)]),
    "dach": dict(szene="favela", args=["--junge", "ja"], keys=[(0, (-5, 9, 17.5), (4.6, 22, 18.4), 34), (1, (-4.5, 10, 17.6), (4.6, 22, 18.4), 40)]),
    "dach_leer": dict(szene="favela", keys=[(0, (-4.5, 10, 17.6), (4.6, 22, 18.4), 40), (1, (-4.4, 10.2, 17.6), (4.6, 22, 18.4), 44)]),
    "loop_dach": dict(szene="favela", loop=3.0, shake=0.06, keys=[(0, (-5, 9, 17.5), (4.6, 22, 18.4), 34), (1, (-4.9, 9.1, 17.5), (4.6, 22, 18.4), 34)]),
    "aussteigen": dict(szene="favela", args=["--caveirao", "steht"], shake=0.15, keys=[(0, (-2, -12, 1.4), (1, 6, 6), 20),
                                                                                    (1, (0, -8, 1.8), (1, 20, 8), 20)]),
    "tuer": dict(szene="favela", shake=0.08, keys=[(0, (6, 29, 15.8), (6, 37, 18.6), 22), (1, (6, 31, 16.4), (6, 37, 18.6), 24)]),
    "tuer2": dict(szene="favela", args=["--tuer", "offen"], shake=0.3, keys=[(0, (6, 34.0, 17.6), (6, 40, 18.6), 20),
                                                                          (1, (6, 36.2, 18.6), (6, 41, 18.4), 20)]),
    "raum": dict(szene="favela", args=["--tuer", "offen"], shake=0.06, keys=[(0, (6, 37.6, 19.4), (7.0, 41, 18.2), 22),
                                                                          (1, (6, 38.2, 19.3), (7.0, 41, 18.2), 24)]),
    "treppe_runter": dict(szene="favela", args=["--zeit", "daemmerung"], shake=0.1, keys=[(0, (-6, 26, 13.2), (-6, 4, 5), 20),
                                                                                       (1, (-6, 20, 11.0), (-6, 0, 4), 20)]),
    "morgen": dict(szene="favela", args=["--zeit", "morgen"], keys=[(0, (-40, -60, 30), (0, 30, 12), 26), (1, (-30, -48, 24), (0, 30, 12), 28)]),
    "morgen2": dict(szene="favela", args=["--zeit", "morgen"], keys=[(0, (0, -30, 4), (0, 30, 22), 22), (1, (-3, -28, 4.5), (0, 30, 24), 22)]),
    "loop_morgen": dict(szene="favela", args=["--zeit", "morgen", "--caveirao", "steht"], loop=4.0, shake=0.1,
                        keys=[(0, (-4, -13, 1.8), (2, 10, 6), 26), (1, (-3.7, -12.8, 1.85), (2, 10, 6), 26)]),
    "dach_morgen": dict(szene="favela", args=["--zeit", "morgen", "--junge", "winkt"], keys=[(0, (-5, 9, 17.5), (4.6, 22, 18.4), 34),
                                                                                         (1, (-4.6, 9.6, 17.6), (4.6, 22, 18.4), 40)]),
    "abfahrt": dict(szene="favela", args=["--zeit", "morgen", "--caveirao", "ab"], keys=[(0, (-20, -26, 6), (0, -10, 2), 24),
                                                                                       (1, (-40, -50, 20), (0, 10, 5), 24)]),
}
ANIM_SHOTS = {i: s["anim"] for i, s in enumerate(SHOTS) if s.get("anim")}
