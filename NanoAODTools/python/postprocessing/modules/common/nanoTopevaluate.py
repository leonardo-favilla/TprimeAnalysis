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
import os
#from datetime import datetime

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

#nuovi modelli
#folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_highpt/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
#model_name = 'DNN_phase1_test_highpt.h5'#"DNN_phase1_test.h5"#"DNN_withtopmass.h5"
#model_highpt = keras.models.load_model(folder_model+model_name)

#folder_model = "../../data/dict_tresholds/"
folder_model = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/" % os.environ['CMSSW_BASE']

#folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_DNN/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model_name = 'DNN_phase1_test_lowpt_DNN.h5'#"DNN_phase1_test.h5"#"DNN_withtopmass.h5"
model_lowpt_DNN = keras.models.load_model(folder_model+model_name)

#folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_LSTM/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
#model_name = 'DNN_phase1_test_lowpt_LSTM.h5'#"DNN_phase1_test.h5"#"DNN_withtopmass.h5"
#model_lowpt_LSTM = keras.models.load_model(folder_model+model_name)
# phase2
#folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test2/"#"/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model2_name = "DNN_phase2_test2.h5"#"DNN_withtopmass_phase2.h5"
model_highpt_p2 = keras.models.load_model(folder_model+model2_name)


class nanoTopevaluate(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        
        "branches Top candidate high pt"
        #self.out.branch("TopHighPt_score", "F", lenVar="nTopHighPt")
        self.out.branch("TopHighPt_score2", "F", lenVar="nTopHighPt")
        self.out.branch("TopLowPt_scoreDNN", "F", lenVar="nTopLowPt")
        #self.out.branch("TopLowPt_scoreLSTM", "F", lenVar="nTopLowPt")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets = Collection(event,"Jet")
        njets = len(jets)
        fatjets = Collection(event,"FatJet")
        nfatjets = len(fatjets)

        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets = len(goodjets)
        ngoodfatjets = len(goodfatjets)
        
        tophighpt = Collection(event, "TopHighPt")
        toplowpt = Collection(event, "TopLowPt")
        met = Object(event, "MET")
        mindelta = Object(event, "MinDelta")
        
        if met.pt > 200 and mindelta.phi >0.6:
            # loop su high pt e low pt candidate per valutare lo score con i modelli corrispondenti
            fj_dnn = np.zeros((int(len(tophighpt)), 12)) 
            jets_dnn = np.zeros((int(len(tophighpt)), 3, 8))        
            mass_dnn = np.zeros((len(tophighpt), 2))
            for i, top in enumerate(tophighpt):
                if top.idxJet2==-1:
                    j0, j1 = goodjets[top.idxJet0],goodjets[top.idxJet1]
                    fj = goodfatjets[top.idxFatJet]
                    sumjet = j0.p4()+j1.p4()
                    jets_dnn = fill_jets(jets_dnn = jets_dnn, j0=j0, j1=j1, j2=0, sumjet = sumjet,  fj_phi= fj.phi, fj_eta=fj.eta, idx_top=i)
                    fj_dnn = fill_fj(fj_dnn, fj, i)
                    mass_dnn = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =None, fj = fj)
                elif top.idxFatJet==-1:
                    j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                    fj = ROOT.TLorentzVector()
                    fj.SetPtEtaPhiM(0,0,0,0)
                    sumjet = j0.p4()+j1.p4()+j2.p4()
                    jets_dnn = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i)
                    mass_dnn = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =j2, fj = None)
                else:
                    j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                    fj = goodfatjets[top.idxFatJet]
                    sumjet = j0.p4() + j1.p4() +j2.p4()
                    jets_dnn = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.phi, fj.eta, i)
                    fj_dnn = fill_fj(fj_dnn, fj, i)
                    mass_dnn = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =j2, fj = fj)
            if len(tophighpt)!=0:
                #top_score = model_highpt.predict({'fatjet':fj_dnn, 'jet': jets_dnn}).flatten().tolist()
                top_score2 = model_highpt_p2.predict({'fatjet':fj_dnn, 'jet': jets_dnn,  'top_mass': mass_dnn}).flatten().tolist()
            else:
                #top_score = []
                top_score2 = []
            #self.out.fillBranch("TopHighPt_score", top_score)
            self.out.fillBranch("TopHighPt_score2", top_score2)

            jets_dnn = np.zeros((int(len(toplowpt)), 3, 8))        
            for i, top in enumerate(toplowpt):
                j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                sumjet = j0.p4()+j1.p4()+j2.p4()
                jets_dnn = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i)
            if len(toplowpt)!=0:
                top_score_DNN = model_lowpt_DNN.predict({"jet0": jets_dnn[:,0,:-2], "jet1": jets_dnn[:,1,:-2], "jet2": jets_dnn[:,2,:-2]}).flatten().tolist()
                #top_score_LSTM = model_lowpt_LSTM.predict({"jet": jets_dnn[:,:,:-2]})
            else:
                top_score_DNN = []
                #top_score_LSTM = []
            self.out.fillBranch("TopLowPt_scoreDNN", top_score_DNN)
        else:
            top_score2 = np.tile(-10, len(tophighpt))
            top_score_DNN = np.tile(-10, len(toplowpt))
            self.out.fillBranch("TopLowPt_scoreDNN", top_score_DNN)
            self.out.fillBranch("TopHighPt_score2", top_score2)
        #self.out.fillBranch("TopLowPt_scoreLSTM", top_score_LSTM)
        # t1 = datetime.now()
        # print("TopEvaluate module time :", t1-t0) 
        return True
