import ROOT
import os
import re
import sys
import math
import yaml
import optparse
import cmsstyle as CMS
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# Pre-fit and post-fit stacks of the Trota SF fit, split by tag category (topmatched, nonmatched, other) instead of by sample
# Adapted from plot_histograms.py of https://github.com/vicha-w/TopSF, drawn with PyROOT + cmsstyle
#   prefit:  shapes file of the datacard (<ev_cat>[_symmetrized][_zerosFixed].root), MC normalized to lumi only as in produce_stacks.py
#            (the fit also multiplies the MC by norm_match_mc_data of the datacard, not applied here)
#   postfit: shapes_fit_s of fitDiagnostics_<ev_cat>.root (written by fit_procedure.sh), compared with the prefit above;
#            the postfit band needs FitDiagnostics --saveWithUncertainties (default of collectHistograms.py)
# Run from postselection_prefitTopSF/ after collectHistograms.py (and fit_procedure.sh for the postfit plots)

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

usage                   = "python3 plot_TopSF_stacks.py --era <era> --TopCategory <TopCategory> --wp_cat <wp_cat> [--outdir <outdir>]"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                   help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      '--TopCategory',            dest='TopCategory',                 type=str,     default="Mixed",                                  help='Top category for the histograms: Resolved, Mixed or Merged')
parser.add_option(      "--wp_cat",                 dest="wp_cat",                      type=str,     default="Tight",                                  help="Working point category to consider among: Loose, Tight, XTight")
parser.add_option(      "--outdir",                 dest="outdir",                      type=str,     default=None,                                     help="Output folder, plots in <outdir>/stacks_<wp_cat>/<fit_variable>/ (default: <TrotaScaleFactor/folder_www/<era>>/<TopCategory> of config/config.yaml)")
(opt, args)             = parser.parse_args()
era                     = opt.era
TopCategory             = opt.TopCategory
wp_cat                  = opt.wp_cat
region                  = f"{TopCategory}{wp_cat}"
outputfolder            = config["TrotaScaleFactor"]["outputfolder"][TopCategory][era]
fit_variable            = config["TrotaScaleFactor"]["fit_variable"][region]
lumi                    = config["plotting"]["lumi_dict"][era]
workspaceSubFolder      = f"{outputfolder}/workspace_{wp_cat}/{fit_variable}/"
if opt.outdir is not None:
    outdir              = opt.outdir
else:
    folder_www          = config["TrotaScaleFactor"].get("folder_www", {}).get(era, "")
    if not folder_www:
        print(f"Output folder not given: use --outdir or set TrotaScaleFactor/folder_www/{era} in {config_paths}, exiting")
        sys.exit(1)
    outdir              = f"{folder_www}/{TopCategory}"
plotsFolder             = f"{outdir}/stacks_{wp_cat}/{fit_variable}/"
os.makedirs(plotsFolder, exist_ok=True)

event_categories        = ["pt0to200","pt200to400","pt400to600","pt600to1000","pt0to400","pt400to1000"]
if TopCategory == "Merged":
    event_categories.remove("pt0to200")     # not fitted for Merged (probe among the GoodFatJet, pt>200), as in collectHistograms.py
categories              = {
                            "topmatched":   {"color": ROOT.TColor.GetColor("#5790fc"), "label": "Top-matched"},
                            "nonmatched":   {"color": ROOT.TColor.GetColor("#e42536"), "label": "Non-matched"},
                            "other":        {"color": ROOT.TColor.GetColor("#964a8b"), "label": "Other"},
                            }
total_color             = ROOT.TColor.GetColor("#717581")
xtitles                 = {"MT_W": "M_{T}^{W} [GeV]"}
xtitle                  = xtitles.get(fit_variable, fit_variable)


############# Inputs #############
def detached_clone(hist, name):
    """clone not attached to the current directory: otherwise it is deleted when the open ROOT file is closed"""
    clone = hist.Clone(name)
    clone.SetDirectory(0)
    return clone


def read_shapes_file(ev_cat):
    """shapes file of the datacard <ev_cat>.txt written by collectHistograms.py"""
    with open(f"{workspaceSubFolder}/{ev_cat}.txt") as card:
        text = card.read()
    return re.search(r"^shapes data_obs pass (\S+)", text, re.M).group(1)


