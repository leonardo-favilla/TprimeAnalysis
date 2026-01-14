import os
import optparse
import sys
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import subprocess
import ROOT
import yaml
import json

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())

usage               = "python3 jobChecker.py -o <outFolder> --year <year>"
parser              = optparse.OptionParser(usage)
parser.add_option("-o", "--outputFolder",   dest="outFolder", type=str,             default="davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework/",     help="Please enter the output folder where the results of the jobs are stored.")
parser.add_option(      "--year",           dest="year",      type=str,             default="2023",                                                                                                     help="Please enter the year of the samples to check, e.g. 2022, 2022EE, etc.")
(opt, args)         = parser.parse_args()
outputFolder        = opt.outFolder
year                = int(opt.year[:4])
period              = opt.year
certpath            = "/tmp/x509up_u"+str(uid)

#### LOAD dict_samples.py ####
dict_samples_file   = config["dict_samples"][str(year)]
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)

samples_to_check    = [
                        "QCD",
                        "TT",
                        "TW",
                        "ZJetsToNuNu_2jets",
                        "WJets_2jets",
                        "DataJetMET",
                        ]
components_to_check = []

for s in samples_to_check:
    s = s+"_"+period
    if hasattr(sample_dict[s], "components"):
        components_to_check.extend([c.label for c in sample_dict[s].components])
    else:
        components_to_check.append(s)
print(components_to_check)



######### HERE THERE IS THE ACTUAL JOB CHECKING ############
to_rerun = []
for c in components_to_check:

    # Determine if MC or Data
    if "Data" not in c:
        isMC = True
        scenarios = ["nominal", "jerUp", "jerDown", "jesUp", "jesDown"]
    else:
        isMC = False
        scenarios = ["nominal"]

    outputSubFolder = f"{outputFolder}{c}/"

    # print(f"\nChecking folder: {outputSubFolder}")
    # print(f"davix-ls {outputSubFolder} -E {certpath} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")

    # List folder
    res = subprocess.run(
        ["davix-ls", outputSubFolder,
         "-E", certpath,
         "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"],
        capture_output=True, text=True
    )

    if res.returncode != 0:
        print(f"Could not list folder {outputSubFolder}")
        print(res.stderr.strip())
        continue

    # print("Folder OK. Checking scenarios...")

    # Check scenario files
    for scenario in scenarios:
        result = subprocess.run([
                                "davix-ls",
                                outputSubFolder,
                                "-E", certpath,
                                "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
                                ],
                                capture_output=True, text=True)

        files_in_inFolder   = result.stdout.splitlines()
        remote_files        = [f"{outputSubFolder}{f}" for f in files_in_inFolder if scenario in f]

        ### Determine number of slices per each component ###
        nfiles_max              = len(samples[c][c]['strings'])
        if nfiles_max < 100:
            nSlices             = 1
        elif nfiles_max < 500:
            nSlices             = 2
        elif nfiles_max < 1000:
            nSlices             = 4
        else:
            nSlices             = 6

        for sliceNumber in range(nSlices):
            filePath = f"{outputSubFolder}{c}_{scenario}_{sliceNumber}.root"
            # print(f"\nChecking file: {filePath}")

            if filePath not in remote_files:
                print(f"File not found: {filePath}")
                to_rerun.append((c, scenario, sliceNumber))
                continue

            res = subprocess.run(
                ["davix-ls", filePath,
                "-E", certpath,
                "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"],
                capture_output=True, text=True
            )

            if res.returncode != 0:
                print(f"File does not exist: {filePath}")
                print(res.stderr.strip())
                to_rerun.append((c, scenario, sliceNumber))
                continue

            # print("File exists. Trying to open with ROOT...")

            try:
                f       = ROOT.TFile.Open(filePath)
                if not f or f.IsZombie():
                    print(f"ROOT error for {filePath}")
                    to_rerun.append((c, scenario, sliceNumber))
                    continue
                tree        = f.Get("Events")
                nev         = tree.GetEntries()
                branches    = [b.GetName() for b in tree.GetListOfBranches()]
                print(f"File {filePath} opened successfully with {nev} entries.")
                if ("xsecWeight" not in branches) or ("ntotEvents" not in branches):
                    print(f"xsecWeight or ntotEvents branch not found in {filePath}")
                    to_rerun.append((c, scenario, sliceNumber))
                    continue
                f.Close()
                # print(f"ROOT opened file successfully: {filePath}")
            except Exception as e:
                print(f"Could not open file {filePath}: {e}")
                to_rerun.append((c, scenario, sliceNumber))
                continue

print("\n\nSummary of files to rerun:")
for c, scenario, sliceNumber in to_rerun:
    print(f"Component: {c}, Scenario: {scenario}, Slice Number: {sliceNumber}")