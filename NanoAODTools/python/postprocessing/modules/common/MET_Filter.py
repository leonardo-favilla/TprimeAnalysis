import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MET_Filter(Module): # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Run_3_2022_and_2023_data_and_MC
    def __init__(self, year):
        self.year = year
        pass
    def endJob(self):
        pass
    def beginJob(self):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # HLT = Object(event, "HLT")
        flag = Object(event, 'Flag')
        if(self.year == 2016):
            # good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight  #to check
            good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter
        elif(self.year == 2017):
            # good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight  #to check
            good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.ecalBadCalibFilterV2
        elif(self.year == 2018):
            # good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight
            good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.ecalBadCalibFilter and flag.eeBadScFilter
        # to add elif(self.year == 2022): ....
        elif(self.year == 2022):
            # good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight
            good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.BadPFMuonDzFilter and flag.hfNoisyHitsFilter and flag.eeBadScFilter
        elif(self.year == 2023):
            # good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight
            good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.BadPFMuonDzFilter and flag.hfNoisyHitsFilter and flag.eeBadScFilter
        else:
            print ("Please specify the year: possible choices are 2016, 2017, 2018, 2022, 2023")
        
        return good_MET

MET_Filter_2016 = lambda : MET_Filter(2016)
MET_Filter_2017 = lambda : MET_Filter(2017)
MET_Filter_2018 = lambda : MET_Filter(2018)
MET_Filter_2022 = lambda : MET_Filter(2022)
MET_Filter_2023 = lambda : MET_Filter(2023)