import ROOT
import cmsstyle as CMS
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

inFilePath      = "/eos/user/a/acagnott/DarkMatter/nosynch/run2022_Jan26/plots/TT_dilep_2022.root"
var             = "LeadingJetPt_pt"
r               = "AH"
histo_nominal   = f"{var}_{r}_nominal"
histo_up        = f"{var}_{r}_FSR_up"
histo_down      = f"{var}_{r}_FSR_down"
histo_stat      = f"{var}_{r}_stat"
histo_syst      = f"{var}_{r}_syst"
histo_err       = f"{var}_{r}_err"

f               = ROOT.TFile.Open(inFilePath)
h_nom           = f.Get(histo_nominal)
h_up            = f.Get(histo_up)
h_down          = f.Get(histo_down)
h_stat          = h_nom.Clone("h_stat")
h_syst          = h_nom.Clone("h_syst")
# h_err           = h_nom.Clone("h_err")
# h_err.Reset()
# h_err.SetDirectory(0)
h_syst.Reset()
# h_syst.SetDirectory(0)
for i in range(1, h_nom.GetNbinsX()+1):
    nom         = h_nom.GetBinContent(i)
    up          = h_up.GetBinContent(i)
    down        = h_down.GetBinContent(i)
    err_syst    = abs(up - down) / 2.0
    err_stat    = h_stat.GetBinError(i)
    err_tot     = (err_syst**2 + err_stat**2)**0.5

    h_syst.SetBinContent(i, nom)
    h_syst.SetBinError(i, err_syst)
    # h_err.SetBinContent(i, nom)
    # h_err.SetBinError(i, err_tot)

canv = CMS.cmsCanvas(
                        canvName=f"{var}_{r}",
                        x_min=0,
                        x_max=1000,
                        y_min=0,
                        y_max=h_up.GetMaximum()*1.4,
                        nameXaxis="Leading Jet p_{T} [GeV]",
                        nameYaxis="Normalized Events",
                        square=CMS.kRectangular,
                        extraSpace=0.1,
                        iPos=0
                        )

CMS.cmsDraw(h_up,       "hist",    fcolor=ROOT.kRed,    fstyle=0,   lcolor=ROOT.kRed,   lwidth=2)
CMS.cmsDraw(h_nom,      "hist",    fcolor=ROOT.kGreen,              lcolor=ROOT.kGreen, lwidth=2)
CMS.cmsDraw(h_down,     "hist",    fcolor=ROOT.kBlue,   fstyle=0,   lcolor=ROOT.kBlue,  lwidth=2)
CMS.cmsDraw(h_syst,     "e2same0", fcolor=ROOT.kGray+3, fstyle=3004, msize=0)
# CMS.cmsDraw(h_err,      "e2same0", fcolor=ROOT.kGray+3, fstyle=3004)

CMS.SaveCanvas(canv, f"{var}_{r}" + ".png",  close=True)