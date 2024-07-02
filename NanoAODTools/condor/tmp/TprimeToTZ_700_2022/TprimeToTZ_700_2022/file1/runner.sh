#!/bin/bash
cd /afs/cern.ch/user/a/acagnott/
source analysisel9.sh
mkdir -p /tmp/acagnott/TprimeToTZ_700_2022/file1/
cd /tmp/acagnott/TprimeToTZ_700_2022/file1/
pwd
python3 /afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/condor/tmp/TprimeToTZ_700_2022/TprimeToTZ_700_2022/file1/crab_script.py
pwd
hadd -f tree_hadd_1.root tree.root hist.root
pwd
davix-put tree_hadd_1.root davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/Run3Analysis_Tprime/TprimeToTZ_700_2022/20240701_181038/tree_hadd_1.root -E $1 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/
