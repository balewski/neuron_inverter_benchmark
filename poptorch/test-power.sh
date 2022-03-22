export POPLAR_RUNTIME_OPTIONS='{"streamCallbacks.maxLookahead" : "unlimited"}'
export POPTORCH_CACHE_DIR=/localdata/$USER/exec_cache
TEMP_DIR=/localdata/$USER/my_temp
mkdir -p $TEMP_DIR
export TEMPDIR=$TEMP_DIR
export TMPDIR=$TEMP_DIR
export TEMP=$TEMP_DIR
export TMP=$TEMP_DIR

# Please modify this data path on your system.
# It needs to be either shared by multiple hosts,
# or copied to the local folders of hosts.

# To measure power consumption of IPUs via GCDA and record in PVTI:
#export GCDA_MONITOR=1

DATA_PATH=/localdata/$USER/neuron-data/

LEARNING_RATE=0.002

for REPLICAS in 16 #8 4 2 1
  do
  for EPOCHS in 50 #150
    do
    OUTPATH=out/r"$REPLICAS"_e$EPOCHS
    echo "++++++ r$REPLICAS: $EPOCHS"
    date +%s%N | cut -b1-13
    date +%Y-%m-%d_%H-%M-%S
    bash test-energy.sh >& log.energy_"$REPLICAS"_"$EPOCHS".csv & eneId=$!
    sleep 60
    poprun -vv --mpi-global-args='--tag-output --allow-run-as-root ' --mpi-local-args=' -x OPAL_PREFIX -x LD_LIBRARY_PATH -x PATH -x PYTHONPATH -x IPUOF_VIPU_API_TIMEOUT=600 -x POPLAR_RUNTIME_OPTIONS -x POPTORCH_CACHE_DIR -x TEMPDIR -x TMPDIR -x TEMP -x TMP' --ipus-per-replica 1 --numa-aware 1 --num-instances $REPLICAS --num-replicas $REPLICAS ./train_replica.py --design common --cellName witness2c --outPath $OUTPATH --initLR $LEARNING_RATE --epochs $EPOCHS 
    sleep 60
    kill $eneId
    done
  done

date +%s%N | cut -b1-13
