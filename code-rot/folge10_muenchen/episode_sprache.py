"""Folge 10 München 1972 – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*POLIZEI*", titel_sprich="[shouting] Polizei!", pause=1.5),
    S("Du bist Polizist in *München*."),
    S("Olympische Spiele, *1972*.", sprich="Olympische Spiele, neunzehnhundertzweiundsiebzig."),
    S("Acht Terroristen stürmen das Quartier der *Israelis*."),
    S("Zwei aus dem Team werden *getötet*.", regie="[somber]"),
    S("*Neun* werden Geiseln."),
    S("Und Deutschland hat *keine* Spezialeinheit."),
    S("Wie rettest du neun Menschen, ohne *Training*?"),
    S("Merk dir die Frage.", regie="[whispers]"),
    S("Ihr klettert auf die *Dächer*."),
    S("Verkleidet in *Trainingsanzügen*."),
    S("Aber das Fernsehen überträgt *live*."),
    S("Und die Terroristen schauen *zu*."),
    S("Der Einsatz wird *abgebrochen*."),
    S("Neuer Plan: ein *Flugplatz*."),
    S("Zwei Hubschrauber bringen alle nach *Fürstenfeldbruck*."),
    S("Dort wartet ein Flugzeug."),
    S("Darin: Polizisten, als *Crew* verkleidet."),
    S("Dein Einsatzleiter sagt:"),
    S("„Sobald sie im Flugzeug sind, *schlagen* wir zu.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Warte auf das *Signal*."),
    S("Schieß nur auf *Täter*."),
    S("Triff keine *Geisel*."),
    S("Und: alle *neun* lebend."),
    S("Aber im Flugzeug stimmen die Polizisten *ab*."),
    S("Sie *gehen*. Einfach so."),
    S("Das Flugzeug ist *leer*."),
    S("Jetzt seid nur noch ihr da. *Fünf* Schützen."),
    S("Kein Zielfernrohr. Kein *Nachtsichtgerät*."),
    S("Ihr glaubt, es sind fünf Täter. Es sind *acht*."),
    S("Die Hubschrauber landen.", regie="[tense]"),
    S("Zwei Terroristen prüfen das Flugzeug."),
    S("*Leer*. Sie rennen zurück."),
    S("Dann fallen die ersten *Schüsse*.", regie="[tense]"),
    S("Die Panzerwagen? Stecken im *Stau*."),
    S("Kurz vor Mitternacht meldet die Regierung: *Erfolg*."),
    S("Doch *keine* Geisel überlebt.", regie="[somber]"),
    S("Und es wird noch schlimmer."),
    S("Drei Terroristen überleben."),
    S("Weniger als zwei Monate später wird ein Flugzeug *entführt*."),
    S("Die Forderung: die *drei* freilassen."),
    S("Und Deutschland lässt sie *gehen*."),
    S("Danach gründet Deutschland die *GSG 9*.", sprich="Danach gründet Deutschland die Ge Es Ge Neun."),
    S("Aber hätte man es verhindern *können*?", regie="[serious]"),
    S("Versagen oder Pech? Schreib’s in die *Kommentare*."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
