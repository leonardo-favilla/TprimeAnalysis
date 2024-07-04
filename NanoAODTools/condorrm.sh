#!/bin/bash

# Definisci l'intervallo di numeri
start=6871402
end=6872085

# Itera attraverso l'intervallo e lancia i comandi
for num in $(seq $start $end); do
    job_id="${num}.0"
    echo "Eseguendo condor_rm per job_id $job_id"
    condor_rm $job_id
    if [ $? -eq 0 ]; then
        echo "Comando eseguito con successo per job_id $job_id"
    else
        echo "Errore nell'esecuzione di condor_rm per job_id $job_id"
    fi
done
