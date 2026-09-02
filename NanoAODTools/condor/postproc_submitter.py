import os
import optparse
import sys
import time
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.get_file_fromdas import *
from checkjobs import get_file_sizes, find_folder, check_status_submission
from config import models # import machine learning models dictionary from config.py

usage = 'python3 postproc_submitter.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--tier', dest='tier', type=str, default = 'pisa', help='Please enter location where to write the output file (tier pisa or bari)')
parser.add_option('--syst', dest='syst', action='store_true', default=False, help='calculate jerc')
parser.add_option('--dryrun', dest='debug', action='store_true', default=False, help='dryrun')
# parser.add_option('-w', '--write', dest='write', type=str, default = 'tier', help='Please enter location where to write the output file (eos or tier)')
parser.add_option('-s', '--submit', dest='submit', action='store_true', default=False, help='submit jobs')
parser.add_option('-r', '--resubmit', dest='resubmit', action='store_true', default=False, help='resubmit failed jobs')
parser.add_option('--status', dest='status', action='store_true', default=False, help='check jobs status')
parser.add_option('--delete', dest='delete_files', action='store_true', default=False, help='delete files from tier for jobs with davix errors during resubmission')
(opt, args) = parser.parse_args()
debug = opt.debug 
submit = opt.submit
resubmit = opt.resubmit
status = opt.status
calculate_systematics = opt.syst
where_to_write = opt.tier
delete_files = opt.delete_files

if where_to_write.lower() =='pisa':
    redirector = "davs://stwebdav.pi.infn.it:8443/cms"
elif where_to_write.lower() =='bari':
    redirector = "davs://webdav.recas.ba.infn.it:8443/cms"
elif where_to_write.lower() == 'legnaro':
    redirector = "davs://t2-xrdcms.lnl.infn.it:2880/pnfs/lnl.infn.it/data/cms"
else:
    print("Please select a valid tier (pisa or bari) OTHERWISE add the correct redirector in the code")
    exit()

#Insert here your uid... you can see it typing echo $uid
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
workdir  = "user" if "user" in os.environ.get('PWD') else "work"
name_main_folder = "TprimeAnalysis" if "TprimeAnalysis" in os.environ.get('PWD') else "Analysis"

if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


# insert here the name of output folder
remote_folder_name = "Run3Analysis_Tprime"

print("\033[92m\n\n######################## POSTPROC SUBMITTER ########################\033[0m")
print("Launching crab script for dataset: ", opt.dat)

