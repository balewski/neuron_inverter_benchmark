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
from toolbox.Util_Misc import  smoothF
from toolbox.Util_IOfunc import write_yaml

from plotEnergyPM import ana_one_job as ana_one_job_pm
from plotEnergyGC import ana_one_job as ana_one_job_gc

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("--numAcc",default=32)

    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "--smoothWindow", default=10, type=int,help=" smooth the data using a window with requested size (bins)")
    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='eneUse'
    args.sourcePathPM='/global/homes/b/balewski/prjs/SC2022-neuron-inverter/ref-jobs-for-GC/april_GCpaper'
    args.sourcePathGC='gc-20220727/'

    args.formatVenue='prod'
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args


def find_index_range(T,tV):
    [t1,t2]=tV
    idxAr = np.argwhere(T>=t1)
    i1=int(idxAr[0])
    print('FIR',t1, i1, T[i1])
    idxAr = np.argwhere(T>=t2)
    i2=int(idxAr[0])
    print('FIR',t2, i2, T[i1])
    return i1,i2

#............................
#............................
#............................
class Plotter_EnergyComp(Plotter_Backbone):
    def __init__(self, args):
        Plotter_Backbone.__init__(self,args)
        self.args=args

    #...!...!....................
    def one_job(self,metaD,bigD,bigD_gc,wallTR,figId=5):
        nrow,ncol=1,1
        #  grid is (yN,xN) - y=0 is at the top,  so dumm
        figId=self.smart_append(figId)
        self.plt.figure(figId,facecolor='white', figsize=(5,4))
        ax=self.plt.subplot(nrow,ncol,1)

        #tit='jobId=%s, node=%s'%(metaD['jobId'],metaD['hostname'])
        Tpm=bigD['time']/60.
        Epm=np.array(bigD['power']['4gpu_ene_J'])/4.

        col='b'
        ax.plot(Tpm,Epm,c=col)
        
        i1,i2=find_index_range(Tpm,wallTR['PM'])
        print(type(Tpm),type(Epm))
        print(Tpm[i1:i2].shape,Epm.shape)
        ax.fill_between(Tpm[i1:i2],Epm[i1:i2], facecolor="none", hatch="\\\\", edgecolor=col, linewidth=0.0,label='GPU')
        

        ipu=bigD_gc['M2000']
        Tgc=[];Egc=[]
        for t in sorted(ipu):
            Tgc.append(t/60.)
            Egc.append(ipu[t])

        Tgc=np.array(Tgc)
        Egc=np.array(Egc)/4.
        if self.args.smoothWindow>0: Egc=smoothF(Egc,args.smoothWindow)

        col='r'
        ax.plot(Tgc,Egc,c=col)
        i1,i2=find_index_range(Tgc,wallTR['GC'])
        ax.fill_between(Tgc[i1:i2],Egc[i1:i2], facecolor="none", hatch="//", edgecolor=col, linewidth=0.0,label='IPU')
        
        ax.legend(loc='best', title='train pass')
        ax.set(xlabel='wall time (min)',ylabel='used power (W/accelerator)')#, title=tit)
        #ax.grid(True)
        ax.set_xlim(0,15)
        ax.set_ylim(0,)

        # Setting the number of ticks
        ax.locator_params(axis='both', nbins=4)
        txt='%d acceletarors'%args.numAcc
        ax.text(0.04,0.95,txt,color='k',transform=ax.transAxes,fontsize=12)
        return
        
         
                
         

#=================================
#=================================
#  M A I N 
#=================================
#=================================
args=get_parser()

if args.numAcc==32:
    wallTR={'PM':[2.7,11.8], 'GC':[2.7,14]} # train time ranges

#..........  GC
args.dataName='pod%d-energy'%args.numAcc
inpF_gc=args.sourcePathGC+'%s.log'%args.dataName
table_gc,_=read_one_csv(inpF_gc,delim='|')
jobD_gc=ana_one_job_gc(table_gc,args)

#............. PM
jobId_pm='G%dscan'%args.numAcc
inpF_pm=os.path.join(args.sourcePathPM,jobId_pm,'lr.002','log.energy.csv')
table_pm,label_pm=read_one_csv(inpF_pm)
metaD_pm,bigD_pm=ana_one_job_pm(jobId_pm,table_pm,args)


# ----  just plotting 
plot=Plotter_EnergyComp(args)

plot.one_job(metaD_pm,bigD_pm,jobD_gc,wallTR)
plot.display_all('aa')
