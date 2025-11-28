from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
    getMETUnclDeltaXY,
)


from CMSJMECalculators import config as calcConfigs

def getJetMETArgsPostProcessor(jets , genjets, rho ,RawMET , CorrT1METJet, MET, lumiblock ,run ,_event, npv, isMC=True, forMET=False, addHEM2018Issue=False, NanoAODv=12):
    """ Get the input values for the jet/met variations calculator from a tree (PyROOT-style) 
        PuppiMET bool is not used in this function, to change between Puppi and chs it is sufficient to pass the right collection in the place of MET
    """
    jetpt, jeteta, jetphi, jetmass, jetrawFactor, jetarea, jetjetId = [], [], [], [], [], [], [] 
    jetmuonSubtrFactor, jetneEmEF, jetchEmEF = [], [], []
    jetgenJetIdx, jetpartonFlavour = [], []
    for j in jets:
        jetpt.append(j.pt)
        jeteta.append(j.eta)
        jetphi.append(j.phi)
        jetmass.append(j.mass)
        jetrawFactor.append(j.rawFactor)
        jetarea.append(j.area)
        if forMET:
            jetmuonSubtrFactor.append(j.muonSubtrFactor)
            jetneEmEF.append(j.neEmEF)
            jetchEmEF.append(j.chEmEF)
        if isMC:
            jetgenJetIdx.append(j.genJetIdx)
            jetpartonFlavour.append(j.partonFlavour)
        if addHEM2018Issue:
            jetjetId.append(j.jetId)
    if isMC:
        genJetpt, genJeteta, genJetphi, genJetmass = [], [], [], []
        for genjet in genjets:
            genJetpt.append(genjet.pt)
            genJeteta.append(genjet.eta)
            genJetphi.append(genjet.phi)
            genJetmass.append(genjet.mass)
    if forMET:
        corrt1metjetrawPt, corrt1metjeteta, corrt1metjetphi, corrt1metjetarea, corrt1metjetmuonSubtrFactor = [], [], [], [], []
        for cmetjet in CorrT1METJet:
            corrt1metjetrawPt.append(cmetjet.rawPt)
            corrt1metjeteta.append(cmetjet.eta)
            corrt1metjetphi.append(cmetjet.phi)
            corrt1metjetarea.append(cmetjet.area)
            corrt1metjetmuonSubtrFactor.append(cmetjet.muonSubtrFactor)

    args = [
        toRVecFloat(jetpt),
        toRVecFloat(jeteta),
        toRVecFloat(jetphi),
        toRVecFloat(jetmass),
        toRVecFloat(jetrawFactor),
        toRVecFloat(jetarea),
        ]
    if forMET:
        args += [
            toRVecFloat(jetmuonSubtrFactor),
            toRVecFloat(jetneEmEF),
            toRVecFloat(jetchEmEF),
            ]
    args.append(toRVecInt(jetjetId if addHEM2018Issue else []))
    args.append(rho if NanoAODv < 10 else rho.fixedGridRhoFastjetAll)
    # print(rho if NanoAODv < 10 else rho.fixedGridRhoFastjetAll)
    if isMC:
        args += [
            toRVecInt(jetgenJetIdx),
            toRVecInt(jetpartonFlavour),
            _event,
            int(run),
            toRVecFloat(genJetpt),
            toRVecFloat(genJeteta),
            toRVecFloat(genJetphi),
            toRVecFloat(genJetmass)
            ]
        # print(_event)
    else:
        args += [ toRVecInt([]), toRVecInt([]), 0, run, toRVecFloat([]), toRVecFloat([]), toRVecFloat([]), toRVecFloat([]) ]
    if forMET:
        args += [ RawMET.phi, RawMET.pt ]
        args += [ toRVecFloat(corrt1metjetrawPt), 
                  toRVecFloat(corrt1metjeteta), 
                  toRVecFloat(corrt1metjetphi), 
                  toRVecFloat(corrt1metjetarea), 
                  toRVecFloat(corrt1metjetmuonSubtrFactor) ]

        args += [ toRVecFloat([]), toRVecFloat([]) ]
        
        if hasattr(MET, "ptUnclusteredUp") and hasattr(MET, "phiUnclusteredUp"):
            MetUnclustEnUpDeltaX, MetUnclustEnUpDeltaY = getMETUnclDeltaXY(
                MET.pt, MET.phi, MET.ptUnclusteredUp, MET.phiUnclusteredUp)
            args += [ MetUnclustEnUpDeltaX, MetUnclustEnUpDeltaY]
        elif hasattr(MET, "MetUnclustEnUpDeltaX") is not None and getattr(MET, "MetUnclustEnUpDeltaY") is not None:
                args += [ MET.MetUnclustEnUpDeltaX, MET.MetUnclustEnUpDeltaY]
        args += [npv]
        
    # print([a for a in args])
    return args

