"""CODE ROT – Folge 1: GSG 9. Einstellungsliste (Shotlist) für die automatische Pipeline.

Jede Einstellung: Text (VO + Untertitel, *rot* _gelb_), Hintergrund, Figuren, Bewegung, Extras.
Hintergründe: Blender-Renders in bg/ (Name ohne .png) oder "intro:<x>" (Spind-Streifen) oder "svg:<name>".
Bewegungen: zoom_in, zoom_out, zoom_schnell, pan_l, pan_r, pan_hoch, shake, shake_stark, statisch, whip:<von>:<bis>
"""

STIMME = "JH302OKVzGGJc47f08ex"  # Manuel – Profound, Deep and Strong
MODELL = "eleven_multilingual_v2"
STIMM_EINSTELLUNG = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.15}

# Standard-Platzierungen für Halbnah-Figuren (viewBox 600x1000)
MITTE = dict(x=150, y=560, w=780)
LINKS = dict(x=-80, y=600, w=780)
RECHTS = dict(x=380, y=600, w=780)
NAH = dict(x=40, y=380, w=1000)
TIEF = dict(x=150, y=1150, w=780)        # nur Kopf schaut über den Bildrand (liegend)
GANZ = dict(x=290, y=330, w=500)


def fig(name, pos=MITTE, **kw):
    d = dict(src=name, **pos); d.update(kw); return d


def S(text, bg, figuren=(), move="zoom_in", **extra):
    return dict(text=text, bg=bg, figuren=list(figuren), move=move, **extra)


BEFEHLE = ["Kein Laut bis zum Signal", "!Alle Türen gleichzeitig", "Geiseln zuerst", "!Kein zweiter Versuch"]
UNSCHARF = "blur(10px) brightness(.55)"

