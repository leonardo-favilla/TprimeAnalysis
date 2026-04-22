import ROOT
import os
import json
import yaml
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

usage                   = "python3 extract_ScaleFactors.py --era <era> --region <region>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                   help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      "--region",                 dest="region",                      type=str,     default="MixedLooseButNotTight",                  help="SemiLep region to consider among: ResolvedLooseButNotTight, ResolvedTight, MixedLooseButNotTight, MixedTight, MergedLooseButNotTight, MergedTight")
(opt, args)             = parser.parse_args()
era                     = opt.era
region                  = opt.region
outputfolder            = config["TrotaScaleFactor"]["outputfolder"][era]
fit_variable            = config["TrotaScaleFactor"]["fit_variable"][region]
workspaceFolder         = f"{outputfolder}/workspace_{region}/{fit_variable}"
outFolder               = f"{outputfolder}/ScaleFactors_MT_W/"

if "Resolved" in region:
    cand                = "Resolved"
elif "Mixed" in region:
    cand                = "Mixed"
elif "Merged" in region:
    cand                = "Merged"

if "LooseButNotTight" in region:
    wp_cat              = "LooseButNotTight"
elif "Tight" in region:
    wp_cat              = "Tight"

outName                 = f"TrotaScaleFactors_{wp_cat}"
outJsonPath             = f"{outFolder}/{outName}.json"

categories              = ["topmatched", "nonmatched", "other"]
event_categories        = ["pt0to200", "pt200to400", "pt400to600", "pt600to1000"]

if not os.path.exists(outFolder):
    os.makedirs(outFolder)
if os.path.exists(outJsonPath):
    print(f"Output file {outJsonPath} already exists. Retrieving existing results.")
    with open(outJsonPath, "r") as json_file:
        sf_dict     = json.load(json_file)
else:
    print(f"Output file {outJsonPath} does not exist. Extracting scale factors from fit results.")
    sf_dict         = {}

if era in sf_dict:
    print(f"Era {era} already exists in the results. Overwriting existing scale factors for this era.")
else:
    sf_dict[era]        = {}
if cand in sf_dict[era]:
    print(f"Candidate {cand} already exists in the results for era {era}. Overwriting existing scale factors for this candidate.")
else:    
    sf_dict[era][cand]  = {}


for cat in categories:
    poi                     = f"SF_{cat}"
    sf_dict[era][cand][cat] = {}
    sf_dict[era][cand][cat]["pass"] = {
                                        "value": [],
                                        "error": []
                                    }
    sf_dict[era][cand][cat]["fail"] = {
                                        "value": [],
                                        "error": []
                                    }
    for evcat in event_categories:
        print(f"\nExtracting scale factors for event category: {evcat}")
        inFilePath      = f"{workspaceFolder}/fitDiagnostics_{evcat}.root"
        file            = ROOT.TFile.Open(inFilePath, "READ")
        fit             = file.Get("fit_s")                             # get the signal+background fit
        norm_prefit     = file.Get("norm_prefit")
        # fit.Print("v")

        sf              = fit.floatParsFinal().find(poi)
        total_data      = 0.0                                           # retrieve total DATA yield from the prefit shapes
        for channel in ["pass", "fail"]:
            data_graph  = file.Get(f"shapes_prefit/{channel}/data")
            dataY       = [data_graph.GetY()[i] for i in range(data_graph.GetN())]
            total_data  += sum(dataY)
        
        norm_factor     = fit.constPars().find("norm_match_mc_data")    # frozen rate parameter used to match the total MC yield to data
        if norm_factor:
            norm_factor_val = norm_factor.getVal()
            norm_factor_err = 0.0
        else:
            None

        ###############
        ### SF_pass ###
        ###############
        if sf:
            sf_pass_value = sf.getVal()
            sf_pass_error = sf.getError()
            sf_dict[era][cand][cat]["pass"]["value"].append(sf_pass_value)
            sf_dict[era][cand][cat]["pass"]["error"].append(sf_pass_error)
            print(f"{poi} \t\t= {sf_pass_value:.4f} ± {sf_pass_error:.4f}")
        else:
            print(f"{poi} not found in RooFitResult")

        ###############
        ### SF_fail ###
        ###############
        if sf:   
            norm_prefit_pass = norm_prefit.find(f"pass/{cat}").getVal()
            norm_prefit_fail = norm_prefit.find(f"fail/{cat}").getVal()
            print(f"Calculating w_fail for {evcat} using the relation:      w_fail = SF_fail    = 1 + (1 - SF_pass) * (norm_prefit_pass / norm_prefit_fail)")
            print(f"with error:                                             sigma_fail          = sigma_pass * (norm_prefit_pass / norm_prefit_fail)")
            print(f"where                                                   w_pass = SF_pass    = {sf_pass_value:.4f} ± {sf_pass_error:.4f}, norm_prefit_pass = {norm_prefit_pass:.4f}, norm_prefit_fail = {norm_prefit_fail:.4f}")
            sf_dict[era][cand][cat]["fail"]["value"].append(1 + (1 - sf_pass_value) * (norm_prefit_pass / norm_prefit_fail))
            sf_dict[era][cand][cat]["fail"]["error"].append(sf_pass_error * (norm_prefit_pass / norm_prefit_fail))
        else:
            print(f"{poi} not found in RooFitResult")



with open(outJsonPath, "w") as json_file:
    json.dump(sf_dict, json_file, indent=4)
    print(f"Scale factors saved to {outJsonPath}")