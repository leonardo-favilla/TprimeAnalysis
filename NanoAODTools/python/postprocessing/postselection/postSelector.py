import ROOT
# ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
import sys
import os
import optparse
import json
import numpy as np
import math
import shutil
from datetime import datetime
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.bookhisto import bookhisto
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.bookhisto2D import bookhisto2D
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.savehisto import savehisto
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.savehisto2d import savehisto2d
from PhysicsTools.NanoAODTools.postprocessing.postselection.utils.weightsets import REMOVABLE_WEIGHTS, parse_weightsets
import importlib.util
# from PhysicsTools.NanoAODTools.postprocessing.variables import *
sys.path.append('../')

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
WorkDir  = os.environ["PWD"]

usage                   = 'python3 postSelector.py -d <datasets> --dict_samples_file <dict_samples_file> --hist_folder <hist_folder> --nfiles_max <nfiles_max> --noTrotaSF --weightset allWeights --weightset noSFbtag --syst'
parser                  = optparse.OptionParser(usage)
parser.add_option('-d', '--datasets',           dest='datasets',            type=str,               default="QCD_2023",                             help='Datasets to process, in the form: QCD_2023,TT_2023...')
parser.add_option(      '--dict_samples_file',  dest='dict_samples_file',   type=str,               default="../samples/dict_samples_2023.json",    help='Path to the JSON file containing the sample definitions')
parser.add_option(      '--varfile',            dest='varfile',             type=str,               default="../variables.py",                      help='Path to the variable file')
parser.add_option(      '--hist_folder',        dest='hist_folder',         type=str,               default="",                                     help='Folder where to save the histograms')
parser.add_option(      '--syst',               dest='syst',                action='store_true',    default=False,                                  help='calculate jerc')
parser.add_option(      '--nfiles_max',         dest='nfiles_max',          type=int,               default=1,                                      help='Max number of files to process per sample')
parser.add_option(      '--noSFbtag',           dest='noSFbtag',            action='store_true',    default=False,                                  help='remove b tag SF')
parser.add_option(      '--noPuWeight',         dest='noPuWeight',          action='store_true',    default=False,                                  help='remove PU weight')
parser.add_option(      '--noTopPtWeight',      dest='noTopPtWeight',       action='store_true',    default=False,                                  help='remove top pt weight')
parser.add_option(      '--noTrotaSF',          dest='noTrotaSF',           action='store_true',    default=False,                                  help='remove Trota SF')
parser.add_option(      '--weightset',          dest='weightset',           action='append',        default=None,                                   help='set of weights to produce the histograms with, repeatable: allWeights or the weights to remove separated by commas, '
                                                                                                                                                                                 'e.g. --weightset allWeights --weightset noSFbtag --weightset noSFbtag,noTrotaSF; the --noXXX options remove the weight from every weightset. '
                                                                                                                                                                                 'Each weightset is saved in <hist_folder>/<removed weights joined by _, or allWeights>/plots/; default: one weightset, allWeights')
parser.add_option(      '--tmpfold',            dest='tmpfold',             action='store_true',    default=False,                                  help='test tmp folder for out file')
parser.add_option(      '--printcutflow',       dest='printcutflow',        action='store_true',    default=False,                                  help='print cutflow')
parser.add_option(      '--partsize',       dest='partsize',        type=int,    default=-1,                                  help='number of files to run for a given portion To use if you are doing the a-priori splitting option, together with firstfile  ')
parser.add_option(      '--firstfile',       dest='firstfile',        type=int,    default=0,                                  help='fist file to run in the dataset, to use together with partsize')
parser.add_option(      '--npart',       dest='npart',        type=int,    default=1,                                  help='part number of the dataset for the outfile, to use together with partsize')
parser.add_option(      '--snapshot',           dest='snapshot',            action='store_true',    default=False,                                  help='instead of the histograms, save the preselected events (b-tag columns and weights, see branches) in <hist_folder>/snapshots/snap_<sample>.root; not with --syst')



(opt, args)             = parser.parse_args()
in_dataset              = opt.datasets.split(",")
nfiles_max              = opt.nfiles_max
do_variations           = opt.syst
global_removed          = [n for n in REMOVABLE_WEIGHTS if getattr(opt, n)]     # --noXXX options given
weightsets              = parse_weightsets(opt.weightset, global_removed)       # [(label, removed weights)]
useTrotaSF              = any("noTrotaSF" not in removed for label, removed in weightsets)
dict_samples_file       = opt.dict_samples_file
hist_folder             = opt.hist_folder
tmpfold                 = opt.tmpfold
printcutflow            = opt.printcutflow
varfile                 = opt.varfile
do_snapshot             = opt.snapshot
do_histos               = not do_snapshot
if do_snapshot and do_variations:
    print("ERROR: --snapshot cannot be used with --syst")
    sys.exit(1)

partsize=opt.partsize
firstfile=opt.firstfile
npart=opt.npart

partname="" if partsize==-1 else "_part"+str(npart)

if do_variations == True:
    variations          = ["nominal", "pu", "jer", "jesTotal", "pdf_total", "QCDScale", "ISR", "FSR", "triggerSF"]
    if useTrotaSF:
        variations      += ["TrotaResolved", "TrotaMixed", "TrotaMerged"]
else :
    variations          = ["nominal"]

if hist_folder=="":
    print("Please provide a valid hist_folder name")
    sys.exit(1)
folder                  = hist_folder
repohisto               = {label: folder+label+"/plots/" for label, removed in weightsets}     # one output folder per weightset

if not os.path.exists(folder):
    os.makedirs(folder, exist_ok=True)
for label, removed in weightsets:
    if do_histos and not os.path.exists(repohisto[label]):
        os.makedirs(repohisto[label], exist_ok=True)


# columns saved with --snapshot (the ones missing in a sample, e.g. the MC-only ones in Data, are skipped), plus the w_<weightset> columns
branches = [
            "run", "luminosityBlock", "event",
            "nGoodJet", "GoodJet_idx",
            "Jet_pt_nominal", "Jet_eta", "Jet_hadronFlavour", "Jet_btagUParTAK4B", "Jet_btagPNetB",
            "nJetBtagLoose", "nJetBtagMedium",
            "PuppiMET_T1_pt_nominal",
            "SFbtag_nominal", "puWeight", "triggerSF", "NLOEW", "w_topPt", "LHEWeight_originalXWGTUP",
           ]

#### LOAD utils/postselection.h ####
text_file = open(WorkDir+"/postselection.h", "r")
data      = text_file.read()
def my_initialization_function():
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(data))
    print("end of initialization")
my_initialization_function()

#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)

#### LOAD variables.py ####
variables_path  = os.path.abspath(varfile)
spec            = importlib.util.spec_from_file_location("variables", variables_path)
variables       = importlib.util.module_from_spec(spec)
spec.loader.exec_module(variables)

#### LOAD TopTagging_WorkingPoints.json ####
with open(WorkDir+"/TopTagging_WorkingPoints.json", "r") as json_file:
    TopTagging_WorkingPoints = json.load(json_file)

if do_histos:
    print("You are producing histograms")
    print("local folder histos: {}".format(folder))
snapshot_folder         = folder+"snapshots/"
snapshot_dfs            = []        # lazy snapshots, one per sample, all run at the end
if do_snapshot:
    print("You are producing snapshots, no histograms")
    print("snapshots folder: " + snapshot_folder)
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)








cut         = variables.requirements  # ---> see variables.py
regions_def = variables.regions       # ---> see variables.py
var         = variables.vars          # ---> variables.py
var2d       = variables.vars2D        # ---> variables.py

TopSF_CorrLibFilePath_dict = {
                                "2022":             "",
                                "2022EE":           "",
                                # "2023":             "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/corrections/2023/CorrLib_TrotaScaleFactors_2023.json",
                                # "2023":             "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/corrections/2023_NewWPs/CorrLib_TrotaScaleFactors_2023.json",
                                "2023":             "./TopSF-corrections/2023/CorrLib_TrotaScaleFactors_2023.json",
                                "2023postBPix":     "",
                                "2024":             "",
                            }
