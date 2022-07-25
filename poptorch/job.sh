# This is a complete list of slurm jobs,
# for 1, 2, 4, 8, 16, 32, 64, 128 and 256 IPUs.
for i in 1 2 4 8 16
  do
    sbatch -N 1 -p sub64 --exclusive ./test-pod.sh $i 0.0002  -t 9:0:0
    sbatch -N 1 -p sub64 --exclusive ./test-pod.sh $i 0.0005  -t 9:0:0
    sbatch -N 1 -p sub64 --exclusive ./test-pod.sh $i 0.001  -t 9:0:0
    sbatch -N 1 -p sub64 --exclusive ./test-pod.sh $i 0.002  -t 9:0:0
    sbatch -N 1 -p sub64 --exclusive ./test-pod.sh $i 0.005  -t 9:0:0
  done

for i in 32 64
  do
    sbatch -N 4 -p pod64 --ntasks-per-node=16 --exclusive ./test-pod.sh $i 0.0005  -t 9:0:0
    sbatch -N 4 -p pod64 --ntasks-per-node=16 --exclusive ./test-pod.sh $i 0.001  -t 9:0:0
    sbatch -N 4 -p pod64 --ntasks-per-node=16 --exclusive ./test-pod.sh $i 0.002  -t 9:0:0
    sbatch -N 4 -p pod64 --ntasks-per-node=16 --exclusive ./test-pod.sh $i 0.005  -t 9:0:0
    sbatch -N 4 -p pod64 --ntasks-per-node=16 --exclusive ./test-pod.sh $i 0.01  -t 9:0:0
  done

  # 128 IPUs
sbatch -N 4 -p pod128 --ntasks-per-node=16 --exclusive ./test-pod.sh 128 0.0005  -t 9:0:0
sbatch -N 4 -p pod128 --ntasks-per-node=16 --exclusive ./test-pod.sh 128 0.001  -t 9:0:0
sbatch -N 4 -p pod128 --ntasks-per-node=16 --exclusive ./test-pod.sh 128 0.002  -t 9:0:0
sbatch -N 4 -p pod128 --ntasks-per-node=16 --exclusive ./test-pod.sh 128 0.005  -t 9:0:0
sbatch -N 4 -p pod128 --ntasks-per-node=16 --exclusive ./test-pod.sh 128 0.01  -t 9:0:0

# 256 IPUs
sbatch -N 16 -p pod256 --ntasks-per-node=16 --exclusive ./test-pod.sh 256 0.0005  -t 9:0:0
sbatch -N 16 -p pod256 --ntasks-per-node=16 --exclusive ./test-pod.sh 256 0.001  -t 9:0:0
sbatch -N 16 -p pod256 --ntasks-per-node=16 --exclusive ./test-pod.sh 256 0.002  -t 9:0:0
sbatch -N 16 -p pod256 --ntasks-per-node=16 --exclusive ./test-pod.sh 256 0.005  -t 9:0:0
sbatch -N 16 -p pod256 --ntasks-per-node=16 --exclusive ./test-pod.sh 256 0.01  -t 9:0:0
