#!/bin/bash

ERA="2023"

for TopCategory in Resolved Mixed Merged; do
  for wp_cat in Loose Tight; do
    for channel in pass fail; do
      BASE_DIR="/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run${ERA}_${TopCategory}_NewWPs_TopPtReweightingTheory"
      OUT_DIR="/eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/run${ERA}_${TopCategory}_NewWPs_TopPtReweightingTheory"

      input_json="${BASE_DIR}/ScaleFactors/TrotaScaleFactors_${ERA}_${TopCategory}.json"
      output="${OUT_DIR}/ScaleFactors/SF_${TopCategory}_${wp_cat}_${channel}"

      echo "Running: TopCategory=${TopCategory}, wp_cat=${wp_cat}, channel=${channel}"

      python3 visualize_ScaleFactors.py \
        "${input_json}" \
        --TopCategory "${TopCategory}" \
        --wp_cat "${wp_cat}" \
        --channel "${channel}" \
        --output "${output}"

    done
  done
done