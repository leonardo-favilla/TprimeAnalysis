import ROOT
import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.variables import vars
import yaml
import sys

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)







plotsFolder     = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_Semilep_MixedLooseButNotTight_until010326/plots/"
workspaceFolder = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_Semilep_MixedLooseButNotTight_until010326/workspace/"
era             = "2023"
if not os.path.exists(workspaceFolder):
    os.makedirs(workspaceFolder)
    print(f"Created workspace folder: {workspaceFolder}")


event_categories    = ["pt0to200","pt200to400","pt400to600","pt600to1000"]
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

print(inputHistograms_dict.keys())
# print(inputHistograms_dict["DataMuonC1_0_2023"].keys())
# print(inputHistograms_dict["TT_semilep_2023"].keys())



outFile_dict            = {ev_cat: ROOT.TFile.Open(os.path.join(workspaceFolder, f"{ev_cat}.root"), "RECREATE") for ev_cat in event_categories}
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
    for var in vars:
        varname                                 = var._name
        for ev_cat in event_categories:
            for pass_tag in ["pass", "fail"]:
                for unc,unc_tag in uncertainties_tags.items():
                    histoname           = f"{tag_cat}_{varname}_{ev_cat}_{pass_tag}"
                    histoname_out       = f"{tag_cat}_{varname}_{ev_cat}_{pass_tag}"
                    if "data" in histoname:
                        lumi            = 1.0
                    else:
                        lumi            = config["plotting"]["lumi_dict"][era]
                        histoname       += f"_{unc}"
                        histoname_out   += f"_{unc_tag}"

                    histo               = None
                    for component in components_in_cat:
                        print(f"Looking for histogram: {histoname} in component: {component}")
                        if histoname in inputHistograms_dict[component]:
                            if histo is None:
                                histo   = inputHistograms_dict[component][histoname].Clone(histoname)
                            else:
                                histo.Add(inputHistograms_dict[component][histoname])

                    histo.Scale(lumi)
                    histo.SetName(histoname_out)
                    outputHistograms_dict[histoname_out]    = histo
                    outputCount_dict[histoname_out]         = histo.Integral()

for var in vars[0]:
    for ev_cat in event_categories:
        data_pass_count = 0
        data_fail_count = 0
        mc_pass_count   = 0
        mc_fail_count   = 0
        for tag_cat in tag_categories:
            for pass_tag in ["pass", "fail"]:
                histoname      = f"{tag_cat}_{var._name}_{ev_cat}_{pass_tag}_nominal"
                if histoname in outputCount_dict:
                    count = outputCount_dict[histoname]
                    if "data" in histoname:
                        if pass_tag == "pass":
                            data_pass_count += count
                        else:
                            data_fail_count += count
                    else:
                        if pass_tag == "pass":
                            mc_pass_count += count
                        else:
                            mc_fail_count += count

for histoname_out in outputHistograms_dict:
    outFile_dict[ev_cat].cd()
    outputHistograms_dict[histoname_out].Write()
    


for ev_cat, outFile in outFile_dict.items():
    outFile.Close()
    
with open(os.path.join(workspaceFolder, "histogram_counts.txt"), "w") as count_file:
    for histoname, count in outputCount_dict.items():
        if ("data" in histoname) or ("nominal" in histoname):
            count_file.write(f"{histoname}: {count}\n")
print(outFile_dict.keys())
print(outputHistograms_dict.keys())