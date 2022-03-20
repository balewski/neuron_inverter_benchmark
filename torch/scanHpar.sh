#!/bin/bash
set -u ;  # exit  if you try to use an uninitialized variable
#set -x ;  # print out the statements as they are being executed
#set -e ;  #  bash exits if any statement returns a non-true return value
#set -o errexit ;  # exit if any statement returns a non-true return value

k=0
nodes=2 ; runTime=4:25:00
#nodes=64 ; runTime=25:00
taskPerNode=4
#epochs=30
cellName=practice140c
#cellName=witness2c
design=pmref
G=$[ ${taskPerNode} * ${nodes} ]
echo N=${nodes} G=$G runTime=$runTime
for lr in  .0001 .0002 .0005 .001  .002 .005  ; do 
    jobId=fp16inp_lr${lr}    
    echo job=$jobId
    export NEUINV_WRK_SUFIX="G${G}scan/$jobId"
    export NEUINV_OTHER_PAR=" --initLR ${lr}  --jobId ${jobId} --cellName $cellName --design $design "  # will overwrite any other settings
    # spare: --epochs ${epochs} 
    
    sbatch  -N $nodes --ntasks-per-node $taskPerNode  --time $runTime  batchShifter.slr      # PM
    #./batchShifter.slr      # PM  - interactive
    sleep 1
    k=$[ ${k} + 1 ]
    #exit
done
date

#Cancel all my jobs:
#squeue -u $USER -h | awk '{print $1}' | xargs scancel
