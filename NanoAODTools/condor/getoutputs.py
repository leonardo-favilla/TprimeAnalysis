# to run from lxplus8
import ROOT, os
from checkjobs import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import optparse
import json
from tqdm import tqdm

usage = 'python3 postproc_submitter.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('-o', '--output', dest='output', type=str, default = 'dict_samples_2022.json', help='Please enter a json output file')
(opt, args) = parser.parse_args()

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

def find_folder_8(folder, sample, cert_path, ca_path):
    command = "davix-ls -E "+cert_path+" --capath "+ca_path+" davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/"+folder+"/"+sample+"/"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    subfold = output.decode('utf-8').splitlines()
    subfold.sort()

    return "davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/"+folder+"/"+sample+"/"+subfold[-1]

def get_file_sizes_8(directory_url, cert_path, ca_path):
    command = "davix-ls -l -E "+cert_path+" --capath "+ca_path+" "+directory_url
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = result.communicate()
    output = output.decode('utf-8').splitlines()
    
    file_sizes = {}
    
    for line in output:
        if line.endswith('.root') and line:
            parts = line.split()
            file_name = parts[-1]
            file_size = parts[2]
            file_sizes[file_name] = int(file_size)
    
    return file_sizes
    
def get_files_on_tier(folder, cert_path, ca_path):
    try:
        command = "davix-ls -E "+cert_path+" --capath "+ca_path+" "+folder
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        output, error = process.communicate()
        output = output.decode('utf-8')

        files = []
        for line in output.splitlines():
            # Ignora le righe non relative ai file (come intestazioni o directory)
            if line.endswith('.root') and line:
                file_name = line
                files.append(file_name)
        
        return files
    
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'esecuzione di davix-ls: {e}")
        return {}


dataset = opt.dat 

if dataset == '':
    print("Please enter a dataset name")
    exit()
elif dataset not in sample_dict.keys():
    print("Dataset not found")
    exit()
elif dataset in sample_dict.keys():
    if hasattr(sample_dict[dataset], "components"):
        print("---------- Running dataset: ", dataset)
        print("Components: ", [s.label for s in sample_dict[dataset].components])
        samples = sample_dict[dataset].components
    else:
        print("You are running a single sample")
        print("---------- Running sample: ", dataset)
        samples = [sample_dict[dataset]]

out_dict = {}
out_dict[dataset] = {}

if 'lxplus9' in os.environ['HOSTNAME']:
    print("ERROR: Please run this script from lxplus8")
    exit()


for sample in samples:
    print("---------- Running dataset: ", dataset)
    out_dict[dataset][sample.label] = {}
    if dataset!=sample.label: 
        out_dict[sample.label] = {}
        out_dict[sample.label][sample.label] = {}
    print("---------- Running sample: ", sample.label)
    folder = find_folder_8(remote_folder_name, sample.label, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    print("Folder: ", folder)
    
    files_strings = get_files_on_tier(folder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    file_sizes = get_file_sizes_8(folder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    files_strings = []
    for file_name, file_size in file_sizes.items():
        if file_size <1000:
            print(f"Excluding File: {file_name}, Size: {file_size} bytes")
        else:
            files_strings.append(file_name)
    path_file = "root://cms-xrd-global.cern.ch/"+folder.replace("davs://stwebdav.pi.infn.it:8443/cms", "")
    ntot = []
    out_strings = []
    for f in tqdm(files_strings): 
        f = path_file+"/"+f
        out_strings.append(f)
        if not "Data" in sample.label:
            rootfile = ROOT.TFile.Open(f)
            histo = rootfile.Get("plots/h_genweight")
            ntot.append(histo.GetBinContent(1))
        else:
            ntot.append(None)
    out_dict[dataset][sample.label] = {'strings': out_strings, "ntot": ntot}
    if dataset!=sample.label: out_dict[sample.label][sample.label] = {'strings': out_strings, "ntot": ntot}
# print(out_dict)
# 

outjson = opt.output

if os.path.exists('../python/postprocessing/samples/'+outjson):
    with open('../python/postprocessing/samples/'+outjson, 'r') as json_input:
        json_out = json.load(json_input)
else:
    json_out = {}
json_out[dataset] = out_dict[dataset]
if dataset != sample.label: 
    for sample in samples:
        json_out[sample.label] = out_dict[sample.label]

with open('../python/postprocessing/samples/'+outjson, 'w') as json_output:
    json.dump(json_out, json_output, indent = 2)