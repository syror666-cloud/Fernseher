#!/bin/bash
# Neuer Look (Referenz-Niveau): 3D-Szenen in 720x1280 mit goldener Stunde neu rendern, dann Folge 4 schneiden (B + A).
set -u
R=/home/user/Fernseher/code-rot; cd "$R"
LOG=$R/neulook.log
log() { echo "[$(date +%H:%M)] $*" | tee -a "$LOG"; }
push() {
  cd /home/user/Fernseher
  git add code-rot/pipeline code-rot/folge04_bloque/episode.py code-rot/folge04_bloque/figuren_folge.py code-rot/folge04_bloque/svg \
    code-rot/folge04_bloque/anim/gruppen.json code-rot/folge04_bloque/export code-rot/neulook.log >/dev/null 2>&1
  git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FCMPR79eF3f3cbbQsykT4T" >/dev/null 2>&1
  for i in 1 2 3 4; do git push -q -u origin claude/nice-keller-en8zl7 >/dev/null 2>&1 && break; sleep $((i * 15)); done
  cd "$R"
}
F=folge04_bloque
log "Folge 4: 3D-Renders 720x1280 (neuer Look)"
for i in 1 2; do
  python3 -I pipeline/anim_render.py $F/episode.py --samples 8 --res 720x1280 >> $F/anim/render.log 2>&1 || true
  grep -q FEHLER <(tail -40 $F/anim/render.log) || break
  log "Folge 4: Renderfehler -> Versuch $((i+1))"
done
log "Folge 4: Schnitt B (Roulette)"
HOOK=roulette ANIM_JOBS=3 python3 -I pipeline/cut.py $F/episode.py --aggressiv >> "$LOG" 2>&1 && log "B_FERTIG" || log "B_FEHLER"
log "Folge 4: Schnitt A (Hook 2.0)"
ANIM_JOBS=3 python3 -I pipeline/cut.py $F/episode.py --aggressiv >> "$LOG" 2>&1 && log "A_FERTIG" || log "A_FEHLER"
push "Folge 4 im neuen Look: goldene Stunde, 720p-Renders, Figuren mit Kontur in ganzer Größe im Bild"
log "NEULOOK4_ENDE"
