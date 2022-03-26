#!/bin/bash
set -u ;  # exit  if you try to use an uninitialized variable
#set -x ;  # print out the statements as they are being executed
#set -e ;  #  bash exits if any statement returns a non-true return value
#set -o errexit ;  # exit if any statement returns a non-true return value

k=0
#nodes=2 ; runTime=4:25:00
nodes=16 ; runTime=15:00
#nodes=32 ; runTime=10:00
taskPerNode=4
#epochs=30
cellName=practice140c  # Kewei
#cellName=witness2c   #GC-SC22
cellName=witness13c_fp16   #GC-Jane
#design=pmref # Kewei
design=gcref2 #GC-Jane
G=$[ ${taskPerNode} * ${nodes} ]
echo N=${nodes} G=$G runTime=$runTime
#for lr in .0005 .001 .002 .005   ; do  # 8G,4G, 2G?
##for lr in  .001 .002 .005 .01 0.02  ; do  # 16G
for lr in   .002 .005 .01   ; do  # 32,64,128G
#for lr in   .0005   ; do
    jobId=lr${lr}    
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

# 4 steps per decade
# for lr in  .0010 .0018 .0032 .0056 0.010 0.018 0.056  ; do  # 16G
