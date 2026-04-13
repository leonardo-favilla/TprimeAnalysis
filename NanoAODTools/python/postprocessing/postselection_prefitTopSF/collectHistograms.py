import ROOT
import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import yaml
import sys
import optparse

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)


usage                   = "python3 collectHistograms.py --era <era> --region <region>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                   help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      "--region",                 dest="region",                      type=str,     default="MixedLooseButNotTight",                  help="SemiLep region to consider among: ResolvedLooseButNotTight, ResolvedTight, MixedLooseButNotTight, MixedTight, MergedLooseButNotTight, MergedTight")
(opt, args)             = parser.parse_args()
era                     = opt.era
region                  = opt.region
outputfolder            = config["TrotaScaleFactor"]["outputfolder"][era]
fit_variable            = config["TrotaScaleFactor"]["fit_variable"][region]
plotsFolder             = f"{outputfolder}/plots/"
workspaceFolder         = f"{outputfolder}/workspace_{region}/"
workspaceSubFolder      = f"{workspaceFolder}/{fit_variable}/"

if not os.path.exists(workspaceFolder):
    os.makedirs(workspaceFolder)
    print(f"Created workspace folder: {workspaceFolder}")
if not os.path.exists(workspaceSubFolder):
    os.makedirs(workspaceSubFolder)
    print(f"Created workspace subfolder: {workspaceSubFolder}")

event_categories    = ["pt0to200","pt200to400","pt400to600","pt600to1000"]
uncertainties       = {
                        "lumi":         [1.013,"lnN"],
                        "pu":           [1,"factor"],
                        "jesTotal":     [1,"file"],
                        "jer":          [1,"file"]
                        }
uncertainties_tags  = {
                        "nominal":          "nominal",
                        "pu_up":            "puUp",
                        "pu_down":          "puDown",
                        "jesTotal_up":      "jesTotalUp",
                        "jesTotal_down":    "jesTotalDown",
                        "jer_up":           "jerUp",
                        "jer_down":         "jerDown"
                        }

tag_categories      = {
                        "data": {
                            "processes": ["DataMuon"]
                                },
                        "topmatched": {
                            "processes": ["TT","TW"]
                                        },
                        "nonmatched": {
                            "processes": ["TT","TW"]
                                        },
                        "other": {
                            "processes": ["QCD","ZJetsToNuNu_2jets","WJets_2jets"]
                                    }
                        }
processes   = [
                "DataMuon",
                "TT",
                "TW",
                "QCD",
                "ZJetsToNuNu_2jets",
                "WJets_2jets"
                ]
datasets    = [proc+"_"+era for proc in processes]
components  = []
for dataset_to_run in datasets:
    if hasattr(sample_dict[dataset_to_run], "components"):
        components.extend([c.label for c in sample_dict[dataset_to_run].components])
    else:
        components.extend(sample_dict[dataset_to_run].label)



inputHistograms_dict      = {}
for c in components:
    filepath    = plotsFolder + c + ".root"
    print(f"Opening {filepath}")
    f = ROOT.TFile.Open(filepath)

    if not f or f.IsZombie():
        print(f"Skipping bad file: {filepath}")
        continue

    inputHistograms_dict[c] = {}

    for key in f.GetListOfKeys():

        obj = key.ReadObj()

        # Only store histograms (optional filter)
        if isinstance(obj, ROOT.TH1):

            obj.SetDirectory(0)  # IMPORTANT: detach from file
            inputHistograms_dict[c][obj.GetName()] = obj

    f.Close()

# print(inputHistograms_dict.keys())
# print(inputHistograms_dict["DataMuonC1_0_2023"].keys())
# print(inputHistograms_dict["TT_semilep_2023"].keys())


outFile_dict            = {ev_cat: ROOT.TFile.Open(os.path.join(workspaceSubFolder, f"{ev_cat}.root"), "RECREATE") for ev_cat in event_categories}
outputHistograms_dict   = {}
outputCount_dict        = {}

