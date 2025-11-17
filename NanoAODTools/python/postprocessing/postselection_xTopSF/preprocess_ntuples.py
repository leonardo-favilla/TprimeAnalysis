import ROOT
ROOT.gStyle.SetOptStat(0)
import os, sys
import optparse
import json
import numpy as np
import yaml
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')

# inFilePath                  = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/QCD_HT200to400_2022/20240704_122343/tree_hadd_67.root"
# chain                       = [inFilePath]
# year                        = 2022
config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)


usage                   = 'python3 preprocess_ntuples.py -c <component> --nfiles_max <nfiles_max>'
parser                  = optparse.OptionParser(usage)
parser.add_option('-c', '--component',          dest='component',           type=str,               default="QCD_HT400to600_2022",                      help='Single component to process, in the form: QCD_HT400to600_2022')
parser.add_option(      '--nfiles_max',         dest='nfiles_max',          type=int,               default=1,                                          help='Max number of files to process per sample')
parser.add_option(      '--certpath',           dest='certpath',            type=str,               default="/tmp/x509up_u{}".format(str(os.getuid())), help='Path to the certificate file')
(opt, args)             = parser.parse_args()
in_dataset              = opt.component
year                    = int(in_dataset.split("_")[-1][:4])
EE                      = 1 if len(in_dataset.split("_")[-1])>4 else 0
nfiles_max              = opt.nfiles_max
certpath                = opt.certpath
where_to_write          = "eos" # options are "tier" or "eos"
dict_samples_file       = config["dict_samples"][year]

#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)

#### User info ####
username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())


#### Retrieve files to process for the given component and ntot ####
# samples_list                                        = samples[in_dataset][in_dataset] #### THIS I SUSELESS

# if not "Data" in in_dataset:
#     ntot_events                                     = np.sum(samples[in_dataset][in_dataset]['ntot'][:nfiles_max])
# else:
#     ntot_events                                     = None

# chain                                               = []
# tchain                                              = ROOT.TChain("Events")
# for i, string in enumerate(samples[in_dataset][in_dataset]['strings']):
#     samples[in_dataset][in_dataset]['strings'][i]   = string.replace("root://cms-xrd-global.cern.ch/", "root://stormgf2.pi.infn.it/")
#     f                                               = samples[in_dataset][in_dataset]['strings'][i]
#     try:
#         TFile                                       = ROOT.TFile.Open(f)
#         tchain.Add(f)
#     except:
#         ntot_events -= samples[in_dataset][in_dataset]['ntot'][i]
#         print("Could not add file: ", f)
#         continue
# chain                                               = samples[in_dataset][in_dataset]['strings'][:nfiles_max]

inFilePath                                          = "davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/Run3Analysis_Tprime/TT_semilep_2022/20251114_145029/tree_hadd_0.root"
chain                                               = [inFilePath]
ntot_events                                         = 170916
tchain                                              = ROOT.TChain("Events")
tchain.Add(inFilePath)
print(f"Processing component {in_dataset}, year {year}, with {len(chain)} files")
print(chain[0])

#### Define output files and folders ####
if where_to_write == "eos":
    remote_folder_name              = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF"
    outFolder                       = remote_folder_name+"/preprocessed_ntuples/"
    outSubFolder                    = outFolder+in_dataset+"/"
    if not os.path.exists(remote_folder_name):
        os.makedirs(remote_folder_name)
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    if not os.path.exists(outSubFolder):
        os.makedirs(outSubFolder)
