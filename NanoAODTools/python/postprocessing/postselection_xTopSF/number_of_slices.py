import yaml
import json
import optparse
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)


usage               = "python3 number_of_slices.py --year <year>"
parser              = optparse.OptionParser(usage)
parser.add_option(      "--year",           dest="year",      type=str,             default="2023",                                                                                                     help="Please enter the year of the samples to check, e.g. 2022, 2022EE, etc.")
(opt, args)         = parser.parse_args()
year                = opt.year




samples_list        = [
                        # "QCD",
                        "TT",
                        # "TW",
                        # "ZJetsToNuNu_2jets",
                        # "WJets_2jets",
                        # "DataJetMET",
                        # "DataMuon"
                    ]
components          = []

for s in samples_list:
    s = s+"_"+year
    if hasattr(sample_dict[s], "components"):
        components.extend([c.label for c in sample_dict[s].components])
    else:
        components.append(s)
print(components)  
        
#### LOAD dict_samples.py ####
dict_samples_file   = config["dict_samples"][year]
with open(dict_samples_file, "rb") as sample_file:
    samples         = json.load(sample_file)

for c in components:
    ### Determine number of slices per each component ###
    nfiles_max              = len(samples[c][c]["strings"])
    if nfiles_max < 200:
        nSlices             = 1
    elif nfiles_max < 500:
        nSlices             = 2
    elif nfiles_max < 1000:
        nSlices             = 4
    else:
        nSlices             = 6

    nFilesPerSlice          = nfiles_max // nSlices
    remainder               = nfiles_max % nSlices
    slices                  = []
    start                   = 0
    for i in range(nSlices):
        end                 = start + nFilesPerSlice + (1 if i < remainder else 0)
        slices.append([start, end])
        start               = end
    print(f"Component: {c:<50}  Number of files: {nfiles_max:<10}   Number of slices: {nSlices:<5}")
    print(f"Files splitting:    {slices}")
