#!/usr/bin/env python3
""" 
read data file and convert all np arrays from fp32 to fp16

It requires high mem node, all is done in memory
Name change from:
witness17c_8inhib.cellSpike_3prB8kHz.data.h5
to
witness17c_fp16_8inhib.cellSpike_3prB8kHz.data.h5
It retains the template:
# h5nameTemplate: '*_8inhib.cellSpike_3prB8kHz.data.h5'

Use case:  ./pack32fp16.py --dataName october12c


"""

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

import numpy as np

import  time
import sys,os
from toolbox.Util_H5io3  import write3_data_hdf5, read3_data_hdf5
from pprint import pprint
import argparse

#...!...!..................
def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataPath",
                        #default='/global/cfs/cdirs/m2043/balewski/neuronBBP-pack8kHzRam/probe_3prB8kHz/ontra3/etype_8inhib_v1' # inhibitory on Cori
                        #default='/global/cfs/cdirs/m2043/balewski/neuronBBP-pack8kHzRam/probe_4prB8kHz/ontra4/etype_excite_v1'  # excitatory on Cori
                        default='/global/cfs/cdirs/m2043/balewski/neuronBBP2-pack8kHzRam/probe_4prB8kHz/ontra4' # excitatory BBP2
                        ,help='input data path')
                        
    parser.add_argument("--outPath", default='/global/homes/b/balewski/prjs/tm3p_neurInv',help="output path for plots and tables")
 
  
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2], help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("--dataName", type=str, default='witness17c', help="alternative cell shortName ")
    args = parser.parse_args()
    #args.nameSufix='8inhib.cellSpike_3prB8kHz.data.h5' # inhibitory on Cori
    args.nameSufix='excite.cellSpike_4prB8kHz.data.h5' # excitatory on Cori

    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args


#=================================
#=================================
#  M A I N 
#=================================
#=================================
if __name__ == '__main__':
  args=get_parser()
  inpF='%s_%s'%(args.dataName,args.nameSufix)
  inpF=os.path.join(args.dataPath,inpF)
  t1=time.time()
  blob,metaD=read3_data_hdf5(inpF)
  t2=time.time()
  rT=t2-t1
  print('M: read time=%.1f min'%(rT/60.))
  pprint(metaD)

  # repacking .....
  for x in blob:
      blob[x]=blob[x].astype('float16')
      print('converted ',x,time.time()-t2)
  t3=time.time()
  cT=t3-t2
  print('M:  convert time=%.1f min'%(cT/60.))
  metaD['dataPrecision']='fp16'

  # writing output
  outF='%s_fp16_%s'%(args.dataName,args.nameSufix)
  outF=os.path.join(args.outPath,outF)
  write3_data_hdf5(blob,outF,metaD=metaD)

  t4=time.time()
  rT=t4-t3
  print('M: write time=%.1f min'%(rT/60.))
