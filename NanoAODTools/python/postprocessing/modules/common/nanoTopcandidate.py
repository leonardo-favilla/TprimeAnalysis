import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *
import keras.models 
from itertools import combinations, chain
from scipy.special import comb

def ncombs(n, k):  # return (n k) --> numero di k-ple dati n jets
    if (n-k)<0:
        return 0
    else:
        return factorial(n)/(factorial(n-k)*factorial(k))

def factorial(n):
    if n==0:
        return 1
    elif n<0:
        return 0
    else:
        return n*factorial(n-1)

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj):
    if fj == None:#3j0fj
        top = j0.p4()+j1.p4()+j2.p4()
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
    return mass_dnn, top

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
#nuovi modelli
folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_highpt/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model_name = 'DNN_phase1_test_highpt.h5'#"DNN_phase1_test.h5"#"DNN_withtopmass.h5"
model_highpt = keras.models.load_model(folder_model+model_name)

folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_DNN/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model_name = 'DNN_phase1_test_lowpt_DNN.h5'#"DNN_phase1_test.h5"#"DNN_withtopmass.h5"
model_lowpt_DNN = keras.models.load_model(folder_model+model_name)

folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_LSTM/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model_name = 'DNN_phase1_test_lowpt_LSTM.h5'#"DNN_phase1_test.h5"#"DNN_withtopmass.h5"
model_lowpt_LSTM = keras.models.load_model(folder_model+model_name)

folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model2_name = "DNN_phase2_test.h5"#"DNN_withtopmass_phase2.h5"
model2 = keras.models.load_model(folder_model+model2_name)
class nanoTopcand(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        
        "branches Top candidate"
        self.out.branch("nTop", "I")
        self.out.branch("Top_idxFatJet", "I", lenVar="nTop")
        self.out.branch("Top_idxJet0", "I", lenVar="nTop")
        self.out.branch("Top_idxJet1", "I", lenVar="nTop")
        self.out.branch("Top_idxJet2", "I", lenVar="nTop")
        self.out.branch("Top_sumjetPt", "F", lenVar="nTop")
        self.out.branch("Top_sumjetEta", "F", lenVar="nTop")
        self.out.branch("Top_sumjetPhi", "F", lenVar="nTop")
        self.out.branch("Top_sumjetMass", "F", lenVar="nTop")
        self.out.branch("Top_pt", "F", lenVar="nTop")
        self.out.branch("Top_eta", "F", lenVar="nTop")
        self.out.branch("Top_phi", "F", lenVar="nTop")
        self.out.branch("Top_mass", "F", lenVar="nTop")
        self.out.branch("Top_sumjetDeltaRFatJet", "F", lenVar="nTop")
        self.out.branch("Top_sumjetMaxDeltaRJet", "F", lenVar="nTop")
        self.out.branch("Top_score", "F", lenVar="nTop")
        self.out.branch("Top_score_p2", "F", lenVar="nTop")
        self.out.branch("Top_truth", "F", lenVar="nTop")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        listOfBranches = event.getListOfBranches()
        if "Jet_matched" in listOfBranches: 
            file_signal = True
        else:
            file_signal = False
        jets = Collection(event,"Jet")
        njets = len(jets)
        fatjets = Collection(event,"FatJet")
        nfatjets = len(fatjets)

        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets = len(goodjets)
        ngoodfatjets = len(goodfatjets)
        
        '''init variables to branch'''
        
        ntop_3j1fj = int(ncombs(ngoodjets, 3) * ngoodfatjets) #3j1fj
        ntop_3j0fj = int(ncombs(ngoodjets, 3)) #3j0fj
        ntop_2j1fj = int(ncombs(ngoodjets, 2) * ngoodfatjets) #2j1fj
        ntop = ntop_3j1fj + ntop_3j0fj + ntop_2j1fj
        
        top_idxfatjet = []
        top_idxjet0 = []
        top_idxjet1 = []
        top_idxjet2 = []
        top_sumjetpt = []
        top_sumjeteta = []
        top_sumjetphi = []
        top_sumjetmass = []
        top_pt_ = []
        top_eta_ = []
        top_phi_ = []
        top_mass_ = []
        top_sumjetdeltarfatjet = []
        top_sumjetmaxdeltarjet = []
        top_truth = []
                    
        fj_dnn = np.zeros((int(ntop), 12)) 
        jets_dnn = np.zeros((int(ntop), 3, 8))        
        mass_dnn = np.zeros((int(ntop), 2))

        idx_top = 0
        #print(jets.keys())
        while (idx_top<ntop):
            for idx_j0 in range(ngoodjets):
                for idx_j1 in range(idx_j0):
                    for idx_fj in range(ngoodfatjets):
                        top_idxfatjet.append(idx_fj)
                        top_idxjet0.append(idx_j0)
                        top_idxjet1.append(idx_j1)
                        top_idxjet2.append(-1)
                        
                        j0, j1 = goodjets[idx_j0],goodjets[idx_j1]
                        fj = goodfatjets[idx_fj]
                        sumjet = j0.p4()+j1.p4()
                        
                        top_sumjetpt.append(sumjet.Pt())
                        top_sumjeteta.append(sumjet.Eta())
                        top_sumjetphi.append(sumjet.Phi())
                        top_sumjetmass.append(sumjet.M())
                        top_sumjetdeltarfatjet.append(deltaR(fj.phi,fj.eta, sumjet.Phi(), sumjet.Eta()))
                        top_sumjetmaxdeltarjet.append(max([deltaR(j0.phi, j0.eta, sumjet.Phi(), sumjet.Eta()), 
                                                           deltaR(j1.phi, j1.eta, sumjet.Phi(), sumjet.Eta())]))
                        
                        jets_dnn = fill_jets(jets_dnn = jets_dnn, j0=j0, j1=j1, j2=0, sumjet = sumjet,  fj_phi= fj.phi, fj_eta=fj.eta, idx_top=idx_top)
                        fj_dnn = fill_fj(fj_dnn, fj, idx_top)
                        mass_dnn, top_p4 = fill_mass(mass_dnn=mass_dnn, idx_top=idx_top, j0=j0, j1=j1, j2 =None, fj = fj)
                        top_pt_.append(top_p4.Pt())
                        top_eta_.append(top_p4.Eta())
                        top_phi_.append(top_p4.Phi())
                        top_mass_.append(top_p4.M())

                        if file_signal:
                            top_truth.append(truth(j0=j0, j1=j1, fj=fj))
                        else:
                            top_truth.append(0)
                        idx_top +=1

                    for idx_j2 in range(idx_j1):
                        top_idxfatjet.append(-1)
                        top_idxjet0.append(idx_j0)
                        top_idxjet1.append(idx_j1)
                        top_idxjet2.append(idx_j2)
                        
                        j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                        fj = ROOT.TLorentzVector()
                        fj.SetPtEtaPhiM(0,0,0,0)
                        sumjet = j0.p4()+j1.p4()+j2.p4()
                        
                        top_sumjetpt.append(sumjet.Pt())
                        top_sumjeteta.append(sumjet.Eta())
                        top_sumjetphi.append(sumjet.Phi())
                        top_sumjetmass.append(sumjet.M())
                        top_sumjetdeltarfatjet.append(deltaR(fj.Phi(),fj.Eta(), sumjet.Phi(), sumjet.Eta()))
                        top_sumjetmaxdeltarjet.append(max([deltaR(j0.phi, j0.eta, sumjet.Phi(), sumjet.Eta()), 
                                                           deltaR(j1.phi, j1.eta, sumjet.Phi(), sumjet.Eta()), 
                                                           deltaR(j2.phi, j2.eta, sumjet.Phi(), sumjet.Eta())]))
        
                        jets_dnn = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), idx_top)
                        mass_dnn, top_p4 = fill_mass(mass_dnn=mass_dnn, idx_top=idx_top, j0=j0, j1=j1, j2=j2, fj=None)
                        top_pt_.append(top_p4.Pt())
                        top_eta_.append(top_p4.Eta())
                        top_phi_.append(top_p4.Phi())
                        top_mass_.append(top_p4.M())
                        if file_signal:
                            top_truth.append(truth(j0=j0, j1=j1, j2=j2))
                        else: 
                            top_truth.append(0)
                        
                        idx_top +=1
                        
                        for idx_fj in range(ngoodfatjets):
                            top_idxfatjet.append(idx_fj)
                            top_idxjet0.append(idx_j0)
                            top_idxjet1.append(idx_j1)
                            top_idxjet2.append(idx_j2)
                            
                            j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                            fj = goodfatjets[idx_fj]
                            sumjet = j0.p4() + j1.p4() +j2.p4()
                            
                            top_sumjetpt.append(sumjet.Pt())
                            top_sumjeteta.append(sumjet.Eta())
                            top_sumjetphi.append(sumjet.Phi())
                            top_sumjetmass.append(sumjet.M())
                            top_sumjetdeltarfatjet.append(deltaR(fj.phi,fj.eta, sumjet.Phi(), sumjet.Eta()))
                            top_sumjetmaxdeltarjet.append(max([deltaR(j0.phi, j0.eta, sumjet.Phi(), sumjet.Eta()), 
                                                               deltaR(j1.phi, j1.eta, sumjet.Phi(), sumjet.Eta()), 
                                                               deltaR(j2.phi, j2.eta, sumjet.Phi(), sumjet.Eta())]))
                            
                            jets_dnn = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.phi, fj.eta, idx_top)
                            fj_dnn = fill_fj(fj_dnn, fj, idx_top)
                            mass_dnn, top_p4 = fill_mass(mass_dnn=mass_dnn, idx_top=idx_top, j0=j0, j1=j1, j2=j2, fj=fj)
                            top_pt_.append(top_p4.Pt())
                            top_eta_.append(top_p4.Eta())
                            top_phi_.append(top_p4.Phi())
                            top_mass_.append(top_p4.M())
                            if file_signal:
                                top_truth.append(truth(j0=j0, j1=j1, j2=j2, fj=fj))
                            else: 
                                top_truth.append(0)
                            idx_top+=1
        if(ntop>0): 
            #for n in nTop:
            top_score = model.predict({'fatjet':fj_dnn, 'jet': jets_dnn, 'top_mass': mass_dnn}).flatten().tolist()
            top_score_p2 = model2.predict({'fatjet':fj_dnn, 'jet': jets_dnn, 'top_mass': mass_dnn}).flatten().tolist()
        else: 
            top_score = []
            top_score_p2 = []
        
        self.out.fillBranch("nTop", ntop)
        self.out.fillBranch("Top_idxFatJet", top_idxfatjet)
        self.out.fillBranch("Top_idxJet0", top_idxjet0)
        self.out.fillBranch("Top_idxJet1", top_idxjet1)
        self.out.fillBranch("Top_idxJet2", top_idxjet2)
        self.out.fillBranch("Top_sumjetPt", top_sumjetpt)
        self.out.fillBranch("Top_sumjetEta", top_sumjeteta)
        self.out.fillBranch("Top_sumjetPhi", top_sumjetphi)
        self.out.fillBranch("Top_sumjetMass", top_sumjetmass)
        self.out.fillBranch("Top_pt", top_pt_)
        self.out.fillBranch("Top_eta", top_eta_)
        self.out.fillBranch("Top_phi", top_phi_)
        self.out.fillBranch("Top_mass", top_mass_)
        self.out.fillBranch("Top_sumjetDeltaRFatJet", top_sumjetdeltarfatjet)
        self.out.fillBranch("Top_sumjetMaxDeltaRJet", top_sumjetmaxdeltarjet)
        self.out.fillBranch("Top_score", top_score)
        self.out.fillBranch("Top_score_p2", top_score_p2)
        self.out.fillBranch("Top_truth", top_truth)
        
        return True