elif where_to_write == "tier":
    remote_folder_name              = "TopSF"
    outFolder                       = remote_folder_name+"/preprocessed_ntuples/"
    outSubFolder                    = outFolder+in_dataset+"/"

    print("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, remote_folder_name, certpath))
    subprocess.run(
        ["davix-mkdir",
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{remote_folder_name}/",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )

    print("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, outFolder, certpath))
    subprocess.run(
        ["davix-mkdir",
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFolder}",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )

    print("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, outSubFolder, certpath))
    subprocess.run(
        ["davix-mkdir",
        f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outSubFolder}",
        "-E", certpath,
        "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )

    outFolder_tmp                   = "/tmp/{}/".format(username)
    if not os.path.exists(outFolder_tmp):
        os.makedirs(outFolder_tmp)
    outFilePath_nominal_tmp         = outFolder_tmp+in_dataset+"_nominal.root"

    if not "Data" in in_dataset:
        outFilePath_jerUp_tmp       = outFolder_tmp+in_dataset+"_jerUp.root"
        outFilePath_jerDown_tmp     = outFolder_tmp+in_dataset+"_jerDown.root"
        outFilePath_jesUp_tmp       = outFolder_tmp+in_dataset+"_jesUp.root"
        outFilePath_jesDown_tmp     = outFolder_tmp+in_dataset+"_jesDown.root"



outFilePath_nominal         = outSubFolder+in_dataset+"_nominal.root"
if not "Data" in in_dataset:
    outFilePath_jerUp           = outSubFolder+in_dataset+"_jerUp.root"
    outFilePath_jerDown         = outSubFolder+in_dataset+"_jerDown.root"
    outFilePath_jesUp           = outSubFolder+in_dataset+"_jesUp.root"
    outFilePath_jesDown         = outSubFolder+in_dataset+"_jesDown.root"





print("Input file 0:                ", chain[0])
print("Year:                        ", year)
print("Output folder:               ", outFolder)
print("Output nominal file:         ", outFilePath_nominal)
if not "Data" in in_dataset:
    print("Output jerUp file:           ", outFilePath_jerUp)
    print("Output jerDown file:         ", outFilePath_jerDown)
    print("Output jesUp file:           ", outFilePath_jesUp)
    print("Output jesDown file:         ", outFilePath_jesDown)



# df                      = ROOT.RDataFrame("Events", chain)
df                      = ROOT.RDataFrame(tchain)
branches                = list(map(str, df.GetColumnNames()))
if not "Data" in in_dataset:
    df                  = df.Define("SFbtag", "SFbtag_nominal")
    branches.remove("SFbtag_nominal")
branches_nominal        = [b for b in branches if b.endswith("_nominal")]
if not "Data" in in_dataset:
    branches_jerup          = [b for b in branches if b.endswith("_jerup")]
    branches_jerdown        = [b for b in branches if b.endswith("_jerdown")]
    branches_jesTotalup     = [b for b in branches if b.endswith("_jesTotalup")]
    branches_jesTotaldown   = [b for b in branches if b.endswith("_jesTotaldown")]
else:
    branches_jerup          = []
    branches_jerdown        = []
    branches_jesTotalup     = []
    branches_jesTotaldown   = []
branches_common         = [b for b in branches if not (b in branches_nominal or b in branches_jerup or b in branches_jerdown or b in branches_jesTotalup or b in branches_jesTotaldown)]
hlt                     = {
                            2022: [
                                    "HLT_PFMET120_PFMHT120_IDTight",          # MET (2022-2023)
                                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",  # MET (2022-2023)
                                    "HLT_Photon200",                          # High-pT electron (2022)
                                    "HLT_Ele27_WPTight_Gsf",                  # Low-pT electron (2022)
                                    "HLT_Mu50",                               # Muon (2022-2023)
                                    "HLT_IsoMu24",                            # Muon (2022-2023)
                                    "HLT_HighPtTkMu100",                      # Muon (2022-2023)
                                    ],

                            2023: [
                                    "HLT_PFMET120_PFMHT120_IDTight",          # MET (2022-2023)
                                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",  # MET (2022-2023)
                                    "HLT_Photon175EB_TightID_TightIso",       # High-pT electron (2023)
                                    "HLT_Ele30_WPTight_Gsf",                  # Low-pT electron (2023)
                                    "HLT_Mu50",                               # Muon (2022-2023)
                                    "HLT_IsoMu24",                            # Muon (2022-2023)
                                    "HLT_HighPtTkMu100",                      # Muon (2022-2023)
                                ],
                            2024: [
                                ]
                            }
eventWeights            = ["SFbtag", "puWeight", "puWeightDown", "puWeightUp", "LHEWeight_originalXWGTUP"]

branches_to_save        = [
                            *hlt[year],

                            "TopGenTopPart_pt",
                            "TopGenTopPart_eta",
                            "TopGenTopPart_phi",
                            "TopGenTopPart_mass",

                            "Electron_pt",
                            "Electron_eta",
                            "Electron_phi",
                            "Electron_cutBased",

                            "Muon_pt",
                            "Muon_eta",
                            "Muon_phi",
                            "Muon_looseId", 
                            "Muon_tightId",

                            "FatJet_jetId",
                            "FatJet_mass",
                            "FatJet_msoftdrop",
                            "FatJet_pt",
                            "FatJet_phi",
                            "FatJet_eta",
                            "FatJet_particleNetWithMass_WvsQCD",
                            "FatJet_particleNetWithMass_TvsQCD",
                            "FatJet_matched",

                            "Jet_jetId",
                            "Jet_mass",
                            "Jet_pt",
                            "Jet_phi",
                            "Jet_eta",
                            "Jet_btagPNetB",

                            "PuppiMET_T1_pt",
                            "PuppiMET_T1_phi",

                            "TopResolved_mass",
                            "TopResolved_pt",
                            "TopResolved_eta",
                            "TopResolved_phi",
                            "TopResolved_TopScore",
                            "TopResolved_idxJet0",
                            "TopResolved_idxJet1",
                            "TopResolved_idxJet2",
                            "TopResolved_truth",

                            "TopMixed_mass",
                            "TopMixed_pt",
                            "TopMixed_eta",
                            "TopMixed_phi",
                            "TopMixed_TopScore",
                            "TopMixed_idxFatJet",
                            "TopMixed_idxJet0",
                            "TopMixed_idxJet1",
                            "TopMixed_idxJet2",
                            "TopMixed_truth"

                            ]

if not "Data" in in_dataset:
    branches_to_save    += eventWeights

print("Total number of branches in the input file:  ", len(branches))
print("Number of common branches:                   ", len(branches_common))
print("Number of branches for nominal:              ", len(branches_nominal))
print("Number of branches for jerup:                ", len(branches_jerup))
print("Number of branches for jerdown:              ", len(branches_jerdown))
print("Number of branches for jesTotalup:           ", len(branches_jesTotalup))
print("Number of branches for jesTotaldown:         ", len(branches_jesTotaldown))
print("Number of branches to save:                  ", len(branches_to_save))


opts            = ROOT.RDF.RSnapshotOptions()
opts.fLazy      = True
df_nominal,df_jerup,df_jerdown,df_jesTotalup,df_jesTotaldown = [df,df,df,df,df]
for b in branches_nominal:
    try:
        df_nominal      = df_nominal.Redefine(b.replace("_nominal", ""), b)
    except:
        df_nominal      = df_nominal.Define(b.replace("_nominal", ""), b)
for b in branches_jerup:
    try:
        df_jerup        = df_jerup.Redefine(b.replace("_jerup", ""), b)
    except:
        df_jerup        = df_jerup.Define(b.replace("_jerup", ""), b)
for b in branches_jerdown:
    try:
        df_jerdown      = df_jerdown.Redefine(b.replace("_jerdown", ""), b)
    except:
        df_jerdown      = df_jerdown.Define(b.replace("_jerdown", ""), b)
for b in branches_jesTotalup:
    try:
        df_jesTotalup   = df_jesTotalup.Redefine(b.replace("_jesTotalup", ""), b)
    except:
        df_jesTotalup   = df_jesTotalup.Define(b.replace("_jesTotalup", ""), b)
for b in branches_jesTotaldown:
    try:
        df_jesTotaldown = df_jesTotaldown.Redefine(b.replace("_jesTotaldown", ""), b)
    except:
        df_jesTotaldown = df_jesTotaldown.Define(b.replace("_jesTotaldown", ""), b)


# branches_to_save        = list(map(str, df_nominal.GetColumnNames()))
if where_to_write == "tier":
    df_nominal              = df_nominal.Snapshot("Events", outFilePath_nominal_tmp, branches_to_save, opts)
    if not "Data" in in_dataset:
        df_jerup                = df_jerup.Snapshot("Events", outFilePath_jerUp_tmp, branches_to_save, opts)
        df_jerdown              = df_jerdown.Snapshot("Events", outFilePath_jerDown_tmp, branches_to_save, opts)
        df_jesTotalup           = df_jesTotalup.Snapshot("Events", outFilePath_jesUp_tmp, branches_to_save, opts)
        df_jesTotaldown         = df_jesTotaldown.Snapshot("Events", outFilePath_jesDown_tmp, branches_to_save, opts)
else:
    df_nominal                  = df_nominal.Snapshot("Events", outFilePath_nominal, branches_to_save, opts)
    if not "Data" in in_dataset:
        df_jerup                = df_jerup.Snapshot("Events", outFilePath_jerUp, branches_to_save, opts)
        df_jerdown              = df_jerdown.Snapshot("Events", outFilePath_jerDown, branches_to_save, opts)
        df_jesTotalup           = df_jesTotalup.Snapshot("Events", outFilePath_jesUp, branches_to_save, opts)
        df_jesTotaldown         = df_jesTotaldown.Snapshot("Events", outFilePath_jesDown, branches_to_save, opts)

df_nominal.GetValue()
if not "Data" in in_dataset:
    df_jerup.GetValue()
    df_jerdown.GetValue()
    df_jesTotalup.GetValue()
    df_jesTotaldown.GetValue()
print("Snapshot done!")

if where_to_write == "tier":
    print("Copying files to tier...")
    subprocess.run(
        [
            "davix-put", outFilePath_nominal_tmp, f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath_nominal}", "-E", certpath, "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
        ],
        check=True
    )
    print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_nominal_tmp, username, outFilePath_nominal, certpath))
    if not "Data" in in_dataset:
        print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_jerUp_tmp, username, outFilePath_jerUp, certpath))
        subprocess.run(
            ["davix-put", outFilePath_jerUp_tmp, f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath_jerUp}", "-E", certpath, "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"],
            check=True
        )
        print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_jerDown_tmp, username, outFilePath_jerDown, certpath))
        subprocess.run(
            ["davix-put", outFilePath_jerDown_tmp, f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath_jerDown}", "-E", certpath, "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"],
            check=True
        )
        print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_jesUp_tmp, username, outFilePath_jesUp, certpath))
        subprocess.run(
            ["davix-put", outFilePath_jesUp_tmp, f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath_jesUp}", "-E", certpath, "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"],
            check=True
        )
        print("davix-put {} davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} -E {} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(outFilePath_jesDown_tmp, username, outFilePath_jesDown, certpath))
        subprocess.run(
            ["davix-put", outFilePath_jesDown_tmp, f"davs://stwebdav.pi.infn.it:8443/cms/store/user/{username}/{outFilePath_jesDown}", "-E", certpath, "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"],
            check=True
        )
    print("Done!")