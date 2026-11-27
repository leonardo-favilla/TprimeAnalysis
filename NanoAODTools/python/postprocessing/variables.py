import math
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.variable import variable, variable2D    # classes in postselection/utils/variable.py


### Definition of requeriments for plots (cut), variables and regions

requirements = ""#"leptonveto" #"leptonveto && MET_pt>150 && MinDelta_phi>0.6"

######## 1D variables for histos

vars = []

# vars.append(variable(name = "SFbtag_nominal", title= "#omega_{b-tag SF}", nbins = 100, xmin = 0, xmax=2, MConly = True))

# vars.append(variable(name = "MET_pt", title= "p_{T}^{miss} [GeV]", nbins = 6, xmin = 200, xmax=800))
# vars.append(variable(name = "MET_phi", title= "MET #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 12, xmin = 200, xmax=800))
# vars.append(variable(name = "PuppiMET_phi", title= "MET #phi (Puppi) [GeV]", nbins = 6, xmin = -math.pi, xmax=math.pi))
vars.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 13, xmin = 200, xmax=850))
vars.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))

vars.append(variable(name = "LeadingJetPt_pt", title= "Leading Jet p_{T} [GeV]", nbins = 8, xmin = 50, xmax=850))
# vars.append(variable(name = "LeadingJetPt_eta", title= "Leading Jet #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingJetPt_phi", title= "Leading Jet #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingJetPt_mass", title= "Leading Jet mass [GeV]", nbins = 10, xmin = 50, xmax=550))

vars.append(variable(name = "LeadingFatJetPt_pt", title= "Leading FatJet p_{T} [GeV]", nbins = 8, xmin = 50, xmax=850))
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

# vars.append(variable(name = "nTightTopMerged",      title= "# Top Candidate Merged",    nbins = 40, xmin = -0.5, xmax=80.5))
# vars.append(variable(name = "nTightTopMixed",       title= "# Top Candidate Mixed",     nbins = 40, xmin = -0.5, xmax=80.5))
# vars.append(variable(name = "nTightTopResolved",    title= "# Top Candidate Resolved",  nbins = 25, xmin = -0.5, xmax=49.5))
vars.append(variable(name = "nJet",                 title = "# Jet",                    nbins = 10, xmin = -0.5, xmax=9.5))
vars.append(variable(name = "nFatJet",              title = "# FatJet",                 nbins = 5,  xmin = -0.5, xmax=4.5))
vars.append(variable(name = "nGoodJet",             title = "# Good Jet",               nbins = 10, xmin = -0.5, xmax=9.5))
vars.append(variable(name = "nGoodFatJet",          title = "# Good FatJet",            nbins = 5,  xmin = -0.5, xmax=4.5))
vars.append(variable(name = "JetBTagScore",         title = "b-Jet Score",              nbins = 40, xmin = 0,    xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "nJetBtagLoose",        title = "# b-Jet (L) ",             nbins = 5,  xmin = -0.5, xmax = 4.5))
vars.append(variable(name = "nJetBtagMedium",       title = "# b-Jet (M)",              nbins = 5,  xmin = -0.5, xmax = 4.5))
vars.append(variable(name = "nJetBtagTight",        title = "# b-Jet (T)",              nbins = 5,  xmin = -0.5, xmax = 4.5))
vars.append(variable(name = "MinDelta_phi", title= "min #Delta #phi", nbins = 18, xmin = 0, xmax = math.pi))
# vars.append(variable(name = "MaxEta_jet", title= "max #eta jet", nbins = 5, xmin = 0, xmax = 5, noUnOvFlowbin=True))
vars.append(variable(name = "HT_eventHT", title= "event HT", nbins = 20, xmin = 0, xmax = 2000))
# vars.append(variable(name = "run", title= "Run Number", nbins = 5142, xmin = 315251.5, xmax = 320393.5))

