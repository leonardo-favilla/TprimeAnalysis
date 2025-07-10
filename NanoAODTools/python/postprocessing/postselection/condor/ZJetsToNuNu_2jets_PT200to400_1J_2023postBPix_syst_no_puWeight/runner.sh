#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
cd python/postprocessing/postselection/
python3 postSelector.py -d ZJetsToNuNu_2jets_PT200to400_1J_2023postBPix --dict_samples_file ../samples/dict_samples_2023.json --hist_folder run2023postBPix_syst_no_puWeight --nfiles_max 1000 --syst
