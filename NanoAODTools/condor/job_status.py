import os
import optparse
from checkjobs import get_file_sizes, find_folder, summarize_job_status
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import pandas as pd

usage           = 'python3 job_status.py -d dataset_name'
parser          = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
(opt, args)     = parser.parse_args()

dataset_to_run  = opt.dat


#Insert here your uid... you can see it typing echo $uid
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
workdir  = "user" if "user" in os.environ.get('PWD') else "work"
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


if dataset_to_run == '':
    print("Please enter a dataset name")
    exit()
elif dataset_to_run not in sample_dict.keys():
    print("Dataset not found")
    exit()
elif dataset_to_run in sample_dict.keys():
    if hasattr(sample_dict[dataset_to_run], "components"):
        print("---------- Running dataset: ", dataset_to_run)
        # print("Components: ", [s.label for s in sample_dict[dataset_to_run].components])
        samples = sample_dict[dataset_to_run].components
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset_to_run)
        samples = [sample_dict[dataset_to_run]]

running_folder                      = "/afs/cern.ch/"+workdir+"/"+inituser+"/"+username+"/TprimeAnalysis/NanoAODTools/condor/tmp/"
remote_folder_name                  = "Run3Analysis_Tprime"
if not os.path.exists(running_folder):
    os.makedirs(running_folder)


df_summary                          = summarize_job_status(username, uid, samples, running_folder, remote_folder_name)
print(df_summary.to_string(index=False))