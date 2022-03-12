#!/usr/bin/env python
""" 
Neuron-inverter  weak scaling at different facilities
"""

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

import numpy as np
import  time
import argparse
import sys,os

from toolbox.Plotter_Backbone import Plotter_Backbone
from toolbox.Util_IOfunc import read_one_csv

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2], help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("-d", "--dataPath", default='scaling-2021-09/',help="input path for data")
    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")
 
    parser.add_argument( "-X","--noXterm", dest='noXterm', action='store_true', default=False,help="disable X-term for batch mode")

    args = parser.parse_args()
    args.prjName='weakScale'
    args.formatVenue='prod'
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args

#............................
#............................
#............................
class Plotter_Design(Plotter_Backbone):
    def __init__(self, args):
        Plotter_Backbone.__init__(self,args)
        
#...!...!..................
    def weakScaleAbs(self,scalData,figId=1):
        nrow,ncol=1,1
        #  grid is (yN,xN) - y=0 is at the top,  so dumm
        self.figL.append(figId)
        self.plt.figure(figId,facecolor='white', figsize=(6,6))

        ax=self.plt.subplot(nrow,ncol,1)
        tit='Weak scaling, Neuron-Inverter,  ver=21-09-7'
        for  faciN in faciL:
            data=scalData[faciN]
            xV=data[:,0]; yV=data[:,1]
            idV=yV[0]/xV  # ideal scaling
            infoL=faciD[faciN]
            [hcol,hmar]=infoL[1:3]
            hlab='%s, %s'%(faciN,infoL[0]) 
            ax.plot(xV,yV, color=hcol,marker=hmar,label=hlab)
            ax.plot(xV,idV, color=hcol,linestyle ='--',linewidth=0.7,label=' ideal')
        ax.grid(True)
        ax.set_xscale('log')
        ax.set_yscale('log')
        #ax.set_ylim(0,)
        ax.set(xlabel='num accelerators',ylabel='one epoch time (sec)',title=tit)
        ax.legend(loc='best', title='Facility')
        ax.text(0.2,0.2,'(smaller is better)',transform=ax.transAxes)
        
#...!...!..................
    def weakScaleNorm(self,scalData,figId=1):
        nrow,ncol=1,1
        #  grid is (yN,xN) - y=0 is at the top,  so dumm
        self.figL.append(figId)
        self.plt.figure(figId,facecolor='white', figsize=(6,6))

        ax=self.plt.subplot(nrow,ncol,1)
        tit='Weak scaling, Neuron-Inverter ver=21-09-7'
        for  faciN in faciL:
            data=scalData[faciN]
            xV=data[:,0]; yV=data[:,1]*xV
            ideY=yV[0]  # ideal scaling
            infoL=faciD[faciN]
            [hcol,hmar]=infoL[1:3]
            hlab='%s, %s'%(faciN,infoL[0]) 
            ax.plot(xV,yV, color=hcol,marker=hmar,label=hlab)
            #ax.plot(xV,idV, color=hcol,linestyle ='--',linewidth=0.7,label=' ideal')
            ax.axhline(ideY, color=hcol,linestyle ='--',linewidth=0.7,label=' ideal')
        ax.grid(True)
        ax.set_xscale('log')
        #ax.set_yscale('log')
        ax.set_ylim(0,)
        ax.set(xlabel='num accelerators',ylabel='num_GPU * epoch_time (sec*GPU)',title=tit)
        ax.legend(loc='best', title='Computing System')
        ax.text(0.1,0.05,'(smaller is better)',transform=ax.transAxes)
        
#...!...!..................
def readTable(faciN):
    inpF=args.dataPath+"neur-inv_scaling3.%s.csv"%faciN
    tabL,keyL=read_one_csv(inpF)

    infoL=faciD[faciN]
    kL=[ infoL[0],'epoch time(sec)']

    xyL=[]
    for row in tabL:
        #print( row[kL[0]])
        xy=[ float(row[k]) for k in kL] 
        xyL.append(xy)
    return np.array(xyL)



#=================================
#=================================
#  M A I N 
#=================================
#=================================
args=get_parser()
faciL=["Summit","CoriGpu","Perlmutter","Graphcore"]

#faciL=["Perlmutter","Graphcore"]  # for Kris, 2022-03-11

# all collected data
faciD={"A100":['GPU','C3','o'],"Perlmutter":['GPU A100','C3','o'],"Summit": ['GPU V100','C2','^'],"CoriGpu": ['GPU V100','C0','x'],"Graphcore": ['IPU','C4','D']}



scalData={}
for faciN in faciL:
    scalData[faciN]=readTable(faciN)
    #print(scalData[faciN])
    
plot=Plotter_Design(args)

plot.weakScaleAbs(scalData,figId=10)
plot.weakScaleNorm(scalData,figId=11)

plot.display_all()  
