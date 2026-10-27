import ROOT
import sys
import os
import optparse
import json
import numpy as np
import math
from datetime import datetime
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')

# MC b-tagging efficiency maps for the fixed-WP b-tag scale factors (Run3 eras, WPs L/M/T).
# For each MC sample: 2D histograms (|eta| vs pt) of the good jets of each flavour, all jets and jets passing each WP.
# Efficiency = pass/all is computed later by CreateCorrLibFile.py, which writes the correctionlib json read by postselection/postSelector.py.
# Phase space and event weights are the ones of postselection/postSelector.py, without b-tag and Trota scale factors.

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
WorkDir  = os.environ["PWD"]

usage                   = 'python3 postSelector.py -d <datasets> --dict_samples_file <dict_samples_file> --hist_folder <hist_folder> --nfiles_max <nfiles_max>'
parser                  = optparse.OptionParser(usage)
parser.add_option('-d', '--datasets',           dest='datasets',            type=str,               default="TT_2024",                              help='Datasets to process, in the form: TT_2024,QCD_2024...')
parser.add_option(      '--dict_samples_file',  dest='dict_samples_file',   type=str,               default="../samples/dict_samples_2024.json",    help='Path to the JSON file containing the sample definitions')
parser.add_option(      '--hist_folder',        dest='hist_folder',         type=str,               default="",                                     help='Folder where to save the histograms')
parser.add_option(      '--nfiles_max',         dest='nfiles_max',          type=int,               default=1,                                      help='Max number of files to process per sample')
parser.add_option(      '--tmpfold',            dest='tmpfold',             action='store_true',    default=False,                                  help='test tmp folder for out file')

(opt, args)             = parser.parse_args()
in_dataset              = opt.datasets.split(",")
nfiles_max              = opt.nfiles_max
dict_samples_file       = opt.dict_samples_file
hist_folder             = opt.hist_folder
tmpfold                 = opt.tmpfold
if hist_folder=="":
    print("Please provide a valid hist_folder name")
    sys.exit(1)
folder                  = hist_folder
repohisto               = folder+"plots/"
if not os.path.exists(repohisto):
    os.makedirs(repohisto)

############# b-tagging efficiency maps: binning as in BTV examples (lib/btag_sf.py) #############
# https://gitlab.cern.ch/cms-analysis-corrections/BTV/examples
BTagEff_abseta_bins     = [0., 1.305, 2.5]
BTagEff_pt_bins         = [20., 30., 50., 70., 100., 140., 200., 300., 600., 1000.]
flavours                = {"b": 5, "c": 4, "light": 0}                                  # Jet_hadronFlavour
wps                     = ["all", "L", "M", "T"]                                        # "all" = no WP cut

############# era-dependent b-tagging settings: discriminant and WP thresholds (defined in postselection.h) #############
bTagAlg_dict            = {2022: "Jet_btagPNetB", 2023: "Jet_btagPNetB", 2024: "Jet_btagUParTAK4B"}
btagWP_dict             = {
                            "2022":         {"L": "btagPNet_looseWP_2022",          "M": "btagPNet_mediumWP_2022",          "T": "btagPNet_tightWP_2022"},
                            "2022EE":       {"L": "btagPNet_looseWP_2022EE",        "M": "btagPNet_mediumWP_2022EE",        "T": "btagPNet_tightWP_2022EE"},
                            "2023":         {"L": "btagPNet_looseWP_2023",          "M": "btagPNet_mediumWP_2023",          "T": "btagPNet_tightWP_2023"},
                            "2023postBPix": {"L": "btagPNet_looseWP_2023postBPix",  "M": "btagPNet_mediumWP_2023postBPix",  "T": "btagPNet_tightWP_2023postBPix"},
                            "2024":         {"L": "btagUParTAK4B_looseWP_2024",     "M": "btagUParTAK4B_mediumWP_2024",     "T": "btagUParTAK4B_tightWP_2024"},
                          }

def get_era(s):
    # as in postselection/postSelector.py
    if s.year == 2022:
        return "2022EE" if getattr(s, "EE", 0) == 1 else "2022"
    if s.year == 2023:
        return "2023postBPix" if getattr(s, "EE", 0) == 1 else "2023"
    return str(s.year)

#### LOAD postselection/postselection.h ####
text_file = open(WorkDir+"/../postselection/postselection.h", "r")
data      = text_file.read()
def my_initialization_function():
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(data))
    print("end of initialization")
my_initialization_function()

#### LOAD samples ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)

