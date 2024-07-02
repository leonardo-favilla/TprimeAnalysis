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
    if fj == None:#3j0fj
        j0_p4 = ROOT.TLorentzVector()
        j1_p4 = ROOT.TLorentzVector()
        j2_p4 = ROOT.TLorentzVector()
        if scenario == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif scenario == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup) 
        elif scenario == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif scenario == "jerup":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif scenario == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        top_p4 = j0_p4+j1_p4+j2_p4
        mass_dnn[idx_top, 0] = top_p4.M()
        mass_dnn[idx_top, 1] = top_p4.M()
        mass_dnn[idx_top, 2] = top_p4.Pt()

    elif j2 == None:#2j1fj
        j0_p4 = ROOT.TLorentzVector()
        j1_p4 = ROOT.TLorentzVector()
        if scenario == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        elif scenario == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        elif scenario == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        elif scenario == "jerup":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        elif scenario == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        top_p4 = j0_p4+j1_p4
        mass_dnn[idx_top, 0] = top_p4.M()
        top                  = top2j1fj(fj, j0, j1, scenario)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    else: #3j1fj
        j0_p4 = ROOT.TLorentzVector()
        j1_p4 = ROOT.TLorentzVector()
        j2_p4 = ROOT.TLorentzVector()
        if scenario == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif scenario == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup) 
        elif scenario == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif scenario == "jerup":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif scenario == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        top_p4 = j0_p4+j1_p4+j2_p4
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
        fj_dnn[idx_top, 10] = fj.phi
        if scenario == "nominal":
            fj_dnn[idx_top, 9]  = fj.mass_nominal
            fj_dnn[idx_top, 11] = fj.pt_nominal
        elif scenario == "jesTotalup":
            fj_dnn[idx_top, 9]  = fj.mass_jesTotalup
            fj_dnn[idx_top, 11] = fj.pt_jesTotalup
        elif scenario == "jesTotaldown":
            fj_dnn[idx_top, 9]  = fj.mass_jesTotaldown
            fj_dnn[idx_top, 11] = fj.pt_jesTotaldown
        elif scenario == "jerup":
            fj_dnn[idx_top, 9]  = fj.mass_jerup
            fj_dnn[idx_top, 11] = fj.pt_jerup
        elif scenario == "jerdown":
            fj_dnn[idx_top, 9]  = fj.mass_jerdown
            fj_dnn[idx_top, 11] = fj.pt_jerdown

    elif year==2022: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.particleNetWithMass_QCD
        fj_dnn[idx_top, 3]  = fj.particleNetWithMass_TvsQCD
        fj_dnn[idx_top, 4]  = fj.particleNetWithMass_WvsQCD
        fj_dnn[idx_top, 5]  = fj.eta
        fj_dnn[idx_top, 7]  = fj.phi
        if scenario == "nominal":
            fj_dnn[idx_top, 6]  = fj.mass_nominal
            fj_dnn[idx_top, 8] = fj.pt_nominal
        elif scenario == "jesTotalup":
            fj_dnn[idx_top, 6]  = fj.mass_jesTotalup
            fj_dnn[idx_top, 8] = fj.pt_jesTotalup
        elif scenario == "jesTotaldown":
            fj_dnn[idx_top, 6]  = fj.mass_jesTotaldown
            fj_dnn[idx_top, 8] = fj.pt_jesTotaldown
        elif scenario == "jerup":
            fj_dnn[idx_top, 6]  = fj.mass_jerup
            fj_dnn[idx_top, 8] = fj.pt_jerup
        elif scenario == "jerdown":
            fj_dnn[idx_top, 6]  = fj.mass_jerdown
            fj_dnn[idx_top, 8] = fj.pt_jerdown
    return fj_dnn

