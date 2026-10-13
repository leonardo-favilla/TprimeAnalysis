import math
import numpy as np
class variable(object):
    def __init__(self, name, title, taglio=None, nbins=None, xmin=None, xmax=None, xarray=None, MConly = False, noUnOvFlowbin = False):
        self._name = name
        self._title = title
        self._taglio = taglio
        self._nbins = nbins
        self._xmin = xmin
        self._xmax = xmax
        self._xarray = xarray
        self._MConly = MConly
        self._noUnOvFlowbin = noUnOvFlowbin
    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._title)+'\",\"'+str(self._taglio)+'\",'+str(self._nbins)+','+str(self._xmin)+','+str(self._xmax)
#variable("Top_pt", "Top p_T [GeV]", nbins = 50, xmin = 0 , xmax = 1000)
class variable2D(object):
    def __init__(self, name, xname, yname, xtitle, ytitle, taglio=None, nxbins=None, xmin=None, xmax=None, xarray=None, 
                    nybins=None, ymin=None, ymax=None, yarray=None):
        self._name = name
        self._xname = xname
        self._yname = yname
        self._xtitle = xtitle
        self._ytitle = ytitle
        self._taglio = taglio
        self._nxbins = nxbins
        self._xmin = xmin
        self._xmax = xmax
        self._xarray = xarray
        self._nybins = nybins
        self._ymin = ymin
        self._ymax = ymax
        self._yarray = yarray
    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._xtitle)+'\",\"'+str(self._ytitle)+'\",\"'+str(self._taglio)+'\",'+str(self._nxbins)+','+str(self._xmin)+','+str(self._xmax)+','+str(self._nybins)+','+str(self._ymin)+','+str(self._ymax)


### Definition of requeriments for plots (cut), variables and regions

requirements = ""#"leptonveto" #"leptonveto && MET_pt>150 && MinDelta_phi>0.6"

######## 1D variables for histos

vars = []

vars.append(variable(name = "PuppiMET_T1_pt_nominal",   title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 12, xmin = 250,     xmax=850))
vars.append(variable(name = "nJet",                     title = "# Jet",                            nbins = 10, xmin = -0.5,    xmax=9.5))
vars.append(variable(name = "nJetBtagLoose",            title = "# b-Jet (L)",                      nbins = 5,  xmin = -0.5,    xmax = 4.5))
vars.append(variable(name = "MT_T",                     title= "M_{T} [GeV]",                       nbins = 30, xmin = 500,     xmax=2000, noUnOvFlowbin = True))

######## 2D variables for histos
vars2D = []


################## December 2023    
nocut = ""
hemveto = "(isMC || (year != 2018) || (HEMVeto || run<319077.))" 
met_filters = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_ecalBadCalibFilter && Flag_eeBadScFilter)"
hlt_filters = "(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight || HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200 || HLT_IsoMu24)"
hlt2_filters = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hlt3_filters = "(HLT_PFMET140_PFMHT140_IDTight || HLT_PFMETNoMu140_PFMHTNoMu140_IDTight)"
metcut = "(MET_pt>250)"
hltmet_filters = "(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hltmu_filters = "(HLT_IsoMu24)"
################## January 2024
singleLep   = "((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1))"
singleMu    = "(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1)"
singleE     = "(nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)"
SRPresel    = "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0"

regions = {

    ################### May2024
    "btagSFcheck"          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",
    # "SRTopLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0",
    "AHTight"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AHLoose"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=4 && EventTopCategory<=6",

    "SL"                   : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0",
    "SLTight"              : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SLLoose"              : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=4 && EventTopCategory<=6",

    "AH1lWR"               : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0",
    "AH1lWRTight"          : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH1lWRLoose"          : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=4 && EventTopCategory<=6",

    "AH0lZR"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0",
    "AH0lZRTight"          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH0lZRLoose"          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=4 && EventTopCategory<=6",

}