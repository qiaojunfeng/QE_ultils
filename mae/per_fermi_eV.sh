#!/bin/bash

FERMI=`grepfermi.sh | tail -2 | head -1`
FERMIEV=`pwuc au2ev $FERMI`
# remove all whitespace
FERMIEV="$(echo -e $FERMIEV | tr -d '[:space:]' )"
echo $FERMIEV
