#sbatch -N 1 -p sub64 --exclusive ./test-slurm.sh $1 0.0002  -t 9:0:0
sbatch -N 1 -p sub64 --exclusive ./test-slurm.sh 8 0.001 15 -t 9:0:0
sbatch -N 1 -p sub64 --exclusive ./test-slurm.sh 4 0.001 15 -t 9:0:0
sbatch -N 1 -p sub64 --exclusive ./test-slurm.sh 2 0.0005 15 -t 9:0:0
#sbatch -N 1 -p sub64 --exclusive ./test-slurm.sh $1 0.002 15 -t 9:0:0
#sbatch -N 1 -p sub64 --exclusive ./test-slurm.sh $1 0.005 15 -t 9:0:0
