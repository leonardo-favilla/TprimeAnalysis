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
vars.append(variable(name = "PuppiMET_T1_pt_nominal",   title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 20, xmin = 50,          xmax=850))
vars.append(variable(name = "PuppiMET_T1_phi_nominal",  title= "Puppi MET #phi nominal",            nbins = 6,  xmin = -math.pi,    xmax=math.pi))

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
# vars.append(variable(name = "nJet",             title = "# Jet",            nbins = 10, xmin = -0.5, xmax=9.5))
# vars.append(variable(name = "nGoodJet",         title = "# GoodJet",        nbins = 10, xmin = -0.5, xmax=9.5))
# vars.append(variable(name = "nFatJet",          title = "# FatJet",         nbins = 5,  xmin = -0.5, xmax=4.5))
# vars.append(variable(name = "nGoodFatJet",      title = "# GoodFatJet",     nbins = 5,  xmin = -0.5, xmax=4.5))
vars.append(variable(name = "Jet_btagPNetB",    title = "jet btag score",   nbins = 20, xmin = 0,    xmax = 1,    noUnOvFlowbin = True))
# vars.append(variable(name = "nJetBtagLoose",    title = "# b-Jet (L) ",     nbins = 5,  xmin = -0.5, xmax = 4.5))
# vars.append(variable(name = "nJetBtagMedium",   title = "# b-Jet (M)",      nbins = 5,  xmin = -0.5, xmax = 4.5))
# vars.append(variable(name = "nJetBtagTight",    title = "# b-Jet (T)",      nbins = 5,  xmin = -0.5, xmax = 4.5))
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

# vars.append(variable(name="dR_muTopLep_bJetTopLep",   title="dR(#muTopLep, bTopLep)",            nbins=20, xmin=0,          xmax=math.pi,   noUnOvFlowbin = True))
# vars.append(variable(name="dPhi_muTopLep_MET",        title="d#Phi(#muTopLep, MET)",             nbins=20, xmin=-math.pi,   xmax=math.pi,   noUnOvFlowbin = True))
# vars.append(variable(name="dPhi_bJetTopLep_MET",      title="d#Phi(bTopLep, MET)",               nbins=20, xmin=-math.pi,   xmax=math.pi,   noUnOvFlowbin = True))

vars.append(variable(name="BestTopResolved_mass",     title="BestTopResolved mass [GeV]",        nbins=20, xmin=0,          xmax=1000,      noUnOvFlowbin = True))
vars.append(variable(name="BestTopMixed_mass",        title="BestTopMixed mass [GeV]",           nbins=20, xmin=0,          xmax=1000,      noUnOvFlowbin = True))
vars.append(variable(name="BestTopMerged_mass",       title="BestTopMerged mass [GeV]",          nbins=20, xmin=0,          xmax=1000,      noUnOvFlowbin = True))

# vars.append(variable(name="W_pt",                     title="W p_{T} [GeV]",                     nbins=10, xmin=0,          xmax=250,       noUnOvFlowbin = True))
vars.append(variable(name="MT_W",                     title="M^{W}_{T} [GeV]",                   nbins=10, xmin=0,          xmax=250,       noUnOvFlowbin = True))
# vars.append(variable(name="MT_lb",                    title="M^{lb}_{T} [GeV]",                  nbins=20, xmin=0,          xmax=500,       noUnOvFlowbin = True))
# vars.append(variable(name="MT_toplep",                title="M^{TopLep}_{T} [GeV]",              nbins=20, xmin=0,          xmax=500,       noUnOvFlowbin = True))

vars.append(variable(name="TopLep_mass",              title="TopLep mass [GeV]",                 nbins=20, xmin=0,          xmax=1000,      noUnOvFlowbin = True))
vars.append(variable(name="TopLep_pt",                title="TopLep p_{T} [GeV]",                nbins=20, xmin=0,          xmax=1000,      noUnOvFlowbin = True))
vars.append(variable(name="TopLep_mtw",               title="TopLep mtw [GeV]",                  nbins=20, xmin=0,          xmax=1000,      noUnOvFlowbin = True))
vars.append(variable(name="TopLep_eta",               title="TopLep #eta",                       nbins=20, xmin=-4,         xmax=4,         noUnOvFlowbin = True))
vars.append(variable(name="TopLep_phi",               title="TopLep #phi",                       nbins=20, xmin=-math.pi,   xmax=math.pi,   noUnOvFlowbin = True))

