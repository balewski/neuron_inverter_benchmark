#!/usr/bin/env python
""" 
plot energy usage by GC job
Jane: went back to use the tool “gc-monitor” to get the power.
"""

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

import numpy as np
import  time
import sys,os
from pprint import pprint
from toolbox.Util_IOfunc import read_one_csv


from scipy import interpolate
from toolbox.Util_Misc import smoothF,mini_plotter

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("--dataName",default="power128",  help="dataName")

    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "--smoothWindow", default=5, type=int,help=" smooth the data using a window with requested size (bins)")
    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='eneGC'
   
    args.sourcePath='gc-20220727/'
 
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args


#...!...!....................
def plot_one_job(plot,table,args):
        nrow,ncol=1,1
        plt.figure(1,facecolor='white', figsize=(10,6))
        ax=plt.subplot(nrow,ncol,1)

        tit=args.dataName+', per M2000'

        T=[];P=[]
        for r in table:
            print(r)
            T.append(float(r['time_sec'])/60.)
            P.append(float(r['power_W'])/32. )
            
        P=np.array(P)
        if args.smoothWindow>0: P=smoothF(P,args.smoothWindow)
        
        ax.plot(T,P,'*-')

        ax.legend(loc='best')#, title='total used energy: (Wh)')
        ax.set(xlabel='wall time (min)',ylabel='power (W)', title=tit)
        ax.grid(True)
        ax.set_ylim(0,)
         

#=================================
#=================================
#  M A I N 
#=================================
#=================================
if __name__ == '__main__':
    args=get_parser()

    inpF=args.sourcePath+'%s.csv'%args.dataName
    table,_=read_one_csv(inpF,delim=',')
    

    plt=mini_plotter(args)

    plot_one_job(plt,table,args)
    outF='out/'+args.dataName+'.png'
    plt.savefig(outF)
    print('saved:',outF)
    plt.show()

