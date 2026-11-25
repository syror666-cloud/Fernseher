# Hörprüfung folge04_bloque

## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)

| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |
|---|---|---|---|
| alarm | echt | an alarm siren (40%), a walkie talkie radio squelch beep (39%), electronic beeps (16%) | ✅ |
| drone_hit | echt | a deep dark cinematic drone hit (80%), a deep cinematic impact boom (13%), a fast whoosh swoosh sound effect (3%) | ✅ |
| funk | echt | a walkie talkie radio squelch beep (91%), electronic beeps (4%), applause (2%) | ✅ |
| heartbeat | echt | a heartbeat (80%), a fast whoosh swoosh sound effect (5%), a ticking clock (4%) | ✅ |
| impact | echt | a deep cinematic impact boom (81%), fire igniting and burning (16%), a fast whoosh swoosh sound effect (1%) | ✅ |
| schuesse | echt | gunshots (97%), a deep cinematic impact boom (1%), footsteps (1%) | ✅ |
| static | echt | white noise static hiss (91%), rain (4%), applause (3%) | ✅ |
| tick | echt | a ticking clock (97%), a heartbeat (2%), rain (1%) | ✅ |
| tuer | echt | a heavy door slamming (79%), a deep cinematic impact boom (19%), a fast whoosh swoosh sound effect (0%) | ✅ |
| whoosh | echt | a fast whoosh swoosh sound effect (100%), a deep cinematic impact boom (0%), a walkie talkie radio squelch beep (0%) | ✅ |
| atmo_stadt | echt | a car engine (41%), city at night ambience with distant dogs and traffic (29%), rain (18%) | ✅ |

## C) Pegel je Einstellung (Stimme vs. Hintergrund)

63 Einstellungen geprüft, 4 mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).

## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)

Übereinstimmung Skript ↔ Gehörtes: **97%** (gut ab ~85 %).

## E) Lautheit
Integriert: -29.0 LUFS (Ziel −14 … −16), True Peak: -9.9 dBFS

## Ergebnis
- Einstellung 26 ('Und: Er darf *nicht* entkommen'): Stimme nur 6.1 dB über Hintergrund
- Einstellung 38 ('Am Fenster: ein Mann mit Bart.'): Stimme nur 7.5 dB über Hintergrund
- Einstellung 41 ('„*Jetzt*.“'): Stimme nur 3.8 dB über Hintergrund
- Einstellung 45 ('*Schüsse*.'): Stimme nur 6.5 dB über Hintergrund
