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

folderIn= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"

datasets = ['tDM_mPhi1000_mChi1', 'QCD_HT1000', 'TT_Mtt-700to1000', 'TT_Mtt-1000toInf']

infile = {datasets[0]: "tDM_mPhi1000_mChi1_Skim_Skim.root", 
          datasets[1]: "QCD_HT1000_Skim.root",
          datasets[2]: "TT_Mtt-700to1000_2018_Skim_Skim.root",
          datasets[3]: "TT_Mtt-1000toInf_2018_Skim_Skim.root"
}

categories = ['3j0fj', '3j1fj', '2j1fj']

output = {d: {c: 0  for c in categories} for d in datasets}

#-------------------------------------------------------------
#------ utilities---------------------------------------------
#-------------------------------------------------------------

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj):
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
def topcategory(top):  #take as argument a top candidate and return an int : 0 = 3j1fj, 1 = 3j0fj, 2 = 2j1fj 
    top_category = 0
    if top.idxFatJet==-1: #idxFatJet
        top_category = 1
    elif top.idxJet2==-1:
        top_category = 2
    return top_category
def get_category_top_collection(category, top): #return a collection of tops of the same category
    if category == 0:
        return list(filter(lambda x : x.idxFatJet!=-1 and x.idxJet2!=-1 , top))
    elif category == 1:
        return list(filter(lambda x : x.idxFatJet==-1, top))
    elif category == 2:
        return list(filter(lambda x : x.idxJet2==-1 , top))
    else:
        print("idx category error: ", category)
        return None

#----------------------------------------------------
#--------- loop--------------------------------------
#----------------------------------------------------
for d in datasets:
    rfile = ROOT.TFile.Open(folderIn+infile[d])
    tree = InputTree(rfile.Get("Events"))
    
    data_jets = np.zeros((1,3,8))
    data_fatjets = np.zeros((1,12))
    data_mass = np.zeros((1,2))
    data_label = np.zeros((1,1))
    event_category = np.zeros((1,1))
    top_pt = np.zeros((1,1))
    for i in range(1000):#range(tree.GetEntries()):
        event = Event(tree, i)
        
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        tops = Collection(event, "Top")
        ntops = len(tops)
        goodjets, goodfatjets = presel(jets, fatjets)
        
        jet_toappend = np.zeros((ntops,3,8))
        fatjet_toappend = np.zeros((ntops,12))
        mass_toappend = np.zeros((ntops, 2))
        label_toappend = np.zeros((ntops,1))
        event_category_toappend = np.zeros((ntops,1))
        top_pt_toappend = np.zeros((ntops,1))
        if ntops>0:
            idx_top = 0
            top_3j1fj = get_category_top_collection(0, tops)
            top_3j0fj = get_category_top_collection(1, tops)
            top_2j1fj = get_category_top_collection(2, tops)
            
            for t in top_3j1fj:
                fj = goodfatjets[t.idxFatJet]
                j0,j1,j2 = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                fatjet_toappend = fill_fj(fatjet_toappend, fj, idx_top)
                jet_toappend = fill_jets(jet_toappend, j0, j1, j2, (j0.p4()+j1.p4()+j2.p4()), fj.phi, fj.eta, idx_top)
                mass_toappend = fill_mass(mass_toappend, idx_top, j0, j1, j2, fj)
                if not 'QCD' in d: label_toappend[idx_top] = truth(fj=fj, j0=j0, j1=j1, j2=j2) 
                event_category_toappend[idx_top] = 0
                top_pt_toappend[idx_top] = t.pt
                idx_top+=1
            for t in top_3j0fj:
                fj = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                j0,j1,j2 = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                
                jet_toappend = fill_jets(jet_toappend, j0, j1, j2, (j0.p4()+j1.p4()+j2.p4()), fj.Phi(), fj.Eta(), idx_top)
                mass_toappend = fill_mass(mass_toappend, idx_top, j0, j1, j2, fj=None)
                if not 'QCD' in d: label_toappend[idx_top] = truth(j0=j0, j1=j1, j2=j2) 
                event_category_toappend[idx_top] = 1
                top_pt_toappend[idx_top] = t.pt
                idx_top+=1
            for t in top_2j1fj:
                fj = goodfatjets[t.idxFatJet]
                j0,j1 = goodjets[t.idxJet0], goodjets[t.idxJet1]
                fatjet_toappend = fill_fj(fatjet_toappend, fj, idx_top)
                jet_toappend = fill_jets(jets_dnn=jet_toappend, j0=j0, j1=j1, j2=0, sumjet=(j0.p4()+j1.p4()), fj_phi=fj.phi, fj_eta=fj.eta, idx_top=idx_top)
                mass_toappend = fill_mass(mass_dnn=mass_toappend, idx_top=idx_top, j0=j0, j1=j1, j2=None, fj=fj)
                if not 'QCD' in d: label_toappend[idx_top] = truth(fj=fj, j0=j0, j1=j1) 
                event_category_toappend[idx_top] = 2
                top_pt_toappend[idx_top] = t.pt
                idx_top+=1

            #dopo aver fillato jet_toappend e fatjet_toappend
            data_jets = np.append(data_jets, jet_toappend, axis = 0)
            data_fatjets = np.append(data_fatjets, fatjet_toappend, axis = 0)
            data_mass = np.append(data_mass, mass_toappend, axis = 0)
            data_label = np.append(data_label, label_toappend, axis=0)
            top_pt = np.append(top_pt, top_pt_toappend, axis=0)
            event_category = np.append(event_category, event_category_toappend, axis=0)
            if (data_jets[0, 0, 0]<0.0000001):
                data_jets = np.delete(data_jets, 0, axis = 0)
                data_fatjets = np.delete(data_fatjets, 0, axis = 0)
                data_mass = np.delete(data_mass, 0, axis = 0)
                data_label = np.delete(data_label, 0, axis = 0)
                event_category = np.delete(event_category, 0, axis = 0)
                top_pt = np.delete(top_pt, 0, axis = 0)
    event_category = event_category.flatten()
    for c in categories:
        if '0fj' in c : n = 1
        elif '2j' in c : n=2
        else: n=0
        output[d][c] = [data_jets[event_category == n], data_fatjets[event_category == n], data_mass[event_category == n], data_label[event_category == n],
                        top_pt[event_category == n]]

outfile = open("/eos/home-a/acagnott/DarkMatter/trainingSet/trainingset.pkl", "wb")
pkl.dump(output, outfile)
outfile.close()
