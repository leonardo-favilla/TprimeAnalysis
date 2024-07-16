import ROOT 
import cmsstyle as CMS
import os
from variables import *
from samples.samples import *
import numpy as np
import json
import copy
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

def plot(h, folder, fillcolor, canv_name = "canv" ,extraTest="Preliminary", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "Efficiency"):

    if type(h)==list:
        h1 = h[0]
        # hist_dict = [k.GetName() for k in h]
    else:
        h1 = h
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)

    x_min = h1.GetXaxis().GetXmin()
    x_max = h1.GetXaxis().GetXmax()
    y_min = h1.GetMinimum()
    if y_min !=0: y_min = y_min - 0.2
    y_max = h1.GetMaximum()
    y_max = y_max + 0.3 * (y_max - y_min)
    x_axis_name = h1.GetXaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular,extraSpace=1.1, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    if type(h)==list:
        CMS.cmsDraw(h[1], "P", marker= 8, lcolor =  ROOT.TColor.GetColor("#e42536"), mcolor =  ROOT.TColor.GetColor("#e42536"))
        leg.AddEntry(h[1], "Simulation", "l")
        CMS.cmsDraw(h[0], "P", marker= 8, lcolor = ROOT.kBlack, mcolor = ROOT.kBlack)
        leg.AddEntry(h[0], "Data", "l")
        leg.Draw("same")
    else:
        if ytitle=="SF":
            CMS.cmsDraw(h1, "P", marker= 8 , mcolor = fillcolor)
        else:
            CMS.cmsDraw(h1, "P", marker= 8 ,lcolor = fillcolor, mcolor = fillcolor)
    CMS.SaveCanvas(canv, folder+"/pdf/"+canv_name+".pdf")
    # CMS.SaveCanvas(canv, folder+"/png/"+canv_name+".png")
    # CMS.SaveCanvas(canv, folder+"/C/"+canv_name+".C")

def plot2D(h1, folder, v, canv_name = "canv2d" ,extraTest="Simulation", iPos=0, energy="13", lumi = "",  addInfo="", ztitle="Efficiency"):

    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)

    # x_min = h1.GetXaxis().GetXmin()
    # x_max = h1.GetXaxis().GetXmax()
    # y_min = h1.GetYaxis().GetYmin()
    # y_max = h1.GetYaxis().GetYmin()
    # x_axis_name = h1.GetXaxis().GetTitle()
    # y_axis_name = h1.GetYaxis().GetTitle()
    x_min = v._xarray[0]
    x_max = v._xarray[-1]
    y_min = v._yarray[0]
    y_max = v._yarray[-1]
    x_axis_name = v._xtitle
    y_axis_name = v._ytitle
    # h1.GetXaxis().SetTitleOffset(1.01)
    # h1.GetXaxis().SetTitleSize(0.001)
    # h1.GetXaxis().SetLabelSize(0.001)
    # h1.GetXaxis().SetLabelOffset(0.005)
    # h1.GetYaxis().SetTitleOffset(1.01)
    # h1.GetYaxis().SetTitleSize(0.001)
    # h1.GetYaxis().SetLabelSize(0.001)
    # h1.GetYaxis().SetLabelOffset(0.005)
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,y_axis_name,square=CMS.kSquare,extraSpace= 0.01, iPos=iPos, with_z_axis=True)
    h1.Draw("same colz")
    h1.GetZaxis().SetTitle(ztitle)
    h1.GetZaxis().SetTitleOffset(1.35)
    h1.GetZaxis().SetTitleSize(0.035)
    h1.GetZaxis().SetLabelSize(0.035)
    h1.GetZaxis().SetLabelOffset(0.005)

    # Set the CMS official palette
    CMS.SetCMSPalette()
    CMS.UpdatePalettePosition(h1, canv)
    
    # CMS.cmsDraw(h1, "", marker= 10 ,lcolor = fillcolor)
    CMS.SaveCanvas(canv, folder+"/pdf/"+canv_name+".pdf")
    # CMS.SaveCanvas(canv, folder+"/png/"+canv_name+".png")
    # CMS.SaveCanvas(canv, folder+"/C/"+canv_name+".C")

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
    "DataEGamma_2022", 
    "TT_2022", 
    "QCD_2022", 
    "ZJetsToNuNu_2jets_2022",
     "WJets_2jets_2022"
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
# print("blind            = {}".format(blind))

################# variables & regions definition --> defined in variables.py 
# print("Producing histos:  {}".format([v._name for v in vars[1:]]))
# print("Regions:           {}".format(regions.keys()))

############### out folders  
folder = "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_triggerSF/"

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
var.append(variable(name = "PuppiMET_T1_pt_nominal", title= "p_{T}^{miss}(Puppi) [GeV]", nbins = 12, xarray = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "MHT", title= "MHT [GeV]", nbins = 6, xarray = np.array([0, 100, 200, 300, 400, 500, 1000], dtype = 'd')))#,xmin = 100, xmax=800))
var.append(variable(name = "PuppiMET_T1_phi_nominal", title= "Puppi MET #phi nominal", nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
var.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
var.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
var2d = [] 
var2d.append(variable2D(name = "PuppiMET_T1_pt_nominalVsMHT", xname = "PuppiMET_T1_pt_nominal", yname = "MHT", xtitle = "p_{T}^{miss}(Puppi) [GeV]", ytitle = "MHT [GeV]", nxbins = 12, xarray = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000], dtype = 'd'),  nybins = 6, yarray = np.array([0, 100, 200, 300, 400, 500, 1000], dtype = 'd')))

