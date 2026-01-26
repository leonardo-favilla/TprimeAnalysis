import ROOT
import cmsstyle as CMS
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetPalette(57)  # "DeepSea" palette


def make_stack_with_ratio(canv_name, histo_bkg_dict, histo_data=None, histo_signals_dict=None, region=None, xMin=0, xMax=100, yMin=0, yMax=100, rMin=0, rMax=2, xTitle="xTitle", yTitle="yTitle", rTitle="rTitle", extraText="Work in Progress", lumi=1, extraSpace=0.1, iPos=0, logy=False, repo=None, colors_bkg=None, style_signals_dict=None, systErr=False):
    ############ CREATE CANVAS AND PADS ############ 
    CMS.SetExtraText(extraText)
    CMS.SetLumi(lumi)
    CMS.SetEnergy("13.6")
    # Write extra lines below the extra text (usuful to define regions/channels)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(region)

    
    if (logy) and (yMin <= 0):
        print("yMin must be greater than 0 when logy is True.")
        yMin = 1e-1  # Set a small value for yMin to avoid log(0) issues
        print(f"Setting yMin to {yMin} for logarithmic scale.")
    dicanv = CMS.cmsDiCanvas(
                            canv_name,
                            xMin,
                            xMax,
                            yMin,
                            yMax,
                            rMin,
                            rMax,
                            xTitle,
                            yTitle,
                            rTitle,
                            square=CMS.kRectangular,
                            extraSpace=extraSpace,
                            iPos=iPos,
                        )
    ################## PAD1 ##################
    pad1                = dicanv.cd(1)
    # hup                 = CMS.GetcmsCanvasHist(pad1)
    # hup.Draw("hist")
    signals_factor      = 10
    if logy:
        pad1.SetLogy()
        pad1.Update()
        signals_factor  = 1

    leg                 = CMS.cmsLeg(0.4, 0.88, 0.9, 0.67, textSize=0.025, columns=3)
    if region:
        latex           = ROOT.TLatex()
        latex.SetTextFont(52)
        latex.SetTextSize(0.06)
        latex.DrawLatexNDC(0.15, 0.83, f"{region}")

        # CMS.cmsHeader(leg, f"{region}", textSize=0.05)

    ##### Set graphics style for Backgrounds ##### 
    if colors_bkg is not None:
        palette     = colors_bkg
    else:
        palette     = None
    stack           = ROOT.THStack("stack", "Stack Histogram")
    # CMS.cmsDrawStack(stack=stack, legend=leg, MC=histo_bkg_dict, data=histo_data, palette=palette)
    CMS.cmsDrawStack(stack=stack, legend=leg, MC=histo_bkg_dict, data=None, palette=palette)
    if histo_data is not None:
        CMS.cmsDraw(histo_data, "PE", mcolor=ROOT.kBlack)

    h_bkg           = stack.GetStack().Last().Clone("h_bkg")
    CMS.cmsDraw(h_bkg, "e2same0", fcolor=ROOT.kGray+3, fstyle=3004, msize=0)
    leg.AddEntry(h_bkg, "Stat. Unc.", "F")

    if systErr:
        systErr_tag = "QCDScale"
        

    ##### Set graphics style for Signals #####
    if histo_signals_dict is not None:
        for label, histo_signal in histo_signals_dict.items():
            histo_signal.Scale(signals_factor)
            CMS.cmsDraw(histo_signal, **style_signals_dict[label])
            if signals_factor != 1:
                label = f"{label} [x{signals_factor}]"
            leg.AddEntry(histo_signal, label, "l")

    pad1.RedrawAxis()

    ################## PAD2 ##################
    pad2    = dicanv.cd(2)
    # hdw     = CMS.GetcmsCanvasHist(pad2)
    # hdw.Draw("hist")

    # how alternative way to pass style options
    # style = {"style": "hist", "lcolor": ROOT.kAzure + 2, "lwidth": 2, "fstyle": 0}
    # CMS.cmsDraw(self.ratio_nosignal, **style)
    # CMS.cmsDraw(

    # histo_ratio = histo_data.Clone("histo_ratio")
    # histo_ratio.Divide(histo_signal)
    if histo_data is None:
        pass
    else:
        histo_ratio = histo_data.Clone("histo_ratio")
        histo_ratio.Divide(stack.GetStack().Last())
        CMS.cmsDraw(histo_ratio, "epx0e0same", mcolor=ROOT.kBlack, msize=1.2)





    h_bkg_err   = h_bkg.Clone("h_err")
    h_bkg_err.Reset()
    for i in range(1, h_bkg.GetNbinsX()+1):
        h_bkg_err.SetBinContent(i,1)
        if(h_bkg.GetBinContent(i)):
            h_bkg_err.SetBinError(i, (h_bkg.GetBinError(i)/h_bkg.GetBinContent(i)))
        else:
            h_bkg_err.SetBinError(i, 10^(-99))
    CMS.cmsDraw(h_bkg_err, "e2same0", fcolor=ROOT.kGray+3, fstyle=3001, msize=0)





    ref_line = ROOT.TLine(xMin, 1, xMax, 1)
    CMS.cmsDrawLine(ref_line, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted)


    
    if repo is not None:
        if repo[-1] != "/":
            repo += "/"
        CMS.SaveCanvas(dicanv, repo + canv_name + ".pdf",  close=False)
        CMS.SaveCanvas(dicanv, repo + canv_name + ".png",  close=False)
        CMS.SaveCanvas(dicanv, repo + canv_name + ".C",    close=True)
    return dicanv






