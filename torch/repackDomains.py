#!/usr/bin/env python3
'''
 change Domain split

'''
import os
import numpy as np
from toolbox.Util_H5io3 import  read3_data_hdf5, write3_data_hdf5
dataPath='/global/cfs/cdirs/m2043/www/tryML/'
inpN='witness2c_fp16_excite.cellSpike_4prB8kHz.data.h5' 
inpF=os.path.join(dataPath,inpN)
bigD,predMD=read3_data_hdf5(inpF)

delta=100000  # number of samples moved from 'test' to 'val'
for obs in ['frames','unitStar_par']:
    A=bigD['val_'+obs]
    B=bigD['test_'+obs]
    print(obs,'before A:',A.shape,'B:',B.shape)
    C=np.concatenate((A,B[:delta]))
    D=B[delta:]
    print('   after C:',C.shape,'D:',D.shape)
    bigD['val_'+obs]=C
    bigD['test_'+obs]=D
    
    
outN='witness2c_fp16b_excite.cellSpike_4prB8kHz.data.h5' 
outF=os.path.join(dataPath,outN)
write3_data_hdf5(bigD,outF,metaD=predMD)