BTV_CorrLibFilePath_dict        = {
                                "2024":             "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-10-20/btagging.json.gz",
                            }
BTagEff_CorrLibFilePath_dict    = {
                                "2024":             "../BTagEfficiency/BTagEfficiency_2024.json",
                            }


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
        print("Dataset is ", in_d, "sample is ", sample_dict[in_d])
        datasets.append(sample_dict[in_d])
print("Datasets to process: ", [d.label for d in datasets])



chain                       = {}
ntot_events                 = {}
tchains                     = {}
outfile_dict                = {label: {} for label, removed in weightsets}      # outfile_dict[weightset][sample]
for d in datasets:
    if hasattr(d, "components"):
        samples_list        = d.components
    else:
        samples_list        = [d]
    for s in samples_list:
        for label, removed in weightsets:
            if tmpfold:
                repohisto_tmp = "/tmp/"+username+"/"+os.path.basename(os.path.normpath(hist_folder))+"/"+label+"/"+s.label+"/"
                os.makedirs(repohisto_tmp, exist_ok=True)      # exist_ok: parts of the same sample started together on one node
                outfile_path = repohisto_tmp+s.label+partname+'.root'
                print("outfile path is: ",outfile_path)
            else:
                outfile_path = repohisto[label]+s.label+partname+'.root'

            outfile_dict[label][s.label] = outfile_path
    chain[d.label]          = {}
    ntot_events[d.label]    = {}
    tchains[d.label]        = {}
    for s in samples_list:
        totfiles = (len(samples[d.label][s.label]['strings']))
        nfiles = min(nfiles_max,totfiles)
        nstart=0
        nend= nfiles_max
        if(partsize>-1):
            nstart=firstfile 
            nend=firstfile+partsize
            print(" firstfile n ",nstart," lastfile n ",nend)
        for i, string in enumerate(samples[d.label][s.label]['strings']):
            # samples[d.label][s.label]['strings'][i] = string.replace("root://cms-xrd-global.cern.ch/", "davs://stwebdav.pi.infn.it:8443/cms/") # root://stormgf2.pi.infn.it/
            samples[d.label][s.label]['strings'][i] = string.replace("root://cms-xrd-global.cern.ch/", "root://xrootd-cms.infn.it/") # root://stormgf2.pi.infn.it/
        chain[d.label][s.label] = samples[d.label][s.label]['strings'][nstart:nend]
        if not "Data" in s.label:
            if (partsize>-1):
                # part method: every part is normalized to the total weight of ALL the files of the sample,
                # assuming all the parts will be summed together (-m h of postSelector_submitter_large.py)
                ntot_events[d.label][s.label] = np.sum(samples[d.label][s.label]['ntot'][0:totfiles])
            else:
                # no parts: the output is used alone, so it is normalized to the total weight of the files actually processed
                # (the first nfiles_max files; all of them when nfiles_max >= number of files, as in the submitters)
                ntot_events[d.label][s.label] = np.sum(samples[d.label][s.label]['ntot'][nstart:nend])
        else:
            ntot_events[d.label][s.label] = None
        print("Dataset : "+s.label)
        print("# of files to process : ", len(chain[d.label][s.label]))
        if len(chain[d.label][s.label])>1:
            print("files strings :\n  {}\n  {}\n  ... \n  {}\n  {}".format(chain[d.label][s.label][0], chain[d.label][s.label][1], chain[d.label][s.label][-2], chain[d.label][s.label][-1]))
        else:
            print("files strings :\n  {}".format(chain[d.label][s.label][0]))
        print("# of total events in the files to process (MC only, if Data the number is None): ", ntot_events[d.label][s.label])

        #### tchain def
        tchains[d.label][s.label] = ROOT.TChain("Events")
        for i, f in enumerate(chain[d.label][s.label]):
            try:
                TFile = ROOT.TFile.Open(f)
                tchains[d.label][s.label].Add(f)
            except:
                if ntot_events[d.label][s.label] is not None:       # None for Data
                    ntot_events[d.label][s.label] -= samples[d.label][s.label]['ntot'][nstart+i]       # i counts from the first file of the part
                print("Could not add file: ", f)
                if (partsize>=-1):
                    print("Since using the part method we are interrupting the job with an ERROR")
                    sys.exit(1)
                continue
        print("Number of events in the TChain: ", tchains[d.label][s.label].GetEntries())
        print("Number of total events in the TChain (MC only, if Data the number is None): ", ntot_events[d.label][s.label])

print("outfile_dict has following entries: ")
for label, removed in weightsets:
    print(f"  weightset {label} (removed: {', '.join(n for n in REMOVABLE_WEIGHTS if n in removed) or 'none'})")
    for k, v in outfile_dict[label].items():
        print(f"    {k}: {v}")

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_")

################### GenTopLep ################
def GenTopLep(df):
    df = df.Define("nTopGenLep",        "countTopGenLep(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_genPartIdxMother_prompt, GenPart_statusFlags)")\
           .Define("TopGenLep_idx",     "TopGenLep_genPartIdx(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_genPartIdxMother_prompt, GenPart_statusFlags)")\
           .Define("TopGenLep_pt",      "TopGenLep_var(TopGenLep_idx, GenPart_pt)")\
           .Define("TopGenLep_eta",     "TopGenLep_var(TopGenLep_idx, GenPart_eta)")\
           .Define("TopGenLep_phi",     "TopGenLep_var(TopGenLep_idx, GenPart_phi)")\
           .Define("TopGenLep_mass",    "TopGenLep_var(TopGenLep_idx, GenPart_mass)")

    return df

