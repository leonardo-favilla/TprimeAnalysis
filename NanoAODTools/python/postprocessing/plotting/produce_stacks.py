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
import yaml
import optparse
import math

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)


usage                   = 'python3 produce_stacks.py --year_tag <year_tag>'
parser                  = optparse.OptionParser(usage)
parser.add_option("--year_tag",          dest="year_tag",         help="Year tag: 2022, 2022EE, 2023, 2023postBPix, Full2022, Full2023, Full2022_Full2023",       type="string")
(opt, args)             = parser.parse_args()
################## input parameters
extraText                           = "Work in Progress"
extraSpace                          = 0.1
iPos                                = 0                 # Position of the legend (0: top-right, 1: top-left, etc.)
cut                                 = requirements      # defined in variables.py
blind                               = False             # Set to True if you want to blind the data
scale_signals                       = config["plotting"]["scale_signals"]                # Scaling factor for the signals
year_tag                            = opt.year_tag

lumi_dict                           = config["plotting"]["lumi_dict"]
lumi_dict["Full2022"]               = lumi_dict["2022"] + lumi_dict["2022EE"]
lumi_dict["Full2023"]               = lumi_dict["2023"] + lumi_dict["2023postBPix"]
lumi_dict["Full2022_Full2023"]      = lumi_dict["Full2022"] + lumi_dict["Full2023"]


folder_dict                         = config["plotting"]["folder_dict"]
folder_www_dict                     = config["plotting"]["folder_www_dict"] 


datasets_dict                       = config["plotting"]["datasets_to_plot"]
datasets_dict["Full2022"]           = datasets_dict["2022"] + datasets_dict["2022EE"]
datasets_dict["Full2023"]           = datasets_dict["2023"] + datasets_dict["2023postBPix"]
datasets_dict["Full2022_Full2023"]  = datasets_dict["Full2022"] + datasets_dict["Full2023"]

json_file_dict                      = config["dict_samples"]
json_file_dict["2022EE"]            = json_file_dict["2022"]
json_file_dict["2023postBPix"]      = json_file_dict["2023"]

