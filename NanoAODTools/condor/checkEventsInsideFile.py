import ROOT
import os
from checkjobs import get_file_sizes, find_folder
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import optparse

usage           = 'python3 job_status.py -d dataset_name'
parser          = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
(opt, args)     = parser.parse_args()
username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"
dataset_to_run  = opt.dat


def key_exists_in_root_file(file_path, key_name):
    f = ROOT.TFile.Open(file_path)
    if not f or f.IsZombie():
        print(f"Error: Cannot open file {file_path}")
        return False

    keys = [key.GetName() for key in f.GetListOfKeys()]
    f.Close()
    return key_name in keys



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


        

for sample in samples:
    print(sample.label)
    remote_folder_name              = "Run3Analysis_Tprime"
    davixfolder                     = find_folder(username, remote_folder_name, sample.label, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    file_sizes                      = get_file_sizes(davixfolder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    print(len(file_sizes))
    for file_name, file_size in file_sizes.items():
        path_file = "root://cms-xrd-global.cern.ch/"+davixfolder.replace("davs://stwebdav.pi.infn.it:8443/cms", "")
        f         = path_file+"/"+file_name
        if not key_exists_in_root_file(f, "Events"):
            print(f"File {f} does not contain 'Events' tree...")