#!/bin/bash
set -u ;  # exit  if you try to use an uninitialized variable
#set -x ;  # print out the statements as they are being executed
#set -e ;  #  bash exits if any statement returns a non-true return value
#set -o errexit ;  # exit if any statement returns a non-true return value

k=0
nodes=1 ; taskPerNode=1 ; runTime=50:00
nodes=1 ; taskPerNode=2 ; runTime=30:00
nodes=8 ; taskPerNode=4 ; runTime=20:00

cellName=witness2c
design=gcrefSC22
G=$[ ${taskPerNode} * ${nodes} ]
echo N=${nodes} G=$G runTime=$runTime

for epochs in  50 150  ; do 
    jobId=epoch$epochs
    echo job=$jobId
    export NEUINV_WRK_SUFIX="G${G}ene/$jobId"
    export NEUINV_OTHER_PAR="   --jobId ${jobId} --cellName $cellName --design $design  --epochs ${epochs} "  # will overwrite any other settings
    # spare:  
    
    sbatch  -N $nodes --ntasks-per-node $taskPerNode --time $runTime -J ni_ene  batchShifter.slr      # PM
    #./batchShifter.slr      # PM  - interactive
    sleep 1
    k=$[ ${k} + 1 ]
    #exit
done
date

#Cancel all my jobs:
#squeue -u $USER -h | awk '{print $1}' | xargs scancel
