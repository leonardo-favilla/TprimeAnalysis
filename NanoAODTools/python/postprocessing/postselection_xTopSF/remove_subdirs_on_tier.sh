#!/bin/bash

# Configurazione certificati
CERT="/tmp/x509up_u159320"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"

# Cartella principale da pulire
BASE_URL="davs://webdav.recas.ba.infn.it:8443/cms/store/user/lfavilla/TopSF/ntuples_ready_for_TopSF_Framework_minimal_latest"

# Lista delle sottocartelle
folders=$(davix-ls --cert "$CERT" --capath "$CAPATH" "$BASE_URL")

for folder in $folders; do
    FULL_PATH="$BASE_URL/$folder"
    echo "Processing folder: $FULL_PATH"

    # Lista dei file nella cartella
    files=$(davix-ls --cert "$CERT" --capath "$CAPATH" "$FULL_PATH")
    
    # Cancella i file
    for f in $files; do
        FILE_PATH="$FULL_PATH/$f"
        echo "Deleting file: $FILE_PATH"
        davix-rm --cert "$CERT" --capath "$CAPATH" "$FILE_PATH"
    done

    # Prova a cancellare la cartella vuota
    echo "Deleting folder: $FULL_PATH"
    davix-rm --cert "$CERT" --capath "$CAPATH" "$FULL_PATH"
done
