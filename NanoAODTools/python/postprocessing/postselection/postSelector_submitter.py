import os
import optparse
import sys
import time
import shutil
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import yaml
from pathlib import Path
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


usage               = "python3 postSelector_submitter.py -d dataset_name --syst --dryrun --noSFbtag"
parser              = optparse.OptionParser(usage)
parser.add_option("-d", "--dat",                    dest="dat",                 type=str,                                                                       help="Please enter a dataset name")
# parser.add_option(      '--period',                 dest='period',              type=str,               default = "2023",                                       help='era you are running: 2022, 2022EE, 2023 or 2023postBPix')
parser.add_option(      '--syst',                   dest='syst',                action='store_true',    default = False,                                        help='calculate jerc')
parser.add_option(      '--dryrun',                 dest='dryrun',              action='store_true',    default = False,                                        help='dryrun')
parser.add_option(      '--noSFbtag',               dest='noSFbtag',            action='store_true',    default = False,                                        help='remove b tag SF')
parser.add_option(      '--noPuWeight',             dest='noPuWeight',          action='store_true',    default = False,                                        help='remove PU weight')
parser.add_option(      '--noTopPtWeight',          dest='noTopPtWeight',       action='store_true',    default = False,                                        help='remove top pt weight')
parser.add_option(      '--noTrotaSF',              dest='noTrotaSF',           action='store_true',    default = False,                                        help='remove Trota SF')
parser.add_option(      '--printcutflow',           dest='printcutflow',        action='store_true',    default=False,                                          help='print cutflow')

(opt, args)         = parser.parse_args()
dataset_to_run      = opt.dat
syst                = opt.syst
nfiles_max          = 10000#opt.nfiles_max
dryrun              = opt.dryrun
noSFbtag            = opt.noSFbtag
noPuWeight          = opt.noPuWeight
noTopPtWeight       = opt.noTopPtWeight
noTrotaSF           = opt.noTrotaSF
printcutflow        = opt.printcutflow

period              = dataset_to_run.split("_")[-1]
if period not in ["2022", "2022EE", "2023", "2023postBPix", "2024"]:
    print("Please select a valid period among: 2022, 2022EE, 2023, 2023postBPix")
    sys.exit(1)
year                = 0
if "2022" in period:
    year            = "2022"
elif "2023" in period:
    year            = "2023"
elif "2024" in period:
    year            = "2024"

dict_samples_file   = config["dict_samples"][year]

syst_suffix         = ""
if syst:
    syst_suffix    += "_syst"
if noSFbtag:
    syst_suffix    += "_noSFbtag"
if noPuWeight:
    syst_suffix    += "_noPuWeight"
if noTopPtWeight:
    syst_suffix    += "_noTopPtWeight"
if noTrotaSF:
    syst_suffix    += "_noTrotaSF"

