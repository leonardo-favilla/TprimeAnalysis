import os
import sys
import json
import yaml
import argparse
import ROOT
import cmsstyle as CMS
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# Plots of the Trota SFs and MC efficiencies of the Loose, Tight and XTight WPs of one era, as the b-tag efficiency plots
# (BTagEfficiency/plotEfficiencies.py), from postselection/TopSF-corrections/<era>/:
#   fitted/2D/   maps (pT bin x tag category) of the fitted SFs (pass, fail) and efficiencies, 6 event categories
#                (TrotaScaleFactors_<era>_<TopCategory>.json, TrotaEfficiencies_<era>_<TopCategory>.json of extract_ScaleFactors.py)
#   fitted/1D/   SF (pass, fail) and efficiency in the 6 event categories (0-200, 200-400, 400-600, 600-1000 | 0-400, 400-1000),
#                one bin of the same size each, the 3 WPs overlaid, one plot per top category and tag category
#   applied/2D/  maps of the SFs and efficiencies applied in step 2, 4 pT bins
#                (CorrLib_TrotaScaleFactors_<era>.json, CorrLib_TrotaEfficiencies_<era>.json of produceTrotaCorrLib.py)
#   applied/1D/  SF (pass, fail) and efficiency in the pT bins of the correctionlib files, the 3 WPs overlaid
#                (null bins of TrotaSF_binning.yaml: SF 1 +- 0 drawn as applied, efficiency -1 not drawn)
# Missing inputs (file, WP not fitted yet) are skipped with a warning.
# Output folder: --output, or <TrotaScaleFactor/folder_www/<era>>/ScaleFactors of config/config.yaml

usage   = "python3 visualize_ScaleFactors.py --era <era> [--input_folder <folder>] [--output <folder>]"
parser  = argparse.ArgumentParser(usage=usage)
parser.add_argument("--era",            default="2023")
parser.add_argument("--input_folder",   default=None,   help="default: ../postselection/TopSF-corrections/<era>")
parser.add_argument("--output",         default=None,   help="default: <TrotaScaleFactor/folder_www/<era>>/ScaleFactors of config/config.yaml")
args = parser.parse_args()
era             = args.era
input_folder    = args.input_folder if args.input_folder is not None else f"../postselection/TopSF-corrections/{era}"
if args.output is not None:
    output      = args.output
else:
    config_path = os.environ.get('PWD')+'/../config/config.yaml'
    config      = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as _f:
            config = yaml.safe_load(_f) or {}
    folder_www  = config.get("TrotaScaleFactor", {}).get("folder_www", {}).get(era, "")
    if not folder_www:
        print(f"Output folder not given: use --output or set TrotaScaleFactor/folder_www/{era} in {config_path}, exiting")
        sys.exit(1)
    output      = f"{folder_www}/ScaleFactors"

TopCategories   = ["Resolved", "Mixed", "Merged"]
wp_cats         = ["Loose", "Tight", "XTight"]
wp_colors       = {"Loose": ROOT.TColor.GetColor("#dc3428"), "Tight": ROOT.TColor.GetColor("#4cac58"), "XTight": ROOT.TColor.GetColor("#3f90da")}   # red, green, blue
wp_offsets      = {"Loose": -0.2, "Tight": 0.0, "XTight": 0.2}         # 1D plots: marker shifted by this fraction of the bin width, so the WPs do not overlap
channels        = ["pass", "fail"]
matchings       = ["topmatched", "nonmatched", "other"]

fitted_xlabels  = ["[0,200[", "[200,400[", "[400,600[", "[600,1000)", "[0,400[", "[400,1000)"]   # event categories of extract_ScaleFactors.py: pt0to200, pt200to400, pt400to600, pt600to1000, pt0to400, pt400to1000
fitted_n_exclusive = 4                                                                          # the first 4 are the exclusive pT bins, then the 2 wide ones


def is_missing(value):
    """9999: fit not available (fitted json); -1: null bin of TrotaSF_binning.yaml (efficiency correctionlib file)"""
    return value == 9999.0 or value == -1.0


def load_json(file_path):
    if not os.path.exists(file_path):
        print(f"WARNING: {file_path} not found, skipped")
        return None
    with open(file_path) as f:
        return json.load(f)


