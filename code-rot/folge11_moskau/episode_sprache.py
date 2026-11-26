"""Folge 11 Moskau 2002 (Nord-Ost) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*ALPHA*", titel_sprich="[shouting] Alpha!", pause=1.5),
    S("Du bist bei der *Alpha*-Gruppe."),
    S("Moskau, Oktober 2002.", sprich="Moskau, Oktober zweitausendzwei."),
    S("Ein voller *Theatersaal*. Ein Musical."),
    S("Plötzlich stürmen Bewaffnete die *Bühne*."),
    S("Über *850* Geiseln.", sprich="Über achthundertfünfzig Geiseln."),
    S("Rund *40* Angreifer. Sprengstoff am *Körper*.", sprich="Rund vierzig Angreifer. Sprengstoff am Körper."),
    S("Wenn ihr stürmt, sprengen sie *alles*."),
    S("Wie rettest du *850* Menschen auf einmal?", sprich="Wie rettest du achthundertfünfzig Menschen auf einmal?"),
    S("Merk dir die Frage.", regie="[whispers]"),
    S("Fast drei Tage wird verhandelt."),
    S("Die Forderung: Russland soll aus *Tschetschenien* abziehen."),
    S("Dann kommt der *Befehl*."),
    S("Nicht durch die Tür. Durch die *Lüftung*."),
    S("Dein Kommandant sagt:"),
    S("„Erst das Gas. Dann *ihr*.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Gasmaske *auf*."),
    S("Keiner darf *zünden*."),
    S("Rein, sobald es *still* ist."),
    S("Und: Holt sie alle *raus*."),
    S("26. Oktober. Früher Morgen.", sprich="Sechsundzwanzigster Oktober. Früher Morgen."),
    S("Ein Gas strömt in den *Saal*.", regie="[whispers]"),
    S("Die Menschen schlafen *ein*."),
    S("Auch die Angreifer."),
    S("Ihr stürmt.", regie="[tense]"),
    S("Alle Angreifer sterben."),
    S("Zuerst heißt es: *keine* Geisel tot."),
    S("Du hast es geschafft."),
    S("Aber draußen …"),
    S("Menschen liegen in Reihen auf dem *Bürgersteig*."),
    S("Die Ärzte erwarten Opfer von Schüssen und *Bomben*."),
    S("Nicht von einem geheimen *Gas*."),
    S("Ein Gegenmittel hätte helfen können. Sofort *gegeben*."),
    S("*73* Geiseln bekommen gar keine Hilfe.", sprich="Dreiundsiebzig Geiseln bekommen gar keine Hilfe.", regie="[somber]"),
    S("Am Ende sterben rund *130* Geiseln.", sprich="Am Ende sterben rund hundertdreißig Geiseln.", regie="[somber]"),
    S("Fast keiner durch eine *Kugel*."),
    S("Sondern durch das *Gas*."),
    S("Welches Gas genau? Russland hat es nie ganz *offengelegt*."),
    S("Ein Gericht in Straßburg urteilt: Die Rettung war schlecht *geplant*."),
    S("Über *700* gerettet. Rund *130* tot.", sprich="Über siebenhundert gerettet. Rund hundertdreißig tot.", regie="[somber]"),
    S("Rettung oder *Katastrophe*?", regie="[serious]"),
    S("Was hättest *du* getan? Schreib’s in die *Kommentare*."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
