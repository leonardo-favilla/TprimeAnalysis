import os
import sys
import time
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')

year                = 2022
components_to_run   = ["QCD_HT70to100_2022", "QCD_HT100to200_2022", "QCD_HT200to400_2022", "QCD_HT400to600_2022", "QCD_HT600to800_2022", "QCD_HT800to1000_2022", "QCD_HT1000to1200_2022", "QCD_HT1200to1500_2022", "QCD_HT1500to2000_2022", "QCD_HT2000_2022", "TT_semilep_2022", "DataJetMETC_2022", "DataJetMETD_2022"]
# components_to_run   = ["TT_semilep_2022"]
# components_to_run   = ["DataJetMETC_2022"]
nfiles_max          = 1
dryrun              = False  # if True, condor jobs are not submitted

username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    print("Please run voms command")
    exit()
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


def sub_writer(run_folder, log_folder, component):
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
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write('+JobTag                 = "'+component+'"\n')
    f.write("executable              = "+run_folder+"runner.sh\n")
    f.write("arguments               = $(Proxy_path)\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+log_folder+"output/preprocess_"+component+".out\n")
    f.write("error                   = "+log_folder+"error/preprocess_"+component+".err\n")
    f.write("log                     = "+log_folder+"log/preprocess_"+component+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(run_folder, component, nfiles_max):
    f = open(run_folder+"runner.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
    f.write("source analysis_TPrime.sh\n")
    f.write("cd python/postprocessing/postselection_xTopSF/\n")
    f.write(f"python3 preprocess_ntuples.py -c {component} --nfiles_max {nfiles_max} --certpath $1"+"\n")



######## LAUNCH CONDOR ########
for component_to_run in components_to_run:
    condor_folder           = "/afs/cern.ch/" + workdir + "/" + inituser + "/" + username + "/TprimeAnalysis/NanoAODTools/python/postprocessing/postselection_xTopSF/condor_preprocess/"
    condor_subfolder        = condor_folder + component_to_run + "/"
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


    run_folder              = condor_subfolder
    if not os.path.exists(run_folder):
        os.makedirs(run_folder)
        print(f"Creating run folder:        {run_folder}")


    runner_writer(run_folder, component_to_run, nfiles_max)
    sub_writer(run_folder, log_folder, component_to_run)
    if not dryrun:
        os.popen("condor_submit " + run_folder + "condor.sub")
    time.sleep(2)