#!/bin/bash

PROXY="/tmp/x509up_u159320"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
REMOTE_ENTER_PATH="davs://stwebdav.pi.infn.it:8443/cms/store/user/lfavilla/Run3Analysis_Tprime/DataJetMETD1_0_2023postBPix/20250429_120346/tree_hadd_72.root"
LOCAL_PATH="/tmp/tree_hadd_72.root"
REMOTE_OUT_PATH="davs://stwebdav.pi.infn.it:8443/cms/store/user/lfavilla/Run3Analysis_Tprime/DataJetMETD1_0_2023postBPix/20250429_124746/tree_hadd_72.root"

# Check file exists remotely
davix-ls -E "$PROXY" --capath "$CAPATH" "$REMOTE_ENTER_PATH"

# Download to local
davix-get -E "$PROXY" --capath "$CAPATH" "$REMOTE_ENTER_PATH" "$LOCAL_PATH"

# Upload to new remote location
davix-put -E "$PROXY" --capath "$CAPATH" "$LOCAL_PATH" "$REMOTE_OUT_PATH"

# Clean up local file
rm -f "$LOCAL_PATH"