import json
import correctionlib.schemav2 as cs
import yaml
import sys
import os
import math
import optparse

script_folder           = os.path.dirname(os.path.abspath(__file__))

# Two correctionlib files per era, read by postselection/postSelector.py (GetTrotaSF in postselection.h):
#   CorrLib_TrotaScaleFactors_<era>.json: fitted Loose, Tight, XTight SFs (pass and fail)
#   CorrLib_TrotaEfficiencies_<era>.json: MC efficiencies n_pass/n_total of Loose, Tight, XTight, from the prefit yields of the same fits
# The SFs of the tops passing a WP but not the tighter one (LooseButNotTight, TightButNotXTight) are computed in step 2
# from these SFs and efficiencies (BTV fixed-WP formula), not stored here.
usage                   = "python3 produceTrotaCorrLib.py --era <era>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                                       help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      "--binning",                dest="binning",                     type=str,     default=f"{script_folder}/TrotaSF_binning.yaml",                      help="yaml file with the event categories used in each pT bin, per era and top category")
parser.add_option(      "--output",                 dest="output",                      type=str,     default="",                                                           help="Output correctionlib file of the SFs, default: <era>/CorrLib_TrotaScaleFactors_<era>.json in this folder")
parser.add_option(      "--output_eff",             dest="output_eff",                  type=str,     default="",                                                           help="Output correctionlib file of the efficiencies, default: <era>/CorrLib_TrotaEfficiencies_<era>.json in this folder")
(opt, args)             = parser.parse_args()
era                     = opt.era
binningFilePath         = opt.binning
eraFolder               = f"{script_folder}/{era}"     # input json from postselection_prefitTopSF/extract_ScaleFactors.py and output correctionlib file
outFilePath             = opt.output if opt.output else f"{eraFolder}/CorrLib_TrotaScaleFactors_{era}.json"
outEffFilePath          = opt.output_eff if opt.output_eff else f"{eraFolder}/CorrLib_TrotaEfficiencies_{era}.json"

pt_edges                = [0, 200, 400, 600, 1000]
event_categories        = ["pt0to200", "pt200to400", "pt400to600", "pt600to1000", "pt0to400", "pt400to1000"]   # same order as in extract_ScaleFactors.py
wp_cats                 = ["Loose", "Tight", "XTight"]       # fitted WPs; LooseButNotTight and TightButNotXTight are computed in step 2
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
    """Loose, Tight or XTight SF (value, error) fitted in the event category evcat; (1.0, 0.0) if evcat is None"""
    if evcat is None:
        return 1.0, 0.0
    if wp_cat not in sf_dict:
        print(f"ERROR: {wp_cat} SFs not in the input json (fitted: {list(sf_dict.keys())}): fit {wp_cat} and run extract_ScaleFactors.py --wp_cat {wp_cat}")
        sys.exit(1)
    evcat_idx           = event_categories.index(evcat)
    value               = sf_dict[wp_cat][TagCat][channel]["value"][evcat_idx]
    error               = sf_dict[wp_cat][TagCat][channel]["error"][evcat_idx]
    if value == 9999.0:
        print(f"ERROR: {wp_cat} {TagCat} {channel} SF missing (9999) for {evcat}: fit not available, choose another event category in {binningFilePath}")
        sys.exit(1)
    return value, error


def get_efficiency(eff_dict, wp_cat, TagCat, evcat):
    """MC efficiency n_pass/n_total of wp_cat in the event category evcat (same prefit yields as the fit); -1 if evcat is None (null bin: SF 1 +- 0 in step 2)"""
    if evcat is None:
        return -1.0
    if wp_cat not in eff_dict:
        print(f"ERROR: {wp_cat} efficiencies not in the input json (fitted: {list(eff_dict.keys())}): fit {wp_cat} and run extract_ScaleFactors.py --wp_cat {wp_cat}")
        sys.exit(1)
    evcat_idx           = event_categories.index(evcat)
    efficiency          = eff_dict[wp_cat][TagCat]["efficiency"][evcat_idx]
    if efficiency == 9999.0:
        print(f"ERROR: {wp_cat} {TagCat} efficiency missing (9999) for {evcat}: fit not available, choose another event category in {binningFilePath}")
        sys.exit(1)
    return efficiency


