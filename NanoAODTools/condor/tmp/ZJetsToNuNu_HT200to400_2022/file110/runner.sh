#!/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
mkdir -p /tmp/lfavilla/ZJetsToNuNu_HT200to400_2022/file110/
cd /tmp/lfavilla/ZJetsToNuNu_HT200to400_2022/file110/
pwd
python3 /afs/cern.ch/user/l/lfavilla/TprimeAnalysis/NanoAODTools/condor/tmp//ZJetsToNuNu_HT200to400_2022/file110/crab_script.py
pwd
hadd -f tree_hadd_110.root tree.root hist.root
pwd
davix-put tree_hadd_110.root davs://stwebdav.pi.infn.it:8443/cms/store/user/lfavilla/Run3Analysis_Tprime/ZJetsToNuNu_HT200to400_2022/20250310_160222/tree_hadd_110.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/