def fill_jets(year, jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top, scenario): 
    if year==2018:
        jets_dnn[idx_top, 0, 0] = j0.area
        jets_dnn[idx_top, 0, 1] = j0.btagDeepB
        jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
        jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
        jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
        jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet

        jets_dnn[idx_top, 1, 0] = j1.area
        jets_dnn[idx_top, 1, 1] = j1.btagDeepB
        jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
        jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
        jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
        jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
        if scenario == "nominal":
            jets_dnn[idx_top, 0, 3] = j0.mass_nominal
            jets_dnn[idx_top, 0, 5] = j0.pt_nominal
            jets_dnn[idx_top, 1, 3] = j1.mass_nominal
            jets_dnn[idx_top, 1, 5] = j1.pt_nominal
        elif scenario == "jesTotalup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotalup
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotalup
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotalup
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotalup
        elif scenario == "jesTotaldown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotaldown
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotaldown
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotaldown
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotaldown
        elif scenario == "jerup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerup
            jets_dnn[idx_top, 0, 5] = j0.pt_jerup
            jets_dnn[idx_top, 1, 3] = j1.mass_jerup
            jets_dnn[idx_top, 1, 5] = j1.pt_jerup
        elif scenario == "jerdown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerdown
            jets_dnn[idx_top, 0, 5] = j0.pt_jerdown
            jets_dnn[idx_top, 1, 3] = j1.mass_jerdown
            jets_dnn[idx_top, 1, 5] = j1.pt_jerdown
                        
        if hasattr(j2,"pt"):
            jets_dnn[idx_top, 2, 0] = j2.area
            jets_dnn[idx_top, 2, 1] = j2.btagDeepB
            jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
            jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
            jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
            jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
            if scenario == "nominal":
                jets_dnn[idx_top, 2, 3] = j2.mass_nominal
                jets_dnn[idx_top, 2, 5] = j2.pt_nominal
            elif scenario == "jesTotalup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotalup
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotalup
            elif scenario == "jesTotaldown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotaldown
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotaldown
            elif scenario == "jerup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerup
                jets_dnn[idx_top, 2, 5] = j2.pt_jerup
            elif scenario == "jerdown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerdown
                jets_dnn[idx_top, 2, 5] = j2.pt_jerdown

    elif year==2022:
        jets_dnn[idx_top, 0, 0] = j0.area
        jets_dnn[idx_top, 0, 1] = j0.btagPNetB
        jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
        jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
        jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
        jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet

        jets_dnn[idx_top, 1, 0] = j1.area
        jets_dnn[idx_top, 1, 1] = j1.btagPNetB
        jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
        jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
        jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
        jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
        if scenario == "nominal":
            jets_dnn[idx_top, 0, 3] = j0.mass_nominal
            jets_dnn[idx_top, 0, 5] = j0.pt_nominal
            jets_dnn[idx_top, 1, 3] = j1.mass_nominal
            jets_dnn[idx_top, 1, 5] = j1.pt_nominal
        elif scenario == "jesTotalup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotalup
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotalup
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotalup
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotalup
        elif scenario == "jesTotaldown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotaldown
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotaldown
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotaldown
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotaldown
        elif scenario == "jerup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerup
            jets_dnn[idx_top, 0, 5] = j0.pt_jerup
            jets_dnn[idx_top, 1, 3] = j1.mass_jerup
            jets_dnn[idx_top, 1, 5] = j1.pt_jerup
        elif scenario == "jerdown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerdown
            jets_dnn[idx_top, 0, 5] = j0.pt_jerdown
            jets_dnn[idx_top, 1, 3] = j1.mass_jerdown
            jets_dnn[idx_top, 1, 5] = j1.pt_jerdown
                        
        if hasattr(j2,"pt"):
            jets_dnn[idx_top, 2, 0] = j2.area
            jets_dnn[idx_top, 2, 1] = j2.btagPNetB
            jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
            jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
            jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
            jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
            if scenario == "nominal":
                jets_dnn[idx_top, 2, 3] = j2.mass_nominal
                jets_dnn[idx_top, 2, 5] = j2.pt_nominal
            elif scenario == "jesTotalup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotalup
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotalup
            elif scenario == "jesTotaldown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotaldown
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotaldown
            elif scenario == "jerup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerup
                jets_dnn[idx_top, 2, 5] = j2.pt_jerup
            elif scenario == "jerdown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerdown
                jets_dnn[idx_top, 2, 5] = j2.pt_jerdown
    return jets_dnn


# Leo's models #
# path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models"
# path_to_model_folder    = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models" % os.environ["CMSSW_BASE"]

# modelli da usare
# path_to_model_folder    = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/" % os.environ["CMSSW_BASE"]
# folder_model_antimo     = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/" % os.environ["CMSSW_BASE"]
path_to_model_folder    = "/afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/python/postprocessing/data/dict_tresholds/"
folder_model_antimo     = "/afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/python/postprocessing/data/dict_tresholds/"

# antimo_model_name_H     = "DNN_phase2_test2.h5"#"DNN_withtopmass_phase2.h5"
# antimo_model_name_L     = "DNN_phase1_test_lowpt_DNN.h5"

TopMixed2022            = "model_TopMixed_2022_p2.h5"
TopMixed2018            = "model_base2.h5"
TopResolved2022         = "model_TopResolved_2022.h5"
TopResolved2018         = "DNN_phase1_test_lowpt_DNN.h5"