######## 1D variables for histos
vars2D = []

# vars2D.append(variable2D(name = "nTightTopMixedVsnTightTopResolved", xname = "nTightTopMixed", yname = "nTightTopResolved", xtitle = "# of Top Mixed", ytitle = "# of Top Merged", nxbins = 6, xmin = -0.5, xmax = 5.5, nybins = 6, ymin = -0.5, ymax = 5.5))
# vars2D.append(variable2D(name = "MinDelta_phiVsHT_eventHT", xname = "MinDelta_phi", yname = "HT_eventHT", xtitle = " min #Delta #phi", ytitle = "event HT", nxbins = 18, xmin = 0, xmax = math.pi,
#                             nybins = 20, ymin = 0, ymax = 2000))


####################################
######## REGIONS DEFINITION ########
####################################

# Top_Resolved_wp = {"10%": 0.1422998,           "5%": 0.29475874,               "1%": 0.59264845,           "0.1%": 0.86580896}
# Top_Mixed_wp    = {"10%": 0.7214655876159668,  "5%": 0.8474694490432739,       "1%": 0.9436638951301575,   "0.1%": 0.9789741635322571}
# Top_Merged_wp   = {"10%": 0.8,                 "5%": 0.9,                      "1%": 1.,                   "0.1%": 1.}
Top_Resolved_wp             = { "10%": 0.425, "5%": 0.625,}
Top_Mixed_wp                = { "10%": 0.900, "5%": 0.950,}
Top_Merged_wp               = { "10%": 0.075, "5%": 0.250,}


semilepPresel               = ""
semilepPresel_njg2_nfjeq0   = "nGoodJet>2 && nGoodFatJet==0"
semilepPresel_njfgeq1       = "nGoodFatJet>0"
semilepPresel_MET           = "PuppiMET_T1_pt_nominal>50"
semilepPresel_MET_W         = "W_pt>150 && PuppiMET_T1_pt_nominal>50"
semilepPreselResolved       = "W_pt>150 && PuppiMET_T1_pt_nominal>50 && dR_bJetTopLep_BestTopResolved>=1.2 && dR_muTopLep_BestTopResolved>=1.2"
semilepPreselMixed          = "W_pt>150 && PuppiMET_T1_pt_nominal>50 && dR_bJetTopLep_BestTopMixed>=1.2 && dR_muTopLep_BestTopMixed>=1.2"
semilepPreselMerged         = "W_pt>150 && PuppiMET_T1_pt_nominal>50 && dR_bJetTopLep_BestTopMerged>=1.2 && dR_muTopLep_BestTopMerged>=1.2"

topResolved_topmatched      = "TopResolvedMatched_to_GenTop_dR0p2"
topResolved_nonmatched      = "!TopResolvedMatched_to_GenTop_dR0p2"
topResolved_other           = "!TopResolvedMatched_to_GenTop_dR0p2"
topMixed_topmatched         = "TopMixedMatched_to_GenTop_dR0p2"
topMixed_nonmatched         = "!TopMixedMatched_to_GenTop_dR0p2"
topMixed_other              = "!TopMixedMatched_to_GenTop_dR0p2"
topMerged_topmatched        = "TopMergedMatched_to_GenTop_dR0p2"
topMerged_nonmatched        = "!TopMergedMatched_to_GenTop_dR0p2"
topMerged_other             = "!TopMergedMatched_to_GenTop_dR0p2"

topResolved_Tight_pass                  = f"BestTopResolved_score>={Top_Resolved_wp['5%']}"
topResolved_Tight_fail                  = f"BestTopResolved_score<{Top_Resolved_wp['5%']}"
topResolved_LooseButNotTight_pass       = f"BestTopResolved_score>={Top_Resolved_wp['10%']} && BestTopResolved_score<{Top_Resolved_wp['5%']}"
topResolved_LooseButNotTight_fail       = f"BestTopResolved_score<{Top_Resolved_wp['10%']}"
topResolved_Loose_pass                  = f"BestTopResolved_score>={Top_Resolved_wp['10%']}"
topResolved_Loose_fail                  = f"BestTopResolved_score<{Top_Resolved_wp['10%']}"

