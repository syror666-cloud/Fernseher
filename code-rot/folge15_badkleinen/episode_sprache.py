"""Folge 15 Bad Kleinen 1993 (nur Deutsch) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*GSG 9*", titel_sprich="[shouting] Ge-Es-Ge Neun!", pause=1.5),
    S("Heute stirbt dein Kollege. Und danach heißt es: *Ihr* seid die Mörder.", regie="[tense] [quietly]"),
    S("Ein kleiner Bahnhof in Mecklenburg. Zwei Terroristen der *RAF*."),
    S("Und am Ende bleibt eine Frage: Wer hat *geschossen*?"),
    S("Merk dir die Frage.", regie="[whispers]"),
    S("Ein Spitzel hat das Treffen *verraten*."),
    S("Wolfgang Grams und Birgit Hogefeld. Beide *gesucht*."),
    S("Du bist bei der GSG 9. Ihr wartet am *Tunnel*.", sprich="Du bist bei der Ge-Es-Ge Neun. Ihr wartet am Tunnel."),
    S("Dein Einsatzleiter sagt:"),
    S("„Erst auf fünf Meter. Dann *Zugriff*.“", stimme="chef"),
    S("Deine Befehle:"),
    S("Warte auf das *Signal*."),
    S("Fünf Meter *Abstand*."),
    S("Keine *Schüsse*."),
    S("Und: beide *lebend*."),
    S("Aber ein Funkspruch wird *falsch* verstanden."),
    S("Das Signal kommt zu *früh*. Ihr seid *15* Meter weg.", sprich="Das Signal kommt zu früh. Ihr seid fünfzehn Meter weg.", regie="[tense]"),
    S("Grams rennt auf den *Bahnsteig*. Und schießt.", regie="[tense]"),
    S("Dein Kollege Michael Newrzella wird *getroffen*. Er ist *25*.", sprich="Dein Kollege Michael Newrzella wird getroffen. Er ist fünfundzwanzig."),
    S("Er stirbt am *Abend*.", regie="[somber]"),
    S("Grams fällt auf die *Gleise*. Kopfschuss."),
    S("Hogefeld wird im Tunnel *festgenommen*."),
    S("Dann sagt eine Zeugin: Grams wurde *hingerichtet*."),
    S("Der Spiegel schreibt dasselbe. Der Innenminister tritt *zurück*."),
    S("Aber die Ermittler sagen: Er hat sich selbst *erschossen*."),
    S("Ein Gutachten aus Zürich bestätigt das."),
    S("Nur: Spuren wurden *abgewaschen*. Die tödliche Kugel? Nie *gefunden*."),
    S("Später zweifelt sogar der Spiegel an seiner eigenen *Quelle*."),
    S("Selbstmord oder *Hinrichtung*?", regie="[serious]"),
    S("Was glaubst *du*? Schreib’s in die *Kommentare*."),
    S("Und morgen?"),
    S("Holt dich eine *andere*."),
]
