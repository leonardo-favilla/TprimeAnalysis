#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
cd python/postprocessing/postselection/
python3 postSelector.py -d QCD_HT2000_2023 --dict_samples_file ../samples/dict_samples_2023.json --hist_folder run2023_syst_no_SFbtag --nfiles_max 1000 --syst