topMixed_Tight_pass                     = f"BestTopMixed_score>={Top_Mixed_wp['5%']}"
topMixed_Tight_fail                     = f"BestTopMixed_score<{Top_Mixed_wp['5%']}"
topMixed_LooseButNotTight_pass          = f"BestTopMixed_score>={Top_Mixed_wp['10%']} && BestTopMixed_score<{Top_Mixed_wp['5%']}"
topMixed_LooseButNotTight_fail          = f"BestTopMixed_score<{Top_Mixed_wp['10%']}"
topMixed_Loose_pass                     = f"BestTopMixed_score>={Top_Mixed_wp['10%']}"
topMixed_Loose_fail                     = f"BestTopMixed_score<{Top_Mixed_wp['10%']}"

topMerged_Tight_pass                    = f"BestTopMerged_score>={Top_Merged_wp['5%']}"
topMerged_Tight_fail                    = f"BestTopMerged_score<{Top_Merged_wp['5%']}"
topMerged_LooseButNotTight_pass         = f"BestTopMerged_score>={Top_Merged_wp['10%']} && BestTopMerged_score<{Top_Merged_wp['5%']}"
topMerged_LooseButNotTight_fail         = f"BestTopMerged_score<{Top_Merged_wp['10%']}"
topMerged_Loose_pass                    = f"BestTopMerged_score>={Top_Merged_wp['10%']}"
topMerged_Loose_fail                    = f"BestTopMerged_score<{Top_Merged_wp['10%']}"

