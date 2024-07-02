#######################################################
# Script to make efficiency plots for the Tagger Studies
######################################################

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
# parser.add_option('-l', '--lumi', dest='lumi', type=float, default = 14, help='Please enter Luminosity to consider, default 14 fb^-1')
# parser.add_option('-n', '--nfile', dest='nfile', type=int, default = 1, help='Please enter the numbers of file runned in postselection for this samples, default 1')
parser.add_option('--effpt', dest='ptefficiency', default = False, action='store_true', help='Default make no Pt efficiency')
parser.add_option('--misidpt', dest='ptmisid', default = False, action='store_true', help='Default make no Pt misid')
# parser.add_option('--efficiencyeta', dest='etaefficiency', default = False, action='store_true', help='Default make no Eta efficiency')
# parser.add_option('--efficiencypteta', dest='ptetaefficiency', default = False, action='store_true', help='Default make no 2D efficiency Pt eta')
# parser.add_option('--topscore', dest='topscore', default = False, action='store_true', help='Default make no topscore plot')
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

ptmin, ptmax, step = {"Mixed": 200, "Resolved":0 }, {"Mixed": 1000, "Resolved":400 }, {"Mixed": 100, "Resolved":50 }
ptminRes, ptmaxRes, stepRes = 0, 400, 50
cluster = "T1"
truth = "standard"
if opt.ptefficiency:
    for top in TopTypes:
        str_truereco = "TopCluster"+cluster+top+"TrueRecoFirstCluster"+truth
        str_true = "TopCluster"+cluster+top+"MCTagTrueFirstCluster"+truth
        str_topPt = "Top_pt_"+top
        query = "MET_pt>25 && NGoodTopLep==1"
        ptbin = [(i, i+step[top]) for i in np.arange(ptmin[top], ptmax[top], step[top])]
        h = ROOT.TH1F("h", ";Top p_{T};#epsilon_{S}", int((ptmax[top]-ptmin[top])/step[top]), ptmin[top], ptmax[top])
        h_min = h.Clone("h_min")
        h_max = h.Clone("h_max")
        for b, pt in enumerate(ptbin):
            tree.Draw(str_truereco+">>truereco_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_truereco = ROOT.gDirectory.Get("truereco_"+str(pt[0])).GetBinContent(2)
            tree.Draw(str_true+">>true_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_true = ROOT.gDirectory.Get("true_"+str(pt[0])).GetBinContent(2)
            if tmp_true!=0:
                epsilon = tmp_truereco/tmp_true
                err = math.sqrt(epsilon*(1-epsilon)/tmp_true)
            else:
                epsilon = 0
                err = 0
            print(b+1, tmp_truereco,tmp_true, epsilon, err)
            h.SetBinContent(b+1, epsilon)
            h_min.SetBinContent(b+1, epsilon-err)
            h_max.SetBinContent(b+1, epsilon+err)
        h_uncertainty = h.Clone("h_uncertainty")
        for i in range(1, h_uncertainty.GetNbinsX() + 1):
            y_up = h_max.GetBinContent(i)
            y_down = h_min.GetBinContent(i)
            h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
            h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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
        leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
        leg_stack.SetNColumns(2)
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

        if "Mixed" in top: c = ROOT.kGreen+1
        elif "Resolved" in top: c = ROOT.kBlue+2

        h_uncertainty.SetFillColor(c)
        h_uncertainty.SetMarkerStyle(0)
        h_uncertainty.SetLineWidth(100)
        h_uncertainty.SetFillStyle(3244)
        h_uncertainty.SetMarkerSize(0)
        h_uncertainty.SetFillColor(c+2)
        h_uncertainty.GetXaxis().SetTitleOffset(1.)
        h_uncertainty.GetYaxis().SetTitleOffset(0.9)
        h_uncertainty.GetYaxis().SetTitleSize(0.05)
        h_uncertainty.SetFillStyle(3244)  # Stile pieno
        h_uncertainty.GetYaxis().SetRangeUser(0., 1.)
        h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
        h.SetLineColor(c)
        h.SetLineWidth(2)
        h.GetYaxis().SetNdivisions(503)
        h.GetYaxis().SetLabelFont(42)
        h.GetYaxis().SetTitleFont(42)
        h.GetYaxis().SetTitleOffset(0.35)
        h.GetYaxis().SetLabelSize(0.15)
        h.GetYaxis().SetTitleSize(0.16)
        h.GetYaxis().SetLabelOffset(0.02)
        h.GetYaxis().SetRangeUser(0., 1.)
        h.Draw("same hist")
        leg_stack.AddEntry(h, "Top "+top, "l")
        leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
        leg_stack.Draw("same")

        CMS_lumi(pad1, lumi_sqrtS, iPos, "")
        pad1.Update()

        canvas.Print(outfolderMiscellaneus+"PtEfficiency/pdf/"+dataset+"_PtEfficiency_Top"+top+".pdf")
        canvas.Print(outfolderMiscellaneus+"PtEfficiency/png/"+dataset+"_PtEfficiency_Top"+top+".png")
        canvas.Print(outfolderMiscellaneus+"PtEfficiency/C/"+dataset+"_PtEfficiency_Top"+top+".C")

if opt.ptmisid:
    for top in TopTypes:
        str_falsereco = "TopCluster"+cluster+top+"FalseRecoFirstCluster"+truth
        str_false = "TopCluster"+cluster+top+"MCTagFalseFirstCluster"+truth
        str_topPt = "Top_pt_"+top
        query = "MET_pt>25 && NGoodTopLep==1"
        ptbin = [(i, i+step[top]) for i in np.arange(ptmin[top], ptmax[top], step[top])]
        h = ROOT.TH1F("h", ";Top p_{T};MisId", int((ptmax[top]-ptmin[top])/step[top]), ptmin[top], ptmax[top])
        h_min = h.Clone("h_min")
        h_max = h.Clone("h_max")
        for b, pt in enumerate(ptbin):
            tree.Draw(str_falsereco+">>falsereco_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_falsereco = ROOT.gDirectory.Get("falsereco_"+str(pt[0])).GetBinContent(2)
            tree.Draw(str_false+">>false_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_false = ROOT.gDirectory.Get("false_"+str(pt[0])).GetBinContent(2)
            if tmp_false!=0:
                epsilon = tmp_falsereco/tmp_false
                err = math.sqrt(epsilon*(1-epsilon)/tmp_false)
            else:
                epsilon = 0
                err = 0
            print(b+1, tmp_falsereco,tmp_false, epsilon, err)
            h.SetBinContent(b+1, epsilon)
            h_min.SetBinContent(b+1, epsilon-err)
            h_max.SetBinContent(b+1, epsilon+err)
        h_uncertainty = h.Clone("h_uncertainty")
        for i in range(1, h_uncertainty.GetNbinsX() + 1):
            y_up = h_max.GetBinContent(i)
            y_down = h_min.GetBinContent(i)
            h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
            h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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
        leg_stack = ROOT.TLegend(0.4,0.80,0.98,0.70)
        leg_stack.SetNColumns(2)
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

        if "Mixed" in top: c = ROOT.kGreen+1
        elif "Resolved" in top: c = ROOT.kBlue+2

        h_uncertainty.SetFillColor(c)
        h_uncertainty.SetMarkerStyle(0)
        h_uncertainty.SetLineWidth(100)
        h_uncertainty.SetFillStyle(3244)
        h_uncertainty.SetMarkerSize(0)
        h_uncertainty.SetFillColor(c+2)
        h_uncertainty.GetXaxis().SetTitleOffset(1.2)
        h_uncertainty.GetYaxis().SetTitleOffset(1.5)
        h_uncertainty.GetYaxis().SetTitleSize(0.05)
        h_uncertainty.SetFillStyle(3244)  # Stile pieno
        h_uncertainty.GetYaxis().SetRangeUser(0., 0.5)
        h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
        h.SetLineColor(c)
        h.SetLineWidth(2)
        h.GetYaxis().SetNdivisions(503)
        h.GetYaxis().SetLabelFont(42)
        h.GetYaxis().SetTitleFont(42)
        h.GetYaxis().SetTitleOffset(0.35)
        h.GetYaxis().SetLabelSize(0.15)
        h.GetYaxis().SetTitleSize(0.16)
        h.GetYaxis().SetLabelOffset(0.02)
        h.GetYaxis().SetRangeUser(0., 0.5)
        h.Draw("same hist")
        
        leg_stack.AddEntry(h, "Top "+top, "l")
        leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
        leg_stack.Draw("same")

        CMS_lumi(pad1, lumi_sqrtS, iPos, "")
        pad1.Update()
        
        canvas.Print(outfolderMiscellaneus+"PtMisId/pdf/"+dataset+"_PtMisId_Top"+top+".pdf")
        canvas.Print(outfolderMiscellaneus+"PtMisId/png/"+dataset+"_PtMisId_Top"+top+".png")
        canvas.Print(outfolderMiscellaneus+"PtMisId/C/"+dataset+"_PtMisId_Top"+top+".C")

# TopMerged
if opt.ptefficiency:
    query = "MET_pt>25 && NGoodTopLep==1"
    mpt, Mpt, st = 200, 1000, 100
    ptbin = [(i, i+st) for i in np.arange(mpt, Mpt, st)]
    h = ROOT.TH1F("h", ";Top p_{T};#epsilon_{S}", int((Mpt-mpt)/st), mpt, Mpt)
    h_min = h.Clone("h_min")
    h_max = h.Clone("h_max")
    for b, pt in enumerate(ptbin):
        tree.Draw("TopMerged_bestTopTruth>>truereco_"+str(pt[0]), query+" && TopMerged_bestTopPt>"+str(pt[0])+" && TopMerged_bestTopPt<"+str(pt[1])+"&& TopMerged_bestTopScore>0.94")
        tmp_truereco = ROOT.gDirectory.Get("truereco_"+str(pt[0])).GetBinContent(2)
        tree.Draw("TopMerged_truth_exists>>true_"+str(pt[0]), query+" && TopMerged_bestTopPt>"+str(pt[0])+" && TopMerged_bestTopPt<"+str(pt[1]))
        tmp_true = ROOT.gDirectory.Get("true_"+str(pt[0])).GetBinContent(2)
        if tmp_true == 0:
            epsilon = 0
            err = 0
        else:
            epsilon = tmp_truereco/tmp_true
            err = math.sqrt(epsilon*(1-epsilon)/tmp_true)    
        print(b+1, tmp_truereco,tmp_true, epsilon, err)
        h.SetBinContent(b+1, epsilon)
        h_min.SetBinContent(b+1, epsilon-err)
        h_max.SetBinContent(b+1, epsilon+err)
    h_uncertainty = h.Clone("h_uncertainty")
    for i in range(1, h_uncertainty.GetNbinsX() + 1):
        y_up = h_max.GetBinContent(i)
        y_down = h_min.GetBinContent(i)
        h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
        h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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

    leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
    leg_stack.SetNColumns(2)
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


    h_uncertainty.SetFillColor(ROOT.kRed+1)
    h_uncertainty.SetMarkerStyle(0)
    h_uncertainty.SetLineWidth(100)
    h_uncertainty.SetFillStyle(3244)
    h_uncertainty.SetMarkerSize(0)
    h_uncertainty.SetFillColor(ROOT.kRed+2)
    h_uncertainty.GetXaxis().SetTitleOffset(1.2)
    h_uncertainty.GetYaxis().SetTitleOffset(1.5)
    h_uncertainty.GetYaxis().SetTitleSize(0.05)
    h_uncertainty.SetFillStyle(3244)  # Stile pieno
    h_uncertainty.GetYaxis().SetRangeUser(0., 1.)
    h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
    h.SetLineColor(ROOT.kRed+1)
    h.SetLineWidth(2)
    h.GetYaxis().SetNdivisions(503)
    h.GetYaxis().SetLabelFont(42)
    h.GetYaxis().SetTitleFont(42)
    h.GetYaxis().SetTitleOffset(0.35)
    h.GetYaxis().SetLabelSize(0.15)
    h.GetYaxis().SetTitleSize(0.16)
    h.GetYaxis().SetLabelOffset(0.02)
    h.GetYaxis().SetRangeUser(0., 1.)
    h.Draw("same hist")

    leg_stack.AddEntry(h, "Top Merged", "l")
    leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
    leg_stack.Draw("same")

    CMS_lumi(pad1, lumi_sqrtS, iPos, "")
    pad1.Update()

    canvas.Print(outfolderMiscellaneus+"PtEfficiency/pdf/"+dataset+"_PtEfficiency_TopMerged.pdf")
    canvas.Print(outfolderMiscellaneus+"PtEfficiency/png/"+dataset+"_PtEfficiency_TopMerged.png")
    canvas.Print(outfolderMiscellaneus+"PtEfficiency/C/"+dataset+"_PtEfficiency_TopMerged.C")

if opt.ptmisid:
    query = "MET_pt>25 && NGoodTopLep==1"
    mpt, Mpt, st = 200, 1000, 100
    ptbin = [(i, i+st) for i in np.arange(mpt, Mpt, st)]
    h = ROOT.TH1F("h", ";Top p_{T};MisId", int((Mpt-mpt)/st), mpt, Mpt)
    h_min = h.Clone("h_min")
    h_max = h.Clone("h_max")
    for b, pt in enumerate(ptbin):
        tree.Draw("TopMerged_bestTopTruth>>falsereco_"+str(pt[0]), query+" && TopMerged_bestTopPt>"+str(pt[0])+" && TopMerged_bestTopPt<"+str(pt[1])+"&& TopMerged_bestTopScore>0.94")
        tmp_falsereco = ROOT.gDirectory.Get("falsereco_"+str(pt[0])).GetBinContent(1)
        tree.Draw("TopMerged_truth_exists>>false_"+str(pt[0]), query+" && TopMerged_bestTopPt>"+str(pt[0])+" && TopMerged_bestTopPt<"+str(pt[1]))
        tmp_false = ROOT.gDirectory.Get("false_"+str(pt[0])).GetBinContent(1)
        if tmp_false == 0:
            epsilon = 0
            err = 0
        else:
            epsilon = tmp_falsereco/tmp_false
            err = math.sqrt(epsilon*(1-epsilon)/tmp_false)    
        print(b+1, tmp_falsereco,tmp_false, epsilon, err)
        h.SetBinContent(b+1, epsilon)
        h_min.SetBinContent(b+1, epsilon-err)
        h_max.SetBinContent(b+1, epsilon+err)
    h_uncertainty = h.Clone("h_uncertainty")
    for i in range(1, h_uncertainty.GetNbinsX() + 1):
        y_up = h_max.GetBinContent(i)
        y_down = h_min.GetBinContent(i)
        h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
        h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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

    leg_stack = ROOT.TLegend(0.4,0.80,0.98,0.70)
    leg_stack.SetNColumns(2)
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

    h_uncertainty.SetFillColor(ROOT.kRed+1)
    h_uncertainty.SetMarkerStyle(0)
    h_uncertainty.SetLineWidth(100)
    h_uncertainty.SetFillStyle(3244)
    h_uncertainty.SetMarkerSize(0)
    h_uncertainty.SetFillColor(ROOT.kRed+2)
    h_uncertainty.GetXaxis().SetTitleOffset(1.2)
    h_uncertainty.GetYaxis().SetTitleOffset(1.5)
    h_uncertainty.GetYaxis().SetTitleSize(0.05)
    h_uncertainty.SetFillStyle(3244)  # Stile pieno
    h_uncertainty.GetYaxis().SetRangeUser(0., 0.5)
    h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
    h.SetLineColor(ROOT.kRed+1)
    h.SetLineWidth(2)
    h.GetYaxis().SetNdivisions(503)
    h.GetYaxis().SetLabelFont(42)
    h.GetYaxis().SetTitleFont(42)
    h.GetYaxis().SetTitleOffset(0.35)
    h.GetYaxis().SetLabelSize(0.15)
    h.GetYaxis().SetTitleSize(0.16)
    h.GetYaxis().SetLabelOffset(0.02)
    h.GetYaxis().SetRangeUser(0., 0.5)
    h.Draw("same hist")

    leg_stack.AddEntry(h, "Top Merged", "l")
    leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
    leg_stack.Draw("same")

    CMS_lumi(pad1, lumi_sqrtS, iPos, "")
    pad1.Update()

    canvas.Print(outfolderMiscellaneus+"PtMisId/pdf/"+dataset+"_PtMisId_TopMerged.pdf")
    canvas.Print(outfolderMiscellaneus+"PtMisId/png/"+dataset+"_PtMisId_TopMerged.png")
    canvas.Print(outfolderMiscellaneus+"PtMisId/C/"+dataset+"_PtMisId_TopMerged.C")

if opt.ptmisid:
    for top in TopTypes:
        str_falsereco = "TopCluster"+cluster+top+"FalseRecoFirstCluster"+truth
        str_false = "TopCluster"+cluster+top+"MCTagFalseFirstCluster"+truth
        str_topPt = "HT_eventHT"
        query = "MET_pt>25 && NGoodTopLep==1"
        ptbin = [(i, i+step[top]) for i in np.arange(0,600, 100)]
        h = ROOT.TH1F("h", ";HT;MisId", int((ptbin[-1][1]-ptbin[0][0])/100), ptbin[0][0], ptbin[-1][1])
        h_min = h.Clone("h_min")
        h_max = h.Clone("h_max")
        for b, pt in enumerate(ptbin):
            tree.Draw(str_falsereco+">>falsereco_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_falsereco = ROOT.gDirectory.Get("falsereco_"+str(pt[0])).GetBinContent(2)
            tree.Draw(str_false+">>false_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_false = ROOT.gDirectory.Get("false_"+str(pt[0])).GetBinContent(2)
            if tmp_false!=0:
                epsilon = tmp_falsereco/tmp_false
                err = math.sqrt(epsilon*(1-epsilon)/tmp_false)
            else:
                epsilon = 0
                err = 0
            print(b+1, tmp_falsereco,tmp_false, epsilon, err)
            h.SetBinContent(b+1, epsilon)
            h_min.SetBinContent(b+1, epsilon-err)
            h_max.SetBinContent(b+1, epsilon+err)
        h_uncertainty = h.Clone("h_uncertainty")
        for i in range(1, h_uncertainty.GetNbinsX() + 1):
            y_up = h_max.GetBinContent(i)
            y_down = h_min.GetBinContent(i)
            h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
            h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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

        leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
        leg_stack.SetNColumns(2)
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

        if "Mixed" in top: c = ROOT.kGreen+1
        elif "Resolved" in top: c = ROOT.kBlue+2

        h_uncertainty.SetFillColor(c)
        h_uncertainty.SetMarkerStyle(0)
        h_uncertainty.SetLineWidth(100)
        h_uncertainty.SetFillStyle(3244)
        h_uncertainty.SetMarkerSize(0)
        h_uncertainty.SetFillColor(c+2)
        h_uncertainty.GetXaxis().SetTitleOffset(1.2)
        h_uncertainty.GetYaxis().SetTitleOffset(1.5)
        h_uncertainty.GetYaxis().SetTitleSize(0.05)
        h_uncertainty.SetFillStyle(3244)  # Stile pieno
        h_uncertainty.GetYaxis().SetRangeUser(0., 1.)
        h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
        h.SetLineColor(c)
        h.SetLineWidth(2)
        h.GetYaxis().SetNdivisions(503)
        h.GetYaxis().SetLabelFont(42)
        h.GetYaxis().SetTitleFont(42)
        h.GetYaxis().SetTitleOffset(0.35)
        h.GetYaxis().SetLabelSize(0.15)
        h.GetYaxis().SetTitleSize(0.16)
        h.GetYaxis().SetLabelOffset(0.02)
        h.GetYaxis().SetRangeUser(0., 1.)
        h.Draw("same hist")
        
        leg_stack.AddEntry(h, "Top "+top, "l")
        leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
        leg_stack.Draw("same")

        CMS_lumi(pad1, lumi_sqrtS, iPos, "")
        pad1.Update()
        
        canvas.Print(outfolderMiscellaneus+"HTMisId/pdf/"+dataset+"_HTMisId_Top"+top+".pdf")
        canvas.Print(outfolderMiscellaneus+"HTMisId/png/"+dataset+"_HTMisId_Top"+top+".png")
        canvas.Print(outfolderMiscellaneus+"HTMisId/C/"+dataset+"_HTMisId_Top"+top+".C")

if opt.ptefficiency:
    for top in TopTypes:
        str_falsereco = "TopCluster"+cluster+top+"TrueRecoFirstCluster"+truth
        str_false = "TopCluster"+cluster+top+"MCTagTrueFirstCluster"+truth
        str_topPt = "HT_eventHT"
        query = "MET_pt>25 && NGoodTopLep==1"
        ptbin = [(i, i+step[top]) for i in np.arange(0,600, 100)]
        h = ROOT.TH1F("h", ";HT;#epsilon_{S}", int((ptbin[-1][1]-ptbin[0][0])/100), ptbin[0][0], ptbin[-1][1])
        h_min = h.Clone("h_min")
        h_max = h.Clone("h_max")
        for b, pt in enumerate(ptbin):
            tree.Draw(str_falsereco+">>falsereco_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_falsereco = ROOT.gDirectory.Get("falsereco_"+str(pt[0])).GetBinContent(2)
            tree.Draw(str_false+">>false_"+str(pt[0]), query+" && "+str_topPt+">"+str(pt[0])+" && "+str_topPt+"<"+str(pt[1]))
            tmp_false = ROOT.gDirectory.Get("false_"+str(pt[0])).GetBinContent(2)
            if tmp_false!=0:
                epsilon = tmp_falsereco/tmp_false
                err = math.sqrt(epsilon*(1-epsilon)/tmp_false)
            else:
                epsilon = 0
                err = 0
            print(b+1, tmp_falsereco,tmp_false, epsilon, err)
            h.SetBinContent(b+1, epsilon)
            h_min.SetBinContent(b+1, epsilon-err)
            h_max.SetBinContent(b+1, epsilon+err)
        h_uncertainty = h.Clone("h_uncertainty")
        for i in range(1, h_uncertainty.GetNbinsX() + 1):
            y_up = h_max.GetBinContent(i)
            y_down = h_min.GetBinContent(i)
            h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
            h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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

        leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
        leg_stack.SetNColumns(2)
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

        if "Mixed" in top: c = ROOT.kGreen+1
        elif "Resolved" in top: c = ROOT.kBlue+2

        h_uncertainty.SetFillColor(c)
        h_uncertainty.SetMarkerStyle(0)
        h_uncertainty.SetLineWidth(100)
        h_uncertainty.SetFillStyle(3244)
        h_uncertainty.SetMarkerSize(0)
        h_uncertainty.SetFillColor(c+2)
        h_uncertainty.GetXaxis().SetTitleOffset(1.2)
        h_uncertainty.GetYaxis().SetTitleOffset(1.5)
        h_uncertainty.GetYaxis().SetTitleSize(0.05)
        h_uncertainty.SetFillStyle(3244)  # Stile pieno
        h_uncertainty.GetYaxis().SetRangeUser(0., 1.)
        h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
        h.SetLineColor(c)
        h.SetLineWidth(2)
        h.GetYaxis().SetNdivisions(503)
        h.GetYaxis().SetLabelFont(42)
        h.GetYaxis().SetTitleFont(42)
        h.GetYaxis().SetTitleOffset(0.35)
        h.GetYaxis().SetLabelSize(0.15)
        h.GetYaxis().SetTitleSize(0.16)
        h.GetYaxis().SetLabelOffset(0.02)
        h.GetYaxis().SetRangeUser(0., 1.)
        h.Draw("same hist")
        
        leg_stack.AddEntry(h, "Top "+top, "l")
        leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
        leg_stack.Draw("same")

        CMS_lumi(pad1, lumi_sqrtS, iPos, "")
        pad1.Update()

        canvas.Print(outfolderMiscellaneus+"HTEfficiency/pdf/"+dataset+"_HTEfficiency_Top"+top+".pdf")
        canvas.Print(outfolderMiscellaneus+"HTEfficiency/png/"+dataset+"_HTEfficiency_Top"+top+".png")
        canvas.Print(outfolderMiscellaneus+"HTEfficiency/C/"+dataset+"_HTEfficiency_Top"+top+".C")

if opt.ptefficiency:
    query = "MET_pt>25 && NGoodTopLep==1"
    mpt, Mpt, st = 0, 600, 100
    ptbin = [(i, i+st) for i in np.arange(mpt, Mpt, st)]
    h = ROOT.TH1F("h", ";HT;#epsilon_{S}", int((Mpt-mpt)/st), mpt, Mpt)
    h_min = h.Clone("h_min")
    h_max = h.Clone("h_max")
    for b, pt in enumerate(ptbin):
        tree.Draw("TopMerged_bestTopTruth>>truereco_"+str(pt[0]), query+" && HT_eventHT>"+str(pt[0])+" && HT_eventHT<"+str(pt[1])+"&& TopMerged_bestTopScore>0.94")
        tmp_truereco = ROOT.gDirectory.Get("truereco_"+str(pt[0])).GetBinContent(2)
        tree.Draw("TopMerged_truth_exists>>true_"+str(pt[0]), query+" && HT_eventHT>"+str(pt[0])+" && HT_eventHT<"+str(pt[1]))
        tmp_true = ROOT.gDirectory.Get("true_"+str(pt[0])).GetBinContent(2)
        if tmp_true == 0:
            epsilon = 0
            err = 0
        else:
            epsilon = tmp_truereco/tmp_true
            err = math.sqrt(epsilon*(1-epsilon)/tmp_true)    
        print(b+1, tmp_truereco,tmp_true, epsilon, err)
        h.SetBinContent(b+1, epsilon)
        h_min.SetBinContent(b+1, epsilon-err)
        h_max.SetBinContent(b+1, epsilon+err)
    h_uncertainty = h.Clone("h_uncertainty")
    for i in range(1, h_uncertainty.GetNbinsX() + 1):
        y_up = h_max.GetBinContent(i)
        y_down = h_min.GetBinContent(i)
        h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
        h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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

    leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
    leg_stack.SetNColumns(2)
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

    h_uncertainty.SetFillColor(ROOT.kRed+1)
    h_uncertainty.SetMarkerStyle(0)
    h_uncertainty.SetLineWidth(100)
    h_uncertainty.SetFillStyle(3244)
    h_uncertainty.SetMarkerSize(0)
    h_uncertainty.SetFillColor(ROOT.kRed+2)
    h_uncertainty.GetXaxis().SetTitleOffset(1.2)
    h_uncertainty.GetYaxis().SetTitleOffset(1.5)
    h_uncertainty.GetYaxis().SetTitleSize(0.05)
    h_uncertainty.SetFillStyle(3244)  # Stile pieno
    h_uncertainty.GetYaxis().SetRangeUser(0., 1.)
    h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
    h.SetLineColor(ROOT.kRed+1)
    h.SetLineWidth(2)
    h.GetYaxis().SetNdivisions(503)
    h.GetYaxis().SetLabelFont(42)
    h.GetYaxis().SetTitleFont(42)
    h.GetYaxis().SetTitleOffset(0.35)
    h.GetYaxis().SetLabelSize(0.15)
    h.GetYaxis().SetTitleSize(0.16)
    h.GetYaxis().SetLabelOffset(0.02)
    h.GetYaxis().SetRangeUser(0., 1.)
    h.Draw("same hist")

    leg_stack.AddEntry(h, "Top Merged", "l")
    leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
    leg_stack.Draw("same")

    CMS_lumi(pad1, lumi_sqrtS, iPos, "")
    pad1.Update()

    canvas.Print(outfolderMiscellaneus+"HTEfficiency/pdf/"+dataset+"_HTEfficiency_TopMerged.pdf")
    canvas.Print(outfolderMiscellaneus+"HTEfficiency/png/"+dataset+"_HTEfficiency_TopMerged.png")
    canvas.Print(outfolderMiscellaneus+"HTEfficiency/C/"+dataset+"_HTEfficiency_TopMerged.C")

if opt.ptmisid:
    query = "MET_pt>25 && NGoodTopLep==1"
    mpt, Mpt, st = 200, 1000, 100
    ptbin = [(i, i+st) for i in np.arange(0, 600, 100)]
    h = ROOT.TH1F("h", ";HT;MisId", int((ptbin[-1][1]-ptbin[0][0])/100), ptbin[0][0], ptbin[-1][1])
    h_min = h.Clone("h_min")
    h_max = h.Clone("h_max")
    for b, pt in enumerate(ptbin):
        tree.Draw("TopMerged_bestTopTruth>>falsereco_"+str(pt[0]), query+" && HT_eventHT>"+str(pt[0])+" && HT_eventHT<"+str(pt[1])+"&& TopMerged_bestTopScore>0.94")
        tmp_falsereco = ROOT.gDirectory.Get("falsereco_"+str(pt[0])).GetBinContent(1)
        tree.Draw("TopMerged_truth_exists>>false_"+str(pt[0]), query+" && HT_eventHT>"+str(pt[0])+" && HT_eventHT<"+str(pt[1]))
        tmp_false = ROOT.gDirectory.Get("false_"+str(pt[0])).GetBinContent(1)
        if tmp_false == 0:
            epsilon = 0
            err = 0
        else:
            epsilon = tmp_falsereco/tmp_false
            err = math.sqrt(epsilon*(1-epsilon)/tmp_false)    
        print(b+1, tmp_falsereco,tmp_false, epsilon, err)
        h.SetBinContent(b+1, epsilon)
        h_min.SetBinContent(b+1, epsilon-err)
        h_max.SetBinContent(b+1, epsilon+err)
    h_uncertainty = h.Clone("h_uncertainty")
    for i in range(1, h_uncertainty.GetNbinsX() + 1):
        y_up = h_max.GetBinContent(i)
        y_down = h_min.GetBinContent(i)
        h_uncertainty.SetBinContent(i, 0.5 * (y_up + y_down))
        h_uncertainty.SetBinError(i, 0.5 * (y_up - y_down))
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

    leg_stack = ROOT.TLegend(0.4,0.20,0.98,0.15)
    leg_stack.SetNColumns(2)
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

    h_uncertainty.SetFillColor(ROOT.kRed+1)
    h_uncertainty.SetMarkerStyle(0)
    h_uncertainty.SetLineWidth(100)
    h_uncertainty.SetFillStyle(3244)
    h_uncertainty.SetMarkerSize(0)
    h_uncertainty.SetFillColor(ROOT.kRed+2)
    h_uncertainty.GetXaxis().SetTitleOffset(1.2)
    h_uncertainty.GetYaxis().SetTitleOffset(1.5)
    h_uncertainty.GetYaxis().SetTitleSize(0.05)
    h_uncertainty.SetFillStyle(3244)  # Stile pieno
    h_uncertainty.GetYaxis().SetRangeUser(0., 1.)
    h_uncertainty.Draw("E2")  # Disegna con errori come rettangoli colorati
    h.SetLineColor(ROOT.kRed+1)
    h.SetLineWidth(2)
    h.GetYaxis().SetNdivisions(503)
    h.GetYaxis().SetLabelFont(42)
    h.GetYaxis().SetTitleFont(42)
    h.GetYaxis().SetTitleOffset(0.35)
    h.GetYaxis().SetLabelSize(0.15)
    h.GetYaxis().SetTitleSize(0.16)
    h.GetYaxis().SetLabelOffset(0.02)
    h.GetYaxis().SetRangeUser(0., 1.)
    h.Draw("same hist")

    leg_stack.AddEntry(h, "Top Merged", "l")
    leg_stack.AddEntry(h_uncertainty, "Stat. Unc.", "f")    
    leg_stack.Draw("same")

    CMS_lumi(pad1, lumi_sqrtS, iPos, "")
    pad1.Update()

    canvas.Print(outfolderMiscellaneus+"HTMisId/pdf/"+dataset+"_HTMisId_TopMerged.pdf")
    canvas.Print(outfolderMiscellaneus+"HTMisId/png/"+dataset+"_HTMisId_TopMerged.png")
    canvas.Print(outfolderMiscellaneus+"HTMisId/C/"+dataset+"_HTMisId_TopMerged.C")