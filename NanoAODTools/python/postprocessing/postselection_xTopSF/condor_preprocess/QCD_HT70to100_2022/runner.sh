#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
cd python/postprocessing/postselection_xTopSF/
python3 preprocess_ntuples.py -c QCD_HT70to100_2022 --dict_samples_file ../samples/dict_samples_2022.json --year 2022 --nfiles_max 1 --certpath $1