################### preselection ###############
def preselection(df, btagAlg, year, EE):
    if year in [2022,2023]:
        df = df.Define("Jet_passJetIdTight",            "Jet_passJetIdTight(Jet_eta, Jet_jetId, Jet_neHEF, Jet_neEmEF)")\
               .Define("Jet_passJetIdTightLepVeto",     "Jet_passJetIdTightLepVeto(Jet_eta, Jet_passJetIdTight, Jet_muEF, Jet_chEmEF)")\
               .Redefine("Jet_jetId",                   "ROOT::VecOps::RVec<int>(Jet_passJetIdTight) * 2 + ROOT::VecOps::RVec<int>(Jet_passJetIdTightLepVeto) * 4") # https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV
    elif year in [2024]:
        df = df

    # leptons: ID, isolation, pt, eta only (no DeltaR from jets)
    df = df.Define("nTightElectron",                    "nTightElectron(Electron_pt, Electron_eta, Electron_cutBased, Electron_mvaIso_WP80)")\
           .Define("TightElectron_idx",                 "TightElectron_idx(Electron_pt, Electron_eta, Electron_cutBased, Electron_mvaIso_WP80)")\
           .Define("nLooseElectron",                    "nLooseElectron(Electron_pt, Electron_eta, Electron_cutBased, Electron_mvaIso_WP80)")\
           .Define("LooseElectron_idx",                 "LooseElectron_idx(Electron_pt, Electron_eta, Electron_cutBased, Electron_mvaIso_WP80)")\
           .Define("nVetoElectron",                     "nVetoElectron(Electron_pt, Electron_cutBased, Electron_eta, Electron_mvaIso_WP80)")\
           .Define("VetoElectron_idx",                  "VetoElectron_idx(Electron_pt, Electron_cutBased, Electron_eta, Electron_mvaIso_WP80)")
    df = df.Define("nTightMuon",                        "nTightMuon(Muon_pt, Muon_eta, Muon_tightId, Muon_pfIsoId)")\
           .Define("TightMuon_idx",                     "TightMuon_idx(Muon_pt, Muon_eta, Muon_tightId, Muon_pfIsoId)")\
           .Define("nLooseMuon",                        "nLooseMuon(Muon_pt, Muon_eta, Muon_looseId, Muon_pfIsoId)")\
           .Define("LooseMuon_idx",                     "LooseMuon_idx(Muon_pt, Muon_eta, Muon_looseId, Muon_pfIsoId)")\
           .Define("nVetoMuon",                         "nVetoMuon(Muon_pt, Muon_eta, Muon_looseId, Muon_pfIsoId)")\
           .Define("VetoMuon_idx",                      "VetoMuon_idx(Muon_pt, Muon_eta, Muon_looseId, Muon_pfIsoId)")

    # jets: jetId==6, pt>30, |eta|<2.4, and DeltaR>=0.4 from every veto electron and veto muon
    df = df.Define("GoodJet_idx",                       "CleanGoodJets_fromVetoLeptons(GetGoodJet(Jet_pt_nominal, Jet_eta, Jet_jetId), Jet_eta, Jet_phi, VetoElectron_idx, Electron_eta, Electron_phi, VetoMuon_idx, Muon_eta, Muon_phi, 0.4)")
    df = df.Define("nGoodJet",                          "GoodJet_idx.size()")
    df = df.Define("GoodFatJet_idx",                    "GetGoodFatJet(FatJet_pt_nominal, FatJet_eta, FatJet_jetId)") # richiesto jetId==6
    df = df.Define("nGoodFatJet",                       "GoodFatJet_idx.size()")
    df = df.Filter("nGoodJet>2 || nGoodFatJet>0 ",      "jet presel")

    df = df.Redefine("MinDelta_phi",                    "min_DeltaPhi(PuppiMET_T1_phi_nominal, Jet_phi, GoodJet_idx)")

    df = df.Define("Lepton_flavour",                    "Lepton_flavour(nTightElectron, nTightMuon)").Define("Lep_pt", "Lepton_var(Lepton_flavour, Electron_pt, TightElectron_idx, Muon_pt, TightMuon_idx)").Define("Lep_phi", "Lepton_var(Lepton_flavour, Electron_phi, TightElectron_idx, Muon_phi, TightMuon_idx)")
    df = df.Define("MT",                                "sqrt(2 * Lep_pt * PuppiMET_T1_pt_nominal * (1 - cos(Lep_phi - PuppiMET_T1_phi_nominal)))")
    
    df = df.Define("LeadingJetPt_idx",                  "GetLeadingPtJet(Jet_pt_nominal)")\
           .Define("LeadingJetPt_pt",                   "GetLeadingJetVar(LeadingJetPt_idx, Jet_pt_nominal)")\
           .Define("LeadingJetPt_eta",                  "GetLeadingJetVar(LeadingJetPt_idx, Jet_eta)")\
           .Define("LeadingJetPt_phi",                  "GetLeadingJetVar(LeadingJetPt_idx, Jet_phi)")\
           .Define("LeadingJetPt_mass",                 "GetLeadingJetVar(LeadingJetPt_idx, Jet_mass_nominal)")
    df = df.Define("LeadingFatJetPt_idx",               "GetLeadingPtJet(FatJet_pt_nominal)")\
           .Define("LeadingFatJetPt_pt",                "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_pt_nominal)")\
           .Define("LeadingFatJetPt_eta",               "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_eta)")\
           .Define("LeadingFatJetPt_phi",               "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_phi)")\
           .Define("LeadingFatJetPt_mass",              "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_mass_nominal)")\
           .Define("LeadingFatJetPt_msoftdrop",         "GetLeadingJetVar(LeadingFatJetPt_idx, FatJet_msoftdrop_nominal)")
    df = df.Define("LeadingMuonPt_idx",                 "GetLeadingPtLep(Muon_pt, Muon_eta, Muon_looseId)")\
           .Define("LeadingMuonPt_pt",                  "GetLeadingJetVar(LeadingMuonPt_idx, Muon_pt)")\
           .Define("LeadingMuonPt_eta",                 "GetLeadingJetVar(LeadingMuonPt_idx, Muon_eta)")\
           .Define("LeadingMuonPt_phi",                 "GetLeadingJetVar(LeadingMuonPt_idx, Muon_phi)")\
           .Define("LeadingElectronPt_idx",             "GetLeadingPtLep(Electron_pt, Electron_eta, Electron_cutBased)")\
           .Define("LeadingElectronPt_pt",              "GetLeadingJetVar(LeadingElectronPt_idx, Electron_pt)")\
           .Define("LeadingElectronPt_eta",             "GetLeadingJetVar(LeadingElectronPt_idx, Electron_eta)")\
           .Define("LeadingElectronPt_phi",             "GetLeadingJetVar(LeadingElectronPt_idx, Electron_phi)")
    
    df = df.Define("nForwardJet",                       "nForwardJet(Jet_pt_nominal, Jet_jetId, Jet_eta)") #richiesto jetId==6
    df = df.Define("MHT",                               "MHT(GoodJet_idx, Jet_pt_nominal, Jet_phi, Jet_eta, Jet_mass_nominal)")
    df = df.Define("JetBTagLoose_idx",                  "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 0)")\
           .Define("nJetBtagLoose",                     "static_cast<int>(JetBTagLoose_idx.size());")\
           .Define("JetBTagMedium_idx",                 "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 1)")\
           .Define("nJetBtagMedium",                    "static_cast<int>(JetBTagMedium_idx.size());")\
           .Define("JetBTagTight_idx",                  "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+", 2)")\
           .Define("nJetBtagTight",                     "static_cast<int>(JetBTagTight_idx.size());")\
           .Define("JetBTagScore",                      "GetJetBTagScore(GoodJet_idx, "+bTagAlg+")")

    df = df.Redefine("PuppiMET_T1_pt_nominal",          "PuppiMET_T1_pt_nominal_vec[0]")\
           .Redefine("PuppiMET_T1_phi_nominal",         "PuppiMET_T1_phi_nominal_vec[0]")
    
    return df

############### trigger selection #####################
def trigger_filter(df, data, isMC):
    hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
    df_trig = df.Filter(hlt_met, "triggerMET")
    return df_trig

