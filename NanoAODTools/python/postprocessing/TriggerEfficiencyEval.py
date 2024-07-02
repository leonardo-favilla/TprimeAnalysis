import ROOT
import os
import sys
from samples.samples import *
from CMS_lumi import CMS_lumi
from variables import *
import copy
import json
import numpy as np
#import math
#import pickle as pkl
#from datetime import datetime
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)


################## input parameters

cut  = requirements  ### defined in variables.py 
lumi = 7.87#34.3 (full2022) #59.97(2018) 
run2 = False
run3 = not run2
# datasets = [
#     DataHT_2018,
#     TT_2018, ZJetsToNuNu_2018, QCD_2018, WJets_2018,   
#     # TprimeToTZ_700_2018, TprimeToTZ_1000_2018, TprimeToTZ_1800_2018,
#                ]
datasets = [
    # "DataMETA_2018",
    # DataSingleMuA_2018,
    # "TT_hadr_2018", "TT_semilep_2018", "TT_Mtt1000toInf_2018", "TT_Mtt700to1000_2018", 
    # "QCDHT_100to200_2018", "QCDHT_200to300_2018","QCDHT_300to500_2018", "QCDHT_500to700_2018", "QCDHT_700to1000_2018", "QCDHT_1000to1500_2018", "QCDHT_1500to2000_2018", "QCDHT_2000toInf_2018", 
    # "ZJetsToNuNu_HT100to200_2018", "ZJetsToNuNu_HT200to400_2018", "ZJetsToNuNu_HT400to600_2018", "ZJetsToNuNu_HT600to800_2018", "ZJetsToNuNu_HT800to1200_2018", "ZJetsToNuNu_HT1200to2500_2018", "ZJetsToNuNu_HT2500toInf_2018", 
    # "WJetsHT100to200_2018", "WJetsHT200to400_2018", "WJetsHT400to600_2018", "WJetsHT600to800_2018", "WJetsHT800to1200_2018", "WJetsHT1200to2500_2018", "WJetsHT2500toInf_2018",   
    # "TprimeToTZ_700_2018", "TprimeToTZ_1000_2018", "TprimeToTZ_1800_2018",
    "DataJetMET_2022", #    "DataMuon_2022", 
    "DataEGamma_2022", 
    "TT_2022", "QCD_2022", "ZJetsToNuNu_2jets_2022", "WJets_2jets_2022"#, "TprimeToTZ_700_2022", "TprimeToTZ_1800_2022",
    # "WJets_2jets_2022"
               ]

for d in datasets:
    ### Extract Components ###
    if hasattr(sample_dict[d], "components"):
        components = sample_dict[d].components
    else:
        components = [sample_dict[d]]

blind = False # Set to True if you want to blind the data


# Specify the path to the JSON file
json_file = "samples/dict_samples_2022.json"

# Load the JSON file
with open(json_file, "r") as file:
    samples = json.load(file)

print("Paremeters setted") 
print("cut              = {}".format(cut))      
print("lumi (fb)        = {}".format(str(lumi)))
print("input datasets   = {}".format([sample_dict[d].label for d in datasets]))
print("blind            = {}".format(blind))

################# variables & regions definition --> defined in variables.py 
print("Producing histos:  {}".format([v._name for v in vars[1:]]))
print("Regions:           {}".format(regions.keys()))

############### out folders  
folder = "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_triggerSF/"
# "/eos/home-a/acagnott/DarkMatter/nosynch/run2018_exo22014_v2_MET/"

if not os.path.exists(folder):
    os.mkdir(folder)
repohisto = folder+"plots/"
if not os.path.exists(repohisto):
    os.mkdir(repohisto)
repostack = folder+"stacks/"
if not os.path.exists(repostack):
    os.mkdir(repostack)
if not os.path.exists(repostack+"/png"):
    os.mkdir(repostack+"/png")
if not os.path.exists(repostack+"/pdf"):
    os.mkdir(repostack+"/pdf")
if not os.path.exists(repostack+"/C"):
    os.mkdir(repostack+"/C")

print("Created folders 'plots' and 'stacks' at ", folder)

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_").replace("<", "_l_")

var = []
var.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 8, xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_phi", title= "MET #phi (Puppi) [GeV]", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 11, xarray = np.array([100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
var.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
var.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))

hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hlt_mu  = "(HLT_IsoMu24 || HLT_Mu50)"
hlt_ele = "(HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200)"

regions = {
    "orthogonalPreselR_Ntot"     : hlt_ele +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nVetoElectron > 0",
    "orthogonalPreselR_Npass"    : hlt_ele +" && "+hlt_met+" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nVetoElectron > 0"
}

infile      = {'Data': [], 'signal': [], 'bkg': []}
insample    = {'Data': [], 'signal': [], 'bkg': []}

cut_tag     = cut_string(cut)

