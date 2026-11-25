#!/bin/bash
# Folge 5 (Mossad) im neuen Look: wartet auf Folge 4 (neulook_lauf.sh), rendert die 3D-Szenen in 720x1280
# (Nacht mit violettem Horizont), Hörprüfung, aggressiver Schnitt (Hook 2.0), Push.
set -u
R=/home/user/Fernseher/code-rot; cd "$R"
LOG=$R/neulook.log
F=folge05_mossad
log() { echo "[$(date +%H:%M)] $*" | tee -a "$LOG"; }
push() {
  cd /home/user/Fernseher
  git add code-rot/pipeline code-rot/$F/episode.py code-rot/$F/figuren_folge.py code-rot/$F/svg code-rot/$F/anim/gruppen.json \
    code-rot/$F/export code-rot/$F/HOERPRUEFUNG.md code-rot/neulook.log >/dev/null 2>&1
  git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FCMPR79eF3f3cbbQsykT4T" >/dev/null 2>&1
  for i in 1 2 3 4; do git push -q -u origin claude/nice-keller-en8zl7 >/dev/null 2>&1 && break; sleep $((i * 15)); done
  cd "$R"
}
log "Folge 5: wartet auf Folge 4 (neuer Look)"
until grep -q NEULOOK4_ENDE "$LOG"; do sleep 60; done
if [ ! -f $F/anim/.neulook ]; then
  for d in $F/anim/*/; do case "$d" in */intro/|*/outro/) ;; *) rm -f "$d"*.png ;; esac; done
  touch $F/anim/.neulook
fi
log "Folge 5: 3D-Renders 720x1280 (neuer Look)"
for i in 1 2; do
  python3 -I pipeline/anim_render.py $F/episode.py --samples 8 --res 720x1280 >> $F/anim/render.log 2>&1 || true
  grep -q FEHLER <(tail -40 $F/anim/render.log) || break
  log "Folge 5: Renderfehler -> Versuch $((i+1))"
done
nice python3 -I pipeline/hoerpruefung.py $F/episode.py >> "$LOG" 2>&1 || true
log "Folge 5: Schnitt A (Hook 2.0)"
ANIM_JOBS=3 python3 -I pipeline/cut.py $F/episode.py --aggressiv >> "$LOG" 2>&1 && log "A5_FERTIG" || log "A5_FEHLER"
push "Folge 5 MOSSAD im neuen Look: Nacht mit violettem Horizont, Figuren handeln im Bild"
log "NEULOOK5_ENDE"
