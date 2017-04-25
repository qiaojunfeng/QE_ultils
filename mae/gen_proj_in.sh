#!/bin/bash
# should ensure you are currently in '1-par/' or '2-per'
# both '1-par' and '2-per' should exist.
# fermi energy will be extracted from '2-per'

touchProjPar() {
    cat << EOF > proj_par.in
 &projwfc
    outdir = './tempdir/'
    prefix = 'par'
! eV
    Emin = -35.0
    Emax = 35.0
    DeltaE = 0.01
! Ry
    degauss = 0.002
    ngauss = -1
    lsym = .false.
    filproj = 'eband_par.dat'
! ef_0 unit: eV
    ef_0 = 7.3704909800885954
    lforcet = .true.
 /
EOF
}

touchProjPer() {
    cat << EOF > proj_per.in
 &projwfc
    outdir = './tempdir/'
    prefix = 'per'
! eV
    Emin = -35.0
    Emax = 35.0
    DeltaE = 0.01
! Ry
    degauss = 0.002
    ngauss = -1
    lsym = .false.
    filproj = 'eband_per.dat'
! ef_0 unit: eV
    ef_0 = 7.3704909800885954
    lforcet = .true.
 /
EOF
}

PWDIR=`pwd`
CURDIR=`basename $PWD`

if [ -e 'proj_par.in' ]; then
    DIREC='par'
    echo '1'
elif [ -e 'proj_per.in' ]; then
    DIREC='per'
    echo '2'
elif [ "$CURDIR" = '1-par' ]; then
    touchProjPar
    DIREC='par'
    echo '3'
elif [ "$CURDIR" = '2-per' ]; then
    touchProjPer
    DIREC='per'
    echo '4'
else
    echo '5'
    exit 1
fi

if [ -d "../2-per/" ]; then
    cd ../2-per/
else
    exit 1
fi
FERMI=`grepfermi.sh | tail -2 | head -1`
FERMIEV=`pwuc au2ev $FERMI`
# remove all whitespace
FERMIEV="$(echo -e $FERMIEV | tr -d '[:space:]' )"
cd $PWDIR

echo $FERMIEV

sed -i "s/    ef_0 = .*/    ef_0 = $FERMIEV/" "proj_"$DIREC".in"
