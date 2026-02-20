import ROOT
def open_root_files(paths):
    files = []
    for p in paths:
        f = ROOT.TFile.Open(p)
        if not f or f.IsZombie():
            print("Failed to open:", p)
            continue
        print("Opened:", p)
        files.append(f)
    return files

# Example usage: replace with your actual file list or generate it with glob
files_to_open = [
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC1_0_2023/DataJetMETC1_0_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC1_1_2023/DataJetMETC1_1_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC2_0_2023/DataJetMETC2_0_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC2_1_2023/DataJetMETC2_1_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC3_0_2023/DataJetMETC3_0_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC3_1_2023/DataJetMETC3_1_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC4_0_2023/DataJetMETC4_0_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC4_0_2023/DataJetMETC4_0_2023_nominal_1.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC4_1_2023/DataJetMETC4_1_2023_nominal_0.root",
    # "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataJetMETC4_1_2023/DataJetMETC4_1_2023_nominal_1.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC1_0_2023/DataMuonC1_0_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC1_1_2023/DataMuonC1_1_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC2_0_2023/DataMuonC2_0_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC2_1_2023/DataMuonC2_1_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC3_0_2023/DataMuonC3_0_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC3_1_2023/DataMuonC3_1_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC4_0_2023/DataMuonC4_0_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC4_0_2023/DataMuonC4_0_2023_nominal_1.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC4_1_2023/DataMuonC4_1_2023_nominal_0.root",
    "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal/DataMuonC4_1_2023/DataMuonC4_1_2023_nominal_1.root"
    ]



root_files                  = open_root_files(files_to_open)
files_in_error              = []
sum_entries_stack_data      = 0
sum_entries_fit_data        = 0
for f in root_files:
    tree        = f.Get("Events")
    histname    = "hist_test"
    var         = "BestTopMixed_mass"
    cut         = "W_pt>150 && MET_pt>50 && dR_bJetTopLep_BestTopMixed>=1.2 && dR_muTopLep_BestTopMixed>=1.2 && (BestTopMixed_pt>=400) && (BestTopMixed_pt<600) && BestTopMixed_score<0.7214655876159668"
    if "Data" in f.GetName():
        weight  = "1"
    else:
        weight  = "xsecWeight/ntotEvents*nloewcorrection*puWeight*SFbtag*(LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP))"

    h           = ROOT.TH1F(histname, histname, 100, 1, -1)
    project_out = tree.Project(histname, var, f"({cut})*({weight})", "e")
    print(f"Projected {project_out} entries into histogram {histname} from file {f.GetName()}\n")
    if project_out == -1:
        files_in_error.append(f.GetName())
    else:
        sum_entries_fit_data   += project_out
print("Files with projection errors:", files_in_error)
print("Total entries in fit data:", sum_entries_fit_data)





files_to_open = [
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC1_0_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC1_1_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC2_0_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC2_1_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC3_0_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC3_1_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC4_0_2023.root",
    "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/DataMuonC4_1_2023.root",
    ]
root_files                  = open_root_files(files_to_open)
for f in root_files:
    histname    = "BestTopMixed_mass_SemiLep_MergedLooseButNotTight_pt400to600_fail"
    h           = f.Get(histname)
    if not h:
        print(f"Failed to retrieve histogram {histname} from file {f.GetName()}")
        continue
    entries     = h.GetEntries()
    print(f"Histogram {histname} from file {f.GetName()} has {entries} entries\n")
    sum_entries_stack_data += entries
print("Total entries in stack data:", sum_entries_stack_data)