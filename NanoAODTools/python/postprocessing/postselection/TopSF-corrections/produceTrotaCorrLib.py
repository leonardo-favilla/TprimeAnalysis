import json
import correctionlib.schemav2 as cs
import yaml
import sys
import os
import math
import optparse

script_folder           = os.path.dirname(os.path.abspath(__file__))

usage                   = "python3 produceTrotaCorrLib.py --era <era>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                                       help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      "--binning",                dest="binning",                     type=str,     default=f"{script_folder}/TrotaSF_binning.yaml",                      help="yaml file with the event categories used in each pT bin, per era and top category")
parser.add_option(      "--output",                 dest="output",                      type=str,     default="",                                                           help="Output correctionlib file, default: <era>/CorrLib_TrotaScaleFactors_<era>.json in this folder")
(opt, args)             = parser.parse_args()
era                     = opt.era
binningFilePath         = opt.binning
eraFolder               = f"{script_folder}/{era}"     # input json from postselection_prefitTopSF/extract_ScaleFactors.py and output correctionlib file
outFilePath             = opt.output if opt.output else f"{eraFolder}/CorrLib_TrotaScaleFactors_{era}.json"

pt_edges                = [0, 200, 400, 600, 1000]
event_categories        = ["pt0to200", "pt200to400", "pt400to600", "pt600to1000", "pt0to400", "pt400to1000"]   # same order as in extract_ScaleFactors.py
wp_cats                 = ["Loose", "LooseButNotTight", "Tight"]
channels                = ["pass", "fail"]

with open(binningFilePath, "r") as _f:
    binning             = yaml.safe_load(_f)[era]
print(f"Loaded binning for era {era} from {binningFilePath}")


def load_input_json(TopCat, inJsonName):
    inFilePath          = f"{eraFolder}/{inJsonName}_{era}_{TopCat}.json"
    print(f"Loading {inFilePath}")
    with open(inFilePath, "r") as json_file:
        return json.load(json_file)[TopCat]


def get_fitted_sf(sf_dict, wp_cat, TagCat, channel, evcat):
    """Loose or Tight SF (value, error) fitted in the event category evcat; (1.0, 0.0) if evcat is None"""
    if evcat is None:
        return 1.0, 0.0
    evcat_idx           = event_categories.index(evcat)
    value               = sf_dict[wp_cat][TagCat][channel]["value"][evcat_idx]
    error               = sf_dict[wp_cat][TagCat][channel]["error"][evcat_idx]
    if value == 9999.0:
        print(f"ERROR: {wp_cat} {TagCat} {channel} SF missing (9999) for {evcat}: fit not available, choose another event category in {binningFilePath}")
        sys.exit(1)
    return value, error


def get_LooseButNotTight_sf(sf_dict, eff_dict, TagCat, channel, evcat):
    """
    LooseButNotTight SF (value, error) from the Loose and Tight SFs and n_pass of the same event category evcat:
        SF_LBNT     = (SF_L * n_L - SF_T * n_T) / (n_L - n_T)
        sigma_LBNT  = sqrt((sigma_L * n_L)^2 + (sigma_T * n_T)^2) / |n_L - n_T|
    (1.0, 0.0) if evcat is None, for the fail channel, if n_L == n_T, or if SF_LBNT <= 0
    """
    if (evcat is None) or (channel == "fail"):
        return 1.0, 0.0
    evcat_idx           = event_categories.index(evcat)
    sf_L, error_L       = get_fitted_sf(sf_dict, "Loose", TagCat, "pass", evcat)
    sf_T, error_T       = get_fitted_sf(sf_dict, "Tight", TagCat, "pass", evcat)
    n_L                 = eff_dict["Loose"][TagCat]["n_pass"][evcat_idx]
    n_T                 = eff_dict["Tight"][TagCat]["n_pass"][evcat_idx]
    if n_L == n_T:
        print(f"Warning: LooseButNotTight {TagCat} {evcat}: n_pass Loose = n_pass Tight = {n_L}, SF set to 1.0 +- 0.0")
        return 1.0, 0.0
    value               = (sf_L * n_L - sf_T * n_T) / (n_L - n_T)
    error               = math.sqrt((error_L * n_L)**2 + (error_T * n_T)**2) / abs(n_L - n_T)
    if value <= 0:
        # negative SF set to 1 (no correction), according to BTV recommendations: https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/#scale-factor-recommendations-for-event-reweighting
        print(f"Warning: LooseButNotTight {TagCat} {evcat}: SF = {value:.4f} +- {error:.4f} <= 0, set to 1.0 +- 0.0")
        return 1.0, 0.0
    return value, error


