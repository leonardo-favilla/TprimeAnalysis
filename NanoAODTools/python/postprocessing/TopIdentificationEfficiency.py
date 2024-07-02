import ROOT, os, math
import numpy as np
import optparse
from samples.samples import *
import json
from CMS_lumi import CMS_lumi

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

usage = 'python EfficiencyPlots.py -f folder_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dataset', dest='dataset', type=str, default = '', help='Please enter a dataset, default nothing')
parser.add_option('-f', '--folder', dest='folder', type=str, default = 'TaggerStudies_2018', help='Please enter a folder in the path /eos/home-a/acagnott/DarkMattter/nosynch/, default "TaggerStudies_2018"')

(opt, args) = parser.parse_args()

# lumi = opt.lumi
fold = opt.folder
dataset = opt.dataset
InputFolderSnap = "/eos/home-a/acagnott/DarkMatter/nosynch/"+fold+"/"
# InputFolderPlots = "/eos/home-a/acagnott/DarkMatter/nosynch/"+fold+"/plots/"

outfolderMiscellaneus = "/eos/home-a/acagnott/DarkMatter/nosynch/"+fold+"/miscellaneus/"
outfolderWeighted = "/eos/home-a/acagnott/DarkMatter/nosynch/"+fold+"/WeightedPlots/"

if not os.path.exists(outfolderMiscellaneus):
    os.makedirs(outfolderMiscellaneus)
if not os.path.exists(outfolderWeighted):
    os.makedirs(outfolderWeighted)
if not os.path.exists(InputFolderSnap):
    print("The folder does not exist")
filesnap = InputFolderSnap+"snapTagger_"+dataset+".root"
# if not os.path.exists(InputFolderPlots):
#     print("The plots folder does not exist")


print("InputFolders: ", InputFolderSnap)
print("OutputFolders: ", outfolderMiscellaneus, outfolderWeighted)
print("File: ", filesnap)

# General Info
TopTypes   = ["Resolved", "Mixed"]
TruthTypes = ["standard", "truth1", "truth2"]
ClusType = ["T1","T2"]
print("TopTypes: ", TopTypes)
print("TruthTypes: ", TruthTypes)
print("ClusType: ", ClusType)

rfile = ROOT.TFile.Open(filesnap)
tree = rfile.Get("events_nominal")

ptmin, ptmax, step = 0, 1000, 100
ptbin = [(i, i+step) for i in np.arange(ptmin, ptmax, step)]
print("ptbin: ", ptbin)

h_Mer = ROOT.TH1F("h", ";Gen Top p_{T};Efficiency", int((ptmax-ptmin)/step), ptmin, ptmax)
h_Mix = ROOT.TH1F("h", ";Gen Top p_{T};Efficiency", int((ptmax-ptmin)/step), ptmin, ptmax)
h_Res = ROOT.TH1F("h", ";Gen Top p_{T};Efficiency", int((ptmax-ptmin)/step), ptmin, ptmax)
h_min_Mer = h_Mer.Clone("h_min")
h_max_Mer = h_Mer.Clone("h_max")
h_min_Mix = h_Mix.Clone("h_min")
h_max_Mix = h_Mix.Clone("h_max")
h_min_Res = h_Res.Clone("h_min")
h_max_Res = h_Res.Clone("h_max")

