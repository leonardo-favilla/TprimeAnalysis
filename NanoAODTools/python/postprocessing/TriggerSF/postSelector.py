import ROOT
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
# from PhysicsTools.NanoAODTools.postprocessing.variables import *
sys.path.append('../')

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
WorkDir  = os.environ["PWD"]

usage                   = 'python3 postSelector.py -d <datasets> --dict_samples_file <dict_samples_file> --hist_folder <hist_folder> --nfiles_max <nfiles_max> --noSFbtag --syst'
parser                  = optparse.OptionParser(usage)
parser.add_option('-d', '--datasets',           dest='datasets',            type=str,               default="QCD_2023",                             help='Datasets to process, in the form: QCD_2023,TT_2023...')
parser.add_option(      '--dict_samples_file',  dest='dict_samples_file',   type=str,               default="../samples/dict_samples_2023.json",    help='Path to the JSON file containing the sample definitions')
parser.add_option(      '--hist_folder',        dest='hist_folder',         type=str,               default="",                                     help='Folder where to save the histograms')
parser.add_option(      '--syst',               dest='syst',                action='store_true',    default=False,                                  help='calculate jerc')
parser.add_option(      '--nfiles_max',         dest='nfiles_max',          type=int,               default=1,                                      help='Max number of files to process per sample')
parser.add_option(      '--noSFbtag',           dest='noSFbtag',            action='store_true',    default=False,                                  help='remove b tag SF')
parser.add_option(      '--tmpfold',           dest='tmpfold',            action='store_true',    default=False,                                  help='test tmp folder for out file')


(opt, args)             = parser.parse_args()
in_dataset              = opt.datasets.split(",")
nfiles_max              = opt.nfiles_max
do_variations           = opt.syst
noSFbtag                = opt.noSFbtag
dict_samples_file       = opt.dict_samples_file
hist_folder             = opt.hist_folder
tmpfold                 = opt.tmpfold
do_histos               = True
do_snapshot             = False
if do_variations:
    do_snapshot         = False
remote_subfolder_name   = datetime.now().strftime("%Y%m%d") #20231229
if hist_folder=="":
    print("Please provide a valid hist_folder name")
    sys.exit(1)
folder                  = hist_folder
repohisto               = folder+"plots/"


if not os.path.exists(folder):
    os.mkdir(folder)
repohisto = folder+"plots/"
if not os.path.exists(repohisto):
    os.mkdir(repohisto)

try:
    f = open(repohisto+"/test.txt", "w")
    f.write("This folder contains the output histograms from the postSelector step.\n")
    f.close()
    os.remove(repohisto+"/test.txt")
except:
    sys.exit(1)


hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
# hlt_mu  = "(HLT_IsoMu24 || HLT_Mu50)"
hlt_ele = "(HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200)"

regions_def = {
    "orthogonalPreselR_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR2_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR2_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron>0",
    "orthogonalPreselR_CR"       :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron==0",
}
print("Regions to book: ")
for r in regions_def.keys():
    print("  "+r)

var = []
var.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 8, xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_phi", title= "MET #phi (Puppi) [GeV]", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 12, xarray = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "MHT", title= "MHT [GeV]", nbins = 6, xarray = np.array([0, 100, 200, 300, 400, 500, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
var.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
var.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
var2d = [] 
var2d.append(variable2D(name = "PuppiMET_T1_pt_nominalVsMHT", xname = "PuppiMET_T1_pt_nominal", yname = "MHT", xtitle = " Puppi MET p_{T} [GeV]", ytitle = "MHT [GeV]", nxbins = 12, xarray = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000], dtype = 'd'),
                            nybins = 6, yarray = np.array([0, 100, 200, 300, 400, 500, 1000], dtype = 'd')))

print("Variables for histograms :")
print([v._name for v in var])

#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)


datasets = []
for in_d in in_dataset:
    if not in_d in sample_dict.keys():
        print("Check the in_dataset string... ", sample_dict.keys())
    else : 
        datasets.append(sample_dict[in_d])
print("Datasets to process : ", [d.label for d in datasets])

text_file = open(WorkDir+"../postselection/postselection.h", "r")
data = text_file.read()
def my_initialization_function():
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(data))
    print("end of initialization")
