# Edit below settings accordingly in order to call run.sh
# To execute, type "bash test.sh"
HOSTS=lr67-1-poplar-1
PARTITION=lr67-1-64ipum # To get partition name: vipu-admin list partition
SERVER=lr67-1-ctrl
NETMASK=10.5.0.0/16

GA=2 #3
LR=0.002

for NUM_REPLICAS in 32 64
#for LR in 0.001 #0.001 0.002 0.005
  do
  # use 4 hosts for 16 IPUs and above
  # although there is only 1 host for 16 IPUs
  # HOSTS can be extended for up to 16 hosts for POD256 using more branches
  HOSTS=lr67-1-poplar-[1-4]
  if [ $NUM_REPLICAS -eq 32 ]
  then
    HOSTS=lr67-1-poplar-[1-2]
  fi
  INSTANCES=$((NUM_REPLICAS/4))
  for i in `seq 0 2` # 1 or more runs
    do 
    bash run.sh $NUM_REPLICAS $INSTANCES $HOSTS $PARTITION $SERVER $NETMASK $LR $GA 2>&1 | tee r"$NUM_REPLICAS"_v"$i".log
    done
  done

