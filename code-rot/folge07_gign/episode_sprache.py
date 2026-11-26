"""Folge 7 GIGN – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
STIMME = "JH302OKVzGGJc47f08ex"
MODELL = "eleven_v3"  # lebendiger, mit Regieanweisungen (regie="[whispers]" …), Tags nicht im Timing
STIMM_EINSTELLUNG = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True, "speed": 1.2}  # v3 spricht Deutsch sonst sehr langsam
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
    S("", titel="*GIGN*", titel_sprich="[shouting] Gé! I! Gé! Enn!", pause=1.5),
    S("Du bist bei der *GIGN*.", sprich="Du bist bei der Ge I Ge En.", regie="[excited]"),
    S("Vier Entführer. Ein *Airbus* voller Menschen."),
    S("Sie wollen nach *Paris*."),
    S("Und fordern *27 Tonnen* Treibstoff.", sprich="Und fordern siebenundzwanzig Tonnen Treibstoff."),
    S("Merk dir die Zahl.", regie="[whispers]"),
    S("An Heiligabend kapern sie die Maschine in *Algier*."),
    S("Verkleidet als *Polizisten*."),
    S("*Drei* Geiseln sind schon tot."),
    S("An Bord: *Dynamit*."),
    S("Ihr übt an einer *baugleichen* Maschine."),
    S("Dann landet sie in *Marseille*."),
    S("Der Tank ist fast leer."),
    S("Und *niemand* bringt ihnen Sprit."),
    S("Dein Kommandant sagt nur:"),
    S("„Diese Maschine startet *nicht* mehr.“", stimme="chef"),
    S("Deine Befehle:"),
    S("*Drei* Treppen."),
    S("Drei Türen *zugleich*."),
    S("Vorsicht, *Dynamit*."),
    S("Und: *Passagiere* raus."),
    S("*17:12*.", sprich="Siebzehn Uhr zwölf.", regie="[tense]"),
    S("Die Treppen rollen los."),
    S("Deine steht zu *hoch*."),
    S("Die Tür geht *nicht* auf."),
    S("Zurück. Und noch mal ran."),
    S("Dann seid ihr *drin*."),
    S("Schüsse aus dem *Cockpit*.", regie="[excited]"),
    S("Über *tausend* Schuss."),
    S("Eine *Granate* fliegt."),
    S("Der Copilot springt aus dem *Fenster*."),
    S("Hinten rutschen die Geiseln ins Freie."),
    S("Der letzte Entführer fällt."),
    S("*Kein* Passagier stirbt beim Sturm."),
    S("Du hast es geschafft.", regie="[relieved]"),
    S("Aber erinnerst du dich an die *27 Tonnen*?", sprich="Aber erinnerst du dich an die siebenundzwanzig Tonnen?", regie="[whispers]"),
    S("Bis Paris hätten rund *acht* gereicht."),
    S("Wozu der *Rest*?"),
    S("Die Ermittler hatten einen *Verdacht*."),
    S("Das Flugzeug sollte selbst die *Bombe* sein.", regie="[tense]"),
    S("Über Paris. Vielleicht am *Eiffelturm*."),
    S("Fast *sieben* Jahre vor dem 11. September.", sprich="Fast sieben Jahre vor dem elften September."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