keys                    = ["base2"]

models                  = {}
# models["base"]          = tf.keras.models.load_model(f"{path_to_model_folder}/model_base.h5")
# print(path_to_model_folder+"model_base2.h5")
models["TopMixed_2018"]         = tf.keras.models.load_model(path_to_model_folder+TopMixed2018)
models["TopMixed_2022"]         = tf.keras.models.load_model(path_to_model_folder+TopMixed2022)
models["TopResolved_2018"]      = tf.keras.models.load_model(path_to_model_folder+TopResolved2018)
models["TopResolved_2022"]      = tf.keras.models.load_model(path_to_model_folder+TopResolved2022)
# models["score2"]        = tf.keras.models.load_model(folder_model_antimo+antimo_model_name_H)

# for key in keys:
#     models[key]         = tf.keras.models.load_model(f"{path_to_model_folder}/model_{key}.h5")






class nanoTopevaluate_MultiScore(Module):
    def __init__(self, isMC=1, year=2018):
        self.isMC = isMC
        self.year = year
        if isMC : self.scenarios = ["nominal", "jesTotalup", "jesTotaldown", "jerup", "jerdown"]
        else: self.scenarios = ["nominal"]
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
            fj_dnn      = { s: np.zeros((int(len(tophighpt)), 12)) for s in self.scenarios}
        elif self.year == 2022:
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
        scores = []
        if len(tophighpt)!=0:
            # top_score2      = models["score2"].predict({"fatjet":fj_dnn, "jet": jets_dnn,  "top_mass": mass_dnn[:,:2]}).flatten().tolist()
            if self.year == 2018:
                model = models["TopMixed_2018"]
            elif self.year == 2022 or self.year == 2023:
                model = models["TopMixed_2022"]
            # print(fj_dnn.shape, jets_dnn.shape, mass_dnn.shape)

            # Concatenate jets_dnn[s] along the first axis
            jets_dnn_concatenated = np.concatenate(list(jets_dnn.values()), axis=0)
            fj_dnn_concatenated = np.concatenate(list(fj_dnn.values()), axis=0)
            mass_dnn_concatenated = np.concatenate(list(mass_dnn.values()), axis=0)

            scores_ = model({"fatjet": fj_dnn_concatenated, "jet": jets_dnn_concatenated, "top": mass_dnn_concatenated}).numpy().flatten().tolist()
            scores = {}
            for i, s in enumerate(self.scenarios):
                scores[s] = scores_[0 + i*len(tophighpt): len(tophighpt)+i*len(tophighpt)]
        else:
            # top_score2  = []
            scores = {s : [] for s in self.scenarios}

        # Branch the scores calculated #
        # self.out.fillBranch("TopHighPt_score2", top_score2)
        for s in self.scenarios:
            self.out.fillBranch(f"TopMixed_TopScore_"+s, scores[s])


        # loop su Low Pt candidates per valutare lo score con i modelli corrispondenti
        
        jets_dnn = {s: np.zeros((int(len(toplowpt)), 3, 8)) for s in self.scenarios}        
        for i, top in enumerate(toplowpt):
            j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
            fj = ROOT.TLorentzVector()
            fj.SetPtEtaPhiM(0,0,0,0)
            sumjet = j0.p4()+j1.p4()+j2.p4()
            for s in self.scenarios:
                jets_dnn[s] = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i, scenario = s)

        if len(toplowpt)!=0:
            if self.year == 2018:
                modelRes = models["TopResolved_2018"]
            elif self.year == 2022 or self.year == 2023:
                modelRes = models["TopResolved_2022"]
            # Concatenate jets_dnn[s] along the first axis
            jets_dnn_concatenated = np.concatenate(list(jets_dnn.values()), axis=0)
            top_score_DNN_ = modelRes({"jet0": jets_dnn_concatenated[:,0,:-2], "jet1": jets_dnn_concatenated[:,1,:-2], "jet2": jets_dnn_concatenated[:,2,:-2]}).numpy().flatten().tolist()
            top_score_DNN = {}
            for i, s in enumerate(self.scenarios):
                top_score_DNN[s] = top_score_DNN_[0 + i*len(toplowpt): len(toplowpt)+i*len(toplowpt)]
        else:
            top_score_DNN = {s: [] for s in self.scenarios}

        for s in self.scenarios:
            self.out.fillBranch("TopResolved_TopScore_"+s, top_score_DNN[s])
        return True
