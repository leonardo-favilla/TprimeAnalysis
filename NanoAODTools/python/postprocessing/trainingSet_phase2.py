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


select_trs= True#False#
select_best_top= False#True#

folderIn= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"

datasets = ['tDM_mPhi1000_mChi1', 'QCD_HT1000to1500','QCD_HT1500to2000', 'QCD_HT2000toInf', 'TT_Mtt_700to1000', 'TT_Mtt_1000toInf']
infile = {datasets[0]: "tDM_mPhi1000_mChi1_Skim_Skim_Skim.root", 
          datasets[1]: "QCD_HT1000_Skim_Skim.root", 
          datasets[2]: "QCD-HT1500to2000_2018_Skim_Skim.root",
          datasets[3]: "QCD-HT2000toInf_2018_Skim_Skim.root",
          datasets[4]: "TT_Mtt-700to1000_2018_Skim_Skim_Skim.root",
          datasets[5]: "TT_Mtt-1000toInf_2018_Skim_Skim_Skim.root"
}

categories = ['3j0fj', '3j1fj', '2j1fj']

output = {d: {c: 0  for c in categories} for d in datasets}

#-------------------------------------------------------------
#------ utilities---------------------------------------------
#-------------------------------------------------------------

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, variables_cluster):
    if fj == None:#3j0fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
    elif j2 == None:#2j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
        top = top2j1fj(fj, j0, j1)
        mass_dnn[idx_top, 1] = top.M()
    else: #3j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        top = top3j1fj(fj, j0, j1, j2)
        mass_dnn[idx_top, 1] = top.M()
    if isinstance(variables_cluster,list):
        mass_dnn[idx_top, 2] = variables_cluster[0]
        mass_dnn[idx_top, 3] = variables_cluster[1]
        mass_dnn[idx_top, 4] = variables_cluster[2]
    return mass_dnn

def fill_fj(fj_dnn, fj, idx_top): 
    fj_dnn[idx_top, 0] = fj.area
    fj_dnn[idx_top, 1] = fj.btagDeepB
    fj_dnn[idx_top, 2] = fj.deepTagMD_TvsQCD
    fj_dnn[idx_top, 3] = fj.deepTagMD_WvsQCD
    fj_dnn[idx_top, 4] = fj.deepTag_QCD
    fj_dnn[idx_top, 5] = fj.deepTag_QCDothers
    fj_dnn[idx_top, 6] = fj.deepTag_TvsQCD
    fj_dnn[idx_top, 7] = fj.deepTag_WvsQCD
    fj_dnn[idx_top, 8] = fj.eta
    fj_dnn[idx_top, 9] = fj.mass
    fj_dnn[idx_top, 10] = fj.phi
    fj_dnn[idx_top, 11] = fj.pt
    return fj_dnn

def fill_jets(jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top): 

    jets_dnn[idx_top, 0, 0] = j0.area
    jets_dnn[idx_top, 0, 1] = j0.btagDeepB
    jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
    jets_dnn[idx_top, 0, 3] = j0.mass
    jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
    jets_dnn[idx_top, 0, 5] = j0.pt
    jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
    jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet
    
    jets_dnn[idx_top, 1, 0] = j1.area
    jets_dnn[idx_top, 1, 1] = j1.btagDeepB
    jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
    jets_dnn[idx_top, 1, 3] = j1.mass
    jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
    jets_dnn[idx_top, 1, 5] = j1.pt
    jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
    jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
    if hasattr(j2,"pt"):
        jets_dnn[idx_top, 2, 0] = j2.area
        jets_dnn[idx_top, 2, 1] = j2.btagDeepB
        jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
        jets_dnn[idx_top, 2, 3] = j2.mass
        jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
        jets_dnn[idx_top, 2, 5] = j2.pt
        jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
        jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
    
    return jets_dnn

#----------------------------------------------------
#--------- loop--------------------------------------
#----------------------------------------------------
ntopcand = []
ntoptrue= []
ntopcand3j1fj, ntopcand3j0fj, ntopcand2j1fj = [], [], []
ntoptrue3j1fj, ntoptrue3j0fj, ntoptrue2j1fj = [], [], []

