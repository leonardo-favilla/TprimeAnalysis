from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.tresholds_ml import *
import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True

dRmin = 0.8
ptmax_res = 300
ptmin_mix = 300
ptmax_mix = 500
ptmin_mer = 500
debug = False

class topselection(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch("isResolved", "I")
        self.out.branch("isMix", "I")
        self.out.branch("isMerged", "I")
        self.out.branch("MinDelta_phi", "F")
        self.out.branch("MaxEta_jet", "F")
        self.out.branch("BestTop_pt", "F")
        self.out.branch("BestTop_mass", "F")
        self.out.branch("BestTop_eta", "F")
        self.out.branch("BestTop_phi", "F")
        self.out.branch("BestTop_score", "F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        tophighpt = Collection(event, "TopHighPt")
        toplowpt = Collection(event, "TopLowPt")
        met = Object(event, "MET")
        goodjets, goodfatjets = presel(jets, fatjets)
        mindphi=1000
        maxetajet=0
        for j in goodjets:
            if j.pt<30 and j.jetId<2: continue
            dphi = abs(deltaPhi(j.phi,met.phi))
            if dphi<mindphi: mindphi = dphi
            if j.pt<50:continue
            if abs(j.eta)>maxetajet: maxetajet=abs(j.eta)
        top_res = top_select(toplowpt, trs_res, ptmin=0, ptmax=ptmax_res, dR =dRmin, category='res')
        top_mix = top_select(tophighpt, trs_mix, ptmin=ptmax_res, ptmax=ptmax_mix, dR=dRmin, category='mix')
        top_mer = top_select(goodfatjets, trs_mer, ptmin=ptmax_mix, ptmax=10000, dR=dRmin, category='mer')
        n_tres=len(top_res)
        n_tmix= len(top_mix)
        n_tmer=len(top_mer)
        if n_tres>0 and n_tmix==0 and n_tmer==0:
            isres = 1
            ismix = 0
            ismer = 0
            best_top = top_res[np.argmax([t.scoreDNN for t in top_res])]
            best_top_score = top_res[np.argmax([t.scoreDNN for t in top_res])].scoreDNN
        elif n_tres<2 and n_tmix>0 and n_tmer==0:
            isres = 0
            ismix = 1
            ismer = 0
            best_top = top_mix[np.argmax([t.score2 for t in top_mix])]
            best_top_score = top_mix[np.argmax([t.score2 for t in top_mix])].score2
        elif n_tres==0 and n_tmix<2 and n_tmer>0:
            isres = 0
            ismix = 0
            ismer = 1
            best_top = top_mer[np.argmax([t.deepTag_TvsQCD for t in top_mer])]
            best_top_score = top_mer[np.argmax([t.deepTag_TvsQCD for t in top_mer])].deepTag_TvsQCD
        else:
            isres = 0
            ismix = 0
            ismer = 0
            best_top = None
            best_top_score = None
        if best_top == None:
            return False
        else:
            self.out.fillBranch("isResolved", isres)
            self.out.fillBranch("isMix", ismix)
            self.out.fillBranch("isMerged", ismer)
            self.out.fillBranch("MinDelta_phi", mindphi)
            self.out.fillBranch("MaxEta_jet", maxetajet)
            self.out.fillBranch("BestTop_pt", best_top.pt)
            self.out.fillBranch("BestTop_mass", best_top.mass)
            self.out.fillBranch("BestTop_eta", best_top.eta)
            self.out.fillBranch("BestTop_phi", best_top.phi)
            self.out.fillBranch("BestTop_score", best_top_score)
            
            return True
