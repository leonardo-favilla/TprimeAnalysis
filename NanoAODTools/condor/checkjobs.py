import subprocess

def get_file_sizes(directory_url, cert_path, ca_path):
    try:
        # Esegui il comando davix-ls per ottenere la lista dei file e le loro dimensioni
        result = subprocess.run([
            'davix-ls', '-l', '-E', cert_path, '--capath', ca_path, directory_url
        ], capture_output=True, text=True, check=True)
        
        # Leggi l'output del comando
        output = result.stdout
        
        # Dichiara un dizionario per contenere i nomi dei file e le loro dimensioni
        file_sizes = {}
        
        # Analizza l'output riga per riga
        for line in output.splitlines():
            # Ignora le righe non relative ai file (come intestazioni o directory)
            if line.endswith('.root') and line:
                parts = line.split()
                # L'ultima parte è il nome del file
                file_name = parts[-1]
                # La quarta parte è la dimensione del file
                file_size = parts[2]
                file_sizes[file_name] = int(file_size)
        
        return file_sizes
    
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'esecuzione di davix-ls: {e}")
        return {}

def find_folder(remote_dir, dataset_label, cert_path, ca_path):
    results = subprocess.run([
        'davix-ls', '-E', cert_path, '--capath', ca_path, "davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/"+remote_dir+"/"+dataset_label+"/"
    ], capture_output=True, text=True, check=True)
    subfold = results.stdout.splitlines()[-1]

    return "davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/"+remote_dir+"/"+dataset_label+"/"+subfold

# # Esempio di utilizzo
# folder = find_folder("Run3Analysis_Tprime", "TprimeToTZ_1800_2022", "/tmp/x509up_u140541", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
# # directory_url = "davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/Run3Analysis_Tprime/DataEGammaC_2022/20240703_092359/"
# # cert_path = "/tmp/x509up_u140541"
# # ca_path = "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
# file_sizes = get_file_sizes(folder, "/tmp/x509up_u140541", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
# for file_name, file_size in file_sizes.items():
#     if file_size <1000:
#         print(f"File: {file_name}, Size: {file_size} bytes")