hlt_met = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hlt_ele = "(HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200)"

regions = {
    "orthogonalPreselR_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR2_Ntot"     :  hlt_ele +" && PuppiMET_T1_pt_nominal>100 && nTightElectron>0",
    "orthogonalPreselR2_Npass"    :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron>0",
    "orthogonalPreselR_CR"       :  hlt_ele+" && "+ hlt_met +" && PuppiMET_T1_pt_nominal>100 && MinDelta_phi>0.6 && nTightElectron==0"
}

infile      = {'Data': [], 'signal': [], 'bkg': []}
infile2D      = {'Data': [], 'signal': [], 'bkg': []}
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
            if len(var2d)>0:
                infile2D['Data'].append(ROOT.TFile.Open(repohisto + s.label + "_2D.root"))
        else:
            infile['bkg'].append(ROOT.TFile.Open(repohisto + s.label + ".root"))
            insample['bkg'].append(s)
            if len(var2d)>0:
                infile2D['bkg'].append(ROOT.TFile.Open(repohisto + s.label + "_2D.root"))
    
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
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
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
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
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

    # efficiencies histograms
    h_eff_data = h_data_pass.Clone("")
    h_eff_data.Divide(h_data_total)
    h_eff_bkg = h_bkg_pass.Clone("")
    h_eff_bkg.Divide(h_bkg_total)
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

    # plot
    plot(h_eff_data, repostack, ROOT.kBlack, "TriggerEff_"+v._name+"_eff_data", "Preliminary", 11, "13.6", str(lumi), "")
    plot(h_eff_bkg, repostack, ROOT.TColor.GetColor("#e42536"), "TriggerEff_"+v._name+"_eff_bkg", "Preliminary", 11, "13.6", str(lumi), "")
    plot([h_eff_data, h_eff_bkg], repostack, ROOT.TColor.GetColor("#e42536"), "TriggerEff_"+v._name+"_eff", "Preliminary", 11, "13.6", str(lumi), "")
    
    h_ratio = h_eff_bkg.Clone("")
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
    plot(h_ratio, repostack, ROOT.kBlack, "TriggerEff_"+v._name+"_SF", "Preliminary", 11, "13.6", str(lumi), "", ytitle="SF")

# Plots 2D
h_bkg_total    = None
h_data_total   = None
h_bkg_pass     = None
h_data_pass    = None

for v in var2d:
    r = "orthogonalPreselR_Ntot"
    for i, (f,s) in enumerate(zip(infile2D["bkg"], insample["bkg"])):
        tmp = copy.deepcopy(ROOT.TH2D(f.Get(v._name+"_"+r+"_"+cut_tag)))
        if len(samples[s.label][s.label]["ntot"]):
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_total==None:
            h_bkg_total = tmp.Clone("")
            h_bkg_total.SetName(v._name+"_"+r+"_bkgtotal")
        else:
            h_bkg_total.Add(tmp)
        
    for f, s in zip(infile2D["Data"], insample["Data"]):
        tmp = copy.deepcopy(f.Get(v._name+"_"+r+"_"+cut_tag))
        tmp.SetTitle("")
        if h_data_total==None:
            h_data_total = tmp.Clone("")
            h_data_total.SetName(v._name+"_"+r+"_datatotal")
        else:
            h_data_total.Add(tmp)

    r = "orthogonalPreselR_Npass"
    for i, (f,s) in enumerate(zip(infile2D["bkg"], insample["bkg"])):
        # print(v._name+"_"+r+"_"+cut_tag)
        tmp = copy.deepcopy(ROOT.TH2D(f.Get(v._name+"_"+r+"_"+cut_tag)))
        if len(samples[s.label][s.label]["ntot"]):
            # tmp.Scale(s.sigma*(10**3)*lumi/np.sum(samples[s.label][s.label]["ntot"]))
            tmp.Scale(lumi)
        else:
            continue
        tmp.SetTitle("")
        if h_bkg_pass==None:
            h_bkg_pass = tmp.Clone("")
            h_bkg_pass.SetName(v._name+"_"+r+"_bkgpass")
        else:
            h_bkg_pass.Add(tmp)
        
    for f, s in zip(infile2D["Data"], insample["Data"]):
        tmp = copy.deepcopy(f.Get(v._name+"_"+r+"_"+cut_tag))
        tmp.SetTitle("")
        if h_data_pass==None:
            h_data_pass = tmp.Clone("")
            h_data_pass.SetName(v._name+"_"+r+"_datapass")
        else:
            h_data_pass.Add(tmp)
    # efficiencies histograms
    h_eff_data = h_data_pass.Clone("")
    h_eff_data.Divide(h_data_total)
    h_eff_bkg = h_bkg_pass.Clone("")
    h_eff_bkg.Divide(h_bkg_total)
    # plot
    print(type(h_eff_data))
    plot2D(h_eff_bkg, repostack, var2d[0], canv_name="TriggerEff_2Dplot_eff_bkg", extraTest="Preliminary", iPos=0, energy="13.6", lumi=str(lumi), addInfo="")
    plot2D(h_eff_data, repostack,var2d[0], canv_name="TriggerEff_2Dplot_eff_data", extraTest="Preliminary", iPos=0, energy="13.6", lumi=str(lumi), addInfo="")
    # SF
    h_ratio = h_eff_bkg.Clone("")
    h_ratio.Divide(h_eff_data)
    plot2D(h_ratio, repostack,var2d[0], canv_name="TriggerEff_2Dplot_SF", extraTest="Preliminary", iPos=0, energy="13.6", lumi=str(lumi), addInfo="", ztitle="SF")
