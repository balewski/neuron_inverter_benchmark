#!/bin/bash

SIZE=$1
if [ $SIZE -eq 32 ]
then
   SIZE=64
elif [ $SIZE -le 16 ]
then
   SIZE=16
fi
vipu create partition p${SLURM_JOB_ID} --allocation c${SLURM_JOB_ID} --size $SIZE --reconfigurable

source /mnt/poddata/users/janel/torch-1025.sh
export IPUOF_VIPU_API_HOST=lr17-1-ctrl
export IPUOF_VIPU_API_PARTITION_ID=p${SLURM_JOB_ID}
PARTITION=p${SLURM_JOB_ID}

SERVER=lr17-1-ctrl
NETMASK=10.5.0.0/16

NW=2
#IOT=104
COMP=0
#GA=15

NUM_REPLICAS=$1
LR=$2
GA=$3
INSTANCES=$NUM_REPLICAS
#bash test-gc-monitor.sh lr17-1-ctrl p${SLURM_JOB_ID} >& log.energy_"$NUM_REPLICAS".csv & eneId=$!
#sleep 60
bash run-slurm.sh $NUM_REPLICAS $INSTANCES $PARTITION $SERVER $NETMASK $LR $NW $GA $COMP
#sleep 60
#kill $eneId
