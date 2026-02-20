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

# vars.append(variable(name = "SFbtag_nominal", title= "#omega_{b-tag SF}", nbins = 100, xmin = 0, xmax=2, MConly = True))

# vars.append(variable(name = "MET_pt", title= "p_{T}^{miss} [GeV]", nbins = 6, xmin = 200, xmax=800))
# vars.append(variable(name = "MET_phi", title= "MET #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 20, xmin = 25, xmax=850))
# vars.append(variable(name = "PuppiMET_phi", title= "MET #phi (Puppi) [GeV]", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 20, xmin = 25, xmax=850))
# vars.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))

# vars.append(variable(name = "LeadingJetPt_pt", title= "Leading Jet p_{T} [GeV]", nbins = 8, xmin = 50, xmax=850))
# vars.append(variable(name = "LeadingJetPt_eta", title= "Leading Jet #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingJetPt_phi", title= "Leading Jet #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingJetPt_mass", title= "Leading Jet mass [GeV]", nbins = 10, xmin = 50, xmax=550))

# vars.append(variable(name = "LeadingFatJetPt_pt", title= "Leading FatJet p_{T} [GeV]", nbins = 8, xmin = 50, xmax=850))
# vars.append(variable(name = "LeadingFatJetPt_eta", title= "Leading FatJet #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingFatJetPt_phi", title= "Leading FatJet #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingFatJetPt_mass", title= "Leading FatJet mass [GeV]", nbins = 10, xmin = 50, xmax=550))
# vars.append(variable(name = "LeadingFatJetPt_msoftdrop", title= "Leading FatJet m_{SD} [GeV]", nbins = 20, xmin = 70, xmax=110))
# vars.append(variable(name = "LeadingMuonPt_pt", title= "Leading Muon p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
# vars.append(variable(name = "LeadingMuonPt_eta", title= "Leading Muon #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingMuonPt_phi", title= "Leading Muon #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
# vars.append(variable(name = "LeadingElectronPt_eta", title= "Leading Electron #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingElectronPt_phi", title= "Leading Electron #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))

# vars.append(variable(name = "nTightTopMixed", title= "# Top Candidate Mix", nbins = 40, xmin = -0.5, xmax=80.5))
# vars.append(variable(name = "nTightTopResolved", title= "# Top Candidate Resolved", nbins = 25, xmin = -0.5, xmax=49.5))
# vars.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
# vars.append(variable(name = "nJetBtagMedium", title= "# b-Jet ", nbins = 5, xmin = -0.5, xmax=4.5))
# vars.append(variable(name = "nJetBtagLoose", title= "# b-Jet ", nbins = 5, xmin = -0.5, xmax=4.5))
# vars.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
# vars.append(variable(name = "MinDelta_phi", title= "min #Delta #phi", nbins = 18, xmin = 0, xmax = math.pi))
# vars.append(variable(name = "MaxEta_jet", title= "max #eta jet", nbins = 5, xmin = 0, xmax = 5, noUnOvFlowbin=True))
# vars.append(variable(name = "HT_eventHT", title= "event HT", nbins = 20, xmin = 0, xmax = 2000))
# vars.append(variable(name = "run", title= "Run Number", nbins = 5142, xmin = 315251.5, xmax = 320393.5))

# vars.append(variable(name = "MHT", title= "event HT", nbins = 20, xmin = 0, xmax = 2000))
# vars.append(variable(name = "PV_npvsGood", title= "Number of PV", nbins = 25, xmin = -0.5, xmax = 49.5))

# vars.append(variable(name = "TopMixed_TopScore_nominal", title= "Top Mixed Score", nbins = 20, xmin = 0, xmax=1, noUnOvFlowbin = True))
# vars.append(variable(name = "TopResolved_TopScore_nominal", title= "Top Resolved Score", nbins = 20, xmin = 0, xmax=1, noUnOvFlowbin = True))


