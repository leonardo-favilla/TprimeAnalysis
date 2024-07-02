import ROOT
import math
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class preselection(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("HT_eventHT",  "F") 
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        #t0 = datetime.now()
        goodEvent = False
        """process event, return True (go to next module) or False (fail, go to next event)"""
        met = Object(event, "MET")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, "PV")
        eventSum = ROOT.TLorentzVector()
        
        goodJet, goodfatjet = presel(jets, fatjets)
        isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2)
        
        isGoodEvent =  (len(goodJet)>2 or len(goodfatjet)>0) and met.pt>25 
        #((((len(goodMu) >= 1) and (len(goodEle) == 0)) or ((len(goodMu) == 0) and (len(goodEle) >= 1))) and len(goodJet)>=1)
        goodEvent = isGoodPV and isGoodEvent

        for j in goodJet:
            eventSum += j.p4()
            
        self.out.fillBranch("HT_eventHT", eventSum.Pt())
        # t1 = datetime.now()
        # print("preselection module time :", t1-t0)
        return goodEvent

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#MySelectorModuleConstr = lambda : exampleProducer(jetetaSelection= lambda j : abs(j.eta)<2.4)
