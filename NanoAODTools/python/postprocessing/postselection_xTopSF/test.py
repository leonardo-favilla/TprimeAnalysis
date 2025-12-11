import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import yaml
import json

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)



# in_dataset              = "QCD_HT800to1000_2022"
in_datasets             = [
                            "QCD_2023postBPix",
                            "TT_2023postBPix",
                            "TW_2023postBPix",
                            "WJets_2jets_2023postBPix",
                            "ZJetsToNuNu_2jets_2023postBPix",
                            "TprimeToTZ_700_2023postBPix",
                            "TprimeToTZ_1000_2023postBPix",
                            "TprimeToTZ_1800_2023postBPix"

                        ]
year                    = 2023
nfiles_max              = 100000
dict_samples_file       = config["dict_samples"][year]
with open(dict_samples_file, "rb") as sample_file:
    samples             = json.load(sample_file)

components_to_check     = []
for dataset_to_run in in_datasets:
    if hasattr(sample_dict[dataset_to_run], "components"):
        print("---------- Running dataset: ", dataset_to_run)
        print("Components: ", [s.label for s in sample_dict[dataset_to_run].components])
        components_to_check.extend([c.label for c in sample_dict[dataset_to_run].components])
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset_to_run)
        components_to_check.extend([sample_dict[dataset_to_run].label])
print(components_to_check)


for in_dataset in components_to_check:
    if "Data" not in in_dataset:
        ntot_list = samples[in_dataset][in_dataset]['ntot'][:nfiles_max]
        if None in ntot_list:
            print(f"Sample {in_dataset} has null entries in ntot, please check!")


in_dataset              = "WJets_2jets2J_2022EE"
if "Data" not in in_dataset:
    isMC                = True
    scenarios           = ["nominal", "jerUp", "jerDown", "jesUp", "jesDown"]
    xsecWeight          = sample_dict[in_dataset].sigma*10**3
    ntot_events         = np.sum(samples[in_dataset][in_dataset]['ntot'][:nfiles_max])
else:
    isMC                = False
    scenarios           = ["nominal"]
    xsecWeight          = 1.0
    ntot_events         = 1.0

print(isMC, scenarios, xsecWeight, ntot_events)