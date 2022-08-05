export IPUOF_VIPU_API_HOST=$1
export IPUOF_VIPU_API_PARTITION_ID=$2
while true;
 do
   #for i in {0..127}; do IPUOF_VIPU_API_GCD_ID=$i gc-monitor --no-card-info; done # for pod128
   gc-monitor --no-card-info;
   sleep 1s;
 done
