"""Folge 12 Entebbe 1976 (nur Deutsch) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*SAYERET MATKAL*", titel_sprich="[shouting] Sayeret Matkal!", pause=1.5),
    S("Ein Fehler von *dir*, und *106* Menschen sterben.", sprich="Ein Fehler von dir, und hundertsechs Menschen sterben.", regie="[tense] [quietly]"),
    S("Sie sitzen mitten in Afrika. Bewacht von Terroristen und einer ganzen *Armee*.", regie="[tense]"),
    S("Du bist *4.000* Kilometer entfernt.", sprich="Du bist viertausend Kilometer entfernt."),
    S("Und alles hängt an einem Auto in der falschen *Farbe*."),
    S("Merk dir das Auto.", regie="[whispers]"),
    S("Eine Woche vorher: ein Flug von Tel Aviv nach *Paris*."),
    S("Vier Entführer. Zwei davon sind *Deutsche*."),
    S("Sie landen in *Uganda*. Diktator Idi Amin hilft ihnen."),
    S("Dann trennen sie: Israelis auf eine Seite. Die meisten anderen dürfen *gehen*."),
    S("Die Forderung: *53* Gefangene frei. Sonst sterben Geiseln.", sprich="Die Forderung: dreiundfünfzig Gefangene frei. Sonst sterben Geiseln."),
    S("Euer Plan: vier Transportflugzeuge. Nachts. Im *Tiefflug*."),
    S("Vorneweg ein schwarzer *Mercedes*. Wie der des Diktators."),
    S("Dein Kommandant sagt:"),
    S("„Die Wachen halten uns für ihren *Präsidenten*.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Leise bis zum *Terminal*."),
    S("Schieß nur auf *Täter*."),
    S("Keine Geisel bleibt *zurück*."),
    S("Und: schnell wieder *weg*."),
    S("Kurz vor Mitternacht. Ihr landet.", regie="[tense]"),
    S("Zwei Wachen stoppen den *Mercedes*."),
    S("Denn ihr Präsident fährt seit kurzem einen *weißen*."),
    S("Schüsse. Die Tarnung ist *weg*.", regie="[tense]"),
    S("Ihr stürmt das *Terminal*.", regie="[tense]"),
    S("Alle Entführer sterben."),
    S("*102* Geiseln kommen frei.", sprich="Hundertzwei Geiseln kommen frei."),
    S("Aber euer Kommandant fällt: Yoni *Netanjahu*.", regie="[somber]"),
    S("Der Bruder von Benjamin *Netanjahu*."),
    S("Drei Geiseln sterben beim Sturm. Eine vierte wird danach *ermordet*.", regie="[somber]"),
    S("Uganda nennt es einen *Angriff*. Der UN-Sicherheitsrat streitet."),
    S("Rettung oder *Rechtsbruch*?"),
    S("Was hättest *du* getan? Schreib’s in die *Kommentare*.", regie="[serious]"),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
