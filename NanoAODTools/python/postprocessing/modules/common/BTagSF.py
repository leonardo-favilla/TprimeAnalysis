import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from correctionlib import _core

def getFlavorBTV(flavor, verbose=False):
    '''
    Maps hadronFlavor to BTV flavor:
    Note the flavor convention: hadronFlavor is b = 5, c = 4, f = 0
    Convert them to the btagging group convention of 0, 1, 2
    '''
    flavor_btv = None
    if abs(flavor) == 5:
        flavor_btv = 5
    elif abs(flavor) == 4:
        flavor_btv = 4
    elif abs(flavor) in [0, 1, 2, 3, 21]:
        flavor_btv = 0
    else:
        if verbose > 0:
            print( "WARNING: Unknown flavor '%s', setting b-tagging SF to -1!" % repr(flavor))
        return -1.
    #print("check_the_flavour!!!")
    return flavor_btv
def eta_jet(input_eta):
    epsilon = 1.e-3
    max_abs_eta = 2.5
    if(input_eta <= -max_abs_eta):
        eta = -max_abs_eta + epsilon
    elif(input_eta >= +max_abs_eta):
        eta = +max_abs_eta - epsilon
    else: eta = input_eta
    return abs(eta)

class BTagSF(Module):
    def __init__(self, year, EE): # eratag from https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/BTV/
        if year == 2022:
            if EE:
                eratag          = "2022_Summer22EE"
            else:
                eratag          = "2022_Summer22"
        elif year == 2023:
            if EE:
                eratag          = "2023_Summer23BPix"
            else:
                eratag          = "2023_Summer23"
        else:
            print("Please specify the correct era tag for the BTag SF. 2022_Summer22 - 2022_Summer22EE - 2023_Summer23 - 2023_Summer23BPix.")
            print("Alternativly, find the era in the json file and modify PUreweight.py accordingly.")
        self.jsonfile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/"+eratag+"/btagging.json.gz"
        self.evaluator = _core.CorrectionSet.from_file(self.jsonfile)
        self.tagger = 'particleNet_shape'
        # if(year == 2022 and "22EE" in eratag):
        #     self.map_name = "Summer22EE_23Sep2023_RunEFG_V1"
        # elif(year == 2022 and not "EE" in eratag):
        #     self.map_name = "Summer22_23Sep2023_RunCD_V1"
        self.btagsf = self.evaluator[self.tagger]
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("SFbtag_nominal","F")
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets   = Collection(event, "Jet")   
        w = 1.0    
        jetSel = list(filter(lambda x: x.pt > 30 and x.jetId>=2 and x.btagPNetB>=0, jets))
        # muons  = Collection(event, "Muon")
        for j in jetSel:
            # print("central", getFlavorBTV(j.hadronFlavour, verbose=True), eta_jet(j.eta), j.pt, j.btagPNetB)
            w *=self.btagsf.evaluate("central", getFlavorBTV(j.hadronFlavour, verbose=True), eta_jet(j.eta), j.pt, j.btagPNetB)
        # print(w)
        self.out.fillBranch("SFbtag_nominal", w)

        return True