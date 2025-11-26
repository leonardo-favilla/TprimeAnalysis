import ROOT
ROOT.gStyle.SetOptStat(0)
import sys
import os
import optparse
import json
import numpy as np
import math
from datetime import datetime
from PhysicsTools.NanoAODTools.postprocessing.variables import *
import yaml
sys.path.append('../')


config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

#### User info ####
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
WorkDir  = os.environ["PWD"]


usage                   = 'python3 postSelector.py -c <component> --scenario <scenario> --nfiles_max <nfiles_max> [--certpath <path_to_certificate_file>]'
parser                  = optparse.OptionParser(usage)
parser.add_option('-c', '--component',          dest='component',           type=str,               default="QCD_HT400to600_2022",                      help='Single component to process, in the form: QCD_HT400to600_2022')
parser.add_option(      '--scenario',           dest='scenario',            type=str,               default="nominal",                                  help='Systematic scenario to process: nominal, jerUp, jerDown, jesUp, jesDown')
parser.add_option(      '--nfiles_max',         dest='nfiles_max',          type=int,               default=1,                                          help='Max number of files to process per sample')
parser.add_option(      '--certpath',           dest='certpath',            type=str,               default="/tmp/x509up_u{}".format(str(os.getuid())), help='Path to the certificate file')


(opt, args)             = parser.parse_args()
in_dataset              = opt.component
year                    = int(in_dataset.split("_")[-1][:4])
EE                      = 1 if len(in_dataset.split("_")[-1])>4 else 0
scenario                = opt.scenario
nfiles_max              = opt.nfiles_max
certpath                = opt.certpath
where_to_write          = "eos" # options are "tier" or "eos"
dict_samples_file       = config["dict_samples"][year]
scenario_tag            = {
                            "nominal":  "nominal",
                            "jerUp":    "jerup",
                            "jerDown":  "jerdown",
                            "jesUp":    "jesTotalup",
                            "jesDown":  "jesTotaldown"
                        }

if "Data" not in in_dataset:
    isMC                = True
    scenarios           = ["nominal", "jerUp", "jerDown", "jesUp", "jesDown"]
else:
    isMC                = False
    scenarios           = ["nominal"]
if year == 2018:
    bTagAlg = "Jet_btagDeepB"
elif year in [2022,2023]:
    bTagAlg = "Jet_btagPNetB"


print(f"Processing component {in_dataset}, year {year}, scenario {scenario}")

#### Define output files and folders ####
if where_to_write == "eos":
    remote_folder_name              = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF"
    outFolder                       = remote_folder_name+"/ntuples_ready_for_TopSF_Framework/"
    outSubFolder                    = outFolder+in_dataset+"/"
    if not os.path.exists(remote_folder_name):
        os.makedirs(remote_folder_name)
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    if not os.path.exists(outSubFolder):
        os.makedirs(outSubFolder)
