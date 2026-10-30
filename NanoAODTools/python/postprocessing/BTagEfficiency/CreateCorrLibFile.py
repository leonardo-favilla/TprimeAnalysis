import os
import sys
import json
import math
import optparse
import yaml
import ROOT
import correctionlib.schemav2 as cs
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')

# Build the correctionlib json with the MC b-tagging efficiency maps from the histograms produced by postSelector.py.
# For each process group (TT, TW, QCD, ...) and for all the processes together ("inclusive"):
#   eff(wp, flavour, |eta|, pt) = BTagEff_<flavour>_<wp> / BTagEff_<flavour>_all
# Output corrections, with the BTV signature evaluate(wp, flav, abseta, pt) (https://gitlab.cern.ch/cms-analysis-corrections/BTV/examples):
#   <tagger>_efficiency_<process>   one per process group
#   <tagger>_efficiency             inclusive
#   <tagger>_efficiency_TT_TW_ZJetsToNuNu   inclusive of the processes with large statistics only (reference_processes):
#                                   the inclusive map is dominated by the large weights of the low-HT QCD samples
# Bins with no jets in a process take the inclusive efficiency.

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

usage                   = "python3 CreateCorrLibFile.py --era <era>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      '--era',            dest='era',             type=str,   default="2024",     help='Era: 2022, 2022EE, 2023, 2023postBPix, 2024')
parser.add_option(      '--plots_folder',   dest='plots_folder',    type=str,   default=None,       help='Folder with the postSelector.py histograms (default: btagEfficiency_results of the era in config.yaml + plots/)')
parser.add_option(      '--output',         dest='output',          type=str,   default=None,       help='Output json (default: BTagEfficiency_<era>.json in this folder)')
(opt, args)             = parser.parse_args()
era                     = opt.era
plots_folder            = opt.plots_folder if opt.plots_folder is not None else config["outputfolder"]["btagEfficiency_results"][era] + "plots/"
output                  = opt.output if opt.output is not None else f"BTagEfficiency_{era}.json"

# Same categories as in postSelector.py; tagger names as in the BTV json
flavours                = {"b": 5, "c": 4, "light": 0}
wps                     = ["L", "M", "T"]
tagger_dict             = {"2022": "particleNet", "2022EE": "particleNet", "2023": "particleNet", "2023postBPix": "particleNet", "2024": "UParTAK4"}
tagger                  = tagger_dict[era]

# Processes summed in the second inclusive map: large statistics and homogeneous weights
reference_processes     = ["TT", "TW", "ZJetsToNuNu"]
reference_group         = "_".join(reference_processes)

def get_era(s):
    # as in postSelector.py
    if s.year == 2022:
        return "2022EE" if getattr(s, "EE", 0) == 1 else "2022"
    if s.year == 2023:
        return "2023postBPix" if getattr(s, "EE", 0) == 1 else "2023"
    return str(s.year)


############# Sum the histograms of the samples per process group #############
histos = {}     # histos[process][histo name] = TH2D summed over the samples of the process
for file_name in sorted(os.listdir(plots_folder)):
    label = file_name.replace(".root", "")
    if label not in sample_dict or get_era(sample_dict[label]) != era:
        print(f"Skipping {file_name}: not a sample of era {era}")
        continue
    s           = sample_dict[label]
    process     = s.process.split("_")[0] if hasattr(s, "process") else s.label.split("_")[0]
    in_file     = ROOT.TFile.Open(plots_folder + file_name)
    groups      = [process, "inclusive"]
    if process in reference_processes:
        groups.append(reference_group)
    print(f"Adding {label} to {groups}")
    for group in groups:
        histos.setdefault(group, {})
        for flavour in flavours:
            for wp in ["all"] + wps:
                name = f"BTagEff_{flavour}_{wp}"
                h    = in_file.Get(name)
                if name not in histos[group]:
                    histos[group][name] = h.Clone(f"{name}_{group}")
                    histos[group][name].SetDirectory(0)
                else:
                    histos[group][name].Add(h)
    in_file.Close()

if "inclusive" not in histos:
    print(f"No histograms of era {era} found in {plots_folder}")
    sys.exit(1)


############# Efficiencies #############
def efficiency(group, flavour, wp, ix, iy):
    # pass/all in the bin, limited to [0, 1] (bins with very few jets and negative weights can go outside);
    # bins with no jets take the inclusive efficiency (0 if empty also there)
    n_all  = histos[group][f"BTagEff_{flavour}_all"].GetBinContent(ix, iy)
    n_pass = histos[group][f"BTagEff_{flavour}_{wp}"].GetBinContent(ix, iy)
    if n_all > 0:
        return min(max(n_pass / n_all, 0.), 1.)
    if group != "inclusive":
        return efficiency("inclusive", flavour, wp, ix, iy)
    return 0.

