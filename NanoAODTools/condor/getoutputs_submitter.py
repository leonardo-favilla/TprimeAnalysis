import os
import sys
import argparse
import shutil
import time
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


parser          = argparse.ArgumentParser()
parser.add_argument("-d",   "--datasets",      required=True,   help="Comma-separated list of datasets (can be either entire samples or single components)")
parser.add_argument("-o",   "--output_json",   required=True,   help="Output JSON file name")
parser.add_argument('--tier', dest='tier', type=str, default = 'pisa', help='Please enter location where to write the output file (tier pisa or bari)')

args            = parser.parse_args()
output_json     = args.output_json
tier            = args.tier
username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"

if not os.path.exists("/tmp/x509up_u" + str(uid)):
    print("Please run voms command")
    sys.exit()
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

# --------------------------------------------------
# Get datasets
# --------------------------------------------------
datasets    = [dataset.strip() for dataset in args.datasets.split(",") if dataset.strip()]
samples     = []
for dataset in datasets:
    if dataset not in sample_dict.keys():
        print(f"Dataset {dataset} not found")
        sys.exit()
    elif dataset in sample_dict.keys():
        if hasattr(sample_dict[dataset], "components"):
            samples.extend(sample_dict[dataset].components)
        else:
            samples.extend([sample_dict[dataset]])

print([sample.label for sample in samples])

def sub_writer(run_folder, log_folder, dataset):
    f = open(run_folder+"condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    # f.write("should_transfer_files   = YES\n")
    # f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    # f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    # f.write('requirements            = (TARGET.OpSysAndVer =?= "CentOS7")\n')
    f.write("+JobFlavour             = \"workday\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write('+JobTag                 = "'+dataset+'"\n')
    f.write("executable              = "+run_folder+"runner.sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+log_folder+"output/"+dataset+".out\n")
    f.write("error                   = "+log_folder+"error/"+dataset+".err\n")
    f.write("log                     = "+log_folder+"log/"+dataset+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(run_folder, dataset, output_json):
    runner_path = os.path.join(run_folder, f"runner.sh")
    pycommand   = f"python3 getoutputs.py -d {dataset} -o {output_json} --tier {tier}"

    with open(runner_path, "w") as f:
        f.write("#!/usr/bin/bash\n\n")
        f.write("echo \"X509_USER_PROXY: ${X509_USER_PROXY}\"\n")
        f.write("voms-proxy-info\n")
        f.write('echo "===== Job started ====="\n')
        f.write('echo "Host: $(hostname)"\n')
        f.write('echo "Date: $(date)"\n')
        f.write(f'echo "Dataset: {dataset}"\n\n')
        f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
        f.write("source analysis_TPrime.sh\n")
        f.write("cd condor/\n\n")
        f.write('echo "Running command:"\n')
        f.write(f'echo "{pycommand}"\n\n')
        f.write(pycommand + "\n\n")
        f.write('echo "===== Job finished ====="\n')
        f.write('echo "Date: $(date)"\n')





for sample in samples:
    condor_folder    = os.environ.get("PWD") + "/condor_getoutputs/"
    condor_subfolder = condor_folder + sample.label + "/"
    log_folder       = condor_subfolder + "condor/"

    if not os.path.exists(condor_folder):
        os.makedirs(condor_folder)
        print(f"Creating condor folder:     {condor_folder}")
    if not os.path.exists(condor_subfolder):
        os.makedirs(condor_subfolder)
        print(f"Creating condor subfolder:  {condor_subfolder}")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
        print(f"Creating log folder:        {log_folder}")

    for subdir in ["output", "error", "log"]:
        path = os.path.join(log_folder, subdir)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    run_folder = condor_subfolder

    runner_writer(run_folder, sample.label, output_json)
    sub_writer(run_folder, log_folder, sample.label)
    # if not dryrun:
    #     os.popen("condor_submit " + run_folder + "condor.sub")
    time.sleep(2)