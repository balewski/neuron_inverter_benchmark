#!/usr/bin/env python
""" 
plot energy usage by PM jobs
"""

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

import numpy as np
import  time,os
from pprint import pprint
from toolbox.Plotter_Backbone import Plotter_Backbone
from toolbox.Util_IOfunc import read_one_csv
import matplotlib.ticker
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')


    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='trainScale'
   

    args.formatVenue='prod'
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args



        
#............................
#............................
#............................
class Plotter_TrainScaling(Plotter_Backbone):
    def __init__(self, args):
        Plotter_Backbone.__init__(self,args)

    #...!...!....................
    def epoch_time(self,table_gc,table_pm,figId=5):
        nrow,ncol=1,1
        #  grid is (yN,xN) - y=0 is at the top,  so dumm
        figId=self.smart_append(figId)
        self.plt.figure(figId,facecolor='white', figsize=(5,4))
        ax=self.plt.subplot(nrow,ncol,1)

        nAcc=[]; timeGC=[]; timeGCI=[]
        for rec in table_gc:
            print(rec)
            nAcc.append(int(rec['num_acc']))
            timeGC.append(float(rec['epoch_sec']))
            #timeGCI.append(float(rec['ideal_sec']))

        col='r'
        ax.plot(nAcc,timeGC,"o",c=col,ms=12, mfc='none',label="GC200 IPUs")
        #ax.plot(nAcc,timeGCI,"--",c=col,label="IPUs ideal")

        nAcc=[]; timePM=[]; timePMI=[]
        for rec in table_pm:
            print(rec)
            nAcc.append(int(rec['num_acc']))
            timePM.append(float(rec['epoch_sec']))
            timePMI.append(float(rec['ideal_sec']))
  
        col='b'
        ax.plot(nAcc,timePM,"D-",c=col,ms=7,label="A100  GPUs")
        ax.plot(nAcc,timePMI,"--",c='k',label="ideal scaling")
        
        ax.legend(loc='best')
        ax.set(xlabel='num accelerators',ylabel='time per epoch (sec)')
        ax.set_xscale('log')
        ax.set_yscale('log')
        
        ax.set_xticks([1,4, 16, 64, 256])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
       
        #ax.grid(True)
        return
        

    #...!...!....................
    def val_loss(self,table_gc,table_pm,figId=5):
        nrow,ncol=1,1
        #  grid is (yN,xN) - y=0 is at the top,  so dumm
        figId=self.smart_append(figId)
        self.plt.figure(figId,facecolor='white', figsize=(6,4))
        ax=self.plt.subplot(nrow,ncol,1)

        nAcc=[]; lossGC=[]
        for rec in table_gc:
            print(rec)
            nAcc.append(int(rec['num_acc']))
            lossGC.append(float(rec['val_loss']))
            
        col='r'
        ax.plot(nAcc,lossGC,"o-",c=col,ms=10, mfc='none',label="GC200 IPUs")

        nAcc=[]; lossPM=[]
        for rec in table_pm:
            print(rec)
            nAcc.append(int(rec['num_acc']))
            lossPM.append(float(rec['val_loss']))
  
        col='b'
        ax.plot(nAcc,lossPM,"D-",c=col,ms=7,label="A100  GPUs")
        
        ax.legend(loc='upper left')
        ax.set(xlabel='num accelerators',ylabel='validation loss')
        ax.set_ylim(0,0.05)
        ax.set_xscale('log')

        ax.locator_params(axis='y', nbins=4)
        
        ax.set_xticks([1,4, 16, 64, 256])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
 
        #ax.grid(True)
        return
         
                
         

#=================================
#=================================
#  M A I N 
#=================================
#=================================
if __name__ == '__main__':

    args=get_parser()
    inpF='gc-20220727/gc_train.dat'
    table_gc,label_gc=read_one_csv(inpF,delim='\t')

    inpF='pm-202204/pm_train.dat'
    table_pm,label_pm=read_one_csv(inpF,delim='\t')

    # ----  just plotting 
    plot=Plotter_TrainScaling(args)

    plot.epoch_time(table_gc,table_pm)
    plot.val_loss(table_gc,table_pm)
    plot.display_all('aa',png=0)