trs_file = open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_highpt/tresholds.pkl", "rb")
trs = pkl.load(trs_file)
trs10 = trs['fpr 10']
trs5 = trs['fpr 5']
trs1 = trs['fpr 1']
trs01 = trs['fpr 01']
print(trs10, trs1, trs01)

trs_toselect = trs10#trs01  #--------------------------------------------------------------------------
trs_cluster = trs10
print("Starting datasets loop")
for d in datasets:
    rfile = ROOT.TFile.Open(folderIn+infile[d])
    tree = InputTree(rfile.Get("Events"))    
    data_jets = np.zeros((1,3,8))
    data_fatjets = np.zeros((1,12))
    data_mass = np.zeros((1,5))
    data_label = np.zeros((1,1))
    event_category = np.zeros((1,1))
    print("Starting event loop for ", d)
    for i in range(tree.GetEntries()):
        event = Event(tree, i)
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        tops = Collection(event, "TopHighPt")
        ntops = len(tops)
        goodjets, goodfatjets = presel(jets, fatjets)
        ntopcand.append(ntops)
        ntopcand3j1fj.append(0)
        ntopcand3j0fj.append(0) 
        ntopcand2j1fj.append(0)
        ntoptrue3j1fj.append(0)
        ntoptrue3j0fj.append(0) 
        ntoptrue2j1fj.append(0)
        for t in tops:
            tmp = topcategory(t)
            if tmp ==0: ntopcand3j1fj[-1]+=1
            elif tmp==1: ntopcand3j0fj[-1]+=1
            else:ntopcand2j1fj[-1]+=1
        if 'QCD' not in d:
            tr= 0
            cat =  -1
            for t in tops:
                if t.truth==1:
                    tr +=1
                    tmp = topcategory(t)
                    if tmp ==0: ntoptrue3j1fj[-1]+=1
                    elif tmp==1: ntoptrue3j0fj[-1]+=1
                    else:ntoptrue2j1fj[-1]+=1
            #if tr==0: print(i)    
            ntoptrue.append(tr)
        if ntops==0: continue
 
        best_top = []
        if select_trs:
            best_top = get_top_over_trs(tops, trs_toselect, 'highpt')
            variables_cluster = None
            #for t in best_top:
        if select_best_top:
            t__ = get_best_top(tops)
            if t__.score>trs_toselect:
                best_top.append(get_best_top(tops))
                top_over_trs = get_top_over_trs(tops, trs_toselect)
                out = top_cluster_excl(tops, trs_cluster)
                variables_cluster = [out['n_cluster'][0], out['n_cluster_over_trs'][0]/out['n_cluster'][0], out['best_score'][0]]
            #print(variables_cluster)
        #print(best_top)
        if(i%1000==0): print("dataset ",d," event ",i) 
        for t in best_top:
            
            best_top_category = topcategory(t)
            
            jet_toappend = np.zeros((1,3,8))
            fatjet_toappend = np.zeros((1,12))
            mass_toappend = np.zeros((1, 5))
            label_toappend = np.zeros((1,1))
            event_category_toappend = np.zeros((1,1))
            
            if best_top_category == 0:
                fj = goodfatjets[t.idxFatJet]
                j0, j1, j2 = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                fatjet_toappend = fill_fj(fj_dnn= fatjet_toappend, fj=fj, idx_top=0)
                jet_toappend = fill_jets(jets_dnn= jet_toappend, j0= j0, j1= j1, j2= j2, sumjet= (j0.p4()+j1.p4()+j2.p4()), 
                                         fj_phi= fj.phi, fj_eta= fj.eta, idx_top= 0)
                mass_toappend = fill_mass(mass_dnn= mass_toappend, idx_top= 0, j0= j0, j1= j1, j2= j2, fj= fj, variables_cluster=variables_cluster)
                if not 'QCD' in d: label_toappend[0] = truth(fj=fj, j0=j0, j1=j1, j2=j2) 
                event_category_toappend[0] = best_top_category
                
            elif best_top_category == 1:
                fj = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                j0, j1, j2 = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                jet_toappend = fill_jets(jets_dnn= jet_toappend, j0= j0, j1= j1, j2= j2, sumjet= (j0.p4()+j1.p4()+j2.p4()), 
                                         fj_phi= fj.Phi(), fj_eta= fj.Eta(), idx_top= 0)
                mass_toappend = fill_mass(mass_dnn= mass_toappend, idx_top= 0, j0= j0, j1= j1, j2= j2, fj= None, variables_cluster=variables_cluster)
                if not 'QCD' in d: label_toappend[0] = truth(j0=j0, j1=j1, j2=j2) 
                event_category_toappend[0] = best_top_category
            else:
                fj = goodfatjets[t.idxFatJet]
                j0, j1 = goodjets[t.idxJet0], goodjets[t.idxJet1]
                fatjet_toappend = fill_fj(fj_dnn= fatjet_toappend, fj=fj, idx_top=0)
                jet_toappend = fill_jets(jets_dnn= jet_toappend, j0= j0, j1= j1, j2=0, sumjet= (j0.p4()+j1.p4()), 
                                         fj_phi= fj.phi, fj_eta= fj.eta, idx_top= 0)
                mass_toappend = fill_mass(mass_dnn= mass_toappend, idx_top= 0, j0= j0, j1= j1, j2= None, fj= fj, variables_cluster=variables_cluster)
                if not 'QCD' in d: label_toappend[0] = truth(fj=fj, j0=j0, j1=j1) 
                event_category_toappend[0] = best_top_category
            
            #dopo aver fillato jet_toappend e fatjet_toappend
            data_jets = np.append(data_jets, jet_toappend, axis = 0)
            data_fatjets = np.append(data_fatjets, fatjet_toappend, axis = 0)
            data_mass = np.append(data_mass, mass_toappend, axis = 0)
            if label_toappend[0]==2: print(d, i, label_toappend)
            data_label = np.append(data_label, label_toappend, axis=0)
            #print(event_category, event_category_toappend)
            event_category = np.append(event_category, event_category_toappend, axis=0)
            #print(event_category)
            if (data_jets[0, 0, 0]==0):
                data_jets = np.delete(data_jets, 0, axis = 0)
                data_fatjets = np.delete(data_fatjets, 0, axis = 0)
                data_mass = np.delete(data_mass, 0, axis = 0)
                data_label = np.delete(data_label, 0, axis = 0)
                event_category = np.delete(event_category, 0, axis = 0)
            #print(data_mass)
    event_category = event_category.flatten()
    for c in categories:
        if '0fj' in c :
            n = 1
        elif '2j' in c :
            n = 2
        else:
            n = 0
        output[d][c] = [data_jets[event_category == n], data_fatjets[event_category == n], data_mass[event_category == n], data_label[event_category == n]]

