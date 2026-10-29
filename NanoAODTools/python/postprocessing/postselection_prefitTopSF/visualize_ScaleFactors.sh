#!/bin/bash

ERA="2023"

for TopCategory in Resolved Mixed Merged; do
  for wp_cat in Loose Tight; do
    for channel in pass fail; do
      OUT_DIR="/eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/SemiLep_prefit/run${ERA}_${TopCategory}_NewWPs"

      input_json="../postselection/TopSF-corrections/${ERA}/TrotaScaleFactors_${ERA}_${TopCategory}.json"
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