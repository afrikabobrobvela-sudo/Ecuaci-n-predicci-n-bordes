#!/bin/bash
cd "$(dirname "$0")"
export TMPDIR=$PWD/tmp
for c in $(ls -S -r ../../data/estructuras_cod/cif/*.cif); do
  grep -q "^$c " work/pred_cod.jsonl 2>/dev/null && continue
  s=$(date +%s)
  python3 hagh_m5.py "$c" 2>&1 | grep '^\.\./' >> work/pred_cod.jsonl
  echo "$(basename $c) $(( $(date +%s)-s ))s" >> work/progreso.log
done
echo FIN >> work/progreso.log
