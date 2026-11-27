"""Folge 13 Gladbeck 1988 (nur Deutsch) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*SEK*", titel_sprich="[shouting] Ess-Ee-Kaa!", pause=1.5),
    S("Du stehst zwei Meter neben den Geiselnehmern. Und darfst *nichts* tun.", regie="[tense] [quietly]"),
    S("Zwei Bankräuber. Geiseln im Auto. *54* Stunden auf der Flucht.", sprich="Zwei Bankräuber. Geiseln im Auto. Vierundfünfzig Stunden auf der Flucht."),
    S("Und das Verrückteste: Die Reporter sind *näher* dran als du."),
    S("Merk dir die Reporter.", regie="[whispers]"),
    S("Es beginnt in einer Bank in *Gladbeck*."),
    S("Die Täter verlangen Geld und ein *Fluchtauto*. Sie bekommen beides."),
    S("In Bremen kapern sie einen *Bus*. Mit *32* Menschen.", sprich="In Bremen kapern sie einen Bus. Mit zweiunddreißig Menschen."),
    S("Ein *14*-jähriger Junge schützt seine Schwester.", sprich="Ein vierzehnjähriger Junge schützt seine Schwester."),
    S("Er wird *erschossen*.", regie="[somber]"),
    S("Am nächsten Tag: Köln, *Fußgängerzone*."),
    S("Reporter umringen das Auto. Sie machen *Interviews*. Mit den Tätern."),
    S("Ein Reporter steigt sogar *ein*. Und zeigt ihnen den Weg."),
    S("Du bist beim SEK. Ihr seid direkt *daneben*.", sprich="Du bist beim Ess-Ee-Kaa. Ihr seid direkt daneben."),
    S("Dein Einsatzleiter sagt:"),
    S("„Ihr geht nur *ohne* Waffen ran.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Nicht *auffallen*."),
    S("Keine *Waffen*."),
    S("Keine Geisel *gefährden*."),
    S("Und: Wartet auf die *Autobahn*."),
    S("Ihr brecht *ab*. Die Täter fahren weiter."),
    S("Autobahn A3. Ein gepanzerter Wagen *rammt* das Fluchtauto.", sprich="Autobahn A drei. Ein gepanzerter Wagen rammt das Fluchtauto.", regie="[tense]"),
    S("Es fallen *62* Schüsse.", sprich="Es fallen zweiundsechzig Schüsse."),
    S("Die Täter geben auf."),
    S("Aber die Geisel Silke, *18*, ist tot.", sprich="Aber die Geisel Silke, achtzehn, ist tot.", regie="[somber]"),
    S("Die Kugel kam aus der Waffe des *Täters*."),
    S("*54* Stunden. *Drei* Tote.", sprich="Vierundfünfzig Stunden. Drei Tote.", regie="[somber]"),
    S("Bremens Innensenator tritt *zurück*."),
    S("Wer hat versagt: Polizei oder *Presse*?", regie="[serious]"),
    S("Schreib’s in die *Kommentare*."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