colors_bkg                          = ["#e42536", "#ffcc00", "#bebdb8", "#86c8dd", "#caeba5"]
style_signals_dict                  = {
                                        "T (0.7TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen,      "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kSolid},
                                        "T (1.0TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen+1,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashed},
                                        "T (1.8TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen+2,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDotted},
                                        "tDM (m_{#phi}=50 GeV, m_{#chi}=1 GeV)":    {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kSolid},
                                        "tDM (m_{#phi}=200 GeV, m_{#chi}=1 GeV)":   {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta+1,  "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashed},
                                        "tDM (m_{#phi}=500 GeV, m_{#chi}=1 GeV)":   {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta+2,  "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDotted},
                                        "tDM (m_{#phi}=1000 GeV, m_{#chi}=1 GeV)":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kMagenta+3,  "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashDotted},
                                    }
labels_dict                         = {
                                        "TT":               "t#bar{t}",
                                        "TW":               "tW",
                                        "QCD":              "QCD",
                                        "ZJetsToNuNu":      "Z (#nu#nu) + Jets",
                                        "WJets":            "W (#it{l}#nu) + Jets",
                                        "TprimeToTZ_700":   "T (0.7TeV) #rightarrow tZ",
                                        "TprimeToTZ_1000":  "T (1.0TeV) #rightarrow tZ",
                                        "TprimeToTZ_1800":  "T (1.8TeV) #rightarrow tZ",
                                        "tDM_mPhi50":       "tDM (m_{#phi}=50 GeV, m_{#chi}=1 GeV)",
                                        "tDM_mPhi200":      "tDM (m_{#phi}=200 GeV, m_{#chi}=1 GeV)",
                                        "tDM_mPhi500":      "tDM (m_{#phi}=500 GeV, m_{#chi}=1 GeV)",
                                        "tDM_mPhi1000":     "tDM (m_{#phi}=1000 GeV, m_{#chi}=1 GeV)",
                                    }

systematics_dict                        = config["plotting"]["systematics"]
systematics_dict["Full2022"]            = list(set(systematics_dict["2022"]) & set(systematics_dict["2022EE"]))
systematics_dict["Full2023"]            = list(set(systematics_dict["2023"]) & set(systematics_dict["2023postBPix"]))
systematics_dict["Full2022_Full2023"]   = list(set(systematics_dict["Full2022"]) & set(systematics_dict["Full2023"]))
systematics                             = [f"{syst}_{variation}" for syst in systematics_dict[year_tag] for variation in ["up", "down"]]
if len(systematics) == 0:
    systErr     = False
    print(f"No systematics to be added for year {year_tag}")
else:
    systErr     = True
    print(f"Systematics to be added for year {year_tag}: {systematics}")

if scale_signals != 1:
    style_signals_dict = {key+f" x{scale_signals}": style_signals_dict[key] for key in style_signals_dict}
    for key in labels_dict:
        if ("Tprime" in key) or ("tDM" in key):
            labels_dict[key] = labels_dict[key] + f" x{scale_signals}"





############### SETTINGS ############### 
tot_lumi        = lumi_dict[year_tag] # 9.451 (2023postBPix), 17.794 (2023), 34.3 (full2022), 7.87 (2022), 59.97 (2018)
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
if isinstance(json_file, list):                 # multiple json files, when combining years
    samples = {}
    for jf in json_file:
        with open(jf, "r") as file:
            samples.update(json.load(file))
elif isinstance(json_file, str):                # single json file, when running on a single era/year
    with open(json_file, "r") as file:
        samples = json.load(file)

print("Parameters setted")
print("year_tag         = {}".format(year_tag))
print("cut              = {}".format(cut))
print("lumi (fb)        = {}".format(str(tot_lumi)))
print("input datasets   = {}".format([sample_dict[d].label for d in datasets]))
print("blind            = {}".format(blind))

################# variables & regions definition --> defined in variables.py 
print("Producing histos:  {}".format([v._name for v in vars[1:]]))
print("Regions:           {}".format(regions.keys()))

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_").replace("<", "_l_")

###############################################
################## MAIN CODE ##################
###############################################
inFilePath          = {"Data": [], "signal": [], "bkg": []}
inFile              = {"Data": [], "signal": [], "bkg": []}
inSample            = {"Data": [], "signal": [], "bkg": []}
cut_tag             = cut_string(cut)

for dat in datasets:
    if "Tprime" in dat:
        continue
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
MT_T_xbins          = array.array('d', [500, 600, 700, 800, 1000, 1400, 2000])
PuppiMET_pt_xbins   = array.array('d', [250, 300, 350, 400, 450, 500, 600, 850])


# for v in vars:
# for v in [var for var in vars if var._name == "MT_T"]:
for v in [var for var in vars if var._name == "PuppiMET_T1_pt_nominal"]:
# for v in [var for var in vars if var._name in ["LeadingFatJetPt_msoftdrop", "FatJet_msoftdrop_nominal"]]:
# for v in [var for var in vars if var._name in ["MT_T", "PuppiMET_T1_pt_nominal"]]:
    # for r in regions.keys():
    # for r in ["SRTop"]:
    for r in ["AH"]:
        ###############################################
        ############ PreProcess Histograms ############
        ############ normalization to Lumi ############
        ###############################################
        ROOT.TH1.SetDefaultSumw2()
        histo_bkg_dict                  = {}
        histo_bkg_dict["nominal"]       = {
                                            "t#bar{t}":                 None,
                                            "tW":                       None,
                                            "QCD":                      None,
                                            "Z (#nu#nu) + Jets":        None,
                                            "W (#it{l}#nu) + Jets":     None
                                            }
        histo_bkg_dict["err_syst"]      = None
        histo_data                      = None
        histo_signals_dict              = {}

        # print(f"Processing variable {v._name} in region {r}")

        ##### Normalize Signals (Lumi) ######
        # print("Processing Signals")
        for i, (f,s) in enumerate(zip(inFile["signal"], inSample["signal"])):
            histo_name                          = v._name+"_"+r+"_"+"nominal"
            tmp                                 = None
            tmp                                 = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
            year_tag                            = s.label.split("_")[-1]
            lumi                                = lumi_dict[year_tag]
            if v._name == "MT_T":
                tmp_                            = tmp.Rebin(len(MT_T_xbins)-1, histo_name+"_", MT_T_xbins)
                tmp                             = copy.deepcopy(tmp_)
                tmp.SetName(histo_name)
            elif v._name == "PuppiMET_T1_pt_nominal":
                tmp_                            = tmp.Rebin(len(PuppiMET_pt_xbins)-1, histo_name+"_", PuppiMET_pt_xbins)
                tmp                             = copy.deepcopy(tmp_)
                tmp.SetName(histo_name)
            if len(samples[s.label][s.label]["ntot"]):
                tmp.Scale(lumi)
                tmp                             = copy.deepcopy(tmp)
            else:
                continue
            leg_label                           = labels_dict["_".join(s.label.split("_")[:2])]
            if scale_signals != 1:
                tmp.Scale(scale_signals)                                        # scale signals for better visibility in the stack plots
            if leg_label not in histo_signals_dict:
                histo_signals_dict[leg_label]   = copy.deepcopy(tmp)
            else:
                histo_signals_dict[leg_label].Add(copy.deepcopy(tmp))
        # print("Finished Processing Signals\n")

        ##### Normalize Backgrounds (Lumi) ######
        # print("Processing Backgrounds")
        # NOMINAL #
        err_dict_SystSampleBin              = {syst: {} for syst in systematics}
        for i, (f,s) in enumerate(zip(inFile["bkg"], inSample["bkg"])):
            histo_name                      = v._name+"_"+r+"_"+"nominal"
            tmp                             = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
            year_tag                        = s.label.split("_")[-1]
            lumi                            = lumi_dict[year_tag]
            if v._name == "MT_T":
                tmp_                        = tmp.Rebin(len(MT_T_xbins)-1, histo_name+"_", MT_T_xbins)
                tmp                         = copy.deepcopy(tmp_)
                tmp.SetName(histo_name)
            elif v._name == "PuppiMET_T1_pt_nominal":
                tmp_                        = tmp.Rebin(len(PuppiMET_pt_xbins)-1, histo_name+"_", PuppiMET_pt_xbins)
                tmp                         = copy.deepcopy(tmp_)
                tmp.SetName(histo_name)
            if len(samples[s.label][s.label]["ntot"]):
                tmp.Scale(lumi)
            else:
                continue
            tmp_nom                         = copy.deepcopy(tmp)
            nbins                           = tmp_nom.GetNbinsX()
            leg_label                       = labels_dict[s.process.split("_")[0]]
            if histo_bkg_dict["nominal"][leg_label] is None:
                histo_bkg_dict["nominal"][leg_label]   = copy.deepcopy(tmp_nom)
            else:
                histo_bkg_dict["nominal"][leg_label].Add(copy.deepcopy(tmp_nom))
            
            
            
            # SYSTEMATICS #
            for syst in systematics:
                err_dict_SystSampleBin[syst][s.label]     = []
                histo_name                  = v._name+"_"+r+"_"+syst
                tmp                         = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
                if v._name == "MT_T":
                    tmp_                    = tmp.Rebin(len(MT_T_xbins)-1, histo_name+"_", MT_T_xbins)
                    tmp                     = copy.deepcopy(tmp_)
                    tmp.SetName(histo_name)
                elif v._name == "PuppiMET_T1_pt_nominal":
                    tmp_                    = tmp.Rebin(len(PuppiMET_pt_xbins)-1, histo_name+"_", PuppiMET_pt_xbins)
                    tmp                     = copy.deepcopy(tmp_)
                    tmp.SetName(histo_name)
                if len(samples[s.label][s.label]["ntot"]):
                    tmp.Scale(lumi)
                else:
                    continue
                tmp_syst                    = copy.deepcopy(tmp)

                for bin in range(1, nbins+1):
                    value_nom               = tmp_nom.GetBinContent(bin)
                    value_syst              = tmp_syst.GetBinContent(bin)
                    err_dict_SystSampleBin[syst][s.label].append(value_nom - value_syst)
        
        # Combine systematic errors from different backgrounds in quadrature #
        errSyst_up                      = []
        errSyst_down                    = []
        err_dict_SystBin                = {}
        for syst in systematics:
            err_dict_SystBin[syst]      = []
            for bin in range(nbins):
                err_dict_SystBin[syst].append(math.hypot(*[err_dict_SystSampleBin[syst][s.label][bin] for s in inSample["bkg"]]))
        
        for bin in range(nbins):
            print(f"eyU in bin {bin} --> {[err_dict_SystSampleBin[syst][s.label][bin] for s in inSample['bkg'] for syst in systematics if 'up' in syst]}")
            print(f"eyD in bin {bin} --> {[err_dict_SystSampleBin[syst][s.label][bin] for s in inSample['bkg'] for syst in systematics if 'down' in syst]}")
            errSyst_up.append(math.hypot(*[err_dict_SystBin[syst][bin] for syst in systematics if "up" in syst]))
            errSyst_down.append(math.hypot(*[err_dict_SystBin[syst][bin] for syst in systematics if "down" in syst]))

        print(f"err_dict_SystSampleBin: {err_dict_SystSampleBin}")
        print(f"err_dict_SystBin:       {err_dict_SystBin}")
        print(f"errSyst_up:             {errSyst_up}")
        print(f"errSyst_down:           {errSyst_down}")

        histo_bkg_dict["err_syst"] = ROOT.TGraphAsymmErrors(nbins,
                                                            array.array("d", [tmp_nom.GetBinCenter(bin) for bin in range(1, nbins+1)]),
                                                            array.array("d", [0.0 for bin in range(nbins)]),
                                                            array.array("d", [tmp_nom.GetBinWidth(bin)/2.0 for bin in range(1, nbins+1)]),
                                                            array.array("d", [tmp_nom.GetBinWidth(bin)/2.0 for bin in range(1, nbins+1)]),
                                                            array.array("d", errSyst_up),
                                                            array.array("d", errSyst_down)
                                                            ) # n, x, y, exl, exh, eyl, eyh
        # print("Finished Processing Backgrounds\n")

        ##### Data #####
        # print("Processing Data")
        if (not blind) and ((not ("SR" in r) or ("SRTopLoose" in r)) or (("SR" in r) and not ("SRTop" in r))):
            if not v._MConly:
                histo_name                          = v._name+"_"+r
                for f, s in zip(inFile["Data"], inSample["Data"]):
                    tmp                             = copy.deepcopy(ROOT.TH1D(f.Get(histo_name)))
                    if v._name == "MT_T":
                        tmp_                        = tmp.Rebin(len(MT_T_xbins)-1, histo_name+"_", MT_T_xbins)
                        tmp                         = copy.deepcopy(tmp_)
                        tmp.SetName(histo_name)
                    elif v._name == "PuppiMET_T1_pt_nominal":
                        tmp_                        = tmp.Rebin(len(PuppiMET_pt_xbins)-1, histo_name+"_", PuppiMET_pt_xbins)
                        tmp                         = copy.deepcopy(tmp_)
                        tmp.SetName(histo_name)
                    if histo_data is None:
                        histo_data                  = copy.deepcopy(tmp)
                    else:
                        histo_data.Add(copy.deepcopy(tmp))
        # print("Finished Processing Data\n")


        ###############################
        ########## DRAW STEP ##########
        ###############################

        ##### Drawing Options ######
        if v._name in ["LeadingFatJetPt_msoftdrop", "FatJet_msoftdrop_nominal"]:
            # logy    = False
            logy    = False
        elif "SR" in r:
            # logy = False
            logy    = True
        else:
            logy    = True

        ##### X-axis ######
        xTitle              = v._title
        xMin                = v._xmin
        xMax                = v._xmax
        if "msoftdrop" in v._name:
            xMin            = 72
            xMax            = 108

        ##### Y-axis ######
        yTitle              = "Events"
        if (not blind) and not ("SR" in r) and (not v._MConly):
            yMax            = max(sum([histo_bkg_dict["nominal"][process].GetMaximum() for process in histo_bkg_dict["nominal"]]), histo_data.GetMaximum())
            if len(histo_signals_dict) != 0:
                yMin        = min([h.GetMinimum() for label,h in histo_signals_dict.items()])
            else:
                if logy:
                    yMin    = 1e-1
                else:
                    yMin    = 0
        
        else:
            yMax            = sum([histo_bkg_dict["nominal"][process].GetMaximum() for process in histo_bkg_dict["nominal"]])
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
        
        if v._name in ["LeadingFatJetPt_msoftdrop", "FatJet_msoftdrop_nominal"]:
            if r=="AH":
                yMax        = 1300
                yMin        = 0
            elif r=="AH1lWR":
                yMax        = 4000
                yMin        = 0
            elif r=="SL":
                yMax        = 1e4
                yMin        = 0
            elif r in ["SR", "AH0lZR"]:
                yMax        = 200
                yMin        = 0

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
                                                lumi                = tot_lumi,
                                                extraSpace          = extraSpace,
                                                iPos                = iPos,
                                                logy                = logy,
                                                repo                = repostack_www,
                                                colors_bkg          = colors_bkg,
                                                style_signals_dict  = style_signals_dict,
                                                systErr             = systErr
                                                )


print(histo_bkg_dict.keys())