regions_Resolved                        = {
                                            "semilepPresel"                                 : semilepPresel,
                                            "semilepPresel_njg2_nfjeq0"                     : semilepPresel_njg2_nfjeq0,
                                            "semilepPresel_njfgeq1"                         : semilepPresel_njfgeq1,
                                            "semilepPresel_MET"                             : semilepPresel_MET,
                                            "semilepPresel_MET_W"                           : semilepPresel_MET_W,
                                            "semilepPreselResolved"                         : semilepPreselResolved,
                                            ####################
                                            ##### RESOLVED #####
                                            ####################
                                            ###### Loose ######
                                            "SemiLep_ResolvedLoose_pt0to200_pass":                                 semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_pass,
                                            "SemiLep_ResolvedLoose_pt0to200_fail":                                 semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_fail,
                                            "SemiLep_ResolvedLoose_pt0to200_pass_topmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_pass      + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt0to200_pass_nonmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_pass      + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt0to200_pass_other":                           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_pass      + " && " + topResolved_other,
                                            "SemiLep_ResolvedLoose_pt0to200_fail_topmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_fail      + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt0to200_fail_nonmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_fail      + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt0to200_fail_other":                           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Loose_fail      + " && " + topResolved_other,

                                            "SemiLep_ResolvedLoose_pt200to400_pass":                               semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_pass,
                                            "SemiLep_ResolvedLoose_pt200to400_fail":                               semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_fail,
                                            "SemiLep_ResolvedLoose_pt200to400_pass_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_pass    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt200to400_pass_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_pass    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt200to400_pass_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_pass    + " && " + topResolved_other,
                                            "SemiLep_ResolvedLoose_pt200to400_fail_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_fail    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt200to400_fail_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_fail    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt200to400_fail_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Loose_fail    + " && " + topResolved_other,

                                            "SemiLep_ResolvedLoose_pt400to600_pass":                               semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_pass,
                                            "SemiLep_ResolvedLoose_pt400to600_fail":                               semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_fail,
                                            "SemiLep_ResolvedLoose_pt400to600_pass_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_pass    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt400to600_pass_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_pass    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt400to600_pass_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_pass    + " && " + topResolved_other,
                                            "SemiLep_ResolvedLoose_pt400to600_fail_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_fail    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt400to600_fail_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_fail    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt400to600_fail_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Loose_fail    + " && " + topResolved_other,

                                            "SemiLep_ResolvedLoose_pt600to1000_pass":                              semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_pass,
                                            "SemiLep_ResolvedLoose_pt600to1000_fail":                              semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_fail,
                                            "SemiLep_ResolvedLoose_pt600to1000_pass_topmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_pass   + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt600to1000_pass_nonmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_pass   + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt600to1000_pass_other":                        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_pass   + " && " + topResolved_other,
                                            "SemiLep_ResolvedLoose_pt600to1000_fail_topmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_fail   + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedLoose_pt600to1000_fail_nonmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_fail   + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedLoose_pt600to1000_fail_other":                        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Loose_fail   + " && " + topResolved_other,

                                            ###### Loose But Not Tight ######
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_pass":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_pass,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_fail":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_fail,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_pass_topmatched":           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_pass      + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_pass_nonmatched":           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_pass      + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_pass_other":                semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_pass      + " && " + topResolved_other,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_fail_topmatched":           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_fail      + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_fail_nonmatched":           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_fail      + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt0to200_fail_other":                semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_LooseButNotTight_fail      + " && " + topResolved_other,

                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_pass":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_pass,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_fail":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_fail,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_pass_topmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_pass    + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_pass_nonmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_pass    + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_pass_other":              semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_pass    + " && " + topResolved_other,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_fail_topmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_fail    + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_fail_nonmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_fail    + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt200to400_fail_other":              semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_LooseButNotTight_fail    + " && " + topResolved_other,

                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_pass":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_pass,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_fail":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_fail,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_pass_topmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_pass    + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_pass_nonmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_pass    + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_pass_other":              semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_pass    + " && " + topResolved_other,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_fail_topmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_fail    + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_fail_nonmatched":         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_fail    + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt400to600_fail_other":              semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_LooseButNotTight_fail    + " && " + topResolved_other,

                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_pass":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_pass,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_fail":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_fail,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_pass_topmatched":        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_pass   + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_pass_nonmatched":        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_pass   + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_pass_other":             semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_pass   + " && " + topResolved_other,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_fail_topmatched":        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_fail   + " && " + topResolved_topmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_fail_nonmatched":        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_fail   + " && " + topResolved_nonmatched,
                                            # "SemiLep_ResolvedLooseButNotTight_pt600to1000_fail_other":             semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_LooseButNotTight_fail   + " && " + topResolved_other,

                                            ###### Tight ######
                                            "SemiLep_ResolvedTight_pt0to200_pass":                                 semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_pass,
                                            "SemiLep_ResolvedTight_pt0to200_fail":                                 semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_fail,
                                            "SemiLep_ResolvedTight_pt0to200_pass_topmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_pass      + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt0to200_pass_nonmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_pass      + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt0to200_pass_other":                           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_pass      + " && " + topResolved_other,
                                            "SemiLep_ResolvedTight_pt0to200_fail_topmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_fail      + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt0to200_fail_nonmatched":                      semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_fail      + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt0to200_fail_other":                           semilepPreselResolved + " && (BestTopResolved_pt>=0) && (BestTopResolved_pt<200)" + " && " + topResolved_Tight_fail      + " && " + topResolved_other,

                                            "SemiLep_ResolvedTight_pt200to400_pass":                               semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_pass,
                                            "SemiLep_ResolvedTight_pt200to400_fail":                               semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_fail,
                                            "SemiLep_ResolvedTight_pt200to400_pass_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_pass    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt200to400_pass_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_pass    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt200to400_pass_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_pass    + " && " + topResolved_other,
                                            "SemiLep_ResolvedTight_pt200to400_fail_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_fail    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt200to400_fail_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_fail    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt200to400_fail_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=200) && (BestTopResolved_pt<400)" + " && " + topResolved_Tight_fail    + " && " + topResolved_other,

                                            "SemiLep_ResolvedTight_pt400to600_pass":                               semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_pass,
                                            "SemiLep_ResolvedTight_pt400to600_fail":                               semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_fail,
                                            "SemiLep_ResolvedTight_pt400to600_pass_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_pass    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt400to600_pass_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_pass    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt400to600_pass_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_pass    + " && " + topResolved_other,
                                            "SemiLep_ResolvedTight_pt400to600_fail_topmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_fail    + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt400to600_fail_nonmatched":                    semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_fail    + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt400to600_fail_other":                         semilepPreselResolved + " && (BestTopResolved_pt>=400) && (BestTopResolved_pt<600)" + " && " + topResolved_Tight_fail    + " && " + topResolved_other,

                                            "SemiLep_ResolvedTight_pt600to1000_pass":                              semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_pass,
                                            "SemiLep_ResolvedTight_pt600to1000_fail":                              semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_fail,
                                            "SemiLep_ResolvedTight_pt600to1000_pass_topmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_pass   + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt600to1000_pass_nonmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_pass   + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt600to1000_pass_other":                        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_pass   + " && " + topResolved_other,
                                            "SemiLep_ResolvedTight_pt600to1000_fail_topmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_fail   + " && " + topResolved_topmatched,
                                            "SemiLep_ResolvedTight_pt600to1000_fail_nonmatched":                   semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_fail   + " && " + topResolved_nonmatched,
                                            "SemiLep_ResolvedTight_pt600to1000_fail_other":                        semilepPreselResolved + " && (BestTopResolved_pt>=600) && (BestTopResolved_pt<1000)" + " && " + topResolved_Tight_fail   + " && " + topResolved_other,
                                        }

