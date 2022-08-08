#!/usr/bin/env python
""" 
plot energy scaling for GC & PM
"""

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

import numpy as np
import  time
import sys,os
from pprint import pprint
import matplotlib.ticker

from toolbox.Util_Misc import smoothF,mini_plotter

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='eneScale'
    
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args


#...!...!....................
def plot_ene_scale( gce, pme):
        nrow,ncol=1,1
        plt.figure(1,facecolor='white', figsize=(5,4))
        ax=plt.subplot(nrow,ncol,1)

        col='b'
        ax.plot(pme[:,0], pme[:,1],"D-",c=col,ms=7,label="GPUs")

        col='r'
        print(gce.shape)  # 
        ax.plot(gce[:,0], gce[:,1],"o-",c=col,ms=10, mfc='none',label="IPUs")

        ax.set_xscale('log')
        ax.legend(loc='best')
        ax.set(xlabel='num accelerators',ylabel='used energy (Wh/epoch)')
        # Setting the number of ticks
        #plt.locator_params(axis='both', nbins=4)

        ax.set_xticks([4, 16, 64, 128])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        #ax.grid(True)
        ax.set_ylim(0,8)
         

#=================================
#=================================
#  M A I N 
#=================================
#=================================
if __name__ == '__main__':
    args=get_parser()
    # GC: https://docs.google.com/spreadsheets/d/1sOJwBkggUG6kJJHHF28A0I8cu25iW-al8aZrTiwAqgg/edit?usp=sharing
    
    gc_ene= np.array([ [4,1.90], [8, 1.93], [16,2.22], [32,2.03], [64,2.16], [128, 2.61]])

    # PM: https://docs.google.com/spreadsheets/d/1KmXtGCThlef10CrRzuKhJ1CbDJ_SMC7wej5c0fHGI4w/edit?usp=sharing 
    pm_ene= np.array([ [4,4.98], [8,5.02], [16,5.37] , [32,5.55], [64,6.08], [128,6.75]])
    plt=mini_plotter(args)

    plot_ene_scale(gc_ene,pm_ene)
    outF='out/eneScale.pdf'
    plt.tight_layout()
    plt.savefig(outF)
    print('saved:',outF)
    plt.show()

