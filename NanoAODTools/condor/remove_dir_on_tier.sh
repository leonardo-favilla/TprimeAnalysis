#!/bin/bash

PROXY="/tmp/x509up_u159320"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://stwebdav.pi.infn.it:8443/cms/store/user/lfavilla/Run3Analysis_Tprime/DataJetMETD1_0_2023postBPix/20250429_120346"

# Step 1: List files
files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")

# Step 2: Delete each file
for file in $files; do
    echo "Deleting $BASE/$file"
    davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE/$file"
done

# Step 3: Remove the (now empty) directory
echo "Deleting directory $BASE"
davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE"
