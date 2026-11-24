#!/bin/bash
# Rendert alle Hintergründe für Folge 1 (864x1536, wird auf 1080x1920 skaliert)
set -u
B=/home/user/tools/blender-4.2.3-linux-x64/blender
R=/home/user/Fernseher/code-rot
O=$R/folge01_gsg9/bg
RES=864x1536; SM=20
r() { local name=$1; shift; [ -f "$O/$name.png" ] && { echo "SKIP $name"; return; }
  $B -b -P "$@" --out "$O/$name.png" 2>&1 | grep -E "FERTIG|Error|Traceback" ; }
RF="$R/pipeline/blender/scene_rollfeld.py --"
KB="$R/pipeline/blender/scene_kabine.py --"
r drohne       $RF --shot drohne --fire 0 --res $RES --samples $SM
r boden        $RF --shot boden --fire 0 --res $RES --samples $SM
r boden_tief   $RF --shot boden_tief --fire 0 --res $RES --samples $SM
r fenster      $RF --shot fenster --fire 0 --res $RES --samples $SM
r leiter       $RF --shot tragflaeche --leiter --fire 1 --res $RES --samples $SM
r nase_feuer   $RF --shot nase --fire 1 --res $RES --samples $SM
r boden_feuer  $RF --shot boden --fire 1 --res $RES --samples $SM
r drohne_feuer $RF --shot drohne --fire 1 --leiter --res $RES --samples $SM
r rutsche      $RF --shot rutsche --rutsche --offen --fire 0.3 --res $RES --samples $SM
r drohne_ende  $RF --shot drohne --rutsche --offen --fire 0.3 --res $RES --samples $SM
r kabine_dunkel   $KB --shot gang --licht dunkel --res $RES --samples $SM
r kabine_zugriff  $KB --shot gang --licht zugriff --res $RES --samples $SM
r kabine_reihe    $KB --shot reihe --licht zugriff --res $RES --samples $SM
r kabine_ausstieg $KB --shot notausstieg --licht zugriff --res $RES --samples $SM
[ -f "$O/spinde_streifen.png" ] || $B -b -P $R/pipeline/blender/scene_spinde.py -- --out $O/spinde_streifen.png --hoehe 1536 --samples 20 \
   --font $R/assets/fonts/Montserrat-Black.ttf --figuren $R/folge01_gsg9/test/figuren/png 2>&1 | grep -E "FERTIG|Error|Traceback"
echo ALLE_FERTIG