############### top selection ########################
def select_top(df, isMC, year):
    if year in [2022,2023]:
        TopMerged_discriminator = "particleNetWithMass_TvsQCD"
    elif year in [2024]:
        TopMerged_discriminator = "globalParT3_withMassTopvsQCD"

        
    df            = df.Define("TopMerged_TopScore_nominal",         f"FatJet_{TopMerged_discriminator}")\
    # return indices of the FatJet with particleNet score over the thresholds
    df_goodtopMer = df.Define("LooseTopMer_idx",                    f"select_TopMer(TopMerged_TopScore_nominal, GoodFatJet_idx, {Top_Merged_wp['10%']})")\
                      .Define("TightTopMer_idx",                    f"select_TopMer(TopMerged_TopScore_nominal, GoodFatJet_idx, {Top_Merged_wp['5%']})")\
                      .Define("LooseNOTTightTopMer_idx",            f"SubtractIntVectors(LooseTopMer_idx, TightTopMer_idx)")
    # return indices of the TopMixed over the threshold with any object in common
    df_goodtopMix = df_goodtopMer.Define("LooseTopMix_idx",         f"select_TopMix(TopMixed_TopScore_nominal, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx, {Top_Mixed_wp['10%']})")\
                                 .Define("TightTopMix_idx",         f"select_TopMix(TopMixed_TopScore_nominal, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx, {Top_Mixed_wp['5%']})")\
                                 .Define("LooseNOTTightTopMix_idx", f"SubtractIntVectors(LooseTopMix_idx, TightTopMix_idx)")
    # return indices of the TopResolved over the threshold with any object in common
    df_goodtopRes = df_goodtopMix.Define("LooseTopRes_idx",         f"select_TopRes(TopResolved_TopScore_nominal, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx, {Top_Resolved_wp['10%']})")\
                                 .Define("TightTopRes_idx",         f"select_TopRes(TopResolved_TopScore_nominal, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx, {Top_Resolved_wp['5%']})")\
                                 .Define("LooseNOTTightTopRes_idx", f"SubtractIntVectors(LooseTopRes_idx, TightTopRes_idx)")

    # extra-tight (XT, 1% mistag) tops, only for the eras with the "1%" WP in TopTagging_WorkingPoints.json
    # (for the other eras the XT lists are empty: the XT categories 1-3 are empty and 4-6 are exactly the old Tight 1-3).
    if ("1%" in Top_Merged_wp) and ("1%" in Top_Mixed_wp) and ("1%" in Top_Resolved_wp):
        df_goodtopXT = df_goodtopRes.Define("XTightTopMer_idx",     f"select_TopMer(TopMerged_TopScore_nominal, GoodFatJet_idx, {Top_Merged_wp['1%']})")\
                                    .Define("XTightTopMix_idx",     f"select_TopMix(TopMixed_TopScore_nominal, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx, {Top_Mixed_wp['1%']})")\
                                    .Define("XTightTopRes_idx",     f"select_TopRes(TopResolved_TopScore_nominal, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx, {Top_Resolved_wp['1%']})")
    else:
        print(f"No XT (1%) top tagging WP for era {year} in TopTagging_WorkingPoints.json: no XT tops, the XT categories 1-3 are empty")
        df_goodtopXT = df_goodtopRes.Define("XTightTopMer_idx",     "ROOT::VecOps::RVec<int>()")\
                                    .Define("XTightTopMix_idx",     "ROOT::VecOps::RVec<int>()")\
                                    .Define("XTightTopRes_idx",     "ROOT::VecOps::RVec<int>()")
    df_goodtopXT = df_goodtopXT.Define("TightNOTXTightTopMer_idx",  "SubtractIntVectors(TightTopMer_idx, XTightTopMer_idx)")\
                               .Define("TightNOTXTightTopMix_idx",  "SubtractIntVectors(TightTopMix_idx, XTightTopMix_idx)")\
                               .Define("TightNOTXTightTopRes_idx",  "SubtractIntVectors(TightTopRes_idx, XTightTopRes_idx)")

    df_nTops = df_goodtopXT.Define("nLooseTopResolved", "nTop(LooseTopRes_idx)")\
                            .Define("nLooseTopMixed", "nTop(LooseTopMix_idx)")\
                            .Define("nLooseTopMerged", "nTop(LooseTopMer_idx)")\
                            .Define("nTightTopResolved", "nTop(TightTopRes_idx)")\
                            .Define("nTightTopMixed", "nTop(TightTopMix_idx)")\
                            .Define("nTightTopMerged", "nTop(TightTopMer_idx)")\
                            .Define("nXTightTopResolved", "nTop(XTightTopRes_idx)")\
                            .Define("nXTightTopMixed", "nTop(XTightTopMix_idx)")\
                            .Define("nXTightTopMerged", "nTop(XTightTopMer_idx)")
    
    # EventTopCategory (see select_TopCategoryWithXT in postselection.h):
    #   1-3 XT, 4-6 Tight-not-XT, 7-9 Loose-not-Tight (Resolved, Mixed, Merged), 10 else
    # EventTopFlavour: 1 Resolved, 2 Mixed, 3 Merged for categories 1-9, 7 for category 10 (old "else" category,
    # used by select_TopVar and TopIsolation_NJets)
    df_topcategory = df_nTops.Define("EventTopCategory", "select_TopCategoryWithXT(XTightTopMer_idx, XTightTopMix_idx, XTightTopRes_idx, TightNOTXTightTopMer_idx, TightNOTXTightTopMix_idx, TightNOTXTightTopRes_idx, LooseNOTTightTopMer_idx, LooseNOTTightTopMix_idx, LooseNOTTightTopRes_idx)")\
                             .Define("EventTopFlavour",  "TopFlavourOfCategory(EventTopCategory)")

    df_topselected = df_topcategory.Define("Top_idx",
                                           "select_bestTopInCategory(EventTopCategory, XTightTopMer_idx, XTightTopMix_idx, XTightTopRes_idx, TightNOTXTightTopMer_idx, TightNOTXTightTopMix_idx, TightNOTXTightTopRes_idx, LooseNOTTightTopMer_idx, LooseNOTTightTopMix_idx, LooseNOTTightTopRes_idx, TopMerged_TopScore_nominal, TopMixed_TopScore_nominal, TopResolved_TopScore_nominal)")
    # return best top idx wrt category --> the idx is referred to the list of candidates fixed by the EventTopCategory
    df_topvariables = df_topselected.Define("Top_pt", "select_TopVar(EventTopFlavour, Top_idx, FatJet_pt_nominal, TopMixed_pt_nominal, TopResolved_pt_nominal)")\
                        .Define("Top_eta", "select_TopVar(EventTopFlavour, Top_idx, FatJet_eta, TopMixed_eta, TopResolved_eta)")\
                        .Define("Top_phi", "select_TopVar(EventTopFlavour, Top_idx, FatJet_phi, TopMixed_phi, TopResolved_phi)")\
                        .Define("Top_mass", "select_TopVar(EventTopFlavour, Top_idx, FatJet_mass_nominal, TopMixed_mass_nominal, TopResolved_mass_nominal)")\
                        .Define("Top_score", "select_TopVar(EventTopFlavour, Top_idx, TopMerged_TopScore_nominal, TopMixed_TopScore_nominal, TopResolved_TopScore_nominal)")\
                        .Define("Top_isolationPtJetsdR04","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.4, 1)")\
                        .Define("Top_isolationPtJetsdR06","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.6, 1)")\
                        .Define("Top_isolationPtJetsdR08","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.8, 1)")\
                        .Define("Top_isolationPtJetsdR12","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 1.2, 1)")\
                        .Define("Top_isolationNJetsdR04","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.4, 0)")\
                        .Define("Top_isolationNJetsdR06","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.6, 0)")\
                        .Define("Top_isolationNJetsdR08","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 0.8, 0)")\
                        .Define("Top_isolationNJetsdR12","TopIsolation_NJets(EventTopFlavour, Top_idx, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_pt_nominal, TopMixed_phi, TopMixed_eta, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, TopResolved_pt_nominal, TopResolved_phi, TopResolved_eta, FatJet_pt_nominal, FatJet_eta, FatJet_phi, FatJet_jetId, Jet_pt_nominal, Jet_eta, Jet_phi, Jet_jetId, 1.2, 0)")

    if isMC:
        df_topvariables = df_topvariables.Define("Top_truth", "select_TopVar(EventTopFlavour, Top_idx, FatJet_matched, TopMixed_truth, TopResolved_truth)")
    # NB: TopTruth for Merged is replaced with FatJet_matched, the variable is between 0 and 3 
    # where 3 means true end less than 3 means false 

    df_topvariables = df_topvariables.Define("BestTopResolved_idx",      "(int)ArgMax(TopResolved_TopScore_nominal)")\
                                     .Define("BestTopMixed_idx",         "(int)ArgMax(TopMixed_TopScore_nominal)")\
                                     .Define("BestTopMerged_idx",        "(int)ArgMax(TopMerged_TopScore_nominal)")

    df_topvariables = df_topvariables.Define("BestTopResolved_pt",       "TopResolved_pt_nominal[BestTopResolved_idx]")\
                                     .Define("BestTopResolved_eta",      "TopResolved_eta[BestTopResolved_idx]")\
                                     .Define("BestTopResolved_phi",      "TopResolved_phi[BestTopResolved_idx]")\
                                     .Define("BestTopResolved_mass",     "TopResolved_mass_nominal[BestTopResolved_idx]")\
                                     .Define("BestTopResolved_score",    "TopResolved_TopScore_nominal[BestTopResolved_idx]")\
                                     .Define("BestTopMixed_pt",          "TopMixed_pt_nominal[BestTopMixed_idx]")\
                                     .Define("BestTopMixed_eta",         "TopMixed_eta[BestTopMixed_idx]")\
                                     .Define("BestTopMixed_phi",         "TopMixed_phi[BestTopMixed_idx]")\
                                     .Define("BestTopMixed_mass",        "TopMixed_mass_nominal[BestTopMixed_idx]")\
                                     .Define("BestTopMixed_score",       "TopMixed_TopScore_nominal[BestTopMixed_idx]")\
                                     .Define("BestTopMerged_pt",         "FatJet_pt_nominal[BestTopMerged_idx]")\
                                     .Define("BestTopMerged_eta",        "FatJet_eta[BestTopMerged_idx]")\
                                     .Define("BestTopMerged_phi",        "FatJet_phi[BestTopMerged_idx]")\
                                     .Define("BestTopMerged_mass",       "FatJet_mass_nominal[BestTopMerged_idx]")\
                                     .Define("BestTopMerged_score",      "TopMerged_TopScore_nominal[BestTopMerged_idx]")
    return df_topvariables
    
