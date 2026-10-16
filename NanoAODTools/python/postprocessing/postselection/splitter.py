import ROOT
# ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
import sys
import os
import optparse
import json
import numpy as np
import math
import shutil
from datetime import datetime
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')

def sampleSplitter(samplesfile, sample,dataset,njobs_per_part ):

    
    print("dataset ", dataset.label, "has components? ",hasattr(dataset, "components")  )
    if hasattr(dataset, "components"):
        comps        = dataset.components
        comp_list = [s.label for s in comps]
        if not (sample in comp_list):
            print(f"sample {sample} not in dataset{dataset.label}, check they match!")
            return
    else:
        if sample != dataset.label:
            print(f"sample {sample} does not correspond to dataset{dataset.label}, check they match!")


            #    print(samples)
    
    totfiles=len(samplesfile[dataset.label][sample]['strings'])
    if (njobs_per_part==-1):
        return 1,totfiles

    nparts = int(totfiles/njobs_per_part)+1
    print("njobs_per_part is ",njobs_per_part," totfiles is ", totfiles," --> nparts is " , nparts)
    lenlastpart=totfiles-njobs_per_part*(nparts-1)
    print("len last part is: ", lenlastpart )
    return nparts, lenlastpart 

#sampleSplitter(samp,datasets[0],njobsperpart)
