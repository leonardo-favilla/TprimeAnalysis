import os
import optparse
import sys
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import subprocess
import ROOT

usage               = "python3 jobChecker.py -o <outFolder> --year <year> [options]"
parser              = optparse.OptionParser(usage)
parser.add_option("-o", "--outputFolder",   dest="outFolder", type=str,             default="/eos/user/l/lfavilla/RDF_DManalysis/results/run2023_syst_310725/plots/",   help="Please enter the output folder where the results of the jobs are stored.")
parser.add_option(      "--year",           dest="year",      type=str,             default="2023",                                                                     help="Please enter the year of the samples to check, e.g. 2022, 2022EE, etc.")
parser.add_option(      '--suffix',         dest='suffix',    type=str,             default = None,                                                                     help='suffix to add to condor folder name')
(opt, args)         = parser.parse_args()
outputFolder        = opt.outFolder
year                = opt.year
suffix              = f"_{opt.suffix}" if opt.suffix is not None else ""
rerun_script_path   = f"rerun_failed_jobs_{year}.sh"
samples_to_check    = [
                        "QCD",
                        "TT",
                        "TW",
                        "ZJetsToNuNu_2jets",
                        "WJets_2jets",
                        "DataJetMET",
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
jobs_failed         = []
jobs_done           = []
jobs_running        = []

######### HERE THERE IS THE ACTUAL JOB CHECKING ############
result              = subprocess.run("condor_q -af:h ClusterId JobStatus JobTag", shell=True, capture_output=True, text=True)
if os.path.exists(outputFolder):                                # check out existence
    print(f"Output folder {outputFolder} exists.")
    print("Will check condor jobs...")
    for c in components_to_check:
        for line in result.stdout.splitlines()[1:]:
            jobId, runStatus, JobTag = line.split()
            if f"{c}{suffix}" in JobTag:
                jobs_running.append(c)
                break
        if c in jobs_running:
            continue

        filePath                    = outputFolder + c + ".root"
        if os.path.exists(filePath):                            # check file existence
            try:
                f                   = ROOT.TFile.Open(filePath)
                keys                = [key.GetName() for key in f.GetListOfKeys()]
                if len(keys)>0:                                 # if exists, check if there is at least 1 key
                    jobs_done.append(c)
                else:
                    print(f"Job {c}: FAILED, empty root file")
                    jobs_failed.append(c)
                f.Close()

            except:
                print(f"Job {c}: FAILED, could not open file")
                jobs_failed.append(c)

        else:
            print(f"Job {c}: FAILED, file does not exist")
            jobs_failed.append(c)

else:
    print(f"Output folder {outputFolder} does not exist.")
    print("Cannot check any job, exiting...")
    sys.exit(1)

### Rerun commands for the failed jobs ###
with open(rerun_script_path, "w") as f:
    f.write("#!/bin/bash\n\n")
    for c in jobs_failed:
        if "Data" in c:
            # cmd1 = f"python3 postSelector_submitter.py -d {c} --dryrun\n"
            cmd2 = f"condor_submit ./condor{suffix}/{c}{suffix}/condor.sub\n"
            cmd3 = f"echo resubmitting job for {c}\n\n"
        else:
            # cmd1 = f"python3 postSelector_submitter.py -d {c} --syst --dryrun\n"
            cmd2 = f"condor_submit ./condor{suffix}/{c}{suffix}/condor.sub\n"
            cmd3 = f"echo resubmitting job for {c}{suffix}\n\n"
        # f.write(cmd1)
        f.write(cmd2)
        f.write(cmd3)


print("--------------------------------------------------")
print(f"Total jobs to check:                                {jobs_total}")
print(f"Jobs done:                                          {len(jobs_done)}")
print(f"Jobs running:                                       {len(jobs_running)}")
print(f"Jobs failed:                                        {len(jobs_failed)}")
print(f"\nYou can find the commands to rerun failed jobs in {rerun_script_path}")
print("--------------------------------------------------")