# commenti
# funziona il run e scrive sul tier il file di output
# non riesco ad aprire il file sul tier (ma quello in locale è ok) sembra un problema di compatibilità alma9 con tier
# I file in locale vengono scritti comunque

import os
import optparse
import sys
import time
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.get_file_fromdas import *
import tqdm

usage = 'python3 postproc_submitter.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--dryrun', dest='debug', action='store_true', default=False, help='dryrun')
parser.add_option('-w', '--write', dest='write', type=str, default = 'tier', help='Please enter location where to write the output file (eos or tier)')
(opt, args) = parser.parse_args()
debug = opt.debug 
where_to_write = opt.write

#Insert here your uid... you can see it typing echo $uid
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'adeiorio':
    uid = 103214
elif username == 'acagnott':
    uid = 140541
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

# insert here the name of output folder
remote_folder_name = "Run3Analysis_Tprime"

print("Launching crab script for dataset: ", opt.dat)
if where_to_write == 'tier':
    print("Remote folder name (tier): ", remote_folder_name)
    os.popen("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(username, remote_folder_name, str(uid)))
    print("davs://stwebdav.pi.infn.it:8443/cms/store/user/{}/{} created".format(username, remote_folder_name))

elif where_to_write == 'eos':
    print("Remote folder name (eos): ", remote_folder_name)
    if not os.path.exists("/eos/home-l/lfavilla/xAnimo/"+remote_folder_name):
        os.makedirs("/eos/home-l/lfavilla/xAnimo/"+remote_folder_name)
    print("root://eosuser.cern.ch//eos/user/l/lfavilla/xAnimo/{} created".format(remote_folder_name))

def write_crab_script(sample, file, modules, run_folder):

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
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_syst import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_syst import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.lumiMask import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculators_module import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsHelper import *\n")
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
    else:
        year_tag = year
    if isMC:
        f.write("p=PostProcessor('.', ['root://cms-xrd-global.cern.ch/"+file+"'], '', modules=["+modules+"], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/scripts/keep_and_drop.txt')\n")# haddFileName='"+sample.label+".root'
    else: 
        f.write("p=PostProcessor('.', ['root://cms-xrd-global.cern.ch/"+file+"'], '', modules=["+modules+"], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/scripts/keep_and_drop.txt')\n")#
        
    f.write("p.run()\n")
    f.write("print('DONE')\n")
    f.close()

def sub_writer(run_folder, log_folder, label):
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
    f.write("source analysisel9.sh\n")
    f.write("mkdir -p "+outfolder+"\n")
    f.write("cd "+outfolder+"\n")
    f.write("pwd\n")
    f.write("python3 "+folder+"/crab_script.py\n")
    f.write("pwd\n")
    f.write("hadd -f tree_hadd_"+str(i)+".root tree.root hist.root\n")
    f.write("pwd\n")
    if where_to_write == 'eos':
        f.write("mv tree_hadd_{}.root /eos/home-l/lfavilla/xAnimo/{}/{}/{}/.\n".format(str(i), remote_folder_name, sample_folder, launchtime))
    elif where_to_write == 'tier':
        f.write("davix-put tree_hadd_{}.root davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/{}/{}/{}/tree_hadd_{}.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/\n".format(str(i), remote_folder_name, sample_folder, launchtime, str(i)))
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
        print("Running dataset: ", dataset_to_run)
        print("Components: ", sample_dict[dataset_to_run].components)
        samples = sample_dict[dataset_to_run].components
    else:
        print("You are running a single sample")
        print("Running sample: ", dataset_to_run)
        samples = [sample_dict[dataset_to_run]]

running_folder = "/afs/cern.ch/work/a/"+username+"/Analysis/NanoAODTools/condor/tmp/"+dataset_to_run
if not os.path.exists(running_folder):
    os.makedirs(running_folder)



for sample in samples:
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
    launchtime = time.strftime("%Y%m%d_%H%M%S")
    if where_to_write == 'tier':
        os.popen("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(remote_folder_name, sample_folder, str(uid)))
        print("davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/{}/{} created".format(remote_folder_name, sample_folder))
        os.popen("davix-mkdir davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/{}/{}/{}/ -E /tmp/x509up_u{} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/".format(remote_folder_name, sample_folder, launchtime, str(uid)))
        print("davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/{}/{}/{} created".format(remote_folder_name, sample_folder, launchtime))
    elif where_to_write == 'eos':
        if not os.path.exists("/eos/home-l/lfavilla/xAnimo/"+remote_folder_name+"/"+sample_folder):
            os.makedirs("/eos/home-l/lfavilla/xAnimo/"+remote_folder_name+"/"+sample_folder)
        print("root://eosuser.cern.ch//eos/user/l/lfavilla/xAnimo/{}/{} created".format(remote_folder_name, sample_folder))
        if not os.path.exists("/eos/home-l/lfavilla/xAnimo/"+remote_folder_name+"/"+sample_folder+"/"+launchtime):
            os.makedirs("/eos/home-l/lfavilla/xAnimo/"+remote_folder_name+"/"+sample_folder+"/"+launchtime)
        print("root://eosuser.cern.ch//eos/user/l/lfavilla/xAnimo/{}/{}/{} created".format(remote_folder_name, sample_folder, launchtime))

    outfolder_tmp = "/tmp/"+username+"/"
    outfolder_crabscript = outfolder_tmp+sample.label+"/"

    isMC = True
    if "Data" in sample.label: isMC = False

    if isMC:
        if sample.year == 2018:
            modules = "MCweight_writer(), MET_HLT_Filter(), preselection(), SampleIdx("+ str(dictSample[sample.label]) +"), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(),nanoTopcand(isMC=1), globalvar(), nanoTopevaluate_MultiScore(year = "+str(sample.year)+")"
        elif sample.year == 2022:
            modules = "MCweight_writer(),MET_Filter(year = "+str(sample.year)+"),JetVetoMaps_run3(year="+str(sample.year)+",EE="+str(sample.EE)+"),preselection(),PUreweight(year="+str(sample.year)+",EE="+str(sample.EE)+"),BTagSF(year="+str(sample.year)+",EE="+str(sample.EE)+"),CMSJMECalculators(configcreate(isMC=True,year="+str(sample.year)+",EE="+str(sample.EE)+",runPeriod='.',jetType='AK4PFPuppi',forMET=False,doJer=True),jetType='AK4PFPuppi',isMC=True,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=True,year="+str(sample.year)+",EE="+str(sample.EE)+",runPeriod='.',jetType='AK8PFPuppi',forMET=False,doJer=True),jetType='AK8PFPuppi',isMC=True,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=True,year="+str(sample.year)+",EE="+str(sample.EE)+",runPeriod='.',jetType='AK4PFPuppi',forMET=True,doJer=True),jetType='AK4PFPuppi',isMC=True,forMET=True,PuppiMET=True,addHEM2018Issue=False,NanoAODv=12),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(),nanoTopcand(isMC=True),globalvar(), nanoTopevaluate_MultiScore(year = "+str(sample.year)+")" 
    else:
        if sample.year==2018:
            modules = "lumiMask(year = "+str(sample.year)+"), MET_Filter(year = "+str(sample.year)+"), preselection(), SampleIdx("+ str(dictSample[sample.label]) +"), nanoTopcand(isMC=0), globalvar(), nanoTopevaluate_MultiScore(isMC=0, year = "+str(sample.year)+")"
        if sample.year==2022:
            modules = "lumiMask(year = "+str(sample.year)+"),MET_Filter(year = "+str(sample.year)+"),JetVetoMaps_run3(year="+str(sample.year)+",EE="+str(sample.EE)+"),preselection(),CMSJMECalculators(configcreate(isMC=False,year="+str(sample.year)+",EE="+str(sample.EE)+",runPeriod='"+sample.runP+"',jetType='AK4PFPuppi',forMET=False,doJer=True),jetType='AK4PFPuppi',isMC=False,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=False,year="+str(sample.year)+",EE="+str(sample.EE)+",runPeriod='"+sample.runP+"',jetType='AK8PFPuppi',forMET=False,doJer=True),jetType='AK8PFPuppi',isMC=False,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=False,year="+str(sample.year)+",EE="+str(sample.EE)+",runPeriod='"+sample.runP+"',jetType='AK4PFPuppi',forMET=True,doJer=True),jetType='AK4PFPuppi',isMC=False,forMET=True,PuppiMET=True,addHEM2018Issue=False,NanoAODv=12),nanoTopcand(isMC=False),globalvar(), nanoTopevaluate_MultiScore(isMC=0,year = "+str(sample.year)+")" 

    files = get_files_string(sample)

    for i, f in tqdm.tqdm(enumerate(files[:1])):
        outfolder_crabscript_i = outfolder_tmp+sample.label+"/file"+str(i)+"/"
        running_subfolder_file = running_subfolder + "/file" + str(i)
        if not os.path.exists(running_subfolder_file):
            os.makedirs(running_subfolder_file)
        write_crab_script(sample, f, modules, running_subfolder_file)
        runner_writer(running_subfolder_file, i, remote_folder_name, sample_folder, launchtime, outfolder_crabscript_i)
        sub_writer(running_subfolder_file, running_subfolder+"/condor", sample.label+"_file"+str(i))
        if not debug : os.popen("condor_submit " + running_subfolder_file + "/condor.sub")
    print("Submitted ", sample.label)