RDataFrame = ROOT.RDataFrame
my_initialization_function()

chain                       = {}
ntot_events                 = {}
tchains                     = {}
for d in datasets:
    if hasattr(d, "components"):
        samples_list        = d.components
    else:
        samples_list        = [d]
    chain[d.label]          = {}
    ntot_events[d.label]    = {}
    tchains[d.label]        = {}
    for s in samples_list:
        nfiles              = nfiles_max
        for i, string in enumerate(samples[d.label][s.label]['strings']):
            # samples[d.label][s.label]['strings'][i] = string.replace("root://cms-xrd-global.cern.ch/", "davs://stwebdav.pi.infn.it:8443/cms/") # root://stormgf2.pi.infn.it/
            samples[d.label][s.label]['strings'][i] = string.replace("root://cms-xrd-global.cern.ch/", "root://xrootd-cms.infn.it/") # root://stormgf2.pi.infn.it/
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

        #### tchain def
        tchains[d.label][s.label] = ROOT.TChain("Events")
        for i, f in enumerate(chain[d.label][s.label]):
            try:
                TFile = ROOT.TFile.Open(f)
                tchains[d.label][s.label].Add(f)
            except:
                ntot_events[d.label][s.label] -= samples[d.label][s.label]['ntot'][i]
                print("Could not add file: ", f)
                continue
        print("Number of events in the TChain: ", tchains[d.label][s.label].GetEntries())
        print("Number of total events in the TChain (MC only, if Data the number is None): ", ntot_events[d.label][s.label])

################### preselection ###############
def preselection(df, btagAlg, year, EE):
    
    df = df.Define("GoodJet_idx", "GetGoodJet(Jet_pt_nominal, Jet_eta, Jet_jetId)")
    df = df.Define("nGoodJet", "nGoodJet(GoodJet_idx)")
    df = df.Define("GoodFatJet_idx", "GetGoodJet(FatJet_pt_nominal, FatJet_eta, FatJet_jetId)")
    df = df.Define("nGoodFatJet", "GoodFatJet_idx.size()")
    df = df.Filter("nGoodJet>2 || nGoodFatJet>0 ", "jet presel")
    
    # df = df.Redefine("MaxEta_jet", "max_etajet(Jet_eta, GoodJet_idx)")
    df = df.Redefine("MinDelta_phi", "min_DeltaPhi(PuppiMET_T1_phi_nominal, Jet_phi, GoodJet_idx)")
    
    df = df.Define("nTightElectron", "nTightElectron(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("TightElectron_idx", "TightElectron_idx(Electron_pt, Electron_eta, Electron_cutBased)")
    df = df.Define("nVetoElectron", "nVetoElectron(Electron_pt, Electron_cutBased, Electron_eta)")
    df = df.Define("nTightMuon", "nTightMuon(Muon_pt, Muon_eta, Muon_tightId)")
    df = df.Define("TightMuon_idx", "TightMuon_idx(Muon_pt, Muon_eta, Muon_tightId)")
    df = df.Define("nVetoMuon", "nVetoMuon(Muon_pt, Muon_eta, Muon_looseId)")
    df = df.Define("Lepton_flavour", "Lepton_flavour(nTightElectron, nTightMuon)").Define("Lep_pt", "Lepton_var(Lepton_flavour, Electron_pt, TightElectron_idx, Muon_pt, TightMuon_idx)").Define("Lep_phi", "Lepton_var(Lepton_flavour, Electron_phi, TightElectron_idx, Muon_phi, TightMuon_idx)")
    df = df.Define("MT", "sqrt(2 * Lep_pt * PuppiMET_T1_pt_nominal * (1 - cos(Lep_phi - PuppiMET_T1_phi_nominal)))")
    df = df.Define("MHT", "MHT(GoodJet_idx, Jet_pt, Jet_phi, Jet_eta, Jet_mass)")

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
    # df = df.Define("JetBTag_idx", "GetJetBTag(GoodJet_idx, "+bTagAlg+","+str(year)+","+str(EE)+")")\
    #             .Define("nJetBtag", "static_cast<int>(JetBTag_idx.size());")
    
    return df

############### trigger selection #####################
def trigger_filter(df, data, isMC):
    hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
    # hlt_mu  = "(HLT_IsoMu24 || HLT_Mu50)"
    hlt_ele = "(HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200)"
    df_trig = df.Filter(hlt_met+" || "+hlt_ele, "trigger")
    return df_trig

def bookhisto(df, regions_def, var, s_cut):
    h_ = {}
    for reg in regions_def.keys():
        h_[reg] = {}
        for v in var:
            if "SFbtag" in v._name: continue

            if v._MConly and not sampleflag: 
                continue
            else:
                if regions_def[reg] == "":
                    if v._xarray is None:
                        h_[reg][v._name]= df.Histo1D((v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name, "w_nominal")
                    else:
                        h_[reg][v._name]= df.Histo1D((v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xarray), v._name, "w_nominal")
                else:
                    if v._xarray is None:
                        # print(v._name, reg, regions_def[reg])
                        h_[reg][v._name]= df.Filter(regions_def[reg]).Histo1D((v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name, "w_nominal")
                    else:
                        h_[reg][v._name]= df.Filter(regions_def[reg]).Histo1D((v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xarray), v._name, "w_nominal")                    
    
    return h_

def bookhisto2D(df, regions_def, var2d, s_cut):
    h_ = {}
    for reg in regions_def.keys():
        h_[reg] = {}
        for v in var2d:
            if regions_def[reg]=="":
                if v._xarray is None:
                    h_[reg][v._name] = df.Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xmin)+","+str(v._xmax)+")")\
                                     .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
                                     .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname, "w_nominal")
                else:
                    h_[reg][v._name] = df.Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xarray[0])+","+str(v._xarray[-1])+")")\
                                     .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
                                     .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xarray, v._nybins, v._ymin, v._ymax), v._xname, v._yname, "w_nominal")
            else:
                if v._xarray is None:
                    h_[reg][v._name] = df.Filter(regions_def[reg])\
                                     .Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xmin)+","+str(v._xmax)+")")\
                                     .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._ymin)+","+str(v._ymax)+")")\
                                     .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax), v._xname, v._yname, "w_nominal")
                else:
                    h_[reg][v._name] = df.Filter(regions_def[reg])\
                                     .Redefine(v._xname, "UnOvBin("+v._xname+","+str(v._nxbins)+","+str(v._xarray[0])+","+str(v._xarray[-1])+")")\
                                     .Redefine(v._yname, "UnOvBin("+v._yname+","+str(v._nybins)+","+str(v._yarray[0])+","+str(v._yarray[-1])+")")\
                                     .Histo2D((v._xname+"Vs"+v._yname+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xarray, v._nybins, v._yarray), v._xname, v._yname, "w_nominal")
    return h_

