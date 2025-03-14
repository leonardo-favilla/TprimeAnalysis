#!/bin/bash
cd /afs/cern.ch/user/l/lfavilla/
source analysis_TPrime.sh
mkdir -p /tmp/lfavilla/TT_hadr_2022/file0/
cd /tmp/lfavilla/TT_hadr_2022/file0/
pwd
python3 /afs/cern.ch/user/l/lfavilla/TprimeAnalysis/NanoAODTools/condor/tmp//TT_hadr_2022/file0/crab_script.py
pwd
hadd -f tree_hadd_0.root tree.root hist.root
pwd
davix-put tree_hadd_0.root davs://stwebdav.pi.infn.it:8443/cms/store/user/lfavilla/Run3Analysis_Tprime/TT_hadr_2022/20250226_113431/tree_hadd_0.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/