outFolder_path      = config["outputfolder"]["postselector_results"][period]

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
    runner_path = run_folder + "runner.sh"
    run_label   = os.path.basename(os.path.normpath(hist_folder))
    dest_dir    = hist_folder.rstrip("/") + "/plots"
    base_tmp     = "/tmp/" + username
    pycommand = (
        "python3 postSelector.py "
        + f"-d {dataset} "
        + f"--dict_samples_file {dict_samples_file} "
        + f"--hist_folder {hist_folder} "
        + f"--nfiles_max {nfiles_max} "
        + "--tmpfold"
    )

    if syst:
        pycommand += " --syst"
    if noSFbtag:
        pycommand += " --noSFbtag"
    if noPuWeight:
        pycommand += " --noPuWeight"
    if noTopPtWeight:
        pycommand += " --noTopPtWeight"
    if noTrotaSF:
        pycommand += " --noTrotaSF"
    if printcutflow:
        pycommand += " --printcutflow"

    with open(runner_path, "w") as f:
        f.write("#!/usr/bin/bash\n")
        f.write('echo "===== Job started ====="\n')
        f.write('echo "Host: $(hostname)"\n')
        f.write('echo "Date: $(date)"\n')
        f.write('echo "User: ${USER:-unknown}"\n')
        f.write('echo "PWD at start: $(pwd)"\n')
        
        f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
        f.write("source analysis_TPrime.sh\n")
        f.write("cd python/postprocessing/postselection/\n\n")

        f.write(f'base_tmp="{base_tmp}"\n')
        f.write(f'run_label="{run_label}"\n')
        f.write(f'dataset="{dataset}"\n')
        f.write('outdir="${base_tmp}/${run_label}/${dataset}"\n')
        f.write('outfile="${outdir}/${dataset}.root"\n')
        f.write(f'destdir="{dest_dir}"\n\n')

        f.write('echo "base_tmp: ${base_tmp}"\n')
        f.write('echo "outdir: ${outdir}"\n')
        f.write('echo "outfile: ${outfile}"\n')
        f.write('echo "destdir: ${destdir}"\n\n')

        f.write('echo "Creating local output directory: ${outdir}"\n')
        f.write('mkdir -p "${outdir}"\n')
        f.write('mkdir -p "${destdir}"\n\n')

        f.write('echo "Running postSelector command:"\n')
        f.write(f'echo "{pycommand}"\n\n')
        f.write(pycommand + "\n")
        f.write('echo "Checking expected output file: ${outfile}"\n')
        f.write('if [ ! -s "${outfile}" ]; then\n')
        f.write('    echo "ERROR: expected output file does not exist or is empty: ${outfile}" >&2\n')
        f.write('    echo "Listing base tmp area:" >&2\n')
        f.write('    ls -lthra "${base_tmp}" || true\n')
        f.write('    echo "Listing run label directory:" >&2\n')
        f.write('    ls -lthra "${base_tmp}/${run_label}" || true\n')
        f.write('    echo "Listing expected output directory:" >&2\n')
        f.write('    ls -lthra "${outdir}" || true\n')
        f.write("fi\n\n")

        f.write('echo "Copying output to ${destdir}"\n')
        f.write('cp "${outfile}" "${destdir}/"\n\n')

        f.write('echo "Final destination content:"\n')
        f.write('ls -lthra "${destdir}/"\n\n')

        f.write('echo "===== Job finished successfully ====="\n')
        f.write('echo "Date: $(date)"\n')

    
    # f = open(run_folder+"runner.sh", "w")
    # f.write("#!/usr/bin/bash\n")
    # f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
    # f.write("source analysis_TPrime.sh\n")
    # f.write("cd python/postprocessing/postselection/\n")
    # pycommand = "python3 postSelector.py "+f"-d {dataset} --dict_samples_file {dict_samples_file} --hist_folder {hist_folder} --nfiles_max {nfiles_max} --tmpfold"
    # if syst:
    #     pycommand += " --syst"
    # if noSFbtag:
    #     pycommand += " --noSFbtag"
    # if noPuWeight:
    #     pycommand += " --noPuWeight"
    # if noTopPtWeight:
    #     pycommand += " --noTopPtWeight"
    # if noTrotaSF:
    #     pycommand += " --noTrotaSF"
    # if printcutflow:
    #     pycommand += " --printcutflow"

    # f.write(pycommand+"\n")
    # f.write("ls -lthra /tmp/"+username+"/"+"\n")
    # f.write("ls -lthra /tmp/"+username+"/"+os.path.basename(os.path.normpath(hist_folder))+"/"+"\n")
    # f.write("ls -lthra /tmp/"+username+"/"+os.path.basename(os.path.normpath(hist_folder))+"/"+dataset+"/"+"\n")
    # f.write("cp /tmp/"+username+"/"+os.path.basename(os.path.normpath(hist_folder))+"/"+dataset+"/"+dataset+".root "+hist_folder+"plots/.\n")
    # f.write("ls -lthra "+hist_folder+"plots/.\n")
    # f.close()


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
    condor_folder           = os.environ.get('PWD') + "/condor" + syst_suffix + "/"
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
    else:
        shutil.rmtree(log_folder+"output/")
        os.makedirs(log_folder+"output/")
    if not os.path.exists(log_folder+"error/"):
        os.makedirs(log_folder+"error/")
    else:
        shutil.rmtree(log_folder+"error/")
        os.makedirs(log_folder+"error/")
    if not os.path.exists(log_folder+"log/"):
        os.makedirs(log_folder+"log/")
    else:
        shutil.rmtree(log_folder+"log/")
        os.makedirs(log_folder+"log/")

    run_folder              = condor_subfolder

    runner_writer(run_folder, sample.label, dict_samples_file, outFolder_path, nfiles_max, syst)
    sub_writer(run_folder, log_folder, sample.label, syst_suffix)
    if not dryrun:
        os.popen("condor_submit " + run_folder + "condor.sub")
    time.sleep(2)