def produce_TrotaScaleFactors_dict():
    """TrotaScaleFactors_dict[TopCat][wp_cat][TagCat][channel] = {"value": [one per pT bin], "error": [one per pT bin]}"""
    TrotaScaleFactors_dict = {}
    for TopCat in binning.keys():
        evcats_used     = [evcat for TagCat in binning[TopCat].keys() for evcat in binning[TopCat][TagCat] if evcat is not None]
        if evcats_used:
            sf_dict     = load_input_json(TopCat, "TrotaScaleFactors")
        else:
            print(f"{TopCat}: all pT bins null in {binningFilePath}, SFs set to 1.0 +- 0.0 (no input json needed)")
            sf_dict     = None
        TrotaScaleFactors_dict[TopCat] = {}
        for wp_cat in wp_cats:
            TrotaScaleFactors_dict[TopCat][wp_cat] = {}
            for TagCat in binning[TopCat].keys():
                TrotaScaleFactors_dict[TopCat][wp_cat][TagCat] = {}
                for channel in channels:
                    values      = []
                    errors      = []
                    for evcat in binning[TopCat][TagCat]:
                        value, error = get_fitted_sf(sf_dict, wp_cat, TagCat, channel, evcat)
                        values.append(value)
                        errors.append(error)
                    TrotaScaleFactors_dict[TopCat][wp_cat][TagCat][channel] = {
                        "value": values,
                        "error": errors,
                    }
    return TrotaScaleFactors_dict


def produce_TrotaEfficiencies_dict():
    """TrotaEfficiencies_dict[TopCat][wp_cat][TagCat] = [efficiency, one per pT bin] (-1 in the null bins)"""
    TrotaEfficiencies_dict = {}
    for TopCat in binning.keys():
        evcats_used     = [evcat for TagCat in binning[TopCat].keys() for evcat in binning[TopCat][TagCat] if evcat is not None]
        if evcats_used:
            eff_dict    = load_input_json(TopCat, "TrotaEfficiencies")
        else:
            print(f"{TopCat}: all pT bins null in {binningFilePath}, efficiencies set to -1 (no input json needed)")
            eff_dict    = None
        TrotaEfficiencies_dict[TopCat] = {}
        for wp_cat in wp_cats:
            TrotaEfficiencies_dict[TopCat][wp_cat] = {}
            for TagCat in binning[TopCat].keys():
                TrotaEfficiencies_dict[TopCat][wp_cat][TagCat] = [get_efficiency(eff_dict, wp_cat, TagCat, evcat) for evcat in binning[TopCat][TagCat]]
    return TrotaEfficiencies_dict


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
            cs.Variable(name="wp_cat",          type="string", description="working point category: Loose, Tight, XTight"),
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


def make_efficiency_correction_set(TrotaEfficiencies_dict):
    corr = cs.Correction(
        name="TrotaEfficiencies",
        version=1,
        inputs=[
            cs.Variable(name="TopCat",          type="string", description="Top category: Resolved, Mixed, Merged"),
            cs.Variable(name="wp_cat",          type="string", description="working point category: Loose, Tight, XTight"),
            cs.Variable(name="TagCat",          type="string", description="Tag category: topmatched, nonmatched, other"),
            cs.Variable(name="TopCandidate_pt", type="real",   description="Top candidate pt"),
        ],
        output=cs.Variable(
            name="TrotaEfficiency",
            type="real",
            description="MC efficiency n_pass/n_total of the Trota top tagger WP in the region of the fit (-1: null bin)",
        ),
        data=cs.Category(
            nodetype="category",
            input="TopCat",
            content=[
                {
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
                                            "value": cs.Binning(
                                                nodetype="binning",
                                                input="TopCandidate_pt",
                                                edges=pt_edges,
                                                content=TrotaEfficiencies_dict[TopCat][wp_cat][TagCat],
                                                flow="clamp",
                                            ),
                                        }
                                        for TagCat in TrotaEfficiencies_dict[TopCat][wp_cat].keys()
                                    ],
                                ),
                            }
                            for wp_cat in TrotaEfficiencies_dict[TopCat].keys()
                        ],
                    ),
                }
                for TopCat in TrotaEfficiencies_dict.keys()
            ],
        ),
    )

    cset = cs.CorrectionSet(schema_version=2, corrections=[corr])
    return cset.dict()


TrotaScaleFactors_dict  = produce_TrotaScaleFactors_dict()
TrotaEfficiencies_dict  = produce_TrotaEfficiencies_dict()

cset_dict               = make_correction_set(TrotaScaleFactors_dict)
with open(outFilePath, "w") as f:
    json.dump(cset_dict, f, indent=2)
print(f"Saved correctionlib file: {outFilePath}")

cset_eff_dict           = make_efficiency_correction_set(TrotaEfficiencies_dict)
with open(outEffFilePath, "w") as f:
    json.dump(cset_eff_dict, f, indent=2)
print(f"Saved correctionlib file: {outEffFilePath}")
