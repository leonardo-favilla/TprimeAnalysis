import ROOT
import os
import json

workspaceFolder     = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/workspace_MixedLooseButNotTight"
era                 = "2023"
cand                = "Mixed"
outFolder           = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/ScaleFactors"
outName             = "TrotaScaleFactors_LooseButNotTight"
categories          = ["topmatched", "nonmatched", "other"]
event_categories    = ["pt0to200", "pt200to400", "pt400to600", "pt600to1000"]
outJsonPath         = f"{outFolder}/{outName}.json"

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
    sf_dict[era][cand][cat] = {
                                "value": [],
                                "error": []
                            }
    for evcat in event_categories:
        print(f"\nExtracting scale factors for event category: {evcat}")
        inFilePath      = f"{workspaceFolder}/fitDiagnostics_{evcat}.root"
        file            = ROOT.TFile.Open(inFilePath, "READ")
        fit             = file.Get("fit_s")  # get the signal+background fit
        # fit.Print("v")
        sf              = fit.floatParsFinal().find(poi)
        if sf:
            sf_dict[era][cand][cat]["value"].append(sf.getVal())
            sf_dict[era][cand][cat]["error"].append(sf.getError())
            print(f"{poi} \t\t= {sf.getVal():.4f} ± {sf.getError():.4f}")
        else:
            print(f"{poi} not found in RooFitResult")



with open(outJsonPath, "w") as json_file:
    json.dump(sf_dict, json_file, indent=4)
    print(f"Scale factors saved to {outJsonPath}")