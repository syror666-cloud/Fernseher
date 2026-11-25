#!/bin/bash
# Folge 1 + 2 nach Einbau der Figurenstimmen neu schneiden (normal + Hörprüfung + aggressiv), dann pushen.
set -u
R=/home/user/Fernseher/code-rot; LOG=$R/neuschnitt.log; cd "$R"
log() { echo "[$(date +%H:%M)] $*" | tee -a "$LOG"; }
for f in folge01_gsg9 folge02_seals; do
  if grep -q "$f: NEU_FERTIG" "$LOG" 2>/dev/null; then continue; fi
  log "$f: Neuschnitt normal"
  ANIM_JOBS=2 nice python3 -I pipeline/cut.py $f/episode.py >> "$LOG" 2>&1 && \
  nice python3 -I pipeline/hoerpruefung.py $f/episode.py >> "$LOG" 2>&1
  log "$f: Neuschnitt aggressiv"
  ANIM_JOBS=2 nice python3 -I pipeline/cut.py $f/episode.py --aggressiv >> "$LOG" 2>&1 && log "$f: NEU_FERTIG"
  cd /home/user/Fernseher && git add -A code-rot >/dev/null 2>&1 && git commit -qm "CODE ROT $f: Neuschnitt mit Figurenstimmen

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FCMPR79eF3f3cbbQsykT4T" >/dev/null 2>&1
  for i in 1 2 3 4; do git push -q -u origin claude/nice-keller-en8zl7 >/dev/null 2>&1 && break; sleep $((i * 15)); done
  cd "$R"
done
log "NEUSCHNITT_ENDE"
