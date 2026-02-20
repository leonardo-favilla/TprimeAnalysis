import ROOT
from loadHists import loadHists
import sys
sys.path.append('../')
from samples.samples import *
import copy

year_tags       = ["2022", "2022EE", "2023", "2023postBPix"]
folder_dict     = {
                    "2022":         "/eos/home-a/acagnott/DarkMatter/nosynch/run2022_systematics/",
                    "2022EE":       "/eos/home-a/acagnott/DarkMatter/nosynch/run2022EE_systematics/",

                    "2023":         "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst/",
                    # "2023":         "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_no_nloewcorrection/",
                    # "2023":         "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_no_SFbtag/",
                    # "2023":         "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_no_puWeight/",

                    "2023postBPix": "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst/",
                    # "2023postBPix": "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst_no_nloewcorrection/",
                    # "2023postBPix": "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst_no_SFbtag/",
                    # "2023postBPix": "/eos/user/l/lfavilla/RDF_DManalysis/results/run2023postBPix_syst_no_puWeight/",
                }
lumi_dict       = {
                    "2018":         59.97,
                    "2022":         7.87,
                    "2022EE":       26.43,
                    "2023":         17.794,
                    "2023postBPix": 9.451,
                }

samples_to_rescale = ["QCD", "TT", "WJets_2jets", "ZJetsToNuNu_2jets", "TprimeToTZ_700", "TprimeToTZ_1000", "TprimeToTZ_1800"]




############# Rescale files to Lumi (the lumi value is different per each Era) #############
print("Rescaling files to Lumi...")
for year_tag in year_tags:
    datasets                = [s+"_"+year_tag for s in samples_to_rescale]
    components_to_rescale   = []
    for dat in datasets:
        d                   = sample_dict[dat]
        if hasattr(d, "components"):
            s_list          = d.components
        else:
            s_list          = [d]
        components_to_rescale.extend([s.label for s in s_list])
    print(components_to_rescale)

    lumi                    = lumi_dict[year_tag]
    repohisto               = folder_dict[year_tag] + "plots/"
    output_folder           = folder_dict[year_tag] + "plots_rescaled_to_lumi/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    if not os.path.exists(repohisto):
        os.makedirs(repohisto)
        print(f"Created repository folder for histograms: {repohisto}")


    for c in components_to_rescale:
        file_to_rescale    = folder_dict[year_tag]+"plots/"+c+".root"
        print(file_to_rescale)
        if not os.path.exists(file_to_rescale):
            print(f"WARNING: No files found for {c} in {year_tag}. Skipping...")
            continue


        histList            = loadHists(file_to_rescale)
        output_file_path    = os.path.join(output_folder, os.path.basename(file_to_rescale))
        print(f"Output file path: {output_file_path}")

        # Create ROOT file for output
        outputFile = ROOT.TFile(output_file_path, "RECREATE")
        for hname, hist in histList.items():
            hist.Scale(lumi)
            # print(type(hist))
            hist.Write(hname)
        outputFile.Close()
        print(f"Saved rescaled histograms to: {output_file_path}")
        
    print("\n")

