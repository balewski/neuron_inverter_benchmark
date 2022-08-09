__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

'''
this data loader reads all data upon start, there is no distributed sampler

reads all data at once and serves them from RAM
- optimized for mult-GPU training
- only used block of data  from each H5-file
- reads data from common file for all ranks
- allows for in-fly transformation

Shuffle: only  all samples after read is compleated

'''

import time,  os
import random
import h5py
import numpy as np
from pprint import pprint

import copy
from torch.utils.data import Dataset, DataLoader
import torch
import logging
import poptorch
import popdist.poptorch

class SyntheticDataset(Dataset):
    def __init__(self):
        super().__init__()
        self.length = 10000000
        data, target = torch.ones([1600, 4]).contiguous(), torch.ones([15]).contiguous()
        self.data = [data, target]
    def __getitem__(self, idx):
        return self.data
    def __len__(self):
        return self.length

#...!...!..................
def get_data_loader(params,  inpMD,domain,popopts, verb=1):
    conf=copy.deepcopy(params)  # the input is reused later in the upper level code
    #print('\n\nGDL:',domain)
    conf['domain']=domain
    conf['h5name']=params['data_path']+inpMD['h5nameTemplate'].replace('*',params['cell_name'])
    if params['num_inp_chan']!=None: #user wants a change
        assert params['num_inp_chan']>0
        assert params['num_inp_chan']<=inpMD['numFeature']
        conf['numInpChan']=params['num_inp_chan']
    else:  # just copy the meta-data value
        conf['numInpChan']=inpMD['numFeature']

    conf['doAux']=False  #legacy switch never used
    #pprint(conf)
    # dataset = Dataset_saved_h5_neuronInverter(domain)
    dataset = Dataset_h5_neuronInverter(conf, verb)
    if 'max_samples_per_epoch' in params:
        max_samp= params['max_samples_per_epoch']
        print('GDL: WARN, shorter %s max_samples=%d from %d'%(domain,max_samp,dataset.numLocFrames))
        dataset.numLocFrames=min(max_samp,dataset.numLocFrames)

    #print('bb',len(dataset),dataset.sanity())

    # GC-speciffic constraint:
    assert len(dataset)//conf['local_batch_size']//conf['gc_m2000']['replica_steps_per_iter']>0

    params[domain+'_steps_per_epoch']=dataset.sanity()

    params['model']['inputShape']=list(dataset.data_frames[0].shape[0:])
    params['model']['outputSize']=dataset.data_parU[0].shape[0]

    num_data_workers = conf['num_data_workers']
    if 'num_data_workers' in params:
        num_data_workers = params['num_data_workers']
    rebatch_size = conf['gc_m2000']['rebatch_size']
    if 'rebatch_size' in params:
        rebatch_size = params['rebatch_size']

    #shuffle=domain=='train'  # use False only for reproducibility
    shuffle=True # both: train & val

    async_options = {
        "sharing_strategy": poptorch.SharingStrategy.SharedMemory,
        "early_preload": True,
        "buffer_size": num_data_workers,
        "load_indefinitely": True,
        "miss_sleep_time_in_ms": 0
    }
    dataloader = poptorch.DataLoader(popopts,dataset,
                             batch_size=conf['local_batch_size'],
                             num_workers=num_data_workers,
                             shuffle=shuffle,
                             mode=poptorch.DataLoaderMode.Async,
                             async_options=async_options,
                             auto_distributed_partitioning=False)

    dataloader.conf = conf
    dataset.conf = conf
    #print('cc',len(dataloader))

    return dataloader

class Dataset_saved_h5_neuronInverter(Dataset):

    def __init__(self, mode):
        if mode == "train":
            self.file_name = "re_worked_data/"
        elif mode == "val":
            self.file_name = "re_worked_data/valid_loader/"
        elif mode == "pseudo_val":
            self.file_name = "re_worked_data/psedo_valid_loader/"
        self.mode = mode

        self.data_frames = torch.load(self.file_name + "data0")
        self.data_parU = torch.zeros((96, 15))

    def __getitem__(self, idx):
        # print('DSI:',idx,self.conf['name'],self.cnt); self.cnt+=1
        return torch.load(self.file_name + "data" + str(idx.item())), torch.load(self.file_name + "target" + str(idx.item()))

    def sanity(self):
        if self.mode == "train":
            return 1621
        elif self.mode == "val":
            return 607
        elif self.mode == "pseudo_val":
            return 201

    def __len__(self):
        if self.mode == "train":
            return 1621
        elif self.mode == "val":
            return 607
        elif self.mode == "pseudo_val":
            return 201

