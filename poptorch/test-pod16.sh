ga=3
lr=0.002
reb=32
for r in 2 4 8 16
  do
  for i in `seq 0 0`
    do
      bash ./run-pod16.sh $r $r $lr $ga $reb 2>&1 | tee r"$r"_v"$i"_ga"$ga"_reb"$reb".log
    done
  done