vars.append(variable(name = "MHT", title= "event HT", nbins = 20, xmin = 0, xmax = 2000))
vars.append(variable(name = "PV_npvsGood", title= "Number of PV", nbins = 25, xmin = -0.5, xmax = 49.5))

vars.append(variable(name = "TopResolved_TopScore_nominal",     title= "Top Resolved Score",    nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "TopMixed_TopScore_nominal",        title= "Top Mixed Score",       nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "TopMerged_TopScore_nominal",       title= "Top Merged Score",      nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))


vars.append(variable(name = "EventTopCategory", title= "Top Category", nbins = 10, xmin = 0.5, xmax = 10.5))     # 1-3 XT, 4-6 Tight-not-XT, 7-9 Loose-not-Tight, 10 else
# vars.append(variable(name = "Top_truth", title= "Top Truth", nbins = 4, xmin = -0.5, xmax = 3.5, MConly = True))
# vars.append(variable(name = "EventTopCategoryWithTruth", title= "Top Category (only true)", nbins = 4, xmin = 0.5, xmax = 4.5, MConly = True))
vars.append(variable(name = "Top_mass",         title= "Top mass [GeV]", nbins = 30, xmin = 100, xmax=250, noUnOvFlowbin = True))
vars.append(variable(name = "Top_pt",           title= "Top p_{T} [GeV]", nbins = 30, xmin = 100, xmax=1000, noUnOvFlowbin = True))
vars.append(variable(name = "Top_score",        title= "Top Score", nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "MT_T",             title= "M_{T} [GeV]", nbins = 30, xmin = 500, xmax=2000, noUnOvFlowbin = True))
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



######## 1D variables for histos
vars2D = []

# vars2D.append(variable2D(name = "nTightTopMixedVsnTightTopResolved", xname = "nTightTopMixed", yname = "nTightTopResolved", xtitle = "# of Top Mixed", ytitle = "# of Top Merged", nxbins = 6, xmin = -0.5, xmax = 5.5, nybins = 6, ymin = -0.5, ymax = 5.5))

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
# TightMuon_Jets_minimumDistance      = "Muon_minDeltaR_fromGoodJets[TightMuon_idx[0]] >= 0.4"
# VetoMuon_Jets_minimumDistance       = "Muon_minDeltaR_fromGoodJets[VetoMuon_idx[0]] >= 0.4"
# TightElectron_Jets_minimumDistance  = "Electron_minDeltaR_fromGoodJets[TightElectron_idx[0]] >= 0.4"
# VetoElectron_Jets_minimumDistance   = "Electron_minDeltaR_fromGoodJets[VetoElectron_idx[0]] >= 0.4"
# singleLep   = "((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0 && " + TightElectron_Jets_minimumDistance + " && " + VetoElectron_Jets_minimumDistance + ")||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1 && " + TightMuon_Jets_minimumDistance + " && " + VetoMuon_Jets_minimumDistance + "))"
# singleMu    = "(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1 && " + TightMuon_Jets_minimumDistance + " && " + VetoMuon_Jets_minimumDistance + ")"
# singleE     = "(nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0 && " + TightElectron_Jets_minimumDistance + " && " + VetoElectron_Jets_minimumDistance + ")"
singleLep   = "((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1))"
singleMu    = "(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1)"
singleE     = "(nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)"
SRPresel    = "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0"

