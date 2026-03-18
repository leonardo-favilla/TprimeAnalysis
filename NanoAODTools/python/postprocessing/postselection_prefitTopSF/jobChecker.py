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
rerun_script_path   = f"rerun_failed_jobs_{year}.sh"
samples_to_check    = [
                        "QCD",
                        "TT",
                        "TW",
                        "ZJetsToNuNu_2jets",
                        "WJets_2jets",
                        "DataMuon",
                        # "DataJetMET",
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
components_to_rerun = []

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
                    components_to_rerun.append(c)
                f.Close()
            except:
                print(f"Job {c}: FAILED, could not open file")
                jobs_failed        += 1
                components_to_rerun.append(c)
        else:
            print(f"Job {c}: FAILED, file does not exist")
            jobs_failed            += 1
            components_to_rerun.append(c)

else:
    print(f"Output folder {outputFolder} does not exist.")
    print("Cannot check any job, exiting...")
    sys.exit(1)


### Rerun commands for the failed jobs ###
with open(rerun_script_path, "w") as f:
    f.write("#!/bin/bash\n\n")
    for c in components_to_rerun:
        if "Data" in c:
            cmd1 = f"python3 postSelector_submitter.py -d {c} --dryrun\n"
            cmd2 = f"condor_submit ./condor/{c}/condor.sub\n"
            cmd3 = f"echo resubmitting job for {c}\n\n"
        else:
            cmd1 = f"python3 postSelector_submitter.py -d {c} --syst --dryrun\n"
            cmd2 = f"condor_submit ./condor_syst/{c}_syst/condor.sub\n"
            cmd3 = f"echo resubmitting job for {c}_syst\n\n"
        f.write(cmd1)
        f.write(cmd2)
        f.write(cmd3)


print("--------------------------------------------------")
print(f"Total jobs to check:                                {jobs_total}")
print(f"Jobs done:                                          {jobs_done}")
print(f"Jobs failed:                                        {jobs_failed}")
print(f"\nYou can find the commands to rerun failed jobs in {rerun_script_path}")
print("--------------------------------------------------")