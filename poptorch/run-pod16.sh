# This script is for a POD16 with a single host.
# To run it using 1 replica 1 instance:
#   bash run-pod16.sh 1 0.005 10
# Or any number of replicas, up to 16, for example,
#   bash run-pod16.sh 4 0.005 5
# Please modify the data path and your output path if you don't use /localdata.

export POPLAR_RUNTIME_OPTIONS='{"streamCallbacks.maxLookahead" : "unlimited"}'
export POPTORCH_CACHE_DIR=/localdata/$USER/exec_cache
TEMP_DIR=/localdata/$USER/my_temp
mkdir -p $TEMP_DIR
export TEMPDIR=$TEMP_DIR
export TMPDIR=$TEMP_DIR
export TEMP=$TEMP_DIR
export TMP=$TEMP_DIR

REPLICAS=$1

# Please modify this data path on your system.
# It needs to be either shared by multiple hosts,
# or copied to the local folders of hosts.

DATA_PATH=/localdata/$USER/neuron-data/

LEARNING_RATE=$2
GRADIENT_ACCUMULATION=$3
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

poprun -vv --mpi-global-args='--tag-output --allow-run-as-root ' --mpi-local-args=' -x OPAL_PREFIX -x LD_LIBRARY_PATH -x PATH -x PYTHONPATH -x IPUOF_VIPU_API_TIMEOUT=600 -x POPLAR_RUNTIME_OPTIONS -x POPTORCH_CACHE_DIR -x TEMPDIR -x TMPDIR -x TEMP -x TMP' --ipus-per-replica 1 --numa-aware 1 --num-instances $REPLICAS --num-replicas $REPLICAS ./train_replica.py --design common --cellName witness13c_fp16 --outPath /localdata/$USER/ga"$GA"/r"$REPLICAS"_lr"$LEARNING_RATE"/"$TIMESTAMP" --initLR $LEARNING_RATE --gradientAcc $GRADIENT_ACCUMULATION
#--epochs 1
