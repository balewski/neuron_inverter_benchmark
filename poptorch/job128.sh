#sbatch -N 4 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.0002  -t 9:0:0
#sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.0005  -t 9:0:0
sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.001 15 -t 9:0:0
sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.002 15 -t 9:0:0
sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.002 15 -t 9:0:0
sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.002 15 -t 9:0:0
sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.005 15 -t 9:0:0
sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.01  15 -t 9:0:0
#sbatch -N 8 -p pod128 --ntasks-per-node=16 --exclusive ./test-slurm.sh 128 0.02  -t 9:0:0
