import ROOT
import os
import re
import sys
import yaml
import optparse
import numpy as np
import mplhep as hep
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
ROOT.gROOT.SetBatch()
plt.style.use(hep.style.CMS)

# Pre-fit and post-fit stacks of the Trota SF fit, split by tag category (topmatched, nonmatched, other) instead of by sample
# Adapted from plot_histograms.py of https://github.com/vicha-w/TopSF
#   prefit:  shapes file of the datacard (<ev_cat>[_symmetrized][_zerosFixed].root), MC normalized to lumi only as in produce_stacks.py
#            (the fit also multiplies the MC by norm_match_mc_data of the datacard, not applied here)
#   postfit: shapes_fit_s of fitDiagnostics_<ev_cat>.root (written by fit_procedure.sh), compared with the prefit above
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

usage                   = "python3 plot_TopSF_stacks.py --era <era> --TopCategory <TopCategory> --wp_cat <wp_cat> --outdir <outdir>"
parser                  = optparse.OptionParser(usage)
parser.add_option(      "--era",                    dest="era",                         type=str,     default="2023",                                   help="Please enter the era, e.g. 2022, 2022EE, etc.")
parser.add_option(      '--TopCategory',            dest='TopCategory',                 type=str,     default="Mixed",                                  help='Top category for the histograms: Resolved, Mixed or Merged')
parser.add_option(      "--wp_cat",                 dest="wp_cat",                      type=str,     default="Tight",                                  help="Working point category to consider among: Loose, Tight")
parser.add_option(      "--outdir",                 dest="outdir",                      type=str,     default="",                                       help="Output folder (required), plots in <outdir>/stacks_<wp_cat>/<fit_variable>/")
(opt, args)             = parser.parse_args()
era                     = opt.era
TopCategory             = opt.TopCategory
wp_cat                  = opt.wp_cat
region                  = f"{TopCategory}{wp_cat}"
outputfolder            = config["TrotaScaleFactor"]["outputfolder"][TopCategory][era]
fit_variable            = config["TrotaScaleFactor"]["fit_variable"][region]
lumi                    = config["plotting"]["lumi_dict"][era]
workspaceSubFolder      = f"{outputfolder}/workspace_{wp_cat}/{fit_variable}/"
outdir                  = opt.outdir
if not outdir:
    print("Output folder not given: use --outdir, exiting")
    sys.exit(1)
plotsFolder             = f"{outdir}/stacks_{wp_cat}/{fit_variable}/"
os.makedirs(plotsFolder, exist_ok=True)

event_categories        = ["pt0to200","pt200to400","pt400to600","pt600to1000","pt0to400","pt400to1000"]
categories              = {
                            "topmatched":   {"color": "#5790fc", "label": "Top-matched"},
                            "nonmatched":   {"color": "#e42536", "label": "Non-matched"},
                            "other":        {"color": "#964a8b", "label": "Other"},
                            }
xlabels                 = {"MT_W": r"$M_{T}^{W}$ [GeV]"}
xlabel                  = xlabels.get(fit_variable, fit_variable)
com                     = 13.6


def read_shapes_file(ev_cat):
    """shapes file of the datacard <ev_cat>.txt written by collectHistograms.py"""
    with open(f"{workspaceSubFolder}/{ev_cat}.txt") as card:
        text = card.read()
    return re.search(r"^shapes data_obs pass (\S+)", text, re.M).group(1)

def hist_to_bins(hist):
    return np.array([hist.GetBinLowEdge(i) for i in range(1, hist.GetNbinsX()+2)])

def hist_to_array(hist):
    values  = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    errors  = np.array([hist.GetBinError(i)   for i in range(1, hist.GetNbinsX()+1)])
    return values, errors

def data_hist_to_array(hist):
    """data yields with Poisson errors (up, down)"""
    hist.SetBinErrorOption(ROOT.TH1.kPoisson)
    values  = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    errors  = np.array([[hist.GetBinErrorUp(i) for i in range(1, hist.GetNbinsX()+1)],
                        [hist.GetBinErrorLow(i) for i in range(1, hist.GetNbinsX()+1)]])
    return values, errors

