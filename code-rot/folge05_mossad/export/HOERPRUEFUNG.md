# Hörprüfung folge05_mossad

## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)

| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |
|---|---|---|---|
| alarm | echt | an alarm siren (40%), a walkie talkie radio squelch beep (39%), electronic beeps (16%) | ✅ |
| drone_hit | echt | a deep dark cinematic drone hit (80%), a deep cinematic impact boom (13%), a fast whoosh swoosh sound effect (3%) | ✅ |
| heartbeat | echt | a heartbeat (80%), a fast whoosh swoosh sound effect (5%), a ticking clock (4%) | ✅ |
| impact | echt | a deep cinematic impact boom (81%), fire igniting and burning (16%), a fast whoosh swoosh sound effect (1%) | ✅ |
| static | echt | white noise static hiss (91%), rain (4%), applause (3%) | ✅ |
| tick | echt | a ticking clock (97%), a heartbeat (2%), rain (1%) | ✅ |
| tuer | echt | a heavy door slamming (79%), a deep cinematic impact boom (19%), a fast whoosh swoosh sound effect (0%) | ✅ |
| whoosh | echt | a fast whoosh swoosh sound effect (100%), a deep cinematic impact boom (0%), a walkie talkie radio squelch beep (0%) | ✅ |
| atmo_nacht | echt | music (49%), rain (17%), quiet night ambience with wind and crickets (17%) | ✅ |

## C) Pegel je Einstellung (Stimme vs. Hintergrund)

57 Einstellungen geprüft, 4 mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).

## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)

Übereinstimmung Skript ↔ Gehörtes: **95%** (gut ab ~85 %).

## E) Lautheit
Integriert: -27.9 LUFS (Ziel −14 … −16), True Peak: -7.5 dBFS

## Ergebnis
- Einstellung 3 ('ob du *zurückkommst*.'): Stimme nur 6.7 dB über Hintergrund
- Einstellung 4 (''): Stimme nur 6.7 dB über Hintergrund
- Einstellung 6 ('Mai 1960.'): Stimme nur 8.0 dB über Hintergrund
- Einstellung 14 ('Seit fünfzehn Jahren auf der F'): Stimme nur 12.3 dB über Hintergrund, Geräuschspitze 12.4 dB über Stimme
