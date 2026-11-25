#!/bin/bash
# Schneidet alle Folgen zusätzlich im aggressiven Modus (cut.py --aggressiv).
# Folge 3 wartet, bis der Nachtlauf ihren normalen Schnitt fertig hat (3D-Renders müssen vollständig sein).
set -u
R=/home/user/Fernseher/code-rot
LOG=$R/aggressiv.log
cd "$R"
log() { echo "[$(date +%H:%M)] $*" | tee -a "$LOG"; }
for f in folge01_gsg9 folge02_seals folge03_bope; do
  if [ "$f" = folge03_bope ]; then
    until grep -q "Folge 3 BOPE: FERTIG\|Folge 3 BOPE: Schnitt fehl" nacht.log; do sleep 60; done
  fi
  log "$f: aggressiver Schnitt"
  if ANIM_JOBS=2 nice python3 -I pipeline/cut.py $f/episode.py --aggressiv >> "$LOG" 2>&1; then
    log "$f: AGGRESSIV_FERTIG -> $f/export/${f}_aggressiv.mp4"
  else
    log "$f: AGGRESSIV_FEHLER"
  fi
done
log "AGGRESSIV_ENDE"
