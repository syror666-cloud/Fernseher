"""Folge 14 Eagle Claw 1980 (nur Deutsch) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
STIMME = "JH302OKVzGGJc47f08ex"
MODELL = "eleven_v3"  # lebendig, mit Regieanweisungen (regie="[whispers]" …), Tags nicht im Timing
STIMM_EINSTELLUNG = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True, "speed": 1.0}
# Titelkarte: Einheitenname laut, fast gerufen (eigene Aufnahme)
TITEL_MODELL = "eleven_v3"
TITEL_EINSTELLUNG = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.8, "use_speaker_boost": True, "speed": 1.0}
TITEL_PEGEL = 3.0  # dB über der normalen Erzählerlautstärke


def S(text, **extra):
    return dict(text=text, **extra)


SHOTS = [
    S("Eine dieser *Einheiten*"),
    S("holt dich heute Nacht."),
    S("Mal sehen,"),
    S("ob du *zurückkommst*."),
    S("", titel="*DELTA FORCE*", titel_sprich="[shouting] Delta Force!", pause=1.5),
    S("Acht Männer sterben heute Nacht. Und keiner durch den *Feind*.", regie="[tense] [quietly]"),
    S("Teheran, 1980. *52* Amerikaner. Seit fast sechs Monaten Geiseln.", sprich="Teheran, neunzehnhundertachtzig. Zweiundfünfzig Amerikaner. Seit fast sechs Monaten Geiseln."),
    S("Und euer größter Gegner ist: *Sand*."),
    S("Merk dir den Sand.", regie="[whispers]"),
    S("Du bist bei der Delta Force. Der Plan ist *riesig*."),
    S("Acht Hubschrauber starten von einem *Flugzeugträger*."),
    S("Transportflugzeuge fliegen zu einem Punkt in der Wüste: *Desert One*."),
    S("Dort tanken alle. Dann geht es nach *Teheran*."),
    S("Mindestens *sechs* Hubschrauber müssen ankommen. Sonst: Abbruch."),
    S("Dein Kommandant sagt:"),
    S("„Sechs Maschinen. Sonst fliegen wir *heim*.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Leise *landen*."),
    S("Niemand darf euch *sehen*."),
    S("Tanken, *weiter*."),
    S("Und: Holt alle *raus*."),
    S("Nacht. Ihr landet in der Wüste.", regie="[tense]"),
    S("Plötzlich: ein *Bus*. Voller Iraner."),
    S("Dann ein Tanklaster. Er wird beschossen und *explodiert*.", regie="[tense]"),
    S("Und die Hubschrauber? Ein Sandsturm hat sie *erwischt*."),
    S("Nur *fünf* sind einsatzbereit."),
    S("Einer zu wenig. Der Präsident bricht *ab*."),
    S("Beim Abflug rammt ein Hubschrauber ein *Flugzeug*."),
    S("Feuer. Acht Soldaten *sterben*.", regie="[somber]"),
    S("Ihr lasst die Hubschrauber in der Wüste *zurück*."),
    S("Kein Schuss auf den Feind. Keine Geisel *frei*."),
    S("Frei kommen sie erst nach *444* Tagen.", sprich="Frei kommen sie erst nach vierhundertvierundvierzig Tagen."),
    S("Am Tag, an dem ein neuer Präsident sein Amt *antritt*."),
    S("Mut oder *Größenwahn*?", regie="[serious]"),
    S("Was hättest *du* getan? Schreib’s in die *Kommentare*."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