for i, pt in enumerate(ptbin):
    tree.Draw("GenPartTop_pt>>h_total", "GenPartTop_pt>"+str(pt[0])+" && GenPartTop_pt<"+str(pt[1])+" && GenPartTop_pt>0 && MET_pt>25 && NGoodTopLep==1")
    h_total = ROOT.gDirectory.Get("h_total")
    tree.Draw("GenPartTop_pt>>h_TopMer", "GenPartTop_pt>"+str(pt[0])+" && GenPartTop_pt<"+str(pt[1])+" && TopMerged_truth_exists && GenPartTop_pt>0 && MET_pt>25 && NGoodTopLep==1")
    h_TopMer = ROOT.gDirectory.Get("h_TopMer")
    tree.Draw("GenPartTop_pt>>h_TopMix", "GenPartTop_pt>"+str(pt[0])+" && GenPartTop_pt<"+str(pt[1])+" && nTopClusterT1MixedMCTagstandard>0 && GenPartTop_pt>0 && MET_pt>25 && NGoodTopLep==1")
    h_TopMix = ROOT.gDirectory.Get("h_TopMix")
    tree.Draw("GenPartTop_pt>>h_TopRes", "GenPartTop_pt>"+str(pt[0])+" && GenPartTop_pt<"+str(pt[1])+" && nTopClusterT1ResolvedMCTagstandard>0 && GenPartTop_pt>0 && MET_pt>25 && NGoodTopLep==1")
    h_TopRes = ROOT.gDirectory.Get("h_TopRes")
    if h_total.GetEntries() > 0:
        epsilon_TopMer = h_TopMer.GetEntries()/h_total.GetEntries()
        err_TopMer = math.sqrt(epsilon_TopMer*(1-epsilon_TopMer)/h_total.GetEntries())
        epsilon_TopMix = h_TopMix.GetEntries()/h_total.GetEntries()
        err_TopMix = math.sqrt(epsilon_TopMix*(1-epsilon_TopMix)/h_total.GetEntries())
        epsilon_TopRes = h_TopRes.GetEntries()/h_total.GetEntries()
        err_TopRes = math.sqrt(epsilon_TopRes*(1-epsilon_TopRes)/h_total.GetEntries())
    else:
        epsilon_TopMer = 0
        err_TopMer = 0
        epsilon_TopMix = 0
        err_TopMix = 0
        epsilon_TopRes = 0
        err_TopRes = 0
    print(pt, h_total.GetEntries(), h_TopMer.GetEntries(), h_TopMix.GetEntries(), epsilon_TopMer, epsilon_TopMix, epsilon_TopRes)
    h_Mer.SetBinContent(i+1, epsilon_TopMer)
    h_Mer.SetBinError(i+1, err_TopMer)
    h_Mix.SetBinContent(i+1, epsilon_TopMix)
    h_Mix.SetBinError(i+1, err_TopMix)
    h_Res.SetBinContent(i+1, epsilon_TopRes)
    h_Res.SetBinError(i+1, err_TopRes)
    h_min_Mer.SetBinContent(i+1, epsilon_TopMer-err_TopMer)
    h_max_Mer.SetBinContent(i+1, epsilon_TopMer+err_TopMer)
    h_min_Mix.SetBinContent(i+1, epsilon_TopMix-err_TopMix)
    h_max_Mix.SetBinContent(i+1, epsilon_TopMix+err_TopMix)
    h_min_Res.SetBinContent(i+1, epsilon_TopRes-err_TopRes)
    h_max_Res.SetBinContent(i+1, epsilon_TopRes+err_TopRes)
    
h_uncertainty_Mer = h_Mer.Clone("h_uncertainty")
h_uncertainty_Mix = h_Mix.Clone("h_uncertainty")
h_uncertainty_Res = h_Res.Clone("h_uncertainty")
for i in range(1, h_uncertainty_Mer.GetNbinsX() + 1):
    y_up_Mer = h_max_Mer.GetBinContent(i)
    y_down_Mer = h_min_Mer.GetBinContent(i)
    h_uncertainty_Mer.SetBinContent(i, 0.5 * (y_up_Mer + y_down_Mer))
    h_uncertainty_Mer.SetBinError(i, 0.5 * (y_up_Mer - y_down_Mer))
for i in range(1, h_uncertainty_Mix.GetNbinsX() + 1):
    y_up_Mix = h_max_Mix.GetBinContent(i)
    y_down_Mix = h_min_Mix.GetBinContent(i)
    h_uncertainty_Mix.SetBinContent(i, 0.5 * (y_up_Mix + y_down_Mix))
    h_uncertainty_Mix.SetBinError(i, 0.5 * (y_up_Mix - y_down_Mix))
