import ROOT
ROOT.gStyle.SetOptStat(0)
import sys
import os
import optparse
import json
import numpy as np
import math
from datetime import datetime
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.variables import *
sys.path.append('../')

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
workdir  = "user" if "user" in os.environ.get('PWD') else "work"


usage                   = 'python3 postSelector.py -d <datasets> --dict_samples_file <dict_samples_file> --hist_folder <hist_folder> --nfiles_max <nfiles_max>'
parser                  = optparse.OptionParser(usage)
parser.add_option('-d', '--datasets',           dest='datasets',            type=str,               default="QCD_2023",                             help='Datasets to process, in the form: QCD_2023,TT_2023...')
parser.add_option(      '--dict_samples_file',  dest='dict_samples_file',   type=str,               default="../samples/dict_samples_2023.json",    help='Path to the JSON file containing the sample definitions')
parser.add_option(      '--hist_folder',        dest='hist_folder',         type=str,               default="run2023/",                             help='Folder where to save the histograms')
parser.add_option(      '--syst',               dest='syst',                action='store_true',    default=False,                                  help='calculate jerc')
parser.add_option(      '--nfiles_max',         dest='nfiles_max',          type=int,               default=1,                                      help='Max number of files to process per sample')

(opt, args)             = parser.parse_args()
in_dataset              = opt.datasets.split(",")
nfiles_max              = opt.nfiles_max
do_variations           = opt.syst
dict_samples_file       = opt.dict_samples_file
hist_folder             = opt.hist_folder
do_histos               = True
do_snapshot             = False
if do_variations:
    do_snapshot         = False
remote_subfolder_name   = datetime.now().strftime("%Y%m%d") #20231229




if do_variations == True:
    variations          = ["nominal", "pu", "jer", "jesTotal"]
else :
    variations          = ["nominal"]

remote_folder_name      = "Snapshots"
results_folder          = "/eos/user/l/lfavilla/RDF_DManalysis/results/" # "./results/"
folder                  = results_folder+hist_folder+"/"
repohisto               = folder+"plots/"
if not os.path.exists(results_folder):
    os.mkdir(results_folder)
if not os.path.exists(folder):
    os.mkdir(folder)
if not os.path.exists(repohisto):
    os.mkdir(repohisto)


branches = {"PuppiMET_T1_pt_nominal", "PuppiMET_T1_phi_nominal", "MHT", 
            "Top_mass", "Top_pt", "Top_score", "Top_isolationPtJetsdR04", "Top_isolationPtJetsdR06", "Top_isolationPtJetsdR08", "Top_isolationPtJetsdR12", "Top_isolationNJetsdR04", "Top_isolationNJetsdR06", "Top_isolationNJetsdR08", "Top_isolationNJetsdR12",
            "nVetoMuon", "nVetoElectron", "nJetBtagLoose", "nJetBtagMedium", 
            "nGoodJet", "nTightElectron", "nTightMuon", "MT", "MT_T"
           }

#### LOAD utils/postselection.h ####
text_file = open("/afs/cern.ch/" + workdir + "/" + inituser + "/" + username + "/TprimeAnalysis/NanoAODTools/python/postprocessing/postselection/postselection.h", "r")
data      = text_file.read()
def my_initialization_function():
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(data))
    print("end of initialization")
my_initialization_function()

#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)





if do_histos:
    print("You are producing histograms")
    print("local folder histos: {}".format(folder))
if do_snapshot:
    print("You are producing snapshot")
if do_snapshot and remote_subfolder_name == datetime.now().strftime("%Y%m%d"): 
    print("You are naming the tier subfolder using the current day \n")
    print("Snapshots folder name : ~/{}/{}/{}".format(username,remote_folder_name, remote_subfolder_name))
elif do_snapshot:
    print("You are saving snapshots in local")
    print("folder name : " + folder)








cut         = requirements  # ---> see variables.py
regions_def = regions       # ---> see variables.py
var         = vars          # ---> variables.py
var2d       = vars2D        # ---> variables.py

print("Regions to book: ")
for r in regions_def.keys():
    print("  "+r)
