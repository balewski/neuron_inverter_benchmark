#!/bin/bash
set -u ;  # exit  if you try to use an uninitialized variable
#set -x ;  # print out the statements as they are being executed
#set -e ;  #  bash exits if any statement returns a non-true return value
#set -o errexit ;  # exit if any statement returns a non-true return value

k=0
nodes=4
epochs=161
cellName=practice140c
#for lr in .0001  .0002 .0003 .001 .003  ; do 
for lr in  .0006 .0008 .0011 .0015 .002 .005  ; do 
    jobId=lr${lr}
    echo job=$jobId
    export NEUINV_WRK_SUFIX="try4/$jobId"
    export NEUINV_OTHER_PAR=" --epochs ${epochs} --initLR ${lr}  --jobId ${jobId} --cellName $cellName "  # will overwrite any other settings
    
    sbatch  -N $nodes batchShifter.slr      # PM
    #./batchShifter.slr      # PM  - interactive
    sleep 1
    k=$[ ${k} + 1 ]
    #exit
done
date

#Cancel all my jobs:
#squeue -u $USER -h | awk '{print $1}' | xargs scancel
