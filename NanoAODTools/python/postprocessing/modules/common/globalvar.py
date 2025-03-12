from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
# from PhysicsTools.NanoAODTools.postprocessing.tresholds_ml import *
import ROOT
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from datetime import datetime

class globalvar(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch("MinDelta_phi", "F")
        self.out.branch("MaxEta_jet", "F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
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
        
        self.out.fillBranch("MinDelta_phi", mindphi)
        self.out.fillBranch("MaxEta_jet", maxetajet)
        # t1 = datetime.now()
        # print("globalvar module time :", t1-t0)
        return True
