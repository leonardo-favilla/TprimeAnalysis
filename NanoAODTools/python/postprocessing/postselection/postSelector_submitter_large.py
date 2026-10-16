import os
import optparse
import sys
import time
import json
import shutil
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.postselection.splitter import sampleSplitter

import yaml
from pathlib import Path
sys.path.append('../')


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
parser.add_option(      '--printcutflow',           dest='printcutflow',        action='store_true',    default = False,                                        help='print cutflow')

parser.add_option( '-m',     '--mode',           dest='mode',        type=str ,  default = "s",                 help='modes: s = submit, c = check failed, r = resubmit failed, h = add histograms  ')

parser.add_option('--config_paths', dest='config_paths', type=str, default = None, help='config file path ')
parser.add_option('--dict_samples_file', dest='dict_samples_file', type=str, default = None, help='samples file path - will override the one in the config ')
parser.add_option('--suffix', dest='suffix', type=str,               default = None, help='suffix to add to condor folder name')
parser.add_option('--partsize', dest='partsize',type=int,    default=-1, help='size of the dataset portion to get. To use if you are doing the a-priori splitting option, together with npart ')
parser.add_option(      '--mergepath',           dest='mergepath',        type=str,    default = "",       help='path where you want to merge histograms, if different from output folder  ')

parser.add_option(      '--outpath',           dest='outpath',        type=str,    default = "",       help='path where you want to output histograms, if different from  path of the config file  ')
parser.add_option(      '--verbose',           dest='verbose',        type=int,    default = 0,       help='output verbosity level  ')


(opt, args)         = parser.parse_args()
dataset_to_run      = opt.dat
syst                = opt.syst
dryrun              = opt.dryrun
nfiles_max          = 10000
# nfiles_max          = 10000 if not dryrun else 1
noSFbtag            = opt.noSFbtag
noPuWeight          = opt.noPuWeight
noTopPtWeight       = opt.noTopPtWeight
noTrotaSF           = opt.noTrotaSF
printcutflow        = opt.printcutflow
njobs_per_part      = opt.partsize
suffix              = f"_{opt.suffix}" if opt.suffix is not None else ""
mode = opt.mode
verb = opt.verbose

if not ( (mode == "s") or (mode=="r") or (mode =="c") or (mode == "h")):
    print("operational mode should be s, c, r, or h - please check that was not a typo in the command line for the option --mode ")
    exit

config = {}
config_p = os.environ.get('PWD')+'/../config/config.yaml'
config_p = os.environ.get('PWD')+'/../config/config_tdm.yaml'

config_paths = os.environ.get('PWD')+f"/{opt.config_paths}" if opt.config_paths is not None else config_p 

if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

print(dataset_to_run)

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

dict_samples_file   = config["dict_samples"][year] if opt.dict_samples_file is None else opt.dict_samples_file
#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samplesfile = json.load(sample_file)


# suffix         = ""
# if syst:
#     suffix    += "_syst"
# if noSFbtag:
#     suffix    += "_noSFbtag"
# if noPuWeight:
#     suffix    += "_noPuWeight"
# if noTopPtWeight:
#     suffix    += "_noTopPtWeight"
# if noTrotaSF:
#     suffix    += "_noTrotaSF"

outFolder_path      = config["outputfolder"]["postselector_results"][period] if opt.outpath=="" else opt.outpath
mergeFolder_path = outFolder_path if opt.mergepath=="" else opt.mergepath
print("outfolder path: ",outFolder_path)
username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