regions_Mixed                        = {
                                            "semilepPresel"                                 : semilepPresel,
                                            "semilepPresel_njg2_nfjeq0"                     : semilepPresel_njg2_nfjeq0,
                                            "semilepPresel_njfgeq1"                         : semilepPresel_njfgeq1,
                                            "semilepPresel_MET"                             : semilepPresel_MET,
                                            "semilepPresel_MET_W"                           : semilepPresel_MET_W,
                                            "semilepPreselMixed"                            : semilepPreselMixed,
                                            ###################
                                            ###### MIXED ######
                                            ###################
                                            ###### Loose ######
                                            "SemiLep_MixedLoose_pt0to200_pass":                                 semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_pass,
                                            "SemiLep_MixedLoose_pt0to200_fail":                                 semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_fail,
                                            "SemiLep_MixedLoose_pt0to200_pass_topmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_pass      + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt0to200_pass_nonmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_pass      + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt0to200_pass_other":                           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_pass      + " && " + topMixed_other,
                                            "SemiLep_MixedLoose_pt0to200_fail_topmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_fail      + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt0to200_fail_nonmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_fail      + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt0to200_fail_other":                           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Loose_fail      + " && " + topMixed_other,

                                            "SemiLep_MixedLoose_pt200to400_pass":                               semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_pass,
                                            "SemiLep_MixedLoose_pt200to400_fail":                               semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_fail,
                                            "SemiLep_MixedLoose_pt200to400_pass_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_pass    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt200to400_pass_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_pass    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt200to400_pass_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_pass    + " && " + topMixed_other,
                                            "SemiLep_MixedLoose_pt200to400_fail_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_fail    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt200to400_fail_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_fail    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt200to400_fail_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Loose_fail    + " && " + topMixed_other,

                                            "SemiLep_MixedLoose_pt400to600_pass":                               semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_pass,
                                            "SemiLep_MixedLoose_pt400to600_fail":                               semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_fail,
                                            "SemiLep_MixedLoose_pt400to600_pass_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_pass    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt400to600_pass_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_pass    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt400to600_pass_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_pass    + " && " + topMixed_other,
                                            "SemiLep_MixedLoose_pt400to600_fail_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_fail    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt400to600_fail_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_fail    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt400to600_fail_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Loose_fail    + " && " + topMixed_other,

                                            "SemiLep_MixedLoose_pt600to1000_pass":                              semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_pass,
                                            "SemiLep_MixedLoose_pt600to1000_fail":                              semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_fail,
                                            "SemiLep_MixedLoose_pt600to1000_pass_topmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_pass   + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt600to1000_pass_nonmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_pass   + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt600to1000_pass_other":                        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_pass   + " && " + topMixed_other,
                                            "SemiLep_MixedLoose_pt600to1000_fail_topmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_fail   + " && " + topMixed_topmatched,
                                            "SemiLep_MixedLoose_pt600to1000_fail_nonmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_fail   + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedLoose_pt600to1000_fail_other":                        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Loose_fail   + " && " + topMixed_other,

                                            ###### Loose But Not Tight ######
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_pass":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_pass,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_fail":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_fail,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_pass_topmatched":           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_pass      + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_pass_nonmatched":           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_pass      + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_pass_other":                semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_pass      + " && " + topMixed_other,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_fail_topmatched":           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_fail      + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_fail_nonmatched":           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_fail      + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt0to200_fail_other":                semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_LooseButNotTight_fail      + " && " + topMixed_other,

                                            # "SemiLep_MixedLooseButNotTight_pt200to400_pass":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_pass,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_fail":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_fail,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_pass_topmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_pass    + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_pass_nonmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_pass    + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_pass_other":              semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_pass    + " && " + topMixed_other,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_fail_topmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_fail    + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_fail_nonmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_fail    + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt200to400_fail_other":              semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_LooseButNotTight_fail    + " && " + topMixed_other,

                                            # "SemiLep_MixedLooseButNotTight_pt400to600_pass":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_pass,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_fail":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_fail,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_pass_topmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_pass    + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_pass_nonmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_pass    + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_pass_other":              semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_pass    + " && " + topMixed_other,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_fail_topmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_fail    + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_fail_nonmatched":         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_fail    + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt400to600_fail_other":              semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_LooseButNotTight_fail    + " && " + topMixed_other,

                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_pass":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_pass,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_fail":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_fail,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_pass_topmatched":        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_pass   + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_pass_nonmatched":        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_pass   + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_pass_other":             semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_pass   + " && " + topMixed_other,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_fail_topmatched":        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_fail   + " && " + topMixed_topmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_fail_nonmatched":        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_fail   + " && " + topMixed_nonmatched,
                                            # "SemiLep_MixedLooseButNotTight_pt600to1000_fail_other":             semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_LooseButNotTight_fail   + " && " + topMixed_other,

                                            ###### Tight ######
                                            "SemiLep_MixedTight_pt0to200_pass":                                 semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_pass,
                                            "SemiLep_MixedTight_pt0to200_fail":                                 semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_fail,
                                            "SemiLep_MixedTight_pt0to200_pass_topmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_pass      + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt0to200_pass_nonmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_pass      + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt0to200_pass_other":                           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_pass      + " && " + topMixed_other,
                                            "SemiLep_MixedTight_pt0to200_fail_topmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_fail      + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt0to200_fail_nonmatched":                      semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_fail      + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt0to200_fail_other":                           semilepPreselMixed + " && (BestTopMixed_pt>=0) && (BestTopMixed_pt<200)" + " && " + topMixed_Tight_fail      + " && " + topMixed_other,

                                            "SemiLep_MixedTight_pt200to400_pass":                               semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_pass,
                                            "SemiLep_MixedTight_pt200to400_fail":                               semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_fail,
                                            "SemiLep_MixedTight_pt200to400_pass_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_pass    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt200to400_pass_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_pass    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt200to400_pass_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_pass    + " && " + topMixed_other,
                                            "SemiLep_MixedTight_pt200to400_fail_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_fail    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt200to400_fail_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_fail    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt200to400_fail_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=200) && (BestTopMixed_pt<400)" + " && " + topMixed_Tight_fail    + " && " + topMixed_other,

                                            "SemiLep_MixedTight_pt400to600_pass":                               semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_pass,
                                            "SemiLep_MixedTight_pt400to600_fail":                               semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_fail,
                                            "SemiLep_MixedTight_pt400to600_pass_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_pass    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt400to600_pass_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_pass    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt400to600_pass_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_pass    + " && " + topMixed_other,
                                            "SemiLep_MixedTight_pt400to600_fail_topmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_fail    + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt400to600_fail_nonmatched":                    semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_fail    + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt400to600_fail_other":                         semilepPreselMixed + " && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600)" + " && " + topMixed_Tight_fail    + " && " + topMixed_other,

                                            "SemiLep_MixedTight_pt600to1000_pass":                              semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_pass,
                                            "SemiLep_MixedTight_pt600to1000_fail":                              semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_fail,
                                            "SemiLep_MixedTight_pt600to1000_pass_topmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_pass   + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt600to1000_pass_nonmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_pass   + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt600to1000_pass_other":                        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_pass   + " && " + topMixed_other,
                                            "SemiLep_MixedTight_pt600to1000_fail_topmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_fail   + " && " + topMixed_topmatched,
                                            "SemiLep_MixedTight_pt600to1000_fail_nonmatched":                   semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_fail   + " && " + topMixed_nonmatched,
                                            "SemiLep_MixedTight_pt600to1000_fail_other":                        semilepPreselMixed + " && (BestTopMixed_pt>=600) && (BestTopMixed_pt<1000)" + " && " + topMixed_Tight_fail   + " && " + topMixed_other,
                                        }

