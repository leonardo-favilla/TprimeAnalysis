import sys
sys.path.append('../')
import ROOT
import os
import cmsstyle
from samples.samples import *
import json
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

lumi = 62.41 # fb-1
def createcanv(name_canv ):
    ############ CREATE CANVAS AND PADS ############ 
    cmsstyle.SetEnergy(13.6)
    cmsstyle.SetLumi(lumi,"fb","",1)
    cmsstyle.SetExtraText("")
    # Scientific notation
    # hdf = cmsstyle.GetcmsCanvasHist(canv)
    # hdf.GetYaxis().SetMaxDigits(2)
    # Shift multiplier position
    # ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    canv = cmsstyle.cmsCanvas(name_canv, -0.5, 5.5, -0.5, 5.5, "# Top Mixed", "# Top Resolved", square=True, with_z_axis=True, iPos=0)
    # canv.SetLeftMargin(0.15)
    # canv.SetBottomMargin(0.15)
    # canv.SetRightMargin(0.15)
    # canv.SetTopMargin(0.15)
    return canv

with open("../samples/dict_samples_2023.json", "r") as f:
    filejson = json.load(f)
samples = []

folder = "/eos/user/a/acagnott/DarkMatter/nosynch/run2023_Jan26/plots/"
filelist = []
for filename in os.listdir(folder):
    if not filename.endswith("_2D.root"):
        continue
    filepath = os.path.join(folder, filename)
    samples.append(filename.replace("_2D.root",""))
    filelist.append(filepath)

samples = [sample_dict[sample] for sample in samples if sample in sample_dict]
ntot = [sum(filejson[sample.label][sample.label]["ntot"]) for sample in samples if sample.label in filejson]

for t in ["0TopMer", "1TopMer"]:
    canv = createcanv(f"NtopResVsNtopMixVs{t}_bkg")

    histogram_fin_bkg = ROOT.TH2D("", "", 6, -0.5, 5.5, 6, -0.5, 5.5)

    for filepath, sample, n in zip(filelist, samples, ntot):
        if "Tprime" in filepath:
            continue
        histname = f"nTightTopMixedVsnTightTopResolved_incl_{t}"
        print("Loading histogram:", histname, "from file:", filepath)
        file = ROOT.TFile.Open(filepath)
        hist = file.Get(histname)
        xsec = sample.sigma if sample.sigma is not None else 1.0
        nev = n if n > 0 else 1.0
        print(hist)
        histogram_fin_bkg.Add(hist)
        hist.Scale(xsec * 10**3 * lumi / nev)
        if hist is None:
            print(f"Histogram {histname} not found in file {filepath}")
            continue
        file.Close()
    h1 = histogram_fin_bkg.Clone()
    h1.Scale(1.0 / histogram_fin_bkg.Integral())

    cmsstyle.SetAlternative2DColor(h1)

    cmsstyle.cmsObjectDraw(h1,f"COLZ text")
    cmsstyle.SaveCanvas(canv, folder+f"NtopResVsNtopMixVs{t}_bkg.png",  close=False)
    cmsstyle.SaveCanvas(canv, folder+f"NtopResVsNtopMixVs{t}_bkg.pdf")

    histogram_fin ={}
    for filepath, sample, n in zip(filelist, samples, ntot):
        if "Tprime" not in filepath:
            continue
        canv = createcanv(f"NtopResVsNtopMixVs{t}_{sample.label}")
        histogram_fin[sample.label] = ROOT.TH2D("", "", 6, -0.5, 5.5, 6, -0.5, 5.5)
        histname = f"nTightTopMixedVsnTightTopResolved_incl_{t}"
        # hist = load_2Dhist(filepath, histname)
        file = ROOT.TFile.Open(filepath)
        hist = file.Get(histname)
        xsec = sample.sigma if sample.sigma is not None else 1.0
        nev = n if n > 0 else 1.0
        hist.Scale(xsec * 10**3 * lumi / nev)
        if hist is None:
            print(f"Histogram {histname} not found in file {filepath}")
            continue
        print(hist)
        histogram_fin[sample.label].Add(hist)
        h1 = histogram_fin[sample.label].Clone()
        h1.Scale(1.0 / histogram_fin[sample.label].Integral())

        cmsstyle.SetAlternative2DColor(h1)

        cmsstyle.cmsObjectDraw(h1,f"COLZ text")
        cmsstyle.SaveCanvas(canv, folder+f"NtopResVsNtopMixVs{t}_{sample.label}.png",  close=False)
        cmsstyle.SaveCanvas(canv, folder+f"NtopResVsNtopMixVs{t}_{sample.label}.pdf")
        file.Close()

    for i in range(1, histogram_fin_bkg.GetNbinsX() + 1):
        for j in range(1, histogram_fin_bkg.GetNbinsY() + 1):
            content = histogram_fin_bkg.GetBinContent(i, j)
            if content > 0:
                histogram_fin_bkg.SetBinContent(i, j, content**0.5)

    for k in histogram_fin.keys():
        canv = createcanv(f"NtopResVsNtopMixVs{t}_{k}_significance")
        hist_significance = histogram_fin[k].Clone()
        hist_significance.Divide(histogram_fin_bkg)
        cmsstyle.SetAlternative2DColor(hist_significance)
        cmsstyle.cmsObjectDraw(hist_significance, "COLZ text")
        cmsstyle.SaveCanvas(canv, folder+f"NtopResVsNtopMixVs{t}_{k}_significance.png", close=False)
        cmsstyle.SaveCanvas(canv, folder+f"NtopResVsNtopMixVs{t}_{k}_significance.pdf")