def sub_writer(run_folder, log_folder, dataset, suffix):
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
    f.write('+JobTag                 = "'+dataset+suffix+'"\n')
    f.write("executable              = "+run_folder+"runner.sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+log_folder+"output/postSelector_"+dataset+".out\n")
    f.write("error                   = "+log_folder+"error/postSelector_"+dataset+".err\n")
    f.write("log                     = "+log_folder+"log/postSelector_"+dataset+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(run_folder, dataset, dict_samples_file, hist_folder, nfiles_max, syst=False, parts="",filesuffix=""):
    runner_path = run_folder + "runner.sh"
    run_label   = os.path.basename(os.path.normpath(hist_folder))
    dest_dir    = hist_folder.rstrip("/") + "/plots"
    base_tmp    = "/tmp/" + username

    pycommand = (
        "python3 postSelector.py "
        + f"-d {dataset} "
        + f"--dict_samples_file {dict_samples_file} "
        + f"--hist_folder {hist_folder} "
        + f"--nfiles_max {nfiles_max} "
        + f"{parts} "
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
        f.write("source setANRun3Workspace.sh\n")
#       f.write("source analysis_TPrime.sh\n")
        f.write("cd python/postprocessing/postselection/\n\n")

        f.write(f'base_tmp="{base_tmp}"\n')
        f.write(f'run_label="{run_label}"\n')
        f.write(f'dataset="{dataset}"\n')
        f.write('outdir="${base_tmp}/${run_label}/${dataset}"\n')
        f.write('outfile="${outdir}/${dataset}'+filesuffix+'.root"\n')
        f.write(f'destdir="{dest_dir}"\n\n')

        f.write('echo "base_tmp: ${base_tmp}"\n')
        f.write('echo "outdir: ${outdir}"\n')
        f.write('echo "outfile: ${outfile}"\n')
        f.write('echo "destdir: ${destdir}"\n\n')

        f.write('echo "Creating local output directory: ${outdir}"\n')
        f.write('mkdir -p "${outdir}"\n')
        f.write('mkdir -p "${destdir}"\n\n')

        # ------------------------------------------------------------
        # Run postSelector
        # ------------------------------------------------------------

        f.write('echo "Running postSelector command:"\n')
        f.write(f'echo "{pycommand}"\n\n')

        f.write(pycommand + "\n")
        f.write("postselector_status=$?\n\n")

        f.write('echo "postSelector.py exit code: ${postselector_status}"\n\n')

        # ------------------------------------------------------------
        # Check postSelector exit code
        # ------------------------------------------------------------

        f.write('if [ "${postselector_status}" -ne 0 ]; then\n')
        f.write('    echo "ERROR: postSelector.py failed with exit code ${postselector_status}" >&2\n')
        f.write('    exit "${postselector_status}"\n')
        f.write("fi\n\n")

        # ------------------------------------------------------------
        # Check output file
        # ------------------------------------------------------------

        f.write('echo "Checking expected output file: ${outfile}"\n')

        f.write('if [ ! -s "${outfile}" ]; then\n')
        f.write('    echo "ERROR: expected output file does not exist or is empty: ${outfile}" >&2\n')

        f.write('    echo "Listing base tmp area:" >&2\n')
        f.write('    ls -lthra "${base_tmp}" || true\n')

        f.write('    echo "Listing run label directory:" >&2\n')
        f.write('    ls -lthra "${base_tmp}/${run_label}" || true\n')

        f.write('    echo "Listing expected output directory:" >&2\n')
        f.write('    ls -lthra "${outdir}" || true\n')

        f.write("    exit 1\n")
        f.write("fi\n\n")

        f.write('echo "Output file successfully produced:"\n')
        f.write('ls -lh "${outfile}"\n\n')

        # ------------------------------------------------------------
        # Copy output
        # ------------------------------------------------------------

        f.write('echo "Copying output to ${destdir}"\n')
        f.write('cp "${outfile}" "${destdir}/"\n')
        f.write("cp_status=$?\n\n")

        f.write('if [ "${cp_status}" -ne 0 ]; then\n')
        f.write('    echo "ERROR: failed to copy output to ${destdir}" >&2\n')
        f.write('    exit "${cp_status}"\n')
        f.write("fi\n\n")

        # ------------------------------------------------------------
        # Final check
        # ------------------------------------------------------------

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


def checkJobHasFailed(condorFolder, sampleLabel, dataset, verbose=0): #returns true if the job has to be rerun
    if not os.path.exists(condorFolder):
        if(verbose==1): print ("job does not have condor folder - has to be rerun" )
        return True

    outputfileName=condorFolder+"/condor/output/postSelector_"+sampleLabel+".out"
    errorfileName=condorFolder+"/condor/error/postSelector_"+sampleLabel+".err"
    
    outputfileExists=os.path.exists(outputfileName)
    errorfileExists=os.path.exists(errorfileName)

    if(verbose==1):
        print("outfile ",outputfileName," exists? ", outputfileExists)
        print("errorfile ",errorfileName," exists? ", errorfileExists)
    
    jobHasEnded = (outputfileExists and errorfileExists)#check here job is not running - still to implement better 
    if jobHasEnded==False:
        if(verbose==1): print ("job had not ended - does not have to be rerun yet") 
        return False

    if (errorfileExists and not outputfileExists):
        if(verbose==1): print ("only error exists, this should not happen - job has to be rerun ") 
        return True

    with open (outputfileName,"r" ) as fo:
        if not ( ("postSelector.py exit code: 0" in fo.read() ) or ("failed to copy output" in fo.read() ) ): 
            if(verbose==1): print ("postselector did end with an error or not at all - job has to be rerun") 
            return True
        else:
            if(verbose==1): print ("postselector did end successfully")
    #alternative: put a check on the output root file whether it exists
        
    return False

#outFolder_path      = config["outputfolder"]["postselector_results"][period]
def histoMergeWriter(outpath, mergepath, sampleLabel):
    if not os.path.exists(mergepath):
        print (" warning, merge path: "+mergepath+" did not exist at time of adding histos, creating it on the fly.")
        os.makedirs(mergepath)
    commandHadd = "hadd -f "+mergepath+"/"+sampleLabel+".root " + outpath+"/"+sampleLabel+"_part*.root" 
    return commandHadd
    
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    print("Please run voms command")
    exit()

pass_fail_jobs={}
#maxlaunch = 10

#njobs_per_part=100

######## LAUNCH CONDOR ########
dss=opt.dat.split(",")
if len(dss)==0:
    print("Please enter a dataset name")
    exit()
for d in dss:
    dataset_to_run = d
    if dataset_to_run == '':
        print("Please enter a dataset name")
        exit()
    elif dataset_to_run not in sample_dict.keys():
        print("Dataset not found")
        exit()
    elif dataset_to_run in sample_dict.keys():
        dat= sample_dict[dataset_to_run]
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
        nsplit,lastpartsize = sampleSplitter(samplesfile,sample.label,dat,njobs_per_part) 
        if mode == "h":
            if nsplit>1:
                hcommand = histoMergeWriter(outFolder_path+"/plots", mergeFolder_path+"/plots", sample.label)
                print (" histomerge command is \n", hcommand)
                if not dryrun:
                    os.system(hcommand)
                    time.sleep(3)
                    continue
            if nsplit==1:
                cpcommand= "cp "+outFolder_path+"/plots/"+sample.label+".root " + mergeFolder_path+"/plots/"+sample.label+".root"
                print (" histomerge copy command is \n", cpcommand)
                if not dryrun:
                    os.system(cpcommand)
                    time.sleep(3)
                    continue
        for ns in range(nsplit):
            postsuffix=""
            parts=""
            partsize=njobs_per_part
            if(nsplit>1):
                postsuffix="_part"+str(ns)
                firstfile=ns*partsize
                if(ns==nsplit-1):partsize=lastpartsize
                parts = (f"--partsize {partsize} --firstfile {firstfile} --npart {ns}")
                
                #print(ns)

            locsuffix=suffix+postsuffix
            
            
            condor_folder           = os.environ.get('PWD') + "/condor" + suffix + "/"
            condor_subfolder        = condor_folder + sample.label + locsuffix + "/"
            log_folder              = condor_subfolder + "condor/"

            hasFailed=False
            if (mode == "c" or mode == "r"): hasFailed= checkJobHasFailed(condor_subfolder,sample.label,dat,0)

            pass_fail_jobs[sample.label + locsuffix] = 1*(not hasFailed)
            if mode=="c":
                if (verb>0): print(" job in ", condor_subfolder, " has failed? ",hasFailed)
                
            if ( mode =="s" or (mode == "r" and hasFailed)):
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
                runner_writer(run_folder, sample.label, dict_samples_file, outFolder_path, nfiles_max, syst, parts, postsuffix)
                sub_writer(run_folder, log_folder, sample.label, locsuffix)
                if not dryrun: 
                    os.popen("condor_submit " + run_folder + "condor.sub")
                    time.sleep(0.1)

            
            
if mode == "c" or mode == "r": 
    for ss in pass_fail_jobs:
        if(verb>1): print (f"{ss} {pass_fail_jobs[ss]}")
    if(verb>0): print ("files to rerun: ")
    ntorerun=0
    for ss in pass_fail_jobs:
        if(pass_fail_jobs[ss]==0):
            ntorerun+=1
            if(verb>0):print(ss)
    if(mode=="c"): print("total to rerun: "+str(ntorerun))
    if(mode=="r"): print("total being rerun: "+str(ntorerun))
