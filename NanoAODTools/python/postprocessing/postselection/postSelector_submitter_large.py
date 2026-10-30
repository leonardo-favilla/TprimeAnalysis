import os
import optparse
import sys
import time
import json
import shutil
import filecmp
import subprocess
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
parser.add_option(      '--varfile',                dest='varfile',             type=str,               default = "../variables.py",                            help='variables file passed to postSelector.py (cuts and regions), resolved from the submission folder')

parser.add_option( '-m',     '--mode',           dest='mode',        type=str ,  default = "s",                 help='modes: s = submit, c = check failed, r = resubmit failed, h = add histograms (hadd <outpath>/parts/<sample>_part*.root into <mergepath>/plots/<sample>.root, merged in a local copy in /tmp/<user>/)  ')

parser.add_option('--config_paths', dest='config_paths', type=str, default = None, help='config file path ')
parser.add_option('--dict_samples_file', dest='dict_samples_file', type=str, default = None, help='samples file path - will override the one in the config ')
parser.add_option('--suffix', dest='suffix', type=str,               default = None, help='suffix to add to condor folder name')
parser.add_option('--partsize', dest='partsize',type=int,    default=-1, help='size of the dataset portion to get. To use if you are doing the a-priori splitting option, together with npart. Split outputs are saved in <outpath>/parts/ ')
parser.add_option(      '--mergepath',           dest='mergepath',        type=str,    default = "",       help='path where you want to merge histograms, if different from output folder  ')
parser.add_option(      '--rmparts',           dest='rmparts',        action='store_true',    default = False,       help='with -m h: remove <outpath>/parts/<sample>_part*.root after a successful and checked merge (and parts/ when empty); use it as the last step, -m c/r then see the removed parts as failed jobs  ')

parser.add_option(      '--outpath',           dest='outpath',        type=str,    default = "",       help='path where you want to output histograms, if different from  path of the config file  ')
parser.add_option(      '--verbose',           dest='verbose',        type=int,    default = 0,       help='output verbosity level  ')
parser.add_option(      '--setupFile',           dest='setupFile',        type=str,    default = "analysis_TPrime.sh",       help='shell files to setup analysis in the home directory  ')

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
# absolute path: the jobs run from another folder
varfile             = os.path.abspath(opt.varfile)
if not os.path.exists(varfile):
    print(f"variables file {varfile} not found - please check the option --varfile")
    exit()
njobs_per_part      = opt.partsize
suffix              = f"_{opt.suffix}" if opt.suffix is not None else ""
mode = opt.mode
verb = opt.verbose
rmparts = opt.rmparts

if not ( (mode == "s") or (mode=="r") or (mode =="c") or (mode == "h")):
    print("operational mode should be s, c, r, or h - please check that was not a typo in the command line for the option --mode ")
    exit