datasets = []
for in_d in in_dataset:
    if not in_d in sample_dict.keys():
        print("Check the in_dataset string... ", sample_dict.keys())
    else:
        datasets.append(sample_dict[in_d])
print("Datasets to process : ", [d.label for d in datasets])

chain                       = {}
ntot_events                 = {}
tchains                     = {}
for d in datasets:
    if "Data" in d.label:
        print("b-tagging efficiencies are computed on MC only, skipping ", d.label)
        continue
    if hasattr(d, "components"):
        samples_list        = d.components
    else:
        samples_list        = [d]
    for s in samples_list:
        if get_era(s) not in btagWP_dict:
            print("b-tagging efficiencies are implemented for the eras ", list(btagWP_dict.keys()), ", got ", s.label)
            sys.exit(1)
        chain[s.label]          = samples[d.label][s.label]['strings'][:nfiles_max]
        ntot_events[s.label]    = np.sum(samples[d.label][s.label]['ntot'][:nfiles_max])    # normalization to the processed files only
        print("Sample : "+s.label)
        print("# of files to process : ", len(chain[s.label]))
        print("# of total events in the files to process : ", ntot_events[s.label])

        tchains[s.label] = ROOT.TChain("Events")
        for i, f in enumerate(chain[s.label]):
            try:
                TFile = ROOT.TFile.Open(f)
                tchains[s.label].Add(f)
            except:
                ntot_events[s.label] -= samples[d.label][s.label]['ntot'][i]
                print("Could not add file: ", f)
                continue
        print("Number of events in the TChain: ", tchains[s.label].GetEntries())

############### selection, as in postselection/postSelector.py ###############
def preselection(df, year):
    df = df.Filter("HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",  "triggerMET")
    if year in [2022,2023]:
        df = df.Define("Jet_passJetIdTight",            "Jet_passJetIdTight(Jet_eta, Jet_jetId, Jet_neHEF, Jet_neEmEF)")\
               .Define("Jet_passJetIdTightLepVeto",     "Jet_passJetIdTightLepVeto(Jet_eta, Jet_passJetIdTight, Jet_muEF, Jet_chEmEF)")\
               .Redefine("Jet_jetId",                   "ROOT::VecOps::RVec<int>(Jet_passJetIdTight) * 2 + ROOT::VecOps::RVec<int>(Jet_passJetIdTightLepVeto) * 4") # https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV
    df = df.Define("GoodJet_idx",                       "GetGoodJet(Jet_pt_nominal, Jet_eta, Jet_jetId)") # richiesto jetId==6
    df = df.Define("GoodFatJet_idx",                    "GetGoodFatJet(FatJet_pt_nominal, FatJet_eta, FatJet_jetId)") # richiesto jetId==6
    df = df.Filter("GoodJet_idx.size()>2 || GoodFatJet_idx.size()>0", "jet presel")
    df = df.Define("JetBTagScore",                      "GetJetBTagScore(GoodJet_idx, "+bTagAlg_dict[year]+")")
    return df

############### event weights: defineWeights as in postselection/postSelector.py, plus the top pT reweighting ###############
def defineWeights(df, sample_process, label, ntot):
    df = df.Define("pdf_total_weights", "PdfWeight_variations(LHEPdfWeight, "+ str(ntot) +")")\
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

    # top pT reweighting for TT only, for the other samples w_topPt is defined as 1 (as in postselection/postSelector.py)
    if "TT" in label and ("semilep" in label or "dilep" in label):
        df = df.Define("TopGenLep_pt", "TopGenLep_var(TopGenLep_genPartIdx(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_genPartIdxMother_prompt, GenPart_statusFlags), GenPart_pt)")
    if "TT" in label:
        if "hadr" in label:
            df = df.Define("w_topPt", "topPtReweighting(TopGenTopPart_pt[0], TopGenTopPart_pt[1])")
        elif "semilep" in label:
            df = df.Define("w_topPt", "topPtReweighting(TopGenTopPart_pt[0], TopGenLep_pt[0])")
        elif "dilep" in label:
            df = df.Define("w_topPt", "topPtReweighting(TopGenLep_pt[0], TopGenLep_pt[1])")
    else:
        df = df.Define("w_topPt", "1.0")
    return df

# all the analysis weights except b-tag and Trota SFs: weights_list of postselection/postSelector.py with --noSFbtag --noTrotaSF
weights_expr = "NLOEW*triggerSF*(LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP))*pdf_totalSF*QCDScaleSF*ISRSF*FSRSF*puWeight*w_topPt"

