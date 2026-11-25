# Hörprüfung folge02_seals

## A/B) Geräusche und Atmosphäre (KI-Erkennung CLAP)

| Geräusch | Datei | erkannt als (Top 3) | Ergebnis |
|---|---|---|---|
| alarm | echt | an alarm siren (40%), a walkie talkie radio squelch beep (39%), electronic beeps (16%) | ✅ |
| drone_hit | echt | a deep dark cinematic drone hit (80%), a deep cinematic impact boom (13%), a fast whoosh swoosh sound effect (3%) | ✅ |
| funk | echt | a walkie talkie radio squelch beep (91%), electronic beeps (4%), applause (2%) | ✅ |
| heartbeat | echt | a heartbeat (80%), a fast whoosh swoosh sound effect (5%), a ticking clock (4%) | ✅ |
| impact | echt | a deep cinematic impact boom (81%), fire igniting and burning (16%), a fast whoosh swoosh sound effect (1%) | ✅ |
| schuesse | echt | gunshots (97%), a deep cinematic impact boom (1%), footsteps (1%) | ✅ |
| tick | echt | a ticking clock (97%), a heartbeat (2%), rain (1%) | ✅ |
| whoosh | echt | a fast whoosh swoosh sound effect (100%), a deep cinematic impact boom (0%), a walkie talkie radio squelch beep (0%) | ✅ |
| atmo_meer | echt | ocean waves at night (40%), white noise static hiss (40%), rain (15%) | ✅ |

## C) Pegel je Einstellung (Stimme vs. Hintergrund)

73 Einstellungen geprüft, 5 mit zu lautem Hintergrund (Ziel: Stimme ≥ 8 dB darüber).

## D) Sprachverständlichkeit (Whisper hört den fertigen Mix)

Übereinstimmung Skript ↔ Gehörtes: **96%** (gut ab ~85 %).

## E) Lautheit
Integriert: -14.6 LUFS (Ziel −14 … −16), True Peak: -0.3 dBFS

## Ergebnis
- Einstellung 27 ('*Schüsse*.'): Stimme nur 3.5 dB über Hintergrund, Geräuschspitze 13.3 dB über Stimme
- Einstellung 33 ('Und: Es gibt *keinen* zweiten '): Stimme nur 4.4 dB über Hintergrund
- Einstellung 48 ('*Jetzt*.'): Stimme nur 2.1 dB über Hintergrund
- Einstellung 49 ('Drei Schüsse.'): Stimme nur 6.1 dB über Hintergrund
- Einstellung 69 ('Drei Schüsse.'): Stimme nur 6.8 dB über Hintergrund
