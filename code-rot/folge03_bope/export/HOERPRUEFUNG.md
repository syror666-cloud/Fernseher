# Hörprüfung folge03_bope

## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)

| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |
|---|---|---|---|
| alarm | echt | an alarm siren (40%), a walkie talkie radio squelch beep (39%), electronic beeps (16%) | ✅ |
| atem | echt | a man breathing heavily (85%), a fast whoosh swoosh sound effect (8%), laughter (4%) | ✅ |
| drone_hit | echt | a deep dark cinematic drone hit (80%), a deep cinematic impact boom (13%), a fast whoosh swoosh sound effect (3%) | ✅ |
| feuerwerk | echt | fireworks exploding (100%), a crowd cheering (0%), footsteps (0%) | ✅ |
| heartbeat | echt | a heartbeat (80%), a fast whoosh swoosh sound effect (5%), a ticking clock (4%) | ✅ |
| impact | echt | a deep cinematic impact boom (81%), fire igniting and burning (16%), a fast whoosh swoosh sound effect (1%) | ✅ |
| static | echt | white noise static hiss (91%), rain (4%), applause (3%) | ✅ |
| tick | echt | a ticking clock (97%), a heartbeat (2%), rain (1%) | ✅ |
| tuer | echt | a heavy door slamming (79%), a deep cinematic impact boom (19%), a fast whoosh swoosh sound effect (0%) | ✅ |
| whoosh | echt | a fast whoosh swoosh sound effect (100%), a deep cinematic impact boom (0%), a walkie talkie radio squelch beep (0%) | ✅ |
| atmo_stadt | echt | a car engine (41%), city at night ambience with distant dogs and traffic (28%), rain (18%) | ✅ |

## C) Pegel je Einstellung (Stimme vs. Hintergrund)

69 Einstellungen geprüft, 6 mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).

## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)

Übereinstimmung Skript ↔ Gehörtes: **95%** (gut ab ~85 %).

## E) Lautheit
Integriert: -15.5 LUFS (Ziel −14 … −16), True Peak: -1.3 dBFS

## Ergebnis
- Einstellung 27 ('Sie *wissen* es.'): Stimme nur 7.9 dB über Hintergrund
- Einstellung 32 ('Und: *Niemand* bleibt zurück.'): Stimme nur 6.0 dB über Hintergrund
- Einstellung 34 ('Ihr steigt aus.'): Stimme nur 4.4 dB über Hintergrund, Geräuschspitze 15.3 dB über Stimme
- Einstellung 43 ('Drei. Zwei. Eins.'): Stimme nur 6.0 dB über Hintergrund, Geräuschspitze 13.7 dB über Stimme
- Einstellung 44 ('Die Tür fliegt auf.'): Stimme nur 6.7 dB über Hintergrund, Geräuschspitze 14.2 dB über Stimme
- Einstellung 63 ('Er ist _zwölf_.'): Stimme nur 7.9 dB über Hintergrund
