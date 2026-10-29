import ROOT
import os
import json
import yaml
import optparse
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

usage                   = "python3 extract_ScaleFactors.py --era <era> --TopCategory <TopCategory> --wp_cat <wp_cat>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                   help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      '--TopCategory',            dest='TopCategory',                 type=str,     default="Mixed",                                  help='Top category for the histograms: Resolved, Mixed or Merged')
parser.add_option(      "--wp_cat",                 dest="wp_cat",                      type=str,     default="Tight",                                  help="Working point category to consider among: Loose, Tight (LooseButNotTight SFs are computed in the analysis from Loose/Tight SFs and efficiencies)")
(opt, args)             = parser.parse_args()
era                     = opt.era
TopCategory             = opt.TopCategory
wp_cat                  = opt.wp_cat
if wp_cat not in ["Loose", "Tight"]:
    print(f"Working point category {wp_cat} not valid: only Loose and Tight are fitted. LooseButNotTight SFs are computed in the analysis from Loose/Tight SFs and efficiencies.")
    sys.exit(1)
region                  = f"{TopCategory}{wp_cat}"
outputfolder            = config["TrotaScaleFactor"]["outputfolder"][TopCategory][era]
fit_variable            = config["TrotaScaleFactor"]["fit_variable"][region]
outFolder               = os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/../postselection/TopSF-corrections/{era}")   # versioned with the analysis, read by postselection/TopSF-corrections/produceTrotaCorrLib.py
outName                 = f"TrotaScaleFactors_{era}_{TopCategory}"
outJsonPath             = f"{outFolder}/{outName}.json"
outEffName              = f"TrotaEfficiencies_{era}_{TopCategory}"
outEffJsonPath          = f"{outFolder}/{outEffName}.json"

categories              = ["topmatched", "nonmatched", "other"]
event_categories        = ["pt0to200", "pt200to400", "pt400to600", "pt600to1000", "pt0to400", "pt400to1000"]
if not os.path.exists(outFolder):
    os.makedirs(outFolder)


if os.path.exists(outJsonPath):
    print(f"Output file {outJsonPath} already exists. Retrieving existing results.")
    with open(outJsonPath, "r") as json_file:
        sf_dict     = json.load(json_file)
else:
    print(f"Output file {outJsonPath} does not exist. Extracting scale factors from fit results.")
    sf_dict         = {}
if (TopCategory in sf_dict) and ("LooseButNotTight" in sf_dict[TopCategory]):
    print(f"Removing old LooseButNotTight scale factors of {TopCategory} from {outJsonPath}: they are computed in the analysis by produceTrotaCorrLib.py")
    del sf_dict[TopCategory]["LooseButNotTight"]
if TopCategory in sf_dict:
    print(f"Candidate {TopCategory} already exists in the results for era {era}. Overwriting existing scale factors for this candidate.")
else:    
    sf_dict[TopCategory]               = {}
if wp_cat in sf_dict[TopCategory]:
    print(f"Working point category {wp_cat} already exists in the results for candidate {TopCategory} and era {era}. Overwriting existing scale factors for this working point category.")
else:
    sf_dict[TopCategory][wp_cat]       = {}

# MC tagging efficiencies (prefit yields, efficiency = n_pass / n_total), needed in the analysis to compute the LooseButNotTight SFs
if os.path.exists(outEffJsonPath):
    print(f"Output file {outEffJsonPath} already exists. Retrieving existing results.")
    with open(outEffJsonPath, "r") as json_file:
        eff_dict    = json.load(json_file)
else:
    print(f"Output file {outEffJsonPath} does not exist. Extracting efficiencies from fit results.")
    eff_dict        = {}
if TopCategory not in eff_dict:
    eff_dict[TopCategory]              = {}
eff_dict[TopCategory][wp_cat]          = {}