if __name__ == "__main__":
    histo_qcd       = ROOT.TH1F("histo_qcd", "QCD Histogram", 20, 0, 100)
    expo_qcd        = ROOT.TF1("expo_qcd", "expo", 0, 100)
    expo_qcd.SetParameters(1, -0.03)  # amplitude, slope
    histo_qcd.FillRandom("expo_qcd", 1000)

    histo_tt        = ROOT.TH1F("histo_tt", "TT Histogram", 20, 0, 100)
    expo_tt         = ROOT.TF1("expo_tt", "expo", 0, 100)
    expo_tt.SetParameters(1, -0.02)
    histo_tt.FillRandom("expo_tt", 800)

    histo_zjets     = ROOT.TH1F("histo_zjets", "ZJets Histogram", 20, 0, 100)
    expo_zjets      = ROOT.TF1("expo_zjets", "expo", 0, 100)
    expo_zjets.SetParameters(1, -0.025)
    histo_zjets.FillRandom("expo_zjets", 600)

    histo_wjets     = ROOT.TH1F("histo_wjets", "WJets Histogram", 20, 0, 100)
    expo_wjets      = ROOT.TF1("expo_wjets", "expo", 0, 100)
    expo_wjets.SetParameters(1, -0.018)
    histo_wjets.FillRandom("expo_wjets", 500)


    histo_data      = ROOT.TH1F("histo_data", "Data Histogram", 20, 0, 100)
    expo_data       = ROOT.TF1("expo_data", "expo", 0, 100)
    expo_data.SetParameters(1, -0.022)
    histo_data.FillRandom("expo_data", 1200)
    histo_data.Scale(2.5)


    histo_signal1   = ROOT.TH1F("histo_signal1", "Signal Histogram 1", 20, 0, 100)
    expo_signal1    = ROOT.TF1("expo_signal1", "expo", 0, 100)
    expo_signal1.SetParameters(1, -0.04)
    histo_signal1.FillRandom("expo_signal1", 400)
    histo_signal1.Scale(0.1)

    histo_signal2   = ROOT.TH1F("histo_signal2", "Signal Histogram 2", 20, 0, 100)
    expo_signal2    = ROOT.TF1("expo_signal2", "expo", 0, 100)
    expo_signal2.SetParameters(1.2, -0.04)
    histo_signal2.FillRandom("expo_signal2", 400)
    histo_signal2.Scale(0.1)

    histo_signal3   = ROOT.TH1F("histo_signal3", "Signal Histogram 3", 20, 0, 100)
    expo_signal3    = ROOT.TF1("expo_signal3", "expo", 0, 100)
    expo_signal3.SetParameters(1.2, -0.04)
    histo_signal3.FillRandom("expo_signal3", 400)
    histo_signal3.Scale(0.1)


    histo_signals_dict = {
                            "T (0.7TeV) #rightarrow tZ": histo_signal1,
                            "T (1.0TeV) #rightarrow tZ": histo_signal2,
                            "T (1.8TeV) #rightarrow tZ": histo_signal3,
                        }
    style_signals_dict  = {
                            "T (0.7TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen,      "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kSolid},
                            "T (1.0TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen+1,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDashed},
                            "T (1.8TeV) #rightarrow tZ":  {"style": "hist",   "msize": 0,    "lcolor": ROOT.kGreen+2,    "lwidth": 2, "fstyle": 0, "lstyle": ROOT.kDotted},
                        }





    canv_name       = "stack_example"
    logy            = False  # Set to True for logarithmic scale on y-axis for Pad1
    xMin            = 0
    xMax            = 100
    if logy:
        yMin        = 1e-2  # Set a small value for yMin to avoid log(0) issues
        yMax        = 1e5
    else:
        yMin        = 0
        yMax        = 500
    rMin            = 0
    rMax            = 2
    xTitle          = "xTitle"
    yTitle          = "yTitle"
    rTitle          = "rTitle"
    extraText       = "McFratm"
    lumi            = 5  # in fb^-1
    extraSpace      = 0.1
    iPos            = 0  # Position of the legend (0: top-right, 1: top-left, etc.)
    region          = "MixSRatleast1fjets"
    histo_bkg_dict  = {
                        "t#bar{t}":                 histo_tt,
                        "QCD":                      histo_qcd,
                        "Z (#nu#nu) + Jets":        histo_zjets,
                        "W (#it{l}#nu) + Jets":     histo_wjets,
                        }

    colors_bkg      = ["#e42536", "#bebdb8", "#86c8dd", "#caeba5"]

    dicanv = make_stack_with_ratio(
                                    canv_name               = canv_name,
                                    histo_bkg_dict          = histo_bkg_dict,
                                    histo_data              = histo_data,
                                    # histo_data              = None,
                                    histo_signals_dict      = histo_signals_dict,
                                    # histo_signals_dict      = None,
                                    region                  = region,
                                    xMin                    = xMin,
                                    xMax                    = xMax,
                                    yMin                    = yMin,
                                    yMax                    = yMax,
                                    rMin                    = rMin,
                                    rMax                    = rMax,
                                    xTitle                  = xTitle,
                                    yTitle                  = yTitle,
                                    rTitle                  = rTitle,
                                    extraText               = extraText,
                                    lumi                    = lumi,
                                    extraSpace              = extraSpace,
                                    iPos                    = iPos,
                                    logy                    = logy,
                                    repo                    = ".",
                                    colors_bkg              = colors_bkg,
                                    style_signals_dict      = style_signals_dict,
                                    )