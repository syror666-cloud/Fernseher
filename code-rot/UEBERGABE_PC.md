# CODE ROT – Übergabe an die Sitzung auf dem PC (Windows, Grafikkarte)

Diese Datei ist für eine **Claude-Code-Sitzung auf dem PC des Nutzers** (Ordner `C:\CodeRot`). Die Cloud-Sitzung hat
Skripte, Episoden, Stimmen und Hook-Audio vorbereitet. Auf dem PC laufen nur die rechenintensiven Teile:
3D-Renders (Blender) und Schnitt. Erst Schritt 1–3 einrichten, dann Folge 5 rendern (Schritt 4).

## Regeln (unbedingt einhalten)
- **Folge 1 (Deutsch) nicht anfassen**, nichts in `folge01_gsg9/` neu schneiden.
- **Keine neue Sprachausgabe erzeugen.** Auf dem PC gibt es keinen ElevenLabs-Schlüssel. Alle Stimmen liegen in
  `<folge>/audio/` (auch `hook_vo_*.mp3`). Fehlt etwas, abbrechen und dem Nutzer melden – die Cloud-Sitzung erzeugt es.
- Nach jedem Schritt kurz berichten. Nur auf den Branch `claude/nice-keller-en8zl7` pushen, nur fertige MP4s
  (vorher mit `ffprobe` prüfen) plus Logs/`gruppen.json`. Bild-Frames (`anim/*/*.png`) sind per `.gitignore` ausgeschlossen.
- Nur aggressive Schnitte.

## 1. Programme installieren (PowerShell)
```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Gyan.FFmpeg -e
```
Danach ein **neues** PowerShell-Fenster öffnen (damit PATH aktualisiert ist).

Blender **4.2 LTS** (genau diese Version, die Szenen-Skripte sind darauf abgestimmt) als ZIP:
```powershell
New-Item -ItemType Directory -Force C:\CodeRot\tools | Out-Null
Invoke-WebRequest https://download.blender.org/release/Blender4.2/blender-4.2.3-windows-x64.zip -OutFile C:\CodeRot\tools\blender.zip
Expand-Archive C:\CodeRot\tools\blender.zip -DestinationPath C:\CodeRot\tools
```

Python- und Browser-Pakete:
```powershell
python -m pip install numpy scipy soundfile librosa requests faster-whisper
npm install -g playwright
npx playwright install chromium
```

## 2. Projekt holen
```powershell
cd C:\CodeRot
git clone -b claude/nice-keller-en8zl7 https://github.com/syror666-cloud/Fernseher.git
cd C:\CodeRot\Fernseher\code-rot
```
(Bei Nachfrage mit dem GitHub-Konto des Nutzers anmelden.)

## 3. Umgebung pro Sitzung
```powershell
$env:BLENDER = "C:\CodeRot\tools\blender-4.2.3-windows-x64\blender.exe"
```
Kurztest (ein Bild, sollte in Sekunden fertig sein):
```powershell
& $env:BLENDER -b -P pipeline/blender/scene_favela.py -- --engine eevee --samples 16 --res 1080x1920 --zeit gold --berge `
  --pfad pipeline/test_pfad.json --out C:/CodeRot/test_####
```
`pipeline/test_pfad.json` liegt im Projekt. Das Bild `C:\CodeRot\test_0001.png` dem Nutzer zeigen.

## 4. Folge 5 (Mossad) rendern und schneiden – volle Auflösung
```powershell
python -I pipeline/anim_render.py folge05_mossad/episode.py --samples 16 --res 1080x1920
python -I pipeline/cut.py folge05_mossad/episode.py --aggressiv
```
Ergebnis: `folge05_mossad/export/folge05_mossad_aggressiv.mp4` und `POSTING_de.md`.

Prüfen (Kontaktbogen aus ~12 Bildern mit ffmpeg): Nacht mit violettem Horizont, Figuren mit Kontur in ganzer Größe,
Aktionen sichtbar (Kollege geht auf die Silhouette zu, Zugriff im Laufschritt, Mund bewegt sich bei „Un momentito,
señor“), Füße auf dem Boden, nichts abgeschnitten. Dann committen und pushen:
```powershell
cd C:\CodeRot\Fernseher
git add code-rot/folge05_mossad/export code-rot/folge05_mossad/anim/gruppen.json
git commit -m "Folge 5 MOSSAD auf dem PC gerendert (1080x1920)"
git push origin claude/nice-keller-en8zl7
```
Bei abgelehntem Push: `git pull --no-rebase origin claude/nice-keller-en8zl7`, dann erneut pushen.

## 5. Danach (nach Rücksprache mit dem Nutzer)
- Folge 4 in 1080x1920 neu: wie Schritt 4 mit `folge04_bloque`, zweimal schneiden – zuerst mit `$env:HOOK="roulette"`
  (Fassung B), dann mit `Remove-Item Env:HOOK` (Fassung A).
- Sprachfassungen (`folge0X_<sprache>/`) nur nach Absprache, die Cloud-Sitzung koordiniert sie.

## Hinweise
- Die Bash-Skripte `pipeline/*_lauf.sh` enthalten Linux-Pfade und sind für die Cloud – auf dem PC die Python-Befehle
  oben direkt ausführen.
- `anim_render.py` überspringt fertige Szenen; ein Abbruch kann einfach neu gestartet werden.
- Grafikkarte: EEVEE nutzt sie automatisch. Bei Cycles (Spind-Streifen) in Blender die GPU wählen.
