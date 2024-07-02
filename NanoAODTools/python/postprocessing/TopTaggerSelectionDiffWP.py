import ROOT, os
import cmsstyle as CMS  
from samples.samples import *
import copy
import json
# Load the JSON file
with open('./samples/dict_samples.json') as f:
    json_samples = json.load(f)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

if not os.path.exists("/eos/home-a/acagnott/DarkMatter/nosynch/TopTagger_JetMET_selectcomparison/pdf/"):
    os.makedirs("/eos/home-a/acagnott/DarkMatter/nosynch/TopTagger_JetMET_selectcomparison/pdf/")
# CMS.SetExtraText("Simulation Preliminary")
# CMS.SetLumi("")
# canv = CMS.cmsCanvas('', 0, 1, 0, 1, '', '', square = CMS.kSquare, extraSpace=0.01, iPos=0)

def plot(h1, fillcolor, canv_name = "canv" ,extraTest="Simulation", iPos=0, energy="13", lumi = "",  addInfo=""):

    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)

    x_min = h1.GetXaxis().GetXmin()
    x_max = h1.GetXaxis().GetXmax()
    y_min = h1.GetMinimum()
    y_max = h1.GetMaximum()
    y_max = y_max + 0.3 * (y_max - y_min)
    x_axis_name = h1.GetXaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,"Events",square=CMS.kRectangular,extraSpace=1.1, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    CMS.cmsDraw(h1, "", marker= 10 ,lcolor = fillcolor)
    CMS.SaveCanvas(canv, "/eos/home-a/acagnott/DarkMatter/nosynch/TopTagger_JetMET_selectcomparison/pdf/"+canv_name+".pdf")

sample_name = "WJets_2018"
sample = sample_dict[sample_name]
if hasattr(sample, "components"):
    list_of_sample = sample.components
    for wp in ["WPloose", "WPmedium", "WPtight"]:
        hmass, hpt = None, None
        for s in list_of_sample:
            f = ROOT.TFile.Open("/eos/home-a/acagnott/DarkMatter/nosynch/TopTagger_JetMET_selectcomparison/plots/"+s.label+".root")
            hmass_tmp = copy.deepcopy(ROOT.TH1D(f.Get("Top_mass_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")))
            # hmass_.SetName(s.label+"Top_mass_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")
            hpt_tmp   = copy.deepcopy(ROOT.TH1D(f.Get("Top_pt_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")))
            # hpt_.SetName(s.label+"Top_pt_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")
            hmass_tmp.Scale(s.sigma*10**3/json_samples[s.label][s.label]["ntot"][0])
            hpt_tmp.Scale(s.sigma*10**3/json_samples[s.label][s.label]["ntot"][0])
            if hmass==None:
                hmass = hmass_tmp.Clone("")
                # hmass.SetName(sample_name+"Top_mass_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")
                hpt = hpt_tmp.Clone("")
                # hpt.SetName(sample_name+"Top_pt_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")
            else:
                hmass.Add(hmass_tmp)
                hpt.Add(hpt_tmp)
        plot(hmass, ROOT.TColor.GetColor("#94a4a2"), sample_name+"top_mass_"+wp, "Simulation", 11, "13", "1", s.leglabel+" ("+wp+")")
        plot(hpt, ROOT.TColor.GetColor("#94a4a2"), sample_name+"top_pt_"+wp, "Simulation", 11, "13", "1", s.leglabel+" ("+wp+")")
else:
    f = ROOT.TFile.Open("/eos/home-a/acagnott/DarkMatter/nosynch/TopTagger_JetMET_selectcomparison/plots/"+sample.label+".root")

    for wp in ["WPloose", "WPmedium", "WPtight"]:
        hmass = f.Get("Top_mass_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")
        hpt = f.Get("Top_pt_"+wp+"_1TopLep_1TopHadrAll_"+wp+"_")
        hmass.Scale(sample.sigma*10**3/json_samples[sample.label][sample.label]["ntot"][0])
        hpt.Scale(sample.sigma*10**3/json_samples[sample.label][sample.label]["ntot"][0])
        plot(hmass, ROOT.TColor.GetColor("#bd1f01"), sample.label+"top_mass_"+wp, "Simulation", 11, "13", "1", "t#bar{t} semileptonic ("+wp+")")
        plot(hpt, ROOT.TColor.GetColor("#bd1f01"), sample.label+"top_pt_"+wp, "Simulation", 11, "13", "1", "t#bar{t} semileptonic ("+wp+")")