for cat in categories:
    poi                         = f"SF_{cat}"
    sf_dict[TopCategory][wp_cat][cat]  = {}
    sf_dict[TopCategory][wp_cat][cat]["pass"] = {
                                        "value": [],
                                        "error": []
                                    }
    sf_dict[TopCategory][wp_cat][cat]["fail"] = {
                                        "value": [],
                                        "error": []
                                    }
    eff_dict[TopCategory][wp_cat][cat] = {
                                        "n_pass":       [],
                                        "n_total":      [],
                                        "efficiency":   []
                                    }
    if wp_cat in ["Loose", "Tight"]:
        event_categories_skipped    = []
        for evcat_idx, evcat in enumerate(event_categories):
            print(f"\nExtracting scale factors for event category: {evcat}")
            workspaceFolder = f"{outputfolder}/workspace_{wp_cat}/{fit_variable}"
            inFilePath      = f"{workspaceFolder}/fitDiagnostics_{evcat}.root"
            if not os.path.exists(inFilePath):
                print(f"Input file {inFilePath} not found. Skipping event category {evcat}.")
                event_categories_skipped.append(evcat)
                sf_dict[TopCategory][wp_cat][cat]["pass"]["value"].append(9999.0)  # assign a dummy value to indicate missing SF, to be treated as an outlier in the final analysis
                sf_dict[TopCategory][wp_cat][cat]["pass"]["error"].append(9999.0)  # assign a dummy error to indicate missing SF, to be treated as an outlier in the final analysis
                sf_dict[TopCategory][wp_cat][cat]["fail"]["value"].append(9999.0)  # assign a dummy value to indicate missing SF, to be treated as an outlier in the final analysis
                sf_dict[TopCategory][wp_cat][cat]["fail"]["error"].append(9999.0)  # assign a dummy error to indicate missing SF, to be treated as an outlier in the final analysis
                eff_dict[TopCategory][wp_cat][cat]["n_pass"].append(9999.0)
                eff_dict[TopCategory][wp_cat][cat]["n_total"].append(9999.0)
                eff_dict[TopCategory][wp_cat][cat]["efficiency"].append(9999.0)
                continue


            file            = ROOT.TFile.Open(inFilePath, "READ")
            fit             = file.Get("fit_s")                             # get the signal+background fit
            norm_prefit     = file.Get("norm_prefit")                       # prefit shapes/yields
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

                ######## Modifications due to low statistics ########
                # if (cat == "other"):
                #     sf_pass_value = 1.0
                #     sf_pass_error = 0.0
                # elif (TopCategory in ["Resolved", "Mixed"]) and (evcat == "pt600to1000"):
                #     sf_pass_value = 1.0
                #     sf_pass_error = 0.0
                # elif (TopCategory == "Merged") and (cat == "topmatched") and (evcat == "pt0to200"):
                #     sf_pass_value = 1.0
                #     sf_pass_error = 0.0

                sf_dict[TopCategory][wp_cat][cat]["pass"]["value"].append(sf_pass_value)
                sf_dict[TopCategory][wp_cat][cat]["pass"]["error"].append(sf_pass_error)
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
                sf_dict[TopCategory][wp_cat][cat]["fail"]["value"].append(1 + (1 - sf_pass_value) * (norm_prefit_pass / norm_prefit_fail))
                sf_dict[TopCategory][wp_cat][cat]["fail"]["error"].append(sf_pass_error * (norm_prefit_pass / norm_prefit_fail))

                eff_dict[TopCategory][wp_cat][cat]["n_pass"].append(norm_prefit_pass)
                eff_dict[TopCategory][wp_cat][cat]["n_total"].append(norm_prefit_pass + norm_prefit_fail)
                eff_dict[TopCategory][wp_cat][cat]["efficiency"].append(norm_prefit_pass / (norm_prefit_pass + norm_prefit_fail))
            else:
                print(f"{poi} not found in RooFitResult")



with open(outJsonPath, "w") as json_file:
    json.dump(sf_dict, json_file, indent=4)
    print(f"Scale factors saved to {outJsonPath}")
with open(outEffJsonPath, "w") as json_file:
    json.dump(eff_dict, json_file, indent=4)
    print(f"Efficiencies saved to {outEffJsonPath}")