if submit:
    print("\nRemote folder name (tier): ", remote_folder_name)
    if not debug: os.popen("davix-mkdir {}/store/user/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, remote_folder_name, str(uid)))
    print("          {}/store/user/{}/{} CREATED".format(redirector, username, remote_folder_name))

def write_crab_script(sample, file, modules, run_folder, calculate_systematics, year, debug):
    f = open(run_folder+"/crab_script.py", "w")
    f.write("#!/usr/bin/env python3\n")
    f.write("import os\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.JetVetoMaps_run3 import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.JetVetoMaps_run3 import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.BTagSF import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.PUreweight import *\n") 
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *\n")
    if year in [2022,2023,2024] and calculate_systematics:
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_syst import *\n")
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_syst import *\n")
    else:
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *\n")
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *\n")

    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.lumiMask import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculators_module import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsHelper import *\n")
    if year in [2024]:
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetId import *\n")
    f.write("from CMSJMECalculators import loadJMESystematicsCalculators\n")
    f.write("from CMSJMECalculators.utils import (\n")
    f.write("    toRVecFloat,\n")
    f.write("    toRVecInt,\n")
    f.write("    getJetMETArgs,\n")
    f.write("    getFatJetArgs,\n")
    f.write(")\n")
    f.write("from CMSJMECalculators import config as calcConfigs\n")
    f.write("loadJMESystematicsCalculators()\n")

    year = str(sample.year)
    if sample.year==2022:
        if "EE" in sample.label:
            year_tag = "\""+year+"EE\""
        else:
            year_tag = "\""+year+"\""
    elif sample.year==2023:
        if "postBPix" in sample.label:
            year_tag = "\""+year+"postBPix\""
        else:
            year_tag = "\""+year+"\""
    else:
        year_tag = year
    
    if debug:
        extra_str=", maxEntries=100"
    else:
        extra_str=""
    if isMC:
        f.write(f"p=PostProcessor('.', ['root://cms-xrd-global.cern.ch/{file}'], '', modules=[{modules}], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/{workdir}/{inituser}/{username}/{name_main_folder}/NanoAODTools/scripts/keep_and_drop.txt'{extra_str})\n")# haddFileName='"+sample.label+".root'

    else:
        f.write(f"p=PostProcessor('.', ['root://cms-xrd-global.cern.ch/{file}'], '', modules=[{modules}], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/{workdir}/{inituser}/{username}/{name_main_folder}/NanoAODTools/scripts/keep_and_drop.txt'{extra_str})\n")#

    f.write("p.run()\n")
    f.write("print('DONE')\n")
    f.close()

def sub_writer(run_folder, log_folder, label, sample_label):
    f = open(run_folder+"/condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    # f.write("should_transfer_files   = YES\n")
    # f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write('+JobTag                 = "'+label+'"\n')
    f.write("executable              = "+run_folder+"/runner.sh\n")
    f.write("arguments               = $(Proxy_path)\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = "+log_folder+"/output/"+ label+".out\n")
    f.write("error                   = "+log_folder+"/error/"+ label+".err\n")
    f.write("log                     = "+log_folder+"/log/"+ label+".log\n")
    f.write("queue\n")
    f.close()

def runner_writer(folder, i, remote_folder_name, sample_folder, launchtime, outfolder):
    f = open(folder+"/runner.sh", "w")
    f.write("#!/bin/bash\n")
    f.write("cd /afs/cern.ch/user/" + inituser + "/" + username + "/\n")
    f.write("source analysis_TPrime.sh\n")
    f.write("mkdir -p "+outfolder+"\n")
    f.write("cd "+outfolder+"\n")
    f.write("pwd\n")
    f.write("python3 "+folder+"/crab_script.py\n")
    f.write("pwd\n")
    f.write("hadd -f tree_hadd_"+str(i)+".root tree.root hist.root\n")
    f.write("pwd\n")
    f.write("davix-put tree_hadd_{}.root {}/store/user/{}/{}/{}/{}/tree_hadd_{}.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/\n".format(str(i), redirector, username, remote_folder_name, sample_folder, launchtime, str(i)))
    f.close()

dataset_to_run = opt.dat

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

running_folder = os.environ.get('PWD')+"/tmp/"
if not os.path.exists(running_folder):
    os.makedirs(running_folder)


if submit:
    print("\n################################################ SUBMITTING mode")
    launchtime = time.strftime("%Y%m%d_%H%M%S") #"20240704_122343" ho sottomesso diversi job con lo stesso launchtime
    for sample in samples:
        if sample.year in [2018,2022,2023]:
            nanoaod_version = 12
        elif sample.year in [2024]:
            nanoaod_version = 15

        running_subfolder = running_folder + "/" + sample.label
        if not os.path.exists(running_subfolder):
            os.makedirs(running_subfolder)
        if not os.path.exists(running_subfolder+"/condor/output"):
            os.makedirs(running_subfolder+"/condor/output")
        if not os.path.exists(running_subfolder+"/condor/error"):
            os.makedirs(running_subfolder+"/condor/error")
        if not os.path.exists(running_subfolder+"/condor/log"):
            os.makedirs(running_subfolder+"/condor/log")

        sample_folder = sample.label
        if not debug: 
            command1 = os.popen("davix-mkdir {}/store/user/{}/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, remote_folder_name, sample_folder, str(uid)))
            res1 = command1.read()
            if "Error:" in res1:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CREATE THIS FOLDER MANUALLY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") 
                print("Folder : {}/store/user/{}/{}/{}/   NOT CREATED".format(redirector, username, remote_folder_name, sample_folder))
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") 
            else:
                print("Folder : {}/store/user/{}/{}/{}/ created".format(redirector, username, remote_folder_name, sample_folder))
            command2 = os.popen("davix-mkdir {}/store/user/{}/{}/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(redirector, username, remote_folder_name, sample_folder, launchtime, str(uid)))
            res2 = command2.read()
            if "Error:" in res2:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CREATE THIS FOLDER MANUALLY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") 
                print("Folder : {}/store/user/{}/{}/{}/{}   NOT CREATED".format(redirector, username, remote_folder_name, sample_folder, launchtime))
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("Folder : {}/store/user/{}/{}/{}/{} created".format(redirector, username, remote_folder_name, sample_folder, launchtime))

        outfolder_tmp = "/tmp/"+username+"/"
        outfolder_crabscript = outfolder_tmp+sample.label+"/"

        if "Data" in sample.label:
            isMC = False
        else:
            isMC = True

        modelMix_path = models["TopMixed_"+str(sample.year)]
        modelRes_path = models["TopResolved_"+str(sample.year)]
        if isMC:
            if sample.year == 2018:
                modules = "MCweight_writer(), MET_Filter(year = "+str(sample.year)+"), preselection(), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(),nanoTopcand(isMC=1), globalvar(), nanoTopevaluate_MultiScore(year = "+str(sample.year)+", modelMix_path='"+modelMix_path+"', modelRes_path='"+modelRes_path+"')"
            elif sample.year in [2022,2023,2024]:
                modules_list = []

                modules_list.append(f'MCweight_writer()')
                modules_list.append(f'MET_Filter(year={sample.year})')
                if sample.year in [2024]:
                    modules_list.append(f'jetId(year={sample.year},EE={sample.EE})')
                modules_list.append(f'JetVetoMaps_run3(year={sample.year},EE={sample.EE})')
                modules_list.append(f'preselection()')
                modules_list.append(f'PUreweight(year={sample.year},EE={sample.EE})')
                if sample.year not in [2024]:
                    modules_list.append(f'BTagSF(year={sample.year},EE={sample.EE})')
                if calculate_systematics:
                    modules_list.append(f'CMSJMECalculators(configcreate(isMC={isMC},year={sample.year},EE={sample.EE},runPeriod=".",jetType="AK4PFPuppi",forMET=False,doJer=True),jetType="AK4PFPuppi",isMC={isMC},forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv={nanoaod_version})')
                    modules_list.append(f'CMSJMECalculators(configcreate(isMC={isMC},year={sample.year},EE={sample.EE},runPeriod=".",jetType="AK8PFPuppi",forMET=False,doJer=True),jetType="AK8PFPuppi",isMC={isMC},forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv={nanoaod_version})')
                    modules_list.append(f'CMSJMECalculators(configcreate(isMC={isMC},year={sample.year},EE={sample.EE},runPeriod=".",jetType="AK4PFPuppi",forMET=True,doJer=True),jetType="AK4PFPuppi",isMC={isMC},forMET=True,PuppiMET=True,addHEM2018Issue=False,NanoAODv={nanoaod_version})')
                modules_list.append(f'GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24")')
                modules_list.append(f'nanoprepro()')
                modules_list.append(f'nanoTopcand(isMC={isMC})')
                modules_list.append(f'globalvar()')
                modules_list.append(f'nanoTopevaluate_MultiScore(year={sample.year},modelMix_path="{modelMix_path}",modelRes_path="{modelRes_path}")')

        else:
            if sample.year==2018:
                modules = "lumiMask(year = "+str(sample.year)+"), MET_Filter(year = "+str(sample.year)+"), preselection(), nanoTopcand(isMC=0), globalvar(), nanoTopevaluate_MultiScore(isMC=0, year = "+str(sample.year)+", modelMix_path='"+modelMix_path+"', modelRes_path='"+modelRes_path+"')"
            elif sample.year in [2022,2023,2024]:
                modules_list = []

                modules_list.append(f'lumiMask(year={sample.year})')
                if sample.year in [2024]:
                    modules_list.append(f'jetId(year={sample.year},EE={sample.EE})')
                modules_list.append(f'MET_Filter(year={sample.year})')
                modules_list.append(f'JetVetoMaps_run3(year={sample.year},EE={sample.EE})')
                modules_list.append(f'preselection()')
                if calculate_systematics:
                    modules_list.append(f'CMSJMECalculators(configcreate(isMC={isMC},year={sample.year},EE={sample.EE},runPeriod="{sample.runP}",jetType="AK4PFPuppi",forMET=False,doJer=True),jetType="AK4PFPuppi",isMC={isMC},forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv={nanoaod_version})')
                    modules_list.append(f'CMSJMECalculators(configcreate(isMC={isMC},year={sample.year},EE={sample.EE},runPeriod="{sample.runP}",jetType="AK8PFPuppi",forMET=False,doJer=True),jetType="AK8PFPuppi",isMC={isMC},forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv={nanoaod_version})')
                    modules_list.append(f'CMSJMECalculators(configcreate(isMC={isMC},year={sample.year},EE={sample.EE},runPeriod="{sample.runP}",jetType="AK4PFPuppi",forMET=True,doJer=True),jetType="AK4PFPuppi",isMC={isMC},forMET=True,PuppiMET=True,addHEM2018Issue=False,NanoAODv={nanoaod_version})')
                modules_list.append(f'nanoTopcand(isMC={isMC})')
                modules_list.append(f'globalvar()')
                modules_list.append(f'nanoTopevaluate_MultiScore(isMC={isMC},year={sample.year},modelMix_path="{modelMix_path}",modelRes_path="{modelRes_path}")')

        if sample.year in [2022,2023,2024]:
            modules = ", ".join(modules_list)
        files = get_files_string(sample)
        if debug: files = files[:1] 
        print(len(files))

        for i, f in enumerate(files):
            print("....submitting file", i, end='\r')
            outfolder_crabscript_i = outfolder_tmp+sample.label+"/file"+str(i)+"/"
            running_subfolder_file = running_subfolder + "/file" + str(i)
            if not os.path.exists(running_subfolder_file):
                os.makedirs(running_subfolder_file)
            write_crab_script(sample, f, modules, running_subfolder_file, calculate_systematics, sample.year, debug)
            runner_writer(running_subfolder_file, i, remote_folder_name, sample_folder, launchtime, outfolder_crabscript_i)
            sub_writer(running_subfolder_file, running_subfolder+"/condor", sample.label+"_file"+str(i), sample.label)
            if not debug :
                out = os.popen("condor_submit " + running_subfolder_file + "/condor.sub")
                with open(running_subfolder+"/jobsId.txt", "a") as file:
                    file.write("\n file "+str(i)+"\n"+ out.read())
        print("##########################################################################")
        print("\033[92mSUBMITTED\033[0m", sample.label)
        print("##########################################################################\n")


if status: 
    print("\n################################################ STATUS mode")
    
    for sample in samples:
        print(f"Sample: {sample.label}")
        listoffile = os.listdir(running_folder+"/"+sample.label)
        jobs_total = 0 
        for f in listoffile: 
            if f.startswith("file"):
                n = int(f.split("file")[-1])
                if n>jobs_total: jobs_total = n
        jobs_total += 1
        print(f"Total number of jobs:               {jobs_total}")
        check_status_submission(sample.label,username, uid, remote_folder_name, redirector,jobs_total, resubmit = False)
        files = get_files_string(sample)
        # print(len(files))
        if len(files)!=jobs_total:
            print("\n############## ATTENTION NOT ALL JOB SUBMITTED!")

if resubmit:
    print("\n################################################ RESUBMIT mode")
    
    for sample in samples:
        print(f"Sample: {sample.label}")
        listoffile = os.listdir(running_folder+"/"+sample.label)
        jobs_total = 0 
        for f in listoffile: 
            if f.startswith("file"):
                n = int(f.split("file")[-1])
                if n>jobs_total: jobs_total = n
        jobs_total += 1
        print(f"Total number of jobs:               {jobs_total}")
        check_status_submission(sample.label,username, uid, remote_folder_name, redirector,jobs_total, resubmit = True)
