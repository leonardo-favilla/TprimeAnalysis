import os
import sys
import subprocess


#### User info ####
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
WorkDir  = os.environ["PWD"]


certpath                = "/tmp/x509up_u" + str(uid)
where_to_write          = "tier" # options are "tier" or "eos"
redirector              = "davs://webdav.recas.ba.infn.it:8443/cms"
in_dataset              = "TT_semilep_2022"



if where_to_write == "eos":
    inFolder_path       = f"/eos/user/{inituser}/{username}/RDF_DManalysis/TopSF/ntuples_ready_for_TopSF_Framework/{in_dataset}/"
    outFolder_path      = f"/eos/user/{inituser}/{username}/RDF_DManalysis/TopSF/ntuples_ready_for_TopSF_Framework/{in_dataset}/"
elif where_to_write == "tier":
    inFolder_path       = f"{redirector}/store/user/{username}/TopSF/ntuples_ready_for_TopSF_Framework/{in_dataset}/"
    outFolder_path      = f"{redirector}/store/user/{username}/TopSF/ntuples_ready_for_TopSF_Framework/{in_dataset}/"
scenario                = "nominal"
files_to_hadd           = []




print("Listing all slices...")
if where_to_write == "eos":
    result = subprocess.run([
                                "ls",
                                inFolder_path
                                ],
                                capture_output=True, text=True)
elif where_to_write == "tier":
    result = subprocess.run([
                                "davix-ls",
                                inFolder_path,
                                "-E", certpath,
                                "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
                                ],
                                capture_output=True, text=True)

files_in_inFolder   = result.stdout.splitlines()
remote_files        = [f"{inFolder_path}{f}" for f in files_in_inFolder if scenario in f]
outFilePath_tmp     = "/tmp/"+in_dataset+"_"+scenario+".root"
outFilePath         = f"{outFolder_path}{in_dataset}_{scenario}.root"
print("All files found:", files_in_inFolder)
print("Found slices:", remote_files)
print("Hadding slices...")


if where_to_write == "eos":
    files_to_hadd = remote_files
    print("Hadding files:", files_to_hadd, " to ", outFilePath)
    subprocess.run([
                        "hadd",
                        "-f",
                        outFilePath,
                        *files_to_hadd
                        ])

    result = subprocess.run([
                                "ls",
                                outFilePath
                                ], capture_output=True, text=True)
    print(result.stdout)    
    if scenario in result.stdout:
        print(f"File {outFilePath} successfully created!")
    else:
        print(f"Error: {outFilePath} not found on EOS. Aborting deletion.")
        sys.exit(1)
    
    # print(f"Deleting {scenario} slices from {inFolder_path}")
    # for remote_file in remote_files:
    #     subprocess.run([
    #         "rm",
    #         remote_file
    #     ])

elif where_to_write == "tier":
    for remote_file in remote_files:
        local_file = f"/tmp/{username}/" + remote_file.split("/")[-1]
        print(f"Copying {remote_file} -> {local_file}")
        subprocess.run([
            "davix-get",                            
            "-E", certpath,
            "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/",
            remote_file,
            local_file
        ])
        files_to_hadd.append(local_file)

    print("Hadding files:", files_to_hadd, " to ", outFilePath_tmp)
    subprocess.run([
                        "hadd",
                        "-f",
                        outFilePath_tmp,
                        *files_to_hadd
                    ])

    print(f"Copying {outFilePath_tmp} -> {outFilePath}")
    subprocess.run([
            "davix-put",                            
            "-E", certpath,
            "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/",
            outFilePath_tmp,
            outFilePath
        ])

    result = subprocess.run([
                                "davix-ls",
                                outFilePath,
                                "-E", certpath,
                                "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
                                ], capture_output=True, text=True)
    print(result.stdout)
    if scenario in result.stdout:
        print(f"File {outFilePath} successfully uploaded!")
    else:
        print(f"Error: {outFilePath} not found on remote. Aborting deletion.")
        sys.exit(1)

    # print(f"Deleting {scenario} slices from {inFolder_path}")
    # for remote_file in remote_files:
    #     subprocess.run([
    #         "davix-rm",
    #         "-E", certpath,
    #         "--capath", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/",
    #         remote_file
    #     ])