for i in range(1, h_uncertainty_Res.GetNbinsX() + 1):
    y_up_Res = h_max_Res.GetBinContent(i)
    y_down_Res = h_min_Res.GetBinContent(i)
    h_uncertainty_Res.SetBinContent(i, 0.5 * (y_up_Res + y_down_Res))
    h_uncertainty_Res.SetBinError(i, 0.5 * (y_up_Res - y_down_Res))

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
# leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
leg_stack = ROOT.TLegend(0.15, 0.75, 0.35, 0.9)
leg_stack.SetNColumns(1)
leg_stack.SetFillColor(0)
leg_stack.SetFillStyle(0)
leg_stack.SetTextFont(42)
leg_stack.SetBorderSize(0)
leg_stack.SetTextSize(0.03)

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = ""
# if run2 :
w = dataset.replace("_", " ") 
lumi_sqrtS = w#"(13 TeV)"
# elif run3:
#      lumi_sqrtS = "%s fb^{-1}  (13.6 TeV)"%(lumi)
iPeriod = 0
iPos = 0

c = ROOT.kRed+1

h_uncertainty_Mer.SetFillColor(c)
h_uncertainty_Mer.SetMarkerStyle(0)
h_uncertainty_Mer.SetLineWidth(100)
h_uncertainty_Mer.SetFillStyle(3244)
h_uncertainty_Mer.SetMarkerSize(0)
h_uncertainty_Mer.SetFillColor(c+2)
h_uncertainty_Mer.GetXaxis().SetTitleOffset(1.)
h_uncertainty_Mer.GetYaxis().SetTitleOffset(0.9)
h_uncertainty_Mer.GetYaxis().SetTitleSize(0.05)
h_uncertainty_Mer.SetFillStyle(3244)  # Stile pieno
h_uncertainty_Mer.GetYaxis().SetRangeUser(0., 1.)
# h_uncertainty_Mer.Draw("E2")  # Disegna con errori come rettangoli colorati
h_Mer.SetLineColor(c)
h_Mer.SetLineWidth(3)
h_Mer.SetMarkerStyle(32)
h_Mer.SetMarkerSize(2)
h_Mer.SetMarkerColor(c)
# h_Mer.GetYaxis().SetNdivisions(222)
h_Mer.GetYaxis().SetLabelFont(42)
h_Mer.GetYaxis().SetTitleFont(42)
h_Mer.GetYaxis().SetTitleOffset(0.9)
h_Mer.GetYaxis().SetLabelSize(0.05)
h_Mer.GetYaxis().SetTitleSize(0.05)
h_Mer.GetXaxis().SetLabelSize(0.05)
h_Mer.GetXaxis().SetTitleSize(0.05)
h_Mer.GetYaxis().SetLabelOffset(0.02)
h_Mer.GetYaxis().SetRangeUser(0., 1.2)
h_Mer.Draw(" PE")

c = ROOT.kGreen+2
h_uncertainty_Mix.SetFillColor(c)
h_uncertainty_Mix.SetMarkerStyle(0)
h_uncertainty_Mix.SetLineWidth(24)
h_uncertainty_Mix.SetFillStyle(3244)
h_uncertainty_Mix.SetMarkerSize(0)
h_uncertainty_Mix.SetFillColor(c+2)
h_uncertainty_Mix.GetXaxis().SetTitleOffset(1.)
h_uncertainty_Mix.GetYaxis().SetTitleOffset(0.9)
h_uncertainty_Mix.GetYaxis().SetTitleSize(0.05)
h_uncertainty_Mix.SetFillStyle(3244)  # Stile pieno
h_uncertainty_Mix.GetYaxis().SetRangeUser(0., 1.)
# h_uncertainty_Mix.Draw("same E2")  # Disegna con errori come rettangoli colorati
h_Mix.SetLineColor(c)
h_Mix.SetLineWidth(3)
h_Mix.SetMarkerStyle(21)
h_Mix.SetMarkerColor(c)
h_Mix.SetMarkerSize(2)
h_Mix.GetYaxis().SetNdivisions(503)
h_Mix.GetYaxis().SetLabelFont(42)
h_Mix.GetYaxis().SetTitleFont(42)
h_Mix.GetYaxis().SetTitleOffset(0.9)
h_Mix.GetYaxis().SetLabelSize(0.15)
h_Mix.GetYaxis().SetTitleSize(0.05)
h_Mix.GetYaxis().SetLabelOffset(0.02)
h_Mix.GetYaxis().SetRangeUser(0., 1.)
h_Mix.Draw("same, PE")