def effective_entries(group, flavour, ix, iy):
    # effective number of unweighted jets in the bin, to judge the statistics: n_eff = (sum w)^2 / sum w^2
    h       = histos[group][f"BTagEff_{flavour}_all"]
    sum_w   = h.GetBinContent(ix, iy)                                           # sum of the weights of all the jets in the bin
    sum_w2  = h.GetBinError(ix, iy)**2                                          # sum of the squared weights (the bin error is sqrt(sum w^2))
    return sum_w**2 / sum_w2 if sum_w2 > 0 else 0.

h_ref           = histos["inclusive"]["BTagEff_b_all"]
abseta_edges    = [h_ref.GetXaxis().GetBinLowEdge(ix) for ix in range(1, h_ref.GetNbinsX()+2)]
pt_edges        = [h_ref.GetYaxis().GetBinLowEdge(iy) for iy in range(1, h_ref.GetNbinsY()+2)]
n_abseta, n_pt  = len(abseta_edges)-1, len(pt_edges)-1


############# Print a summary: efficiency range and statistical precision per process, flavour and WP #############
print(f"\n{'process':12s} {'flavour':6s} {'wp':2s} {'eff min':>8s} {'eff max':>8s} {'max rel. stat. err':>18s} {'min eff. jets/bin':>18s}")
for group in histos:
    for flavour in flavours:
        n_eff = [effective_entries(group, flavour, ix, iy) for ix in range(1, n_abseta+1) for iy in range(1, n_pt+1)]
        for wp in wps:
            effs, rel_errs = [], []
            for ix in range(1, n_abseta+1):
                for iy in range(1, n_pt+1):
                    eff = efficiency(group, flavour, wp, ix, iy)
                    n   = effective_entries(group, flavour, ix, iy)
                    effs.append(eff)
                    if eff > 0 and n > 0:
                        rel_errs.append(math.sqrt(eff*(1-eff)/n) / eff)       # binomial error on eff
            max_rel_err = f"{max(rel_errs):.3f}" if rel_errs else "-"
            print(f"{group:12s} {flavour:6s} {wp:2s} {min(effs):8.4f} {max(effs):8.4f} {max_rel_err:>18s} {min(n_eff):18.0f}")


############# Write the correctionlib json #############
def efficiency_map(group):
    # Category wp -> Category flav -> Binning abseta -> Binning pt, as compute_btagging_efficiency in BTV lib/btag_sf.py
    return cs.Category(
        nodetype="category",
        input="wp",
        content=[
            {
                "key": wp,
                "value": cs.Category(
                    nodetype="category",
                    input="flav",
                    content=[
                        {
                            "key": flavour_id,
                            "value": cs.Binning(
                                nodetype="binning",
                                input="abseta",
                                edges=abseta_edges,
                                content=[
                                    cs.Binning(
                                        nodetype="binning",
                                        input="pt",
                                        edges=pt_edges,
                                        content=[efficiency(group, flavour, wp, ix, iy) for iy in range(1, n_pt+1)],
                                        flow="clamp"
                                    ) for ix in range(1, n_abseta+1)
                                ],
                                flow="clamp"
                            )
                        } for flavour, flavour_id in flavours.items()
                    ]
                )
            } for wp in wps
        ]
    )

corrections = []
for group in histos:
    name = f"{tagger}_efficiency" if group == "inclusive" else f"{tagger}_efficiency_{group}"
    corrections.append(cs.Correction(
        name=name,
        version=1,
        description=f"MC b-tagging efficiency of {tagger} for {group} ({era}), as a function of WP, jet hadron flavour, |eta| and pt",
        inputs=[
            cs.Variable(name="wp",      type="string",  description="Working point: L, M, T"),
            cs.Variable(name="flav",    type="int",     description="Jet hadron flavour: 0=udsg, 4=c, 5=b"),
            cs.Variable(name="abseta",  type="real",    description="Jet |eta|"),
            cs.Variable(name="pt",      type="real",    description="Jet pt [GeV]"),
        ],
        output=cs.Variable(name="efficiency", type="real", description="MC b-tagging efficiency"),
        data=efficiency_map(group)
    ))

cset = cs.CorrectionSet(schema_version=2, description=f"MC b-tagging efficiency maps ({era})", corrections=corrections)
with open(output, "w") as f:
    json.dump(cset.model_dump(exclude_unset=True), f, indent=2)
print(f"\nWritten {output} with corrections: {[c.name for c in corrections]}")
