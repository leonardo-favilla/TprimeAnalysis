import subprocess
import sys
sys.path.append('../')
from samples.samples import *






output_folder   = "/eos/user/l/lfavilla/RDF_DManalysis/results/Full2022_Full2023_syst/"
# repohisto       = output_folder + "plots/"
repohisto       = output_folder + "plots/"
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
# samples_to_hadd = ["QCD", "TT", "WJets_2jets", "ZJetsToNuNu_2jets", "TprimeToTZ_700", "TprimeToTZ_1000", "TprimeToTZ_1800", "DataJetMET"]
samples_to_hadd = ["DataJetMET"]
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created output folder: {output_folder}")
if not os.path.exists(repohisto):
    os.makedirs(repohisto)
    print(f"Created repository folder for histograms: {repohisto}")








datasets                = [s+"_2023" for s in samples_to_hadd]
components_to_hadd      = []
for dat in datasets:
    if "Data" in dat:           # If the dataset is Data, we need to handle it differently
        components_to_hadd.extend([dat.replace("_2023","")])
    else:                       # If the dataset is a simulation, we need to get the components from the sample_dict
        d               = sample_dict[dat]
        if hasattr(d, "components"):
            s_list      = d.components
        else:
            s_list      = [d]

        components_to_hadd.extend([s.label.replace("_2023","") for s in s_list])


print("components to hadd:", components_to_hadd)


for c in components_to_hadd:
    if "Data" in c:
        files_to_hadd   = [folder_dict[year_tag]+"plots/"+file for year_tag in year_tags for file in os.listdir(folder_dict[year_tag]+"plots/") if file.startswith(c) and file.endswith(".root")]
    else:
        files_to_hadd   = [folder_dict[year_tag]+"plots_rescaled_to_lumi/"+c+"_"+year_tag+".root" for year_tag in year_tags]
    files_to_hadd   = [f for f in files_to_hadd if os.path.exists(f)]
    if len(files_to_hadd) < len(year_tags):
        print(f"WARNING: Not all files found for {c} in the specified years. Found {len(files_to_hadd)} out of {len(year_tags)}.")
        print(f"Files found: {files_to_hadd}")
        continue
    else:
        print(f"Hadding files for {c} from years {year_tags}: {files_to_hadd}")


    if "Data" in c:
        print(f"Skipping {c} as it is Data and does not require hadding, will just copy them in {repohisto}.")
        for file in files_to_hadd:
            output_file     = repohisto + os.path.basename(file)
            command         = f"cp {file} {output_file}"
            print(f"Running command: {command}")
            command_asList  = command.split()
            results         = subprocess.run(command_asList, capture_output=True, text=True, check=True)
    else:
        output_file         = repohisto + c + ".root"
        command             = "hadd -f " + output_file + " " + " ".join(files_to_hadd)
        print(f"Running command: {command}")
        command_asList      = command.split()
        results             = subprocess.run(command_asList, capture_output=True, text=True, check=True)