c = ROOT.kBlue+2
h_uncertainty_Res.SetFillColor(c)
h_uncertainty_Res.SetMarkerStyle(0)
h_uncertainty_Res.SetLineWidth(100)
h_uncertainty_Res.SetFillStyle(3244)
h_uncertainty_Res.SetMarkerSize(0)
h_uncertainty_Res.SetFillColor(c+2)
h_uncertainty_Res.GetXaxis().SetTitleOffset(1.)
h_uncertainty_Res.GetYaxis().SetTitleOffset(0.9)
h_uncertainty_Res.GetYaxis().SetTitleSize(0.05)
h_uncertainty_Res.SetFillStyle(3244)  # Stile pieno
h_uncertainty_Res.GetYaxis().SetRangeUser(0., 1.)
# h_uncertainty_Res.Draw("same E2")  # Disegna con errori come rettangoli colorati
h_Res.SetLineColor(c)
h_Res.SetLineWidth(3)
h_Res.SetMarkerStyle(26)
h_Res.SetMarkerColor(c)
h_Res.SetMarkerSize(2)
h_Res.GetYaxis().SetNdivisions(503)
h_Res.GetYaxis().SetLabelFont(42)
h_Res.GetYaxis().SetTitleFont(42)
h_Res.GetYaxis().SetTitleOffset(0.9)
h_Res.GetYaxis().SetLabelSize(0.15)
h_Res.GetYaxis().SetTitleSize(0.05)
h_Res.GetYaxis().SetLabelOffset(0.02)
h_Res.GetYaxis().SetRangeUser(0., 1.)
h_Res.Draw("same, PE")

leg_stack.AddEntry(h_Mer, "Top Merged", "Pl")
# leg_stack.AddEntry(h_uncertainty_Mer, "Stat. Unc.", "f")    
leg_stack.AddEntry(h_Mix, "Top Mixed", "Pl")
# leg_stack.AddEntry(h_uncertainty_Mix, "Stat. Unc.", "f")    
leg_stack.AddEntry(h_Res, "Top Resolved", "Pl")
# leg_stack.AddEntry(h_uncertainty_Res, "Stat. Unc.", "f")    
leg_stack.Draw("same")

CMS_lumi(pad1, lumi_sqrtS, iPos, "")
pad1.Update()
if not os.path.exists(outfolderMiscellaneus+"TopIdentificationEfficiency/"):
    os.makedirs(outfolderMiscellaneus+"TopIdentificationEfficiency/")
if not os.path.exists(outfolderMiscellaneus+"TopIdentificationEfficiency/pdf/"):
    os.makedirs(outfolderMiscellaneus+"TopIdentificationEfficiency/pdf/")
if not os.path.exists(outfolderMiscellaneus+"TopIdentificationEfficiency/png/"):
    os.makedirs(outfolderMiscellaneus+"TopIdentificationEfficiency/png/")
if not os.path.exists(outfolderMiscellaneus+"TopIdentificationEfficiency/C/"):
    os.makedirs(outfolderMiscellaneus+"TopIdentificationEfficiency/C/")
canvas.Print(outfolderMiscellaneus+"TopIdentificationEfficiency/pdf/"+dataset+"_TopIdentificationEfficiency.pdf")
canvas.Print(outfolderMiscellaneus+"TopIdentificationEfficiency/png/"+dataset+"_TopIdentificationEfficiency.png")
canvas.Print(outfolderMiscellaneus+"TopIdentificationEfficiency/C/"+dataset+"_TopIdentificationEfficiency.C")

