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
#from Plotter_Backbone import Plotter_Backbone
#sys.path.append(os.path.abspath("../toolbox"))
from toolbox.Util_IOfunc import read_one_csv


from scipy import interpolate
from toolbox.Util_Misc import smoothF,mini_plotter

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("--dataName",default="pod16-energy",  help="dataName")

    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "--smoothWindow", default=20, type=int,help=" smooth the data using a window with requested size (bins)")
    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='eneGC'
   
    args.sourcePath='gc-20220727/'
 
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args

#...!...!....................
def ts_to_sec(x):
    x=x[:-1]
    t0=0
    if 'h' in x:
        xL=x.split('h')
        t0=3600.* int(xL[0])
        x=xL[1]
        
    
    xL=x.split('m')
    #print('tt',xL)
    if len(xL)==2:
        t=int(xL[0])*60.+int(xL[1])
    else:
        t=int(xL[0])
    return t+t0

#...!...!....................
def ps_to_w(x):
    xL=x.split(' ')
    #print('pp',xL)
    return float(xL[0])


#...!...!....................
def ana_one_job(table,args):
    if 'pod4' in  args.dataName:
        args.validIpuIDs=['0']

    if 'pod8' in  args.dataName:
        args.validIpuIDs=['0','4']

    if '16' in  args.dataName:
        args.validIpuIDs=['16','20','24','28']

    if '32' in  args.dataName:
        args.validIpuIDs=['32','36','40','44']

    if '64' in  args.dataName:
        args.validIpuIDs=['0','4','8','12']

    # steps: average power per time step, append time+average to the list
    ipuD={ x:{} for x in  args.validIpuIDs }
    for rec in table:
        #print('rec',rec)
        ipuId=rec['E'].strip()
        if ipuId not in ipuD: continue
        tS=rec['C'].strip()
        #print('=%s='%tS)        
        t=ts_to_sec(tS)
        pS=rec['I'].strip()
        #print('pp',pS)
        assert  len(pS)>0
        pw=ps_to_w(pS)
        ipuD[ipuId][t]=pw
        
    #... agreagte power over 4 IPUs
    yD={}
    for ipu in  args.validIpuIDs:    
        for t in ipuD[ipu]:
            if t not in yD: yD[t]=[]
            yD[t].append(ipuD[ipu][t])

    # .... sum power over IPUs, with re-weighting if data was missing
    ipuD['M2000']={}
    Nipu=len(args.validIpuIDs)
    for t in yD:
        ps=np.mean(yD[t])
        #print(t,ni,ps)
        ipuD['M2000'][t]=ps
        #assert ni==4
    return ipuD


#...!...!....................
def plot_one_job(plot,ipuD,args):
        nrow,ncol=1,1
        plt.figure(1,facecolor='white', figsize=(10,6))
        ax=plt.subplot(nrow,ncol,1)

        tit=args.dataName
        ic=0
        for myId in ['M2000']+ args.validIpuIDs:
            ipu=ipuD[myId]
            T=[];P=[]; ic+=1
            for t in sorted(ipu):
                T.append(t/60.)
                P.append(ipu[t])

            P=np.array(P)
            if args.smoothWindow>0: P=smoothF(P,args.smoothWindow)
        
            dLab=myId
            if ic==1:
                cc='k'
                lw=3.
            else:
                lw=1.
                cc='C%d'%ic
            ax.plot(T,P,label=dLab,c=cc,lw=lw)

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

    inpF=args.sourcePath+'%s.log'%args.dataName
    table,_=read_one_csv(inpF,delim='|')
    jobD=ana_one_job(table,args)

    plt=mini_plotter(args)

    plot_one_job(plt,jobD,args)
    outF=args.dataName+'.png'
    plt.savefig(outF)
    print('saved:',outF)
    plt.show()