############# Values from the inputs: values[TagCat] = {"value": [one per bin], "error": [one per bin] or None} #############
def fitted_sf_values(sf_json, TopCat, wp_cat, channel):
    return {TagCat: {"value": sf_json[TopCat][wp_cat][TagCat][channel]["value"],
                     "error": sf_json[TopCat][wp_cat][TagCat][channel]["error"]} for TagCat in matchings}


def fitted_eff_values(eff_json, TopCat, wp_cat):
    return {TagCat: {"value": eff_json[TopCat][wp_cat][TagCat]["efficiency"],
                     "error": None} for TagCat in matchings}


def corrlib_child(node, key):
    return next(item["value"] for item in node["content"] if item["key"] == key)


def corrlib_keys(node):
    return [item["key"] for item in node["content"]]


def corrlib_xlabels(edges):
    return [f"[{edges[i]:g},{edges[i+1]:g}[" for i in range(len(edges)-2)] + [f"[{edges[-2]:g},{edges[-1]:g})"]


def applied_sf_values(sf_corrlib, TopCat, wp_cat, channel):
    """from the TrotaScaleFactors correction {TopCat, wp_cat, TagCat, channel, value/error, pt}; also returns the pT bin edges"""
    wp_node = corrlib_child(corrlib_child(sf_corrlib["data"], TopCat), wp_cat)
    values  = {}
    for TagCat in matchings:
        channel_node    = corrlib_child(corrlib_child(wp_node, TagCat), channel)
        values[TagCat]  = {"value": corrlib_child(channel_node, "value")["content"],
                           "error": corrlib_child(channel_node, "error")["content"]}
        edges           = corrlib_child(channel_node, "value")["edges"]
    return values, edges


def applied_eff_values(eff_corrlib, TopCat, wp_cat):
    """from the TrotaEfficiencies correction {TopCat, wp_cat, TagCat, pt}; also returns the pT bin edges"""
    wp_node = corrlib_child(corrlib_child(eff_corrlib["data"], TopCat), wp_cat)
    values  = {}
    for TagCat in matchings:
        binning_node    = corrlib_child(wp_node, TagCat)
        values[TagCat]  = {"value": binning_node["content"], "error": None}
        edges           = binning_node["edges"]
    return values, edges


############# Plots #############
def set_cms_header():
    """text on the top right: '<era> (13.6 TeV)'; set directly because cmsstyle 0.4.3 (LCG_107 venv) and 0.5.0 (~/.local, standalone env)
    have different SetLumi/SetEnergy signatures"""
    CMS.SetExtraText("Work in Progress")
    CMS.cmsstyle.cms_lumi   = era
    CMS.cmsstyle.cms_energy = "13.6 TeV"


def redraw_cms_header(c):
    """cmsCanvas draws the header with its own margins: after changing the margins remove it (TLatex) and draw it again"""
    for obj in list(c.GetListOfPrimitives()):
        if obj.InheritsFrom("TLatex"):
            c.GetListOfPrimitives().Remove(obj)
    CMS.CMS_lumi(c, 0)


def draw_map(values, xlabels, ztitle, zmax, output_name):
    """2D map pT bin x tag category, all bins with the same size, value (+- error) written in each bin; missing values labelled N/A"""
    set_cms_header()
    c = CMS.cmsCanvas("c", 0, len(xlabels), 0, len(matchings), "", "",
                      square=False,          # rectangular canvas (CMS.kRectangular not available in cmsstyle 0.5.0)
                      iPos=0, with_z_axis=True)
    c.SetLeftMargin(0.18)    # room for the tag category labels
    c.SetRightMargin(0.16)   # room for the color palette
    c.SetBottomMargin(0.18)

    h = ROOT.TH2F("h", "", len(xlabels), 0, len(xlabels), len(matchings), 0, len(matchings))
    for ix, label in enumerate(xlabels, start=1):
        h.GetXaxis().SetBinLabel(ix, label)
    for iy, TagCat in enumerate(matchings, start=1):
        h.GetYaxis().SetBinLabel(iy, TagCat)
    # fitted json: "other" is never fitted (empty lists)
    for iy, TagCat in enumerate(matchings, start=1):
        for ix, value in enumerate(values[TagCat]["value"], start=1):
            if not is_missing(value):
                h.SetBinContent(ix, iy, max(value, 1e-6))   # COLZ does not paint bins with content 0: a SF = 0 would look like a missing value
    h.SetMinimum(0.0)
    h.SetMaximum(zmax)

    h.GetXaxis().SetTitle("p_{T} [GeV]")
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.4)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetZaxis().SetTitle(ztitle)
    h.GetZaxis().SetTitleSize(0.045)
    h.GetZaxis().SetLabelSize(0.045)

    c.cd()
    h.Draw("COLZ")
    CMS.CMS_lumi(c, 0)       # header drawn again: h.Draw("COLZ") (without SAME) clears the one drawn by cmsCanvas

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(0.020)
    for iy, TagCat in enumerate(matchings, start=1):
        value_list = values[TagCat]["value"]
        error_list = values[TagCat]["error"]
        for ix in range(len(xlabels)):
            if (ix >= len(value_list)) or is_missing(value_list[ix]):
                content = "N/A"
            elif error_list is None:
                content = f"{value_list[ix]:.3f}"
            else:
                content = f"{value_list[ix]:.3f} #pm {error_list[ix]:.3f}"
            latex.DrawLatex(ix + 0.5, iy - 0.5, content)

    CMS.UpdatePalettePosition(h, c)
    for extension in ["png", "pdf"]:
        c.SaveAs(f"{output_name}.{extension}")
    c.Close()


