# BTV normalization factor of the b-tag shape SF: r = sum(w without SFbtag) / sum(w with SFbtag),
# per background process (sum of its components) and inclusive (sum of all the processes), vs the jet multiplicity.
# Input: the step-2 production with --weightset allWeights --weightset noSFbtag --noTrotaSF --varfile ../variables_btagSFr.py
#   <indir>/noTrotaSF/plots/<component>.root          (all weights, b-tag SF included)
#   <indir>/noSFbtag_noTrotaSF/plots/<component>.root (all weights except the b-tag SF)
# The histograms are already scaled to sigma*lumi/N_tot per component, so components and processes are summed directly.
# Output in <outdir> (default <indir>/r_plots):
#   - rBTag_vs_<var>_<era>_<region>.png/pdf : r per bin of <var>, one marker per process, inclusive in black
#   - rBTag_<era>.json                      : {region: {var: {process: {"integrated": [r, err], "bins": {...}}}}}
# Errors: the two histograms are treated as uncorrelated (TH1::Divide), which overestimates the error
# (same events in numerator and denominator), so they are conservative.
# Integrals over bins 1..N: merge_UnOvFlow puts the overflow in the last bin and leaves the overflow bin filled.
#
# Usage: python3 compute_rBTag.py [--indir <production folder>] [--outdir <folder>] [--era 2023]

import os
import json
import argparse
import importlib
import ROOT
import cmsstyle as CMS
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import sample_dict

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("--indir",  default="/eos/user/l/lfavilla/RDF_DManalysis/results/2023/btagSF_r_study")
parser.add_argument("--outdir", default=None, help="default: <indir>/r_plots")
parser.add_argument("--era",    default="2023")
args   = parser.parse_args()
outdir = args.outdir if args.outdir is not None else os.path.join(args.indir, "r_plots")
os.makedirs(outdir, exist_ok=True)

era        = args.era
ws_SF      = "noTrotaSF"            # weightset allWeights
ws_noSF    = "noSFbtag_noTrotaSF"   # weightset noSFbtag
variables  = {"nGoodJet": "nGoodJet", "nJet": "nJet"}
regions    = {"MET250": "p_{T}^{miss} > 250 GeV", "btagSFcheck": "btagSFcheck"}

# process (dataset in sample_dict) -> legend label and color
processes = [
    (f"TT_{era}",                   "t#bar{t}",       CMS.p6.kBlue),
    (f"TW_{era}",                   "tW",             CMS.p6.kYellow),
    (f"QCD_{era}",                  "QCD",            CMS.p6.kRed),
    (f"ZJetsToNuNu_2jets_{era}",    "Z(#nu#nu)+jets", CMS.p6.kGrape),
    (f"WJets_2jets_{era}",          "W(l#nu)+jets",   CMS.p6.kGray),
]
inclusive = (f"inclusive_{era}", "All backgrounds", ROOT.kBlack)


def get_component_histo(ws, component, hname):
    """Histogram <hname> of one component in one weightset, detached from the file."""
    fname = os.path.join(args.indir, ws, "plots", f"{component}.root")
    f     = ROOT.TFile.Open(fname)
    h     = f.Get(hname)
    if not h:
        raise RuntimeError(f"{hname} not found in {fname}")
    h     = h.Clone(f"{hname}_{ws}_{component}")
    h.SetDirectory(0)
    f.Close()
    return h


def get_process_histo(ws, dataset, hname):
    """Sum of the histogram <hname> over all the components of a dataset."""
    h_sum = None
    for comp in sample_dict[dataset].components:
        h = get_component_histo(ws, comp.label, hname)
        if h_sum is None:
            h_sum = h.Clone(f"{hname}_{ws}_{dataset}")
            h_sum.SetDirectory(0)
        else:
            h_sum.Add(h)
    return h_sum


