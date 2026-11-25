# Hörprüfung folge01_gsg9

## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)

| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |
|---|---|---|---|
| alarm | echt | an alarm siren (40%), a walkie talkie radio squelch beep (39%), electronic beeps (16%) | ✅ |
| atem | echt | a man breathing heavily (85%), a fast whoosh swoosh sound effect (8%), laughter (4%) | ✅ |
| drone_hit | echt | a deep dark cinematic drone hit (80%), a deep cinematic impact boom (13%), a fast whoosh swoosh sound effect (3%) | ✅ |
| feuer | echt | fire igniting and burning (96%), a deep cinematic impact boom (3%), a car engine (0%) | ✅ |
| funk | echt | a walkie talkie radio squelch beep (91%), electronic beeps (4%), applause (2%) | ✅ |
| heartbeat | echt | a heartbeat (80%), a fast whoosh swoosh sound effect (5%), a ticking clock (4%) | ✅ |
| impact | echt | a deep cinematic impact boom (81%), fire igniting and burning (16%), a fast whoosh swoosh sound effect (1%) | ✅ |
| schuesse | echt | gunshots (97%), a deep cinematic impact boom (1%), footsteps (1%) | ✅ |
| static | echt | white noise static hiss (91%), rain (4%), applause (3%) | ✅ |
| stimmen | synthetisch | a fast whoosh swoosh sound effect (99%), a ticking clock (0%), a deep cinematic impact boom (0%) | ❌ Platz 17 |
| tick | echt | a ticking clock (97%), a heartbeat (2%), rain (1%) | ✅ |
| tuer | echt | a heavy door slamming (79%), a deep cinematic impact boom (19%), a fast whoosh swoosh sound effect (0%) | ✅ |
| whoosh | echt | a fast whoosh swoosh sound effect (100%), a deep cinematic impact boom (0%), a walkie talkie radio squelch beep (0%) | ✅ |
| atmo_nacht | echt | music (49%), rain (17%), quiet night ambience with wind and crickets (17%) | ✅ |

## C) Pegel je Einstellung (Stimme vs. Hintergrund)

87 Einstellungen geprüft, 11 mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).

## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)

Übereinstimmung Skript ↔ Gehörtes: **94%** (gut ab ~85 %).

## E) Lautheit
Integriert: -15.2 LUFS (Ziel −14 … −16), True Peak: -1.3 dBFS

## Ergebnis
- Geräusch 'stimmen' (synthetisch) klingt nicht wie 'people talking indistinctly' (Platz 17)
- Einstellung 18 ('laufen wir.“'): Stimme nur 8.0 dB über Hintergrund
- Einstellung 24 ('Dann knackt dein *Funk*.'): Stimme nur 11.5 dB über Hintergrund, Geräuschspitze 12.4 dB über Stimme
- Einstellung 29 ('Und: Es gibt *keinen* zweiten '): Stimme nur 5.9 dB über Hintergrund
- Einstellung 47 ('*Jetzt*.'): Stimme nur 4.5 dB über Hintergrund
- Einstellung 48 ('Die Notausstiege fliegen auf.'): Stimme nur 7.7 dB über Hintergrund, Geräuschspitze 15.1 dB über Stimme
- Einstellung 70 ('Drei Entführer sind *tot*.'): Stimme nur 6.7 dB über Hintergrund
- Einstellung 72 ('bewegt sich noch etwas.'): Stimme nur 4.2 dB über Hintergrund
- Einstellung 74 ('Schwer verletzt. Sie wird über'): Stimme nur 5.6 dB über Hintergrund
- Einstellung 76 ('Erinnerst du dich?'): Stimme nur 7.6 dB über Hintergrund
- Einstellung 77 ('Fünf Jahre vorher gab es deine'): Stimme nur 5.9 dB über Hintergrund
- Einstellung 78 ('_München_, 1972.'): Stimme nur 4.2 dB über Hintergrund