SHOTS = [
    # ---------- 1 HOOK ----------
    S("Eine dieser *Einheiten*", "intro", move="whip:0:3", logo=True, sfx="whoosh"),
    S("holt dich heute Nacht.", "intro", move="whip:3:9", logo=True, sfx="whoosh"),
    S("Mal sehen,", "intro", move="whip:9:4", logo=True, sfx="whoosh"),
    S("ob du *zurückkommst*.", "intro", move="whip:4:6", logo=True, sfx="alarm", ende_blitz=True),
    # ---------- 2 TITELKARTE ----------
    S("", "intro_zelle:6", [fig("einheit_gsg9.svg", GANZ, filter="drop-shadow(0 0 30px rgba(255,40,40,.6))")],
      move="zoom_schnell", titel="GSG *9*", untertitel="BUNDESPOLIZEI · SEIT 1972", ringe=True, logo=True,
      tint="rgba(255,60,60,.35)", pause=1.5, sfx="impact"),
    # ---------- 3 SETUP ----------
    S("_Mogadischu_.", "drohne", move="zoom_in", sfx="whoosh", blitz=True),
    S("Oktober _1977_.", "drohne", move="pan_r", sprich="Oktober neunzehnhundertsiebenundsiebzig."),
    S("In Deutschland ist es kurz vor *Mitternacht*.", "boden", move="zoom_in"),
    S("Hier ist es kurz vor _zwei_.", "boden_tief", move="zoom_in", uhr="01:58", sfx="tick"),
    S("Du liegst im Sand.", "boden_tief", [fig("du_neutral.svg", TIEF)], move="zoom_in", uhr="01:58"),
    S("Neben der Rollbahn.", "boden_tief", [fig("du_seitenblick.svg", TIEF)], move="pan_r", uhr="01:58"),
    S("Vor dir: eine Lufthansa-Maschine.", "boden", move="zoom_in", uhr="01:59"),
    S("Die _Landshut_.", "fenster", move="zoom_in", uhr="01:59"),
    S("Seit fünf Tagen in der Hand von vier *Entführern*.", "svg:fenster1", move="zoom_in", uhr="01:59", sfx="drone_hit"),
    S("Fast neunzig Menschen an Bord.", "kabine_dunkel", move="zoom_in", uhr="01:59"),
    S("Den Kapitän haben sie schon *erschossen*.", "kabine_dunkel", move="statisch", uhr="01:59",
      tint="rgba(200,20,20,.35)", sfx="impact"),
    S("Dein Truppführer flüstert nur einen Satz:", "boden_tief", [fig("truppfuehrer_neutral.svg", MITTE)],
      bgfilter=UNSCHARF, uhr="01:59"),
    S("„Wenn das *Feuer* brennt,", "boden_tief", [fig("truppfuehrer_entschlossen.svg", NAH)], bgfilter=UNSCHARF, uhr="01:59"),
    S("laufen wir.“", "boden_tief", [fig("du_angst.svg", MITTE)], bgfilter=UNSCHARF, uhr="01:59", sfx="heartbeat"),
    # ---------- 4 LAGE / OFFENE SCHLEIFE ----------
    S("Vier Entführer.", "svg:fenster2", move="zoom_in", uhr="02:00"),
    S("Bewaffnet. Nervös.", "svg:fenster2", move="shake", uhr="02:00"),
    S("Ihr Ultimatum läuft *heute Nacht* ab.", "boden_tief", [fig("du_seitenblick.svg", MITTE)], bgfilter=UNSCHARF, uhr="02:00"),
    S("Und das Verrückte:", "boden_tief", [fig("du_neutral.svg", NAH)], bgfilter=UNSCHARF, uhr="02:00"),
    S("Fünf Jahre vorher gab es deine Einheit noch *nicht*.", "svg:tv_rauschen", move="zoom_in", sfx="static"),
    S("Dann knackt dein *Funk*.", "boden_tief", [fig("hand_funk.svg", dict(x=0, y=0, w=1080))], bgfilter=UNSCHARF,
      move="shake", uhr="02:00", sfx="funk"),
    # ---------- 5 BEFEHLE ----------
    S("Deine Befehle sind einfach.", "boden_tief", [fig("truppfuehrer_entschlossen_zeigen.svg", LINKS)], bgfilter=UNSCHARF,
      regeln=0),
    S("Kein Laut bis zum Signal.", "boden_tief", [fig("du_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, regeln=1),
    S("Alle Türen *gleichzeitig*.", "boden_tief", [fig("kollege_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, regeln=2),
    S("Geiseln zuerst.", "kabine_dunkel", bgfilter="brightness(.7)", regeln=3),
    S("Und: Es gibt *keinen* zweiten Versuch.", "boden_tief", [fig("truppfuehrer_entschlossen.svg", NAH)],
      bgfilter=UNSCHARF, move="zoom_schnell", regeln=4, sfx="impact"),
    # ---------- 6 ANNÄHERUNG ----------
    S("Zwei Uhr eins.", "drohne", move="zoom_in", uhr="02:01", sfx="tick"),
    S("Ihr kriecht los.", "boden_tief", [fig("du_entschlossen.svg", TIEF)], move="pan_r", uhr="02:01"),
    S("Die Leitern sind mit Gummi umwickelt.", "boden_tief", [fig("hand_leiter.svg", dict(x=0, y=0, w=1080))],
      bgfilter="blur(6px) brightness(.5)", move="pan_hoch", uhr="02:01"),
    S("Kein Klirren.", "boden_tief", [fig("hand_leiter.svg", dict(x=0, y=0, w=1080))], bgfilter="blur(6px) brightness(.5)",
      move="zoom_in", uhr="02:02"),
    S("Du hörst nur deinen eigenen *Atem*.", "boden_tief", [fig("du_angst.svg", NAH)], bgfilter=UNSCHARF, uhr="02:02",
      sfx="atem"),
    S("Zwei Uhr drei.", "leiter", move="zoom_in", uhr="02:03", sfx="tick"),
    S("Die Leiter steht an der Tragfläche.", "leiter", move="pan_hoch", uhr="02:03"),
    S("Über dir: ein Notausstieg.", "leiter", move="zoom_schnell", uhr="02:03"),
    S("Dahinter: *Stimmen*.", "svg:fenster1", move="zoom_in", uhr="02:03", sfx="stimmen"),
    S("Zwei Uhr vier.", "nase_feuer", move="zoom_in", uhr="02:04", tint="rgba(0,0,40,.55)", sfx="tick"),
    S("Vorne, vor dem Cockpit,", "nase_feuer", move="pan_r", uhr="02:04", tint="rgba(0,0,40,.4)"),
    S("lodert plötzlich ein *Feuer*.", "nase_feuer", move="shake", uhr="02:04", blitz="orange", sfx="feuer"),
    S("Somalische Soldaten haben es gelegt.", "drohne_feuer", move="zoom_in", uhr="02:04"),
    S("Die Entführer rennen nach vorne.", "svg:fenster2", move="pan_r", uhr="02:04"),
    S("*Weg* von dir.", "svg:fenster2", move="zoom_schnell", uhr="02:04"),
    S("Zwei Uhr fünf.", "boden_feuer", move="zoom_in", uhr="02:05", sfx="tick"),
    S("Dein Truppführer nickt.", "boden_feuer", [fig("truppfuehrer_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, uhr="02:05"),
    S("*Jetzt*.", "boden_feuer", [fig("du_schreien.svg", NAH)], bgfilter=UNSCHARF, move="shake_stark", uhr="02:05",
      blitz=True, sfx="impact"),
    # ---------- 7 ZUGRIFF ----------
    S("Die Notausstiege fliegen auf.", "kabine_ausstieg", move="shake_stark", uhr="02:05", blitz=True, sfx="tuer"),
    S("Überall gleichzeitig.", "kabine_zugriff", move="shake", uhr="02:06"),
    S("Du bist drin.", "kabine_zugriff", move="zoom_schnell", uhr="02:06"),
    S("Dunkel. Hitze.", "kabine_reihe", move="shake", uhr="02:06", tint="rgba(255,90,20,.18)"),
    S("Ein Gang voller Köpfe.", "kabine_zugriff", move="zoom_in", uhr="02:07"),
    S("„*Köpfe runter!*“", "kabine_zugriff", [fig("du_schreien.svg", NAH)], bgfilter=UNSCHARF, move="shake_stark", uhr="02:07",
      sfx="schrei"),
    S("*Schüsse*.", "kabine_zugriff", move="shake_stark", uhr="02:07", blitz=True, sfx="schuesse"),
    S("Von vorne.", "kabine_zugriff", move="shake", uhr="02:08", tint="rgba(255,255,255,.08)"),
    S("Neben dir geht ein Kollege zu Boden.", "kabine_reihe", [fig("kollege_angst.svg", MITTE)], bgfilter=UNSCHARF,
      move="shake", uhr="02:08"),
    S("*Getroffen*.", "kabine_reihe", [fig("kollege_angst.svg", NAH)], bgfilter=UNSCHARF, move="statisch",
      tint="rgba(200,0,0,.35)", uhr="02:08", sfx="impact"),
    S("Du gehst weiter.", "kabine_zugriff", [fig("du_entschlossen.svg", MITTE)], bgfilter=UNSCHARF, uhr="02:09"),
    S("Reihe für Reihe.", "kabine_zugriff", move="zoom_schnell", uhr="02:10"),
    S("_Sieben_ Minuten.", "kabine_zugriff", move="zoom_in", uhr="02:12", sfx="tick"),
    # ---------- 8 FALSCHE ERLÖSUNG ----------
    S("Dann: Stille.", "kabine_dunkel", move="statisch", bgfilter="grayscale(.6) brightness(.6)", uhr="02:12", pause=0.6,
      stille=True),
    S("Die Notrutschen gehen auf.", "rutsche", move="zoom_in", uhr="02:12", sfx="whoosh"),
    S("Menschen rennen barfuß über die Rollbahn.", "rutsche",
      [fig("zivil_m_angst_ganz.svg", dict(x=40, y=760, w=330)), fig("zivil_f_angst_ganz.svg", dict(x=380, y=800, w=310)),
       fig("zivil_k_angst_ganz.svg", dict(x=700, y=780, w=320))], move="pan_r"),
    S("Dein Kollege lebt.", "rutsche", [fig("kollege_erleichtert.svg", MITTE)], bgfilter=UNSCHARF),
    S("Die Geiseln leben.", "drohne_ende", move="zoom_out"),
    S("_Alle_.", "rutsche", [fig("zivil_f_erleichtert_ganz.svg", dict(x=110, y=700, w=380)),
                             fig("zivil_m_erleichtert_ganz.svg", dict(x=560, y=680, w=400))], move="zoom_in"),
    S("Über Funk geht ein einziges Wort nach Deutschland:", "rutsche", [fig("hand_funk.svg", dict(x=0, y=0, w=1080))],
      bgfilter=UNSCHARF, sfx="funk"),
    S("„_Springtime_.“", "rutsche", [fig("truppfuehrer_erleichtert_funk.svg", NAH)], bgfilter=UNSCHARF),
    S("Du hast es geschafft.", "rutsche", [fig("du_erleichtert.svg", MITTE)], bgfilter="blur(10px) brightness(.75)"),
    # ---------- 9 TWIST ----------
    S("Drei Entführer sind *tot*.", "fenster", move="statisch", bgfilter="grayscale(.5) brightness(.6)", sfx="drone_hit"),
    S("Aber im hinteren Teil der Maschine", "kabine_dunkel", move="zoom_in", tint="rgba(150,0,0,.3)"),
    S("bewegt sich noch etwas.", "kabine_dunkel", move="zoom_schnell", tint="rgba(150,0,0,.4)", sfx="heartbeat"),
    S("Die Vierte *lebt*.", "rutsche", [fig("trage.svg", dict(x=0, y=0, w=1080))], bgfilter="blur(4px) brightness(.5)",
      move="zoom_in", tint="rgba(150,0,0,.25)", sfx="impact"),
    S("Schwer verletzt. Sie wird überleben.", "rutsche", [fig("trage.svg", dict(x=0, y=0, w=1080))],
      bgfilter="blur(4px) brightness(.5)", move="pan_l", tint="rgba(150,0,0,.25)"),
    S("Und Jahre später in Deutschland vor Gericht stehen.", "svg:gericht", move="zoom_in"),
    # ---------- 10 LOOP-ENDE ----------
    S("Erinnerst du dich?", "boden_tief", [fig("du_seitenblick.svg", NAH)], bgfilter=UNSCHARF),
    S("Fünf Jahre vorher gab es deine Einheit nicht.", "svg:tv_rauschen", move="zoom_in", sfx="static"),
    S("_München_, 1972.", "svg:tv_1972", sprich="München, neunzehnhundertzweiundsiebzig.", move="zoom_in", bgfilter="sepia(.4)"),
    S("Olympia. Geiselnahme.", "svg:tv_1972", move="zoom_schnell", bgfilter="sepia(.4)"),
    S("Der Befreiungsversuch *scheitert*.", "svg:tv_rauschen", move="shake", sfx="static"),
    S("Keine Geisel überlebt.", "svg:tv_rauschen", move="statisch", bgfilter="grayscale(1) brightness(.5)"),
    S("Danach schwor Deutschland: *Nie wieder*.", "intro_zelle:6", move="zoom_in", logo=True, sfx="impact"),
    S("_München_ hat sie erschaffen.", "intro_zelle:6", [fig("einheit_gsg9.svg", GANZ)], move="zoom_in",
      tint="rgba(255,60,60,.25)", ringe=True),
    S("_Mogadischu_ hat sie *unsterblich* gemacht.", "drohne_ende", move="zoom_out", sfx="drone_hit"),
    # ---------- 11 SERIEN-TEASER ----------
    S("Und morgen?", "intro", move="whip:6:12", logo=True, sfx="whoosh"),
    S("Holt dich eine *andere*.", "intro", move="whip:12:1", logo=True, sfx="alarm", ende_schwarz=True),
]
