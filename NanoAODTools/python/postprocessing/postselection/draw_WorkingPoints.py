import os
import ROOT
import copy
import loadHists
import cmsstyle as CMS
import sys
sys.path.append('../')
from variables import *

ROOT.gROOT.SetBatch()

remoteFolderPath = "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_March26_TaggerWorkingPoints"
year             = 2023
TopCand          = "Resolved"
inFilePath       = f"{remoteFolderPath}/plotsCollected.root"
if not os.path.exists(inFilePath):
    print(f"File {inFilePath} does not exist. Exiting...")
    exit(1)
else:
    # inFile       = ROOT.TFile.Open(inFilePath, "READ")
    histoDict    = loadHists.loadHists(inFilePath)
color_map        = {
                    "topmatched":   ROOT.TColor.GetColor("#5790fc"),
                    "nonmatched":   ROOT.TColor.GetColor("#e42536"),
                    "other":        ROOT.TColor.GetColor("#964a8b"),
                    }


var                  = f"BestTop{TopCand}_score"
title                = f"Best Top {TopCand} score"


####### Draw working points + cumulative distributions ####### 
CMS.SetExtraText("Private Work")
CMS.SetLumi("")
CMS.SetEnergy("")
CMS.ResetAdditionalInfo()
c                    = CMS.cmsCanvas(
                                        title,
                                        0.0,
                                        1.0,
                                        0.0,
                                        1.0,
                                        title,
                                        "1-cumulative",
                                        square=CMS.kRectangular,
                                        iPos=0
                                    )
leg                  = CMS.cmsLeg(0.57, 0.83, 0.92, 0.67, textSize=0.025)
leg.AddEntry("None", "2023 Working Points", "")

for i,proc in enumerate(color_map):
    histoName        = f"{var}_top{TopCand}_{proc}"
    histo            = copy.deepcopy(histoDict[histoName])
    histo.Scale(1./histo.Integral())
    histo = histo.GetCumulative(forward=ROOT.kFALSE)
    CMS.cmsDraw(histo, "PE", mcolor=color_map[proc])
    leg.AddEntry(histo, proc, "PE")

####### Find working points for topmatched and nonmatched+other ####### 
histo            = copy.deepcopy(histoDict[f"{var}_top{TopCand}_nonmatched"])
histo.Add(copy.deepcopy(histoDict[f"{var}_top{TopCand}_other"]))
histo.Scale(1./histo.Integral())
histo            = histo.GetCumulative(forward=ROOT.kFALSE)
CMS.cmsDraw(histo, "PE", mcolor=ROOT.TColor.GetColor("#e76300"))
leg.AddEntry(histo, "nonmatched+other", "PE")
thr_L = None
bin_L = None
thr_T = None
bin_T = None
for i in range(1, histo.GetNbinsX()+1):
    if (histo.GetBinContent(i) < 0.1):
        if bin_L is None:
            bin_L       = i-1
        elif (histo.GetBinContent(i) < 0.05) and (bin_T is None):
            bin_T       = i-1

thr_L               = histo.GetXaxis().GetBinUpEdge(bin_L)
thr_T               = histo.GetXaxis().GetBinUpEdge(bin_T)
fpr_L               = histo.GetBinContent(bin_L)
fpr_T               = histo.GetBinContent(bin_T)

histo               = copy.deepcopy(histoDict[f"{var}_top{TopCand}_topmatched"])
histo.Scale(1./histo.Integral())
histo               = histo.GetCumulative(forward=ROOT.kFALSE)
tpr_L               = histo.GetBinContent(bin_L)
tpr_T               = histo.GetBinContent(bin_T)
print("\n")
print(f"Working point L for nonmatched+other:                 {thr_L:.3f} @ {100*fpr_L:.1f}%")
print(f"Working point L for topmatched:                       {100*tpr_L:.1f}%")
print(f"Working point T for nonmatched+other:                 {thr_T:.3f} @ {100*fpr_T:.1f}%")
print(f"Working point T for topmatched:                       {100*tpr_T:.1f}%")


WPL_line = ROOT.TLine(thr_L, 0.0, thr_L, 1.0)
CMS.cmsDrawLine(WPL_line, lcolor=ROOT.kRed, lstyle=ROOT.kDashed)
leg.AddEntry(WPL_line, f"WP_L: tpr={100*tpr_L:.1f}% @ fpr={100*fpr_L:.1f}%", "L")
WPT_line = ROOT.TLine(thr_T, 0.0, thr_T, 1.0)
CMS.cmsDrawLine(WPT_line, lcolor=ROOT.kGreen+1, lstyle=ROOT.kDashed)
leg.AddEntry(WPT_line, f"WP_T: tpr={100*tpr_T:.1f}% @ fpr={100*fpr_T:.1f}%", "L")


latex    = ROOT.TLatex()
latex.SetTextFont(52)
latex.SetTextSize(0.025)
latex.SetTextColor(ROOT.kRed)
latex.DrawLatexNDC(thr_L+0.1, 0.83, f"{thr_L:.3f}")

latex    = ROOT.TLatex()
latex.SetTextFont(52)
latex.SetTextSize(0.025)
latex.SetTextColor(ROOT.kGreen+1)
latex.DrawLatexNDC(thr_T+0.02, 0.78, f"{thr_T:.3f}")


c.SaveAs(f"{remoteFolderPath}/{var}.pdf")