outfile = open("/eos/home-a/acagnott/DarkMatter/trainingSet/trainingset_phase2.pkl", "wb")
pkl.dump(output, outfile)
outfile.close()

fig, ax = plt.subplots()
ax.hist(ntopcand, range = [-0.5, 100.5], bins =101, histtype='step', label= 'top candidates')
ax.hist(ntoptrue, range = [-0.5,100.5], bins = 101, histtype='step', label= 'top true')
ax.legend()
ax.set_title("#top per event")
ax.set_xlabel("# top per event")
plt.savefig("/eos/home-a/acagnott/DarkMatter/Ntopperevent.png")
fig, ax = plt.subplots()
ax.hist([ntopcand3j1fj, ntopcand3j0fj, ntopcand2j1fj], 
        range = [-0.5, 100.5], bins =101, 
        histtype='step', label= ['top cand 3j1fj', 'top cand 3j0fj', 'top cand 2j1fj'])
ax.hist([ntoptrue3j1fj, ntoptrue3j0fj, ntoptrue2j1fj], 
        range = [-0.5, 100.5], bins =101, 
        histtype='step', label= ['top true 3j1fj', 'top true 3j0fj', 'top true 2j1fj'])
ax.set_title("#top per event for different categories")
ax.set_xlabel("# top per event")
ax.legend()
plt.savefig("/eos/home-a/acagnott/DarkMatter/Ntopcategoryperevent.png")