def data_graph_from_hist(hist):
    """data yields with Poisson errors (up, down), x at the bin centers"""
    hist.SetBinErrorOption(ROOT.TH1.kPoisson)
    graph = ROOT.TGraphAsymmErrors()
    for i in range(1, hist.GetNbinsX()+1):
        n = graph.GetN()
        graph.SetPoint(n, hist.GetBinCenter(i), hist.GetBinContent(i))
        graph.SetPointError(n, 0., 0., hist.GetBinErrorLow(i), hist.GetBinErrorUp(i))
    return graph


def data_graph_from_fitdiag(fit_graph, binning):
    """data of fitDiagnostics (TGraphAsymmErrors with unit-width bins), moved to the bin centers of the datacard histograms"""
    graph = ROOT.TGraphAsymmErrors()
    for i in range(fit_graph.GetN()):
        graph.SetPoint(i, binning.GetBinCenter(i+1), fit_graph.GetPointY(i))
        graph.SetPointError(i, 0., 0., fit_graph.GetErrorYlow(i), fit_graph.GetErrorYhigh(i))
    return graph


def hist_with_binning(fit_hist, binning, name):
    """fitDiagnostics shapes have unit-width bins: same contents and errors with the binning of the datacard histograms"""
    hist = detached_clone(binning, name)
    hist.Reset()
    for i in range(1, binning.GetNbinsX()+1):
        hist.SetBinContent(i, fit_hist.GetBinContent(i))
        hist.SetBinError(i, fit_hist.GetBinError(i))
    return hist


def ratio_graph(data_graph, mc_hist):
    """data/MC with the data errors divided by MC; bins without data or MC are not drawn"""
    graph = ROOT.TGraphAsymmErrors()
    for i in range(data_graph.GetN()):
        data    = data_graph.GetPointY(i)
        mc      = mc_hist.GetBinContent(i+1)
        if data <= 0 or mc <= 0:
            continue
        n = graph.GetN()
        graph.SetPoint(n, data_graph.GetPointX(i), data/mc)
        graph.SetPointError(n, 0., 0., data_graph.GetErrorYlow(i)/mc, data_graph.GetErrorYhigh(i)/mc)
    return graph


def relative_band(hist):
    """band around 1 with the relative uncertainty of hist (bins with content 0: no band)"""
    band = detached_clone(hist, hist.GetName() + "_relative")
    for i in range(1, hist.GetNbinsX()+1):
        content = hist.GetBinContent(i)
        band.SetBinContent(i, 1.)
        band.SetBinError(i, hist.GetBinError(i)/content if content > 0 else 0.)
    return band


def ratio_half_width(graph, default):
    """half width of the ratio panel around 1: the default one, enlarged (up to 1) to show all the points"""
    max_deviation = max([abs(graph.GetPointY(i) - 1) for i in range(graph.GetN())], default=0.)
    return min(max(default, math.ceil(12*max_deviation)/10), 1.0)                   # 1.2 x max deviation, rounded up to 0.1


def legend_header(ev_cat, channel):
    pt_low, pt_high = re.match(r"pt(\d+)to(\d+)", ev_cat).groups()
    return f"p_{{T}} #in [{pt_low}, {pt_high}] GeV, {channel}"


############# Plots #############
def set_cms_header():
    """text on the top right: '<lumi> fb^{-1} (13.6 TeV)'; set directly because cmsstyle 0.4.3 and 0.5.0 have different SetLumi/SetEnergy"""
    CMS.SetExtraText("Work in Progress")
    CMS.cmsstyle.cms_lumi   = f"{lumi:.1f} fb^{{-1}}"
    CMS.cmsstyle.cms_energy = "13.6 TeV"


def redraw_cms_header(pad):
    """cmsDiCanvas draws the header with its own margins: after changing the margins remove it (TLatex) and draw it again"""
    for obj in list(pad.GetListOfPrimitives()):
        if obj.InheritsFrom("TLatex"):
            pad.GetListOfPrimitives().Remove(obj)
    CMS.CMS_lumi(pad, 0)


def has_errors(hist):
    """False if all the bin errors are 0 (FitDiagnostics without --saveWithUncertainties: no postfit uncertainties)"""
    return any(hist.GetBinError(i) > 0 for i in range(1, hist.GetNbinsX()+1))


