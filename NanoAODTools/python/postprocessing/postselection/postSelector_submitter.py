import os
import optparse
import sys
import time
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')




usage               = "python3 postSelector_submitter.py -d dataset_name --dict_samples_file <dict_samples_file> --hist_folder <hist_folder> --syst --dryrun"
parser              = optparse.OptionParser(usage)
parser.add_option("-d", "--dat",                    dest="dat",                 type=str,                                                                       help="Please enter a dataset name")
parser.add_option(      "--dict_samples_file",      dest="dict_samples_file",   type=str,               default = "../samples/dict_samples_2023.json",          help="Please enter a samples dictionary file, e.g. ../samples/dict_samples_2023.json")
parser.add_option(      '--hist_folder',            dest='hist_folder',         type=str,               default = "run2023/",                                   help='Folder where to save the histograms, e.g. run2023/')
parser.add_option(      '--syst',                   dest='syst',                action='store_true',    default = False,                                        help='calculate jerc')
parser.add_option(      '--dryrun',                 dest='dryrun',              action='store_true',    default = False,                                        help='dryrun')
(opt, args)         = parser.parse_args()
dataset_to_run      = opt.dat
dict_samples_file   = opt.dict_samples_file
hist_folder         = opt.hist_folder
syst                = opt.syst
nfiles_max          = 1000 # opt.nfiles_max
dryrun              = opt.dryrun
if not syst:
    syst_suffix     = ""
else:
    syst_suffix     = "_syst_noSFbtag"

results_folder      = "/eos/user/l/lfavilla/RDF_DManalysis/results/"
outFolder_path      = results_folder + hist_folder
if not os.path.exists(outFolder_path):
    os.makedirs(outFolder_path)
    print(f"Creating output folder:     {outFolder_path}")



username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

def sub_writer(run_folder, log_folder, dataset, syst_suffix):
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
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write('+JobTag                 = "'+dataset+syst_suffix+'"\n')
    f.write("executable              = "+run_folder+"runner.sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+log_folder+"output/postSelector_"+dataset+".out\n")
    f.write("error                   = "+log_folder+"error/postSelector_"+dataset+".err\n")
    f.write("log                     = "+log_folder+"log/postSelector_"+dataset+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(run_folder, dataset, dict_samples_file, hist_folder, nfiles_max, syst=False):
    f = open(run_folder+"runner.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
    f.write("source analysis_TPrime.sh\n")
    f.write("cd python/postprocessing/postselection/\n")
    if syst:
        f.write("python3 postSelector.py "+f"-d {dataset} --dict_samples_file {dict_samples_file} --hist_folder {hist_folder} --nfiles_max {nfiles_max} --syst"+"\n")
    else:
        f.write("python3 postSelector.py "+f"-d {dataset} --dict_samples_file {dict_samples_file} --hist_folder {hist_folder} --nfiles_max {nfiles_max}"+"\n")




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
    condor_folder           = "/afs/cern.ch/" + workdir + "/" + inituser + "/" + username + "/TprimeAnalysis/NanoAODTools/python/postprocessing/postselection/condor_noSFbtag/"
    condor_subfolder        = condor_folder + sample.label + syst_suffix + "/"
    log_folder              = condor_subfolder + "condor/"
    if not os.path.exists(condor_folder):
        os.makedirs(condor_folder)
        print(f"Creating condor folder:     {condor_folder}")
    if not os.path.exists(condor_subfolder):
        os.makedirs(condor_subfolder)
        print(f"Creating condor subfolder:  {condor_subfolder}")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
        print(f"Creating log folder:        {log_folder}")
    if not os.path.exists(log_folder+"output/"):
        os.makedirs(log_folder+"output/")
    if not os.path.exists(log_folder+"error/"):
        os.makedirs(log_folder+"error/")
    if not os.path.exists(log_folder+"log/"):
        os.makedirs(log_folder+"log/")


    outSubFolder_path       = outFolder_path+"/plots/"
    run_folder              = condor_subfolder
    if not os.path.exists(run_folder):
        os.makedirs(run_folder)
        print(f"Creating run folder:        {run_folder}")
    if not os.path.exists(outSubFolder_path):
        os.makedirs(outSubFolder_path)
        print(f"Creating out subfolder:     {outSubFolder_path}")

    runner_writer(run_folder, sample.label, dict_samples_file, hist_folder, nfiles_max, syst)
    sub_writer(run_folder, log_folder, sample.label, syst_suffix)
    if not dryrun:
        os.popen("condor_submit " + run_folder + "condor.sub")
    time.sleep(2)