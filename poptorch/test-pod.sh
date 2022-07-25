#!/bin/bash

SIZE=$1
if [[ $REPLICAS -le 16 ]]
then
    SIZE=16
elif [[ $REPLICAS -le 64 ]]
then
    SIZE=64
fi

vipu create partition p${SLURM_JOB_ID} --allocation c${SLURM_JOB_ID} --size $SIZE --reconfigurable


export IPUOF_VIPU_API_HOST=pod001-1-ctrl
export IPUOF_VIPU_API_PARTITION_ID=p${SLURM_JOB_ID}
PARTITION=p${SLURM_JOB_ID}

SERVER=pod001-1-ctrl
NETMASK=10.5.0.0/16

NW=2
GA=15

LR=$2
NUM_REPLICAS=$1
INSTANCES=$NUM_REPLICAS
bash run-slurm.sh $NUM_REPLICAS $INSTANCES $PARTITION $SERVER $NETMASK $LR $NW $GA $COMP
