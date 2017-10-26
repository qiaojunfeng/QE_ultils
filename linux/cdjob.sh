#!/bin/bash

yhqueue | grep $1
WorkDir=`yhcontrol show job $1 | grep WorkDir | cut -d '=' -f 2`

if [ -d "$WorkDir" ]; then
    echo '             WorkDir =' $WorkDir
    cd $WorkDir
else
    echo 'Nothing done.'
fi
