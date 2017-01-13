#!/bin/bash

echo "create SOC folders and copy there SR density and spin moment..."
echo
read -p 'dir for scf calculation: ' SCF_DIR
read -p 'dir for parallel SOC: ' PAR_DIR
read -p 'dir for perpendicular soc: ' PER_DIR
echo

case "$SCF_DIR" in
    "" ) SCF_DIR='./1-scf/' ;;
    *  ) ;;
esac

case "$PAR_DIR" in
    "" ) PAR_DIR='./2-mae/1-par/' ;;
    *  ) ;;
esac

case "$PER_DIR" in
    "" ) PER_DIR='./2-mae/2-per/' ;;
    *  ) ;;
esac

#echo $SCF_DIR
#echo $PAR_DIR
#echo $PER_DIR

for dtmp in $SCF_DIR $PAR_DIR $PER_DIR
do
    if [ -d "$dtmp" ]; then
        echo $dtmp 'OK'
    else
        echo $dtmp 'not exist!'
        echo '!!!!!!!!!!'
        exit 1
    fi
done

mkdir -p $PAR_DIR/tempdir/par.save
mkdir -p $PER_DIR/tempdir/per.save
cp $SCF_DIR/tempdir/scf.save/data-file.xml $PAR_DIR/tempdir/par.save/
cp $SCF_DIR/tempdir/scf.save/charge-density.dat $PAR_DIR/tempdir/par.save/
cp $SCF_DIR/tempdir/scf.save/spin-polarization.dat $PAR_DIR/tempdir/par.save/
cp $SCF_DIR/tempdir/scf.save/data-file.xml $PER_DIR/tempdir/per.save/
cp $SCF_DIR/tempdir/scf.save/charge-density.dat $PER_DIR/tempdir/per.save/
cp $SCF_DIR/tempdir/scf.save/spin-polarization.dat $PER_DIR/tempdir/per.save/

echo
echo 'finished'
