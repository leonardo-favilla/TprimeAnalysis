import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import tensorflow as tf
from itertools import combinations, chain
import os

###### UTILITIES ######
def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj):
    if fj == None:#3j0fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 2] = (j0.p4()+j1.p4()+j2.p4()).Pt()
    elif j2 == None:#2j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
        top                  = top2j1fj(fj, j0, j1)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    else: #3j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        top                  = top3j1fj(fj, j0, j1, j2)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    return mass_dnn

def fill_fj(year, fj_dnn, fj, idx_top):
    if year==2018: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.deepTagMD_TvsQCD
        fj_dnn[idx_top, 3]  = fj.deepTagMD_WvsQCD
        fj_dnn[idx_top, 4]  = fj.deepTag_QCD
        fj_dnn[idx_top, 5]  = fj.deepTag_QCDothers
        fj_dnn[idx_top, 6]  = fj.deepTag_TvsQCD
        fj_dnn[idx_top, 7]  = fj.deepTag_WvsQCD
        fj_dnn[idx_top, 8]  = fj.eta
        fj_dnn[idx_top, 9]  = fj.mass
        fj_dnn[idx_top, 10] = fj.phi
        fj_dnn[idx_top, 11] = fj.pt

    elif year in [2022,2023]: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.particleNetWithMass_QCD
        fj_dnn[idx_top, 3]  = fj.particleNetWithMass_TvsQCD
        fj_dnn[idx_top, 4]  = fj.particleNetWithMass_WvsQCD
        fj_dnn[idx_top, 5]  = fj.eta
        fj_dnn[idx_top, 6]  = fj.mass
        fj_dnn[idx_top, 7]  = fj.phi
        fj_dnn[idx_top, 8]  = fj.pt

    elif year in [2024]: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.globalParT3_Xbb / (fj.globalParT3_Xbb + fj.globalParT3_QCD)
        fj_dnn[idx_top, 2]  = fj.globalParT3_QCD
        fj_dnn[idx_top, 3]  = fj.globalParT3_withMassTopvsQCD
        fj_dnn[idx_top, 4]  = fj.globalParT3_withMassWvsQCD
        fj_dnn[idx_top, 5]  = fj.eta
        fj_dnn[idx_top, 6]  = fj.mass
        fj_dnn[idx_top, 7]  = fj.phi
        fj_dnn[idx_top, 8]  = fj.pt

    
    return fj_dnn

def fill_jets(year, jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top):
    if year in [2018]:
        jet_btagdiscr = "btagDeepB"
    elif year in [2022,2023]:
        jet_btagdiscr = "btagPNetB"
    elif year in [2024]:
        jet_btagdiscr = "btagUParTAK4B"

    jets_dnn[idx_top, 0, 0] = j0.area
    jets_dnn[idx_top, 0, 1] = getattr(j0, jet_btagdiscr)
    jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
    jets_dnn[idx_top, 0, 3] = j0.mass
    jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
    jets_dnn[idx_top, 0, 5] = j0.pt
    jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
    jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet

    jets_dnn[idx_top, 1, 0] = j1.area
    jets_dnn[idx_top, 1, 1] = getattr(j1, jet_btagdiscr)
    jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
    jets_dnn[idx_top, 1, 3] = j1.mass
    jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
    jets_dnn[idx_top, 1, 5] = j1.pt
    jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
    jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
    if hasattr(j2,"pt"):
        jets_dnn[idx_top, 2, 0] = j2.area
        jets_dnn[idx_top, 2, 1] = getattr(j2, jet_btagdiscr)
        jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
        jets_dnn[idx_top, 2, 3] = j2.mass
        jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
        jets_dnn[idx_top, 2, 5] = j2.pt
        jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
        jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
    return jets_dnn