for tag_cat in tag_categories:
    processes_in_cat    = tag_categories[tag_cat]["processes"]
    datasets_in_cat     = [proc+"_"+era for proc in processes_in_cat]
    components_in_cat   = []
    for dataset_in_cat in datasets_in_cat:
        if hasattr(sample_dict[dataset_in_cat], "components"):
            components_in_cat.extend([c.label for c in sample_dict[dataset_in_cat].components])
        else:
            components_in_cat.extend(sample_dict[dataset_in_cat].label)
    print(f"Tag category:   {tag_cat}")
    print(f"  Processes:    {processes_in_cat}")
    print(f"  Datasets:     {datasets_in_cat}")
    print(f"  Components:   {components_in_cat}")
    
    for ev_cat in event_categories:
        for pass_tag in ["pass", "fail"]:
            for unc,unc_tag in uncertainties_tags.items():
                if tag_cat == "data":
                    histoname       = f"{fit_variable}_SemiLep_{region}_{ev_cat}_{pass_tag}"
                    histoname_out   = f"{tag_cat}_{fit_variable}_{ev_cat}_{pass_tag}"
                    lumi            = 1.0
                else:
                    histoname       = f"{fit_variable}_SemiLep_{region}_{ev_cat}_{pass_tag}_{tag_cat}_{unc}"
                    histoname_out   = f"{tag_cat}_{fit_variable}_{ev_cat}_{pass_tag}_{unc_tag}"
                    lumi            = config["plotting"]["lumi_dict"][era]


                histo               = None
                for component in components_in_cat:
                    print(f"Looking for histogram: '{histoname}' in component: '{component}'")
                    if histoname in inputHistograms_dict[component]:
                        print(f"Found histogram: '{histoname}' in component: '{component}' with integral {inputHistograms_dict[component][histoname].Integral():.1f}")
                        if histo is None:
                            histo   = inputHistograms_dict[component][histoname].Clone(histoname)
                        else:
                            histo.Add(inputHistograms_dict[component][histoname])
                        print(f"Current integral for '{histoname_out}': {histo.Integral():.1f}")

                histo.Scale(lumi)
                histo.SetName(histoname_out)
                outputHistograms_dict[histoname_out]    = histo.Clone(histoname_out)
                outputCount_dict[histoname_out]         = outputHistograms_dict[histoname_out].Integral()
                print(f"Final integral for '{histoname_out}': {outputCount_dict[histoname_out]:.1f}")
                if tag_cat == "data":
                    break
                else:
                    continue
for key in outputHistograms_dict.keys():
    print(f"{key}: {outputCount_dict[key]:.1f}")



summaryCount_dict = {ev_cat: None for ev_cat in event_categories}

for ev_cat in event_categories:
    data_pass_count = 0
    data_fail_count = 0
    mc_pass_count   = 0
    mc_fail_count   = 0
    summaryCount_dict[ev_cat] = {
                                    "data_pass":                        0,
                                    "data_fail":                        0,
                                    "mc_pass":                          0,
                                    "mc_fail":                          0,
                                    "norm_match_mc_to_data":            0
                                }
    for tag_cat in tag_categories:
        for pass_tag in ["pass", "fail"]:
            histoname       = f"{tag_cat}_{fit_variable}_{ev_cat}_{pass_tag}"
            if not "data" in histoname:
                histoname   += "_nominal"
            count           = outputCount_dict[histoname]
            

            if "data" in histoname:
                if "pass" in histoname:
                    data_pass_count += count
                elif "fail" in histoname:
                    data_fail_count += count
            else:
                if "pass" in histoname:
                    mc_pass_count += count
                elif "fail" in histoname:
                    mc_fail_count += count
    
    norm_match_mc_to_data = (data_pass_count + data_fail_count) / (mc_pass_count + mc_fail_count)
    

    summaryCount_dict[ev_cat] = {
                                    "data_pass":                        data_pass_count,
                                    "data_fail":                        data_fail_count,
                                    "mc_pass":                          mc_pass_count,
                                    "mc_fail":                          mc_fail_count,
                                    "norm_match_mc_to_data":            norm_match_mc_to_data
                                }



for ev_cat, outFile in outFile_dict.items():
    outFile.cd()
    for histoname_out, histo in outputHistograms_dict.items():
        if ev_cat in histoname_out:
            histo.Write()
    outFile.Close()
    
with open(os.path.join(workspaceSubFolder, "histogram_counts.txt"), "w") as count_file:
    for ev_cat, summary in summaryCount_dict.items():
        count_file.write(f"Event category:              {ev_cat}\n")
        count_file.write(f"     Data pass count:        {summary['data_pass']:.1f}\n")
        count_file.write(f"     Data fail count:        {summary['data_fail']:.1f}\n")
        count_file.write(f"     MC pass count:          {summary['mc_pass']:.1f}\n")
        count_file.write(f"     MC fail count:          {summary['mc_fail']:.1f}\n")
        count_file.write(f"     Norm factor (data/mc):  {summary['norm_match_mc_to_data']:.4f}\n\n")
    for histoname, count in outputCount_dict.items():
        if ("data" in histoname) or ("nominal" in histoname):
            count_file.write(f"{histoname}: {count}\n")
# print(outFile_dict.keys())
# print(outputHistograms_dict.keys())

