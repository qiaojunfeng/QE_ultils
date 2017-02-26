#!/bin/bash
if [ -e "$1" ]; then
    OUTFILE="$1"
else
    OUTFILE=`find . -maxdepth 1 \( -name '*.out' -and -not -name     'slurm-*.out' \) | head -1`
fi

echo 'OUTFILE is' $OUTFILE
echo

awk -F " " '/iteration #/{print $1,$2,$3} /time/{print "    ",$1,$2,$3,$9,$10,"    diff time",$9-p,"secs"; p=$9;}' $OUTFILE
