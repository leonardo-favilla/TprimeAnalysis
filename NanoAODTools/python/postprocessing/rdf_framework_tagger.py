import ROOT
import os
from samples.samples import *
from variables import *
import pickle as pkl
from datetime import datetime
import json

debug = True

def voms():
    username = str(os.environ.get('USER'))
    inituser = str(os.environ.get('USER')[0])
    if username == 'adeiorio':
        uid = 103214
    elif username == 'acagnott':
        uid = 140541
    if not os.path.exists("/tmp/x509up_u" + str(uid)):
        os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
    return "proxy = /tmp/x509up_u" + str(uid)

def my_initialization_function(data):
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(data))
    print("end of initialization")

########### functions definition
def trigger(df):
    return df.Filter("") # Add triggers

def goodObjects(df):
    df_tmp = df.Define("GoodMu_idx", "GetGoodMuon( Muon_pt,  Muon_eta,  Muon_looseId,  Muon_dxy)")\
               .Define("GoodEl_idx", "GetGoodElectron( Electron_pt,  Electron_eta,  Electron_mvaFall17V2noIso_WPL,  Electron_dxy)")\
               .Define("GoodJet_idx", "GetGoodJet(Jet_pt, Jet_jetId)")\
               .Define("JetBTag_idx", "GetJetBTag(GoodJet_idx, Jet_btagDeepB)")
    return df_tmp


def LeptonTopTag(df):
    df_ = df.Filter("atLeast1GoodLep(GoodMu_idx, GoodEl_idx)")
    
    # ("LeptonTopSelection(rvec_i JetBTag, rvec_f Jet_pt, rvec_f Jet_eta, rvec_f Jet_phi, rvec_f Jet_mass,\
    #                          rvec_i GoodMu, rvec_i Muon_pt, rvec_f Muon_eta, rvec_f Muont_phi, rvec_f Muont_mass,\
    #                          rvec_i GoodEl, rvec_i Electron_pt, rvec_f Electron_eta, rvec_f Electron_phi, rvec_f Electron_mass)", "LeptonTopTagger")
    
    return df_

############### top selection ########################

# forse sono da selezionare solo i mix 

def SelectTopHadr(df):
    df_goodtopMer = df.Define("GoodTopMer_idx", "select_TopMer(FatJet_deepTag_TvsQCD, FatJet_pt, FatJet_eta, FatJet_phi)") 
    # ritorna gli indici dei FatJet che superano la trs del Top Merged (no overlap)
    df_goodtopMix = df_goodtopMer.Define("GoodTopMix_idx", "select_TopMix(TopHighPt_score2, TopHighPt_pt, TopHighPt_eta, TopHighPt_phi)")
    # ritorna gli indici dei FatJet che superano la trs del Top Merged (no overlap)
    df_goodtopRes = df_goodtopMix.Define("GoodTopRes_idx", "select_TopRes(TopLowPt_scoreDNN, TopLowPt_pt, TopLowPt_eta, TopLowPt_phi)")
    # ritorna gli indici dei Fatche superano la trs del Top Merged (no overlap)
    df_topcategory = df_goodtopRes.Define("EventTopCategory", "select_TopCategory(GoodTopMer_idx, GoodTopMix_idx, GoodTopRes_idx)")
    # return:  0- no top sel, 1- top merged, 2- top mix, 3- top resolved
    df_topselected = df_topcategory.Define("Top_idx",
                                           "select_bestTop(EventTopCategory, GoodTopMer_idx, GoodTopMix_idx, GoodTopRes_idx, FatJet_deepTag_TvsQCD, TopHighPt_score2, TopLowPt_scoreDNN)")
    # return best top idx wrt category --> the idx is referred to the list of candidates fixed by the EventTopCategory
    df_topvariables = df_topselected.Define("Top_pt", "select_TopVar(EventTopCategory, Top_idx, FatJet_pt, TopHighPt_pt, TopLowPt_pt)")\
                        .Define("Top_eta", "select_TopVar(EventTopCategory, Top_idx, FatJet_eta, TopHighPt_eta, TopLowPt_eta)")\
                        .Define("Top_phi", "select_TopVar(EventTopCategory, Top_idx, FatJet_phi, TopHighPt_phi, TopLowPt_phi)")\
                        .Define("Top_mass", "select_TopVar(EventTopCategory, Top_idx, FatJet_mass, TopHighPt_mass, TopLowPt_mass)")\
                        .Define("Top_score", "select_TopVar(EventTopCategory, Top_idx, FatJet_deepTag_TvsQCD, TopHighPt_score2, TopLowPt_scoreDNN)")

    return df_topvariables

voms()

## Inputs Parameters
datasets = [
    #### BKGs
    'QCD_2018', 
    'TT_2018',
    'ZJets_2018',
    'WJets_2018',
    #### SIGNALS
    'TprimeToTZ_700_2018',
    'TprimeToTZ_1000_2018',
    'TprimeToTZ_1800_2018',
    #### DATA
    # 'DataHT_2018',
    ]

with open('./samples/stringSample.json', 'r') as f:
    stringSample = json.load(f)
with open('./samples/dictSample.json', 'r') as f:
    dictSample = json.load(f)    

## chain formatting
if all(datasets in sample_dict.keys() for datasets in datasets):
    print("All datasets are included in sample_dict.keys()")
else:
    print("At least one datasets is not included in sample_dict.keys()")
    datasets = []
    print("Check the datasets string... ", sample_dict.keys())
chain = []
for d in datasets:
    if hasattr(sample_dict[d], components):
        for s in sample_dict[d].components:
            chain.append(stringSample[s])
    else:
        chain.append(stringSample[d])

if debug: chain = ["../../crab/AA06967A-EC11-1C40-9600-91B3551483DB_Skim.root"]

## Output folder
outfolder = "/eos/home-a/acagnott/DarkMatter/nosynch/TaggerStudies/"
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
repoSnap = outfolder + "snapshots/"
if not os.path.exists(repoSnap):
    os.makedirs(repoSnap)

#### RDataFrame initialization
rdf = ROOT.RDataFrame
HeaderFile = open("header_tagger.h")
func = HeaderFile.read()
my_initialization_function(func)

print("starting the loop over datasets ", datetime.now().strftime("%H:%M:%S"))

h = {} ### final histograms dictionary

df = rdf("Events", chain)
df = df.Define("isMC", "isMC(Sample)") # nel tree Events deve essere aggiunto il branch Sample
df = df.Define("Year", "Year(Sample)")
df = df.Define("CrossSection", "getXSec(Sample, isMC)")
df = df.Define("Nevents","getNevents(Sample, isMC)")

df_trigger = trigger(df)
df_goodobj = goodObjects(df_trigger)

df_LeptonTopTag = LeptonTopTag(df_goodobj)
df_topsel = SelectTopHadr(df_LeptonTopTag)

myvars = [#"isMC", "Year", "CrossSection", "Nevents", 
          #"Top_pt", "Top_eta", "Top_phi", "Top_mass", "Top_score",
          "MET_pt", "MET_phi"
          ]

h = df_topsel.Histo1D(("MET_pt", "MET_pt", 6, 200, 800), "MET_pt").GetValue()
f = ROOT.TFile.Open("test.root")
h.Write()
f.Close()
# opts = ROOT.RDF.RSnapshotOptions()
# opts.fLazy = False

# df_topsel.Snapshot("events_nominal", repoSnap+"TopSelection.root", )
# df_topsel.Report().Print()

# df_snap = df_topsel.Snapshot("events_nominal", "TopSelection.root", myvars, opts)
# df_snap.GetValue()

#### errore in compilazione... non capisco se è la versione di root o altro