def r_integrated(h_SF, h_noSF):
    """r over bins 1..N and its error, numerator and denominator treated as uncorrelated."""
    n          = h_SF.GetNbinsX()
    y_SF, e_SF     = integral_and_error(h_SF, 1, n)
    y_noSF, e_noSF = integral_and_error(h_noSF, 1, n)
    r          = y_noSF / y_SF
    er         = r * ((e_noSF / y_noSF) ** 2 + (e_SF / y_SF) ** 2) ** 0.5
    return r, er, y_SF, y_noSF


def integral_and_error(h, b1, b2):
    """Integral and its error from Sumw2, over bins b1..b2."""
    y = h.Integral(b1, b2)
    e = sum(h.GetBinError(b) ** 2 for b in range(b1, b2 + 1)) ** 0.5
    return y, e


def r_per_bin(h_SF, h_noSF):
    """Histogram of r per bin (TH1::Divide, uncorrelated errors)."""
    h_r = h_noSF.Clone(h_noSF.GetName() + "_r")
    h_r.SetDirectory(0)
    h_r.Divide(h_SF)
    return h_r


def setup_cms():
    # works with cmsstyle 0.5.0 (~/.local) and 0.4.3 (myvenv_lcg107, the env of analysis_TPrime.sh, needed for sample_dict)
    CMS.SetExtraText("Private Work")
    try:
        CMS.SetLumi(None, run="Run 3")
    except TypeError:
        # 0.4.3: SetLumi has no run argument, the text is the module global cms_lumi
        importlib.import_module("cmsstyle.cmsstyle").cms_lumi = "Run 3"
    CMS.SetEnergy(13.6)
    CMS.ResetAdditionalInfo()


def get_frame(c):
    """Axis frame of a cmsCanvas (GetCmsCanvasHist in 0.5.0, GetcmsCanvasHist in 0.4.3)."""
    getter = getattr(CMS, "GetCmsCanvasHist", None) or getattr(CMS, "GetcmsCanvasHist")
    return getter(c)


def save(c, outname):
    for ext in ("png", "pdf"):
        c.SaveAs(os.path.join(outdir, f"{outname}.{ext}"))
    c.Close()


def draw_r(points, xtitle, title, outname):
    """points: list of (h_r, legend label, color); one marker per bin with SF yield > 0, slightly shifted in x."""
    setup_cms()
    h0    = points[0][0]
    nbins = h0.GetNbinsX()
    x_lo  = h0.GetXaxis().GetXmin()
    x_hi  = h0.GetXaxis().GetXmax()
    c     = CMS.cmsCanvas(outname, x_lo, x_hi, 0.4, 1.4, xtitle,
                          "r = #Sigma w_{no SF} / #Sigma w_{SF}", square=False, iPos=0, extraSpace=0.02, yTitOffset=1.0)
    leg   = CMS.cmsLeg(0.55, 0.90 - 0.036 * (len(points) + 1), 0.94, 0.90, textSize=0.026)
    leg.SetHeader(title)
    graphs = []
    for i, (h_r, label, color) in enumerate(points):
        shift = (i - 0.5 * (len(points) - 1)) * 0.1
        g     = ROOT.TGraphErrors()
        for b in range(1, nbins + 1):
            if h_r.GetBinContent(b) <= 0:
                continue
            ip = g.GetN()
            g.SetPoint(ip, h_r.GetBinCenter(b) + shift, h_r.GetBinContent(b))
            g.SetPointError(ip, 0., h_r.GetBinError(b))
        CMS.cmsDraw(g, "PE", mcolor=color, lcolor=color, msize=1.0)
        leg.AddEntry(g, label, "pe")
        graphs.append(g)
    line = ROOT.TLine(x_lo, 1.0, x_hi, 1.0)
    CMS.cmsDrawLine(line, lcolor=ROOT.kGray + 1, lstyle=ROOT.kDashed, lwidth=2)
    # integer labels centered on the bins, the last one contains the overflow
    xaxis = get_frame(c).GetXaxis()
    xaxis.Set(nbins, x_lo, x_hi)
    for b in range(1, nbins + 1):
        n = int(round(h0.GetBinCenter(b)))
        xaxis.SetBinLabel(b, f"#geq{n}" if b == nbins else str(n))
    xaxis.SetLabelSize(0.05)
    c.RedrawAxis()
    save(c, outname)


