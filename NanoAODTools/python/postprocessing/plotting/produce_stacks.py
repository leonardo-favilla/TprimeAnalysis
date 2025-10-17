#!/usr/bin/env python3
import ROOT
import os
import sys
sys.path.append('../')
from make_stack import make_stack_with_ratio
from samples.samples import *
from variables import *
import copy
import json
import numpy as np
import shutil
import cmsstyle as CMS
import array
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

################## input parameters
extraText       = "Work in Progress"
extraSpace      = 0.1
iPos            = 0                 # Position of the legend (0: top-right, 1: top-left, etc.)
cut             = requirements      # defined in variables.py
blind           = False             # Set to True if you want to blind the data
year_tag        = "2023"    # "2022", "2022EE", "2023", "2023postBPix"

lumi_dict       = {
                    "2018":                 59.97,
                    "2022":                 7.87,
                    "2022EE":               26.43,
                    "2023":                 17.794,
                    "2023postBPix":         9.451,
                }
lumi_dict["Full2022"]          = lumi_dict["2022"] + lumi_dict["2022EE"]
lumi_dict["Full2023"]          = lumi_dict["2023"] + lumi_dict["2023postBPix"]
lumi_dict["Full2022_Full2023"] = lumi_dict["Full2022"] + lumi_dict["Full2023"]


folder_dict     = {
                    "2022":                     "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_systematics/",
                    "2022EE":                   "/eos/home-a/acagnott/DarkMatter/nosynch/run2022EE_systematics/",

                    "2023":                     "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst/",
                    # "2023":                     "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_no_nloewcorrection/",
                    # "2023":                     "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_no_SFbtag/",
                    # "2023":                     "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_no_puWeight/",

                    "2023postBPix":             "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst/",
                    # "2023postBPix":             "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst_no_nloewcorrection/",
                    # "2023postBPix":             "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst_no_SFbtag/",
                    # "2023postBPix":             "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst_no_puWeight/",

                    "Full2022":                 ".", # Placeholder
                    "Full2023":                 ".", # Placeholder
                    "Full2022_Full2023":        "/eos/user/l/lfavilla/RDF_DManalysis/results/Full2022_Full2023_syst/",
                }


folder_www_dict = {
                    "2022":                     "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2022_syst/",
                    "2022EE":                   "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2022EE_syst/",

                    "2023":                     "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023_syst/",
                    # "2023":                     "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023_syst_no_nloewcorrection/",
                    # "2023":                     "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023_syst_no_SFbtag/",
                    # "2023":                     "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023_syst_no_puWeight/",

                    "2023postBPix":             "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023postBPix_syst/",
                    # "2023postBPix":             "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023postBPix_syst_no_nloewcorrection/",
                    # "2023postBPix":             "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023postBPix_syst_no_SFbtag/",
                    # "2023postBPix":             "/eos/user/l/lfavilla/www/RDF_DManalysis/results/run2023postBPix_syst_no_puWeight/",

                    "Full2022":                 "/eos/user/l/lfavilla/www/RDF_DManalysis/results/Full2022_syst/",
                    "Full2023":                 "/eos/user/l/lfavilla/www/RDF_DManalysis/results/Full2023_syst/",
                    "Full2022_Full2023":        "/eos/user/l/lfavilla/www/RDF_DManalysis/results/Full2022_Full2023_syst/",
                }


datasets_dict   = {
                    "2022":
                            [
                                "DataJetMET_2022",
                                "TT_2022",
                                "QCD_2022",
                                "ZJetsToNuNu_2jets_2022",
                                "WJets_2jets_2022",
                                # "tDM_mPhi50_mChi1_2022",
                                # "tDM_mPhi200_mChi1_2022",
                                # "tDM_mPhi500_mChi1_2022",
                                # "tDM_mPhi1000_mChi1_2022",
                                "TprimeToTZ_700_2022",
                                "TprimeToTZ_1000_2022",
                                "TprimeToTZ_1800_2022"
                            ],
                    "2022EE":
                            [
                                "DataJetMET_2022EE",
                                "TT_2022EE",
                                "QCD_2022EE",
                                "ZJetsToNuNu_2jets_2022EE",
                                "WJets_2jets_2022EE",
                                "TprimeToTZ_700_2022EE",
                                "TprimeToTZ_1000_2022EE",
                                "TprimeToTZ_1800_2022EE"
                            ],
                    "2023":
                            [
                                "DataJetMET_2023",
                                "TT_2023",
                                "QCD_2023",
                                "ZJetsToNuNu_2jets_2023",
                                "WJets_2jets_2023",
                                "TprimeToTZ_700_2023",
                                "TprimeToTZ_1000_2023",
                                "TprimeToTZ_1800_2023"
                            ],
                    "2023postBPix":
                            [
                                "DataJetMET_2023postBPix",
                                "TT_2023postBPix",
                                "QCD_2023postBPix",
                                "ZJetsToNuNu_2jets_2023postBPix",
                                "WJets_2jets_2023postBPix",
                                "TprimeToTZ_700_2023postBPix",
                                "TprimeToTZ_1000_2023postBPix",
                                "TprimeToTZ_1800_2023postBPix"
                            ],
                }
