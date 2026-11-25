"""Folge 8 Lima (Chavín de Huántar) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*CHAVÍN*", titel_sprich="Tschawín.", pause=1.5),
    S("Du bist Kommandosoldat in *Peru*."),
    S("*14* Rebellen. *72* Geiseln.", sprich="Vierzehn Rebellen. Zweiundsiebzig Geiseln."),
    S("Seit vier Monaten halten sie diese Villa."),
    S("Und jeden Nachmittag machen sie *denselben* Fehler."),
    S("Merk dir das."),
    S("Es begann auf einer *Party*."),
    S("Beim japanischen Botschafter."),
    S("Sie kamen in einem *Krankenwagen*."),
    S("Und sprengten sich durch die *Mauer*."),
    S("Ihr könnt nicht durch die Tür."),
    S("Also holt ihr *Bergleute*."),
    S("Sie graben *Tunnel* bis unter das Haus."),
    S("Am Morgen dröhnt *Marschmusik*."),
    S("Damit keiner etwas *merkt*."),
    S("Ihr baut das Haus *nach* und probt."),
    S("Versteckte *Mikrofone* hören mit."),
    S("Dein Kommandant sagt nur:"),
    S("„Wir warten auf den *Ball*.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Kein *Geräusch*."),
    S("*72* Leben.", sprich="Zweiundsiebzig Leben."),
    S("Alle Tunnel *zugleich*."),
    S("Und: Warte auf das *Signal*."),
    S("Tag *126*.", sprich="Tag einhundertsechsundzwanzig."),
    S("*15:23*.", sprich="Fünfzehn Uhr dreiundzwanzig."),
    S("Ihr liegt im *Tunnel*."),
    S("Über euch: *Schritte*. Rufe."),
    S("„*Jetzt!*“", stimme="funk"),
    S("Der Boden *explodiert*."),
    S("Ihr kommt von *unten*."),
    S("*148* Soldaten.", sprich="Einhundertachtundvierzig Soldaten."),
    S("Rauch. *Schüsse*."),
    S("Die Geiseln kriechen ins Freie."),
    S("Ein Offizier wirft sich vor einen *Minister*."),
    S("Der Offizier *stirbt*."),
    S("*71* Geiseln überleben.", sprich="Einundsiebzig Geiseln überleben."),
    S("Du hast es geschafft."),
    S("Und der *Fehler*?"),
    S("Jeden Nachmittag spielten sie drinnen *Fußball*."),
    S("Genau über eurem *Tunnel*."),
    S("Ihr habt nur auf den *Anpfiff* gewartet."),
    S("Bis heute wird gestritten,"),
    S("ob sich *einige* schon ergeben hatten."),
    S("Der Name des Einsatzes: ein Tempel voller *Gänge*."),
    S("*Chavín de Huántar*.", sprich="Tschawín de Wántar."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
