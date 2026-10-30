#!/bin/bash
# Pre-fit and post-fit stacks of the Trota SF fits of one era, split by tag category (topmatched, nonmatched, other)
# Inputs: workspace_<wp_cat>/<fit_variable>/ of TrotaScaleFactor.outputfolder in config.yaml (collectHistograms.py + fit_procedure.sh)
# Outputs: <outdir>/stacks_<wp_cat>/<fit_variable>/
# Run from postselection_prefitTopSF/ (ROOT, matplotlib, mplhep)

python3 plot_TopSF_stacks.py --era 2023 --TopCategory Resolved --wp_cat Loose --outdir /eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/2023/Resolved/
python3 plot_TopSF_stacks.py --era 2023 --TopCategory Resolved --wp_cat Tight --outdir /eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/2023/Resolved/
python3 plot_TopSF_stacks.py --era 2023 --TopCategory Mixed    --wp_cat Loose --outdir /eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/2023/Mixed/
python3 plot_TopSF_stacks.py --era 2023 --TopCategory Mixed    --wp_cat Tight --outdir /eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/2023/Mixed/
python3 plot_TopSF_stacks.py --era 2023 --TopCategory Merged   --wp_cat Loose --outdir /eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/2023/Merged/
python3 plot_TopSF_stacks.py --era 2023 --TopCategory Merged   --wp_cat Tight --outdir /eos/user/l/lfavilla/www/RDF_DManalysis/TopSF/results/2023/Merged/