def getFatJetArgsPostProcessor(fatjets, subjets, genjets, subgenjets, rho, run, luminosityBlock, _event, isMC=True, addHEM2018Issue=False, NanoAODv=12):
    """ Get the input values for the jet variations calculator for a fat jet from a tree (PyROOT-style) """
    fatjetpt, fatjeteta, fatjetphi, fatjetmass, fatjetrawFactor, fatjetarea, fatjetmsoftdrop, fatjetsubJetIdx1, fatjetsubJetIdx2, fatjetjetId = [], [], [], [], [], [], [], [], [], []
    fatjetgenJetAK8Idx = []
    for j in fatjets:
        fatjetpt.append(j.pt)
        fatjeteta.append(j.eta)
        fatjetphi.append(j.phi)
        fatjetmass.append(j.mass)
        fatjetrawFactor.append(j.rawFactor)
        fatjetarea.append(j.area)
        fatjetmsoftdrop.append(j.msoftdrop)
        fatjetsubJetIdx1.append(j.subJetIdx1)
        fatjetsubJetIdx2.append(j.subJetIdx2)
        fatjetjetId.append(j.jetId)
        # if isMC:
        #     fatjetgenJetAK8Idx.append(j.genJetAK8Idx)
    subjetpt, subjeteta, subjetphi, subjetmass, subjetrawFactor = [], [], [], [], []
    for j in subjets:
        subjetpt.append(j.pt)
        subjeteta.append(j.eta)
        subjetphi.append(j.phi)
        subjetmass.append(j.mass)
        subjetrawFactor.append(j.rawFactor)
    if isMC:
        genjetpt, genjeteta, genjetphi, genjetmass = [], [], [], []
        subgenjetpt, subgenjeteta, subgenjetphi, subgenjetmass = [], [], [], []
        for j in genjets:
            genjetpt.append(j.pt)
            genjeteta.append(j.eta)
            genjetphi.append(j.phi)
            genjetmass.append(j.mass)
        for j in subgenjets:
            subgenjetpt.append(j.pt)
            subgenjeteta.append(j.eta)
            subgenjetphi.append(j.phi)
            subgenjetmass.append(j.mass)  

    args = [
        toRVecFloat(fatjetpt),
        toRVecFloat(fatjeteta),
        toRVecFloat(fatjetphi),
        toRVecFloat(fatjetmass),
        toRVecFloat(fatjetrawFactor),
        toRVecFloat(fatjetarea),
        toRVecFloat(fatjetmsoftdrop),
        toRVecInt(fatjetsubJetIdx1),
        toRVecInt(fatjetsubJetIdx2),
        toRVecFloat(subjetpt),
        toRVecFloat(subjeteta),
        toRVecFloat(subjetphi),
        toRVecFloat(subjetmass),
        toRVecFloat(subjetrawFactor),
        toRVecInt(fatjetjetId if addHEM2018Issue else [])
        ]
    args.append(rho if NanoAODv < 10 else rho.fixedGridRhoFastjetAll)
    if isMC:
        args += [
            toRVecInt(fatjetgenJetAK8Idx),
            # (run<<20) + (luminosityBlock<<10) + event + 1 + ( int(fatjeteta[0]/.01) if len(fatjets) != 0 else 0),
            _event,
            int(run),
            toRVecFloat(genjetpt),
            toRVecFloat(genjeteta),
            toRVecFloat(genjetphi),
            toRVecFloat(genjetmass)
            ]
    else:

        args += [ toRVecInt([]), 0, int(run), toRVecFloat([]), toRVecFloat([]), toRVecFloat([]), toRVecFloat([]) ]

    return args

