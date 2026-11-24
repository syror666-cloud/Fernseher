# Hörprüfung folge01_gsg9

## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)

| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |
|---|---|---|---|
| alarm | echt | an alarm siren (40%), a walkie talkie radio squelch beep (39%), electronic beeps (16%) | ✅ |
| atem | echt | a man breathing heavily (86%), a fast whoosh swoosh sound effect (8%), laughter (4%) | ✅ |
| drone_hit | echt | a deep dark cinematic drone hit (80%), a deep cinematic impact boom (13%), a fast whoosh swoosh sound effect (3%) | ✅ |
| feuer | echt | fire igniting and burning (96%), a deep cinematic impact boom (3%), a car engine (0%) | ✅ |
| funk | echt | a walkie talkie radio squelch beep (91%), electronic beeps (4%), applause (2%) | ✅ |
| heartbeat | echt | a heartbeat (80%), a fast whoosh swoosh sound effect (5%), a ticking clock (4%) | ✅ |
| impact | echt | a deep cinematic impact boom (81%), fire igniting and burning (16%), a fast whoosh swoosh sound effect (1%) | ✅ |
| schuesse | echt | gunshots (97%), a deep cinematic impact boom (1%), footsteps (1%) | ✅ |
| static | echt | rain (40%), applause (36%), a walkie talkie radio squelch beep (5%) | ❌ Platz 7 |
| stimmen | echt | laughter (51%), a man speaking (34%), a woman speaking (13%) | ❌ Platz 10 |
| tick | echt | a ticking clock (97%), a heartbeat (2%), rain (1%) | ✅ |
| tuer | echt | a heavy door slamming (79%), a deep cinematic impact boom (19%), a fast whoosh swoosh sound effect (0%) | ✅ |
| whoosh | echt | a fast whoosh swoosh sound effect (100%), a deep cinematic impact boom (0%), a walkie talkie radio squelch beep (0%) | ✅ |
| atmo_nacht | echt | music (54%), rain (19%), quiet night ambience with wind and crickets (18%) | ✅ |

## C) Pegel je Einstellung (Stimme vs. Hintergrund)

87 Einstellungen geprüft, 24 mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).

## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)

Übereinstimmung Skript ↔ Gehörtes: **94%** (gut ab ~85 %).

## E) Lautheit
Integriert: -16.0 LUFS (Ziel −14 … −16), True Peak: -1.1 dBFS

## Ergebnis
- Geräusch 'static' (echt) klingt nicht wie 'radio static noise' (Platz 7)
- Geräusch 'stimmen' (echt) klingt nicht wie 'muffled human voices' (Platz 10)
- Einstellung 15 ('Den Kapitän haben sie schon *e'): Stimme nur 3.2 dB über Hintergrund, Geräuschspitze 13.9 dB über Stimme
- Einstellung 18 ('laufen wir.“'): Stimme nur 0.2 dB über Hintergrund, Geräuschspitze 15.6 dB über Stimme
- Einstellung 19 ('Vier Entführer.'): Stimme nur 4.4 dB über Hintergrund, Geräuschspitze 13.1 dB über Stimme
- Einstellung 23 ('Fünf Jahre vorher gab es deine'): Stimme nur 9.3 dB über Hintergrund, Geräuschspitze 8.0 dB über Stimme
- Einstellung 24 ('Dann knackt dein *Funk*.'): Stimme nur 7.8 dB über Hintergrund, Geräuschspitze 15.0 dB über Stimme
- Einstellung 29 ('Und: Es gibt *keinen* zweiten '): Stimme nur -0.5 dB über Hintergrund, Geräuschspitze 14.7 dB über Stimme
- Einstellung 35 ('Zwei Uhr drei.'): Stimme nur 11.3 dB über Hintergrund, Geräuschspitze 7.0 dB über Stimme
- Einstellung 38 ('Dahinter: *Stimmen*.'): Stimme nur 8.0 dB über Hintergrund, Geräuschspitze 10.0 dB über Stimme
- Einstellung 47 ('*Jetzt*.'): Stimme nur -4.9 dB über Hintergrund, Geräuschspitze 13.9 dB über Stimme
- Einstellung 48 ('Die Notausstiege fliegen auf.'): Stimme nur 0.3 dB über Hintergrund, Geräuschspitze 22.1 dB über Stimme
- Einstellung 53 ('„*Köpfe runter!*“'): Stimme nur 9.0 dB über Hintergrund, Geräuschspitze 10.0 dB über Stimme
- Einstellung 54 ('*Schüsse*.'): Stimme nur 4.7 dB über Hintergrund, Geräuschspitze 9.2 dB über Stimme
- Einstellung 67 ('Über Funk geht ein einziges Wo'): Stimme nur 15.6 dB über Hintergrund, Geräuschspitze 12.1 dB über Stimme
- Einstellung 70 ('Drei Entführer sind *tot*.'): Stimme nur 1.0 dB über Hintergrund, Geräuschspitze 11.4 dB über Stimme
- Einstellung 72 ('bewegt sich noch etwas.'): Stimme nur -2.3 dB über Hintergrund, Geräuschspitze 19.3 dB über Stimme
- Einstellung 73 ('Die Vierte *lebt*.'): Stimme nur -0.0 dB über Hintergrund, Geräuschspitze 16.3 dB über Stimme
- Einstellung 74 ('Schwer verletzt. Sie wird über'): Stimme nur 5.6 dB über Hintergrund, Geräuschspitze 8.4 dB über Stimme
- Einstellung 76 ('Erinnerst du dich?'): Stimme nur 7.6 dB über Hintergrund
- Einstellung 77 ('Fünf Jahre vorher gab es deine'): Stimme nur 4.7 dB über Hintergrund, Geräuschspitze 10.9 dB über Stimme
- Einstellung 78 ('_München_, 1972.'): Stimme nur 3.6 dB über Hintergrund, Geräuschspitze 13.3 dB über Stimme
- Einstellung 80 ('Der Befreiungsversuch *scheite'): Stimme nur 6.5 dB über Hintergrund, Geräuschspitze 10.5 dB über Stimme
- Einstellung 82 ('Danach schwor Deutschland: *Ni'): Stimme nur 2.8 dB über Hintergrund, Geräuschspitze 13.5 dB über Stimme
- Einstellung 84 ('_Mogadischu_ hat sie *unsterbl'): Stimme nur 2.9 dB über Hintergrund, Geräuschspitze 15.8 dB über Stimme
- Einstellung 86 ('Holt dich eine *andere*.'): Stimme nur 8.1 dB über Hintergrund, Geräuschspitze 6.1 dB über Stimme