def add_TrotaScaleFactors(df, sampleflag, sample_process, TopSF_CorrLibFilePath):
    # 1. truth:                     if the candidate is matched to a GenTop with dR<0.2
    # 2. top_process_category:      0: topmatched, 1: nonmatched, 2: other
    # The event weight uses the selected top (Top_idx) of the categories 1-9 (EventTopFlavour 1/2/3).
    # GetTrotaSF picks the L or T SF from the score: there is no XT SF, so the XT tops (categories 1-3) get the T SF.

    if sampleflag:
        df_toptruth_with_matching       = df.Define("TopResolved_isMatched_to_GenTop_dR0p2",                "TopMatched_to_GenTop_with_dR(TopGenTopPart_eta, TopGenTopPart_phi, TopResolved_eta, TopResolved_phi, 0.2)")\
                                            .Define("TopMixed_isMatched_to_GenTop_dR0p2",                   "TopMatched_to_GenTop_with_dR(TopGenTopPart_eta, TopGenTopPart_phi, TopMixed_eta, TopMixed_phi, 0.2)")\
                                            .Define("TopMerged_isMatched_to_GenTop_dR0p2",                  "TopMatched_to_GenTop_with_dR(TopGenTopPart_eta, TopGenTopPart_phi, FatJet_eta, FatJet_phi, 0.2)")\
                                            .Define("BestTopResolved_isMatched_to_GenTop_dR0p2",            "TopResolved_isMatched_to_GenTop_dR0p2[BestTopResolved_idx]")\
                                            .Define("BestTopMixed_isMatched_to_GenTop_dR0p2",               "TopMixed_isMatched_to_GenTop_dR0p2[BestTopMixed_idx]")\
                                            .Define("BestTopMerged_isMatched_to_GenTop_dR0p2",              "TopMerged_isMatched_to_GenTop_dR0p2[BestTopMerged_idx]")

        df_top_process_category         = df_toptruth_with_matching.Define("TopResolved_process",           f'top_process_category("{sample_process}", TopResolved_isMatched_to_GenTop_dR0p2)')\
                                                                   .Define("TopMixed_process",              f'top_process_category("{sample_process}", TopMixed_isMatched_to_GenTop_dR0p2)')\
                                                                   .Define("TopMerged_process",             f'top_process_category("{sample_process}", TopMerged_isMatched_to_GenTop_dR0p2)')\
                                                                   .Define("BestTopResolved_process",       "TopResolved_process[BestTopResolved_idx]")\
                                                                   .Define("BestTopMixed_process",          "TopMixed_process[BestTopMixed_idx]")\
                                                                   .Define("BestTopMerged_process",         "TopMerged_process[BestTopMerged_idx]")

        df_IndependentTopCandidates     = df_top_process_category.Define("TopResolved_Independent_idx",     "select_TopRes(TopResolved_TopScore_nominal, TopResolved_idxJet0, TopResolved_idxJet1, TopResolved_idxJet2, GoodJet_idx, -1.0)")\
                                                                 .Define("TopMixed_Independent_idx",        "select_TopMix(TopMixed_TopScore_nominal, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, GoodJet_idx, GoodFatJet_idx, -1.0)")\
                                                                 .Define("TopMerged_Independent_idx",       "select_TopMer(TopMerged_TopScore_nominal, GoodFatJet_idx, -1.0)")
        
        df_NonOverlappingTopCandidates  = df_IndependentTopCandidates.Define("TopMixed_NonOverlappingTo_TopMerged_idx",                 "TopCandidates_NonOverlapping_AcrossTopCategories_idx(TopMerged_Independent_idx, FatJet_eta, FatJet_phi, TopMixed_Independent_idx, TopMixed_eta, TopMixed_phi, 1.2)")\
                                                                     .Define("TopResolved_NonOverlappingTo_TopMerged_idx",              "TopCandidates_NonOverlapping_AcrossTopCategories_idx(TopMerged_Independent_idx, FatJet_eta, FatJet_phi, TopResolved_Independent_idx, TopResolved_eta, TopResolved_phi, 1.2)")\
                                                                     .Define("TopResolved_NonOverlappingTo_TopMergedOrTopMixed_idx",    "TopCandidates_NonOverlapping_AcrossTopCategories_idx(TopMixed_NonOverlappingTo_TopMerged_idx, TopMixed_eta, TopMixed_phi, TopResolved_NonOverlappingTo_TopMerged_idx, TopResolved_eta, TopResolved_phi, 1.2)")\
                                                                     .Define("TopMerged_forEvWeight_idx",                               "(EventTopFlavour == 3) ? RVec<int>{ (int) Top_idx}: ROOT::VecOps::RVec<int>()")\
                                                                     .Define("TopMixed_forEvWeight_idx",                                "(EventTopFlavour == 2) ? RVec<int>{ (int) Top_idx}: ROOT::VecOps::RVec<int>()")\
                                                                     .Define("TopResolved_forEvWeight_idx",                             "(EventTopFlavour == 1) ? RVec<int>{ (int) Top_idx}: ROOT::VecOps::RVec<int>()")\
                                                                     .Define("nTopMerged_forEvWeight",                                  "static_cast<int>(TopMerged_forEvWeight_idx.size());")\
                                                                     .Define("nTopMixed_forEvWeight",                                   "static_cast<int>(TopMixed_forEvWeight_idx.size());")\
                                                                     .Define("nTopResolved_forEvWeight",                                "static_cast<int>(TopResolved_forEvWeight_idx.size());")
                                                                    #  .Define("TopMerged_forEvWeight_idx",                               "TopMerged_Independent_idx")\
                                                                    #  .Define("TopMixed_forEvWeight_idx",                                "TopMixed_NonOverlappingTo_TopMerged_idx")\
                                                                    #  .Define("TopResolved_forEvWeight_idx",                             "TopResolved_NonOverlappingTo_TopMergedOrTopMixed_idx")\
        
        df_TrotaScaleFactors            = df_NonOverlappingTopCandidates.Define("TopMerged_TrotaSF",                                    f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Merged"}", TopMerged_process, TopMerged_TopScore_nominal, {Top_Merged_wp["10%"]}, {Top_Merged_wp["5%"]}, FatJet_pt_nominal, "{"nominal"}")')\
                                                                        .Define("TopMerged_TrotaSFUp",                                  f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Merged"}", TopMerged_process, TopMerged_TopScore_nominal, {Top_Merged_wp["10%"]}, {Top_Merged_wp["5%"]}, FatJet_pt_nominal, "{"up"}")')\
                                                                        .Define("TopMerged_TrotaSFDown",                                f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Merged"}", TopMerged_process, TopMerged_TopScore_nominal, {Top_Merged_wp["10%"]}, {Top_Merged_wp["5%"]}, FatJet_pt_nominal, "{"down"}")')\
                                                                        .Define("TopMixed_TrotaSF",                                     f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Mixed"}", TopMixed_process, TopMixed_TopScore_nominal, {Top_Mixed_wp["10%"]}, {Top_Mixed_wp["5%"]}, TopMixed_pt_nominal, "{"nominal"}")')\
                                                                        .Define("TopMixed_TrotaSFUp",                                   f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Mixed"}", TopMixed_process, TopMixed_TopScore_nominal, {Top_Mixed_wp["10%"]}, {Top_Mixed_wp["5%"]}, TopMixed_pt_nominal, "{"up"}")')\
                                                                        .Define("TopMixed_TrotaSFDown",                                 f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Mixed"}", TopMixed_process, TopMixed_TopScore_nominal, {Top_Mixed_wp["10%"]}, {Top_Mixed_wp["5%"]}, TopMixed_pt_nominal, "{"down"}")')\
                                                                        .Define("TopResolved_TrotaSF",                                  f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Resolved"}", TopResolved_process, TopResolved_TopScore_nominal, {Top_Resolved_wp["10%"]}, {Top_Resolved_wp["5%"]}, TopResolved_pt_nominal, "{"nominal"}")')\
                                                                        .Define("TopResolved_TrotaSFUp",                                f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Resolved"}", TopResolved_process, TopResolved_TopScore_nominal, {Top_Resolved_wp["10%"]}, {Top_Resolved_wp["5%"]}, TopResolved_pt_nominal, "{"up"}")')\
                                                                        .Define("TopResolved_TrotaSFDown",                              f'GetTrotaSF("{TopSF_CorrLibFilePath}", "{"Resolved"}", TopResolved_process, TopResolved_TopScore_nominal, {Top_Resolved_wp["10%"]}, {Top_Resolved_wp["5%"]}, TopResolved_pt_nominal, "{"down"}")')\

    
        df_TrotaScaleFactors            = df_TrotaScaleFactors.Define("MergedTrotaEventWeight",                                         "CalculateCategoryTrotaEventWeight(TopMerged_TrotaSF, TopMerged_forEvWeight_idx)")\
                                                              .Define("MergedTrotaEventWeightUp",                                       "CalculateCategoryTrotaEventWeight(TopMerged_TrotaSFUp, TopMerged_forEvWeight_idx)")\
                                                              .Define("MergedTrotaEventWeightDown",                                     "CalculateCategoryTrotaEventWeight(TopMerged_TrotaSFDown, TopMerged_forEvWeight_idx)")\
                                                              .Define("MixedTrotaEventWeight",                                          "CalculateCategoryTrotaEventWeight(TopMixed_TrotaSF, TopMixed_forEvWeight_idx)")\
                                                              .Define("MixedTrotaEventWeightUp",                                        "CalculateCategoryTrotaEventWeight(TopMixed_TrotaSFUp, TopMixed_forEvWeight_idx)")\
                                                              .Define("MixedTrotaEventWeightDown",                                      "CalculateCategoryTrotaEventWeight(TopMixed_TrotaSFDown, TopMixed_forEvWeight_idx)")\
                                                              .Define("ResolvedTrotaEventWeight",                                       "CalculateCategoryTrotaEventWeight(TopResolved_TrotaSF, TopResolved_forEvWeight_idx)")\
                                                              .Define("ResolvedTrotaEventWeightUp",                                     "CalculateCategoryTrotaEventWeight(TopResolved_TrotaSFUp, TopResolved_forEvWeight_idx)")\
                                                              .Define("ResolvedTrotaEventWeightDown",                                   "CalculateCategoryTrotaEventWeight(TopResolved_TrotaSFDown, TopResolved_forEvWeight_idx)")

    else:
        df_TrotaScaleFactors            = df.Define("BestTopResolved_isMatched_to_GenTop_dR0p2",            "1.")\
                                            .Define("BestTopMixed_isMatched_to_GenTop_dR0p2",               "1.")\
                                            .Define("BestTopMerged_isMatched_to_GenTop_dR0p2",              "1.")\
                                            .Define("BestTopResolved_process",                              "1.")\
                                            .Define("BestTopMixed_process",                                 "1.")\
                                            .Define("BestTopMerged_process",                                "1.")

    return df_TrotaScaleFactors

