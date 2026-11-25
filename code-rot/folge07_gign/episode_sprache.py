"""Folge 7 GIGN – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
STIMME = "JH302OKVzGGJc47f08ex"
MODELL = "eleven_multilingual_v2"
STIMM_EINSTELLUNG = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 1.15}


def S(text, **extra):
    return dict(text=text, **extra)


SHOTS = [
    S("Eine dieser *Einheiten*"),
    S("holt dich heute Nacht."),
    S("Mal sehen,"),
    S("ob du *zurückkommst*."),
    S("", titel="*GIGN*", titel_sprich="G. I. G. N.", pause=1.5),
    S("Du bist bei der *GIGN*.", sprich="Du bist bei der Ge I Ge En."),
    S("Vier Entführer. Ein *Airbus* voller Menschen."),
    S("Sie wollen nach *Paris*."),
    S("Und fordern *27 Tonnen* Treibstoff.", sprich="Und fordern siebenundzwanzig Tonnen Treibstoff."),
    S("Merk dir die Zahl."),
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
    S("*17:12*.", sprich="Siebzehn Uhr zwölf."),
    S("Die Treppen rollen los."),
    S("Deine steht zu *hoch*."),
    S("Die Tür geht *nicht* auf."),
    S("Zurück. Und noch mal ran."),
    S("Dann seid ihr *drin*."),
    S("Schüsse aus dem *Cockpit*."),
    S("Über *tausend* Schuss."),
    S("Eine *Granate* fliegt."),
    S("Der Copilot springt aus dem *Fenster*."),
    S("Hinten rutschen die Geiseln ins Freie."),
    S("Der letzte Entführer fällt."),
    S("*Kein* Passagier stirbt beim Sturm."),
    S("Du hast es geschafft."),
    S("Aber erinnerst du dich an die *27 Tonnen*?", sprich="Aber erinnerst du dich an die siebenundzwanzig Tonnen?"),
    S("Bis Paris hätten rund *acht* gereicht."),
    S("Wozu der *Rest*?"),
    S("Die Ermittler hatten einen *Verdacht*."),
    S("Das Flugzeug sollte selbst die *Bombe* sein."),
    S("Über Paris. Vielleicht am *Eiffelturm*."),
    S("Fast *sieben* Jahre vor dem 11. September.", sprich="Fast sieben Jahre vor dem elften September."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
