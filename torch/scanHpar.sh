#!/bin/bash
set -u ;  # exit  if you try to use an uninitialized variable
#set -x ;  # print out the statements as they are being executed
#set -e ;  #  bash exits if any statement returns a non-true return value
#set -o errexit ;  # exit if any statement returns a non-true return value

k=0

epochs=161
cellName=practice140c
for lr in .0002 .0003 .001 .003  ; do 
    jobId=lr${lr}
    echo job=$jobId
    export NEUINV_WRK_SUFIX="try3/$jobId"
    export NEUINV_OTHER_PAR=" --epochs ${epochs} --initLR ${lr}  --jobId ${jobId} --cellName $cellName "  # will overwrite any other settings
    
    sbatch  batchShifter.slr      # PM
    #./batchShifter.slr      # PM  - interactive
    sleep 1
    k=$[ ${k} + 1 ]
    #exit
done
