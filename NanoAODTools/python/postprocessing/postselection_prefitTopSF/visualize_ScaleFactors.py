import json
import argparse
import ROOT
import cmsstyle as CMS
import os
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

usage   = "python3 visualize_ScaleFactors.py <json_file> --TopCategory <TopCategory> --wp_cat <wp_cat> --channel <channel> --output <output_name>"
parser  = argparse.ArgumentParser(usage=usage, description="2D map (pT bin x tag category) of the Trota SFs, from the fitted SFs json "
                                                          "(TrotaScaleFactors_<era>_<TopCategory>.json, Loose/Tight, 6 event categories) "
                                                          "or from the applied correctionlib file (CorrLib_TrotaScaleFactors_<era>.json, also LooseButNotTight, 4 pT bins)")
parser.add_argument("json_file")
parser.add_argument("--TopCategory",    default="Mixed",    choices=["Resolved", "Mixed", "Merged"])
parser.add_argument("--wp_cat",         default="Loose",    choices=["Loose", "LooseButNotTight", "Tight"])
parser.add_argument("--channel",        default="pass",     choices=["pass", "fail"])
parser.add_argument("--output",         default="sf_map")
args = parser.parse_args()

matchings       = ["topmatched", "nonmatched", "other"]
ylabels         = ["topmatched", "nonmatched", "other"]


def get_block_from_fitted_json(data, TopCat, wp_cat):
    """block[TagCat][channel] = {"value": [...], "error": [...]} for the 6 event categories of extract_ScaleFactors.py"""
    if wp_cat not in data[TopCat]:
        raise SystemExit(f"{wp_cat} not in {args.json_file}: the fitted SFs json has only {list(data[TopCat].keys())}, LooseButNotTight is in the correctionlib file")
    xlabels     = ["[0,200[", "[200,400[", "[400,600[", "[600,1000)", "[0,400[", "[400,1000)"]   # pt0to200, pt200to400, pt400to600, pt600to1000, pt0to400, pt400to1000
    return data[TopCat][wp_cat], xlabels


def get_block_from_corrlib(data, TopCat, wp_cat):
    """block[TagCat][channel] = {"value": [...], "error": [...]} for the pT bins of the correctionlib file"""
    def child(node, key):
        return next(item["value"] for item in node["content"] if item["key"] == key)
    correction  = next(corr for corr in data["corrections"] if corr["name"] == "TrotaScaleFactors")
    wp_node     = child(child(correction["data"], TopCat), wp_cat)
    block       = {}
    for TagCat in matchings:
        block[TagCat] = {}
        for channel in ["pass", "fail"]:
            channel_node            = child(child(wp_node, TagCat), channel)
            block[TagCat][channel]  = {
                "value": child(channel_node, "value")["content"],
                "error": child(channel_node, "error")["content"],
            }
            edges   = child(channel_node, "value")["edges"]
    xlabels     = [f"[{edges[i]:g},{edges[i+1]:g}[" for i in range(len(edges)-2)] + [f"[{edges[-2]:g},{edges[-1]:g})"]
    return block, xlabels


with open(args.json_file) as f:
    data = json.load(f)
if "corrections" in data:
    block, xlabels  = get_block_from_corrlib(data, args.TopCategory, args.wp_cat)
else:
    block, xlabels  = get_block_from_fitted_json(data, args.TopCategory, args.wp_cat)

if not os.path.exists(os.path.dirname(args.output)):
    os.makedirs(os.path.dirname(args.output))


CMS.SetExtraText("Work in Progress")
CMS.SetLumi(None)    # no luminosity label (an empty string breaks cmsstyle 0.5.0)
c = CMS.cmsCanvas(
    "c",
    0, len(xlabels),
    0, len(ylabels),
    "",
    "",
    square=False,          # rectangular canvas (CMS.kRectangular not available in cmsstyle 0.5.0)
    iPos=0,
    with_z_axis=True
)
c.SetLeftMargin(0.18)    # this is the main fix: your y labels are being cut
c.SetRightMargin(0.16)   # leave room for the color palette
c.SetBottomMargin(0.18)

h = ROOT.TH2F("h", "", len(xlabels), 0, len(xlabels), len(ylabels), 0, len(ylabels))

for ix, lab in enumerate(xlabels, start=1):
    h.GetXaxis().SetBinLabel(ix, lab)

for iy, lab in enumerate(ylabels, start=1):
    h.GetYaxis().SetBinLabel(iy, lab)

# fitted SFs json: "other" is never fitted (empty lists), missing fits are 9999 -> bins left empty and labelled N/A
for iy, m in enumerate(matchings, start=1):
    values = block[m][args.channel]["value"]
    for ix in range(len(values)):
        if values[ix] != 9999.0:
            h.SetBinContent(ix + 1, iy, values[ix])

h.SetMinimum(0.0)
h.SetMaximum(2.0)

h.GetXaxis().SetTitle("p_{T} [GeV]")
h.GetXaxis().SetTitleOffset(1.3)
h.GetXaxis().SetTitleSize(0.05)
h.GetXaxis().SetLabelSize(0.045)

h.GetYaxis().SetTitleOffset(1.4)
h.GetYaxis().SetTitleSize(0.05)
h.GetYaxis().SetLabelSize(0.045)

h.GetZaxis().SetTitle(f"SF {args.TopCategory} {args.wp_cat} {args.channel}")
h.GetZaxis().SetTitleSize(0.045)
h.GetZaxis().SetLabelSize(0.045)

c.cd()
h.Draw("COLZ")

latex = ROOT.TLatex()
latex.SetTextAlign(22)
latex.SetTextSize(0.020)

for iy, m in enumerate(matchings, start=1):
    values = block[m][args.channel]["value"]
    errors = block[m][args.channel]["error"]
    for ix in range(len(xlabels)):
        if (ix >= len(values)) or (values[ix] == 9999.0):  # not fitted, or dummy value assigned for missing SFs
            content = "N/A"
        else:
            content = f"{values[ix]:.3f} #pm {errors[ix]:.3f}"
        latex.DrawLatex(ix + 0.5, iy - 0.5, content)

CMS.UpdatePalettePosition(h, c)
c.SaveAs(args.output + ".png")
c.SaveAs(args.output + ".pdf")
