import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

def get_files_string(dataset):
    username = str(os.environ.get('USER'))
    inituser = str(os.environ.get('USER')[0])
    uid      = int(os.getuid())
    if not hasattr(dataset, "dataset"): 
        return "ERROR: a sample with dataset method is required"
    else:
        if not os.path.exists("/tmp/x509up_u" + str(uid)):
            os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
            os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")
            
        os.popen("export XRD_NETWORKSTACK=IPv4")
        command = 'dasgoclient -query="file dataset='+dataset.dataset#+'"'
        if ("Zprime" in dataset.label) or ("tDM" in dataset.label) or ("Tprime" in dataset.label) or ("TprimeToTZ" in dataset.label): 
            command += ' instance=prod/phys03"'
            print(command)
        else:
            command += '"'
        out_stream = os.popen(command)
        files_string = out_stream.read()
        out_stream.close()
        return files_string.split('\n')[:-1]