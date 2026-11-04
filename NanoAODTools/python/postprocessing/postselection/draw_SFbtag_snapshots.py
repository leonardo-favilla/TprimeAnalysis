# Distribution of the event b-tag SF (SFbtag_nominal) from the step-2 snapshots (--snapshot, preselection, no b-tag cut).
# Same plots as the matplotlib version of Nov 3 2026, redone with PyROOT + cmsstyle:
#   - SFbtag_<era>_5components.png       : the 5 backgrounds of one era, normalized to unit area
#   - SFbtag_<process>_2023vs2024.png    : one process, 2023 (PNet shape SF) vs 2024 (UParT fixed-WP SF)
#   - EventWeight_<process>_<era>.png    : event weight w_noTrotaSF with and without SFbtag_nominal
#   - rBTag_vs_nGoodJet_<era>.png        : BTV normalization factor r = sum(w without SF) / sum(w with SF) vs nGoodJet
# Unweighted events, under/overflow put in the first/last bin, means (in the legend) computed on all events (no clipping).
# The snapshots are taken after the step-2 preselection (trigger MET, nGoodJet>2 || nGoodFatJet>0), the same phase space
# of the 2024 b-tag efficiency maps (BTagEfficiency/postSelector.py). w_noTrotaSF contains SFbtag_nominal as a factor,
# so the weight without b-tag SF is w_noTrotaSF / SFbtag_nominal (SFbtag_nominal > 0 in all the snapshots).
#
# Usage: python3 draw_SFbtag_snapshots.py [--indir <folder with snap_*.root>] [--outdir <folder>]

import os
import argparse
import numpy as np
import ROOT
import cmsstyle as CMS

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("--indir",  default="/eos/user/l/lfavilla/RDF_DManalysis/results/2024/test_snapshot_btag/snapshots")
parser.add_argument("--outdir", default=None, help="default: <indir>/plots")
args   = parser.parse_args()
outdir = args.outdir if args.outdir is not None else os.path.join(args.indir, "plots")
os.makedirs(outdir, exist_ok=True)

# SFbtag binning: 0-3.5 in steps of 0.1 (0.05 in the matplotlib plots, too few events per bin)
nbins, xmin, xmax = 35, 0.0, 3.5
binwidth          = (xmax - xmin) / nbins
# event weight binning: -3-5 in steps of 0.1
w_nbins, w_xmin, w_xmax = 80, -3.0, 5.0
# r vs nGoodJet: one point per multiplicity, the last one is >= nj_max; points with less than nj_minevents events are not drawn
nj_max, nj_minevents    = 8, 10

# process -> label and snapshot name in each era (2023 WJets has no MuNu split)
processes = [
    ("TT_semilep",          "TT semilep",          {"2023": "TT_semilep_2023",                    "2024": "TT_semilep_2024"}),
    ("TW_LNu2Q",            "TW LNu2Q",            {"2023": "TWminustoLNu2Q_2023",                "2024": "TWminustoLNu2Q_2024"}),
    ("QCD_HT1000to1200",    "QCD HT1000to1200",    {"2023": "QCD_HT1000to1200_2023",              "2024": "QCD_HT1000to1200_2024"}),
    ("ZJets_PT200to400_2J", "ZJets PT200to400 2J", {"2023": "ZJetsToNuNu_2jets_PT200to400_2J_2023", "2024": "ZJetsToNuNu_2jets_PT200to400_2J_2024"}),
    ("WJets_2J",            "WJets 2J",            {"2023": "WJets_2jets2J_2023",                 "2024": "WJets_2jets_MuNu_2J_2024"}),
]
colors_5     = [CMS.p6.kBlue, CMS.p6.kYellow, CMS.p6.kRed, CMS.p6.kGrape, CMS.p6.kGray]
colors_era   = {"2023": CMS.p6.kBlue, "2024": CMS.p6.kRed}
colors_w     = {"with": CMS.p6.kBlue, "without": CMS.p6.kRed}