for dat in datasets:
    d = sample_dict[dat]
    # print(repohisto + d.label + ".root")
    if hasattr(d, 'components'):
        s_list = d.components
    else:
        s_list = [d]
    for s in s_list:
        if 'Data' in s.label:
            infile['Data'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['Data'].append(s)         
        # elif 'tDM' in s.label or 'Tp' in s.label:
        #     infile['signal'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
        #     insample['signal'].append(s)
        else:
            infile['bkg'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['bkg'].append(s)

h_bkg_total    = None
h_data_total   = None
h_bkg_pass     = None
h_data_pass    = None


outfileroot = ROOT.TFile.Open(repohisto + "TriggerEfficiency.root", "RECREATE")

for v in [var[2]]:
    r = "orthogonalPreselR_Ntot"
    for i, (f,s) in enumerate(zip(infile["bkg"], insample["bkg"])):
        tmp = copy.deepcopy(ROOT.TH1D(f.Get(v._name+"_"+r+"_"+cut_tag)))
        if len(samples[s.label][s.label]["ntot"]):
            tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_total==None:
            h_bkg_total = tmp.Clone("")
            h_bkg_total.SetName(v._name+"_"+r+"_bkgtotal")
        else:
            h_bkg_total.Add(tmp)
        
    for f, s in zip(infile["Data"], insample["Data"]):
        tmp = copy.deepcopy(f.Get(v._name+"_"+r+"_"+cut_tag))
        tmp.SetTitle("")
        if h_data_total==None:
            h_data_total = tmp.Clone("")
            h_data_total.SetName(v._name+"_"+r+"_datatotal")
        else:
            h_data_total.Add(tmp)

    r = "orthogonalPreselR_Npass"
    for i, (f,s) in enumerate(zip(infile["bkg"], insample["bkg"])):
        tmp = copy.deepcopy(ROOT.TH1D(f.Get(v._name+"_"+r+"_"+cut_tag)))
        if len(samples[s.label][s.label]["ntot"]):
            tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_pass==None:
            h_bkg_pass = tmp.Clone("")
            h_bkg_pass.SetName(v._name+"_"+r+"_bkgpass")
        else:
            h_bkg_pass.Add(tmp)
        
    for f, s in zip(infile["Data"], insample["Data"]):
        tmp = copy.deepcopy(f.Get(v._name+"_"+r+"_"+cut_tag))
        tmp.SetTitle("")
        if h_data_pass==None:
            h_data_pass = tmp.Clone("")
            h_data_pass.SetName(v._name+"_"+r+"_datapass")
        else:
            h_data_pass.Add(tmp)
    # Calculate efficiency histograms
    
    for i in range(1, h_data_pass.GetNbinsX() + 1):
        print("data num", h_data_pass.GetBinContent(i))
        print("data den", h_data_total.GetBinContent(i))
    h_eff_bkg = h_bkg_pass.Clone("")
    h_eff_bkg.SetName("bkg_efficiency")
    h_eff_bkg.Divide(h_bkg_total)
    h_eff_data = h_data_pass.Clone("")
    h_eff_data.SetName("data_efficiency")
    h_eff_data.Divide(h_data_total)

    # Calculate uncertainties on efficiencies
    print("Trigger efficiency for MET trigger:")
    for i in range(1, h_eff_bkg.GetNbinsX() + 1):
        eff_bkg = h_eff_bkg.GetBinContent(i)
        eff_data = h_eff_data.GetBinContent(i)
        ntot_bkg = h_bkg_total.GetBinContent(i)
        ntot_data = h_data_total.GetBinContent(i)
        unc_bkg = eff_bkg * (1 - eff_bkg) / ntot_bkg if ntot_bkg > 0 else 0
        unc_data = eff_data * (1 - eff_data) / ntot_data if ntot_data > 0 else 0
        h_eff_bkg.SetBinError(i, unc_bkg)
        h_eff_data.SetBinError(i, unc_data)
        lowedge = h_eff_bkg.GetXaxis().GetBinLowEdge(i)
        upedge = h_eff_bkg.GetXaxis().GetBinUpEdge(i)
        print("MET bin [{}, {}]: bkg eff = {:.5f} +/- {:.5f}, data eff = {:.5f} +/- {:.5f}".format(lowedge, upedge, eff_bkg, unc_bkg, eff_data, unc_data))
    # Save histograms to file
    outfileroot.cd()
    h_eff_bkg.Write()
    h_eff_data.Write()
    h_bkg_pass.Write()
    h_data_pass.Write()
    h_bkg_total.Write()
    h_data_total.Write()

    canvas = ROOT.TCanvas("canvas","canvas", 50,50,900,600)
    canvas.SetFillColor(0)
    # canvas.SetBorderMode(0)
    canvas.SetBorderSize(1)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin(0.15)
    # canvas.SetRightMargin( 0.9 )
    canvas.SetRightMargin(1)
    canvas.SetTopMargin(1)
    canvas.SetBottomMargin(-1)
    canvas.SetTickx(1)
    canvas.SetTicky(1)
    canvas.Draw()
    pad1 = ROOT.TPad("pad1", "pad1", 0.01, 0.01, 0.99, 0.99)
    pad1.Draw()
    pad1.cd()

    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = ""
    lumi_sqrtS = "2022 (13.6 TeV)"
    iPeriod = 0
    iPos = 10

    c = ROOT.kRed+1
    pad1.cd()
    h_eff_bkg.SetLineColor(c)
    h_eff_bkg.SetMarkerColor(c)
    h_eff_bkg.SetMarkerStyle(20)
    h_eff_bkg.SetMarkerSize(0.8)
    h_eff_bkg.GetXaxis().SetTitle(v._title)
    h_eff_bkg.GetYaxis().SetTitle("Efficiency")
    h_eff_bkg.GetYaxis().SetRangeUser(0, 1.4)
    h_eff_bkg.GetYaxis().SetLabelFont(42)
    h_eff_bkg.GetYaxis().SetTitleFont(42)
    h_eff_bkg.GetXaxis().SetTitleSize(0.05)
    h_eff_bkg.GetYaxis().SetTitleSize(0.05)
    h_eff_bkg.Draw("PE")
    c = ROOT.kBlack
    pad1.cd()
    h_eff_data.SetLineColor(c)
    h_eff_data.SetMarkerColor(c)
    h_eff_data.SetMarkerStyle(20)
    h_eff_data.SetMarkerSize(0.8)
    h_eff_data.GetXaxis().SetTitle(v._title)
    h_eff_data.GetYaxis().SetTitle("Efficiency")
    h_eff_data.GetYaxis().SetRangeUser(0, 1.4)
    h_eff_data.Draw("PE, same")
    CMS_lumi(pad1, lumi_sqrtS, iPos, "")
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(h_eff_bkg, "Background", "Pl")
    legend.AddEntry(h_eff_data, "Data", "Pl")
    # legend.SetBorderSize(0)
    # legend.SetFillColor(0)
    legend.SetNColumns(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.Draw()
    pad1.Update()
    canvas.SaveAs(repostack+"/png/" + v._name + "_Triggefficiency.png")
    canvas.SaveAs(repostack+"/pdf/" + v._name + "_Triggefficiency.pdf")
    canvas.SaveAs(repostack+"/C/" + v._name + "_Triggefficiency.C")

    # Calculate the ratio between background efficiency and data efficiency
    h_ratio = h_eff_bkg.Clone("")
    h_ratio.SetName("SF")
    h_ratio.Divide(h_eff_data)
    for i in range(1, h_ratio.GetNbinsX() + 1):
        eff_bkg = h_eff_bkg.GetBinContent(i)
        eff_data = h_eff_data.GetBinContent(i)
        unc_bkg = h_eff_bkg.GetBinError(i)
        unc_data = h_eff_data.GetBinError(i)
        sf = eff_bkg / eff_data if eff_data > 0 else 0
        unc_sf = sf * math.sqrt((unc_bkg / eff_bkg)**2 + (unc_data / eff_data)**2) if eff_bkg > 0 and eff_data > 0 else 0
        h_ratio.SetBinContent(i, sf)
        h_ratio.SetBinError(i, unc_sf)
        print("MET bin [{}, {}]: SF = {:.5f} +/- {:.5f}".format(h_ratio.GetXaxis().GetBinLowEdge(i), h_ratio.GetXaxis().GetBinUpEdge(i), sf, unc_sf))

    # Create a new canvas for the ratio plot
    canvas_ratio = ROOT.TCanvas("canvas_ratio", "canvas_ratio", 50, 50, 900, 600)
    canvas_ratio.SetFillColor(0)
    canvas_ratio.SetBorderSize(1)
    canvas_ratio.SetFrameFillStyle(0)
    canvas_ratio.SetFrameBorderMode(0)
    canvas_ratio.SetLeftMargin(0.15)
    canvas_ratio.SetRightMargin(1)
    canvas_ratio.SetTopMargin(1)
    canvas_ratio.SetBottomMargin(-1)
    canvas_ratio.SetTickx(1)
    canvas_ratio.SetTicky(1)
    canvas_ratio.Draw()

    pad_ratio = ROOT.TPad("pad_ratio", "pad_ratio", 0.01, 0.01, 0.99, 0.99)
    pad_ratio.Draw()
    pad_ratio.cd()

    h_ratio.SetLineColor(ROOT.kBlack)
    h_ratio.SetMarkerColor(ROOT.kBlack)
    h_ratio.SetMarkerStyle(20)
    h_ratio.SetMarkerSize(0.8)
    h_ratio.GetXaxis().SetTitle(v._title)
    h_ratio.GetYaxis().SetTitle("SF")
    h_ratio.GetYaxis().SetRangeUser(0.6, 2.0)
    h_ratio.GetYaxis().SetLabelFont(42)
    h_ratio.GetYaxis().SetTitleFont(42)
    h_ratio.GetXaxis().SetTitleSize(0.05)
    h_ratio.GetYaxis().SetTitleSize(0.05)
    h_ratio.Draw("PE")

    CMS_lumi(pad_ratio, lumi_sqrtS, iPos, "")

    pad_ratio.Update()
    canvas_ratio.SaveAs(repostack+"/png/" + v._name + "_Ratio.png")
    canvas_ratio.SaveAs(repostack+"/pdf/" + v._name + "_Ratio.pdf")
    canvas_ratio.SaveAs(repostack+"/C/" + v._name + "_Ratio.C")

outfileroot.Close()
