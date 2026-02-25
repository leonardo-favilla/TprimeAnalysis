import os
import optparse
import sys
import time
import shutil
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import yaml
from pathlib import Path
import shutil
import json
sys.path.append('../')

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)


usage               = "python3 postSelector_submitter.py -d dataset_name --nfiles_max <nfiles_max> --dryrun"
parser              = optparse.OptionParser(usage)
parser.add_option("-d", "--dat",                    dest="dat",                 type=str,                                                                       help="Please enter a dataset name")
parser.add_option(      '--nfiles_max',             dest='nfiles_max',          type=int,               default = 100000,                                       help='Max number of files to process per sample, default is all files')
parser.add_option(      '--dryrun',                 dest='dryrun',              action='store_true',    default = False,                                        help='dryrun')

(opt, args)         = parser.parse_args()
dataset_to_run      = opt.dat
dryrun              = opt.dryrun
nfiles_max          = opt.nfiles_max

period              = dataset_to_run.split("_")[-1]
if period not in ["2022", "2022EE", "2023", "2023postBPix", "2024"]:
    print("Please select a valid period among: 2022, 2022EE, 2023, 2023postBPix")
    sys.exit(1)
year                = 0
if "2022" in period:
    year            = "2022"
elif "2023" in period:
    year            = "2023"

dict_samples_file   = config["dict_samples"][year]
if "Data" in dataset_to_run:
    scenarios       = ["nominal"]
else:
    scenarios       = ["nominal", "jerUp", "jerDown", "jesUp", "jesDown"]

username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

def sub_writer(run_folder, log_folder, component, scenario, sliceNumber):
    f = open(run_folder+"condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("request_cpus            = 4\n")
    # f.write("should_transfer_files   = YES\n")
    # f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    # f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    # f.write('requirements            = (TARGET.OpSysAndVer =?= "CentOS7")\n')
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write('+JobTag                 = "'+component+"_"+scenario+"_"+str(sliceNumber)+'"\n')
    f.write("executable              = "+run_folder+"runner.sh\n")
    f.write("arguments               = $(Proxy_path)\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+log_folder+"output/postSelector_"+component+".out\n")
    f.write("error                   = "+log_folder+"error/postSelector_"+component+".err\n")
    f.write("log                     = "+log_folder+"log/postSelector_"+component+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(run_folder, component, scenario, fileStart, fileEnd, sliceNumber):
    f = open(run_folder+"runner.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
    f.write("source analysis_TPrime.sh\n")
    f.write("cd python/postprocessing/postselection_xTopSF/\n")
    pycommand = "python3 postSelector.py "+f"-c {component} --scenario {scenario} --fileStart {fileStart} --fileEnd {fileEnd} --sliceNumber {sliceNumber} --certpath $1"

    f.write(pycommand+"\n")
    f.close()


if not os.path.exists("/tmp/x509up_u" + str(uid)):
    print("Please run voms command")
    exit()


#### LOAD dict_samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)

######## LAUNCH CONDOR ########
if dataset_to_run == '':
    print("Please enter a dataset name")
    exit()
elif dataset_to_run not in sample_dict.keys():
    print("Dataset not found")
    exit()
elif dataset_to_run in sample_dict.keys():
    if hasattr(sample_dict[dataset_to_run], "components"):
        print("---------- Running dataset: ", dataset_to_run)
        print("Components: ", [s.label for s in sample_dict[dataset_to_run].components])
        samples_list = sample_dict[dataset_to_run].components
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset_to_run)
        samples_list = [sample_dict[dataset_to_run]]

print("Samples to run: ", [s.label for s in samples_list])


for sample in samples_list:
    condor_folder           = os.environ.get('PWD') + "/condor/"
    if not os.path.exists(condor_folder):
        os.makedirs(condor_folder)
        print(f"Creating condor folder:     {condor_folder}")


    ### Determine number of files per each job ###
    nfiles_max              = min(nfiles_max, len(samples[sample.label][sample.label]['strings']))
    if nfiles_max < 200:
        nSlices             = 1
    elif nfiles_max < 500:
        nSlices             = 2
    elif nfiles_max < 1000:
        nSlices             = 4
    else:
        nSlices             = 6
    nFilesPerSlice          = nfiles_max // nSlices
    remainder               = nfiles_max % nSlices
    slices                  = []
    start                   = 0
    for i in range(nSlices):
        end                 = start + nFilesPerSlice + (1 if i < remainder else 0)
        slices.append([start, end])
        start               = end
    print(f"Component: {sample.label:<50} has {nfiles_max:<10} files to process in {nSlices:<5} slices")
    print(f"Files splitting:    {[list(range(*slice)) for slice in slices]}")

    for scenario in scenarios:
        for sliceNumber in range(nSlices):
            fileStart               = slices[sliceNumber][0]
            fileEnd                 = slices[sliceNumber][1] - 1
            condor_subfolder        = condor_folder + sample.label + "_" + scenario + "_" + str(sliceNumber) + "/"
            log_folder              = condor_subfolder + "condor/"
            if not os.path.exists(condor_subfolder):
                os.makedirs(condor_subfolder, exist_ok=True)
                print(f"Creating condor subfolder:  {condor_subfolder}")
            else:
                shutil.rmtree(condor_subfolder, ignore_errors=True)
                os.makedirs(condor_subfolder, exist_ok=True)
                print(f"Creating condor subfolder:  {condor_subfolder}")
            if not os.path.exists(log_folder):
                os.makedirs(log_folder, exist_ok=True)
                print(f"Creating log folder:        {log_folder}")
            else:
                shutil.rmtree(log_folder, ignore_errors=True)
                os.makedirs(log_folder, exist_ok=True)
                print(f"Creating log folder:        {log_folder}")
            if not os.path.exists(log_folder+"output/"):
                os.makedirs(log_folder+"output/", exist_ok=True)
            else:
                shutil.rmtree(log_folder+"output/", ignore_errors=True)
                os.makedirs(log_folder+"output/", exist_ok=True)
            if not os.path.exists(log_folder+"error/"):
                os.makedirs(log_folder+"error/", exist_ok=True)
            else:
                shutil.rmtree(log_folder+"error/", ignore_errors=True)
                os.makedirs(log_folder+"error/", exist_ok=True)
            if not os.path.exists(log_folder+"log/"):
                os.makedirs(log_folder+"log/", exist_ok=True)
            else:
                shutil.rmtree(log_folder+"log/", ignore_errors=True)
                os.makedirs(log_folder+"log/", exist_ok=True)

            run_folder              = condor_subfolder


            runner_writer(run_folder, sample.label, scenario, fileStart, fileEnd, sliceNumber)
            sub_writer(run_folder, log_folder, sample.label, scenario, sliceNumber)
            if not dryrun:
                print("Submitting condor job for sample ", sample.label, " scenario ", scenario, " slice ", sliceNumber)
                os.popen("condor_submit " + run_folder + "condor.sub")
            time.sleep(2)