def get_histo(snapname):
    """Normalized SFbtag_nominal histogram of one snapshot, with the number of events, mean and std."""
    rdf   = ROOT.RDataFrame("events_nominal", os.path.join(args.indir, f"snap_{snapname}.root"))
    # overflow in the last bin: clip just below xmax
    rdf   = rdf.Define("SFbtag_clipped", f"SFbtag_nominal < {xmax} ? (double)SFbtag_nominal : {xmax - 0.5 * binwidth}")
    h     = rdf.Histo1D((f"h_{snapname}", "", nbins, xmin, xmax), "SFbtag_clipped")
    n     = rdf.Count()
    mean  = rdf.Mean("SFbtag_nominal")
    std   = rdf.StdDev("SFbtag_nominal")
    h     = h.GetValue().Clone()
    h.SetDirectory(0)
    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())
    return h, n.GetValue(), mean.GetValue(), std.GetValue()


def setup_cms():
    CMS.SetExtraText("Private Work")
    CMS.SetLumi(None, run="Run 3")
    CMS.SetEnergy(13.6)
    CMS.ResetAdditionalInfo()


def save(c, outname):
    for ext in ("png", "pdf"):
        c.SaveAs(os.path.join(outdir, f"{outname}.{ext}"))
    c.Close()


def draw(histos, title, outname, x_range=(xmin, xmax), xtitle="SFbtag_nominal (event weight)", bw=binwidth):
    """histos: list of (histo, legend label, color); log y axis, vertical line at x = 1."""
    setup_cms()
    ymax = max(h.GetMaximum() for h, _, _ in histos)
    ytop = ymax * 40    # room for the legend above the histograms
    c    = CMS.cmsCanvas(outname, x_range[0], x_range[1], 3e-5, ytop, xtitle,
                         f"Fraction of events / {bw:.2f}", square=False, iPos=0, extraSpace=0.02, yTitOffset=1.0)
    c.SetLogy()
    # top right, title as legend header (one more row)
    leg  = CMS.cmsLeg(0.55, 0.90 - 0.036 * (len(histos) + 1), 0.94, 0.90, textSize=0.026)
    leg.SetHeader(title)
    for h, label, color in histos:
        CMS.cmsDraw(h, "HIST", lcolor=color, lwidth=2, fstyle=0, marker=0)
        leg.AddEntry(h, label, "l")
    line = ROOT.TLine(1.0, 3e-5, 1.0, ymax * 2)
    CMS.cmsDrawLine(line, lcolor=ROOT.kGray + 1, lstyle=ROOT.kDotted, lwidth=2)
    c.RedrawAxis()
    save(c, outname)


def get_weights(snapname):
    """Event weights with and without SFbtag_nominal and nGoodJet of one snapshot, as numpy arrays."""
    rdf  = ROOT.RDataFrame("events_nominal", os.path.join(args.indir, f"snap_{snapname}.root"))
    cols = rdf.AsNumpy(["w_noTrotaSF", "SFbtag_nominal", "nGoodJet"])
    w_with    = cols["w_noTrotaSF"].astype("float64")
    w_without = w_with / cols["SFbtag_nominal"].astype("float64")
    return w_with, w_without, cols["nGoodJet"].astype(int)


def weight_histo(w, name):
    """Normalized histogram of the event weight, under/overflow in the first/last bin."""
    w_bw = (w_xmax - w_xmin) / w_nbins
    h    = ROOT.TH1D(name, "", w_nbins, w_xmin, w_xmax)
    h.SetDirectory(0)
    w_clipped = np.clip(w, w_xmin + 0.5 * w_bw, w_xmax - 0.5 * w_bw)
    h.FillN(len(w_clipped), w_clipped, np.ones(len(w_clipped)))
    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())
    return h


def r_factor(w_with, w_without):
    """r = sum(w without SF) / sum(w with SF) and its statistical error (linearization of the ratio, same events)."""
    x, y = w_without.sum(), w_with.sum()
    r    = x / y
    var  = (np.sum(w_without**2) - 2 * r * np.sum(w_without * w_with) + r**2 * np.sum(w_with**2)) / y**2
    return r, np.sqrt(max(var, 0.))


def r_vs_nGoodJet(w_with, w_without, nj):
    """Graph of r per nGoodJet (last point >= nj_max), points with less than nj_minevents events skipped."""
    xs, rs, ers = [], [], []
    for n in range(0, nj_max + 1):
        sel = (nj >= n) if n == nj_max else (nj == n)
        if sel.sum() < nj_minevents:
            continue
        r, er = r_factor(w_with[sel], w_without[sel])
        xs.append(n); rs.append(r); ers.append(er)
    return np.array(xs, dtype="float64"), np.array(rs), np.array(ers)