#-------------------
#-------------------
#-------------------
class Dataset_h5_neuronInverter(Dataset):

    def __init__(self, conf,verb=1):
        self.conf=conf
        self.verb=verb

        self.openH5()
        if self.verb and 0:
            print('\nDS-cnst name=%s  shuffle=%r BS=%d steps=%d myRank=%d numSampl/hd5=%d'%(self.conf['name'],self.conf['shuffle'],self.localBS,self.__len__(),self.conf['world_rank'],self.conf['numSamplesPerH5']),'H5-path=',self.conf['dataPath'])
        assert self.numLocFrames>0
        assert self.conf['world_rank']>=0

        # if self.verb :
        #     logging.info(' DS:load-end %s locSamp=%d, X.shape: %s type: %s'%(self.conf['domain'],self.numLocFrames,str(self.data_frames.shape),self.data_frames.dtype))
            #print(' DS:Xall',self.data_frames.shape,self.data_frames.dtype)
            #print(' DS:Yall',self.data_parU.shape,self.data_parU.dtype)


#...!...!..................
    def sanity(self):
        stepPerEpoch=int(np.floor( self.numLocFrames/ self.conf['local_batch_size']))
        if  stepPerEpoch <1:
            print('\nDS:ABORT, Have you requested too few samples per rank?, numLocFrames=%d, BS=%d  name=%s'%(self.numLocFrames, localBS,self.conf['name']))
            exit(67)
        # all looks good
        return stepPerEpoch

#...!...!..................
    def openH5(self):
        cf=self.conf
        inpF=cf['h5name']
        inpFeat=cf['numInpChan'] # this is what user wants
        dom=cf['domain']
        if self.verb>0 : logging.info('DS:fileH5 %s  rank %d of %d '%(inpF,cf['world_rank'],cf['world_size']))

        if not os.path.exists(inpF):
            print('FAILD, missing HD5',inpF)
            exit(22)

        startTm0 = time.time()

        # = = = READING HD5  start
        h5f = h5py.File(inpF, 'r')
        Xshape=h5f[dom+'_frames'].shape
        totSamp=Xshape[0]

        locStep=int(totSamp/cf['world_size']/cf['local_batch_size'])
        locSamp=locStep*cf['local_batch_size']
        #print('totSamp=%d locStep=%d'%(totSamp,locStep))
        assert locStep>0
        maxShard= totSamp// locSamp
        assert maxShard>=cf['world_size']

        # chosen shard is rank dependent, wraps up if not sufficient number of ranks
        myShard=self.conf['world_rank'] %maxShard
        sampIdxOff=myShard*locSamp

        if self.verb: logging.info('DS:file dom=%s myShard=%d, maxShard=%d, sampIdxOff=%d allXshape=%s  inpFeat=%d'%(cf['domain'],myShard,maxShard,sampIdxOff,str(Xshape),inpFeat))

        self.data_frames = []
        self.data_parU = []

        # data reading starts ....
        assert inpFeat==Xshape[2]
        self.data_frames = h5f[dom+'_frames'][sampIdxOff:sampIdxOff+locSamp]
        self.data_parU = h5f[dom+'_unitStar_par'][sampIdxOff:sampIdxOff+locSamp]

        if cf['doAux']:  #never used
            self.data_parP=h5f[dom+'_phys_par'][sampIdxOff:sampIdxOff+locSamp]

        h5f.close()


        # if not self.conf['fp16_inputs']:
        #    self.data_frames = self.data_frames.astype('float32')
        #    self.data_parU = self.data_parU.astype('float32')

        # = = = READING HD5  done
        if self.verb>0 :
            startTm1 = time.time()
            if self.verb: logging.info('DS: hd5 read time=%.2f(sec) dom=%s '%(startTm1 - startTm0,dom))

        # .......................................................
        #.... data embeddings, transformation should go here ....

        #self.data_parU*=1.2
        #.... end of embeddings ........
        # .......................................................

        if 0: # check normalization
            xm=np.mean(self.data_frames)
            xs=np.std(self.data_frames)
            print('xm',xm,xs,myShard,cf['domain'])
            ok99

        self.numLocFrames=len(self.data_frames)
        #self.numLocFrames=512*10  # reduce nymber of  samples

    def __len__(self):
        return self.numLocFrames


    def __getitem__(self, idx):
        # print('DSI:',idx,self.conf['name'],self.cnt); self.cnt+=1
        # assert idx>=0
        # assert idx< self.numLocFrames
        X=self.data_frames[idx]
        Y=self.data_parU[idx]
        return (X,Y)

        if self.conf['x_y_aux']: # predictions for Roy
            AUX=self.data_parP[pCnt:pCnt+bs]
            return (X,Y,AUX)

