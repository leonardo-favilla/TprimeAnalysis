import os
import sys
import ROOT
import math
from array import array
import numpy as np
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import pickle as pkl
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use(hep.style.CMS)
folderIn = './'
infile = "tDM_mPhi1000_mChi1_Skim_Skim.root"
rfile = ROOT.TFile.Open(folderIn+infile)
tree = InputTree(rfile.Get("Events"))

ntot=0
npresel = 0
n2match = 0
ncatomitted = 0
print("nevent ", tree.GetEntries())
for i in range(tree.GetEntries()):
    event = Event(tree, i)
        
    jets = Collection(event, "Jet")
    fatjets = Collection(event, "FatJet")
    tops = Collection(event, "Top")
    ntops = len(tops)
    goodjets, goodfatjets = presel(jets, fatjets)
    
    toptrue=0
    for t in tops:
        if t.truth==1: toptrue+=1
    if toptrue>0: continue
    ntot+=1

    flavs_gj = []
    flavs_gfj = []
            
    for j in goodjets: flavs_gj+= get_pos_nums(j.pdgId)
    for fj in goodfatjets: flavs_gfj+= get_pos_nums(fj.pdgId)
    #print("Event-------------------------", i)
    #print("goodjets flav ", np.unique(flavs_j))
    #print("goodfatjets flav ", np.unique(flavs_fj))
    flavs_j = []
    flavs_fj = []
    for j in jets: 
        flavs_j+= get_pos_nums(j.pdgId)
    for fj in fatjets: flavs_fj+= get_pos_nums(fj.pdgId)
    #print("jets flav ", np.unique(flavs_j))
    #print("fatjets flav ", np.unique(flavs_fj))

    #e_presel, e_2match, e_omitted=-1,-1,-1
    #print(i)
    #print('presel', (len(np.unique(flavs_j+flavs_fj))==3) and (len(np.unique(flavs_gj+flavs_gfj))<3))
    if (len(np.unique(flavs_j+flavs_fj))==3) and (len(np.unique(flavs_gj+flavs_gfj))<3): 
        #e_presel = i
        npresel +=1    
    #print('2match ', len(np.unique(flavs_j+flavs_fj))<3)
    if len(np.unique(flavs_j+flavs_fj))<3: 
        #e_2match = i
        n2match +=1
    #print('omitted', len(np.unique(flavs_gj+flavs_gfj))==3)
    if len(np.unique(flavs_gj+flavs_gfj))==3: 
        #e_omitted= i
        ncatomitted +=1
    if ((len(np.unique(flavs_j+flavs_fj))==3) and (len(np.unique(flavs_gj+flavs_gfj))<3)+
        len(np.unique(flavs_j+flavs_fj))<3+
        len(np.unique(flavs_gj+flavs_gfj))==3)>1: print(i)
    #if e_presel== e_2match or e_presel==e_omitted or e_2match==e_omitted: print(i)


print("eventi senza top true ", ntot)
print("eventi in cui jet matchati vengono scartati dalla preselezione", npresel)
print("eventi in cui non ho 3 match", n2match)
print("eventi di una categoria non considerata", ncatomitted)
