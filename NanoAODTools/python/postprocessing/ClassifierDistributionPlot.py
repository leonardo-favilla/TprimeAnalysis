import ROOT, os, copy
import cmsstyle as CMS
import optparse
from array import array
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

usage = 'python3 ClassifierDistributionPlot.py -i sample'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--inputFile', dest='inputFile', type=str, default = '', help='Please enter the sample')
# parser.add_option('-o','--outputFolder', dest='outputFolder', type = str, default="/eos/home-a/acagnott/www/", help='default save all plots in eos/../www/')
(opt, args) = parser.parse_args()

sample = opt.inputFile #"ttsemilep" "Zprime"


file = ROOT.TFile.Open("output_TopMatchingStudies_"+sample+"_noResinMix.root")

if os.path.exists("trota.root"):
    output_file = ROOT.TFile("trota.root", "UPDATE")
else:
    output_file = ROOT.TFile("trota.root", "RECREATE")

if "ttsemilep"  in sample: 
    samplelabel = "t#bar{t} semilep"
    if not output_file.GetDirectory("ttsemilep"):
        output_file.mkdir("ttsemilep")
    # else:
    #     directory = output_file.GetDirectory("ttsemilep")
elif "Zprime" in sample: 
    samplelabel = "Z' 4tops"
    if not output_file.GetDirectory("Zprime"):
        output_file.mkdir("Zprime")
    # else:
    #     directory = output_file.GetDirectory("Zprime")


xbins = array('d', [i * (1.0 / 30) for i in range(31)])
nxbins = len(xbins) - 1

h_scoreRes = file.Get("h_topresolvedscore_HighestScoreMixXtopgen")
h_scoreRes = h_scoreRes.Rebin(50)
h_scoreRes.Scale(1/h_scoreRes.Integral())

h_scoreMix = file.Get("h_topmixedscore_HighestScoreMixXtopgen")
h_scoreMix = h_scoreMix.Rebin(50)
h_scoreMix.Scale(1/h_scoreMix.Integral())

h_scoreMer = file.Get("h_topmergedscore_HighestScoreMixXtopgen")
h_scoreMer = h_scoreMer.Rebin(50)
h_scoreMer.Scale(1/h_scoreMer.Integral())

h = {"Resolved": h_scoreRes, "Mixed": h_scoreMix, "Merged": h_scoreMer}
color = {"Resolved": ROOT.TColor.GetColor("#92dadd"), "Mixed": ROOT.TColor.GetColor("#ffa90e"), "Merged": ROOT.TColor.GetColor("#bd1f01")}

dir = output_file.GetDirectory(sample)
dir.cd()
if not dir.GetDirectory("ClassifierDistribution"):
    subdir = dir.mkdir("ClassifierDistribution")
else:
    subdir = dir.GetDirectory("ClassifierDistribution")
for t in h.keys():
    tmp = copy.deepcopy(h[t])
    tmp.SetName(f"ClassifierDistributionInclusive_{t}")
    subdir.cd()
    tmp.Write()
output_file.Close()

