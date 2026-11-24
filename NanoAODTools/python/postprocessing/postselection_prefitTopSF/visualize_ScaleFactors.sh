#!/bin/bash
# Plots of the Trota SFs and MC efficiencies (Loose, Tight, XTight) of one era, from postselection/TopSF-corrections/<era>/:
#   fitted/2D/   maps of the fitted SFs and efficiencies, 6 event categories
#   fitted/1D/   SF and efficiency vs pT, the 3 WPs overlaid
#   applied/2D/  maps of the SFs and efficiencies applied in step 2 (correctionlib files)
#   applied/1D/  the same vs pT, the 3 WPs overlaid
# Run from postselection_prefitTopSF/ in the CMSSW environment (cmsstyle)

ERA="2023"
python3 visualize_ScaleFactors.py \
  --era "${ERA}" \
  --input_folder "../postselection/TopSF-corrections/${ERA}"    # output: <TrotaScaleFactor/folder_www/<era>>/ScaleFactors of config.yaml, or --output