def make_canvas(name, binning, ymax, half_width):
    """canvas with the main pad (Events) and the ratio pad (Data/MC in [1 - half_width, 1 + half_width])"""
    set_cms_header()
    xmin    = binning.GetXaxis().GetXmin()
    xmax    = binning.GetXaxis().GetXmax()
    canvas  = CMS.cmsDiCanvas(name, xmin, xmax, 0, 1.6*ymax, 1 - half_width, 1 + half_width,
                              xtitle, "Events", "Data/MC", square=True, iPos=0)
    # wider left margin than cmsDiCanvas (0.15): the y labels have up to 5 digits; y titles moved by the same factor
    for i_pad in [1, 2]:
        pad     = canvas.cd(i_pad)
        frame   = pad.GetListOfPrimitives().FindObject("hframe")
        pad.SetLeftMargin(0.18)
        frame.GetYaxis().SetTitleOffset(1.35 * frame.GetYaxis().GetTitleOffset())
        if i_pad == 2:
            frame.GetYaxis().SetNdivisions(505)
    redraw_cms_header(canvas.cd(1))
    return canvas


def make_legend(n_entries, header):
    """legend in the top right corner of the main pad, header = pT bin and channel"""
    legend = CMS.cmsLeg(0.55, 0.89 - 0.055*(n_entries + 1), 0.92, 0.89, textSize=0.042)
    legend.SetHeader(header)
    return legend


def draw_ratio_pad(canvas, binning, data_graph, mc_hist):
    """data/MC points and the relative uncertainty of mc_hist around 1 (if it has uncertainties)"""
    canvas.cd(2)
    band = relative_band(mc_hist)
    if has_errors(mc_hist):
        CMS.cmsDraw(band, "E2SAME", fcolor=ROOT.kGray+2, fstyle=3004, msize=0, lwidth=0)
    line = ROOT.TLine(binning.GetXaxis().GetXmin(), 1, binning.GetXaxis().GetXmax(), 1)
    CMS.cmsDrawLine(line, lcolor=ROOT.kGray+1, lstyle=ROOT.kDashed, lwidth=1)
    ratio = ratio_graph(data_graph, mc_hist)
    CMS.cmsDraw(ratio, "PZ", marker=20, mcolor=ROOT.kBlack, lcolor=ROOT.kBlack)
    ROOT.gPad.RedrawAxis()
    return band, line, ratio


def save(canvas, filename):
    for extension in ["png", "pdf"]:
        canvas.SaveAs(f"{filename}.{extension}")
    canvas.Close()
    print(f"Saved {filename}.png/.pdf")


def plot_prefit(mc, data_hist, header, filename):
    """stack of the tag categories, MC stat. uncertainty on the total"""
    data_graph  = data_graph_from_hist(data_hist)
    mc_sum      = detached_clone(mc["topmatched"], "mc_sum_prefit")
    mc_sum.Reset()
    for hist in mc.values():
        mc_sum.Add(hist)
    ymax        = max(mc_sum.GetMaximum(), max(data_graph.GetPointY(i) + data_graph.GetErrorYhigh(i) for i in range(data_graph.GetN())))
    half_width  = ratio_half_width(ratio_graph(data_graph, mc_sum), 0.5)
    canvas      = make_canvas("c_prefit", data_hist, ymax, half_width)

    canvas.cd(1)
    legend      = make_legend(len(categories) + 2, header)
    legend.AddEntry(data_graph, "Data", "pe")
    stack       = ROOT.THStack("stack_prefit", "")
    for cat, cat_cfg in categories.items():
        hist = mc[cat]
        hist.SetFillColor(cat_cfg["color"])
        hist.SetLineColor(cat_cfg["color"])
        stack.Add(hist)
    for cat in reversed(list(categories)):              # legend from the top of the stack
        legend.AddEntry(mc[cat], categories[cat]["label"], "f")
    stack.Draw("HIST SAME")
    CMS.cmsDraw(mc_sum, "E2SAME", fcolor=ROOT.kGray+2, fstyle=3004, msize=0, lwidth=0)
    legend.AddEntry(mc_sum, "MC stat. unc.", "f")
    CMS.cmsDraw(data_graph, "PZ", marker=20, mcolor=ROOT.kBlack, lcolor=ROOT.kBlack)
    legend.Draw()
    ROOT.gPad.RedrawAxis()

    ratio_objects = draw_ratio_pad(canvas, data_hist, data_graph, mc_sum)
    save(canvas, filename)


