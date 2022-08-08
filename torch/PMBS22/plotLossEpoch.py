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
from toolbox.Plotter_Backbone import Plotter_Backbone
from toolbox.Util_IOfunc import read_one_csv
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("-j", "--jobId",default='G1',choices=['G1','G128','I1','I128'],  help=" job ID")

    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "--smoothWindow", default=10, type=int,help=" smooth the data using a window with requested size (bins)")
    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='lossEpoch'
    args.sourcePath='/global/homes/b/balewski/neuron_inverter_benchmark/torch/PMBS22/'

    if args.jobId=='G1':
        args.tit=['a)', '1 GPU']; args.jobId='G1scan'; args.dataPath=args.sourcePath+'pm-202204/'
    if args.jobId=='G128':
        args.tit=['c)', '128 GPUs']; args.jobId='G128scan'; args.dataPath=args.sourcePath+'pm-202204/'
    if args.jobId=='I1':
        args.tit=['b)', '1 IPU']; args.jobId='1IPU'; args.dataPath=args.sourcePath+'gc-20220727/'

    if args.jobId=='I128':
        args.tit=['d)', '128 IPU']; args.jobId='128IPU'; args.dataPath=args.sourcePath+'gc-20220727/'

   # args.formatVenue='prod'
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args



#............................
#............................
#............................
class Plotter_LossEpoch(Plotter_Backbone):
    def __init__(self, args):
        Plotter_Backbone.__init__(self,args)

    #...!...!....................
    def one_job(self,metaD,tabTrain,tabVal,ax=None,figId=5):        
        if ax==None:
            nrow,ncol=1,1
            #  grid is (yN,xN) - y=0 is at the top,  so dumm
            figId=self.smart_append(figId)
            self.plt.figure(figId,facecolor='white', figsize=(3.5,3))
            ax=self.plt.subplot(nrow,ncol,1)
       
            
        tit='jobId=%s, '%(metaD['name'])

        E=[]; val=[]; col='green'
        for r in tabTrain:
            E.append(float(r['Step']))
            val.append(float(r['Value']))
        ax.plot(E,val,label='train',c=col)

        
        E=[]; val=[]; col='purple'
        for r in tabVal:
            E.append(float(r['Step']))
            val.append(float(r['Value']))

        if 'IPU' in metaD['name'][1]:
            ee=[E.pop()]; E.pop()
            vv=[val.pop()]; val.pop()
            ax.plot(E,val,label='pseudo-val',c=col)
            ax.plot(ee,vv,"o",c=col,ms=9, mfc='none',label='val')
        else:            
            ax.plot(E,val,label='val',c=col)

        
        ax.legend(loc='upper right', title=metaD['name'][1])
        #ax.set(xlabel='epoch',ylabel='loss')#, title=tit)
        if 'GPU' in metaD['name'][1]: ax.set_ylabel('loss')
        if '128' in metaD['name'][1]: ax.set_xlabel('epoch')
        ax.set_ylim(metaD['y0'],metaD['y1'])
        ax.set_xlim(0.1)
        ax.text(0.1,0.94,metaD['name'][0],transform=ax.transAxes)
        ax.locator_params(axis='both', nbins=4)
        #ax.grid(True)
        return
        #if j==0: 
         
                
         

#=================================
#=================================
#  M A I N 
#=================================
#=================================
if __name__ == '__main__':

    args=get_parser()
      
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_val.csv')
    tableVal,_=read_one_csv(inpF)
    inpF=os.path.join(args.dataPath,args.jobId,'NI_Loss_train.csv')
    tableTrain,_=read_one_csv(inpF)
   
    # ----  just plotting 
    plot=Plotter_LossEpoch(args)

    plMD={'name':args.tit,'maxEpoch':150,'y0':0.02,'y1':0.07}
    plot.one_job(plMD,tableTrain,tableVal)
    plot.display_all(args.jobId,png=0)
