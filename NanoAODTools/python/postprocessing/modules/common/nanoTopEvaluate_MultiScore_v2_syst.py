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
def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, scenario):
    # scenario_p4, top2j1fj, top3j1fj in tools.py (pt_<scenario>/mass_<scenario> of the jets)
    if fj == None:#3j0fj
        top_p4 = scenario_p4(j0, scenario) + scenario_p4(j1, scenario) + scenario_p4(j2, scenario)
        mass_dnn[idx_top, 0] = top_p4.M()
        mass_dnn[idx_top, 1] = top_p4.M()
        mass_dnn[idx_top, 2] = top_p4.Pt()

    elif j2 == None:#2j1fj
        top_p4 = scenario_p4(j0, scenario) + scenario_p4(j1, scenario)
        mass_dnn[idx_top, 0] = top_p4.M()
        top                  = top2j1fj(fj, j0, j1, scenario)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    else: #3j1fj
        top_p4 = scenario_p4(j0, scenario) + scenario_p4(j1, scenario) + scenario_p4(j2, scenario)
        mass_dnn[idx_top, 0] = top_p4.M()
        top                  = top3j1fj(fj, j0, j1, j2, scenario)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    return mass_dnn

def fill_fj(year, fj_dnn, fj, idx_top, scenario):
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
        fj_dnn[idx_top, 9]  = getattr(fj, "mass_"+scenario)
        fj_dnn[idx_top, 10] = fj.phi
        fj_dnn[idx_top, 11]  = getattr(fj, "pt_"+scenario)
        
    elif year in [2022,2023]: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.particleNetWithMass_QCD
        fj_dnn[idx_top, 3]  = fj.particleNetWithMass_TvsQCD
        fj_dnn[idx_top, 4]  = fj.particleNetWithMass_WvsQCD
        fj_dnn[idx_top, 5]  = fj.eta
        fj_dnn[idx_top, 6]  = getattr(fj, "mass_"+scenario)
        fj_dnn[idx_top, 7]  = fj.phi
        fj_dnn[idx_top, 8]  = getattr(fj, "pt_"+scenario)
        
    elif year in [2024]: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.globalParT3_Xbb / (fj.globalParT3_Xbb + fj.globalParT3_QCD)
        fj_dnn[idx_top, 2]  = fj.globalParT3_QCD
        fj_dnn[idx_top, 3]  = fj.globalParT3_withMassTopvsQCD
        fj_dnn[idx_top, 4]  = fj.globalParT3_withMassWvsQCD
        fj_dnn[idx_top, 5]  = fj.eta
        fj_dnn[idx_top, 6]  = getattr(fj, "mass_"+scenario)
        fj_dnn[idx_top, 7]  = fj.phi
        fj_dnn[idx_top, 8]  = getattr(fj, "pt_"+scenario)


    return fj_dnn

def fill_jets(year, jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top, scenario):
    if year in [2018]:
        jet_btagdiscr = "btagDeepB"
    elif year in [2022,2023]:
        jet_btagdiscr = "btagPNetB"
    elif year in [2024]:
        jet_btagdiscr = "btagUParTAK4B"

    jets_dnn[idx_top, 0, 0] = j0.area
    jets_dnn[idx_top, 0, 1] = getattr(j0, jet_btagdiscr)
    jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
    jets_dnn[idx_top, 0, 3] = getattr(j0, "mass_"+scenario)
    jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
    jets_dnn[idx_top, 0, 5] = getattr(j0, "pt_"+scenario)
    jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
    jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet

    jets_dnn[idx_top, 1, 0] = j1.area
    jets_dnn[idx_top, 1, 1] = getattr(j1, jet_btagdiscr)
    jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
    jets_dnn[idx_top, 1, 3] = getattr(j1, "mass_"+scenario)
    jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
    jets_dnn[idx_top, 1, 5] = getattr(j1, "pt_"+scenario)
    jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
    jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
             
    if hasattr(j2,"pt"):
        jets_dnn[idx_top, 2, 0] = j2.area
        jets_dnn[idx_top, 2, 1] = getattr(j2, jet_btagdiscr)
        jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
        jets_dnn[idx_top, 2, 3] = getattr(j2, "mass_"+scenario)
        jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
        jets_dnn[idx_top, 2, 5] = getattr(j2, "pt_"+scenario)
        jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
        jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
        
    return jets_dnn