class nanoTopevaluate_MultiScore(Module):
    def __init__(self, modelMix_path, modelRes_path, isMC=1, year=2018):
        self.modelMix_path = modelMix_path
        self.modelRes_path = modelRes_path
        self.modelMix      = tf.keras.models.load_model(modelMix_path, compile=False)
        self.modelRes      = tf.keras.models.load_model(modelRes_path, compile=False)
        self.isMC = isMC
        self.year = year
        # print(self.year)  
        pass


    def beginJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        "Branch scores to tree"
        # High Pt
        # self.out.branch("TopMixed_score2", "F", lenVar="nTopMixed")
        self.out.branch(f"TopMixed_TopScore", "F", lenVar="nTopMixed")

        # Low Pt
        self.out.branch("TopResolved_TopScore", "F", lenVar="nTopResolved")

        # 2024: the other 2 DNN outputs (False, QCD), only to look at them (TopScore = True output)
        if self.year in [2024]:
            self.out.branch("TopMixed_TopScoreFalse", "F", lenVar="nTopMixed")
            self.out.branch("TopMixed_TopScoreQCD", "F", lenVar="nTopMixed")
            self.out.branch("TopResolved_TopScoreFalse", "F", lenVar="nTopResolved")
            self.out.branch("TopResolved_TopScoreQCD", "F", lenVar="nTopResolved")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets     = Collection(event,"Jet")
        njets    = len(jets)
        fatjets  = Collection(event,"FatJet")
        nfatjets = len(fatjets)

        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets             = len(goodjets)
        ngoodfatjets          = len(goodfatjets)
        
        tophighpt             = Collection(event, "TopMixed")
        toplowpt              = Collection(event, "TopResolved")

        
        # loop su High Pt candidates per valutare lo score con i modelli corrispondenti
        if self.year == 2018:
            fj_dnn      = np.zeros((int(len(tophighpt)), 12))
        elif self.year in [2022,2023,2024]:
            fj_dnn      = np.zeros((int(len(tophighpt)), 9))

        jets_dnn    = np.zeros((int(len(tophighpt)), 3, 8))
        mass_dnn    = np.zeros((len(tophighpt), 3))
        for i, top in enumerate(tophighpt):
            if top.idxJet2==-1:
                j0, j1      = goodjets[top.idxJet0],goodjets[top.idxJet1]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4()+j1.p4()
                jets_dnn    = fill_jets(self.year, jets_dnn = jets_dnn, j0=j0, j1=j1, j2=0, sumjet = sumjet,  fj_phi= fj.phi, fj_eta=fj.eta, idx_top=i)
                fj_dnn      = fill_fj(self.year, fj_dnn, fj, i)
                mass_dnn    = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =None, fj = fj)
            elif top.idxFatJet==-1:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                sumjet      = j0.p4()+j1.p4()+j2.p4()
                jets_dnn    = fill_jets(self.year, jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i)
                mass_dnn    = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =j2, fj = None)
            else:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4() + j1.p4() +j2.p4()
                jets_dnn    = fill_jets(self.year, jets_dnn, j0, j1, j2, sumjet, fj.phi, fj.eta, i)
                fj_dnn      = fill_fj(self.year, fj_dnn, fj, i)
                mass_dnn    = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =j2, fj = fj)



        ####### SCORES ####### 
        # Calculate Scores for several models #
        scores                  = []
        scores_False            = []
        scores_QCD              = []
        if len(tophighpt)!=0:
            if self.year in [2018,2022,2023]:
                scores          = self.modelMix({"fatjet": fj_dnn, "jet": jets_dnn, "top": mass_dnn}).numpy().flatten().tolist()
            elif self.year in [2024]:
                dnn_output      = self.modelMix({"fatjet": fj_dnn, "jet": jets_dnn, "top": mass_dnn}).numpy() # one DNN evaluation, columns: 0 False, 1 True, 2 QCD
                scores_False    = dnn_output[:,0].flatten().tolist()
                scores_True     = dnn_output[:,1].flatten()
                scores_QCD      = dnn_output[:,2].flatten().tolist()
                scores          = scores_True.tolist() # TopScore = True output
        else:
            scores              = []

        # Branch the scores calculated #
        self.out.fillBranch(f"TopMixed_TopScore", scores)
        if self.year in [2024]:
            self.out.fillBranch("TopMixed_TopScoreFalse", scores_False)
            self.out.fillBranch("TopMixed_TopScoreQCD", scores_QCD)


        # loop su Low Pt candidates per valutare lo score con i modelli corrispondenti
        jets_dnn = np.zeros((int(len(toplowpt)), 3, 8))        
        for i, top in enumerate(toplowpt):
            j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
            fj = ROOT.TLorentzVector()
            fj.SetPtEtaPhiM(0,0,0,0)
            sumjet = j0.p4()+j1.p4()+j2.p4()
            jets_dnn = fill_jets(self.year, jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i)
        scores = []
        scores_False = []
        scores_QCD   = []
        if len(toplowpt)!=0:
            if self.year in [2018,2022,2023]:
                scores          = self.modelRes({"jet0": jets_dnn[:,0,:-2], "jet1": jets_dnn[:,1,:-2], "jet2": jets_dnn[:,2,:-2]}).numpy().flatten().tolist()
            elif self.year in [2024]:
                dnn_output      = self.modelRes({"jet": jets_dnn}).numpy() # one DNN evaluation, columns: 0 False, 1 True, 2 QCD
                scores_False    = dnn_output[:,0].flatten().tolist()
                scores_True     = dnn_output[:,1].flatten()
                scores_QCD      = dnn_output[:,2].flatten().tolist()
                scores          = scores_True.tolist() # TopScore = True output
        else:
            scores = []
        self.out.fillBranch("TopResolved_TopScore", scores)
        if self.year in [2024]:
            self.out.fillBranch("TopResolved_TopScoreFalse", scores_False)
            self.out.fillBranch("TopResolved_TopScoreQCD", scores_QCD)

        return True