datasets_dict["Full2022"]          = datasets_dict["2022"] + datasets_dict["2022EE"]
datasets_dict["Full2023"]          = datasets_dict["2023"] + datasets_dict["2023postBPix"]
datasets_dict["Full2022_Full2023"] = datasets_dict["Full2022"] + datasets_dict["Full2023"]

json_file_dict  = {
                    "2018":                 "../samples/dict_samples.json",
                    "2022":                 "../samples/dict_samples_2022.json",
                    "2022EE":               "../samples/dict_samples_2022.json",
                    "2023":                 "../samples/dict_samples_2023.json",
                    "2023postBPix":         "../samples/dict_samples_2023.json",
                    "Full2022":             ".", # Placeholder
                    "Full2023":             ".", # Placeholder
                    "Full2022_Full2023":    "../samples/dict_samples_2023.json"
                }


colors_bkg          = ["#e42536", "#bebdb8", "#86c8dd", "#caeba5"]
style_signals_dict  = {
                        "T (0.7TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen,      "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kSolid},
                        "T (1.0TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen+1,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashed},
                        "T (1.8TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen+2,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDotted},
                        "tDM (m_{#phi}=50 GeV, m_{#chi}=1 GeV)":    {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kSolid},
                        "tDM (m_{#phi}=200 GeV, m_{#chi}=1 GeV)":   {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta+1,  "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashed},
                        "tDM (m_{#phi}=500 GeV, m_{#chi}=1 GeV)":   {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta+2,  "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDotted},
                        "tDM (m_{#phi}=1000 GeV, m_{#chi}=1 GeV)":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta+3,  "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashDotted},
                    }
labels_dict         = {
                        "TT":               "t#bar{t}",
                        "QCD":              "QCD",
                        "ZJetsToNuNu":      "Z (#nu#nu) + Jets",
                        "WJets":            "W (#it{l}#nu) + Jets",
                        "TprimeToTZ_700":   "T (0.7TeV) #rightarrow tZ",
                        "TprimeToTZ_1000":  "T (1.0TeV) #rightarrow tZ",
                        "TprimeToTZ_1800":  "T (1.8TeV) #rightarrow tZ",
                        "tDM_mPhi50":    "tDM (m_{#phi}=50 GeV, m_{#chi}=1 GeV)",
                        "tDM_mPhi200":   "tDM (m_{#phi}=200 GeV, m_{#chi}=1 GeV)",
                        "tDM_mPhi500":   "tDM (m_{#phi}=500 GeV, m_{#chi}=1 GeV)",
                        "tDM_mPhi1000":  "tDM (m_{#phi}=1000 GeV, m_{#chi}=1 GeV)",
                    }




############### SETTINGS ############### 
lumi            = lumi_dict[year_tag] # 9.451 (2023postBPix), 17.794 (2023), 34.3 (full2022), 7.87 (2022), 59.97 (2018)
json_file       = json_file_dict[year_tag]
datasets        = datasets_dict[year_tag]
run2            = False
run3            = not run2
folder          = folder_dict[year_tag]
folder_www      = folder_www_dict[year_tag]
repostack       = folder+"stacks/"
repostack_www   = folder_www+"stacks/"

if not os.path.exists(folder):
    os.mkdir(folder)
if not os.path.exists(repostack):
    os.mkdir(repostack)
    print("Created folders 'stacks' at ", folder)
if not os.path.exists(repostack+"/png"):
    os.mkdir(repostack+"/png")
if not os.path.exists(repostack+"/pdf"):
    os.mkdir(repostack+"/pdf")
if not os.path.exists(repostack+"/C"):
    os.mkdir(repostack+"/C")


if not os.path.exists(folder_www):
    os.mkdir(folder_www)
if not os.path.exists(repostack_www):
    os.mkdir(repostack_www)
    print("Created folder 'stacks' at ", folder_www)
if not os.path.exists(folder_www+"index.php"):
    shutil.copy("/eos/user/l/lfavilla/www/index.php", folder_www)
if not os.path.exists(repostack_www+"index.php"):
    shutil.copy("/eos/user/l/lfavilla/www/index.php", repostack_www)






# Load the JSON file
with open(json_file, "r") as file:     ##### Questo non ho capito a cosa serva
    samples = json.load(file)

print("Parameters setted")
print("cut              = {}".format(cut))
print("lumi (fb)        = {}".format(str(lumi)))
print("input datasets   = {}".format([sample_dict[d].label for d in datasets]))
print("blind            = {}".format(blind))

################# variables & regions definition --> defined in variables.py 
print("Producing histos:  {}".format([v._name for v in vars[1:]]))
print("Regions:           {}".format(regions.keys()))

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_").replace("<", "_l_")


################## MAIN CODE ##################
inFilePath          = {"Data": [], "signal": [], "bkg": []}
inFile              = {"Data": [], "signal": [], "bkg": []}
inSample            = {"Data": [], "signal": [], "bkg": []}
cut_tag             = cut_string(cut)

for dat in datasets:
    year_tag        = dat.split("_")[-1]
    folder_tmp      = folder_dict[year_tag]
    repohisto_tmp   = folder_tmp + "plots/"
    # repohisto_tmp   = folder_tmp + "plots_rescaled_to_lumi/"
    d               = sample_dict[dat]
    if hasattr(d, "components"):
        s_list      = d.components
    else:
        s_list      = [d]
    for s in s_list:
        if "Data" in s.label:
            inFilePath["Data"].append(repohisto_tmp + s.label + ".root")
            inFile["Data"].append(ROOT.TFile.Open(repohisto_tmp + s.label + ".root"))
            inSample["Data"].append(s)
        elif "tDM" in s.label or "Tp" in s.label:
            inFilePath["signal"].append(repohisto_tmp + s.label + ".root")
            inFile["signal"].append(ROOT.TFile.Open(repohisto_tmp + s.label + ".root"))
            inSample["signal"].append(s)
        else:
            inFilePath["bkg"].append(repohisto_tmp + s.label + ".root")
            inFile["bkg"].append(ROOT.TFile.Open(repohisto_tmp + s.label + ".root"))
            inSample["bkg"].append(s)


### rebinning for MT ###
MT_T_xbins = array.array('d', [500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1200, 1400, 1600, 2000])


for v in vars:
    for r in regions.keys():
        if year_tag in ["2022", "2022EE"] and ("Loose" in r):
            continue
    # for r in ["AH"]:
        ###############################################
        ############ PreProcess Histograms ############
        ############ normalization to Lumi ############
        ###############################################
        ROOT.TH1.SetDefaultSumw2()

        histo_bkg_dict      = {
                                "t#bar{t}":                 None,
                                "QCD":                      None,
                                "Z (#nu#nu) + Jets":        None,
                                "W (#it{l}#nu) + Jets":     None
                            }
        histo_data          = None
        histo_signals_dict  = {}


        ##### Normalize Signals (Lumi) ######
        for i, (f,s) in enumerate(zip(inFile["signal"], inSample["signal"])):
            # print(s.label)
            histo_name = v._name+"_"+r+"_"+"nominal"
            tmp                         = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
            if v._name == "MT_T":
                tmp                     = tmp.Rebin(len(MT_T_xbins)-1, histo_name, MT_T_xbins)
            if len(samples[s.label][s.label]["ntot"]):
                tmp.Scale(lumi)
            else:
                continue
            # histo_signals_dict["_".join(s.label.split("_")[:2])] = tmp.Clone(histo_name)
            # histo_signals_dict["_".join(s.label.split("_")[:2])] = copy.deepcopy(tmp)
            leg_label                   = labels_dict["_".join(s.label.split("_")[:2])]
            histo_signals_dict[leg_label] = copy.deepcopy(tmp)


            if leg_label not in histo_signals_dict:
                histo_signals_dict[leg_label]   = copy.deepcopy(tmp)
            else:
                histo_signals_dict[leg_label].Add(copy.deepcopy(tmp))

        ##### Normalize Backgrounds (Lumi) ######
        for i, (f,s) in enumerate(zip(inFile["bkg"], inSample["bkg"])):
            print(s.label)
            histo_name = v._name+"_"+r+"_"+"nominal"
            print(histo_name)
            tmp                         = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
            if v._name == "MT_T":
                tmp                     = tmp.Rebin(len(MT_T_xbins)-1, histo_name, MT_T_xbins)
            if len(samples[s.label][s.label]["ntot"]):
                tmp.Scale(lumi)
            else:
                continue

            if histo_bkg_dict[leg_label] is None:
                histo_bkg_dict[leg_label]   = copy.deepcopy(tmp)
            else:
                histo_bkg_dict[leg_label].Add(copy.deepcopy(tmp))

        
        ##### Data #####
        if (not blind) and not ("SR" in r):
            if not v._MConly:
                # print(v._name+"_"+r)
                histo_name = v._name+"_"+r
                if year_tag in ["2022", "2022EE"]:
                    histo_name += "_"
                for f, s in zip(inFile["Data"], inSample["Data"]):
                    # print(s.label)
                    tmp                 = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
                    if v._name == "MT_T":
                        tmp             = tmp.Rebin(len(MT_T_xbins)-1, histo_name, MT_T_xbins)
                    if histo_data is None:
                        histo_data          = copy.deepcopy(tmp)
                    else:
                        histo_data.Add(copy.deepcopy(tmp))


        # for label,h in histo_signals_dict.items():
        #     print(f"Signal {label} has {h.GetEntries()} entries")
        # for label,h in histo_bkg_dict.items():
        #     print(f"Background {label} has {h.GetEntries()} entries")
        # if histo_data is not None:
        #     print(f"Data has {histo_data.GetEntries()} entries")

        ###############################
        ########## DRAW STEP ##########
        ###############################

        ##### Drawing Options ######
        if "SR" in r:
            # logy = False
            logy = True
        else:
            logy = True

        ##### X-axis ######
        xTitle              = v._title
        xMin                = v._xmin
        xMax                = v._xmax

        ##### Y-axis ######
        yTitle              = "Events"
        if (not blind) and not ("SR" in r) and (not v._MConly):
            yMax            = max(sum([histo_bkg_dict[process].GetMaximum() for process in histo_bkg_dict]), histo_data.GetMaximum())
            if len(histo_signals_dict) != 0:
                yMin        = min([h.GetMinimum() for label,h in histo_signals_dict.items()])
            else:
                if logy:
                    yMin    = 1e-1
                else:
                    yMin    = 0
        
        else:
            yMax            = sum([histo_bkg_dict[process].GetMaximum() for process in histo_bkg_dict])
            if len(histo_signals_dict) != 0:
                yMin        = min([h.GetMinimum() for label,h in histo_signals_dict.items()])
            else:
                if logy:
                    yMin    = 1e-1
                else:
                    yMin    = 0

        if logy:
            yMax            = yMax*10000
            yMin            = yMin
        else:
            yMax            = yMax*1.6
            yMin            = yMin*0.5

        ##### Ratio Plot ######
        rTitle          = "Data / MC"
        rMin            = 0.0
        rMax            = 2.0


        ##### Drawing Stacks ######
        canv_name       = "canvas_"+v._name+"_"+r+"_"+"nominal"
        dicanv          = make_stack_with_ratio(
                                                canv_name           = canv_name,
                                                histo_bkg_dict      = histo_bkg_dict,
                                                histo_data          = histo_data,
                                                histo_signals_dict  = histo_signals_dict,
                                                region              = r,
                                                xMin                = xMin,
                                                xMax                = xMax,
                                                yMin                = yMin,
                                                yMax                = yMax,
                                                rMin                = rMin,
                                                rMax                = rMax,
                                                xTitle              = xTitle,
                                                yTitle              = yTitle,
                                                rTitle              = rTitle,
                                                extraText           = extraText,
                                                lumi                = lumi,
                                                extraSpace          = extraSpace,
                                                iPos                = iPos,
                                                logy                = logy,
                                                repo                = repostack_www,
                                                colors_bkg          = colors_bkg,
                                                style_signals_dict  = style_signals_dict,
                                                )