results     = {}
r_inclusive = {}    # (region, var) -> (histogram of r per bin, integrated r) of all the backgrounds
for reg, reg_title in regions.items():
    results[reg] = {}
    for var in variables:
        hname  = f"{var}_{reg}"
        results[reg][var] = {}
        points = []
        h_SF_incl, h_noSF_incl = None, None
        print(f"\n===== {era} {reg} {var}")
        print(f"{'process':28s} {'yield SF':>12s} {'yield noSF':>12s} {'r':>8s} {'err':>8s}")
        for dataset, label, color in processes + [inclusive]:
            if dataset == inclusive[0]:
                h_SF, h_noSF = h_SF_incl, h_noSF_incl
            else:
                h_SF   = get_process_histo(ws_SF,   dataset, hname)
                h_noSF = get_process_histo(ws_noSF, dataset, hname)
                if h_SF_incl is None:
                    h_SF_incl, h_noSF_incl = h_SF.Clone(f"{hname}_SF_incl"), h_noSF.Clone(f"{hname}_noSF_incl")
                    h_SF_incl.SetDirectory(0); h_noSF_incl.SetDirectory(0)
                else:
                    h_SF_incl.Add(h_SF); h_noSF_incl.Add(h_noSF)
            r, er, y_SF, y_noSF = r_integrated(h_SF, h_noSF)
            h_r = r_per_bin(h_SF, h_noSF)
            print(f"{dataset:28s} {y_SF:12.1f} {y_noSF:12.1f} {r:8.4f} {er:8.4f}")
            bins = {}
            for b in range(1, h_r.GetNbinsX() + 1):
                if h_SF.GetBinContent(b) <= 0:
                    continue
                n = int(round(h_r.GetBinCenter(b)))
                key = f">={n}" if b == h_r.GetNbinsX() else str(n)
                bins[key] = [h_r.GetBinContent(b), h_r.GetBinError(b)]
            results[reg][var][dataset] = {"integrated": [r, er], "yield_SF": y_SF, "yield_noSF": y_noSF, "bins": bins}
            points.append((h_r, f"{label}, r = {r:.3f}", color))
            if dataset == inclusive[0]:
                r_inclusive[(reg, var)] = (h_r, r)
        draw_r(points, variables[var], f"{era}, {reg_title}", f"rBTag_vs_{var}_{era}_{reg}")

# inclusive r (all backgrounds) vs jet multiplicity: nGoodJet and nJet in each region, and the two regions for each variable
colors_var = {"nGoodJet": CMS.p6.kBlue, "nJet": CMS.p6.kRed}
colors_reg = {"MET250": CMS.p6.kBlue, "btagSFcheck": CMS.p6.kRed}
for reg, reg_title in regions.items():
    points = [(r_inclusive[(reg, var)][0], f"{var}, r = {r_inclusive[(reg, var)][1]:.3f}", colors_var[var]) for var in variables]
    draw_r(points, "Jet multiplicity", f"All backgrounds {era}, {reg_title}", f"rBTag_inclusive_vs_jetMultiplicity_{era}_{reg}")
for var in variables:
    points = [(r_inclusive[(reg, var)][0], f"{regions[reg]}, r = {r_inclusive[(reg, var)][1]:.3f}", colors_reg[reg]) for reg in regions]
    draw_r(points, variables[var], f"All backgrounds {era}", f"rBTag_inclusive_vs_{var}_{era}_regions")

with open(os.path.join(outdir, f"rBTag_{era}.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"\nPlots and json in {outdir}")
