import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from correctionlib import _core


class PUreweight(Module):
    def __init__(self, year, EE): # eratag from https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/LUM/2022_Summer22
        if year == 2022 and not EE:
            eratag = "2022_Summer22"
        elif EE:
            eratag = "2022_Summer22EE"
        self.jsonfile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/LUM/"+eratag+"/puWeights.json.gz"
        self.evaluator = _core.CorrectionSet.from_file(self.jsonfile)
        if eratag == "2022_Summer22":
            self.key = 'Collisions2022_355100_357900_eraBCD_GoldenJson'
        elif eratag == "2022_Summer22EE":
            self.key = 'Collisions2022_359022_362760_eraEFG_GoldenJson'
        else:
            print("Please specify the correct era tag for the PU weights. Possible choices are 2022_Summer22 or 2022_Summer22EE.")
            print("Alternativly, find the era in the json file and modify PUreweight.py accordingly.")
        self.puWeig = self.evaluator[self.key]
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("puWeight","F")
        self.out.branch("puWeightUp","F")
        self.out.branch("puWeightDown","F")

        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        pu = Object(event, "Pileup")
        pu_nom = self.puWeig.evaluate(pu.nTrueInt, "nominal")
        pu_up = self.puWeig.evaluate(pu.nTrueInt, "up")
        pu_down = self.puWeig.evaluate(pu.nTrueInt, "down")
        # print(pu.nTrueInt, pu_nom, pu_up, pu_down)
        self.out.fillBranch("puWeight", pu_nom)
        self.out.fillBranch("puWeightUp", pu_up)
        self.out.fillBranch("puWeightDown", pu_down)

        return True