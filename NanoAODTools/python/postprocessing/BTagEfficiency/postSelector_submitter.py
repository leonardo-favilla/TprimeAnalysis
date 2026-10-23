import os
import optparse
import sys
import time
import shutil
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import yaml
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


usage               = "python3 postSelector_submitter.py -d dataset_name --dryrun"
parser              = optparse.OptionParser(usage)
parser.add_option("-d", "--dat",                    dest="dat",                 type=str,                                                                       help="Please enter a dataset name")
parser.add_option(      '--nfiles_max',             dest='nfiles_max',          type=int,               default = 10,                                           help='Max number of files to process per sample (the efficiencies need only a few files)')
parser.add_option(      '--dryrun',                 dest='dryrun',              action='store_true',    default = False,                                        help='dryrun')

(opt, args)         = parser.parse_args()
dataset_to_run      = opt.dat
nfiles_max          = opt.nfiles_max
dryrun              = opt.dryrun

period              = dataset_to_run.split("_")[-1]
if period not in ["2022", "2022EE", "2023", "2023postBPix", "2024"]:
    print("Please select a valid period among: 2022, 2022EE, 2023, 2023postBPix, 2024")
    sys.exit(1)

dict_samples_file   = config["dict_samples"][period]
outFolder_path      = config["outputfolder"]["btagEfficiency_results"][period]
syst_suffix         = "_xBTagEfficiency"

username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

def sub_writer(run_folder, log_folder, dataset, syst_suffix):
    f = open(run_folder+"condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write('+JobTag                 = "'+dataset+syst_suffix+'"\n')
    f.write("executable              = "+run_folder+"runner.sh\n")
    f.write("arguments               = $(Proxy_path)\n")
    f.write("output                  = "+log_folder+"output/postSelector_"+dataset+".out\n")
    f.write("error                   = "+log_folder+"error/postSelector_"+dataset+".err\n")
    f.write("log                     = "+log_folder+"log/postSelector_"+dataset+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(run_folder, dataset, dict_samples_file, hist_folder, nfiles_max):
    f = open(run_folder+"runner.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
    f.write("source analysis_TPrime.sh\n")
    f.write("cd python/postprocessing/BTagEfficiency/\n")
    pycommand = "python3 postSelector.py "+f"-d {dataset} --dict_samples_file {dict_samples_file} --hist_folder {hist_folder} --nfiles_max {nfiles_max} --tmpfold"
    f.write(pycommand+"\n")
    f.write("mkdir -p "+hist_folder+"plots/\n")
    f.write("cp /tmp/"+username+"/"+dataset+"/"+dataset+".root "+hist_folder+"plots/.\n")
    f.write("ls -lthra "+hist_folder+"plots/.\n")
    f.close()


if not os.path.exists("/tmp/x509up_u" + str(uid)):
    print("Please run voms command")
    exit()


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
        samples = sample_dict[dataset_to_run].components
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset_to_run)
        samples = [sample_dict[dataset_to_run]]

print("Samples to run: ", [s.label for s in samples])


for sample in samples:
    condor_folder           = os.environ.get('PWD') + "/condor/"
    condor_subfolder        = condor_folder + sample.label + syst_suffix + "/"
    log_folder              = condor_subfolder + "condor/"
    for folder in [condor_folder, condor_subfolder, log_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Creating folder:            {folder}")
    for log_type in ["output/", "error/", "log/"]:
        if os.path.exists(log_folder+log_type):
            shutil.rmtree(log_folder+log_type)
        os.makedirs(log_folder+log_type)

    run_folder              = condor_subfolder

    runner_writer(run_folder, sample.label, dict_samples_file, outFolder_path, nfiles_max)
    sub_writer(run_folder, log_folder, sample.label, syst_suffix)
    if not dryrun:
        os.popen("condor_submit " + run_folder + "condor.sub")
    time.sleep(2)
