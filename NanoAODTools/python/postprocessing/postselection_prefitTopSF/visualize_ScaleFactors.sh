#!/bin/bash
# 2D maps of the Trota SFs of one era, from postselection/TopSF-corrections/<era>/:
#   fitted/   fitted Loose, Tight and XTight SFs, 6 event categories (TrotaScaleFactors_<era>_<TopCategory>.json)
#   applied/  SFs applied in the analysis, Loose, LooseButNotTight, Tight, TightButNotXTight and XTight, 4 pT bins (CorrLib_TrotaScaleFactors_<era>.json)
# Run from postselection_prefitTopSF/ in the CMSSW environment (cmsstyle)

ERA="2023"
IN_DIR="../postselection/TopSF-corrections/${ERA}"
OUT_DIR="/eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/corrections/${ERA}"
# working points: fitted, and applied in the analysis
FITTED_WPS="Loose Tight XTight"
APPLIED_WPS="Loose LooseButNotTight Tight TightButNotXTight XTight"

for TopCategory in Resolved Mixed Merged; do
  for channel in pass fail; do

    for wp_cat in ${FITTED_WPS}; do
      echo "Running fitted: TopCategory=${TopCategory}, wp_cat=${wp_cat}, channel=${channel}"
      python3 visualize_ScaleFactors.py \
        "${IN_DIR}/TrotaScaleFactors_${ERA}_${TopCategory}.json" \
        --TopCategory "${TopCategory}" \
        --wp_cat "${wp_cat}" \
        --channel "${channel}" \
        --output "${OUT_DIR}/fitted/SF_${TopCategory}_${wp_cat}_${channel}"
    done

    for wp_cat in ${APPLIED_WPS}; do
      echo "Running applied: TopCategory=${TopCategory}, wp_cat=${wp_cat}, channel=${channel}"
      python3 visualize_ScaleFactors.py \
        "${IN_DIR}/CorrLib_TrotaScaleFactors_${ERA}.json" \
        --TopCategory "${TopCategory}" \
        --wp_cat "${wp_cat}" \
        --channel "${channel}" \
        --output "${OUT_DIR}/applied/SF_${TopCategory}_${wp_cat}_${channel}"
    done

  done
done