def savehisto(d, h, regions_def, var, s_cut, isMC):
    histo = {reg: {v._name: ROOT.TH1D(v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xmin, v._xmax) if v._xarray is None else ROOT.TH1D(v._name+"_"+reg+"_"+s_cut," ;"+v._title+"", v._nbins, v._xarray) for v in var} for reg in regions_def.keys()}
    isMC=True
    if "Data" in d.label: isMC = False
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]
    
    for s in s_list:
        outfile = ROOT.TFile.Open(repohisto+s.label+'.root', "RECREATE")
        for reg in regions_def.keys():
            for v in var:
                if "SFbtag" in v._name: continue
                if v._MConly and not isMC:
                    continue
                else:
                    histo[reg][v._name] = h[d.label][s.label][reg][v._name].GetValue()
                    if isMC:
                        histo[reg][v._name].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                    outfile.cd()
                    histo[reg][v._name].Write()
        outfile.Close()

# i plot2d per il momento non ci servono, si deve trovare un modo più intelligente di farli
def savehisto2d(d, h, regions_def, var2d, s_cut, isMC):
    histo = {reg: {v._name: ROOT.TH2D(v._name+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xmin, v._xmax, v._nybins, v._ymin, v._ymax)  if v._xarray is None else ROOT.TH2D(v._name+"_"+reg+"_"+s_cut," ;"+v._xtitle+";"+v._ytitle, v._nxbins, v._xarray, v._nybins, v._yarray)  for v in var2d} for reg in regions_def.keys()}
        
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
                    histo[reg][v].Scale(s.sigma*10**3/ntot_events[d.label][s.label])
                outfile.cd()
                histo[reg][v].Write()
        outfile.Close()


