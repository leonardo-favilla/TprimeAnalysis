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
    "DataJetMET_2022",# "DataEGamma_2022",#"DataMuon_2022", 
    # "DataEGamma_2022", 
    "TT_2022", "QCD_2022", "ZJetsToNuNu_2jets_2022", "WJets_2jets_2022", "TprimeToTZ_700_2022", "TprimeToTZ_1000_2022", "TprimeToTZ_1800_2022",
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
# folder = "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_preselection/"
# folder = "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_triggerSF/"
folder = "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_selection/"

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

# ###########################################
# TriggerSF regions stacks
# vars = []
# vars.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 8, xmin = 100, xmax=800))
# vars.append(variable(name = "PuppiMET_phi", title= "MET #phi (Puppi) [GeV]", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) nominal [GeV]", nbins = 11, xarray = np.array([100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
# vars.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
# vars.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
# vars.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))

# hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
# hlt_mu  = "(HLT_IsoMu24 || HLT_Mu50)"
# hlt_ele = "(HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200)"

# regions = {
#     "orthogonalPreselR_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
#     "orthogonalPreselR_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
#     "orthogonalPreselR_CR"       :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron==0"
# }
####################################################


################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_").replace("<", "_l_")


################## main code 
infile      = {'Data': [], 'signal': [], 'bkg': []}
insample    = {'Data': [], 'signal': [], 'bkg': []}
h_bkg       = []
h_sign      = []
h_err       = []
h_bkg_err   = []

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
        elif 'tDM' in s.label or 'Tp' in s.label:
            infile['signal'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['signal'].append(s)
        else:
            infile['bkg'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['bkg'].append(s)
            
# print("Opened histos files")
# print(infile)
# print(infile.keys())
# sys.exit()
for v in vars:
    for r in regions.keys():
        h_sign = []
        # print("Creating ..")
        # print(v._name+"_"+r+"_"+cut_tag)
        ROOT.gROOT.SetStyle('Plain')
        #ROOT.gStyle.SetPalette(1)
        ROOT.gStyle.SetOptStat(0)
        ROOT.TH1.SetDefaultSumw2()
        stack = ROOT.THStack(v._name+"_"+r+"_"+cut_tag, v._name+"_"+r+"_"+cut_tag)

        leg_stack = ROOT.TLegend(0.45,0.88,0.9,0.71)
        leg_stack.SetNColumns(2)
        leg_stack.SetFillColor(0)
        leg_stack.SetFillStyle(0)
        leg_stack.SetTextFont(42)
        leg_stack.SetBorderSize(0)
        leg_stack.SetTextSize(0.03)
        
        l = []
        for i, (f,s) in enumerate(zip(infile["signal"], insample["signal"])):
            # print(s.label)
            print("Getting histo :", v._name+"_"+r+"_"+cut_tag)
            print(" from:", f)
            print(v._name+"_"+r+"_"+cut_tag)
            tmp = copy.deepcopy(ROOT.TH1D(f.Get(v._name+"_"+r+"_"+cut_tag)))
            if len(samples[s.label][s.label]["ntot"]):
                # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.process][s.label]["ntot"]))
                tmp.Scale(lumi)
            else:
                continue
            # print("scaled lumi "+str(lumi)+" from ", f)
            tmp.GetXaxis().SetTitle(v._title)
            tmp.SetName(s.leglabel)
            tmp.SetLineColor(s.color)
            tmp.SetLineWidth(1)
            tmp.SetTitle("")
            # print(tmp.GetBinContent(1))
            h_sign.append(tmp)
            # print(h_sign)
            # if s.leglabel not in l:
            if s.leglabel :
                l.append(s.leglabel)
                leg_stack.AddEntry(tmp, s.leglabel, "l")
            #f.Close()

        for i, (f,s) in enumerate(zip(infile["bkg"], insample["bkg"])):
            # print(s.label)
            # print("Getting histo :", v._name+"_"+r+"_"+cut_tag)
            # print(" from:", f)
            tmp = copy.deepcopy(ROOT.TH1D(f.Get(v._name+"_"+r+"_"+cut_tag)))
            if len(samples[s.label][s.label]["ntot"]):
                # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.process][s.label]["ntot"]))
                tmp.Scale(lumi)
            else:
                continue
            tmp.GetXaxis().SetTitle(v._title)
            # tmp.SetLineColor(s.color)
            # tmp.SetFillColor(s.color)
            tmp.SetLineColor(s.color)
            tmp.SetLineWidth(0)
            tmp.SetFillColorAlpha(s.color, 0.5)
            tmp.SetName(s.leglabel)
            tmp.SetTitle("")
            stack.Add(tmp)
            if s.leglabel not in l:
                l.append(s.leglabel)
                leg_stack.AddEntry(tmp, s.leglabel, "f")
            #f.Close()

        if (not blind and not "SR"in r):
            h_data = None #ROOT.TH1D()
            if not v._MConly :
                for f, s in zip(infile["Data"], insample["Data"]):
                    # print("Getting histo :", v._name+"_"+r+"_"+cut_tag)
                    # print(" from:", f, s.label)
                    #print(type(f)
                    tmp = copy.deepcopy(f.Get(v._name+"_"+r+"_"+cut_tag))
                    tmp.SetTitle("")
                    #tmp.SetLineColor(ROOT.kBlack)
                    if h_data==None:
                        h_data = tmp.Clone("")
                    else:
                        h_data.Add(tmp)
                    #print("tmp", type(tmp))
                    #print("h_data", type(h_data))
                    #f.Close()
                # print("tmp", type(tmp))
                # print("h_data", type(h_data))
                leg_stack.AddEntry(h_data, "data", "ep")
                h_data.SetMarkerStyle(20)
                h_data.SetMarkerSize(1)
                #stack.SetMaximum(10000)

        
        canvasname = "canvas_"+v._name+"_"+r+"_"+cut_tag
        c1 = ROOT.TCanvas(canvasname,"c1",50,50,900,600)
        # c1 = ROOT.TCanvas(canvasname,"c1",50,50,1500,900)
        c1.SetFillColor(0)
        # c1.SetBorderMode(0)
        c1.SetBorderSize(1)
        c1.SetFrameFillStyle(0)
        c1.SetFrameBorderMode(0)
        c1.SetLeftMargin(0.12)
        # c1.SetRightMargin( 0.9 )
        c1.SetRightMargin(1)
        c1.SetTopMargin(1)
        c1.SetBottomMargin(-1)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.Draw()
        c1.cd()

        # pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 1, 1)
        # pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 0.82, 1)
        pad1 = ROOT.TPad("pad1", "pad1", 0.01, 0.31, 0.85, 1)
        pad1.SetTopMargin(0.1)
        pad1.SetBottomMargin(0.02)
        pad1.SetLeftMargin(0.12)
        # pad1.SetRightMargin(0.05)
        pad1.SetRightMargin(0.1)
        # pad1.SetBorderMode(0)
        pad1.SetBorderSize(1)
        pad1.SetTickx(1)
        pad1.SetTicky(1)
        pad1.Draw()

        if (not blind and not "SR" in r and not v._MConly):
          maximum = max(stack.GetMaximum(),h_data.GetMaximum())
        #   minimum = min(stack.GetMinimum(),h_data.GetMinimum())
          if (len(h_sign) != 0 and h_sign[-1].GetMinimum()!= 0):
              minimum = h_sign[-1].GetMinimum()
          elif stack.GetMinimum()!= 0:
              minimum = stack.GetMinimum()*1e-1
          else:
              minimum = 1e-1 #min(stack.GetMinimum(),1e-4)
        else:
          maximum = stack.GetMaximum()
          if (len(h_sign) != 0):
              minimum = min([h.GetMaximum() for h in h_sign])
              if minimum == 0: 
                  minimum = 1e-1
          elif stack.GetMinimum()!= 0: 
              minimum = stack.GetMinimum()*1e-1
          else:
              minimum = 1e-1  
          #minimum = 1e-4
        
        logscale = True
        pad1.cd()
        if(logscale):
            stack.SetMaximum(maximum*10000)
            stack.SetMinimum(minimum)
            #stack.SetMinimum(minimum)
        else:
            stack.SetMaximum(maximum*1.6)
            stack.SetMinimum(minimum*0.5)
            #stack.SetMinimum(minimum)

        stack.SetTitle("")
        stack.Draw("HIST")
        # if "MinDelta_phi" in v._name:
        #         stack.GetXaxis().SetRange(1, 16)
        h_err = stack.GetStack().Last().Clone("h_err")
        h_err.SetTitle("")
        h_err.SetLineWidth(100)
        h_err.SetFillStyle(3154)
        h_err.SetMarkerSize(0)
        h_err.SetFillColor(ROOT.kGray+2)
        
        leg_stack.AddEntry(h_err, "Stat. Unc.", "f")
        
        h_err.Draw("e2same0")
        # stack.Draw()
        for h in h_sign: 
            # print(h.GetBinContent(1))
            h.Draw("hist same")
        if (not blind and not "SR"in r and not v._MConly):
            h_data.SetTitle("")
            h_data.Draw("eSAMEpx0")
        
        leg_stack.Draw("same")
        CMS_lumi.writeExtraText = 1
        CMS_lumi.extraText = ""
        if run2 :
            lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)
        elif run3:
             lumi_sqrtS = "%s fb^{-1}  (13.6 TeV)"%(lumi)
        iPeriod = 0
        iPos = 10
        # CMS_lumi(pad1, lumi_sqrtS, iPos, r+"_"+regions[r]
        CMS_lumi(pad1, lumi_sqrtS, iPos, r)
        #CMS_lumi(pad1, lumi_sqrtS, iPos, r)
        # pad1.Draw()
        pad1.Update()
        if logscale:
            pad1.SetLogy()
        # pad1.Draw()
        # pad1.Draw()
        #####################################################
    
        hratio = stack.GetStack().Last()
     
        c1.cd()
        # pad2= ROOT.TPad("pad2", "pad2", 0, 0.01 , 1, 0.315)
        # pad2= ROOT.TPad("pad2", "pad2", 0, 0.01 , 0.82, 0.315)
        pad2 = ROOT.TPad("pad2", "pad2", 0.01, 0.01, 0.85, 0.315)
        pad2.SetTopMargin(0.06)
        pad2.SetBottomMargin(0.45)
        pad2.SetLeftMargin(0.12)
        # pad2.SetRightMargin(0.05)
        pad2.SetRightMargin(0.1)
        pad2.SetBorderSize(1)
        ROOT.gStyle.SetHatchesSpacing(2)
        ROOT.gStyle.SetHatchesLineWidth(2)
        pad2.Draw()
        pad2.cd()
        if (not blind and not "SR"in r and not v._MConly):
            ratio = h_data.Clone("ratio")
            ratio.SetLineColor(ROOT.kBlack)
            ratio.SetMaximum(2)
            ratio.SetMinimum(0)
            # ratio.Sumw2()
            ratio.SetStats(0)
        
            ratio.Divide(hratio)
            ratio.SetMarkerStyle(20)
            ratio.SetMarkerSize(0.9)
            ratio.Draw("epx0e0")
            # if "MinDelta_phi" in v._name:
            #     ratio.GetXaxis().SetRange(1, 16)
            ratio.SetTitle("")
            ratio.GetYaxis().SetTitle("Data / MC")
            ratio.GetYaxis().SetNdivisions(503)
            ratio.GetXaxis().SetLabelFont(42)
            ratio.GetYaxis().SetLabelFont(42)
            ratio.GetXaxis().SetTitleFont(42)
            ratio.GetYaxis().SetTitleFont(42)
            ratio.GetXaxis().SetTitleOffset(1.1)
            ratio.GetYaxis().SetTitleOffset(0.35)
            ratio.GetXaxis().SetLabelSize(0.15)
            ratio.GetYaxis().SetLabelSize(0.15)
            ratio.GetXaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetTitleSize(0.16)
            # ratio.GetYaxis().SetRangeUser(0.,2.0)
            ratio.GetXaxis().SetTitle(v._title)
            ratio.GetXaxis().SetLabelOffset(0.04)
            ratio.GetYaxis().SetLabelOffset(0.02)
            ratio.Draw("epx0e0same")
        else:
            ratio = h_sign[0].Clone("ratio")
            for i in range(1, ratio.GetNbinsX() + 1):
               ratio.SetBinContent(i, 1)
            ratio.SetLineColor(ROOT.kBlack)
            ratio.SetMaximum(2)
            ratio.SetMinimum(0)
            ratio.SetStats(0)
            #ratio.Divide(h_sign[0])
            ratio.SetMarkerStyle(20)
            ratio.SetMarkerSize(0.9)
            ratio.Draw("epx0e0")
            # if "MinDelta_phi" in v._name:
            #     ratio.GetXaxis().SetRange(1, 16)
            ratio.SetTitle("")
            ratio.GetYaxis().SetTitle("Data / MC")
            ratio.GetYaxis().SetNdivisions(503)
            ratio.GetXaxis().SetLabelFont(42)
            ratio.GetYaxis().SetLabelFont(42)
            ratio.GetXaxis().SetTitleFont(42)
            ratio.GetYaxis().SetTitleFont(42)
            ratio.GetXaxis().SetTitleOffset(1.1)
            ratio.GetYaxis().SetTitleOffset(0.35)
            ratio.GetXaxis().SetLabelSize(0.15)
            ratio.GetYaxis().SetLabelSize(0.15)
            ratio.GetXaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetRangeUser(0.,2.0)
            ratio.GetXaxis().SetTitle(v._title)
            ratio.GetXaxis().SetLabelOffset(0.04)
            ratio.GetYaxis().SetLabelOffset(0.02)
            ratio.Draw("epx0e0same")
            
        
        h_bkg_err = hratio.Clone("h_err")
        h_bkg_err.Reset()
        #h_bkg_err.Sumw2()
        for i in range(1,hratio.GetNbinsX()+1):
            h_bkg_err.SetBinContent(i,1)
            if(hratio.GetBinContent(i)):
                h_bkg_err.SetBinError(i, (hratio.GetBinError(i)/hratio.GetBinContent(i)))
            else:
                h_bkg_err.SetBinError(i, 10^(-99))
        h_bkg_err.SetLineWidth(100)

        h_bkg_err.SetMarkerSize(0)
        h_bkg_err.SetFillColor(ROOT.kGray+1)
        h_bkg_err.Draw("e20same")
        if v._xarray is None:
            f1 = ROOT.TLine(v._xmin, 1., v._xmax,1.)
        else:
            f1 = ROOT.TLine(v._xarray[0], 1., v._xarray[-1],1.)

        f1.SetLineColor(ROOT.kBlack)
        f1.SetLineStyle(ROOT.kDashed)
        f1.Draw("same")
        
        ratio.GetYaxis().SetTitle("Data / MC")
        ratio.GetYaxis().SetNdivisions(503)
        ratio.GetXaxis().SetLabelFont(42)
        ratio.GetYaxis().SetLabelFont(42)
        ratio.GetXaxis().SetTitleFont(42)
        ratio.GetYaxis().SetTitleFont(42)
        ratio.GetXaxis().SetTitleOffset(1.1)
        ratio.GetYaxis().SetTitleOffset(0.35)
        ratio.GetXaxis().SetLabelSize(0.15)
        ratio.GetYaxis().SetLabelSize(0.15)
        ratio.GetXaxis().SetTitleSize(0.16)
        ratio.GetYaxis().SetTitleSize(0.16)
        # ratio.GetYaxis().SetRangeUser(0.,2.0)
        ratio.GetXaxis().SetTitle(v._title)
        ratio.GetXaxis().SetLabelOffset(0.04)
        ratio.GetYaxis().SetLabelOffset(0.02)
        ratio.Draw("epx0e0same")
        
        pad2.Draw()

        c1.cd()
        c1.RedrawAxis()
        pad2.RedrawAxis()
        #ROOT.TGaxis.SetMaxDigits(3)
        # c1.RedrawAxis()
        # pad2.RedrawAxis()
        # c1.Update()

        c1.Print(repostack+"png/"+canvasname+".png")
        c1.Print(repostack+"pdf/"+canvasname+".pdf")
        c1.Print(repostack+"C/"+canvasname+".C")
        # tmp.Delete()
        # h.Delete()
    
        os.system('set LD_PRELOAD=libtcmalloc.so')
        #####################################################