def draw_r(points, title, outname):
    """points: list of (xs, rs, ers, legend label, color); one marker per process, slightly shifted in x."""
    setup_cms()
    c    = CMS.cmsCanvas(outname, -0.5, nj_max + 0.5, 0.5, 1.4, "nGoodJet",
                         "r = #Sigma w_{no SF} / #Sigma w_{SF}", square=False, iPos=0, extraSpace=0.02, yTitOffset=1.0)
    leg  = CMS.cmsLeg(0.55, 0.90 - 0.036 * (len(points) + 1), 0.94, 0.90, textSize=0.026)
    leg.SetHeader(title)
    graphs = []
    for i, (xs, rs, ers, label, color) in enumerate(points):
        shift = (i - 0.5 * (len(points) - 1)) * 0.08
        g     = ROOT.TGraphErrors(len(xs), xs + shift, rs, np.zeros(len(xs)), ers)
        CMS.cmsDraw(g, "PE", mcolor=color, lcolor=color, msize=1.0)
        leg.AddEntry(g, label, "pe")
        graphs.append(g)
    line = ROOT.TLine(-0.5, 1.0, nj_max + 0.5, 1.0)
    CMS.cmsDrawLine(line, lcolor=ROOT.kGray + 1, lstyle=ROOT.kDashed, lwidth=2)
    # integer labels centered on the points, the last one is >= nj_max
    xaxis = CMS.GetCmsCanvasHist(c).GetXaxis()
    xaxis.Set(nj_max + 1, -0.5, nj_max + 0.5)
    for n in range(nj_max + 1):
        xaxis.SetBinLabel(n + 1, f"#geq{n}" if n == nj_max else str(n))
    xaxis.SetLabelSize(0.05)
    c.RedrawAxis()
    save(c, outname)


# 1) the 5 backgrounds of each era
for era in ("2023", "2024"):
    histos = []
    for (proc, label, snaps), color in zip(processes, colors_5):
        h, n, mean, std = get_histo(snaps[era])
        histos.append((h, f"{label}, mean {mean:.2f}", color))
    draw(histos, f"{era}, preselection (1 file)", f"SFbtag_{era}_5components")

# 2) each process, 2023 vs 2024
for proc, label, snaps in processes:
    histos = []
    for era in ("2023", "2024"):
        h, n, mean, std = get_histo(snaps[era])
        histos.append((h, f"{era}, mean {mean:.2f}", colors_era[era]))
    draw(histos, f"{label}, preselection (1 file)", f"SFbtag_{proc}_2023vs2024")

# 3) event weight with and without SFbtag_nominal, each process and era
for era in ("2023", "2024"):
    for proc, label, snaps in processes:
        w_with, w_without, nj = get_weights(snaps[era])
        r, er  = r_factor(w_with, w_without)
        histos = [(weight_histo(w_with,    f"hw_{proc}_{era}_with"),    f"with SFbtag, mean {w_with.mean():.2f}",       colors_w["with"]),
                  (weight_histo(w_without, f"hw_{proc}_{era}_without"), f"without SFbtag, mean {w_without.mean():.2f}", colors_w["without"])]
        draw(histos, f"{label} {era}, r = {r:.3f} #pm {er:.3f}", f"EventWeight_{proc}_{era}",
             x_range=(w_xmin, w_xmax), xtitle="Event weight (w_noTrotaSF)", bw=(w_xmax - w_xmin) / w_nbins)

# 4) r vs nGoodJet, the 5 backgrounds of each era
for era in ("2023", "2024"):
    points = []
    for (proc, label, snaps), color in zip(processes, colors_5):
        w_with, w_without, nj = get_weights(snaps[era])
        r, er  = r_factor(w_with, w_without)
        print(f"{era} {proc:22s} r = {r:.4f} +- {er:.4f}")
        xs, rs, ers = r_vs_nGoodJet(w_with, w_without, nj)
        points.append((xs, rs, ers, f"{label}, r = {r:.3f}", color))
    draw_r(points, f"{era}, preselection (1 file)", f"rBTag_vs_nGoodJet_{era}")