regions = {

    ### Signal Regions ###
    # EventTopCategory: 1-3 XT, 4-6 Tight-not-XT, 7-9 Loose-not-Tight (Resolved, Mixed, Merged), 10 else.
    # The "Tight" regions (SRTop*, *Tight) are Tight-not-XT (4-6), the "XT" ones 1-3, the "Loose" ones 7-9: disjoint.
    # The "TorXT" CRs are Tight including XT (1-6) = union of the "Tight" and "XT" ones.
    "SR"                            : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0",
    "SR0fjets"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0",
    "SRatleast1fjets"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0",
    "SRTopRes"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4",
    "SRTopRes0fjets"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4 && nForwardJet==0",
    "SRTopResatleast1fjets"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4 && nForwardJet>0",
    "SRTopMix"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5",
    "SRTopMix0fjets"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5 && nForwardJet==0",
    "SRTopMixatleast1fjets"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5 && nForwardJet>0",
    "SRTopMer"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6",
    "SRTopMer0fjets"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6 && nForwardJet==0",
    "SRTopMeratleast1fjets"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6 && nForwardJet>0",
    "SRTop"                         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTop0fjets"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTopatleast1fjets"            : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=4 && EventTopCategory<=6",
    # SRs with an extra-tight (XT) top, EventTopCategory 1-3 (b-tag Loose, MET>250)
    # The "TorXT" SRs are Tight including XT (union of the Tight-not-XT 4-6 and XT 1-3 ones: Res 1|4, Mix 2|5, Mer 3|6, inclusive 1-6), each right after the matching XT one.
    "SRTopResXT"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1",
    "SRTopResTorXT"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==1 || EventTopCategory==4)",
    "SRTop0fjetsResXT"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1 && nForwardJet==0",
    "SRTop0fjetsResTorXT"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet==0",
    "SRTopatleast1fjetsResXT"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1 && nForwardJet>0",
    "SRTopatleast1fjetsResTorXT"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet>0",
    "SRTopMixXT"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2",
    "SRTopMixTorXT"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==2 || EventTopCategory==5)",
    "SRTop0fjetsMixXT"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2 && nForwardJet==0",
    "SRTop0fjetsMixTorXT"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet==0",
    "SRTopatleast1fjetsMixXT"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2 && nForwardJet>0",
    "SRTopatleast1fjetsMixTorXT"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet>0",
    "SRTopMerXT"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3",
    "SRTopMerTorXT"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==3 || EventTopCategory==6)",
    "SRTop0fjetsMerXT"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3 && nForwardJet==0",
    "SRTop0fjetsMerTorXT"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet==0",
    "SRTopatleast1fjetsMerXT"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3 && nForwardJet>0",
    "SRTopatleast1fjetsMerTorXT"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet>0",
    "SRTopXT"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopTorXT"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTop0fjetsXT"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTop0fjetsTorXT"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopatleast1fjetsXT"          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopatleast1fjetsTorXT"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=6",

    ### Associated Control Regions ###
    "SRTopLoose"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTop0fjetsLoose"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopatleast1fjetsLoose"       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopResLoose"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==7",
    "SRTop0fjetsResLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==7",
    "SRTopatleast1fjetsResLoose"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==7",
    "SRTopMixLoose"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==8",
    "SRTop0fjetsMixLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==8",
    "SRTopatleast1fjetsMixLoose"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==8",
    "SRTopMerLoose"                 : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==9",
    "SRTop0fjetsMerLoose"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==9",
    "SRTopatleast1fjetsMerLoose"    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==9",

    ### Signal Regions + Associated Control Regions (b-tag Medium, MET>250) ###
    "SRBtagMedium"                                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0",
    "SR0fjetsBtagMedium"                          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0",
    "SRatleast1fjetsBtagMedium"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0",
    "SRTopResBtagMedium"                          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==4",
    "SRTopRes0fjetsBtagMedium"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==4 && nForwardJet==0",
    "SRTopResatleast1fjetsBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==4 && nForwardJet>0",
    "SRTopMixBtagMedium"                          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==5",
    "SRTopMix0fjetsBtagMedium"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==5 && nForwardJet==0",
    "SRTopMixatleast1fjetsBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==5 && nForwardJet>0",
    "SRTopMerBtagMedium"                          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==6",
    "SRTopMer0fjetsBtagMedium"                    : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==6 && nForwardJet==0",
    "SRTopMeratleast1fjetsBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==6 && nForwardJet>0",
    "SRTopBtagMedium"                             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTop0fjetsBtagMedium"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTopatleast1fjetsBtagMedium"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=4 && EventTopCategory<=6",
    # SRs with an extra-tight (XT) top, EventTopCategory 1-3 (b-tag Medium, MET>250)
    "SRTopResXTBtagMedium"                        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==1",
    "SRTopResTorXTBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==1 || EventTopCategory==4)",
    "SRTop0fjetsResXTBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==1 && nForwardJet==0",
    "SRTop0fjetsResTorXTBtagMedium"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet==0",
    "SRTopatleast1fjetsResXTBtagMedium"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==1 && nForwardJet>0",
    "SRTopatleast1fjetsResTorXTBtagMedium"        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet>0",
    "SRTopMixXTBtagMedium"                        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==2",
    "SRTopMixTorXTBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==2 || EventTopCategory==5)",
    "SRTop0fjetsMixXTBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==2 && nForwardJet==0",
    "SRTop0fjetsMixTorXTBtagMedium"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet==0",
    "SRTopatleast1fjetsMixXTBtagMedium"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==2 && nForwardJet>0",
    "SRTopatleast1fjetsMixTorXTBtagMedium"        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet>0",
    "SRTopMerXTBtagMedium"                        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==3",
    "SRTopMerTorXTBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==3 || EventTopCategory==6)",
    "SRTop0fjetsMerXTBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==3 && nForwardJet==0",
    "SRTop0fjetsMerTorXTBtagMedium"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet==0",
    "SRTopatleast1fjetsMerXTBtagMedium"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==3 && nForwardJet>0",
    "SRTopatleast1fjetsMerTorXTBtagMedium"        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet>0",
    "SRTopXTBtagMedium"                           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopTorXTBtagMedium"                        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTop0fjetsXTBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTop0fjetsTorXTBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopatleast1fjetsXTBtagMedium"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopatleast1fjetsTorXTBtagMedium"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopLooseBtagMedium"                        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTop0fjetsLooseBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopatleast1fjetsLooseBtagMedium"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopResLooseBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==7",
    "SRTop0fjetsResLooseBtagMedium"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory==7",
    "SRTopatleast1fjetsResLooseBtagMedium"        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory==7",
    "SRTopMixLooseBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==8",
    "SRTop0fjetsMixLooseBtagMedium"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory==8",
    "SRTopatleast1fjetsMixLooseBtagMedium"        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory==8",
    "SRTopMerLooseBtagMedium"                     : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==9",
    "SRTop0fjetsMerLooseBtagMedium"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory==9",
    "SRTopatleast1fjetsMerLooseBtagMedium"        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory==9",

    ### Signal Regions + Associated Control Regions (b-tag Loose, MET>200) ###
    "SRMET200"                                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0",
    "SR0fjetsMET200"                              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0",
    "SRatleast1fjetsMET200"                       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0",
    "SRTopResMET200"                              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4",
    "SRTopRes0fjetsMET200"                        : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4 && nForwardJet==0",
    "SRTopResatleast1fjetsMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==4 && nForwardJet>0",
    "SRTopMixMET200"                              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5",
    "SRTopMix0fjetsMET200"                        : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5 && nForwardJet==0",
    "SRTopMixatleast1fjetsMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==5 && nForwardJet>0",
    "SRTopMerMET200"                              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6",
    "SRTopMer0fjetsMET200"                        : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6 && nForwardJet==0",
    "SRTopMeratleast1fjetsMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==6 && nForwardJet>0",
    "SRTopMET200"                                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTop0fjetsMET200"                           : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTopatleast1fjetsMET200"                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=4 && EventTopCategory<=6",
    # SRs with an extra-tight (XT) top, EventTopCategory 1-3 (b-tag Loose, MET>200)
    "SRTopResXTMET200"                            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1",
    "SRTopResTorXTMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==1 || EventTopCategory==4)",
    "SRTop0fjetsResXTMET200"                      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1 && nForwardJet==0",
    "SRTop0fjetsResTorXTMET200"                   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet==0",
    "SRTopatleast1fjetsResXTMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==1 && nForwardJet>0",
    "SRTopatleast1fjetsResTorXTMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet>0",
    "SRTopMixXTMET200"                            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2",
    "SRTopMixTorXTMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==2 || EventTopCategory==5)",
    "SRTop0fjetsMixXTMET200"                      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2 && nForwardJet==0",
    "SRTop0fjetsMixTorXTMET200"                   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet==0",
    "SRTopatleast1fjetsMixXTMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==2 && nForwardJet>0",
    "SRTopatleast1fjetsMixTorXTMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet>0",
    "SRTopMerXTMET200"                            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3",
    "SRTopMerTorXTMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==3 || EventTopCategory==6)",
    "SRTop0fjetsMerXTMET200"                      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3 && nForwardJet==0",
    "SRTop0fjetsMerTorXTMET200"                   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet==0",
    "SRTopatleast1fjetsMerXTMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==3 && nForwardJet>0",
    "SRTopatleast1fjetsMerTorXTMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet>0",
    "SRTopXTMET200"                               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopTorXTMET200"                            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTop0fjetsXTMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTop0fjetsTorXTMET200"                      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopatleast1fjetsXTMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopatleast1fjetsTorXTMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopLooseMET200"                            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTop0fjetsLooseMET200"                      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopatleast1fjetsLooseMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopResLooseMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==7",
    "SRTop0fjetsResLooseMET200"                   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==7",
    "SRTopatleast1fjetsResLooseMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==7",
    "SRTopMixLooseMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==8",
    "SRTop0fjetsMixLooseMET200"                   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==8",
    "SRTopatleast1fjetsMixLooseMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==8",
    "SRTopMerLooseMET200"                         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && EventTopCategory==9",
    "SRTop0fjetsMerLooseMET200"                   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet==0 && EventTopCategory==9",
    "SRTopatleast1fjetsMerLooseMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagLoose>0 && nForwardJet>0 && EventTopCategory==9",

    ### Signal Regions + Associated Control Regions (b-tag Medium, MET>200) ###
    "SRBtagMediumMET200"                          : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0",
    "SR0fjetsBtagMediumMET200"                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0",
    "SRatleast1fjetsBtagMediumMET200"             : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0",
    "SRTopResBtagMediumMET200"                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==4",
    "SRTopRes0fjetsBtagMediumMET200"              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==4 && nForwardJet==0",
    "SRTopResatleast1fjetsBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==4 && nForwardJet>0",
    "SRTopMixBtagMediumMET200"                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==5",
    "SRTopMix0fjetsBtagMediumMET200"              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==5 && nForwardJet==0",
    "SRTopMixatleast1fjetsBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==5 && nForwardJet>0",
    "SRTopMerBtagMediumMET200"                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==6",
    "SRTopMer0fjetsBtagMediumMET200"              : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==6 && nForwardJet==0",
    "SRTopMeratleast1fjetsBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==6 && nForwardJet>0",
    "SRTopBtagMediumMET200"                       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTop0fjetsBtagMediumMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SRTopatleast1fjetsBtagMediumMET200"          : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=4 && EventTopCategory<=6",
    # SRs with an extra-tight (XT) top, EventTopCategory 1-3 (b-tag Medium, MET>200)
    "SRTopResXTBtagMediumMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==1",
    "SRTopResTorXTBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==1 || EventTopCategory==4)",
    "SRTop0fjetsResXTBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==1 && nForwardJet==0",
    "SRTop0fjetsResTorXTBtagMediumMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet==0",
    "SRTopatleast1fjetsResXTBtagMediumMET200"     : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==1 && nForwardJet>0",
    "SRTopatleast1fjetsResTorXTBtagMediumMET200"  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==1 || EventTopCategory==4) && nForwardJet>0",
    "SRTopMixXTBtagMediumMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==2",
    "SRTopMixTorXTBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==2 || EventTopCategory==5)",
    "SRTop0fjetsMixXTBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==2 && nForwardJet==0",
    "SRTop0fjetsMixTorXTBtagMediumMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet==0",
    "SRTopatleast1fjetsMixXTBtagMediumMET200"     : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==2 && nForwardJet>0",
    "SRTopatleast1fjetsMixTorXTBtagMediumMET200"  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==2 || EventTopCategory==5) && nForwardJet>0",
    "SRTopMerXTBtagMediumMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==3",
    "SRTopMerTorXTBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==3 || EventTopCategory==6)",
    "SRTop0fjetsMerXTBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==3 && nForwardJet==0",
    "SRTop0fjetsMerTorXTBtagMediumMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet==0",
    "SRTopatleast1fjetsMerXTBtagMediumMET200"     : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==3 && nForwardJet>0",
    "SRTopatleast1fjetsMerTorXTBtagMediumMET200"  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && (EventTopCategory==3 || EventTopCategory==6) && nForwardJet>0",
    "SRTopXTBtagMediumMET200"                     : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopTorXTBtagMediumMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTop0fjetsXTBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTop0fjetsTorXTBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopatleast1fjetsXTBtagMediumMET200"        : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SRTopatleast1fjetsTorXTBtagMediumMET200"     : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SRTopLooseBtagMediumMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTop0fjetsLooseBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopatleast1fjetsLooseBtagMediumMET200"     : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SRTopResLooseBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==7",
    "SRTop0fjetsResLooseBtagMediumMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory==7",
    "SRTopatleast1fjetsResLooseBtagMediumMET200"  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory==7",
    "SRTopMixLooseBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==8",
    "SRTop0fjetsMixLooseBtagMediumMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory==8",
    "SRTopatleast1fjetsMixLooseBtagMediumMET200"  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory==8",
    "SRTopMerLooseBtagMediumMET200"               : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && EventTopCategory==9",
    "SRTop0fjetsMerLooseBtagMediumMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet==0 && EventTopCategory==9",
    "SRTopatleast1fjetsMerLooseBtagMediumMET200"  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon ==0) && nJetBtagMedium>0 && nForwardJet>0 && EventTopCategory==9",
    


    ### Control Regions (MET>250) ###
    "btagSFcheck"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",
    "STnonTTbar"                    : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && (nJetBtagMedium==1 && nJetBtagLoose==1) && EventTopCategory>=4 && EventTopCategory<=6",
    "STnonTTbarXT"                  : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && (nJetBtagMedium==1 && nJetBtagLoose==1) && EventTopCategory>=1 && EventTopCategory<=3",
    "STnonTTbarTorXT"               : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && (nJetBtagMedium==1 && nJetBtagLoose==1) && EventTopCategory>=1 && EventTopCategory<=6",

    "AH"                            : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0",
    "AHBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0",
    "AHBtagTight"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagTight > 0",
    "AHTight"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AHLoose"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AHXT"                          : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AHTorXT"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=6",
    "AHTightBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AHLooseBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AHXTBtagMedium"                : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AHTorXTBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=6",

    "SL"                            : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0",
    "SLBtagMedium"                  : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagMedium > 0",
    "SLBtagTight"                   : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagTight > 0",
    "SLTight"                       : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SLLoose"                       : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SLXT"                          : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SLTorXT"                       : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SLTightBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SLLooseBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SLXTBtagMedium"                : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SLTorXTBtagMedium"             : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=6",

    "AH1lWR"                        : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0",
    "AH1lWRBtagMedium"              : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0",
    "AH1lWRBtagTight"               : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagTight == 0",
    "AH1lWRTight"                   : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH1lWRLoose"                   : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH1lWRXT"                      : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH1lWRTorXT"                   : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=1 && EventTopCategory<=6",
    "AH1lWRTightBtagMedium"         : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH1lWRLooseBtagMedium"         : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH1lWRXTBtagMedium"            : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH1lWRTorXTBtagMedium"         : "PuppiMET_T1_pt_nominal>250 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=1 && EventTopCategory<=6",

    "AH0lZR"                        : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0",
    "AH0lZRBtagMedium"              : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0",
    "AH0lZRBtagTight"               : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagTight==0",
    "AH0lZRTight"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH0lZRLoose"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH0lZRXT"                      : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH0lZRTorXT"                   : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=1 && EventTopCategory<=6",
    "AH0lZRTightBtagMedium"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH0lZRLooseBtagMedium"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH0lZRXTBtagMedium"            : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH0lZRTorXTBtagMedium"         : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=1 && EventTopCategory<=6",

    ### Control Regions (MET>200) ###
    "btagSFcheckMET200"             : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",
    "STnonTTbarMET200"              : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && (nJetBtagMedium==1 && nJetBtagLoose==1) && EventTopCategory>=4 && EventTopCategory<=6",
    "STnonTTbarXTMET200"            : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && (nJetBtagMedium==1 && nJetBtagLoose==1) && EventTopCategory>=1 && EventTopCategory<=3",
    "STnonTTbarTorXTMET200"         : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && (nJetBtagMedium==1 && nJetBtagLoose==1) && EventTopCategory>=1 && EventTopCategory<=6",

    "AHMET200"                      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0",
    "AHBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0",
    "AHBtagTightMET200"             : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagTight > 0",
    "AHTightMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AHLooseMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AHXTMET200"                    : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AHTorXTMET200"                 : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=6",
    "AHTightBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AHLooseBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AHXTBtagMediumMET200"          : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AHTorXTBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi<0.6 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=6",

    "SLMET200"                      : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagLoose > 0",
    "SLBtagMediumMET200"            : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagMedium > 0",
    "SLBtagTightMET200"             : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagTight > 0",
    "SLTightMET200"                 : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SLLooseMET200"                 : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SLXTMET200"                    : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SLTorXTMET200"                 : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagLoose > 0 && EventTopCategory>=1 && EventTopCategory<=6",
    "SLTightBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "SLLooseBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "SLXTBtagMediumMET200"          : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "SLTorXTBtagMediumMET200"       : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nJetBtagMedium > 0 && EventTopCategory>=1 && EventTopCategory<=6",

    "AH1lWRMET200"                  : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0",
    "AH1lWRBtagMediumMET200"        : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0",
    "AH1lWRBtagTightMET200"         : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagTight == 0",
    "AH1lWRTightMET200"             : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH1lWRLooseMET200"             : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH1lWRXTMET200"                : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH1lWRTorXTMET200"             : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagLoose == 0 && EventTopCategory>=1 && EventTopCategory<=6",
    "AH1lWRTightBtagMediumMET200"   : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH1lWRLooseBtagMediumMET200"   : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH1lWRXTBtagMediumMET200"      : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH1lWRTorXTBtagMediumMET200"   : "PuppiMET_T1_pt_nominal>200 && " + singleLep + " && nGoodJet>=3 && MT<=140 && nJetBtagMedium == 0 && EventTopCategory>=1 && EventTopCategory<=6",

    "AH0lZRMET200"                  : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0",
    "AH0lZRBtagMediumMET200"        : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0",
    "AH0lZRBtagTightMET200"         : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagTight==0",
    "AH0lZRTightMET200"             : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH0lZRLooseMET200"             : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH0lZRXTMET200"                : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH0lZRTorXTMET200"             : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagLoose==0 && EventTopCategory>=1 && EventTopCategory<=6",
    "AH0lZRTightBtagMediumMET200"   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=4 && EventTopCategory<=6",
    "AH0lZRLooseBtagMediumMET200"   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=7 && EventTopCategory<=9",
    "AH0lZRXTBtagMediumMET200"      : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=1 && EventTopCategory<=3",
    "AH0lZRTorXTBtagMediumMET200"   : "PuppiMET_T1_pt_nominal>200 && MinDelta_phi>2.5 && (nVetoMuon+nVetoElectron) == 0 && nJetBtagMedium==0 && EventTopCategory>=1 && EventTopCategory<=6",
}