categories_to_plot   = ["topmatched", "nonmatched", "other"]
number_of_categories = len(categories_to_plot)
print(f"Folder with datacards and workspaces: {workspaceSubFolder}")
for ev_cat in event_categories:
    print(f"Printing datacard {ev_cat}.txt")
    with open(f"{workspaceSubFolder}/{ev_cat}.txt", 'w') as combine_card_file:
        combine_lines = []
        
        combine_lines.append("imax 2 (two channels, pass and fail)\n")
        combine_lines.append(f"jmax {number_of_categories-1} ({number_of_categories} categories minus 1)\n")
        combine_lines.append("kmax * (automatic number of nuisance parameters)\n")
        combine_lines.append("----------\n")

        combine_lines.append(f"shapes data_obs pass {workspaceSubFolder}/{ev_cat}.root data_{fit_variable}_{ev_cat}_pass\n")
        combine_lines.append(f"shapes * pass {workspaceSubFolder}/{ev_cat}.root $PROCESS_{fit_variable}_{ev_cat}_pass_nominal $PROCESS_{fit_variable}_{ev_cat}_pass_$SYSTEMATIC\n")
        combine_lines.append(f"shapes data_obs fail {workspaceSubFolder}/{ev_cat}.root data_{fit_variable}_{ev_cat}_fail\n")
        combine_lines.append(f"shapes * fail {workspaceSubFolder}/{ev_cat}.root $PROCESS_{fit_variable}_{ev_cat}_fail_nominal $PROCESS_{fit_variable}_{ev_cat}_fail_$SYSTEMATIC\n")
        combine_lines.append("----------\n")

        combine_lines.append("bin\tpass\tfail\n")
        combine_lines.append(f"observation\t{summaryCount_dict[ev_cat]['data_pass']:.0f}\t{summaryCount_dict[ev_cat]['data_fail']:.0f}\n")
        combine_lines.append("----------\n")
        
        combine_lines.append("# automatic counting of MC events\n")
        combine_lines.append("bin\t" + "pass\t"*number_of_categories + "fail\t"*number_of_categories + '\n')
        combine_lines.append("process\t"+'\t'.join(list(categories_to_plot)*2) + '\n')
        combine_lines.append("process\t"+'\t'.join(list(map(str, range(number_of_categories)))*2) + '\n')
        combine_lines.append("rate\t"+"-1\t"*number_of_categories*2 + '\n')
        combine_lines.append("----------\n")
        
        for unc,(unc_size,unc_mode) in uncertainties.items():
            unc_line        = unc + '\t'
            if unc_mode in ["factor", "file"]: 
                unc_line    += "shape\t"
            else: 
                unc_line    += unc_mode + '\t'
                            
            combine_lines.append(unc_line+'\t'.join([f"{unc_size}"]*number_of_categories*2)+'\n')
        combine_lines.append("# normalisation factor to match MC and data\n")
        combine_lines.append("# freezes automatically\n")
        combine_lines.append(f"norm_match_mc_data rateParam * * {summaryCount_dict[ev_cat]['norm_match_mc_to_data']:.6f}\n")
        combine_lines.append("nuisance edit freeze norm_match_mc_data\n")
        combine_lines.append("\n")
        combine_lines.append("# activating autoMCStats\n")
        combine_lines.append("* autoMCStats 0\n")
        
        combine_card_file.writelines(combine_lines)

print(f"Printing combine script file combine_script.sh")
with open(f"{workspaceSubFolder}/combine_script.sh", 'w') as combine_script_file:
    combine_script_file.write("#!/bin/bash\n")
    combine_script_file.write("# Converting datacards to workspace file for portability :-)\n")
    combine_script_file.write(f"cd {workspaceSubFolder}/\n")
    for ev_cat in event_categories:
        combine_script_file.write(f"text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe {ev_cat}.txt -o workspace_{ev_cat}.root --PO=categories={','.join(categories_to_plot)}\n")

print(f"Printing fit script file fit_procedure.sh")
with open(f"{workspaceSubFolder}/fit_procedure.sh", 'w') as fit_script_file:
    fit_script_file.write("#!/bin/bash\n")
    fit_script_file.write("# Running the fit procedure\n")
    fit_script_file.write("echo '[1/2] Running MultiDimFit'\n")
    fit_script_file.write(f"cd {workspaceSubFolder}/\n")
    for ev_cat in event_categories:
        fit_script_file.write(
                                f"combine -M MultiDimFit workspace_{ev_cat}.root \\\n"
                                f"    --redefineSignalPOIs {','.join(['SF_' + cat for cat in categories_to_plot])} \\\n"
                                f"    --name _{ev_cat}\n"
                                )
    fit_script_file.write("echo '[2/2] Running FitDiagnostics'\n")
    for ev_cat in event_categories:
        fit_script_file.write(
                                f"combine -M FitDiagnostics workspace_{ev_cat}.root \\\n"
                                f"    --redefineSignalPOIs {','.join(['SF_' + cat for cat in categories_to_plot])} \\\n"
                                f"    --saveShapes \\\n"
                                f"    --saveWithUncertainties \\\n"
                                f"    --name _{ev_cat}\n"
                                )