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
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbosity",type=int,choices=[0, 1, 2],help="increase output verbosity", default=1, dest='verb')

    parser.add_argument("-j", "--jobId",default='65244',  help=" job ID")
    parser.add_argument("--tag",default=None,  help=" extra string in the path")

    parser.add_argument("-o", "--outPath", default='out/',help="output path for plots and tables")

    parser.add_argument( "--smoothWindow", default=10, type=int,help=" smooth the data using a window with requested size (bins)")
    parser.add_argument( "-X","--noXterm", dest='noXterm',  action='store_true', default=False, help="disable X-term for batch mode")


    args = parser.parse_args()
    args.prjName='eneUse'

    #PM
    
    args.sourcePath='/pscratch/sd/b/balewski/tmp_digitalMind/neuInv/benchmark/marchSC22/' #G16ene/ep100/'
    #args.sourcePath='pm-ene-data-2021-09-19'
    args.formatVenue='prod'
    for arg in vars(args):  print( 'myArg:',arg, getattr(args, arg))
    return args


#...!...!....................
def ana_one_job(jobId,table):
    tL=[]; eL={'node_ene_J':[],'cpu_ene_J':[],'memory_ene_J':[]}
    for k in range(4): eL['gpu%d_ene_J'%k]=[]
    for rec in table:
        #print('rec',rec)
        t=float(rec['unix_millisec'])/1000.
        tL.append(t)
        for x in eL: eL[x].append( float(rec[x]))
        #print('t',t,'eL',eL)
    
    N=len(tL)
    eL['4gpu_ene_J']=[]
    # sume GPU energy
    nG=4
    for i in range(N):
        sum=0
        for k in range(nG):  sum+=eL['gpu%d_ene_J'%k][i]
        eL['4gpu_ene_J'].append(sum) # at guven time
        
    #... convert list to NP arrays
    for x in eL: eL[x]=np.array(eL[x])
    
    if args.smoothWindow>0:
        for x in eL: eL[x]=smoothF(eL[x],args.smoothWindow)
        
    #..... convert energy to power
    tL=np.array(tL)
    tL-=tL[0]
    
    pL={x:[0] for x in eL}
    for i in range(1,N):
        dt=tL[i]-tL[i-1]
        #print(i,dt)
        for x in eL: pL[x].append( (eL[x][i]- eL[x][i-1])/dt)

    eT={}
    for x in eL:
        eT[x]= float(eL[x][-1]- eL[x][0])
    elaT=tL[-1]-tL[0]
    eT['avr_gpu_ene_J']=eT['4gpu_ene_J']/nG
    metaD={'elaT':float(elaT),'tot_ene':eT,'jobId':jobId,'hostname':rec['hostname']}
    pprint(metaD)
    bigD={}
    bigD['power']=pL
    bigD['time']=tL
    return metaD,bigD
        
#............................
#............................
#............................
class Plotter_EnergyUse(Plotter_Backbone):
    def __init__(self, args):
        Plotter_Backbone.__init__(self,args)

    #...!...!....................
    def one_job(self,metaD,bigD,figId=5):
        nrow,ncol=1,1
        #  grid is (yN,xN) - y=0 is at the top,  so dumm
        figId=self.smart_append(figId)
        self.plt.figure(figId,facecolor='white', figsize=(10,6))
        ax=self.plt.subplot(nrow,ncol,1)

        tit='jobId=%s, node=%s'%(metaD['jobId'],metaD['hostname'])
        T=bigD['time']
        
        for name in bigD['power']:
            Y=bigD['power'][name]
            ene=metaD['tot_ene'][name] /3600.
            dLab='%s: %.1f'%(name[:-2],ene)
            #print(T,Y)
            ax.plot(T,Y,label=dLab)
           
        ax.legend(loc='best', title='total used energy: (Wh)')
        ax.set(xlabel='wall time (sec)',ylabel='power (W)', title=tit)
        ax.grid(True)
        return
        #if j==0: ax.text(0.1,0.85,'n=%d'%len(lossV),transform=ax.transAxes)
         
                
         

#=================================
#=================================
#  M A I N 
#=================================
#=================================
args=get_parser()

stockD={}
jobId=args.jobId
inpF=os.path.join(args.sourcePath,args.tag,'log.energy_%s.csv'%(jobId))
table,label=read_one_csv(inpF)
metaD,bigD=ana_one_job(jobId,table)

if args.tag==None:
    outF=os.path.join(args.outPath,'energy_%s.yaml'%(jobId))
else:
    xx=args.tag.replace('/','_')
    outF=os.path.join(args.outPath,'energy_%s.yaml'%(xx))

write_yaml(metaD,outF)
[aa,bb,cc]=[metaD['tot_ene'][x]/1000. for x in ['avr_gpu_ene_J','cpu_ene_J','node_ene_J'] ]
print("ss   %.1f,%.1f,%.1f,%.1f"%(aa,bb,cc,metaD['elaT']))
# ----  just plotting 
plot=Plotter_EnergyUse(args)

plot.one_job(metaD,bigD)
plot.display_all('aa')