############### b-tagging efficiency histograms ###############
def define_BTagEfficiency_columns(df, era):
    # BTagEff_<flavour>_<wp>_abseta/_pt: |eta| and pt of the good jets of that flavour passing the WP ("all" = no WP cut).
    # GoodJet_* columns are aligned with GoodJet_idx, as JetBTagScore.
    df = df.Define("GoodJet_pt",                        "Take(Jet_pt_nominal, GoodJet_idx)")\
           .Define("GoodJet_abseta",                    "abs(Take(Jet_eta, GoodJet_idx))")\
           .Define("GoodJet_hadronFlavour",             "Take(Jet_hadronFlavour, GoodJet_idx)")
    for flavour, flavour_id in flavours.items():
        for wp in wps:
            selection = f"GoodJet_hadronFlavour == {flavour_id}"
            if wp != "all":
                selection += f" && JetBTagScore > {btagWP_dict[era][wp]}"
            df = df.Define(f"BTagEff_{flavour}_{wp}_abseta",    f"GoodJet_abseta[{selection}]")\
                   .Define(f"BTagEff_{flavour}_{wp}_pt",        f"GoodJet_pt[{selection}]")
    return df

def book_BTagEfficiency_histos(df):
    h_ = {}
    for flavour in flavours:
        for wp in wps:
            name    = f"BTagEff_{flavour}_{wp}"
            model   = ROOT.RDF.TH2DModel(name, " ;Jet |#eta|;Jet p_{T} [GeV]",
                                         len(BTagEff_abseta_bins)-1, np.array(BTagEff_abseta_bins, dtype="float64"),
                                         len(BTagEff_pt_bins)-1,     np.array(BTagEff_pt_bins,     dtype="float64"))
            h_[name] = df.Histo2D(model, f"{name}_abseta", f"{name}_pt", "w_nominal")
    return h_

def fold_overflow_2D(h2):
    # Move underflow/overflow of both axes into the first/last bins (pt > 1000 GeV goes in the last pt bin)
    nx, ny = h2.GetNbinsX(), h2.GetNbinsY()
    for ix in range(nx+2):
        for iy in range(ny+2):
            jx = min(max(ix, 1), nx)
            jy = min(max(iy, 1), ny)
            if (jx, jy) == (ix, iy):
                continue
            h2.SetBinContent(jx, jy, h2.GetBinContent(jx, jy) + h2.GetBinContent(ix, iy))
            h2.SetBinError(jx, jy, math.sqrt(pow(h2.GetBinError(jx, jy),2) + pow(h2.GetBinError(ix, iy),2)))
            h2.SetBinContent(ix, iy, 0.)
            h2.SetBinError(ix, iy, 0.)

def save_BTagEfficiency_histos(s, h_):
    if tmpfold:
        repohisto_tmp = "/tmp/"+username+"/"+s.label+"/"
        if not os.path.exists(repohisto_tmp):
            os.makedirs(repohisto_tmp)
        outfile = ROOT.TFile.Open(repohisto_tmp+s.label+'.root', "RECREATE")
    else:
        outfile = ROOT.TFile.Open(repohisto+s.label+'.root', "RECREATE")
    for name in h_:
        h2 = h_[name].GetValue()
        fold_overflow_2D(h2)
        h2.Scale(s.sigma*10**3/ntot_events[s.label])
        outfile.cd()
        h2.Write()
    outfile.Close()


t0 = datetime.now()
print("starting loop on datasets: ", [d.label for d in datasets])
print("Local time :", t0)

h = {}
for d in datasets:
    if "Data" in d.label:
        continue
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]
    for s in s_list:
        era             = get_era(s)
        sample_process  = s.process.split("_")[0] if hasattr(s, "process") else s.label.split("_")[0]
        print("Processing sample: ", s.label, " era: ", era, " b-tag discriminant: ", bTagAlg_dict[s.year])

        df              = ROOT.RDataFrame(tchains[s.label])
        df              = df.Define("triggerSF",    f'GetTriggerSF(PuppiMET_pt, "{era}", "sf")')
        df              = defineWeights(df, sample_process, s.label, ntot_events[s.label])
        df              = preselection(df, s.year)
        df              = df.Define("w_nominal",    weights_expr)
        df              = define_BTagEfficiency_columns(df, era)
        h[s.label]      = book_BTagEfficiency_histos(df)

print("All histos booked!")
for d in datasets:
    if "Data" in d.label:
        continue
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]
    for s in s_list:
        save_BTagEfficiency_histos(s, h[s.label])
        print(s.label + " histos saved")

t1 = datetime.now()
print("Job finished in: ", t1-t0)
