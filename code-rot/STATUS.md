# CODE ROT – Status Nachtlauf

Ablauf (automatisch, `pipeline/nachtlauf.sh`, Log: `nacht.log`):
1. Folge 1 GSG 9: restliche 3D-Sequenzen rendern → Animator-Schnitt → Export → Commit
2. Folge 2 NAVY SEALS: 3D-Sequenzen (Meer) → Schnitt → Export → Commit
3. Folge 3 BOPE: 3D-Sequenzen (Favela) → Schnitt → Export → Commit

Wiederaufnahme nach Abbruch: `nohup setsid pipeline/nachtlauf.sh &` – fertige Teile werden übersprungen.

## Ergebnisse
- Folge 1 GSG 9: fertig (02:44) -> folge01_gsg9/export/folge01_gsg9.mp4
- Folge 2 NAVY SEALS: fertig (04:50) -> folge02_seals/export/folge02_seals.mp4
- Folge 2 NAVY SEALS: neu geschnitten (05:05): Titel-Fix, Meer leiser, Limiter