print("Variables for histograms :")
print([v._name for v in var])

datasets = []
for in_d in in_dataset:
    if not in_d in sample_dict.keys():
        print("Check the in_dataset string... ", sample_dict.keys())
    else: 
        datasets.append(sample_dict[in_d])
print("Datasets to process: ", [d.label for d in datasets])


chain                       = {}
ntot_events                 = {}
for d in datasets:
    if hasattr(d, "components"):
        samples_list        = d.components
    else:
        samples_list        = [d]
    chain[d.label]          = {}
    ntot_events[d.label]    = {}
    for s in samples_list:
        nfiles              = nfiles_max
        for i, string in enumerate(samples[d.label][s.label]['strings']):
            samples[d.label][s.label]['strings'][i] = string.replace("root://cms-xrd-global.cern.ch/", "root://stormgf2.pi.infn.it/")
        chain[d.label][s.label] = samples[d.label][s.label]['strings'][:nfiles]
        if not "Data" in s.label:
            ntot_events[d.label][s.label] = np.sum(samples[d.label][s.label]['ntot'][:nfiles])
        else:
            ntot_events[d.label][s.label] = None
        print("Dataset : "+s.label)
        print("# of files to process : ", nfiles)
        if len(chain[d.label][s.label])>1:
            print("files strings :\n  {}\n  {}\n  ... \n  {}\n  {}".format(chain[d.label][s.label][0], chain[d.label][s.label][1], chain[d.label][s.label][-2], chain[d.label][s.label][-1]))
        else:
            print("files strings :\n  {}".format(chain[d.label][s.label][0]))
        print("# of total events in the files to process (MC only, if Data the number is None): ", ntot_events[d.label][s.label])






################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_")

