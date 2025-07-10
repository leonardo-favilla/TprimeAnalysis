#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
cd python/postprocessing/postselection/
python3 postSelector.py -d TprimeToTZ_700_2023postBPix --dict_samples_file ../samples/dict_samples_2023.json --hist_folder run2023postBPix_syst_no_puWeight --nfiles_max 1000 --syst