class CMSJMECalculators(Module):
    def __init__(self, jetvarcalc, jetType="AK4Puppi", isMC=True, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12):
        self.config = jetvarcalc
        self.jetType = jetType
        self.isMC = isMC
        self.forMET = forMET
        self.PuppiMET = PuppiMET
        self.addHEM2018Issue = addHEM2018Issue
        self.NanoAODv = NanoAODv
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if "AK4" in self.jetType:
            for corr in self.config.available():
                if self.forMET:
                    metbranchname = "MET"
                    if self.PuppiMET: metbranchname = "PuppiMET"
                    self.out.branch("%s_T1_pt_%s" % (metbranchname,corr), "F")
                    self.out.branch("%s_T1_phi_%s" % (metbranchname,corr), "F")
                else:
                    self.out.branch("Jet_pt_%s" %(corr), "F", lenVar="nJet")
                    self.out.branch("Jet_mass_%s" %(corr), "F", lenVar="nJet")
        elif "AK8" in self.jetType:
            for corr in self.config.available():
                self.out.branch("FatJet_pt_%s" %(corr), "F", lenVar="nFatJet")
                self.out.branch("FatJet_mass_%s" %(corr), "F", lenVar="nFatJet")
                self.out.branch("FatJet_msoftdrop_%s" %(corr), "F", lenVar="nFatJet")
        # self.out.branch("EventMass", "F")
        
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # defining collection for the arguments
        rho             = Object(event, "Rho")
        run             = event.run
        luminosityBlock = event.luminosityBlock
        _event           = event.event
        npv              = event.PV_npvsGood
        if "AK4" in self.jetType:
            jets      = Collection(event, "Jet")
            if self.isMC :genjets   = Collection(event, "GenJet")
            else: genjets = None

            if self.forMET:
                CorrT1METJet = Collection(event, "CorrT1METJet")
                if self.PuppiMET:
                    RawMET = Object(event, "RawPuppiMET")
                    MET = Object(event, "PuppiMET")
                else: 
                    RawMET = Object(event, "RawMET")
                    MET = Object(event, "MET")
            
            if self.forMET:
                var = getJetMETArgsPostProcessor(jets, genjets, rho, RawMET, CorrT1METJet, MET, luminosityBlock, run, _event, npv,
                            isMC=self.isMC, forMET=self.forMET, addHEM2018Issue=self.addHEM2018Issue, NanoAODv=self.NanoAODv)
                # var = getJetMETArgs(event, isMC = self.isMC, forMET = self.forMET, PuppiMET=self.PuppiMET, addHEM2018Issue = self.addHEM2018Issue)
            else:
                var = getJetMETArgsPostProcessor(jets, genjets, rho, None, None, None, luminosityBlock, run, _event, npv,
                            isMC=self.isMC, forMET=self.forMET, addHEM2018Issue=self.addHEM2018Issue, NanoAODv=self.NanoAODv)
                # var = getFatJetArgs(event, isMC = self.isMC, addHEM2018Issue = self.addHEM2018Issue)
        elif "AK8" in self.jetType:
            fatjets         =  Collection(event, "FatJet")
            subjets         =  Collection(event, "SubJet")
            if self.isMC:
                genjets         =  Collection(event, "GenJetAK8")
                subgenjets      =  Collection(event, "SubGenJetAK8")
            else: 
                genjets, subgenjets = None, None
            var = getFatJetArgsPostProcessor(fatjets, subjets, genjets, subgenjets, rho, run, luminosityBlock, _event, isMC=self.isMC, addHEM2018Issue=self.addHEM2018Issue, NanoAODv=self.NanoAODv)
        else:
            print("Jet type not recognized")
        res = self.config.produce(*var)

        # print(self.config.available())
        # for i in range(self.config.available().size()):
        #     print(res.pt(i))
        if "AK4" in self.jetType:
            for i, corr in enumerate(self.config.available()):
                if self.forMET:
                    metbranchname = "MET"
                    if self.PuppiMET: metbranchname = "PuppiMET"
                    self.out.fillBranch("%s_T1_pt_%s" % (metbranchname,corr), res.pt(i))
                    self.out.fillBranch("%s_T1_phi_%s" % (metbranchname,corr), res.phi(i))
                else:
                    self.out.fillBranch("Jet_pt_%s" %(corr), res.pt(i))
                    self.out.fillBranch("Jet_mass_%s" %(corr), res.mass(i))
        elif "AK8" in self.jetType:
            for i, corr in enumerate(self.config.available()):
                self.out.fillBranch("FatJet_pt_%s" %(corr), res.pt(i))
                self.out.fillBranch("FatJet_mass_%s" %(corr), res.mass(i))
                self.out.fillBranch("FatJet_msoftdrop_%s" %(corr), res.msoftdrop(i))
        return True


# DATA ["L1FastJet", "L2Relative", "L3Absolute", "L2L3Residual"], UncSources = "Total"

# Summer22EEPrompt22_JRV1_MC, Summer22EE_22Sep2023_V2_MC
# JR_Winter22Run3_V1_MC, Summer22_22Sep2023_V2_MC