# vars.append(variable(name = "EventTopCategory", title= "Top Category", nbins = 7, xmin = 0.5, xmax = 7.5))
# vars.append(variable(name = "Top_truth", title= "Top Truth", nbins = 4, xmin = -0.5, xmax = 3.5, MConly = True))
# vars.append(variable(name = "EventTopCategoryWithTruth", title= "Top Category (only true)", nbins = 4, xmin = 0.5, xmax = 4.5, MConly = True))
# vars.append(variable(name = "Top_mass", title= "Top mass [GeV]", nbins = 30, xmin = 100, xmax=250, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_pt", title= "Top p_{T} [GeV]", nbins = 30, xmin = 100, xmax=1000, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_score", title= "Top Score", nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
# vars.append(variable(name = "MT_T", title= "M_{T} [GeV]", nbins = 30, xmin = 500, xmax=2000, noUnOvFlowbin = True))
# vars.append(variable(name = "FatJet_particleNetWithMass_TvsQCD", title= "Top Score", nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
# vars.append(variable(name = "FatJet_msoftdrop_nominal", title= "FatJet m_{SD} [GeV]", nbins = 20, xmin = 70, xmax=110))


# vars.append(variable(name = "Top_isolationPtJetsdR04", title= "Top Iso p_{T} (#Delta R=0.4)", nbins = 20, xmin = 0, xmax=2, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationPtJetsdR06", title= "Top Iso p_{T} (#Delta R=0.6)", nbins = 20, xmin = 0, xmax=2, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationPtJetsdR08", title= "Top Iso p_{T} (#Delta R=0.8)", nbins = 20, xmin = 0, xmax=2, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationPtJetsdR12", title= "Top Iso p_{T} (#Delta R=1.2)", nbins = 20, xmin = 0, xmax=2, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationNJetsdR04", title= "Top Iso n_{jet}  (#Delta R=0.4)", nbins = 11, xmin = -0.5, xmax=10.5, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationNJetsdR06", title= "Top Iso n_{jet}  (#Delta R=0.6)", nbins = 11, xmin = -0.5, xmax=10.5, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationNJetsdR08", title= "Top Iso n_{jet}  (#Delta R=0.8)", nbins = 11, xmin = -0.5, xmax=10.5, noUnOvFlowbin = True))
# vars.append(variable(name = "Top_isolationNJetsdR12", title= "Top Iso n_{jet}  (#Delta R=1.2)", nbins = 11, xmin = -0.5, xmax=10.5, noUnOvFlowbin = True))


#  aggiungere plot per controllare la preselection dei fatjet
#  a bassa ed alto eta

# vars.append(variable(name = "BestTopResolved_pt",       title= "BestTopResolved p_{T} [GeV]",       nbins = 30, xmin = 100, xmax=1000, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopResolved_mass",     title= "BestTopResolved mass [GeV]",        nbins = 20, xmin = 0,   xmax=1000))
# vars.append(variable(name = "BestTopMixed_pt",          title= "BestTopMixed p_{T} [GeV]",          nbins = 30, xmin = 100, xmax=1000, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopMixed_mass",        title= "BestTopMixed mass [GeV]",           nbins = 20, xmin = 0,   xmax=1000))
# vars.append(variable(name = "BestTopMerged_pt",         title= "BestTopMerged p_{T} [GeV]",         nbins = 30, xmin = 100, xmax=1000, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopMerged_mass",       title= "BestTopMerged mass [GeV]",          nbins = 20, xmin = 0,   xmax=1000))



######## 1D variables for histos
vars2D = []

vars2D.append(variable2D(name = "nTightTopMixedVsnTightTopResolved", xname = "nTightTopMixed", yname = "nTightTopResolved", xtitle = "# of Top Mixed", ytitle = "# of Top Merged", nxbins = 6, xmin = -0.5, xmax = 5.5, nybins = 6, ymin = -0.5, ymax = 5.5))
# vars2D.append(variable2D(name = "MinDelta_phiVsHT_eventHT", xname = "MinDelta_phi", yname = "HT_eventHT", xtitle = " min #Delta #phi", ytitle = "event HT", nxbins = 18, xmin = 0, xmax = math.pi,
#                             nybins = 20, ymin = 0, ymax = 2000))

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

semilepPreselResolved   = "W_pt>150 && MET_pt>50 && dR_bJetTopLep_BestTopResolved>=1.2 && dR_muTopLep_BestTopResolved>=1.2"
semilepPreselMixed      = "W_pt>150 && MET_pt>50 && dR_bJetTopLep_BestTopMixed>=1.2 && dR_muTopLep_BestTopMixed>=1.2"
semilepPreselMerged     = "W_pt>150 && MET_pt>50 && dR_bJetTopLep_BestTopMerged>=1.2 && dR_muTopLep_BestTopMerged>=1.2"
topMixed_topmatched         = "TopMixedMatched_to_GenTop_dR0p2"
topMixed_nonmatched         = "TopMixedMatched_to_GenTop_dR0p2"