def produce_TrotaScaleFactors_dict():
    """TrotaScaleFactors_dict[TopCat][wp_cat][TagCat][channel] = {"value": [one per pT bin], "error": [one per pT bin]}"""
    TrotaScaleFactors_dict = {}
    for TopCat in binning.keys():
        evcats_used     = [evcat for TagCat in binning[TopCat].keys() for evcat in binning[TopCat][TagCat] if evcat is not None]
        if evcats_used:
            sf_dict     = load_input_json(TopCat, "TrotaScaleFactors")
            eff_dict    = load_input_json(TopCat, "TrotaEfficiencies")
        else:
            print(f"{TopCat}: all pT bins null in {binningFilePath}, SFs set to 1.0 +- 0.0 (no input json needed)")
            sf_dict     = None
            eff_dict    = None
        TrotaScaleFactors_dict[TopCat] = {}
        for wp_cat in wp_cats:
            TrotaScaleFactors_dict[TopCat][wp_cat] = {}
            for TagCat in binning[TopCat].keys():
                TrotaScaleFactors_dict[TopCat][wp_cat][TagCat] = {}
                for channel in channels:
                    values      = []
                    errors      = []
                    for evcat in binning[TopCat][TagCat]:
                        if wp_cat == "LooseButNotTight":
                            value, error = get_LooseButNotTight_sf(sf_dict, eff_dict, TagCat, channel, evcat)
                        else:
                            value, error = get_fitted_sf(sf_dict, wp_cat, TagCat, channel, evcat)
                        values.append(value)
                        errors.append(error)
                    TrotaScaleFactors_dict[TopCat][wp_cat][TagCat][channel] = {
                        "value": values,
                        "error": errors,
                    }
    return TrotaScaleFactors_dict


def make_topcat_content(TrotaScaleFactors_dict, TopCat):
    return {
        "key": TopCat,
        "value": cs.Category(
            nodetype="category",
            input="wp_cat",
            content=[
                {
                    "key": wp_cat,
                    "value": cs.Category(
                        nodetype="category",
                        input="TagCat",
                        content=[
                            {
                                "key": TagCat,
                                "value": cs.Category(
                                    nodetype="category",
                                    input="channel",
                                    content=[
                                        {
                                            "key": channel,
                                            "value": cs.Category(
                                                nodetype="category",
                                                input="type",
                                                content=[
                                                    {
                                                        "key": "value",
                                                        "value": cs.Binning(
                                                            nodetype="binning",
                                                            input="TopCandidate_pt",
                                                            edges=pt_edges,
                                                            content=TrotaScaleFactors_dict[TopCat][wp_cat][TagCat][channel]["value"],
                                                            flow="clamp",
                                                        ),
                                                    },
                                                    {
                                                        "key": "error",
                                                        "value": cs.Binning(
                                                            nodetype="binning",
                                                            input="TopCandidate_pt",
                                                            edges=pt_edges,
                                                            content=TrotaScaleFactors_dict[TopCat][wp_cat][TagCat][channel]["error"],
                                                            flow="clamp",
                                                        ),
                                                    },
                                                ],
                                            ),
                                        }
                                        for channel in TrotaScaleFactors_dict[TopCat][wp_cat][TagCat].keys()
                                    ],
                                ),
                            }
                            for TagCat in TrotaScaleFactors_dict[TopCat][wp_cat].keys()
                        ],
                    ),
                }
                for wp_cat in TrotaScaleFactors_dict[TopCat].keys()
            ],
        ).dict(),
    }


def make_correction_set(TrotaScaleFactors_dict):
    corr = cs.Correction(
        name="TrotaScaleFactors",
        version=1,
        inputs=[
            cs.Variable(name="TopCat",          type="string", description="Top category: Resolved, Mixed, Merged"),
            cs.Variable(name="wp_cat",          type="string", description="working point category: Loose, LooseButNotTight, Tight"),
            cs.Variable(name="TagCat",          type="string", description="Tag category: topmatched, nonmatched, other"),
            cs.Variable(name="channel",         type="string", description="insert: pass, fail"),
            cs.Variable(name="type",            type="string", description="insert: value, error"),
            cs.Variable(name="TopCandidate_pt", type="real",   description="Top candidate pt"),
        ],
        output=cs.Variable(
            name="TrotaScaleFactor",
            type="real",
            description="Trota Top tagger scale factor",
        ),
        data=cs.Category(
            nodetype="category",
            input="TopCat",
            content=[
                make_topcat_content(TrotaScaleFactors_dict, TopCat)
                for TopCat in TrotaScaleFactors_dict.keys()
            ],
        ),
    )

    cset = cs.CorrectionSet(schema_version=2, corrections=[corr])
    return cset.dict()


TrotaScaleFactors_dict  = produce_TrotaScaleFactors_dict()
cset_dict               = make_correction_set(TrotaScaleFactors_dict)
with open(outFilePath, "w") as f:
    json.dump(cset_dict, f, indent=2)
print(f"Saved correctionlib file: {outFilePath}")
