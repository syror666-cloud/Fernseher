#!/bin/bash
# CODE ROT Nachtlauf: rendert und schneidet alle Folgen nacheinander. Jeder Schritt ist wiederaufnehmbar
# (fertige Renders/Clips werden übersprungen). Start:  nohup setsid pipeline/nachtlauf.sh &
# Fortschritt: code-rot/nacht.log   Status je Folge: code-rot/STATUS.md
set -u
R=/home/user/Fernseher/code-rot
LOG=$R/nacht.log
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

folge() {
  local f=$1 name=$2
  log "== $name: 3D-Animation =="
  # wartet, falls schon ein Renderprozess für diese Folge läuft
  while pgrep -f "anim_render.py $f/" >/dev/null; do sleep 30; done
  python3 -I pipeline/anim_render.py $f/episode.py --samples 6 >> $f/anim/render.log 2>&1 || true
  mkdir -p $f/anim
  if grep -q FEHLER $f/anim/render.log; then log "$name: Renderfehler, siehe $f/anim/render.log (zweiter Versuch)"; \
     python3 -I pipeline/anim_render.py $f/episode.py --samples 6 >> $f/anim/render.log 2>&1 || true; fi
  python3 -I pipeline/freesound.py >> $LOG 2>&1 || true
  log "== $name: Schnitt (Animator, Untertitel, Ton) =="
  if ANIM_JOBS=3 python3 -I pipeline/cut.py $f/episode.py >> $LOG 2>&1; then
    log "$name: FERTIG -> $f/export/$f.mp4"
    echo "- $name: fertig ($(date +%H:%M)) -> $f/export/$f.mp4" >> STATUS.md
    push "CODE ROT $name: fertige Folge"
  else
    log "$name: Schnitt fehlgeschlagen"
    echo "- $name: Schnitt fehlgeschlagen ($(date +%H:%M)), siehe nacht.log" >> STATUS.md
  fi
}

log "Nachtlauf gestartet"
mkdir -p folge02_seals/anim folge03_bope/anim
# Sounds (falls Freesound-Schlüssel aktiv): echte Geräusche laden, sonst bleiben die synthetischen
python3 -I pipeline/freesound.py >> $LOG 2>&1 || log "Freesound nicht verfügbar – synthetische Sounds bleiben"
folge folge01_gsg9 "Folge 1 GSG 9"
folge folge02_seals "Folge 2 NAVY SEALS"
folge folge03_bope "Folge 3 BOPE"
log "NACHTLAUF_ENDE"
