ga=10
for lr in 0.005
  do
  for i in `seq 0 0`
    do 
      bash ./run-pod16.sh 8 $lr $ga
    done
  done
