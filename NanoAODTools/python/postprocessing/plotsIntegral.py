import ROOT, os

eras = ["2022", "2022EE", "2023", "2023postBPix"]
# path = f"/eos/user/l/lfavilla/RDF_DManalysis/results/run{era}_syst_noSFbtag_310725/plots/"

for era in eras:
    path = f"/eos/user/l/lfavilla/RDF_DManalysis/results/run{era}_syst_noSFbtag_310725/plots/"
    files = os.listdir(path)
    int_noSF = 0
    for f in files:
        if f.endswith(".root") and "Tprime" not in f and "Data" not in f:
            # print(f"Processing file: {f} for era: {era}")
            infile = ROOT.TFile.Open(path + f)
            h = infile.Get("MT_T_btagSFcheck_nominal")
            integral = h.Integral()
            int_noSF += integral
            infile.Close()
    print(f"Total integral without btag SF for era {era}: {int_noSF}")
    path = f"/eos/user/l/lfavilla/RDF_DManalysis/results/run{era}_syst_310725/plots/"
    files = os.listdir(path)
    int_SF = 0
    for f in files:
        if f.endswith(".root") and "Tprime" not in f and "Data" not in f:
            # print(f"Processing file: {f} for era: {era}")
            infile = ROOT.TFile.Open(path + f)
            h = infile.Get("MT_T_btagSFcheck_nominal")
            integral = h.Integral()
            int_SF += integral
            infile.Close()
    print(f"Total integral with btag SF for era {era}: {int_SF}")
    print(f"Ratio (w/wo) for era {era}: {int_SF/int_noSF}")