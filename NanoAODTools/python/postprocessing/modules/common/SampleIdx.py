from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import ROOT
import json
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from datetime import datetime

class SampleIdx(Module):
    def __init__(self, SampleIdx):
        self.SampleIdx = SampleIdx
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch("Sample", "I")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        self.out.fillBranch("Sample", self.SampleIdx)
        
        return True
