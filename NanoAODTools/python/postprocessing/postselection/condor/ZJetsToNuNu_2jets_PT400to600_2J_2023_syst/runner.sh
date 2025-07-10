#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
cd python/postprocessing/postselection/
python3 postSelector.py -d ZJetsToNuNu_2jets_PT400to600_2J_2023 --dict_samples_file ../samples/dict_samples_2023.json --hist_folder run2023_syst_condor/ --nfiles_max 1000 --syst