chain = {}
ntot_events = {}
for d in datasets:
    if hasattr(d, "components"):
        samples_list = d.components
    else:
        samples_list = [d]
    chain[d.label] = {}
    ntot_events[d.label] = {}
    for s in samples_list:
        if distributed: 
            nfiles = len(samples[d.label][s.label]['strings'])
            for i, string in enumerate(samples[d.label][s.label]['strings']): 
                samples[d.label][s.label]['strings'][i] = string.replace("root://cms-xrd-global.cern.ch/", "root://stormgf2.pi.infn.it/")
            chain[d.label][s.label] = samples[d.label][s.label]['strings']
        else: 
            nfiles = nfiles_max
            chain[d.label][s.label] = samples[d.label][s.label]['strings'][:nfiles]
        if not "Data" in s.label: ntot_events[d.label][s.label] = np.sum(samples[d.label][s.label]['ntot'][:nfiles])
        else: ntot_events[d.label][s.label] = None
        print("Dataset : "+s.label)
        print("# of files to process : ", nfiles)
        if distributed and len(chain[d.label][s.label])>2:
            print("files strings :\n  {}\n  {}\n  ... \n  {}\n  {}".format(chain[d.label][s.label][0], chain[d.label][s.label][1], chain[d.label][s.label][-2], chain[d.label][s.label][-1]))
        else :
            print("files strings :\n  {}".format(chain[d.label][s.label][0]))
        print("# of total events in the files to process (MC only, if Data the number is None) : ", ntot_events[d.label][s.label])

t0 = datetime.now()
print("starting loop on datasets: ",[d.label for d in datasets])
print("Local time :", t0)

h = {}
for d in datasets:
    if hasattr(d, "components"):
        s_list = d.components
    else:
        s_list = [d]

    if 'Data' in d.label : sampleflag = 0
    else: sampleflag = 1
    c_ = cut
    h[d.label] = {}
    h_2D[d.label] = {}
    for s in s_list:
        if os.path.exists(repohisto+s.label+'.root'):
            os.remove(repohisto+s.label+'.root')
        print("Processing dataset: ", s.label)
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
        df = RDataFrame("Events", tchains[d.label][s.label])
        
        
        df_ismc         = df.Define("isMC", "isMC("+str(sampleflag)+")")
        df_year         = df_ismc.Define("year", str(s.year))
        df_hemveto      = df_year.Define("HEMVeto", "hemveto(Jet_eta, Jet_phi, Electron_eta, Electron_phi)")
        df_hemveto      = df_hemveto.Filter("(isMC || (year != 2018) || (HEMVeto || run<319077.))")
        df_hlt          = trigger_filter(df_hemveto, s.label, sampleflag)

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
        else:
            df_wnom = df_hlt.Redefine('w_nominal', '1')


        df_presel       = preselection(df_wnom, bTagAlg, s.year, EE)
        
        
        if do_snapshot:
            opts = ROOT.RDF.RSnapshotOptions()
            opts.fLazy = True
            if distributed: fold = "./"
            else: fold = folder
            snapshot_df = df_presel.Snapshot("events_nominal", fold+"snap_"+s.label+".root", branches, opts)
            # print("./"+s.label+".root")
        if do_histos:
            s_cut = cut_string(cut)
            if len(var) != 0 :
                h[d.label][s.label] = bookhisto(df_presel, regions_def, var, s_cut)
            if len(var2d) != 0 :
                h_2D[d.label][s.label] = bookhisto2D(df_presel, regions_def, var2d, s_cut)


if do_histos:
    print("All histos booked !")
    for d in datasets:
        if len(var):
            savehisto(d, h, regions_def, var, s_cut, sampleflag)
        if len(var2d) != 0 :
            savehisto2d(d, h_2D, regions_def, var2d, s_cut, sampleflag)
        print(d.label + " histos saved")
if do_snapshot:
    snapshot_df.GetValue()
    if distributed: 
        client.run(transfer_to_tier)
        print("Snapshots saved and trasfered to tier")
    print("Sanpshot done!")
t1 = datetime.now()
print("Job finished in: ", t1-t0)