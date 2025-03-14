import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from correctionlib import _core


class JetVetoMaps_run3(Module):
    def __init__(self, year, EE): # eratag from https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/JME?ref_type=heads
        if year == 2022 and not EE:
            eratag = "2022_Summer22"
        elif EE:
            eratag = "2022_Summer22EE"
        self.jsonfile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+eratag+"/jetvetomaps.json.gz"
        self.evaluator = _core.CorrectionSet.from_file(self.jsonfile)
        if(year == 2022 and EE):
            self.map_name = "Summer22EE_23Sep2023_RunEFG_V1"
        elif(year == 2022 and not EE):
            self.map_name = "Summer22_23Sep2023_RunCD_V1"
        self.vetomap = self.evaluator[self.map_name]
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets   = Collection(event, "Jet")       
        muons  = Collection(event, "Muon")
        jetSel = list(filter(lambda x: x.pt > 15 and x.jetId>=2  and list(closest(x, muons))[1]<0.2 , jets))
        # print("vetomap, ", jets[0].pt)
        flag = 0
        for j in jetSel:
            if j.phi>3.141592653589793 or j.phi<-3.141592653589793:
                phi = 3.141592653589790
            else:
                phi = j.phi
            if j.eta>5.191 or j.eta<-5.191:
                eta = (j.eta/abs(j.eta))*5.190
            else:
                eta = j.eta
            flag += self.vetomap.evaluate("jetvetomap", eta, phi)
        # print("vetomap ",not flag)
        return not flag