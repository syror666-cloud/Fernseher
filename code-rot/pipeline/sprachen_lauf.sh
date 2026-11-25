#!/bin/bash
# Sprachfassungen EN/ES (nur aggressiver Schnitt): Spindstreifen + Spind-Intro/Outro mit übersetzten Schildern,
# Schnitt, Hörprüfung, Push. Folge 4 erst, wenn ihre deutschen 3D-Renders fertig sind. Wiederaufnehmbar.
set -u
R=/home/user/Fernseher/code-rot; LOG=$R/sprachen.log; cd "$R"
B=/home/user/tools/blender-4.2.3-linux-x64/blender
log() { echo "[$(date +%H:%M)] $*" | tee -a "$LOG"; }
push() {
  cd /home/user/Fernseher; git add -A code-rot >/dev/null 2>&1
  git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FCMPR79eF3f3cbbQsykT4T" >/dev/null 2>&1
  for i in 1 2 3 4; do git push -q -u origin claude/nice-keller-en8zl7 >/dev/null 2>&1 && break; sleep $((i * 15)); done
  cd "$R"
}
streifen() {  # $1 Sprache, $2 Variante (standard|bloque)
  local z=$R/spinde/$1_$2.png
  [ -s "$z" ] && return
  log "Spindstreifen $1 $2"
  local extra=(); local fig=$R/folge01_gsg9/test/figuren/png
  if [ "$2" = bloque ]; then extra=(--ersatz "SEK=BLOQUE DE BÚSQUEDA|KOLUMBIEN|bloque" --fokus "BLOQUE DE BÚSQUEDA"); fig=$R/folge04_bloque/test/figuren/png; fi
  nice -n 10 $B -b -P pipeline/blender/scene_spinde.py -- --out "$z" --hoehe 1536 --samples 20 \
    --font $R/assets/fonts/Montserrat-Black.ttf --figuren "$fig" --sprache "$1" "${extra[@]}" >> $R/spinde/render.log 2>&1
}
folge() {  # $1 Basisordner, $2 Sprache
  local f=$1_$2
  grep -q "$f: FERTIG" "$LOG" 2>/dev/null && return
  if [ ! -f $f/audio/timing.json ]; then
    python3 -I pipeline/sprache.py $1/episode.py $2 >> "$LOG" 2>&1
    python3 -I pipeline/vo.py $f/episode.py >> "$LOG" 2>&1
  fi
  local nur=$(python3 -I -c "
import importlib.util
s=importlib.util.spec_from_file_location('e','$f/episode.py');e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
print(','.join(n for n,a in e.ANIM.items() if a['szene']=='spinde'))")
  log "$f: Spind-Animationen ($nur)"
  nice -n 10 python3 -I pipeline/anim_render.py $f/episode.py --samples 6 --nur "$nur" >> $f/anim/render.log 2>&1
  log "$f: Schnitt aggressiv"
  if ANIM_JOBS=2 nice -n 10 python3 -I pipeline/cut.py $f/episode.py --aggressiv >> "$LOG" 2>&1; then
    nice -n 10 python3 -I pipeline/hoerpruefung.py $f/episode.py >> "$LOG" 2>&1
    log "$f: FERTIG -> $f/export/${f}_aggressiv.mp4"
    push "CODE ROT $f: Sprachfassung (aggressiv)"
  else
    log "$f: FEHLER beim Schnitt"
  fi
}
mkdir -p spinde
for L in en es; do
  streifen $L standard
  for F in folge01_gsg9 folge02_seals folge03_bope; do folge $F $L; done
done
log "Folge 4: wartet auf die deutschen 3D-Renders"
until grep -q "Folge 4: Schnitt normal" folge4.log; do sleep 60; done
for L in en es; do
  streifen $L bloque
  folge folge04_bloque $L
done
log "SPRACHEN_ENDE"
