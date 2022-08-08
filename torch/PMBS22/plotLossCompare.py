#!/usr/bin/env python
""" 
plot  loss-vs-epoch using TB output data
Works for both PM & GC

"""

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

import numpy as np
import  time,os
from pprint import pprint
from plotLossEpoch import get_parser, read_one_csv, Plotter_LossEpoch


#=================================
#=================================
#  M A I N 
#=================================
#=================================
if __name__ == '__main__':

    args=get_parser()

    args.tit=['a)' ,'1 GPU']; args.jobId='G1scan'; args.dataPath=args.sourcePath+'pm-202204/'
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_val.csv')
    tableVal,_=read_one_csv(inpF)
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_train.csv')
    tableTrain,_=read_one_csv(inpF)
   
    # ----  just plotting 
    plot=Plotter_LossEpoch(args)
    axs=plot.blank_share2D(figsize=(5,6.5),figId=22)
    
    plMD={'name':args.tit,'maxEpoch':150,'y0':0.02,'y1':0.07}
    plot.one_job(plMD,tableTrain,tableVal,ax=axs[0,0])


    
    # G128
    args.tit=['c)', '128 GPUs']; args.jobId='G128scan'; args.dataPath=args.sourcePath+'pm-202204/'
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_val.csv')
    tableVal,_=read_one_csv(inpF)
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_train.csv')
    tableTrain,_=read_one_csv(inpF)
   
    plMD['name']=args.tit
    plot.one_job(plMD,tableTrain,tableVal,ax=axs[1,0])


    
    # 1 IPU5
    args.tit=['b)', '1 IPU']; args.jobId='1IPU'; args.dataPath=args.sourcePath+'gc-20220727/'
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_val.csv')
    tableVal,_=read_one_csv(inpF)
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_train.csv')
    tableTrain,_=read_one_csv(inpF)
    plMD['name']=args.tit
    plot.one_job(plMD,tableTrain,tableVal,ax=axs[0,1])

    #128 IPUS
    args.tit=['d)', '128 IPUs']; args.jobId='128IPU'; args.dataPath=args.sourcePath+'gc-20220727/'
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_val.csv')
    tableVal,_=read_one_csv(inpF)
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_train.csv')
    tableTrain,_=read_one_csv(inpF)
    plMD['name']=args.tit
    plot.one_job(plMD,tableTrain,tableVal,ax=axs[1,1])

    
    plot.display_all(args.jobId,png=0) 
