MEM=`top -ibn1 |grep avail | cut -d "+" -f 1 | cut -d "." -f 2 | cut -d " " -f 2 `
echo $MEM

if [[ "$MEM" -lt 48000000 ]] #49529488+total
then
    echo "The host memory is in use; test it later"
    exit 1
fi

rm /localdata/janel/exec_cache/*

for i in `seq 0 2`
  do
  POPTORCH_CACHE_DIR=/localdata/$USER/exec_cache IPUOF_VIPU_API_HOST=lr67-1-ctrl IPUOF_VIPU_API_PARTITION_ID=lr67-1-64ipum python ./train_replica.py --design common2c --cellName witness2c_fp16 --outPath /localdata/$USER/outX --epochs 10 --gradientAcc 2 2>&1 | tee r1_v"$i".log
  done

#PCIE configureLinks only supports '8 cards, default M2000' and not 'default sliding window configuration
