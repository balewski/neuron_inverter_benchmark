# This is the script to be called by test.sh
# good for 1 to 256 IPUs using a single host or multiple hosts
if [[ "$#" -gt 11 ||  "$#" == 0 ]]
then
    echo "Usage: $0 NUM_REPLICAS HOSTS PARTITION SERVER NETMASK LR GRAD_ACC NUM_DATA_WORKERS IOT"
    exit 1
fi
# Please modify the data path and your output path if you don't use /localdata.

export POPLAR_RUNTIME_OPTIONS='{"streamCallbacks.maxLookahead":"unlimited"}'
REPLICAS=$1
INSTANCES=$2
PARTITION=$3
VIPU_SERVER_HOST=$4
NETMASK=$5
TEMP_DIR="/localdata/$USER/my_temp/"
export TEMPDIR=$TEMP_DIR
export TMPDIR=$TEMP_DIR
export TEMP=$TEMP_DIR
export TMP=$TEMP_DIR

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# below learning rate and gradient accumulation count are used for tuning validation
LEARNING_RATE=$6
NUM_DATA_WORKERS=$7
#IOT=$8
GRADIENT_ACCUMULATION=$8

#CELLNAME=witness2c_fp16b
CELLNAME=witness13c_fp16
DESIGN=large

HOSTS=1
SLURM_NTASKS_PER_NODE=16
if [[ $REPLICAS -lt 16 ]]
then
    SLURM_NTASKS_PER_NODE=$REPLICAS
else
    HOSTS=$((REPLICAS/16))
fi

HOSTS=$(./hostselect.sh $HOSTS)

echo "++++++++++++++ hosts to be used in poprun: $HOSTS +++++++++"

export POPTORCH_CACHE_DIR=/localdata/$USER/exec_cache

MPI_SETTINGS="--mpi-global-args='--tag-output --allow-run-as-root --mca oob_tcp_if_include "$NETMASK" --mca btl_tcp_if_include "$NETMASK" --npernode "$SLURM_NTASKS_PER_NODE" ' \
	--mpi-local-args=' -x OPAL_PREFIX -x LD_LIBRARY_PATH -x PATH -x PYTHONPATH -x IPUOF_VIPU_API_TIMEOUT=600 -x POPLAR_RUNTIME_OPTIONS -x POPTORCH_CACHE_DIR -x TEMPDIR -x TMPDIR -x TEMP -x TMP --npernode "$SLURM_NTASKS_PER_NODE" ' \
    --update-partition=yes --reset-partition=no --vipu-server-timeout 600 \
    --ipus-per-replica 1 --numa-aware 1 --vipu-server-host "$VIPU_SERVER_HOST" \
    --vipu-partition="$PARTITION" --sync-type ST_POD_NATIVE_DEFAULT "

#below is the command line for training. To enable validation, please add --validation
TRAIN=" poprun \
        -vv $MPI_SETTINGS \
        --num-replicas $REPLICAS --num-instances $INSTANCES \
        --executable-cache-path=/localdata/$USER/exec_cache \
        python ./train_replica.py --design $DESIGN \
        --cellName $CELLNAME --outPath /localdata/$USER/ga"$GRADIENT_ACCUMULATION"/r"$REPLICAS"_lr"$LEARNING_RATE"/"$TIMESTAMP" \
	--gradientAcc "$GRADIENT_ACCUMULATION" \
        --initLR "$LEARNING_RATE" --numDataWorkers "$NUM_DATA_WORKERS" "

#	--host $HOSTS \
echo $TRAIN
eval $TRAIN 
