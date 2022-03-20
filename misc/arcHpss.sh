#!/bin/bash
set -u ;  # exit  if you try to use an uninitialized variable
#set -x ;  # print out the statements as they are being executed
set -e ;  #  bash exits if any statement returns a non-true return value
#set -o errexit ;  # exit if any statement returns a non-true return value
# Single line execution: hsi "mkdir foo, cd foo, put data_file"

# inhibitory
inpPath=/global/cfs/cdirs/m2043/balewski/neuronBBP-pack8kHzRam/probe_3prB8kHz/ontra3/etype_8inhib_v1/
hsiPath=neuronBBP-pack8kHzRam/probe_3prB8kHz/ontra3/etype_8inhib_v1/

# excitatory
inpPath=/global/cfs/cdirs/m2043/balewski/neuronBBP-pack8kHzRam/probe_4prB8kHz/ontra4/etype_excite_v1
hsiPath=neuronBBP-pack8kHzRam/probe_4prB8kHz/ontra4/etype_excite_v1

exit

k=0
cd ${inpPath}
inpF=${inpPath}/all.txt
while IFS= read -r line
do
    k=$[ ${k} + 1 ]
    echo "$k $line"
    
    time hsi " cd ${hsiPath}; put $line "
    #break
done < "$inpF"
cd -
