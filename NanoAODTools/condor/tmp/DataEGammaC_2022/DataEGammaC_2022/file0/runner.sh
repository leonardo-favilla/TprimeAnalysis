#!/bin/bash
cd /afs/cern.ch/user/a/acagnott/
source analysisel9.sh
mkdir -p /tmp/acagnott/DataEGammaC_2022/file0/
cd /tmp/acagnott/DataEGammaC_2022/file0/
pwd
python3 /afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/condor/tmp/DataEGammaC_2022/DataEGammaC_2022/file0/crab_script.py
pwd
hadd -f tree_hadd_0.root tree.root hist.root
pwd
davix-put tree_hadd_0.root davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/Run3Analysis_Tprime/DataEGammaC_2022/20240702_101858/tree_hadd_0.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/