def graph_to_array(graph):
    """data of fitDiagnostics (TGraphAsymmErrors) with errors (up, down)"""
    values  = np.array([graph.GetPointY(i) for i in range(graph.GetN())])
    errors  = np.array([[graph.GetErrorYhigh(i) for i in range(graph.GetN())],
                        [graph.GetErrorYlow(i) for i in range(graph.GetN())]])
    return values, errors

def legend_title(ev_cat, channel):
    pt_low, pt_high = re.match(r"pt(\d+)to(\d+)", ev_cat).groups()
    return rf"$p_T \in [{pt_low}, {pt_high}]$ GeV, {channel}"

def make_figure():
    fig         = plt.figure(figsize=(12, 12), facecolor="white")
    main_ax     = plt.subplot2grid((5, 1), (0, 0), rowspan=4)
    ratio_ax    = plt.subplot2grid((5, 1), (4, 0), sharex=main_ax)
    fig.subplots_adjust(hspace=0)
    return fig, main_ax, ratio_ax

def plot_ratio(ratio_ax, centers, data, data_err, mc_sum):
    """data/MC points, bins without data are not drawn"""
    has_data    = data > 0
    ratio_ax.errorbar(centers[has_data], data[has_data]/mc_sum[has_data], yerr=data_err[:, has_data]/mc_sum[has_data], fmt="o", color="black", capsize=5)
    return data[has_data]/mc_sum[has_data]

def ratio_half_width(ratio, default):
    """half width of the ratio panel around 1: the default one, enlarged (up to 1) to show all the points"""
    max_deviation = np.max(np.abs(ratio[np.isfinite(ratio)] - 1), initial=0)
    return min(max(default, np.ceil(12*max_deviation)/10), 1.0)                     # 1.2 x max deviation, rounded up to 0.1

def finalize(fig, main_ax, ratio_ax, bins, ymax, half_width, filename):
    main_ax.set_xlim((bins[0], bins[-1]))
    main_ax.set_ylim((0, ymax*1.5))
    main_ax.set_ylabel("Events")
    main_ax.tick_params(labelbottom=False)
    main_ax.yaxis.get_major_ticks()[0].label1.set_visible(False)
    ratio_ax.hlines(1, bins[0], bins[-1], linestyles="--", colors="#9c9ca1")
    ratio_ax.set_ylim((1 - half_width, 1 + half_width))
    ratio_ax.yaxis.set_major_locator(MaxNLocator(nbins=4, steps=[1, 2, 2.5, 5, 10], prune="both"))
    ratio_ax.set_xlabel(xlabel)
    ratio_ax.set_ylabel("Data/MC")
    hep.cms.label(llabel="Preliminary", data=True, lumi=lumi, com=com, ax=main_ax)
    fig.savefig(filename + ".png", bbox_inches="tight")
    fig.savefig(filename + ".pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {filename}.png/.pdf")


def plot_prefit(mc, mc_err, data, data_err, bins, title, filename):
    """stack of the tag categories, MC stat. uncertainty on the total"""
    centers     = (bins[:-1] + bins[1:]) / 2
    fig, main_ax, ratio_ax = make_figure()

    baseline    = np.zeros(len(centers))
    for cat, cat_cfg in categories.items():
        main_ax.stairs(mc[cat] + baseline, bins, baseline=baseline, fill=True, label=cat_cfg["label"], facecolor=cat_cfg["color"])
        baseline += mc[cat]
    mc_sum      = baseline
    mc_sum_err  = np.sqrt(sum(mc_err[cat]**2 for cat in categories))
    main_ax.stairs(mc_sum + mc_sum_err, bins, baseline=mc_sum - mc_sum_err, fill=False, hatch="///", color="#717581", linewidth=0, label="MC stat. unc.")
    main_ax.errorbar(centers, data, yerr=data_err, fmt="o", color="black", label="Data", capsize=5)

    handles, labels = main_ax.get_legend_handles_labels()
    order       = [len(labels)-1] + list(range(len(labels)-1))                     # data first
    main_ax.legend([handles[i] for i in order], [labels[i] for i in order], title=title)

    ratio_ax.stairs(1 + mc_sum_err/mc_sum, bins, baseline=1 - mc_sum_err/mc_sum, fill=False, hatch="///", color="black", linewidth=0)
    ratio       = plot_ratio(ratio_ax, centers, data, data_err, mc_sum)

    finalize(fig, main_ax, ratio_ax, bins, max(max(mc_sum), max(data)), ratio_half_width(ratio, 0.5), filename)