regions = {

    ################### May2024
    "btagSFcheck"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",

    # "SRmhtg100"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && MHT>100",
    # "SRmhtl100"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && MHT<100",
    # "SRnoPU"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0",
    
    # "SR"                            : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0",
    # "SR0fjets"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0",
    # "SRatleast1fjets"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0",
    # "SRTopRes"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1",
    # "SRTopRes0fjets"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1 && nForwardJet==0",
    # "SRTopResatleast1fjets"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1 && nForwardJet>0",
    # "SRTopMix"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2",
    # "SRTopMix0fjets"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2 && nForwardJet==0",
    # "SRTopMixatleast1fjets"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2 && nForwardJet>0",
    # "SRTopMer"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3",
    # "SRTopMer0fjets"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3 && nForwardJet==0",
    # "SRTopMeratleast1fjets"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3 && nForwardJet>0",
    # "SRTop"                         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=1 && EventTopCategory<=3",
    # "SRTop0fjets"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=3",
    # "SRTopatleast1fjets"            : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=3",

    # "SRTopLoose"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=4 && EventTopCategory<=6",
    # "SRTop0fjetsLoose"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=4 && EventTopCategory<=6",
    # "SRTopatleast1fjetsLoose"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=4 && EventTopCategory<=6",
    # "SRTopResLoose"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4",
    # "SRTop0fjetsResLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==4",
    # "SRTopatleast1fjetsResLoose"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==4",
    # "SRTopMixLoose"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5",
    # "SRTop0fjetsMixLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==5",
    # "SRTopatleast1fjetsMixLoose"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==5",
    # "SRTopMerLoose"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6",
    # "SRTop0fjetsMerLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==6",
    # "SRTopatleast1fjetsMerLoose"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==6",
    



    # "Presel"               : "PuppiMET_T1_pt_nominal>250",
    # "AH"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0",
    # "AH_BTagLoose"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0",
    # "AHResLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory==4",
    # "AHMixLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory==5",
    # "AHMerLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory==6",
    # "AHLoose"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=4 && EventTopCategory<=6",

    # "SL"                   : singleLep + " && nJetBtagMedium > 0",
    # "SL_metcut"            : singleLep + " && nJetBtagMedium > 0 && PuppiMET_T1_pt_nominal>250",
    # "SL_BTagLoose"         : singleLep + " && nJetBtagLoose > 0",
    # "SLResLoose"           : singleLep + " && nJetBtagMedium > 0 && EventTopCategory==4",
    # "SLMixLoose"           : singleLep + " && nJetBtagMedium > 0 && EventTopCategory==5",
    # "SLMerLoose"           : singleLep + " && nJetBtagMedium > 0 && EventTopCategory==6",
    # "SLLoose"              : singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=4 && EventTopCategory<=6",

    # "SEl"                  : singleE   + " && nJetBtagMedium > 0",
    # "SMu"                  : singleMu  + " && nJetBtagMedium > 0",

    # "AH1lWR"               : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0",
    # "AH1lWR_metcut"        : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && PuppiMET_T1_pt_nominal>250",
    # "AH1lWR_BTagLoose"     : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0",
    # "AH1lWRResLoose"       : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory==4",
    # "AH1lWRMixLoose"       : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory==5",
    # "AH1lWRMerLoose"       : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory==6",
    # "AH1lWRLoose"          : singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=4 && EventTopCategory<=6",
    # "AH1lWREl"             : singleE   + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0",
    # "AH1lWRMu"             : singleMu  + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0",

    # "AH0lZR"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0",
    # "AH0lZRResLoose"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory==4",
    # "AH0lZRMixLoose"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory==5",
    # "AH0lZRMerLoose"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory==6",
    # "AH0lZRLoose"          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=4 && EventTopCategory<=6",



    # "AH0lQCDR"             : "PuppiMET_T1_pt_nominal<250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium == 0", 
    # "NoTop"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4",


    # "PreselNoPu"           : "PuppiMET_T1_pt_nominal>250",
    # "AHNoPu"               : "PuppiMET_T1_pt_nominal>250 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0",
    # "PreselResolved"       : "PuppiMET_T1_pt_nominal>250 && EventTopCategory==1",
    # "PreselMixed"          : "PuppiMET_T1_pt_nominal>250 && EventTopCategory==2",
    # "PreselMerged"         : "PuppiMET_T1_pt_nominal>250 && EventTopCategory==3",
    # "PreselNoTop"          : "PuppiMET_T1_pt_nominal>250 && EventTopCategory==4",
    

    # "SemiLep_ResolvedLooseButNotTight_pt0to200_pass":       semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && BestTopResolved_score>=0.1422998 && BestTopResolved_score<0.29475874",
    # "SemiLep_ResolvedLooseButNotTight_pt0to200_fail":       semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && BestTopResolved_score<0.1422998",
    # "SemiLep_ResolvedLooseButNotTight_pt200to400_pass":     semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && BestTopResolved_score>=0.1422998 && BestTopResolved_score<0.29475874",
    # "SemiLep_ResolvedLooseButNotTight_pt200to400_fail":     semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && BestTopResolved_score<0.1422998",
    # "SemiLep_ResolvedLooseButNotTight_pt400to600_pass":     semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && BestTopResolved_score>=0.1422998 && BestTopResolved_score<0.29475874",
    # "SemiLep_ResolvedLooseButNotTight_pt400to600_fail":     semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && BestTopResolved_score<0.1422998",
    # "SemiLep_ResolvedLooseButNotTight_pt600to1000_pass":    semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && BestTopResolved_score>=0.1422998 && BestTopResolved_score<0.29475874",
    # "SemiLep_ResolvedLooseButNotTight_pt600to1000_fail":    semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && BestTopResolved_score<0.1422998",


    "SemiLep_MixedLooseButNotTight_pt0to200_pass":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    # "topmatched_SemiLep_MixedLooseButNotTight_pt0to200_pass":           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    # "nonmatched_SemiLep_MixedLooseButNotTight_pt0to200_pass":           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    # "other_SemiLep_MixedLooseButNotTight_pt0to200_pass":                semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    "SemiLep_MixedLooseButNotTight_pt0to200_fail":          semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && BestTopMixed_score<0.7214655876159668",
    "SemiLep_MixedLooseButNotTight_pt200to400_pass":        semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    "SemiLep_MixedLooseButNotTight_pt200to400_fail":        semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && BestTopMixed_score<0.7214655876159668",
    "SemiLep_MixedLooseButNotTight_pt400to600_pass":        semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    "SemiLep_MixedLooseButNotTight_pt400to600_fail":        semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && BestTopMixed_score<0.7214655876159668",
    "SemiLep_MixedLooseButNotTight_pt600to1000_pass":       semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && BestTopMixed_score>=0.7214655876159668 && BestTopMixed_score<0.8474694490432739",
    "SemiLep_MixedLooseButNotTight_pt600to1000_fail":       semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && BestTopMixed_score<0.7214655876159668",


    # "SemiLep_MergedLooseButNotTight_pt0to200_pass":         semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && BestTopMerged_score>=0.8 && BestTopMerged_score<0.9",
    # "SemiLep_MergedLooseButNotTight_pt0to200_fail":         semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && BestTopMerged_score<0.8",
    # "SemiLep_MergedLooseButNotTight_pt200to400_pass":       semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && BestTopMerged_score>=0.8 && BestTopMerged_score<0.9",
    # "SemiLep_MergedLooseButNotTight_pt200to400_fail":       semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && BestTopMerged_score<0.8",
    # "SemiLep_MergedLooseButNotTight_pt400to600_pass":       semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && BestTopMerged_score>=0.8 && BestTopMerged_score<0.9",
    # "SemiLep_MergedLooseButNotTight_pt400to600_fail":       semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && BestTopMerged_score<0.8",
    # "SemiLep_MergedLooseButNotTight_pt600to1000_pass":      semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && BestTopMerged_score>=0.8 && BestTopMerged_score<0.9",
    # "SemiLep_MergedLooseButNotTight_pt600to1000_fail":      semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && BestTopMerged_score<0.8",
}