def draw_1D(xlabels, values_per_wp, ytitle, ymax, draw_errors, line_at_one, text_lines, output_name, n_exclusive=None):
    """value in the pT bins labelled xlabels, one bin of the same size each (as the 2D maps), one graph per WP
    (horizontal bar = bin, vertical bar = error if draw_errors; the marker is shifted by wp_offsets inside the bin).
    n_exclusive: vertical dashed line after the first n_exclusive bins (exclusive pT bins | wide ones), None: no line.
    Points are drawn in [0, ymax]; the y axis goes up to 1.4*ymax to leave room for the label and the legend (white boxes, drawn over
    the error bars). A value above ymax is drawn as an arrow above ymax with the value written over it."""
    set_cms_header()
    n_bins  = len(xlabels)
    yframe  = 1.4 * ymax
    c = CMS.cmsCanvas("c1D", 0, n_bins, 0, yframe, "p_{T} [GeV]", ytitle, square=False, iPos=0, yTitOffset=1.0)
    c.SetLeftMargin(0.14)    # room for the y title
    c.SetRightMargin(0.05)
    c.SetBottomMargin(0.15)  # room for the bin labels
    redraw_cms_header(c)

    frame = c.GetListOfPrimitives().FindObject("hframe")    # frame histogram of cmsCanvas: one bin per pT bin, with its label
    frame.GetXaxis().Set(n_bins, 0, n_bins)
    for ix, label in enumerate(xlabels, start=1):
        frame.GetXaxis().SetBinLabel(ix, label)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetXaxis().SetTitleOffset(1.25)
    c.Modified()

    if line_at_one:
        line = ROOT.TLine(0, 1, n_bins, 1)
        CMS.cmsDrawLine(line, lcolor=ROOT.kGray+1, lstyle=ROOT.kDashed, lwidth=1)
    if n_exclusive is not None:
        separator = ROOT.TLine(n_exclusive, 0, n_exclusive, yframe)
        CMS.cmsDrawLine(separator, lcolor=ROOT.kGray+2, lstyle=ROOT.kDashed, lwidth=2)

    legend  = CMS.cmsLeg(0.47, 0.83, 0.945, 0.89, textSize=0.032)   # one row, in the room above ymax
    legend.SetNColumns(3)
    legend.SetFillStyle(1001)
    legend.SetFillColor(ROOT.kWhite)
    graphs  = []
    arrows  = []
    for wp_cat, values in values_per_wp.items():
        graph       = ROOT.TGraphAsymmErrors()
        n_arrows    = 0
        for i in range(n_bins):                                 # bin i goes from x = i to x = i+1
            if i >= len(values["value"]) or is_missing(values["value"][i]):     # not fitted / null bin: no point
                continue
            value       = values["value"][i]
            x_marker    = i + 0.5 + wp_offsets[wp_cat]
            if value > ymax:
                arrows.append((x_marker, value, wp_colors[wp_cat]))
                n_arrows += 1
                continue
            n_points    = graph.GetN()
            error       = values["error"][i] if draw_errors else 0.
            graph.SetPoint(n_points, x_marker, value)
            graph.SetPointError(n_points, x_marker - i, i + 1 - x_marker, error, error)
        if graph.GetN() + n_arrows == 0:
            continue
        if graph.GetN() > 0:
            CMS.cmsDraw(graph, "P", marker=20, mcolor=wp_colors[wp_cat], lcolor=wp_colors[wp_cat])
        else:                                                   # only arrows: style set for the legend entry
            graph.SetMarkerStyle(20)
            graph.SetMarkerColor(wp_colors[wp_cat])
            graph.SetLineColor(wp_colors[wp_cat])
        legend.AddEntry(graph, f"WP {wp_cat}", "lp")
        graphs.append(graph)
    if len(graphs) == 0:
        print(f"WARNING: nothing to draw in {output_name}, skipped")
        c.Close()
        return

    # values above ymax: arrow from ymax up, value written over it (vertical text: the arrows of the 3 WPs are close)
    arrow_objects   = []
    arrow_text      = ROOT.TLatex()
    arrow_text.SetTextSize(0.026)
    arrow_text.SetTextAngle(90)
    arrow_text.SetTextAlign(12)
    for x_marker, value, color in arrows:
        arrow = ROOT.TArrow(x_marker, 1.01 * ymax, x_marker, 1.07 * ymax, 0.012, "|>")
        arrow.SetLineColor(color)
        arrow.SetFillColor(color)
        arrow.SetLineWidth(2)
        arrow.Draw()
        arrow_objects.append(arrow)
        arrow_text.SetTextColor(color)
        arrow_text.DrawLatex(x_marker, 1.08 * ymax, f"{value:.2f}")

    legend.Draw()

    label = ROOT.TPaveText(0.17, 0.89 - 0.045*len(text_lines), 0.45, 0.89, "NDC")
    label.SetFillStyle(1001)
    label.SetFillColor(ROOT.kWhite)
    label.SetBorderSize(0)
    label.SetTextFont(62)
    label.SetTextSize(0.030)
    label.SetTextAlign(12)
    for line_text in text_lines:
        label.AddText(line_text)
    label.Draw()

    c.RedrawAxis()           # the white boxes cover the axis ticks
    for extension in ["png", "pdf"]:
        c.SaveAs(f"{output_name}.{extension}")
    c.Close()