def plot_postfit(prefit, prefit_sum, postfit, postfit_err, postfit_sum, postfit_sum_err, data, data_err, bins, title, filename):
    """pre-fit (dotted) and post-fit (solid) shapes of each tag category and of their sum, post-fit uncertainty on the sum"""
    centers     = (bins[:-1] + bins[1:]) / 2
    fig, main_ax, ratio_ax = make_figure()

    for cat, cat_cfg in categories.items():
        main_ax.stairs(prefit[cat], bins, color=cat_cfg["color"], linestyle=":", linewidth=2)
        main_ax.stairs(postfit[cat], bins, label=cat_cfg["label"], color=cat_cfg["color"], linestyle="-", linewidth=2)
        main_ax.errorbar(centers, postfit[cat], yerr=postfit_err[cat], fmt="none", ecolor=cat_cfg["color"], capsize=5, linewidth=2)
    main_ax.stairs(prefit_sum, bins, color="#717581", linestyle=":", linewidth=2, label="Prefit")
    main_ax.stairs(postfit_sum, bins, color="#717581", linestyle="-", linewidth=2, label="Total SM")
    main_ax.stairs(postfit_sum + postfit_sum_err, bins, baseline=postfit_sum - postfit_sum_err, fill=False, hatch="///", color="#717581", linewidth=0, label="Postfit unc.")
    main_ax.errorbar(centers, data, yerr=data_err, fmt="o", color="black", label="Data", capsize=5, linewidth=2)

    handles, labels = main_ax.get_legend_handles_labels()
    n_cat       = len(categories)
    order       = [len(labels)-1] + list(range(n_cat)) + [n_cat+1, n_cat+2, n_cat]  # data, categories, total, unc., prefit
    main_ax.legend([handles[i] for i in order], [labels[i] for i in order], title=title)

    ratio_ax.stairs(1 + postfit_sum_err/postfit_sum, bins, baseline=1 - postfit_sum_err/postfit_sum, fill=False, hatch="///", color="black", linewidth=0)
    ratio       = plot_ratio(ratio_ax, centers, data, data_err, postfit_sum)

    finalize(fig, main_ax, ratio_ax, bins, max(max(postfit_sum), max(prefit_sum), max(data)), ratio_half_width(ratio, 0.3), filename)


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
        title               = legend_title(ev_cat, channel)
        hist_data           = prefitfile.Get(f"data_{fit_variable}_{ev_cat}_{channel}")
        bins                = hist_to_bins(hist_data)                                   # fitDiagnostics shapes have unit-width bins: use the binning of the datacard histograms
        data, data_err      = data_hist_to_array(hist_data)

        mc, mc_err          = {}, {}
        for cat in categories:
            mc[cat], mc_err[cat] = hist_to_array(prefitfile.Get(f"{cat}_{fit_variable}_{ev_cat}_{channel}_nominal"))
        plot_prefit(mc, mc_err, data, data_err, bins, title, f"{plotsFolder}/prefit_{channel}_{ev_cat}")

        if fitdiagfile is None:
            continue
        postfit, postfit_err = {}, {}
        for cat in categories:
            postfit[cat], postfit_err[cat]  = hist_to_array(fitdiagfile.Get(f"shapes_fit_s/{channel}/{cat}"))
        postfit_sum, postfit_sum_err        = hist_to_array(fitdiagfile.Get(f"shapes_fit_s/{channel}/total"))
        fit_data, fit_data_err              = graph_to_array(fitdiagfile.Get(f"shapes_prefit/{channel}/data"))
        plot_postfit(mc, sum(mc.values()), postfit, postfit_err, postfit_sum, postfit_sum_err, fit_data, fit_data_err, bins, title, f"{plotsFolder}/postfit_{channel}_{ev_cat}")
    prefitfile.Close()
    if fitdiagfile is not None:
        fitdiagfile.Close()