################### preselection ###############
def preselection(df, btagAlg, year, EE):
    
    df = df.Define("GoodJet_idx", "GetGoodJet(Jet_pt_nominal, Jet_eta, Jet_jetId)")
    df = df.Define("nGoodJet", "nGoodJet(GoodJet_idx)")
    df = df.Define("GoodFatJet_idx", "GetGoodJet(FatJet_pt_nominal, FatJet_eta, FatJet_jetId)")
    df = df.Define("nGoodFatJet", "GoodFatJet_idx.size()")
    df = df.Filter("nGoodJet>2 || nGoodFatJet>0 ", "jet presel")

    df = df.Redefine("MinDelta_phi", "min_DeltaPhi(PuppiMET_T1_phi_nominal, Jet_phi, GoodJet_idx)")
    df = df.Define("nTightElectron", "nTightElectron(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("TightElectron_idx", "TightElectron_idx(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("nVetoElectron", "nVetoElectron(Electron_pt, Electron_cutBased, Electron_eta)")
    df = df.Define("nTightMuon", "nTightMuon(Muon_pt, Muon_eta, Muon_tightId)")
    df = df.Define("TightMuon_idx", "TightMuon_idx(Muon_pt, Muon_eta, Muon_tightId)")
    df = df.Define("nVetoMuon", "nVetoMuon(Muon_pt, Muon_eta, Muon_looseId)")
    df = df.Define("Lepton_flavour", "Lepton_flavour(nTightElectron, nTightMuon)").Define("Lep_pt", "Lepton_var(Lepton_flavour, Electron_pt, TightElectron_idx, Muon_pt, TightMuon_idx)").Define("Lep_phi", "Lepton_var(Lepton_flavour, Electron_phi, TightElectron_idx, Muon_phi, TightMuon_idx)")
    df = df.Define("MT", "sqrt(2 * Lep_pt * PuppiMET_T1_pt_nominal * (1 - cos(Lep_phi - PuppiMET_T1_phi_nominal)))")
    
    df = df.Define("LeadingJetPt_idx", "GetLeadingPtJet(Jet_pt_nominal)")
    df = df.Define("LeadingJetPt_pt", "GetLeadingJetVar(LeadingJetPt_idx, Jet_pt_nominal)")
    df = df.Define("LeadingJetPt_eta", "GetLeadingJetVar(LeadingJetPt_idx, Jet_eta)")
    df = df.Define("LeadingJetPt_phi", "GetLeadingJetVar(LeadingJetPt_idx, Jet_phi)")
    df = df.Define("LeadingJetPt_mass", "GetLeadingJetVar(LeadingJetPt_idx, Jet_mass_nominal)")
    df = df.Define("LeadingFatJetPt_idx", "GetLeadingPtJet(FatJet_pt)")
    df = df.Define("LeadingFatJetPt_pt", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_pt_nominal)")
    df = df.Define("LeadingFatJetPt_eta", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_eta)")
    df = df.Define("LeadingFatJetPt_phi", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_phi)")
    df = df.Define("LeadingFatJetPt_mass", "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_mass_nominal)")
    df = df.Define("LeadingMuonPt_idx", "GetLeadingPtLep(Muon_pt, Muon_eta, Muon_looseId)")
    df = df.Define("LeadingMuonPt_pt", "GetLeadingJetVar(LeadingMuonPt_idx, Muon_pt)")
    df = df.Define("LeadingMuonPt_eta", "GetLeadingJetVar(LeadingMuonPt_idx, Muon_eta)")
    df = df.Define("LeadingMuonPt_phi", "GetLeadingJetVar(LeadingMuonPt_idx, Muon_phi)")
    df = df.Define("LeadingElectronPt_idx", "GetLeadingPtLep(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("LeadingElectronPt_pt", "GetLeadingJetVar(LeadingElectronPt_idx, Electron_pt)")
    df = df.Define("LeadingElectronPt_eta", "GetLeadingJetVar(LeadingElectronPt_idx, Electron_eta)")
    df = df.Define("LeadingElectronPt_phi", "GetLeadingJetVar(LeadingElectronPt_idx, Electron_phi)")
    
    df = df.Define("nForwardJet", "nForwardJet(Jet_pt_nominal, Jet_jetId, Jet_eta)")
    df = df.Define("MHT","MHT(GoodJet_idx, Jet_pt_nominal, Jet_phi, Jet_eta, Jet_mass_nominal)")
    df = df.Define("JetBTagLoose_idx", "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 0)")\
                .Define("nJetBtagLoose", "static_cast<int>(JetBTagLoose_idx.size());")
    df = df.Define("JetBTagMedium_idx", "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 1)")\
                .Define("nJetBtagMedium", "static_cast<int>(JetBTagMedium_idx.size());")
    df = df.Redefine("PuppiMET_T1_pt_nominal", "PuppiMET_T1_pt_nominal_vec[0]")\
                .Redefine("PuppiMET_T1_phi_nominal", "PuppiMET_T1_phi_nominal_vec[0]")
    
    return df

############### trigger selection #####################
def trigger_filter(df, data, isMC):
    hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
    df_trig = df.Filter(hlt_met, "triggerMET")
    return df_trig

############### top selection ########################
def select_top(df, isMC):
    # return indices of the FatJet with particleNet score over the thresholds 
    df_goodtopMer = df.Define("GoodTopMer_idx", "select_TopMer(FatJet_particleNetWithMass_TvsQCD, GoodFatJet_idx)")
    # return indices of the TopMixed over the threshold with any object in common
    df_goodtopMix = df_goodtopMer.Define("GoodTopMix_idx", "select_TopMix(TopMixed_TopScore_nominal, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx)")
    # return indices of the TopResolved over the threshold with any object in common
    df_goodtopRes = df_goodtopMix.Define("GoodTopRes_idx", "select_TopRes(TopResolved_TopScore_nominal, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx)")
    
    df_nTops = df_goodtopRes.Define("nGoodTopResolved", "nTop(GoodTopRes_idx)")\
                            .Define("nGoodTopMixed", "nTop(GoodTopMix_idx)")\
                            .Define("nGoodTopMerged", "nTop(GoodTopMer_idx)")
    
    
    # return:  1- Event Resolved, 2- Event Mixed, 3- Event Merged, 4- Event Nothing, ...
    df_topcategory = df_nTops.Define("EventTopCategory", "select_TopCategory(GoodTopMer_idx, GoodTopMix_idx, GoodTopRes_idx)")
    if isMC:
        df_topcategory = df_topcategory.Define("EventTopCategoryWithTruth", "select_TopCategoryWithTruth(EventTopCategory, FatJet_matched, GoodTopMer_idx, TopMixed_truth, GoodTopMix_idx, TopResolved_truth, GoodTopRes_idx)")
    
    df_topselected = df_topcategory.Define("Top_idx",
                                           "select_bestTop(EventTopCategory, FatJet_particleNetWithMass_TvsQCD, TopMixed_TopScore_nominal, TopResolved_TopScore_nominal)")
    # return best top idx wrt category --> the idx is referred to the list of candidates fixed by the EventTopCategory
    df_topvariables = df_topselected.Define("Top_pt", "select_TopVar(EventTopCategory, Top_idx, FatJet_pt_nominal, TopMixed_pt_nominal, TopResolved_pt_nominal)")\
                        .Define("Top_eta", "select_TopVar(EventTopCategory, Top_idx, FatJet_eta, TopMixed_eta, TopResolved_eta)")\
                        .Define("Top_phi", "select_TopVar(EventTopCategory, Top_idx, FatJet_phi, TopMixed_phi, TopResolved_phi)")\
                        .Define("Top_mass", "select_TopVar(EventTopCategory, Top_idx, FatJet_mass_nominal, TopMixed_mass_nominal, TopResolved_mass_nominal)")\
                        .Define("Top_score", "select_TopVar(EventTopCategory, Top_idx, FatJet_particleNetWithMass_TvsQCD, TopMixed_TopScore_nominal, TopResolved_TopScore_nominal)")\
                        .Define("Top_isolationPtJetsdR04","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.4, 1)")\
                        .Define("Top_isolationPtJetsdR06","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.6, 1)")\
                        .Define("Top_isolationPtJetsdR08","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.8, 1)")\
                        .Define("Top_isolationPtJetsdR12","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 1.2, 1)")\
                        .Define("Top_isolationNJetsdR04","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.4, 0)")\
                        .Define("Top_isolationNJetsdR06","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.6, 0)")\
                        .Define("Top_isolationNJetsdR08","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.8, 0)")\
                        .Define("Top_isolationNJetsdR12","TopIsolation_NJets(EventTopCategory, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 1.2, 0)")

    if isMC:
        df_topvariables = df_topvariables.Define("Top_truth", "select_TopVar(EventTopCategory, Top_idx, FatJet_matched, TopMixed_truth, TopResolved_truth)")
    # NB: TopTruth for Merged is replaced with FatJet_matched, the variable is between 0 and 3 
    # where 3 means true end less than 3 means false 
    return df_topvariables
def energetic_variations(df):
    #  Da aggiungere variazione dei fatjet
    df_sys = df.Vary(["Jet_pt_nominal", "Jet_mass_nominal", "FatJet_pt_nominal", "FatJet_mass_nominal", "PuppiMET_T1_pt_nominal_vec", "PuppiMET_T1_phi_nominal_vec", "TopMixed_pt_nominal", "TopResolved_pt_nominal", "TopMixed_mass_nominal", "TopResolved_mass_nominal",  "TopMixed_TopScore_nominal", "TopResolved_TopScore_nominal"], "RVec<RVec<RVec<float>>>{{Jet_pt_jerdown, Jet_pt_jerup}, {Jet_mass_jerdown, Jet_mass_jerup}, {FatJet_pt_jerdown, FatJet_pt_jerup}, {FatJet_mass_jerdown, FatJet_mass_jerup}, {PuppiMET_T1_pt_jerdown_vec, PuppiMET_T1_pt_jerup_vec}, {PuppiMET_T1_phi_jerdown_vec, PuppiMET_T1_phi_jerup_vec}, {TopMixed_pt_jerdown, TopMixed_pt_jerup}, {TopResolved_pt_jerdown, TopResolved_pt_jerup}, {TopMixed_mass_jerdown, TopMixed_mass_jerup}, {TopResolved_mass_jerdown, TopResolved_mass_jerup}, {TopMixed_TopScore_jerdown, TopMixed_TopScore_jerup}, {TopResolved_TopScore_jerdown, TopResolved_TopScore_jerup}}", variationTags=["down", "up"], variationName="jer")\
               .Vary(["Jet_pt_nominal", "Jet_mass_nominal", "FatJet_pt_nominal", "FatJet_mass_nominal", "PuppiMET_T1_pt_nominal_vec", "PuppiMET_T1_phi_nominal_vec", "TopMixed_pt_nominal", "TopResolved_pt_nominal", "TopMixed_mass_nominal", "TopResolved_mass_nominal",  "TopMixed_TopScore_nominal", "TopResolved_TopScore_nominal"], "RVec<RVec<RVec<float>>>{{Jet_pt_jesTotaldown, Jet_pt_jesTotalup}, {Jet_mass_jesTotaldown, Jet_mass_jesTotalup}, {FatJet_pt_jesTotaldown, FatJet_pt_jesTotalup}, {FatJet_mass_jesTotaldown, FatJet_mass_jesTotalup}, {PuppiMET_T1_pt_jesTotaldown_vec, PuppiMET_T1_pt_jesTotalup_vec}, {PuppiMET_T1_phi_jesTotaldown_vec, PuppiMET_T1_phi_jesTotalup_vec}, {TopMixed_pt_jesTotaldown, TopMixed_pt_jesTotalup}, {TopResolved_pt_jesTotaldown, TopResolved_pt_jesTotalup}, {TopMixed_mass_jesTotaldown, TopMixed_mass_jesTotalup}, {TopResolved_mass_jesTotaldown, TopResolved_mass_jesTotalup}, {TopMixed_TopScore_jesTotaldown, TopMixed_TopScore_jesTotalup}, {TopResolved_TopScore_jesTotaldown, TopResolved_TopScore_jesTotalup}}", variationTags=["down", "up"], variationName="jesTotal")
    return df_sys
def SF_variations(df):
    df_sys = df.Vary("puWeight", "RVec<float>{puWeightDown, puWeightUp}", variationTags=["down", "up"], variationName="pu")
    return df_sys




def bookhisto(df, regions_def, var, s_cut):
    h_ = {}
    for reg in regions_def.keys():
        h_[reg] = {}
        for v in var:
            if v._MConly and not sampleflag: 
                continue
            else:
                # print(v._name+"_"+reg+"_"+s_cut)
                if regions_def[reg] == "":
                    if "NoPu" in reg: 
                        h_[reg][v._name]= df.Histo1D((v._name+"_"+reg," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name)
                    else: 
                        h_[reg][v._name]= df.Histo1D((v._name+"_"+reg," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name, "w_nominal")
                else:
                    if "NoPu" in reg: 
                        h_[reg][v._name]= df.Filter(regions_def[reg]).Histo1D((v._name+"_"+reg," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name)
                    else: h_[reg][v._name]= df.Filter(regions_def[reg]).Histo1D((v._name+"_"+reg," ;"+v._title, v._nbins, v._xmin, v._xmax), v._name, "w_nominal")
    return h_

def bookhisto2D(df, regions_def, var2d, s_cut):
    h_ = {}
    for reg in regions_def.keys():
        h_[reg] = {}
        for v in var2d:
            if regions_def[reg]=="":
                h_[reg][v._name] = df.Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xmin)+","+str(v._xmax)+")")\
                                     .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
                                     .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname)
            else:
                h_[reg][v._name] = df.Filter(regions_def[reg])\
                                     .Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xmin)+","+str(v._xmax)+")")\
                                     .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
                                     .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname)
    return h_

def savehisto(d, dict_h, regions_def, var, s_cut):
    histo = {reg: {v._name: ROOT.TH1D(v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xmin, v._xmax) for v in var} for reg in regions_def.keys()}
    isMC=True
    if "Data" in d.label: isMC = False
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]
    
    for s in s_list:
        outfile = ROOT.TFile.Open(repohisto+s.label+'.root', "RECREATE")

        for n, vari in enumerate(variations):
            for reg in regions_def.keys():
                for v in var:
                    if "SFbtag" in v._name: continue
                    if v._MConly and not isMC:
                        continue
                    else:
                        # da capire come fare il getvalue e dividere le variazioni
                        if isMC:
                            if do_variations:
                                if vari=='nominal':
                                    h1 = dict_h[d.label][s.label][reg][v._name]["nominal"]
                                    h1.SetName(h1.GetName()+"_nominal")
                                    nbins = h1.GetNbinsX()
                                    if not v._noUnOvFlowbin:
                                        h1.SetBinContent(1, h1.GetBinContent(0) + h1.GetBinContent(1))
                                        h1.SetBinError(1, math.sqrt(pow(h1.GetBinError(0),2) + pow(h1.GetBinError(1),2)))
                                        h1.SetBinContent(nbins, h1.GetBinContent(nbins) + h1.GetBinContent(nbins+1))
                                        h1.SetBinError(nbins, math.sqrt(pow(h1.GetBinError(nbins),2) + pow(h1.GetBinError(nbins+1),2)))
                                    if isMC:
                                        h1.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                    histo_name = h1.GetName()
                                    if "nominal" not in histo_name : h1.SetName(histo_name+"_nominal")
                                    outfile.cd()
                                    h1.Write()
                                else:
                                    for var_type in ['up', 'down']:
                                        h1 = dict_h[d.label][s.label][reg][v._name][vari+":"+var_type]
                                        # h1.SetName(h1.GetName()+"_"+vari+var_type.capitalize())
                                        histo_name = h1.GetName()
                                        if vari+"_"+var_type not in histo_name:
                                            h1.SetName(h1.GetName()+"_"+vari+"_"+var_type)
                                        if not v._noUnOvFlowbin:
                                            nbins = h1.GetNbinsX()
                                            h1.SetBinContent(1, h1.GetBinContent(0) + h1.GetBinContent(1))
                                            h1.SetBinError(1, math.sqrt(pow(h1.GetBinError(0),2) + pow(h1.GetBinError(1),2)))
                                            h1.SetBinContent(nbins, h1.GetBinContent(nbins) + h1.GetBinContent(nbins+1))
                                            h1.SetBinError(nbins, math.sqrt(pow(h1.GetBinError(nbins),2) + pow(h1.GetBinError(nbins+1),2)))
                                            
                                            # Tommaso aggiunge anche questo loop, ma non so bene a cosa serve
                                            # for i in range(0, nbins + 1):          
                                            #     if h1.GetBinContent(i) < 0:
                                            #         h1.SetBinContent(i, 0.)
                                        
                                        if isMC:
                                            h1.Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                        outfile.cd()
                                        h1.Write()
                            else:
                                histo[reg][v._name] = dict_h[d.label][s.label][reg][v._name].GetValue()      
                                if not v._noUnOvFlowbin:
                                    nbins = histo[reg][v._name].GetNbinsX()
                                    histo[reg][v._name].SetBinContent(1, histo[reg][v._name].GetBinContent(0) + histo[reg][v._name].GetBinContent(1))
                                    histo[reg][v._name].SetBinError(1, math.sqrt(pow(histo[reg][v._name].GetBinError(0),2) + pow(histo[reg][v._name].GetBinError(1),2)))
                                    histo[reg][v._name].SetBinContent(nbins, histo[reg][v._name].GetBinContent(nbins) + histo[reg][v._name].GetBinContent(nbins+1))
                                    histo[reg][v._name].SetBinError(nbins, math.sqrt(pow(histo[reg][v._name].GetBinError(nbins),2) + pow(histo[reg][v._name].GetBinError(nbins+1),2)))
                                if isMC:
                                    histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                                outfile.cd()
                                histo[reg][v._name].Write()
                        else:
                            histo[reg][v._name] = dict_h[d.label][s.label][reg][v._name].GetValue()
                            if not v._noUnOvFlowbin:
                                nbins = histo[reg][v._name].GetNbinsX()
                                histo[reg][v._name].SetBinContent(1, histo[reg][v._name].GetBinContent(0) + histo[reg][v._name].GetBinContent(1))
                                histo[reg][v._name].SetBinError(1, math.sqrt(pow(histo[reg][v._name].GetBinError(0),2) + pow(histo[reg][v._name].GetBinError(1),2)))
                                histo[reg][v._name].SetBinContent(nbins, histo[reg][v._name].GetBinContent(nbins) + histo[reg][v._name].GetBinContent(nbins+1))
                                histo[reg][v._name].SetBinError(nbins, math.sqrt(pow(histo[reg][v._name].GetBinError(nbins),2) + pow(histo[reg][v._name].GetBinError(nbins+1),2)))
                            if isMC:
                                histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                            outfile.cd()
                            histo[reg][v._name].Write()
        outfile.Close()

# i plot2d per il momento non ci servono, si deve trovare un modo più intelligente di farli
def savehisto2d(d, h, regions_def, var2d, s_cut):
    histo = {reg: {v._name: ROOT.TH2D(v._name+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax,) for v in var2d} for reg in regions_def.keys()}
        
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]
    
    for s in s_list:
        outfile = ROOT.TFile.Open(repohisto+s.label+'_2D.root', "RECREATE")
        for reg in regions_def.keys():
            for v in histo[reg].keys():
                histo[reg][v] = h[d.label][s.label][reg][v].GetValue()
                if isMC:
                    histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                outfile.cd()
                histo[reg][v].Write()
        outfile.Close()



    





t0 = datetime.now()
print("starting loop on datasets: ", [d.label for d in datasets])
print("Local time :", t0)
# print("requirements: "+cut)

h                           = {}
h_2D                        = {}
if do_variations:
    h_varied                = {}

for d in datasets:
    s_list                  = []
    if hasattr(d, "components"):
        s_list              = d.components
    else:
        s_list              = [d]
    if 'Data' in d.label:
        sampleflag          = 0
    else:
        sampleflag          = 1
    c_                      = cut
    h[d.label]              = {}
    h_2D[d.label]           = {}
    if do_variations:
        h_varied[d.label]   = {}
    for s in s_list:
        #------------------------------------------------------------------------------
        ############# Fixing variables for 2018-2022-2023 #############################
        #------------------------------------------------------------------------------
        if s.year == 2018:
            bTagAlg = "Jet_btagDeepB"
        elif s.year in [2022,2023]:
            bTagAlg = "Jet_btagPNetB"
        if hasattr(s,"EE"):
            EE = s.EE
        else:
            EE = 0
        #-------------------------------------------------------------------------
        #########################  DF initialization #############################
        #-------------------------------------------------------------------------
        
        print("Initializing DataFrame for "+ s.label +" chain len = ", len(chain[d.label][s.label]))
        if len(chain[d.label][s.label])==1:
            print(chain[d.label][s.label])
        df                  = ROOT.RDataFrame("Events", chain[d.label][s.label])
        df                  = df.Define("PuppiMET_T1_pt_nominal_vec", "RVec<float>{ (float) PuppiMET_T1_pt_nominal}").Define("PuppiMET_T1_phi_nominal_vec", "RVec<float>{ (float) PuppiMET_T1_phi_nominal}")


        if do_variations:
            df              = df.Define("PuppiMET_T1_pt_jerdown_vec", "RVec<float>{ (float) PuppiMET_T1_pt_jerdown}").Define("PuppiMET_T1_phi_jerdown_vec", "RVec<float>{ (float) PuppiMET_T1_phi_jerdown}")\
                                .Define("PuppiMET_T1_pt_jerup_vec", "RVec<float>{ (float) PuppiMET_T1_pt_jerup}").Define("PuppiMET_T1_phi_jerup_vec", "RVec<float>{ (float) PuppiMET_T1_phi_jerup}")\
                                .Define("PuppiMET_T1_pt_jesTotaldown_vec", "RVec<float>{ (float) PuppiMET_T1_pt_jesTotaldown}").Define("PuppiMET_T1_phi_jesTotaldown_vec", "RVec<float>{ (float) PuppiMET_T1_phi_jesTotaldown}")\
                                .Define("PuppiMET_T1_pt_jesTotalup_vec", "RVec<float>{ (float) PuppiMET_T1_pt_jesTotalup}").Define("PuppiMET_T1_phi_jesTotalup_vec", "RVec<float>{ (float) PuppiMET_T1_phi_jesTotalup}")
            df              = SF_variations(df)
            df              = energetic_variations(df)
        else:
            df              = df
        df_ismc             = df.Define("isMC", "isMC("+str(sampleflag)+")")
        df_year             = df_ismc.Define("year", str(s.year))
        df_hemveto          = df_year.Define("HEMVeto", "hemveto(Jet_eta, Jet_phi, Electron_eta, Electron_phi)")
        df_hemveto          = df_hemveto.Filter("(isMC || (year != 2018) || (HEMVeto || run<319077.))")
        df_hlt              = trigger_filter(df_hemveto, s.label, sampleflag)
        
        if "ZJets" in s.label: 
            df_hlt = df_hlt.Define("w_nominal", "nloewcorrectionZ(1., GenPart_pdgId, GenPart_pt, GenPart_statusFlags)")
            # df_hlt = df_hlt.Define("w_nominal", "1")                                                                                             # no nloewcorrection
        elif "WJets" in s.label:
            df_hlt = df_hlt.Define("w_nominal", "nloewcorrectionW(1., GenPart_pdgId, GenPart_pt, GenPart_statusFlags)")
            # df_hlt = df_hlt.Define("w_nominal", "1")                                                                                             # no nloewcorrection
        else:
            df_hlt = df_hlt.Define("w_nominal", "1")
            
        if sampleflag:
            df_wnom = df_hlt.Redefine('w_nominal', 'w_nominal*puWeight*SFbtag_nominal*(LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP))') # AllWeights
            # df_wnom = df_hlt.Redefine('w_nominal', 'w_nominal*puWeight*(LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP))')                # no SFbtag
            # df_wnom = df_hlt.Redefine('w_nominal', 'w_nominal*SFbtag_nominal*(LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP))')          # no puWeight
        else:
            df_wnom = df_hlt.Redefine('w_nominal', '1')

            
        # df_wnom           = df_hlt.Define('w_nominal', '1')
        df_presel       = preselection(df_wnom, bTagAlg, s.year, EE)
        df_topsel       = select_top(df_presel, sampleflag)
        df_topsel       = df_topsel.Define("MT_T", "sqrt(2 * Top_pt * PuppiMET_T1_pt_nominal * (1 - cos(Top_phi - PuppiMET_T1_phi_nominal)))")
        
        if do_snapshot:
            opts        = ROOT.RDF.RSnapshotOptions()
            opts.fLazy  = True
            fold        = folder
            snapshot_df = df_topsel.Snapshot("events_nominal", fold+"snap_"+s.label+".root", branches, opts)
            # print("./"+s.label+".root")
        if do_histos:
            s_cut = cut_string(cut)
            if len(var) != 0 :
                h[d.label][s.label] = bookhisto(df_topsel, regions_def, var, s_cut)
            if len(var2d) != 0 :
                h_2D[d.label][s.label] = bookhisto2D(df_topsel, regions_def, var2d, s_cut)

        
        if do_variations:
            # h [dataset][label][region][variable]
            print("applying vary")
            h_varied[d.label][s.label]={}
            for reg in regions_def.keys():
                h_varied[d.label][s.label][reg] = {}
                for v in var:
                    if "SFbtag" in v._name:
                        continue
                    h_varied[d.label][s.label][reg][v._name] = ROOT.RDF.Experimental.VariationsFor(h[d.label][s.label][reg][v._name])

if do_histos:
    print("All histos booked!")
    for d in datasets:
        if len(var):
            if do_variations:
                print(h_varied.keys())
                # print(h_varied[d.label].keys())
                savehisto(d, h_varied, regions_def, var, s_cut)
            else:
                savehisto(d, h, regions_def, var, s_cut)
        if len(var2d) != 0 :
            savehisto2d(d, h_2D, regions_def, var2d, s_cut)
        print(d.label + " histos saved")
if do_snapshot:
    snapshot_df.GetValue()
    print("Snapshot done!")
t1 = datetime.now()
print("Job finished in: ", t1-t0)