############# fitted: maps and 1D plots #############
for subfolder in ["fitted/2D", "fitted/1D", "applied/2D", "applied/1D"]:
    os.makedirs(f"{output}/{subfolder}", exist_ok=True)

for TopCat in TopCategories:
    sf_json     = load_json(f"{input_folder}/TrotaScaleFactors_{era}_{TopCat}.json")
    eff_json    = load_json(f"{input_folder}/TrotaEfficiencies_{era}_{TopCat}.json")

    sf_wps      = [wp_cat for wp_cat in wp_cats if sf_json is not None and wp_cat in sf_json[TopCat]]
    eff_wps     = [wp_cat for wp_cat in wp_cats if eff_json is not None and wp_cat in eff_json[TopCat]]
    for wp_cat in wp_cats:
        if sf_json is not None and wp_cat not in sf_wps:
            print(f"WARNING: {wp_cat} not fitted in TrotaScaleFactors_{era}_{TopCat}.json, skipped")
        if eff_json is not None and wp_cat not in eff_wps:
            print(f"WARNING: {wp_cat} not in TrotaEfficiencies_{era}_{TopCat}.json, skipped")

    # 2D maps
    for wp_cat in sf_wps:
        for channel in channels:
            draw_map(fitted_sf_values(sf_json, TopCat, wp_cat, channel), fitted_xlabels,
                     f"SF {TopCat} {wp_cat} {channel}", 2.0,
                     f"{output}/fitted/2D/SF_{TopCat}_{wp_cat}_{channel}")
    for wp_cat in eff_wps:
        draw_map(fitted_eff_values(eff_json, TopCat, wp_cat), fitted_xlabels,
                 f"MC efficiency {TopCat} {wp_cat}", 1.0,
                 f"{output}/fitted/2D/Eff_{TopCat}_{wp_cat}")

    # 1D plots, the WPs overlaid; "other" is never fitted
    for TagCat in ["topmatched", "nonmatched"]:
        for channel in channels:
            values_per_wp = {wp_cat: fitted_sf_values(sf_json, TopCat, wp_cat, channel)[TagCat] for wp_cat in sf_wps}
            draw_1D(fitted_xlabels, values_per_wp, f"SF {channel}", 2.0, True, True,
                    [f"{TopCat}, {TagCat}", "fitted"],
                    f"{output}/fitted/1D/SF1D_{TopCat}_{TagCat}_{channel}", n_exclusive=fitted_n_exclusive)
        values_per_wp = {wp_cat: fitted_eff_values(eff_json, TopCat, wp_cat)[TagCat] for wp_cat in eff_wps}
        draw_1D(fitted_xlabels, values_per_wp, "MC efficiency", 1.0, False, False,
                [f"{TopCat}, {TagCat}", "fitted"],
                f"{output}/fitted/1D/Eff1D_{TopCat}_{TagCat}", n_exclusive=fitted_n_exclusive)