def add_BTagFixedWPScaleFactor(df, era, sample_process):
    # b-tag event weight with fixed WPs L/M/T (BTV multi-WP method), MC efficiency maps from BTagEfficiency/
    # only b jets are reweighted (c and light jets keep factor 1, see GetBTagEventWeight_FixedWP)
    # each background uses its own map; the inclusive maps in the json are not used
    eff_names           = [c["name"] for c in json.load(open(BTagEff_CorrLibFilePath_dict[era]))["corrections"]]
    if f"UParTAK4_efficiency_{sample_process}" in eff_names:
        eff_name        = f"UParTAK4_efficiency_{sample_process}"
    else:
        eff_name        = "UParTAK4_efficiency_TT"                          # no map for this process (e.g. TprimeToTZ): closest topology, top + real b jets
    print("b-tag efficiency map: ", eff_name)
    return df.Define("SFbtag_nominal", f'GetBTagEventWeight_FixedWP("{BTV_CorrLibFilePath_dict[era]}", "{BTagEff_CorrLibFilePath_dict[era]}", "{eff_name}", GoodJet_idx, Jet_pt_nominal, Jet_eta, RVec<int>(Jet_hadronFlavour), Jet_btagUParTAK4B, btagUParTAK4B_looseWP_2024, btagUParTAK4B_mediumWP_2024, btagUParTAK4B_tightWP_2024)')

def defineWeights(df, sampleflag, sample_process):
    if sampleflag:
        df = df.Define("pdf_total_weights", "PdfWeight_variations(LHEPdfWeight, "+ str(ntot_events[d.label][s.label]) +")")\
            .Define("pdf_totalSF", "pdf_total_weights[0]")\
            .Define("pdf_totalUp", "pdf_total_weights[1]")\
            .Define("pdf_totalDown", "pdf_total_weights[2]")\
            .Define("QCDScale_weights", "QCDScale_variations(LHEScaleWeight)")\
            .Define("QCDScaleSF", "QCDScale_weights[0]")\
            .Define("QCDScaleUp", "QCDScale_weights[1]")\
            .Define("QCDScaleDown", "QCDScale_weights[2]")\
            .Define("ISRSF", "1.f")\
            .Define("FSRSF", "1.f")\
            .Define("PSWeight_weights", "PSWeight_variations(PSWeight)")\
            .Define("ISRUp", "PSWeight_weights[1]")\
            .Define("ISRDown", "PSWeight_weights[0]")\
            .Define("FSRUp", "PSWeight_weights[3]")\
            .Define("FSRDown", "PSWeight_weights[2]")
        
        if "ZJets" in sample_process: 
            df = df.Define("NLOEW", "nloewcorrectionZ(1., GenPart_pdgId, GenPart_pt, GenPart_statusFlags)")
        elif "WJets" in sample_process:
            df = df.Define("NLOEW", "nloewcorrectionW(1., GenPart_pdgId, GenPart_pt, GenPart_statusFlags)")
        else:
            df = df.Define("NLOEW", "1.0f")

    else: 
        df = df
    return df

