import gzip
import json
import correctionlib

filename = "BTagEfficiency_2024.json"
btv_filename = "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-10-20/btagging.json.gz"
cset     = correctionlib.CorrectionSet.from_file(filename)

print("Available corrections:")
for name in cset:
    print(f"  {name}")


corr     = cset["UParTAK4_efficiency_TT"]
print(f"Name:        {corr.name}")
print(f"Version:     {corr.version}")
print(f"Description: {corr.description}")

print("Inputs:")
for variable in corr.inputs:
    print(
        f"  {variable.name:20s}"
        f"type={variable.type:8s}"
        f"description={variable.description}"
    )

print(
    f"Output: {corr.output.name} "
    f"({corr.output.type}) — {corr.output.description}"
)

eff_M_b_1p0_50  = corr.evaluate("M", 5, 1.0, 50.0)
eff_T_b_2p2_100 = corr.evaluate("T", 5, 2.2, 100.0)

print(f"Efficiency for Medium WP, b jet, |eta|=1.0, pT=50 GeV: {eff_M_b_1p0_50}")
print(f"Efficiency for Tight WP, b jet, |eta|=2.2, pT=100 GeV: {eff_T_b_2p2_100}")


def collect_edges(node, edges):
    # Walk the correction tree and collect the bin edges of every binning node, per input variable (e.g. abseta, pt).
    # Category nodes (systematic, working_point, flavor, ...) are walked through; for "systematic" only the central value.
    if not isinstance(node, dict):
        return
    if node.get("nodetype") == "binning":
        edges.setdefault(node["input"], set()).add(tuple(node["edges"]))
        for child in node["content"]:
            collect_edges(child, edges)
    elif node.get("nodetype") == "category":
        for item in node["content"]:
            if node["input"] == "systematic" and item["key"] != "central":
                continue
            collect_edges(item["value"], edges)

def print_edges(file_path):
    # Bin edges of all the corrections in a correctionlib json (.json or .json.gz)
    open_file = gzip.open if file_path.endswith(".gz") else open
    with open_file(file_path, "rt") as f:
        cset_json = json.load(f)
    print(f"\nBin edges in {file_path}:")
    for correction in cset_json["corrections"]:
        edges = {}
        collect_edges(correction["data"], edges)
        print(f"  {correction['name']}")
        for variable, variable_edges in edges.items():
            for e in sorted(variable_edges):
                print(f"    {variable:8s} {list(e)}")

print_edges(filename)
print_edges(btv_filename)