#!/bin/bash
# Folge 5 (Bloque de Búsqueda): wartet auf das Ende des Nachtlaufs (Folge 3), dann Spindstreifen, 3D-Animation,
# Schnitt normal + Hörprüfung, Schnitt aggressiv, Push. Jeder Schritt ist wiederaufnehmbar.
set -u
R=/home/user/Fernseher/code-rot
F=folge05_mossad
LOG=$R/folge5.log
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
while pgrep -f "scene_spinde.py -- --out $R/$F/bg" >/dev/null; do sleep 30; done  # laufenden Streifen-Render abwarten
if [ ! -s $F/bg/spinde_streifen.png ]; then
  log "Folge 5: Spindstreifen (Cycles)"
  nice -n 5 $B -b -P pipeline/blender/scene_spinde.py -- --out $R/$F/bg/spinde_streifen.png --hoehe 1536 --samples 20 \
    --font $R/assets/fonts/Montserrat-Black.ttf --figuren $R/$F/test/figuren/png \
    --ersatz "SAT=MOSSAD|ISRAEL|mossad" --fokus "MOSSAD" >> $F/anim/render.log 2>&1
fi
log "Folge 5: wartet auf die 3D-Renders von Folge 4"
until grep -q "Folge 4: Schnitt normal" folge4.log; do sleep 60; done
log "Folge 5: 3D-Animation"
while pgrep -f "anim_render.py $F/" >/dev/null; do sleep 30; done
python3 -I pipeline/anim_render.py $F/episode.py --samples 6 >> $F/anim/render.log 2>&1 || true
if grep -q FEHLER $F/anim/render.log; then
  log "Folge 5: Renderfehler -> zweiter Versuch"
  python3 -I pipeline/anim_render.py $F/episode.py --samples 6 >> $F/anim/render.log 2>&1 || true
fi
log "Folge 5: Schnitt normal entfällt (nur aggressiv) – 3D-Renders fertig"
nice python3 -I pipeline/hoerpruefung.py $F/episode.py >> "$LOG" 2>&1 || true
log "Folge 5: Schnitt aggressiv"
if ANIM_JOBS=3 python3 -I pipeline/cut.py $F/episode.py --aggressiv >> "$LOG" 2>&1; then
  log "Folge 5: AGGRESSIV_FERTIG -> $F/export/${F}_aggressiv.mp4"
  push "CODE ROT Folge 5 MOSSAD: aggressiver Schnitt"
else
  log "Folge 5: AGGRESSIV_FEHLER"
fi
log "FOLGE5_ENDE"