def energetic_variations(df):
    #  Da aggiungere variazione dei fatjet
    df_sys = df.Vary(["Jet_pt_nominal", "Jet_mass_nominal", "FatJet_pt_nominal", "FatJet_mass_nominal", "PuppiMET_T1_pt_nominal_vec", "PuppiMET_T1_phi_nominal_vec", "TopMixed_pt_nominal", "TopResolved_pt_nominal", "TopMixed_mass_nominal", "TopResolved_mass_nominal",  "TopMixed_TopScore_nominal", "TopResolved_TopScore_nominal"], "RVec<RVec<RVec<float>>>{{Jet_pt_jerdown, Jet_pt_jerup}, {Jet_mass_jerdown, Jet_mass_jerup}, {FatJet_pt_jerdown, FatJet_pt_jerup}, {FatJet_mass_jerdown, FatJet_mass_jerup}, {PuppiMET_T1_pt_jerdown_vec, PuppiMET_T1_pt_jerup_vec}, {PuppiMET_T1_phi_jerdown_vec, PuppiMET_T1_phi_jerup_vec}, {TopMixed_pt_jerdown, TopMixed_pt_jerup}, {TopResolved_pt_jerdown, TopResolved_pt_jerup}, {TopMixed_mass_jerdown, TopMixed_mass_jerup}, {TopResolved_mass_jerdown, TopResolved_mass_jerup}, {TopMixed_TopScore_jerdown, TopMixed_TopScore_jerup}, {TopResolved_TopScore_jerdown, TopResolved_TopScore_jerup}}", variationTags=["down", "up"], variationName="jer")\
               .Vary(["Jet_pt_nominal", "Jet_mass_nominal", "FatJet_pt_nominal", "FatJet_mass_nominal", "PuppiMET_T1_pt_nominal_vec", "PuppiMET_T1_phi_nominal_vec", "TopMixed_pt_nominal", "TopResolved_pt_nominal", "TopMixed_mass_nominal", "TopResolved_mass_nominal",  "TopMixed_TopScore_nominal", "TopResolved_TopScore_nominal"], "RVec<RVec<RVec<float>>>{{Jet_pt_jesTotaldown, Jet_pt_jesTotalup}, {Jet_mass_jesTotaldown, Jet_mass_jesTotalup}, {FatJet_pt_jesTotaldown, FatJet_pt_jesTotalup}, {FatJet_mass_jesTotaldown, FatJet_mass_jesTotalup}, {PuppiMET_T1_pt_jesTotaldown_vec, PuppiMET_T1_pt_jesTotalup_vec}, {PuppiMET_T1_phi_jesTotaldown_vec, PuppiMET_T1_phi_jesTotalup_vec}, {TopMixed_pt_jesTotaldown, TopMixed_pt_jesTotalup}, {TopResolved_pt_jesTotaldown, TopResolved_pt_jesTotalup}, {TopMixed_mass_jesTotaldown, TopMixed_mass_jesTotalup}, {TopResolved_mass_jesTotaldown, TopResolved_mass_jesTotalup}, {TopMixed_TopScore_jesTotaldown, TopMixed_TopScore_jesTotalup}, {TopResolved_TopScore_jesTotaldown, TopResolved_TopScore_jesTotalup}}", variationTags=["down", "up"], variationName="jesTotal")
    return df_sys

def SF_variations(df):
    df_sys = df.Vary("puWeight", "RVec<float>{puWeightDown, puWeightUp}", variationTags=["down", "up"], variationName="pu")\
               .Vary("pdf_totalSF", "RVec<float>{pdf_totalDown, pdf_totalUp}", variationTags=["down", "up"], variationName="pdf_total")\
               .Vary("QCDScaleSF", "RVec<float>{QCDScaleDown, QCDScaleUp}", variationTags=["down", "up"], variationName="QCDScale")\
               .Vary("ISRSF", "RVec<float>{ISRDown, ISRUp}", variationTags=["down", "up"], variationName="ISR")\
               .Vary("FSRSF", "RVec<float>{FSRDown, FSRUp}", variationTags=["down", "up"], variationName="FSR")\
               .Vary("triggerSF", "RVec<float>{triggerSFDown, triggerSFUp}", variationTags=["down", "up"], variationName="triggerSF")
    return df_sys





t0 = datetime.now()
print("starting loop on datasets: ", [d.label for d in datasets])
print("Local time :", t0)
# print("requirements: "+cut)

# h[weightset][dataset][sample][region][variable]
h                           = {label: {} for label, removed in weightsets}
h_2D                        = {label: {} for label, removed in weightsets}
if do_variations:
    h_varied                = {label: {} for label, removed in weightsets}

