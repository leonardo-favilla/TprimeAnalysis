import os
import optparse
import sys
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage               = "python3 jobChecker.py -o <outFolder> --year <year> [options]"
parser              = optparse.OptionParser(usage)
parser.add_option("-o", "--outputFolder",   dest="outFolder", type=str,             default="/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_310725/plots/",   help="Please enter the output folder where the results of the jobs are stored.")
parser.add_option(      "--year",           dest="year",      type=str,             default="2023",                                                                     help="Please enter the year of the samples to check, e.g. 2022, 2022EE, etc.")
(opt, args)         = parser.parse_args()
outputFolder        = opt.outFolder
year                = opt.year

samples_to_check    = [
                        "QCD",
                        "TT",
                        "TW",
                        "ZJetsToNuNu_2jets",
                        "WJets_2jets",
                        # "DataJetMET",
                        "DataMuon",
                        # "TprimeToTZ_700",
                        # "TprimeToTZ_1000",
                        # "TprimeToTZ_1800",
                        ]
components_to_check = []

for s in samples_to_check:
    s = s+"_"+year
    if hasattr(sample_dict[s], "components"):
        components_to_check.extend([c.label for c in sample_dict[s].components])
    else:
        components_to_check.append(s)
print(components_to_check)

jobs_total          = len(components_to_check)
jobs_failed         = 0
jobs_done           = 0


######### HERE THERE IS THE ACTUAL JOB CHECKING ############
if os.path.exists(outputFolder):                                # check out existence
    print(f"Output folder {outputFolder} exists.")
    print("Will check condor jobs...")
    for c in components_to_check:
        filePath                    = outputFolder + c + ".root"
        if os.path.exists(filePath):                            # check file existence
            try:
                f                   = ROOT.TFile.Open(filePath)
                keys                = [key.GetName() for key in f.GetListOfKeys()]
                if len(keys)>0:                                 # if exists, check if there is at least 1 key
                    jobs_done      += 1
                else:
                    print(f"Job {c}: FAILED, empty root file")
                    jobs_failed    += 1
                f.Close()
            except:
                print(f"Job {c}: FAILED, could not open file")
                jobs_failed        += 1
        else:
            print(f"Job {c}: FAILED, file does not exist")
            jobs_failed            += 1

else:
    print(f"Output folder {outputFolder} does not exist.")
    print("Cannot check any job, exiting...")
    sys.exit(1)

print("--------------------------------------------------")
print(f"Total jobs to check:    {jobs_total}")
print(f"Jobs done:              {jobs_done}")
print(f"Jobs failed:            {jobs_failed}")
print("--------------------------------------------------")