elif where_to_write == "tier":
    remote_folder_name              = "TopSF"
    outFolder                       = remote_folder_name+"/ntuples_ready_for_TopSF_Framework/"
    outSubFolder                    = outFolder+in_dataset+"/"

    print("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, remote_folder_name, certpath))
    subprocess.run(
        ["davix-mkdir",
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{remote_folder_name}/",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )

    print("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, outFolder, certpath))
    subprocess.run(
        ["davix-mkdir",
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFolder}",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )

    print("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, outSubFolder, certpath))
    subprocess.run(
        ["davix-mkdir",
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outSubFolder}",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )

    outFolder_tmp                       = "/tmp/{}/".format(username)
    if not os.path.exists(outFolder_tmp):
        os.makedirs(outFolder_tmp)
    outFilePath_tmp                     = outFolder_tmp+in_dataset+"_"+scenario+".root"
    
outFilePath                             = outSubFolder+in_dataset+"_"+scenario+".root"


print("Output tmp (if needed) will be written to: ", outFilePath_tmp if where_to_write=="tier" else "no tmp folder needed")
print("Output will be written to: ", outFilePath)


if where_to_write == "tier":
    print("Copying files to tier...")
    print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_tmp, username, outFilePath, certpath))
    subprocess.run([
        "davix-put",
        outFilePath_tmp,
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath}",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
    ])
    print("Done!")



#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)

#### LOAD utils/postselection.h ####
text_file           = open(WorkDir+"/../postselection/postselection.h", "r")
data                = text_file.read()
def my_initialization_function():
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(data))
    print("end of initialization")
my_initialization_function()


#### Retrieve files to process for the given component and ntot ####
if not "Data" in in_dataset:
    ntot_events                                     = np.sum(samples[in_dataset][in_dataset]['ntot'][:nfiles_max])
else:
    ntot_events                                     = None

chain                                               = []
tchain                                              = ROOT.TChain("Events")
nfiles_opened                                       = 0
for i, string in enumerate(samples[in_dataset][in_dataset]['strings']):
    if i >= nfiles_max:
        break
    samples[in_dataset][in_dataset]['strings'][i]   = string.replace("root://cms-xrd-global.cern.ch/", "root://stormgf2.pi.infn.it/")
    f                                               = samples[in_dataset][in_dataset]['strings'][i]
    try:
        TFile                                       = ROOT.TFile.Open(f)
        tchain.Add(f)
        nfiles_opened += 1
    except:
        ntot_events -= samples[in_dataset][in_dataset]['ntot'][i]
        print("Could not add file: ", f)
        continue
chain                                               = samples[in_dataset][in_dataset]['strings'][:nfiles_max]
print(f"Opened {nfiles_opened} files out of {nfiles_max} requested for sample {in_dataset}")



#### Define cuts and regions ####
cut         = requirements  # ---> see variables.py
regions_def = regions.keys()       # ---> see variables.py

print("Cut string:                  ", cut)
print("Regions:                     ", regions_def)






################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_")

################### preselection ###############
def preselection(df, btagAlg, year, EE):
    
    df = df.Define("GoodJet_idx", "GetGoodJet(Jet_pt, Jet_eta, Jet_jetId)")
    df = df.Define("nGoodJet", "nGoodJet(GoodJet_idx)")
    df = df.Define("GoodFatJet_idx", "GetGoodJet(FatJet_pt, FatJet_eta, FatJet_jetId)")
    df = df.Define("nGoodFatJet", "GoodFatJet_idx.size()")
    df = df.Filter("nGoodJet>2 || nGoodFatJet>0 ", "jet presel")

    df = df.Redefine("MinDelta_phi", "min_DeltaPhi(PuppiMET_T1_phi, Jet_phi, GoodJet_idx)")
    df = df.Define("nTightElectron", "nTightElectron(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("TightElectron_idx", "TightElectron_idx(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("nVetoElectron", "nVetoElectron(Electron_pt, Electron_cutBased, Electron_eta)")
    df = df.Define("nTightMuon", "nTightMuon(Muon_pt, Muon_eta, Muon_tightId)")
    df = df.Define("TightMuon_idx", "TightMuon_idx(Muon_pt, Muon_eta, Muon_tightId)")
    df = df.Define("nVetoMuon", "nVetoMuon(Muon_pt, Muon_eta, Muon_looseId)")
    df = df.Define("Lepton_flavour", "Lepton_flavour(nTightElectron, nTightMuon)")\
            .Define("Lep_pt", "Lepton_var(Lepton_flavour, Electron_pt, TightElectron_idx, Muon_pt, TightMuon_idx)")\
            .Define("Lep_phi", "Lepton_var(Lepton_flavour, Electron_phi, TightElectron_idx, Muon_phi, TightMuon_idx)")
    df = df.Define("MT", "sqrt(2 * Lep_pt * PuppiMET_T1_pt * (1 - cos(Lep_phi - PuppiMET_T1_phi)))")
    
    df = df.Define("LeadingJetPt_idx", "GetLeadingPtJet(Jet_pt)")
    df = df.Define("LeadingJetPt_pt", "GetLeadingJetVar(LeadingJetPt_idx, Jet_pt)")
    df = df.Define("LeadingJetPt_eta", "GetLeadingJetVar(LeadingJetPt_idx, Jet_eta)")
    df = df.Define("LeadingJetPt_phi", "GetLeadingJetVar(LeadingJetPt_idx, Jet_phi)")
    df = df.Define("LeadingJetPt_mass", "GetLeadingJetVar(LeadingJetPt_idx, Jet_mass)")
    df = df.Define("LeadingFatJetPt_idx", "GetLeadingPtJet(FatJet_pt)")
    df = df.Define("LeadingFatJetPt_pt", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_pt)")
    df = df.Define("LeadingFatJetPt_eta", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_eta)")
    df = df.Define("LeadingFatJetPt_phi", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_phi)")
    df = df.Define("LeadingFatJetPt_mass", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_mass)")
    df = df.Define("LeadingMuonPt_idx", "GetLeadingPtLep(Muon_pt, Muon_eta, Muon_looseId)")
    df = df.Define("LeadingMuonPt_pt", "GetLeadingJetVar(LeadingMuonPt_idx, Muon_pt)")
    df = df.Define("LeadingMuonPt_eta", "GetLeadingJetVar(LeadingMuonPt_idx, Muon_eta)")
    df = df.Define("LeadingMuonPt_phi", "GetLeadingJetVar(LeadingMuonPt_idx, Muon_phi)")
    df = df.Define("LeadingElectronPt_idx", "GetLeadingPtLep(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("LeadingElectronPt_pt", "GetLeadingJetVar(LeadingElectronPt_idx, Electron_pt)")
    df = df.Define("LeadingElectronPt_eta", "GetLeadingJetVar(LeadingElectronPt_idx, Electron_eta)")
    df = df.Define("LeadingElectronPt_phi", "GetLeadingJetVar(LeadingElectronPt_idx, Electron_phi)")
    
    df = df.Define("nForwardJet", "nForwardJet(Jet_pt, Jet_jetId, Jet_eta)")
    df = df.Define("MHT","MHT(GoodJet_idx, Jet_pt, Jet_phi, Jet_eta, Jet_mass)")
    df = df.Define("JetBTagLoose_idx", "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 0)")\
                .Define("nJetBtagLoose", "static_cast<int>(JetBTagLoose_idx.size());")
    df = df.Define("JetBTagMedium_idx", "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 1)")\
                .Define("nJetBtagMedium", "static_cast<int>(JetBTagMedium_idx.size());")
    df = df.Redefine("PuppiMET_T1_pt", "PuppiMET_T1_pt_vec[0]")\
                .Redefine("PuppiMET_T1_phi", "PuppiMET_T1_phi_vec[0]")
    
    return df

############### trigger selection #####################
def trigger_filter(df, data, isMC, year):
    hlt = {
        2022: [
                "HLT_PFMET120_PFMHT120_IDTight",          # MET (2022-2023)
                "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",  # MET (2022-2023)
                "HLT_Photon200",                          # High-pT electron (2022)
                "HLT_Ele27_WPTight_Gsf",                  # Low-pT electron (2022)
                "HLT_Mu50",                               # Muon (2022-2023)
                "HLT_IsoMu24",                            # Muon (2022-2023)
                "HLT_HighPtTkMu100",                      # Muon (2022-2023)
                ],

        2023: [
                "HLT_PFMET120_PFMHT120_IDTight",          # MET (2022-2023)
                "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",  # MET (2022-2023)
                "HLT_Photon175EB_TightID_TightIso",       # High-pT electron (2023)
                "HLT_Ele30_WPTight_Gsf",                  # Low-pT electron (2023)
                "HLT_Mu50",                               # Muon (2022-2023)
                "HLT_IsoMu24",                            # Muon (2022-2023)
                "HLT_HighPtTkMu100",                      # Muon (2022-2023)
            ],
        2024: [
            ]
        }
    # hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
    hlt_met = f"({' || '.join(hlt[year])})"
    df_trig = df.Filter(hlt_met, "triggerMET")
    return df_trig

############### top selection ########################
def select_top(df, isMC):

    Top_Resolved_wp = {"10%": 0.1422998, "5%": 0.29475874, "1%": 0.59264845, "0.1%": 0.86580896}
    # Top_Resolved_wp = { "10%": 0.1, "5%": 0.3, "1%": 0.59264845, "0.1%": 0.86580896}
    Top_Mixed_wp    = {"10%": 0.7214655876159668, "5%": 0.8474694490432739, "1%" : 0.9436638951301575, "0.1%": 0.9789741635322571}
    Top_Merged_wp   = {"10%": 0.8, "5%": 0.9, "1%": 1., "0.1%": 1.} #to double-check these wp values
    
    # return indices of the FatJet with particleNet score over the thresholds 
    # df_goodtopMer = df.Define("GoodTopMer_idx", f"select_TopMer(FatJet_particleNetWithMass_TvsQCD, GoodFatJet_idx, {Top_Merged_wp['10%']})")
    df_goodtopMer = df.Define("LooseTopMer_idx", f"select_TopMer(FatJet_particleNetWithMass_TvsQCD, GoodFatJet_idx, {Top_Merged_wp['10%']})")\
                      .Define("TightTopMer_idx", f"select_TopMer(FatJet_particleNetWithMass_TvsQCD, GoodFatJet_idx, {Top_Merged_wp['5%']})")\
                      .Define("LooseNOTTightTopMer_idx", f"SubtractIntVectors(LooseTopMer_idx, TightTopMer_idx)")
    # return indices of the TopMixed over the threshold with any object in common
    df_goodtopMix = df_goodtopMer.Define("LooseTopMix_idx", f"select_TopMix(TopMixed_TopScore, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx, {Top_Mixed_wp['10%']})")\
                            .Define("TightTopMix_idx", f"select_TopMix(TopMixed_TopScore, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx, {Top_Mixed_wp['5%']})")\
                            .Define("LooseNOTTightTopMix_idx", f"SubtractIntVectors(LooseTopMix_idx, TightTopMix_idx)")
    # return indices of the TopResolved over the threshold with any object in common
    df_goodtopRes = df_goodtopMix.Define("LooseTopRes_idx", f"select_TopRes(TopResolved_TopScore, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx, {Top_Resolved_wp['10%']})")\
                            .Define("TightTopRes_idx", f"select_TopRes(TopResolved_TopScore, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx, {Top_Resolved_wp['5%']})")\
                            .Define("LooseNOTTightTopRes_idx", f"SubtractIntVectors(LooseTopRes_idx, TightTopRes_idx)")
    
    df_nTops = df_goodtopRes.Define("nLooseTopResolved", "nTop(LooseTopRes_idx)")\
                            .Define("nLooseTopMixed", "nTop(LooseTopMix_idx)")\
                            .Define("nLooseTopMerged", "nTop(LooseTopMer_idx)")\
                            .Define("nTightTopResolved", "nTop(TightTopRes_idx)")\
                            .Define("nTightTopMixed", "nTop(TightTopMix_idx)")\
                            .Define("nTightTopMerged", "nTop(TightTopMer_idx)")
    
    # return:  1- Event Resolved, 2- Event Mixed, 3- Event Merged, 4- Event Nothing, ...
    df_topcategory = df_nTops.Define("EventTopCategory", "select_TopCategory(TightTopMer_idx, TightTopMix_idx, TightTopRes_idx, LooseNOTTightTopMer_idx, LooseNOTTightTopMix_idx, LooseNOTTightTopRes_idx)")
    
    df_topselected = df_topcategory.Define("BestTopResolved_idx", "TopResolved_TopScore.size() == 0 ? -1 : (int)ArgMax(TopResolved_TopScore)")\
                                    .Define("BestTopMixed_idx",    "TopMixed_TopScore.size() == 0 ? -1 : (int)ArgMax(TopMixed_TopScore)")\
                                    .Define("BestTopMerged_idx",   "FatJet_particleNetWithMass_TvsQCD.size() == 0 ? -1 : (int)ArgMax(FatJet_particleNetWithMass_TvsQCD)")

    df_topvariables = df_topselected.Define("BestTopResolved_pt",   "BestTopResolved_idx >= 0 && BestTopResolved_idx < (int)TopResolved_pt.size() ? TopResolved_pt[BestTopResolved_idx] : -9999.")\
                                    .Define("BestTopResolved_eta",  "BestTopResolved_idx >= 0 && BestTopResolved_idx < (int)TopResolved_eta.size() ? TopResolved_eta[BestTopResolved_idx] : -9999.")\
                                    .Define("BestTopResolved_phi",  "BestTopResolved_idx >= 0 && BestTopResolved_idx < (int)TopResolved_phi.size() ? TopResolved_phi[BestTopResolved_idx] : -9999.")\
                                    .Define("BestTopResolved_mass", "BestTopResolved_idx >= 0 && BestTopResolved_idx < (int)TopResolved_mass.size() ? TopResolved_mass[BestTopResolved_idx] : -9999.")\
                                    .Define("BestTopResolved_score","BestTopResolved_idx >= 0 && BestTopResolved_idx < (int)TopResolved_TopScore.size() ? TopResolved_TopScore[BestTopResolved_idx] : -9999.")\
                                    .Define("BestTopMixed_pt",   "BestTopMixed_idx >= 0 && BestTopMixed_idx < (int)TopMixed_pt.size() ? TopMixed_pt[BestTopMixed_idx] : -9999.")\
                                    .Define("BestTopMixed_eta",  "BestTopMixed_idx >= 0 && BestTopMixed_idx < (int)TopMixed_eta.size() ? TopMixed_eta[BestTopMixed_idx] : -9999.")\
                                    .Define("BestTopMixed_phi",  "BestTopMixed_idx >= 0 && BestTopMixed_idx < (int)TopMixed_phi.size() ? TopMixed_phi[BestTopMixed_idx] : -9999.")\
                                    .Define("BestTopMixed_mass", "BestTopMixed_idx >= 0 && BestTopMixed_idx < (int)TopMixed_mass.size() ? TopMixed_mass[BestTopMixed_idx] : -9999.")\
                                    .Define("BestTopMixed_score","BestTopMixed_idx >= 0 && BestTopMixed_idx < (int)TopMixed_TopScore.size() ? TopMixed_TopScore[BestTopMixed_idx] : -9999.")\
                                    .Define("BestTopMerged_pt",   "BestTopMerged_idx >= 0 && BestTopMerged_idx < (int)FatJet_pt.size() ? FatJet_pt[BestTopMerged_idx] : -9999.")\
                                    .Define("BestTopMerged_eta",  "BestTopMerged_idx >= 0 && BestTopMerged_idx < (int)FatJet_eta.size() ? FatJet_eta[BestTopMerged_idx] : -9999.")\
                                    .Define("BestTopMerged_phi",  "BestTopMerged_idx >= 0 && BestTopMerged_idx < (int)FatJet_phi.size() ? FatJet_phi[BestTopMerged_idx] : -9999.")\
                                    .Define("BestTopMerged_mass", "BestTopMerged_idx >= 0 && BestTopMerged_idx < (int)FatJet_mass.size() ? FatJet_mass[BestTopMerged_idx] : -9999.")\
                                    .Define("BestTopMerged_score","BestTopMerged_idx >= 0 && BestTopMerged_idx < (int)FatJet_particleNetWithMass_TvsQCD.size() ? FatJet_particleNetWithMass_TvsQCD[BestTopMerged_idx] : -9999.")
        
    if isMC:
        df_topvariables = df_topvariables.Define("TopResolvedMatched_to_GenTop_dR0p2", "TopGenTopPart_pt.size() > 0 ? TopMatched_to_GenTop_with_dR(TopGenTopPart_eta, TopGenTopPart_phi, BestTopResolved_eta, BestTopResolved_phi, 0.2) : 0.")\
                                         .Define("TopMixedMatched_to_GenTop_dR0p2", "TopGenTopPart_pt.size() > 0 ? TopMatched_to_GenTop_with_dR(TopGenTopPart_eta, TopGenTopPart_phi, BestTopMixed_eta, BestTopMixed_phi, 0.2) : 0.")\
                                         .Define("TopMergedMatched_to_GenTop_dR0p2", "TopGenTopPart_pt.size() > 0 ? TopMatched_to_GenTop_with_dR(TopGenTopPart_eta, TopGenTopPart_phi, BestTopMerged_eta, BestTopMerged_phi, 0.2) : 0.")

    return df_topvariables

def tag_toplep(df):
    df_toplep   = df.Define("Muon_px",                          "(int)nTightMuon > 0 ? Muon_pt[TightMuon_idx[0]]*sin(Muon_phi[TightMuon_idx[0]]) : -9999.")\
                    .Define("Muon_py",                          "(int)nTightMuon > 0 ? Muon_pt[TightMuon_idx[0]]*cos(Muon_phi[TightMuon_idx[0]]) : -9999.")\
                    .Define("MET_px",                           "MET_pt*sin(MET_phi)")\
                    .Define("MET_py",                           "MET_pt*cos(MET_phi)")\
                    .Define("W_pt",                             "(int)nTightMuon > 0 ? sqrt(pow(Muon_px+MET_px, 2)+pow(Muon_py+MET_py, 2)) : -9999.")\
                    .Define("bJetsMatched_to_GoodMuon_idx",     "(int)nTightMuon > 0 ? idx_of_bJetsMatched_to_GoodMuon_with_dR(TightMuon_idx, Muon_eta, Muon_phi, JetBTagMedium_idx, Jet_eta, Jet_phi, 2.0) : -9999.")\
                    .Define("bJetsMatched_to_GoodMuon_dR",      "(int)nTightMuon > 0 ? dR_of_bJetsMatched_to_GoodMuon_with_dR(TightMuon_idx, Muon_eta, Muon_phi, JetBTagMedium_idx, Jet_eta, Jet_phi, 2.0) : -9999.")\
                    .Define("nTopLep",                          "(int)nTightMuon > 0 ? (int)bJetsMatched_to_GoodMuon_idx.size() : 0.")

    return df_toplep


######## MAIN CODE ########
t0 = datetime.now()
print("Local time :", t0)

# df                  = ROOT.RDataFrame("Events", inFilePath)
df                      = ROOT.RDataFrame(tchain)
branches                = list(map(str, df.GetColumnNames()))
branches_dict           = {}
if not "Data" in in_dataset:
    df                  = df.Define("SFbtag", "SFbtag_nominal")
    branches.remove("SFbtag_nominal")
if "ZJets" in in_dataset: 
    df = df.Define("nloewcorrection", "nloewcorrectionZ(1., GenPart_pdgId, GenPart_pt, GenPart_statusFlags)")                                                                                         # no nloewcorrection
elif "WJets" in in_dataset:
    df = df.Define("nloewcorrection", "nloewcorrectionW(1., GenPart_pdgId, GenPart_pt, GenPart_statusFlags)")                                                                                         # no nloewcorrection
else:
    df = df.Define("nloewcorrection", "1")


for scenario in scenarios:
    branches_dict[scenario] = [b for b in branches if b.endswith(f"_{scenario_tag[scenario]}")]
branches_common             = [b for b in branches if not any(b in branches_dict[sc] for sc in scenarios)]



opts            = ROOT.RDF.RSnapshotOptions()
opts.fLazy      = True

for b in branches_dict[scenario]:
    try:
        df          = df.Redefine(b.replace(f"_{scenario_tag[scenario]}", ""), b)
    except:
        df          = df.Define(b.replace(f"_{scenario_tag[scenario]}", ""), b)
df                  = df.Define("PuppiMET_T1_pt_vec", "RVec<float>{ (float) PuppiMET_T1_pt}")\
                        .Define("PuppiMET_T1_phi_vec", "RVec<float>{ (float) PuppiMET_T1_phi}")
df_trigger          = trigger_filter(df, None, None, year)
df_presel           = preselection(df_trigger, bTagAlg, year, EE)
df_toplep           = tag_toplep(df_presel)
df_topselected      = select_top(df_toplep, isMC)




branches_to_save    = list(map(str, df_topselected.GetColumnNames()))
if not "Data" in in_dataset:
    branches_to_save.remove("SFbtag_nominal")
opts                = ROOT.RDF.RSnapshotOptions()
opts.fLazy          = True
if where_to_write == "tier":
    df_topselected          = df_topselected.Snapshot("Events", outFilePath_tmp, branches_to_save, opts)
else:
    df_topselected          = df_topselected.Snapshot("Events", outFilePath, branches_to_save, opts)
df_topselected.GetValue()
print("Snapshot done!")

if where_to_write == "tier":
    print("Copying files to tier...")
    subprocess.run(
        [
            "davix-put", outFilePath_nominal_tmp, f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath_nominal}", "-E", certpath, "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )
    print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_nominal_tmp, username, outFilePath_nominal, certpath))



t1 = datetime.now()
print("Job finished in: ", t1-t0)