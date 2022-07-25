#!/bin/bash
CC=$1
if [ "$CC" == "" ]
then echo "Usage $0 <number of instances>"
     exit 1
fi
BASE=$(echo $SLURM_JOB_NODELIST  | cut -d '-' -f 1,2,3)
if [ "${SLURM_JOB_NODELIST/[/}" == "${SLURM_JOB_NODELIST}" ]
then NODELIST=$SLURM_JOB_NODELIST
else
    #echo base=$BASE
    NODERANGE=$(echo $SLURM_JOB_NODELIST | cut -d '-' -f 4,5,6,7 | sed -e "s/\[/{/" -e "s/\-/../g" -e "s/\]/}/" -e "s/,/} {/")
    RAWNODELIST=$(sed "s/{/$BASE-{/g" <<< $NODERANGE )
    #echo raw $RAWNODELIST
    NODELIST=$(eval echo $(echo $RAWNODELIST))
fi
#echo node $NODELIST
COUNT=$(echo $NODELIST | wc -w)
SKIP=$((COUNT/CC))
I=0
read -a NA <<< $NODELIST
HOSTS=""
while [ $I -lt $((COUNT+1)) ]
do
    HOSTS="$HOSTS,${NA[$I]}"
    I=$(($I+$SKIP))
done
HOSTS=$(sed -e 's/^,//g' -e 's/,$//g' <<<$HOSTS)
echo $HOSTS
