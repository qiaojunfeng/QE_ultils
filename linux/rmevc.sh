#!/bin/bash

#cd ~/qiao/
if [[ -e "chg.list" ]]; then
    rm chg.list
fi
if [[ -e "tchg.list" ]]; then
    rm tchg.list
fi

#find . -name 'CHG' -exec ls -l {} > tchg.list \;
find . -name 'evc*.dat' -exec ls -l {} > tchg.list \;
awk 'BEGIN {sum = 0} {print $5,$9; sum += $5} END {print sum/1024/1024/1024,"GB"}' tchg.list > chg.list
head -n-1 chg.list | awk '{print $2}' > tchg.list
more chg.list

echo
echo -e 'Delete?(Y/n):\c ' 
read sel
sel=`echo $sel | tr '[A-Z]' '[a-z]'`
sel=${sel:0:1}
if [[ "$sel" == "y" ]]; then
    xargs rm -rf < tchg.list
    echo 'Deleted.'
fi

rm tchg.list