regions_Merged                        = {
                                            "semilepPresel"                                 : semilepPresel,
                                            "semilepPresel_njg2_nfjeq0"                     : semilepPresel_njg2_nfjeq0,
                                            "semilepPresel_njfgeq1"                         : semilepPresel_njfgeq1,
                                            "semilepPresel_MET"                             : semilepPresel_MET,
                                            "semilepPresel_MET_W"                           : semilepPresel_MET_W,
                                            "semilepPreselMerged"                           : semilepPreselMerged,
                                            ####################
                                            ###### MERGED ######
                                            ####################
                                            ###### Loose ######
                                            "SemiLep_MergedLoose_pt0to200_pass":                                 semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_pass,
                                            "SemiLep_MergedLoose_pt0to200_fail":                                 semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_fail,
                                            "SemiLep_MergedLoose_pt0to200_pass_topmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_pass      + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt0to200_pass_nonmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_pass      + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt0to200_pass_other":                           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_pass      + " && " + topMerged_other,
                                            "SemiLep_MergedLoose_pt0to200_fail_topmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_fail      + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt0to200_fail_nonmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_fail      + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt0to200_fail_other":                           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Loose_fail      + " && " + topMerged_other,

                                            "SemiLep_MergedLoose_pt200to400_pass":                               semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_pass,
                                            "SemiLep_MergedLoose_pt200to400_fail":                               semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_fail,
                                            "SemiLep_MergedLoose_pt200to400_pass_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_pass    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt200to400_pass_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_pass    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt200to400_pass_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_pass    + " && " + topMerged_other,
                                            "SemiLep_MergedLoose_pt200to400_fail_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_fail    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt200to400_fail_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_fail    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt200to400_fail_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Loose_fail    + " && " + topMerged_other,

                                            "SemiLep_MergedLoose_pt400to600_pass":                               semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_pass,
                                            "SemiLep_MergedLoose_pt400to600_fail":                               semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_fail,
                                            "SemiLep_MergedLoose_pt400to600_pass_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_pass    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt400to600_pass_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_pass    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt400to600_pass_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_pass    + " && " + topMerged_other,
                                            "SemiLep_MergedLoose_pt400to600_fail_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_fail    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt400to600_fail_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_fail    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt400to600_fail_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Loose_fail    + " && " + topMerged_other,

                                            "SemiLep_MergedLoose_pt600to1000_pass":                              semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_pass,
                                            "SemiLep_MergedLoose_pt600to1000_fail":                              semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_fail,
                                            "SemiLep_MergedLoose_pt600to1000_pass_topmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_pass   + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt600to1000_pass_nonmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_pass   + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt600to1000_pass_other":                        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_pass   + " && " + topMerged_other,
                                            "SemiLep_MergedLoose_pt600to1000_fail_topmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_fail   + " && " + topMerged_topmatched,
                                            "SemiLep_MergedLoose_pt600to1000_fail_nonmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_fail   + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedLoose_pt600to1000_fail_other":                        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Loose_fail   + " && " + topMerged_other,

                                            ###### Loose But Not Tight ######
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_pass":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_pass,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_fail":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_fail,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_pass_topmatched":           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_pass      + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_pass_nonmatched":           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_pass      + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_pass_other":                semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_pass      + " && " + topMerged_other,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_fail_topmatched":           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_fail      + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_fail_nonmatched":           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_fail      + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt0to200_fail_other":                semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_LooseButNotTight_fail      + " && " + topMerged_other,

                                            # "SemiLep_MergedLooseButNotTight_pt200to400_pass":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_pass,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_fail":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_fail,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_pass_topmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_pass    + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_pass_nonmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_pass    + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_pass_other":              semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_pass    + " && " + topMerged_other,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_fail_topmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_fail    + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_fail_nonmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_fail    + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt200to400_fail_other":              semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_LooseButNotTight_fail    + " && " + topMerged_other,

                                            # "SemiLep_MergedLooseButNotTight_pt400to600_pass":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_pass,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_fail":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_fail,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_pass_topmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_pass    + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_pass_nonmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_pass    + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_pass_other":              semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_pass    + " && " + topMerged_other,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_fail_topmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_fail    + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_fail_nonmatched":         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_fail    + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt400to600_fail_other":              semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_LooseButNotTight_fail    + " && " + topMerged_other,

                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_pass":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_pass,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_fail":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_fail,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_pass_topmatched":        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_pass   + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_pass_nonmatched":        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_pass   + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_pass_other":             semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_pass   + " && " + topMerged_other,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_fail_topmatched":        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_fail   + " && " + topMerged_topmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_fail_nonmatched":        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_fail   + " && " + topMerged_nonmatched,
                                            # "SemiLep_MergedLooseButNotTight_pt600to1000_fail_other":             semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_LooseButNotTight_fail   + " && " + topMerged_other,

                                            ###### Tight ######
                                            "SemiLep_MergedTight_pt0to200_pass":                                 semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_pass,
                                            "SemiLep_MergedTight_pt0to200_fail":                                 semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_fail,
                                            "SemiLep_MergedTight_pt0to200_pass_topmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_pass      + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt0to200_pass_nonmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_pass      + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt0to200_pass_other":                           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_pass      + " && " + topMerged_other,
                                            "SemiLep_MergedTight_pt0to200_fail_topmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_fail      + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt0to200_fail_nonmatched":                      semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_fail      + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt0to200_fail_other":                           semilepPreselMerged + " && (BestTopMerged_pt>=0) && (BestTopMerged_pt<200)" + " && " + topMerged_Tight_fail      + " && " + topMerged_other,

                                            "SemiLep_MergedTight_pt200to400_pass":                               semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_pass,
                                            "SemiLep_MergedTight_pt200to400_fail":                               semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_fail,
                                            "SemiLep_MergedTight_pt200to400_pass_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_pass    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt200to400_pass_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_pass    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt200to400_pass_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_pass    + " && " + topMerged_other,
                                            "SemiLep_MergedTight_pt200to400_fail_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_fail    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt200to400_fail_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_fail    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt200to400_fail_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=200) && (BestTopMerged_pt<400)" + " && " + topMerged_Tight_fail    + " && " + topMerged_other,

                                            "SemiLep_MergedTight_pt400to600_pass":                               semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_pass,
                                            "SemiLep_MergedTight_pt400to600_fail":                               semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_fail,
                                            "SemiLep_MergedTight_pt400to600_pass_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_pass    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt400to600_pass_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_pass    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt400to600_pass_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_pass    + " && " + topMerged_other,
                                            "SemiLep_MergedTight_pt400to600_fail_topmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_fail    + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt400to600_fail_nonmatched":                    semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_fail    + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt400to600_fail_other":                         semilepPreselMerged + " && (BestTopMerged_pt>=400) && (BestTopMerged_pt<600)" + " && " + topMerged_Tight_fail    + " && " + topMerged_other,

                                            "SemiLep_MergedTight_pt600to1000_pass":                              semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_pass,
                                            "SemiLep_MergedTight_pt600to1000_fail":                              semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_fail,
                                            "SemiLep_MergedTight_pt600to1000_pass_topmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_pass   + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt600to1000_pass_nonmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_pass   + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt600to1000_pass_other":                        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_pass   + " && " + topMerged_other,
                                            "SemiLep_MergedTight_pt600to1000_fail_topmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_fail   + " && " + topMerged_topmatched,
                                            "SemiLep_MergedTight_pt600to1000_fail_nonmatched":                   semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_fail   + " && " + topMerged_nonmatched,
                                            "SemiLep_MergedTight_pt600to1000_fail_other":                        semilepPreselMerged + " && (BestTopMerged_pt>=600) && (BestTopMerged_pt<1000)" + " && " + topMerged_Tight_fail   + " && " + topMerged_other,
                                        }


regions = {
            "Resolved"                            : regions_Resolved,
            "Mixed"                               : regions_Mixed,
            "Merged"                              : regions_Merged,
        }
