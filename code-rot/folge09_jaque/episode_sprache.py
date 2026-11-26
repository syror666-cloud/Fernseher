"""Folge 9 Operation Jaque (Kolumbien 2008) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
STIMME = "JH302OKVzGGJc47f08ex"
MODELL = "eleven_v3"  # lebendig, mit Regieanweisungen (regie="[whispers]" …), Tags nicht im Timing
STIMM_EINSTELLUNG = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True, "speed": 1.0}
# Titelkarte: Einheitenname laut, fast gerufen (eigene Aufnahme)
TITEL_MODELL = "eleven_v3"
TITEL_EINSTELLUNG = {"stability": 0.0, "similarity_boost": 0.8, "style": 0.8, "use_speaker_boost": True, "speed": 1.0}
TITEL_PEGEL = 3.0  # dB über der normalen Erzählerlautstärke


def S(text, **extra):
    return dict(text=text, **extra)


SHOTS = [
    S("Eine dieser *Einheiten*"),
    S("holt dich heute Nacht."),
    S("Mal sehen,"),
    S("ob du *zurückkommst*."),
    S("", titel="*JAQUE*", titel_sprich="[shouting] Chake!", pause=1.5),
    S("Du bist Soldat in *Kolumbien*.", regie="[excited]"),
    S("*15* Geiseln im Dschungel.", sprich="Fünfzehn Geiseln im Dschungel."),
    S("Eine von ihnen seit über *sechs* Jahren."),
    S("Bewacht von rund *60* Rebellen.", sprich="Bewacht von rund sechzig Rebellen."),
    S("Wie holt man sie raus, ohne *einen* Schuss?"),
    S("Merk dir die Frage.", regie="[whispers]"),
    S("Ihr hört ihren *Funk* ab."),
    S("Ihr kennt ihre *Codes*."),
    S("Dann schickt ihr ihnen einen *Befehl*."),
    S("Angeblich von ihrem eigenen *Chef*."),
    S("„Bringt die Geiseln zu einer *Hilfsmission*.“", stimme="funk"),
    S("Die Hilfsmission seid *ihr*."),
    S("Ihr streicht zwei Hubschrauber *weiß*."),
    S("Ihr nehmt sogar *Schauspielunterricht*."),
    S("Dein Kommandant sagt nur:"),
    S("„Ein falsches Wort, und alle *sterben*.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Kein *Schuss*."),
    S("Bleib in deiner *Rolle*."),
    S("Keine Waffe *zeigen*."),
    S("Und: alle *15* an Bord.", sprich="Und: alle fünfzehn an Bord."),
    S("2. Juli 2008.", sprich="Zweiter Juli, zweitausendacht."),
    S("Zwei weiße Hubschrauber über dem *Dschungel*."),
    S("Ihr landet auf einer *Lichtung*.", regie="[tense]"),
    S("Um euch herum: *bewaffnete* Rebellen."),
    S("Die Geiseln kommen."),
    S("Ihr legt ihnen selbst *Handschellen* an."),
    S("Damit keiner *Verdacht* schöpft."),
    S("Der Anführer steigt *mit* ein."),
    S("Die Tür geht zu. Ihr startet."),
    S("Dann, in der Luft:", regie="[tense]"),
    S("Zwei Rebellen gehen *zu Boden*.", regie="[excited]"),
    S("„Wir sind die *Armee*. Ihr seid *frei*!“", stimme="jubel"),
    S("Die Geiseln *schreien*. Vor Glück."),
    S("*Kein* Schuss. *15* frei.", sprich="Kein Schuss. Fünfzehn frei."),
    S("Du hast es geschafft.", regie="[relieved]"),
    S("Aber einer von euch trug ein Zeichen, das er *nie* hätte tragen dürfen."),
    S("Das *Rote Kreuz*."),
    S("Im Krieg schützt es *Helfer*."),
    S("Wer es missbraucht, gefährdet *jeden* von ihnen."),
    S("Die Regierung musste sich *entschuldigen*."),
    S("Und der Name *Jaque*?", sprich="Und der Name Chake?", regie="[whispers]"),
    S("Das heißt *Schach*."),
    S("Ihr habt gewonnen, ohne eine einzige *Figur* zu schlagen."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