for d in datasets:

    s_list                  = []
    if hasattr(d, "components"):
        s_list              = d.components
    else:
        s_list              = [d]
    if 'Data' in d.label:
        isMC                = False
        sampleflag          = 0
    else:
        isMC                = True
        sampleflag          = 1
    c_                      = cut
    for label, removed in weightsets:
        h[label][d.label]               = {}
        h_2D[label][d.label]            = {}
        if do_variations:
            h_varied[label][d.label]    = {}
    for s in s_list:
        # remove only this job's own output (not the merged plots/<label>.root when running a part)
        # with --snapshot no histograms are written: the existing ones are left untouched
        for label, removed in weightsets:
            if do_histos and os.path.exists(outfile_dict[label][s.label]):
                os.remove(outfile_dict[label][s.label])
        print("Processing dataset: ", s.label)
        sample_process      = s.process.split("_")[0] if hasattr(s, "process") else s.label.split("_")[0]
        #------------------------------------------------------------------------------
        ############# Fixing variables for 2018-2022-2023 #############################
        #------------------------------------------------------------------------------
        if s.year == 2018:
            bTagAlg = "Jet_btagDeepB"
        elif s.year in [2022,2023]:
            bTagAlg = "Jet_btagPNetB"
        elif s.year in [2024]:
            bTagAlg = "Jet_btagUParTAK4B"
        
        if hasattr(s,"EE"):
            EE = s.EE
        else:
            EE = 0
        era         = ""
        if s.year == 2018:
            era     = "2018"
        elif s.year == 2022:
            era     = "2022"
            if s.EE==1:
                era = "2022EE"
        elif s.year == 2023:
            era     = "2023"
            if s.EE==1:
                era = "2023postBPix"
        elif s.year == 2024:
            era     = "2024"

        Top_Resolved_wp = TopTagging_WorkingPoints[era]["Resolved"]
        Top_Mixed_wp    = TopTagging_WorkingPoints[era]["Mixed"]
        Top_Merged_wp   = TopTagging_WorkingPoints[era]["Merged"]

        if sampleflag and useTrotaSF and TopSF_CorrLibFilePath_dict[era] == "":
            print(f"ERROR: no Trota SF for {era}, remove them with --noTrotaSF (or noTrotaSF in every --weightset)")
            sys.exit(1)

        #-------------------------------------------------------------------------
        #########################  DF initialization #############################
        #-------------------------------------------------------------------------
        
        print("Initializing DataFrame for "+ s.label +" chain len = ", len(chain[d.label][s.label]))
        if len(chain[d.label][s.label])==1:
            print(chain[d.label][s.label])
        # df                  = ROOT.RDataFrame("Events", chain[d.label][s.label])
        df                  = ROOT.RDataFrame(tchains[d.label][s.label])
        # Step-1 top candidates store POSITIONS in the step-1 good jet/fatjet lists (tools.get_jet/get_fatjet): converted to Jet/FatJet indices
        # (before the Redefine of Jet_jetId for 2022/2023: the step-1 lists use the NanoAOD jetId)
        df                  = df.Define("StepOneGoodJet_idx",        "StepOne_GoodJet_idx(Jet_pt, Jet_eta, RVec<int>(Jet_jetId))")\
                                .Define("StepOneGoodFatJet_idx",     "StepOne_GoodFatJet_idx(FatJet_pt, FatJet_eta, RVec<int>(FatJet_jetId))")\
                                .Redefine("TopResolved_idxJet0",     "StepOneIdx_to_CollectionIdx(TopResolved_idxJet0, StepOneGoodJet_idx)")\
                                .Redefine("TopResolved_idxJet1",     "StepOneIdx_to_CollectionIdx(TopResolved_idxJet1, StepOneGoodJet_idx)")\
                                .Redefine("TopResolved_idxJet2",     "StepOneIdx_to_CollectionIdx(TopResolved_idxJet2, StepOneGoodJet_idx)")\
                                .Redefine("TopMixed_idxJet0",        "StepOneIdx_to_CollectionIdx(TopMixed_idxJet0, StepOneGoodJet_idx)")\
                                .Redefine("TopMixed_idxJet1",        "StepOneIdx_to_CollectionIdx(TopMixed_idxJet1, StepOneGoodJet_idx)")\
                                .Redefine("TopMixed_idxJet2",        "StepOneIdx_to_CollectionIdx(TopMixed_idxJet2, StepOneGoodJet_idx)")\
                                .Redefine("TopMixed_idxFatJet",      "StepOneIdx_to_CollectionIdx(TopMixed_idxFatJet, StepOneGoodFatJet_idx)")
        if sampleflag:
            df              = df.Define("triggerSF",        f'GetTriggerSF(PuppiMET_T1_pt_nominal, "{era}", "sf")')\
                                .Define("triggerSFUp",      f'GetTriggerSF(PuppiMET_T1_pt_nominal, "{era}", "up")')\
                                .Define("triggerSFDown",    f'GetTriggerSF(PuppiMET_T1_pt_nominal, "{era}", "down")')     # up/down = sf +/- |1-sf| (TriggerSF/CreateCorrLibFile.py)
        df                  = df.Define("PuppiMET_T1_pt_nominal_vec", "RVec<float>{ (float) PuppiMET_T1_pt_nominal}").Define("PuppiMET_T1_phi_nominal_vec", "RVec<float>{ (float) PuppiMET_T1_phi_nominal}")
        df                  = defineWeights(df, sampleflag, sample_process)

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

        if isMC:
            df_hlt          = GenTopLep(df_hlt)
        else:
            df_hlt          = df_hlt

        if sampleflag:
            if "TT" in s.label:                                                                                                                     # topPt reweighting for TT only, for the other samples w_topPt is defined as 1
                if "hadr" in s.label:
                    df_hlt = df_hlt.Define("w_topPt", "topPtReweighting(TopGenTopPart_pt[0], TopGenTopPart_pt[1])")
                elif "semilep" in s.label:
                    df_hlt = df_hlt.Define("w_topPt", "topPtReweighting(TopGenTopPart_pt[0], TopGenLep_pt[0])")
                elif "dilep" in s.label:
                    df_hlt = df_hlt.Define("w_topPt", "topPtReweighting(TopGenLep_pt[0], TopGenLep_pt[1])")
            else:
                df_hlt = df_hlt.Define("w_topPt", "1.0")

        df_presel           = preselection(df_hlt, bTagAlg, s.year, EE)
        if sampleflag and s.year in [2024]:
            df_presel       = add_BTagFixedWPScaleFactor(df_presel, era, sample_process)
        df_topsel           = select_top(df_presel, sampleflag, s.year)
        df_topsel           = df_topsel.Define("MT_T", "sqrt(2 * Top_pt * PuppiMET_T1_pt_nominal * (1 - cos(Top_phi - PuppiMET_T1_phi_nominal)))")
        df_TrotaSF          = add_TrotaScaleFactors(df_topsel, sampleflag, sample_process, TopSF_CorrLibFilePath_dict[era])
        if do_variations and useTrotaSF:
            # df_TrotaSF      = df_TrotaSF.Vary("TotalTrotaEventWeight", "RVec<float>{TotalTrotaEventWeightDown, TotalTrotaEventWeightUp}", variationTags=["down", "up"], variationName="Trota")
            df_TrotaSF      = df_TrotaSF.Vary("ResolvedTrotaEventWeight",   "RVec<float>{ResolvedTrotaEventWeightDown, ResolvedTrotaEventWeightUp}",    variationTags=["down", "up"], variationName="TrotaResolved")\
                                        .Vary("MixedTrotaEventWeight",      "RVec<float>{MixedTrotaEventWeightDown, MixedTrotaEventWeightUp}",          variationTags=["down", "up"], variationName="TrotaMixed")\
                                        .Vary("MergedTrotaEventWeight",     "RVec<float>{MergedTrotaEventWeightDown, MergedTrotaEventWeightUp}",        variationTags=["down", "up"], variationName="TrotaMerged")
        else:
            df_TrotaSF      = df_TrotaSF

        if sampleflag:
            df_TrotaSF      = df_TrotaSF.Define("TotalTrotaEventWeight",        "MergedTrotaEventWeight * MixedTrotaEventWeight * ResolvedTrotaEventWeight")
                                    #   .Define("TotalTrotaEventWeightUp",        "MergedTrotaEventWeightUp * MixedTrotaEventWeightUp * ResolvedTrotaEventWeightUp")\
                                    #   .Define("TotalTrotaEventWeightDown",      "MergedTrotaEventWeightDown * MixedTrotaEventWeightDown * ResolvedTrotaEventWeightDown")

        ########################## Weights application ##########################
        # one weight column w_<weightset> per weightset, without the weights removed in that weightset
        df_wnom             = df_TrotaSF
        if sampleflag:
            weights_list    = ["NLOEW", "triggerSF", "(LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP))", "pdf_totalSF", "QCDScaleSF", "ISRSF", "FSRSF"]
            weights_list   += list(REMOVABLE_WEIGHTS.values())                  # SFbtag_nominal, puWeight, w_topPt, TotalTrotaEventWeight
            for label, removed in weightsets:
                removed_columns = [REMOVABLE_WEIGHTS[n] for n in removed]
                weights_expr    = "*".join([w for w in weights_list if w not in removed_columns])
                print(f"weights expression {label}: ", weights_expr)
                df_wnom         = df_wnom.Define("w_"+label,    f"{weights_expr}")
        else:
            for label, removed in weightsets:
                df_wnom         = df_wnom.Define("w_"+label,    "1.0f")


        # command for printing the cutflow, add it in the SRs for all the bkgs 
        # if printcutflow:
        #     df_wnom.Report().Print()

        if do_snapshot:
            opts        = ROOT.RDF.RSnapshotOptions()
            opts.fLazy  = True
            columns     = [c for c in branches + ["w_"+label for label, removed in weightsets] if df_wnom.HasColumn(c)]
            print("snapshot columns: ", columns)
            snapshot_dfs.append(df_wnom.Snapshot("events_nominal", snapshot_folder+"snap_"+s.label+".root", columns, opts))
        if do_histos:
            s_cut = cut_string(cut)
            for label, removed in weightsets:
                if len(var) != 0 :
                    # the cutflow is the same for every weightset: printed only once
                    h[label][d.label][s.label] = bookhisto(df_wnom, regions_def, var, s_cut, "w_"+label, sampleflag, printcutflow and label == weightsets[0][0])
                if len(var2d) != 0:
                    h_2D[label][d.label][s.label] = bookhisto2D(df_wnom, regions_def, var2d, "w_"+label)

        
        if do_variations:
            # h_varied[weightset][dataset][sample][region][variable]
            print("applying vary")
            for label, removed in weightsets:
                h_varied[label][d.label][s.label]={}
                for reg in regions_def.keys():
                    h_varied[label][d.label][s.label][reg] = {}
                    for v in var:
                        if "SFbtag" in v._name:
                            continue
                        h_varied[label][d.label][s.label][reg][v._name] = ROOT.RDF.Experimental.VariationsFor(h[label][d.label][s.label][reg][v._name])

if do_histos:
    print("All histos booked!")
    for d in datasets:
        for label, removed in weightsets:
            if len(var):
                if do_variations:
                    savehisto(d, h_varied[label], regions_def, var, s_cut, outfile_dict[label], variations, do_variations, ntot_events)
                else:
                    savehisto(d, h[label], regions_def, var, s_cut, outfile_dict[label], variations, do_variations, ntot_events)
            if len(var2d) != 0 :
                savehisto2d(d, h_2D[label], regions_def, var2d, repohisto[label], ntot_events)
            print(d.label + " histos saved, weightset " + label)
if do_snapshot:
    for snapshot_df in snapshot_dfs:
        snapshot_df.GetValue()
    print("Snapshots done!")
t1 = datetime.now()
print("Job finished in: ", t1-t0)