for t in h.keys():
    # CMS.SetExtraText(extraTest)
    iPos = 0
    canv_name = "classifierdistributionInclusive"+t
    CMS.SetLumi("")
    CMS.SetEnergy("13")
    CMS.ResetAdditionalInfo()

    x_min = 0
    x_max = 1
    y_min = 0
    y_max = h[t].GetMaximum()+0.3#, h_scoreMix.GetMaximum(), h_scoreMer.GetMaximum())
    # y_max = y_max + 0.3 * (y_max - y_min)
    x_axis_name = "Top "+t+" Score"
    y_axis_name = "arbitrary units"
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,y_axis_name,square=CMS.kRectangular,extraSpace=20, iPos=iPos)
    # canv.SetLogx()
    # leg = CMS.cmsLeg(0.5, 0.2, 0.9, 0.4, textSize=0.03)
    # CMS.cmsDraw(roc_mix, "", lcolor = ROOT.TColor.GetColor("#ffa90e"), lwidth=2)
    # leg.AddEntry(roc_mix, "Mixed (AUC = {:.4f})".format(auc_mix), "l")
    # CMS.cmsDraw(roc_res, "", lcolor = ROOT.TColor.GetColor("#92dadd"), lwidth=2)
    # leg.AddEntry(roc_res, "Resolved (AUC = {:.4f})".format(auc_res), "l")
    # CMS.cmsDraw(roc_mer, "", lcolor = ROOT.TColor.GetColor("#bd1f01"), lwidth=2)
    # leg.AddEntry(roc_mer, "Merged (AUC = {:.4f})".format(auc_mer), "l")

    CMS.cmsDraw(h[t], "hist", lcolor = color[t], fcolor = ROOT.kWhite, lwidth=2)
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.SetTextAlign(22)
    latex.DrawLatexNDC(0.25, 0.85, samplelabel)
    if "tt" in sample:
        CMS.SaveCanvas(canv, "/eos/home-a/acagnott/www/TopMatchingStudies/tt_semilep_noResinMix/"+canv_name+".png", close=False)
        CMS.SaveCanvas(canv, "/eos/home-a/acagnott/www/TopMatchingStudies/tt_semilep_noResinMix/"+canv_name+".pdf")
    else:
        CMS.SaveCanvas(canv, "/eos/home-a/acagnott/www/TopMatchingStudies/"+sample+"_noResinMix/"+canv_name+".png", close=False)
        CMS.SaveCanvas(canv, "/eos/home-a/acagnott/www/TopMatchingStudies/"+sample+"_noResinMix/"+canv_name+".pdf")

output_file = ROOT.TFile("trota.root", "UPDATE")
dir = output_file.GetDirectory(sample)
subdir = dir.GetDirectory("ClassifierDistribution")
subdir.cd()

for t in h.keys():        
    h2d = file.Get("h_top" + t.lower() + "scorePt_HighestScoreMixXtopgen")

    h1d_list = []
    for xbin in range(1, h2d.GetNbinsY() + 1):
        h1d = h2d.ProjectionX(f"h1d_{xbin}_{t}", xbin, xbin)
        h1d = h1d.Rebin(50)
        h1d.Scale(1 / h1d.Integral() if h1d.Integral() != 0 else 1)
        h1d_list.append(h1d)
        subdir.cd()
        tmp = copy.deepcopy(h1d)
        tmp.SetName(f"ClassifierDistribution_{t}_PtBin{xbin-1}")
        tmp.Write()

    for idx, h1d in enumerate(h1d_list):
        iPos = 0
        canv_name = "classifierdistributionInclusive"+t
        CMS.SetLumi("")
        CMS.SetEnergy("13")
        CMS.ResetAdditionalInfo()
        canv_name = f"classifierdistribution{t}PtBin{idx}"
        y_max = h1d.GetMaximum() + 0.3
        canv = CMS.cmsCanvas(canv_name, x_min, x_max, y_min, y_max, x_axis_name, y_axis_name, square=CMS.kRectangular, extraSpace=20, iPos=iPos)
        CMS.cmsDraw(h1d, "hist", lcolor=color[t], fcolor=ROOT.kWhite, lwidth=2)
        latex.DrawLatexNDC(0.25, 0.85, f"{samplelabel} - Pt bin {idx}")
        if "tt" in sample:
            CMS.SaveCanvas(canv, f"/eos/home-a/acagnott/www/TopMatchingStudies/tt_semilep_noResinMix/{canv_name}.png", close=False)
            CMS.SaveCanvas(canv, f"/eos/home-a/acagnott/www/TopMatchingStudies/tt_semilep_noResinMix/{canv_name}.pdf")
        else:
            CMS.SaveCanvas(canv, f"/eos/home-a/acagnott/www/TopMatchingStudies/{sample}_noResinMix/{canv_name}.png", close=False)
            CMS.SaveCanvas(canv, f"/eos/home-a/acagnott/www/TopMatchingStudies/{sample}_noResinMix/{canv_name}.pdf")