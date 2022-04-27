ga=2
lr=0.002
for r in 4 #2 4
  do
  for i in `seq 0 2`
    do
      bash ./run-pod16.sh $r 1 $lr $ga 2>&1 | tee r"$r"_v"$i".log
    done
  done

for r in 8 16
  do
  instances=$((r/4))
  for i in `seq 0 2`
    do
      bash ./run-pod16.sh $r $instances $lr $ga 2>&1 | tee r"$r"_v"$i".log
    done
  done