############# applied: maps of the correctionlib files #############
sf_corrlib_file     = load_json(f"{input_folder}/CorrLib_TrotaScaleFactors_{era}.json")
eff_corrlib_file    = load_json(f"{input_folder}/CorrLib_TrotaEfficiencies_{era}.json")
sf_corrlib          = next(corr for corr in sf_corrlib_file["corrections"] if corr["name"] == "TrotaScaleFactors") if sf_corrlib_file is not None else None
eff_corrlib         = next(corr for corr in eff_corrlib_file["corrections"] if corr["name"] == "TrotaEfficiencies") if eff_corrlib_file is not None else None

def corrlib_wps(corrlib, file_name, TopCat):
    """WPs of TopCat in the correctionlib file (Loose, Tight, XTight); [] if the file is missing"""
    if corrlib is None:
        return []
    wps = [wp_cat for wp_cat in wp_cats if wp_cat in corrlib_keys(corrlib_child(corrlib["data"], TopCat))]
    for wp_cat in wp_cats:
        if wp_cat not in wps:
            print(f"WARNING: {wp_cat} not in {file_name} for {TopCat}, skipped")
    return wps


for TopCat in TopCategories:
    sf_wps      = corrlib_wps(sf_corrlib, f"CorrLib_TrotaScaleFactors_{era}.json", TopCat)
    eff_wps     = corrlib_wps(eff_corrlib, f"CorrLib_TrotaEfficiencies_{era}.json", TopCat)

    # 2D maps
    for wp_cat in sf_wps:
        for channel in channels:
            values, edges = applied_sf_values(sf_corrlib, TopCat, wp_cat, channel)
            draw_map(values, corrlib_xlabels(edges), f"SF {TopCat} {wp_cat} {channel}", 2.0,
                     f"{output}/applied/2D/SF_{TopCat}_{wp_cat}_{channel}")
    for wp_cat in eff_wps:
        values, edges = applied_eff_values(eff_corrlib, TopCat, wp_cat)
        draw_map(values, corrlib_xlabels(edges), f"MC efficiency {TopCat} {wp_cat}", 1.0,
                 f"{output}/applied/2D/Eff_{TopCat}_{wp_cat}")

    # 1D plots, the WPs overlaid (all 3 tag categories: in the correctionlib file "other" has SF 1 +- 0 / efficiency -1 if null)
    for TagCat in matchings:
        for channel in channels:
            values_per_wp   = {}
            for wp_cat in sf_wps:
                values, edges           = applied_sf_values(sf_corrlib, TopCat, wp_cat, channel)
                values_per_wp[wp_cat]   = values[TagCat]
            if values_per_wp:
                draw_1D(corrlib_xlabels(edges), values_per_wp, f"SF {channel}", 2.0, True, True,
                        [f"{TopCat}, {TagCat}", "applied"],
                        f"{output}/applied/1D/SF1D_{TopCat}_{TagCat}_{channel}")
        values_per_wp   = {}
        for wp_cat in eff_wps:
            values, edges           = applied_eff_values(eff_corrlib, TopCat, wp_cat)
            values_per_wp[wp_cat]   = values[TagCat]
        if values_per_wp:
            draw_1D(corrlib_xlabels(edges), values_per_wp, "MC efficiency", 1.0, False, False,
                    [f"{TopCat}, {TagCat}", "applied"],
                    f"{output}/applied/1D/Eff1D_{TopCat}_{TagCat}")

print(f"Plots saved in {output}")