def plot_postfit(prefit, prefit_sum, postfit, postfit_sum, data_graph, binning, header, filename):
    """pre-fit (dotted) and post-fit (solid) shapes of each tag category and of their sum, post-fit uncertainty on the sum"""
    ymax        = max(postfit_sum.GetMaximum(), prefit_sum.GetMaximum(),
                      max(data_graph.GetPointY(i) + data_graph.GetErrorYhigh(i) for i in range(data_graph.GetN())))
    half_width  = ratio_half_width(ratio_graph(data_graph, postfit_sum), 0.3)
    canvas      = make_canvas("c_postfit", binning, ymax, half_width)

    canvas.cd(1)
    legend      = make_legend(len(categories) + 3 + has_errors(postfit_sum), header)
    legend.AddEntry(data_graph, "Data", "pe")
    for cat, cat_cfg in categories.items():
        CMS.cmsDraw(prefit[cat], "HISTSAME", lcolor=cat_cfg["color"], lstyle=ROOT.kDotted, lwidth=2, fstyle=0, msize=0)
        CMS.cmsDraw(postfit[cat], "HISTSAME", lcolor=cat_cfg["color"], lstyle=ROOT.kSolid, lwidth=2, fstyle=0, msize=0)
        legend.AddEntry(postfit[cat], cat_cfg["label"], "l")
    CMS.cmsDraw(prefit_sum, "HISTSAME", lcolor=total_color, lstyle=ROOT.kDotted, lwidth=2, fstyle=0, msize=0)
    CMS.cmsDraw(postfit_sum, "HISTSAME", lcolor=total_color, lstyle=ROOT.kSolid, lwidth=2, fstyle=0, msize=0)
    legend.AddEntry(postfit_sum, "Total SM (postfit)", "l")
    if has_errors(postfit_sum):
        postfit_band = detached_clone(postfit_sum, "postfit_band")
        CMS.cmsDraw(postfit_band, "E2SAME", fcolor=ROOT.kGray+2, fstyle=3004, msize=0, lwidth=0)
        legend.AddEntry(postfit_band, "Postfit unc.", "f")
    legend.AddEntry(prefit_sum, "Prefit", "l")
    CMS.cmsDraw(data_graph, "PZ", marker=20, mcolor=ROOT.kBlack, lcolor=ROOT.kBlack)
    legend.Draw()
    ROOT.gPad.RedrawAxis()

    ratio_objects = draw_ratio_pad(canvas, binning, data_graph, postfit_sum)
    save(canvas, filename)


############# Loop on the event categories #############
for ev_cat in event_categories:
    if not os.path.exists(f"{workspaceSubFolder}/{ev_cat}.txt"):
        print(f"Datacard {workspaceSubFolder}/{ev_cat}.txt not found, skipping {ev_cat}")
        continue
    shapes_file         = read_shapes_file(ev_cat)
    print(f"{ev_cat}: shapes from {shapes_file}")
    prefitfile          = ROOT.TFile.Open(shapes_file)
    fitdiagfile_path    = f"{workspaceSubFolder}/fitDiagnostics_{ev_cat}.root"
    fitdiagfile         = ROOT.TFile.Open(fitdiagfile_path) if os.path.exists(fitdiagfile_path) else None
    if fitdiagfile is None:
        print(f"{fitdiagfile_path} not found, only prefit plots for {ev_cat}")

    for channel in ["pass", "fail"]:
        header              = legend_header(ev_cat, channel)
        data_hist           = detached_clone(prefitfile.Get(f"data_{fit_variable}_{ev_cat}_{channel}"), f"data_{channel}")
        mc                  = {}
        for cat in categories:
            mc[cat] = detached_clone(prefitfile.Get(f"{cat}_{fit_variable}_{ev_cat}_{channel}_nominal"), f"prefit_{cat}_{channel}")
        plot_prefit(mc, data_hist, header, f"{plotsFolder}/prefit_{channel}_{ev_cat}")

        if fitdiagfile is None:
            continue
        prefit_sum          = detached_clone(data_hist, f"prefit_sum_{channel}")
        prefit_sum.Reset()
        for hist in mc.values():
            prefit_sum.Add(hist)
        postfit             = {cat: hist_with_binning(fitdiagfile.Get(f"shapes_fit_s/{channel}/{cat}"), data_hist, f"postfit_{cat}_{channel}") for cat in categories}
        postfit_sum         = hist_with_binning(fitdiagfile.Get(f"shapes_fit_s/{channel}/total"), data_hist, f"postfit_total_{channel}")
        fit_data_graph      = data_graph_from_fitdiag(fitdiagfile.Get(f"shapes_prefit/{channel}/data"), data_hist)
        plot_postfit(mc, prefit_sum, postfit, postfit_sum, fit_data_graph, data_hist, header, f"{plotsFolder}/postfit_{channel}_{ev_cat}")
    prefitfile.Close()
    if fitdiagfile is not None:
        fitdiagfile.Close()
