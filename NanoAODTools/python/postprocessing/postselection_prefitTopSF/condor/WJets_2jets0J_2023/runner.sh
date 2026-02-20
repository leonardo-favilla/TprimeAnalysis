#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
cd python/postprocessing/postselection/
python3 postSelector.py -d WJets_2jets0J_2023 --dict_samples_file ../samples/dict_samples_2023.json --hist_folder /eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/ --nfiles_max 10000 --tmpfold
cp /tmp/lfavilla/WJets_2jets0J_2023/WJets_2jets0J_2023.root /eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/.
ls -lthra /eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep/plots/.