class nanoTopevaluate_MultiScore(Module):
    def __init__(self, modelMix_path, modelRes_path, isMC=1, year=2018, scenarios=None):
        # scenarios (MC): list of JES/JER scenarios of the TopMixed/TopResolved scores,
        #                 e.g. top_scenarios(eraTag) from CMSJMECalculatorsHelper; None -> old default list
        self.modelMix_path = modelMix_path
        self.modelRes_path = modelRes_path
        self.modelMix      = tf.keras.models.load_model(modelMix_path, compile=False)
        self.modelRes      = tf.keras.models.load_model(modelRes_path, compile=False)
        self.isMC = isMC
        self.year = year
        if isMC:
            if scenarios is None: self.scenarios = ["nominal", "jesTotalup", "jesTotaldown", "jerup", "jerdown"]
            else:                 self.scenarios = list(scenarios)
        else: self.scenarios = ["nominal"]
        print("nanoTopevaluate_MultiScore scenarios:", self.scenarios)
        pass
 

    def beginJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        "Branch scores to tree"
        # self.out.branch("TopMixed_score2", "F", lenVar="nTopMixed")
        # self.out.branch(f"TopMixed_TopScore", "F", lenVar="nTopMixed")
        # Low Pt
        # self.out.branch("TopResolved_TopScore", "F", lenVar="nTopResolved")
        for scenario in self.scenarios:
            self.out.branch("TopMixed_TopScore_"+scenario, "F", lenVar="nTopMixed")
            self.out.branch("TopResolved_TopScore_"+scenario, "F", lenVar="nTopResolved")
        # 2024: the other 2 DNN outputs (False, QCD), only nominal, only to look at them (TopScore = True output)
        if self.year in [2024]:
            self.out.branch("TopMixed_TopScoreFalse_nominal", "F", lenVar="nTopMixed")
            self.out.branch("TopMixed_TopScoreQCD_nominal", "F", lenVar="nTopMixed")
            self.out.branch("TopResolved_TopScoreFalse_nominal", "F", lenVar="nTopResolved")
            self.out.branch("TopResolved_TopScoreQCD_nominal", "F", lenVar="nTopResolved")

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
            fj_dnn      = {s: np.zeros((int(len(tophighpt)), 12)) for s in self.scenarios}
        elif self.year in [2022,2023,2024]:
            fj_dnn      = {s: np.zeros((int(len(tophighpt)), 9)) for s in self.scenarios}

        jets_dnn    = {s: np.zeros((int(len(tophighpt)), 3, 8)) for s in self.scenarios}
        mass_dnn    = {s: np.zeros((len(tophighpt), 3)) for s in self.scenarios}
        for i, top in enumerate(tophighpt):
            if top.idxJet2==-1:
                j0, j1      = goodjets[top.idxJet0],goodjets[top.idxJet1]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4()+j1.p4()
                for s in self.scenarios:
                    jets_dnn[s]    = fill_jets(self.year, jets_dnn = jets_dnn[s], j0=j0, j1=j1, j2=0, sumjet = sumjet,  fj_phi= fj.phi, fj_eta=fj.eta, idx_top=i, scenario = s)
                    fj_dnn[s]      = fill_fj(self.year, fj_dnn[s], fj, i, scenario = s)
                    mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =None, fj = fj, scenario = s)
            elif top.idxFatJet==-1:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                sumjet      = j0.p4()+j1.p4()+j2.p4()
                for s in self.scenarios:
                    jets_dnn[s]    = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i, scenario = s)
                    mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =j2, fj = None, scenario = s)
            else:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4() + j1.p4() +j2.p4()
                for s in self.scenarios:
                    jets_dnn[s]    = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.phi, fj.eta, i, scenario = s)
                    fj_dnn[s]      = fill_fj(self.year, fj_dnn[s], fj, i, scenario = s)
                    mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =j2, fj = fj, scenario = s)


        ####### SCORES ####### 
        scores                  = {}
        scores_False_nominal    = []
        scores_QCD_nominal      = []
        if len(tophighpt)!=0:
            # Concatenate jets_dnn[s] along the first axis
            jets_dnn_concatenated   = np.concatenate(list(jets_dnn.values()), axis=0)
            fj_dnn_concatenated     = np.concatenate(list(fj_dnn.values()), axis=0)
            mass_dnn_concatenated   = np.concatenate(list(mass_dnn.values()), axis=0)

            if self.year in [2018,2022,2023]:
                scores_         = self.modelMix({"fatjet": fj_dnn_concatenated, "jet": jets_dnn_concatenated, "top": mass_dnn_concatenated}).numpy().flatten().tolist()
            elif self.year in [2024]:
                dnn_output      = self.modelMix({"fatjet": fj_dnn_concatenated, "jet": jets_dnn_concatenated, "top": mass_dnn_concatenated}).numpy() # one DNN evaluation, columns: 0 False, 1 True, 2 QCD
                scores_False    = dnn_output[:,0].flatten()
                scores_True     = dnn_output[:,1].flatten()
                scores_QCD      = dnn_output[:,2].flatten()
                scores_         = scores_True.tolist() # TopScore = True output

                # False and QCD outputs: only the nominal slice of the concatenation over the scenarios
                i_nominal            = self.scenarios.index("nominal")
                scores_False_nominal = scores_False[i_nominal*len(tophighpt): (i_nominal+1)*len(tophighpt)].tolist()
                scores_QCD_nominal   = scores_QCD[i_nominal*len(tophighpt): (i_nominal+1)*len(tophighpt)].tolist()

            for i, s in enumerate(self.scenarios):
                scores[s]       = scores_[0 + i*len(tophighpt): len(tophighpt)+i*len(tophighpt)]
        else:
            scores = {s : [] for s in self.scenarios}

        # Branch the scores calculated #
        for s in self.scenarios:
            self.out.fillBranch(f"TopMixed_TopScore_"+s, scores[s])
        if self.year in [2024]:
            self.out.fillBranch("TopMixed_TopScoreFalse_nominal", scores_False_nominal)
            self.out.fillBranch("TopMixed_TopScoreQCD_nominal", scores_QCD_nominal)


        # loop su Low Pt candidates per valutare lo score con i modelli corrispondenti
        jets_dnn = {s: np.zeros((int(len(toplowpt)), 3, 8)) for s in self.scenarios}        
        for i, top in enumerate(toplowpt):
            j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
            fj = ROOT.TLorentzVector()
            fj.SetPtEtaPhiM(0,0,0,0)
            sumjet = j0.p4()+j1.p4()+j2.p4()
            for s in self.scenarios:
                jets_dnn[s] = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i, scenario = s)

        scores                  = {}
        scores_False_nominal    = []
        scores_QCD_nominal      = []
        if len(toplowpt)!=0:
            jets_dnn_concatenated = np.concatenate(list(jets_dnn.values()), axis=0)
            if self.year in [2018,2022,2023]:
                scores_         = self.modelRes({"jet0": jets_dnn_concatenated[:,0,:-2], "jet1": jets_dnn_concatenated[:,1,:-2], "jet2": jets_dnn_concatenated[:,2,:-2]}).numpy().flatten().tolist()
            elif self.year in [2024]:
                dnn_output      = self.modelRes({"jet": jets_dnn_concatenated}).numpy() # one DNN evaluation, columns: 0 False, 1 True, 2 QCD
                scores_False    = dnn_output[:,0].flatten()
                scores_True     = dnn_output[:,1].flatten()
                scores_QCD      = dnn_output[:,2].flatten()
                scores_         = scores_True.tolist() # TopScore = True output

                # False and QCD outputs: only the nominal slice of the concatenation over the scenarios
                i_nominal            = self.scenarios.index("nominal")
                scores_False_nominal = scores_False[i_nominal*len(toplowpt): (i_nominal+1)*len(toplowpt)].tolist()
                scores_QCD_nominal   = scores_QCD[i_nominal*len(toplowpt): (i_nominal+1)*len(toplowpt)].tolist()

            for i, s in enumerate(self.scenarios):
                scores[s] = scores_[0 + i*len(toplowpt): len(toplowpt)+i*len(toplowpt)]
        else:
            scores = {s: [] for s in self.scenarios}

        for s in self.scenarios:
            self.out.fillBranch("TopResolved_TopScore_"+s, scores[s])
        if self.year in [2024]:
            self.out.fillBranch("TopResolved_TopScoreFalse_nominal", scores_False_nominal)
            self.out.fillBranch("TopResolved_TopScoreQCD_nominal", scores_QCD_nominal)
        return True