config = {}
config_p = os.environ.get('PWD')+'/../config/config.yaml'
# config_p = os.environ.get('PWD')+'/../config/config_tdm.yaml'

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
    # split jobs (filesuffix="_partN") go to parts/, merged into plots/ with -m h
    dest_subdir = "parts" if filesuffix else "plots"
    dest_dir    = hist_folder.rstrip("/") + "/" + dest_subdir
    base_tmp    = "/tmp/" + username

    pycommand = (
        "python3 postSelector.py "
        + f"-d {dataset} "
        + f"--dict_samples_file {dict_samples_file} "
        + f"--hist_folder {hist_folder} "
        + f"--nfiles_max {nfiles_max} "
        + f"{parts} "
        + f"--varfile {varfile} "
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
        f.write("source "+opt.setupFile+"\n")
        #f.write("source setANRun3Workspace.sh\n")
        #f.write("source analysis_TPrime.sh\n")

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

        # cp on the EOS fuse mount can return 0 (and ls show the full size from the local cache)
        # while the file on the server is truncated: check the size seen by the server with xrdfs.
        # A previous truncated copy can be left with incomplete replicas, which EOS refuses to extend
        # ("Read-only file system"): remove it before copying, so that a new file is created
        f.write('echo "Copying output to ${destdir}"\n')
        f.write('local_size=$(stat -c %s "${outfile}")\n')
        f.write('remote_file="${destdir}/$(basename "${outfile}")"\n')
        f.write("copy_ok=0\n")
        f.write("for attempt in 1 2 3; do\n")
        f.write('    rm -f "${remote_file}"\n')
        f.write('    if ! cp "${outfile}" "${destdir}/"; then\n')
        f.write('        echo "cp failed (attempt ${attempt})" >&2\n')
        f.write("        sleep 30\n")
        f.write("        continue\n")
        f.write("    fi\n")
        f.write("    for check in 1 2 3 4 5 6; do\n")
        f.write('        remote_size=$(xrdfs eosuser.cern.ch stat "${remote_file}" 2>/dev/null | awk \'/^Size:/{print $2}\')\n')
        f.write('        echo "attempt ${attempt}, check ${check}: local size ${local_size}, EOS size ${remote_size}"\n')
        f.write('        if [ "${remote_size}" = "${local_size}" ]; then\n')
        f.write("            copy_ok=1\n")
        f.write("            break 2\n")
        f.write("        fi\n")
        f.write("        sleep 10\n")
        f.write("    done\n")
        f.write("done\n\n")

        f.write('if [ "${copy_ok}" -ne 1 ]; then\n')
        f.write('    echo "ERROR: failed to copy output to ${destdir} (size on EOS does not match the local file)" >&2\n')
        f.write("    exit 1\n")
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


def checkOutputFileIsBad(path): #returns true if the root file is missing, empty, truncated or without keys
    import ROOT
    ROOT.gErrorIgnoreLevel = ROOT.kFatal
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return True
    try:
        tf = ROOT.TFile.Open(path)
    except OSError:
        return True
    if not tf or tf.IsZombie():
        return True
    bad = tf.TestBit(ROOT.TFile.kRecovered) or tf.GetListOfKeys().GetEntries() == 0
    tf.Close()
    return bad

def getQueuedJobs(): #returns {JobTag: (state, "cluster.proc", holdReason)} for the jobs of the user still in the condor queue
    states = {"1": "idle", "2": "running", "5": "held", "6": "running", "7": "suspended"} # 3 = removed, 4 = completed: not in the queue anymore
    cmd = ["condor_q", "-af:t", "JobTag", "JobStatus", "ClusterId", "ProcId", "HoldReason"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
    except OSError as e:
        res = None
        err = str(e)
    if res is None or res.returncode != 0:
        # never assume an empty queue: jobs still running would be resubmitted
        print("ERROR: condor_q failed, cannot tell which jobs are still in the queue - exiting")
        print(err if res is None else res.stderr)
        sys.exit(1)
    queued = {}
    for line in res.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 5 or fields[1] not in states:
            continue
        queued[fields[0]] = (states[fields[1]], fields[2]+"."+fields[3], fields[4] if fields[4] != "undefined" else "")
    return queued

def checkJobHasFailed(condorFolder, sampleLabel, dataset, outfilePath, verbose=0, queueKnown=False): #returns true if the job has to be rerun
    # queueKnown: the job is known not to be in the condor queue (checked with condor_q)
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
    
    jobHasEnded = (outputfileExists and errorfileExists)
    if jobHasEnded==False:
        if queueKnown:
            if(verbose==1): print ("job not in queue and without logs - lost, has to be rerun")
            return True
        if(verbose==1): print ("job had not ended - does not have to be rerun yet")
        return False

    if (errorfileExists and not outputfileExists):
        if(verbose==1): print ("only error exists, this should not happen - job has to be rerun ") 
        return True

    # the runner prints this only after postSelector, the output check and the copy to EOS all succeeded
    # (ERROR messages go to stderr, i.e. to the .err file)
    with open (outputfileName,"r" ) as fo:
        if "===== Job finished successfully =====" not in fo.read():
            if(verbose==1): print ("postselector did end with an error or not at all - job has to be rerun")
            return True
        else:
            if(verbose==1): print ("postselector did end successfully")

    if checkOutputFileIsBad(outfilePath):
        if(verbose==1): print ("output file "+outfilePath+" is missing, truncated or empty - job has to be rerun")
        return True

    return False

#outFolder_path      = config["outputfolder"]["postselector_results"][period]
def histoMergeWriter(localParts, localMerged):
    # parallel hadd of the local copies of the parts
    commandHadd = "hadd -f -j 4 "+localMerged+" " + " ".join(localParts)
    return commandHadd

def checkMergedFile(parts, merged, nCheck=20): #returns true if the merged file has the same histograms as the parts and the sums add up
    # same number of keys in every part and in the merged file; for nCheck histograms spread over the key list,
    # sum of bin contents (including under/overflow) and entries of the merged one equal to the sum over the parts
    import ROOT
    ROOT.gErrorIgnoreLevel = ROOT.kFatal
    fm = ROOT.TFile.Open(merged)
    keys = [k.GetName() for k in fm.GetListOfKeys()]
    names = keys[::max(1, len(keys)//nCheck)]
    hm = {n: fm.Get(n) for n in names}
    sumContent = {n: 0. for n in names}
    sumEntries = {n: 0. for n in names}
    for p in parts:
        fp = ROOT.TFile.Open(p)
        if fp.GetListOfKeys().GetEntries() != len(keys):
            print (" ERROR: "+p+" has "+str(fp.GetListOfKeys().GetEntries())+" keys, the merged file "+str(len(keys)))
            fp.Close()
            fm.Close()
            return False
        for n in names:
            h = fp.Get(n)
            sumContent[n] += sum(h.GetBinContent(i) for i in range(h.GetNcells()))
            sumEntries[n] += h.GetEntries()
        fp.Close()
    good = True
    for n in names:
        content = sum(hm[n].GetBinContent(i) for i in range(hm[n].GetNcells()))
        if abs(content - sumContent[n]) > 1e-6*max(abs(content), abs(sumContent[n]), 1e-300) or hm[n].GetEntries() != sumEntries[n]:
            print (" ERROR: "+n+" in the merged file: content "+str(content)+", entries "+str(hm[n].GetEntries())+", sum over the parts: content "+str(sumContent[n])+", entries "+str(sumEntries[n]))
            good = False
    fm.Close()
    return good

def histoMerge(outpath, mergepath, sampleLabel, nsplit, dryrun=False, rmparts=False): #returns true if the merge succeeded
    # hadd reading the parts on EOS takes minutes per sample (many small reads): the parts are copied
    # to a local folder in /tmp, merged there and the result is copied back to EOS (~25 s for 78 parts)
    # rmparts: the parts of the sample are removed if the merged file matches the parts and its copy on EOS is identical
    # to the local one; parts/ is removed when empty, i.e. after the last sample
    parts =[outpath+"/"+sampleLabel+"_part"+str(ns)+".root" for ns in range(nsplit)]
    badParts = [p for p in parts if checkOutputFileIsBad(p)]
    if badParts:
        print (" ERROR: "+sampleLabel+" not merged, missing or broken parts (rerun them with -m r):")
        for p in badParts: print ("   "+p)
        return False
    localFolder = "/tmp/"+username+"/merge_"+sampleLabel+"_"+str(os.getpid())
    localParts  = [localFolder+"/"+os.path.basename(p) for p in parts]
    localMerged = localFolder+"/"+sampleLabel+".root"
    tmpMerged   = mergepath+"/tmp_"+sampleLabel+".root"       # renamed to <sampleLabel>.root only if the merge succeeded
    hcommand    = histoMergeWriter(localParts, localMerged)
    print (" histomerge: "+str(nsplit)+" parts copied to "+localFolder+", command is \n", hcommand)
    if dryrun:
        return True
    if not os.path.exists(mergepath):
        print (" warning, merge path: "+mergepath+" did not exist at time of adding histos, creating it on the fly.")
        os.makedirs(mergepath)
    try:
        os.makedirs(localFolder)
        for p, lp in zip(parts, localParts):
            shutil.copy(p, lp)
        haddStatus = os.system(hcommand)
        if haddStatus != 0 or checkOutputFileIsBad(localMerged):
            print (" ERROR: hadd failed for "+sampleLabel+" (exit status "+str(haddStatus)+"), "+mergepath+"/"+sampleLabel+".root left untouched")
            return False
        mergeChecked = rmparts and checkMergedFile(localParts, localMerged)  # on the local copies, fast
        if rmparts and not mergeChecked:
            print (" ERROR: check of the merged file failed for "+sampleLabel+", parts NOT removed")
        shutil.copy(localMerged, tmpMerged)
        # the copy is always read back byte by byte: opened by ROOT right after the copy, the file on EOS (fuse)
        # can still have a stale tail and is seen as truncated (kRecovered) even if it is fine
        if not filecmp.cmp(localMerged, tmpMerged, shallow=False):
            print (" ERROR: copy of the merged file on EOS differs from the local one for "+sampleLabel+", "+mergepath+"/"+sampleLabel+".root left untouched")
            os.remove(tmpMerged)
            return False
        copyChecked = mergeChecked
    except OSError as e:
        print (" ERROR: merge of "+sampleLabel+" failed ("+str(e)+"), "+mergepath+"/"+sampleLabel+".root left untouched")
        if os.path.exists(tmpMerged): os.remove(tmpMerged)
        return False
    finally:
        shutil.rmtree(localFolder, ignore_errors=True)            # the local copies are removed in any case
    if checkOutputFileIsBad(tmpMerged):
        print (" ERROR: copy of the merged file to "+tmpMerged+" is broken, "+mergepath+"/"+sampleLabel+".root left untouched")
        if os.path.exists(tmpMerged): os.remove(tmpMerged)
        return False
    os.replace(tmpMerged, mergepath+"/"+sampleLabel+".root")
    if copyChecked:
        for p in parts:
            os.remove(p)
        print (" "+str(nsplit)+" parts of "+sampleLabel+" removed")
        if not os.listdir(outpath):
            os.rmdir(outpath)
            print (" "+outpath+" empty, removed")
    return True
    
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    print("Please run voms command")
    exit()

pass_fail_jobs={} # job -> "ok", "failed", "idle", "running", "held" or "suspended"
# jobs still in the condor queue are never checked nor (re)submitted
queued = getQueuedJobs() if (mode in ("s", "c", "r") and not dryrun) else None
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
                histoMerge(outFolder_path+"/parts", mergeFolder_path+"/plots", sample.label, nsplit, dryrun, rmparts)
                if not dryrun:
                    time.sleep(3)
                    continue
            if nsplit==1:
                if os.path.normpath(outFolder_path) == os.path.normpath(mergeFolder_path):
                    print (" "+sample.label+" was not split, output already in "+outFolder_path+"/plots/ - nothing to do")
                    continue
                if not dryrun and not os.path.exists(mergeFolder_path+"/plots"):
                    print (" warning, merge path: "+mergeFolder_path+"/plots did not exist at time of copying histos, creating it on the fly.")
                    os.makedirs(mergeFolder_path+"/plots")
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
            jobkey = sample.label + locsuffix # = JobTag in condor.sub
            # same destination as in runner_writer: split jobs in parts/, unsplit ones in plots/
            outfile_path = outFolder_path.rstrip("/") + "/" + ("parts" if postsuffix else "plots") + "/" + sample.label + postsuffix + ".root"
            if queued is not None and jobkey in queued:
                state, clusterid, holdreason = queued[jobkey]
                pass_fail_jobs[jobkey] = state
                if state == "held":
                    print(f" job {jobkey} is held (cluster {clusterid}): {holdreason}")
                elif (mode == "s" or mode == "r" or verb>0):
                    print(f" job {jobkey} already in queue ({state}, cluster {clusterid}): skipped")
                continue
            if (mode == "c" or mode == "r"): hasFailed= checkJobHasFailed(condor_subfolder,sample.label,dat,outfile_path,0,queued is not None)

            pass_fail_jobs[jobkey] = "failed" if hasFailed else "ok"
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
        if(pass_fail_jobs[ss]=="failed"):
            ntorerun+=1
            if(verb>0):print(ss)
    if(verb>0 and "held" in pass_fail_jobs.values()):
        print ("held jobs (not resubmitted): ")
        for ss in pass_fail_jobs:
            if(pass_fail_jobs[ss]=="held"): print(f"{ss} (cluster {queued[ss][1]}): {queued[ss][2]}")
    counts = {st: list(pass_fail_jobs.values()).count(st) for st in ["ok", "failed", "idle", "running", "held", "suspended"]}
    print("  ".join(f"{st}: {n}" for st, n in counts.items()))
    nqueued = counts["idle"] + counts["running"] + counts["held"] + counts["suspended"]
    if nqueued > 0:
        print(f"WARNING: {nqueued} jobs still in queue: run -m c again when the queue is empty")
    if(mode=="c"): print("total to rerun: "+str(ntorerun))
    if(mode=="r"): print("total being rerun: "+str(ntorerun))
