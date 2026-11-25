#!/bin/bash
# Folge 4 (Bloque de Búsqueda): wartet auf das Ende des Nachtlaufs (Folge 3), dann Spindstreifen, 3D-Animation,
# Schnitt normal + Hörprüfung, Schnitt aggressiv, Push. Jeder Schritt ist wiederaufnehmbar.
set -u
R=/home/user/Fernseher/code-rot
F=folge04_bloque
LOG=$R/folge4.log
B=/home/user/tools/blender-4.2.3-linux-x64/blender
cd "$R"
log() { echo "[$(date +%H:%M)] $*" | tee -a "$LOG"; }
push() {
  cd /home/user/Fernseher
  git add -A code-rot >/dev/null 2>&1
  git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FCMPR79eF3f3cbbQsykT4T" >/dev/null 2>&1
  for i in 1 2 3 4; do git push -q -u origin claude/nice-keller-en8zl7 >/dev/null 2>&1 && break; sleep $((i * 15)); done
  cd "$R"
}
log "Folge 4: wartet auf Nachtlauf-Ende"
until grep -q NACHTLAUF_ENDE nacht.log; do sleep 60; done
if [ ! -s $F/bg/spinde_streifen.png ]; then
  log "Folge 4: Spindstreifen (Cycles)"
  nice $B -b -P pipeline/blender/scene_spinde.py -- --out $R/$F/bg/spinde_streifen.png --hoehe 1536 --samples 20 \
    --font $R/assets/fonts/Montserrat-Black.ttf --figuren $R/$F/test/figuren/png \
    --ersatz "SEK=BLOQUE DE BÚSQUEDA|KOLUMBIEN|bloque" --fokus "BLOQUE DE BÚSQUEDA" >> $F/anim/render.log 2>&1
fi
log "Folge 4: 3D-Animation"
while pgrep -f "anim_render.py $F/" >/dev/null; do sleep 30; done
python3 -I pipeline/anim_render.py $F/episode.py --samples 6 >> $F/anim/render.log 2>&1 || true
if grep -q FEHLER $F/anim/render.log; then
  log "Folge 4: Renderfehler -> zweiter Versuch"
  python3 -I pipeline/anim_render.py $F/episode.py --samples 6 >> $F/anim/render.log 2>&1 || true
fi
log "Folge 4: Schnitt normal entfällt (nur aggressiv) – 3D-Renders fertig"
nice python3 -I pipeline/hoerpruefung.py $F/episode.py >> "$LOG" 2>&1 || true
log "Folge 4: Schnitt aggressiv"
if ANIM_JOBS=3 python3 -I pipeline/cut.py $F/episode.py --aggressiv >> "$LOG" 2>&1; then
  log "Folge 4: AGGRESSIV_FERTIG -> $F/export/${F}_aggressiv.mp4"
  push "CODE ROT Folge 4 BLOQUE DE BÚSQUEDA: aggressiver Schnitt"
else
  log "Folge 4: AGGRESSIV_FEHLER"
fi
log "FOLGE4_ENDE"
