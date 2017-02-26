#!/bin/bash
cd ~

# for submission to yhbatch
for ifile in *
do
    echo -n "$ifile    "
    find $ifile | wc -l 2>&1 > file_count-`date "+%Y_%m_%d"`
done


# running in terminal with output to file
#for ifile in *
#do
#    echo -n "$ifile    "
#    find $ifile | wc -l 2>&1 | tee file_count-`date "+%Y_%m_%d"`
#done


# running in terminal 
#for ifile in *
#do
#    echo -n "$ifile    "
#    find $ifile | wc -l 2>&1
#done
