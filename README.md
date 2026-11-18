# B2G-25-006 Analysis
Analysis code for T'→tZ search, where t→bqq' and Z→νν

## Overview
This repository contains the analysis code for the B2G-25-006 analysis, focusing on the T'→tZ decay channel with hadronic top quark decay and invisible Z boson decay.  
### CMS Internal links:  
[CADI line](https://cms.cern.ch/iCMS/analysisadmin/cadilines?line=B2G-25-006)  
[Analysis Note](https://cmsfence.cern.ch/alcm/note/show-note-details?noteID=CMS%20AN-2024%2F018)  
[PubTalk discussion](https://cms-pub-talk.web.cern.ch/c/b2g/b2g-25-006/828)  
[Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2G25006Review)  

### Most relevant internal talks
- Last VHF update: [1st June 2026](https://indico.cern.ch/event/1687506/#68-update-on-the-trota-scale-f)
- Last B2G update: [14th April 2026](https://indico.cern.ch/event/1671232/#3-analysis-update-b2g-25-006-v)
- [27th October 2025](https://indico.cern.ch/event/1588426/#68-b2g-25-006-status-update-of) 
- [23rd June 2025](https://indico.cern.ch/event/1557401/#66-t-tz-update)
- [30th Sept 2024](https://indico.cern.ch/event/1459687/#66-update-on-t-tz-z-vv)
- [22nd Jan 2024](https://indico.cern.ch/event/1355727/#42-update-on-the-preselection)

## Analysis Workflow
1. **Skimming**: Central NanoAOD skimming + top quark candidate score evaluation with TROTA
2. **Histogram Production**: Using RDataFrame and Vary method
3. **Statistical Analysis**: Using [TprimeStats](https://github.com/acagnotta/TprimeStats)

## Prerequisites
Before running the analysis, make sure you have:
- NanoAOD tools
- Required dependencies installed
- Access to input datasets

## Installation
```bash
# Personal environment setup + JMECalculators lib installation
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_107 x86_64-el9-gcc13-opt
python3 -m venv /afs/cern.ch/user/{u}/{username}/myvenv_lcg107
source /afs/cern.ch/user/{u}/{username}/myvenv_lcg107/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install git+https://gitlab.cern.ch/cms-analysis/general/CMSJMECalculators.git@a6075cbb8022120084e7ee03e63ff20a6e3c3fd1    # 0.4.1.dev33: CMSJMECalculators_module.py does not work with >= 0.4.2 (2 more MET arguments)
python3 -m pip install tf-keras             # [only if needed]
python3 -m pip install "cmsstyle==0.5.0"    # [for plotting]


# Clone the repository
git clone git@github.com:acagnotta/TprimeAnalysis.git

# NanoAOD Tools standalone
cd TprimeAnalysis/NanoAODTools/
bash standalone/env_standalone.sh build
source standalone/env_standalone.sh
```

### Combine environment (top tagging SF fits and statistical analysis)
The fits of the top tagging scale factors and the statistical analysis use combine v11.1.0 and CombineHarvester v4.0.0 in `CMSSW_16_0_0`:
```bash
# once: installation (lxplus el9)
cd /afs/cern.ch/user/{u}/{username}
export SCRAM_ARCH=el9_amd64_gcc13
cmsrel CMSSW_16_0_0
cd CMSSW_16_0_0/src
cmsenv

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit && git checkout v11.1.0 && cd ../..

git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester && git checkout v4.0.0 && cd ..

# physics model of the top tagging SF fits (text2workspace.py -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe)
cp /afs/cern.ch/user/{u}/{username}/TprimeAnalysis/NanoAODTools/python/postprocessing/postselection_prefitTopSF/TagAndProbeExtended.py HiggsAnalysis/CombinedLimit/python/

scramv1 b clean; scramv1 b -j 8
```
`TagAndProbeExtended.py` is the model of [cms-jet/ParticleNetSF](https://github.com/cms-jet/ParticleNetSF/blob/ParticleNet_TopW_SFs_NanoV9/TagAndProbeExtended.py) with one change: the SFs are in the range [0, 10] instead of [0, 2] (`SF_%s[1,0.,10]`), so that SFs and their uncertainties are not cut at 2. Use the copy in this repository, not the original one.

Every time, in a new shell:
```bash
cd /afs/cern.ch/user/{u}/{username}/CMSSW_16_0_0/src
cmsenv
export PYTHONNOUSERSITE=1    # otherwise the packages in ~/.local (e.g. numpy 2) are picked up and text2workspace.py fails with "_ARRAY_API not found"
```

Check:
```bash
combine --help | head -3
python3 -c "import HiggsAnalysis.CombinedLimit.TagAndProbeExtended; print('OK')"
which combineTool.py plotImpacts.py
```

Keep this environment and the NanoAOD Tools standalone one in separate shells: `collectHistograms.py`, `symmetrizeHistos.py` and `makePositiveHistos.py` run in the standalone environment (`PhysicsTools` imports), while the scripts written by `collectHistograms.py` (`combine_script.sh`, `fit_procedure.sh`), `extract_ScaleFactors.py` and `postselection/TopSF-corrections/produceTrotaCorrLib.py` (`correctionlib`) run in `CMSSW_16_0_0`.


## Usage
### Step 0: env setup
```bash
# analysis_TPrime.sh 
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_107 x86_64-el9-gcc13-opt
cd /afs/cern.ch/user/{u}/{username}
source myvenv_lcg107/bin/activate
export TF_USE_LEGACY_KERAS=1
cd /afs/cern.ch/user/{u}/{username}/TprimeAnalysis/NanoAODTools
source standalone/env_standalone.sh
```

### Step 1: Skimming
```bash
cd condor/
python3 postproc_submitter.py -d *dataset_name* --syst (to include jes and jer calc) --s (submit jobs) --r (resubmit failed jobs) --status (running jobs report) --tier bari ("bari" and "pisa" are the only ones supported)
```
When jobs are successfull ended, you need to include the file to the dict_file.json with

```bash
python3 getoutputs.py -d *dataset_name* -o *output_json_file_name*
```

### Step 2: Histograms Production
In order to produce the histograms, you can run the `postSelector_submitter.py` script as follows:
```bash
cd TprimeAnalysis/NanoAODTools/python/postprocessing/postselection/
python3 postSelector_submitter.py -d *dataset_name* --syst
```

#### Split submission and weight sets
`postSelector_submitter_large.py` splits every sample in jobs of `--partsize` files. With `--weightset` (repeatable) one job produces the histograms for several sets of weights: `allWeights`, or the weights to remove separated by commas (`noSFbtag`, `noPuWeight`, `noTopPtWeight`, `noTrotaSF`). The `--noXXX` options remove the weight from every weight set. Without `--weightset` there is one weight set, `allWeights`.
```bash
cd TprimeAnalysis/NanoAODTools/python/postprocessing/postselection/
python3 postSelector_submitter_large.py -d TT_2024 --syst --noTrotaSF --weightset allWeights --weightset noSFbtag --partsize 10 --suffix *suffix* --outpath *outpath*
```
Every weight set has its own folder, named after the removed weights in a fixed order joined by `_` (`allWeights` if none), also when there is only one weight set; e.g. the command above writes in `*outpath*/noTrotaSF/` and `*outpath*/noSFbtag_noTrotaSF/`:
- `<weightset>/parts/<sample>_partN.root`: output of the split jobs;
- `<weightset>/plots/<sample>.root`: merged histograms (and samples not split), the folder to put in `plotting/folder_dict`.

The same options are then used with the other modes (`-m`): `c` checks the jobs, `r` resubmits the failed ones, `h` merges the parts of every weight set into `<weightset>/plots/` (or `--mergepath`), `d` removes the parts after checking them against the merged file.

`postSelector.py --snapshot` (not with `--syst`) saves the preselected events, with the b-tag columns and the weights listed in `branches`, in `<hist_folder>/snapshots/snap_<sample>.root` instead of producing the histograms.

#### config file
The configuration file for the histogram production and plotting can be found at `TprimeAnalysis/NanoAODTools/python/postprocessing/config/config.yaml`.
You can modify this file to select the variables and samples to process, configure the output folders, and choose the plotting and systematic-uncertainty settings. In particular:

- `outputfolder/postselector_results`: folder where the output histograms will be stored for each era;
- `outputfolder/triggerSF_results`: folder where the trigger scale-factor results will be stored for each era;
- `variables_file`: variables definition file used by the histogram-production jobs;
- `dict_samples`: sample dictionary produced at Step 1 and used for each era or era combination;
- `plotting/folder_dict`: folder containing the input histograms used to produce the stacks;
- `plotting/folder_www_dict`: folder where the final plots will be published;
- `plotting/datasets_to_plot`: samples to include in the stacks for each era;
- `plotting/systematics`: systematic uncertainties to include in the stacks. Leave the list empty to draw only statistical uncertainties;
- `plotting/scale_signals`: signal scaling factor (set it to `1` for no scaling);
- `TrotaScaleFactor`: output folders and fit variables of the Trota top tagging scale-factor workflow (see below).

The following template covers all supported Run 3 eras. Fill the empty strings with the appropriate local or EOS folders:

```yaml
outputfolder:
  postselector_results: { 
    "2022":         "",
    "2022EE":       "",
    "2023":         "",
    "2023postBPix": "",
    "2024":         "",
    }
  triggerSF_results: { 
    "2022":         "",
    "2022EE":       "",
    "2023":         "",
    "2023postBPix": "",
    "2024":         "",
    }
  btagEfficiency_results: { 
    "2022":         "",
    "2022EE":       "",
    "2023":         "",
    "2023postBPix": "",
    "2024":         "",
    }

variables_file: "../variables.py"

dict_samples:
  "2022":             "../samples/dict_samples_2022.json"
  "2022EE":           "../samples/dict_samples_2022.json"
  "2023":             "../samples/dict_samples_2023.json"
  "2023postBPix":     "../samples/dict_samples_2023.json"
  "2024":             "../samples/dict_samples_2024.json"
  "Full2022":         "."
  "Full2023":         "."
  "Full2022_Full2023": ["../samples/dict_samples_2022.json", "../samples/dict_samples_2023.json"]

plotting:
  lumi_dict:
    {
      "2022":           7.99,
      "2022EE":         26.68,
      "2023":           17.96,
      "2023postBPix":   9.68,
      "2024":           109.82,
      "2024_C":         7.26,
      "2024_D":         7.98,
      "2024_E":         11.42,
      "2024_F":         28.04,
      "2024_G":         38.07,
      "2024_H":         5.49,
      "2024_I":         11.56,
    }

  folder_dict:
    {
      "2022":               "",
      "2022EE":             "",
      "2023":               "",
      "2023postBPix":       "",
      "2024":               "",
      "Full2022":           "",
      "Full2023":           "",
      "Full2022_Full2023":  "",
    }

  folder_www_dict:
    {
      "2022":               "",
      "2022EE":             "",
      "2023":               "",
      "2023postBPix":       "",
      "2024":               "",
      "Full2022":           "",
      "Full2023":           "",
      "Full2022_Full2023":  "",
    }

  datasets_to_plot:
    {
      "2022":
              [
                  "DataJetMET_2022",
                  "TT_2022",
                  "TW_2022",
                  "QCD_2022",
                  "ZJetsToNuNu_2jets_2022",
                  "WJets_2jets_2022",
                  "TprimeToTZ_700_2022",
                  "TprimeToTZ_1000_2022",
                  "TprimeToTZ_1800_2022"
              ],
      "2022EE":
              [
                  "DataJetMET_2022EE",
                  "TT_2022EE",
                  "TW_2022EE",
                  "QCD_2022EE",
                  "ZJetsToNuNu_2jets_2022EE",
                  "WJets_2jets_2022EE",
                  "TprimeToTZ_700_2022EE",
                  "TprimeToTZ_1000_2022EE",
                  "TprimeToTZ_1800_2022EE"
              ],
      "2023":
              [
                  "DataJetMET_2023",
                  "TT_2023",
                  "TW_2023",
                  "QCD_2023",
                  "ZJetsToNuNu_2jets_2023",
                  "WJets_2jets_2023",
                  "TprimeToTZ_700_2023",
                  "TprimeToTZ_1000_2023",
                  "TprimeToTZ_1800_2023"
              ],
      "2023postBPix":
              [
                  "DataJetMET_2023postBPix",
                  "TT_2023postBPix",
                  "TW_2023postBPix",
                  "QCD_2023postBPix",
                  "ZJetsToNuNu_2jets_2023postBPix",
                  "WJets_2jets_2023postBPix",
                  "TprimeToTZ_700_2023postBPix",
                  "TprimeToTZ_1000_2023postBPix",
                  "TprimeToTZ_1800_2023postBPix"
              ],
      "2024":
              [
                  "DataJetMET_2024",
                  "TT_2024",
                  "TW_2024",
                  "QCD_2024",
                  "ZJetsToNuNu_2jets_2024",
                  "WJets_2jets_2024",
                  "TprimeToTZ_800_2024",
                  "TprimeToTZ_1000_2024",
                  "TprimeToTZ_1800_2024"
              ],
    }
    
  systematics:
    {
      "2022":           [],
      "2022EE":         [],
      "2023":           [],
      "2023postBPix":   [],
      "2024":           [],
    }

  scale_signals: 100

TrotaScaleFactor:
  outputfolder: {
    "Resolved": {
                  "2022":         "",
                  "2022EE":       "",
                  "2023":         "",
                  "2023postBPix": "",
                  "2024":         "",
                },
    "Mixed": {
                  "2022":         "",
                  "2022EE":       "",
                  "2023":         "",
                  "2023postBPix": "",
                  "2024":         "",
                },
    "Merged": {
                  "2022":         "",
                  "2022EE":       "",
                  "2023":         "",
                  "2023postBPix": "",
                  "2024":         "",
                },
    }
    
  fit_variable: {
    "ResolvedLoose":                "MT_W",
    "ResolvedTight":                "MT_W",
    "ResolvedXTight":               "MT_W",
    "MixedLoose":                   "MT_W",
    "MixedTight":                   "MT_W",
    "MixedXTight":                  "MT_W",
    "MergedLoose":                  "MT_W",
    "MergedTight":                  "MT_W",
    "MergedXTight":                 "MT_W",
  }
```
- `outputfolder/btagEfficiency_results`: folder of the b-tag efficiency maps (`BTagEfficiency/`) for each era;
- `TrotaScaleFactor/outputfolder`: folder of the top tagging SF production of each top category and era (prefit histograms in `plots/`, fits in `workspace_<wp_cat>/<fit_variable>/`);
- `TrotaScaleFactor/fit_variable`: variable fitted in each `<TopCategory><wp_cat>` (only Loose, Tight and XTight are fitted, see [Top tagging scale factors](#top-tagging-scale-factors)).

If you want to check if the output files have been correctly produced, i.e. they contain the histograms in the right format, for all component and so on, you can run:
```bash
cd TprimeAnalysis/NanoAODTools/python/postprocessing/postselection/
python3 jobChecker.py -d *plots_folder* --year *era*
```
where *plots_folder* is the folder where all the output histograms are stored and *era* can be something like `2022`, `2022EE`, etc.

### Top tagging scale factors
The Trota top tagging SFs are measured with a tag-and-probe fit in a semileptonic tt̄ region (1 muon), separately for each top category (Resolved, Mixed, Merged), working point (Loose 10%, Tight 5%, XTight 1% mistag, from `postselection/TopTagging_WorkingPoints.json`) and pT bin. The fit variable is `TrotaScaleFactor/fit_variable` of the config file (`MT_W`). Only Loose, Tight and XTight are fitted: the SFs of the tops passing a WP but not the tighter one (LooseButNotTight, TightButNotXTight) are computed in step 2 from the fitted SFs and the MC efficiencies of the same fits.

Environments: the prefit histograms, `collectHistograms.py` and the plots run in the standalone environment of Step 0; the scripts written by `collectHistograms.py`, `extract_ScaleFactors.py` and `produceTrotaCorrLib.py` in `CMSSW_16_0_0` (see [Combine environment](#combine-environment-top-tagging-sf-fits-and-statistical-analysis)). Set `TrotaScaleFactor/outputfolder/<TopCategory>/<era>` in the config file first.

**1. Prefit histograms** (condor, one submission per top category and dataset). The fit needs `DataMuon`, `TT`, `TW`, `QCD`, `ZJetsToNuNu_2jets` and `WJets_2jets`:
```bash
cd TprimeAnalysis/NanoAODTools/python/postprocessing/postselection_prefitTopSF/
for CAT in Resolved Mixed Merged; do
  for DS in TT_2024 TW_2024 QCD_2024 ZJetsToNuNu_2jets_2024 WJets_2jets_2024; do
    python3 postSelector_submitter_large.py -d $DS --TopCategory $CAT --syst --partsize 10 -m s
  done
  python3 postSelector_submitter_large.py -d DataMuon_2024 --TopCategory $CAT --partsize 10 -m s      # Data without --syst: no jes/jer MET variations in the Data files
done
```
Then the same commands with `-m c` (check), `-m r` (resubmit the failed jobs) and `-m h` (merge the parts into `<outputfolder>/plots/`; with `--partsize` every part is normalized to all the files of the sample, so the merge is needed).

**2. Histograms, datacards, fits and SFs**, for each top category and working point:
```bash
# standalone environment, from postselection_prefitTopSF/
python3 collectHistograms.py --era 2024 --TopCategory Mixed --wp_cat Tight --symmetrize jesTotal,jer --positive
# CMSSW_16_0_0 environment
bash -e <outputfolder>/workspace_Tight/MT_W/combine_script.sh      # text2workspace.py
bash <outputfolder>/workspace_Tight/MT_W/fit_procedure.sh          # MultiDimFit, FitDiagnostics, impacts (the impacts are not needed by the next step)
python3 extract_ScaleFactors.py --era 2024 --TopCategory Mixed --wp_cat Tight
```
- `collectHistograms.py` sums the prefit histograms per tag category (topmatched, nonmatched, other) and pT bin, writes `<ev_cat>.root`, the datacards and the combine scripts. `--symmetrize` symmetrizes the jes/jer variations (`symmetrizeHistos.py`), `--positive` fixes the bins <= 0 of the MC histograms (`makePositiveHistos.py`): use both for the fits. `--saveWithUncertainties` adds the postfit uncertainties to FitDiagnostics (postfit band of the stacks, slow).
- `extract_ScaleFactors.py` writes the fitted SFs (pass and fail) and the MC efficiencies (n_pass/n_total from the prefit yields) in `postselection/TopSF-corrections/<era>/TrotaScaleFactors_<era>_<TopCategory>.json` and `TrotaEfficiencies_<era>_<TopCategory>.json`. Event categories without a fit result get 9999.

**3. correctionlib files.** Choose in `postselection/TopSF-corrections/TrotaSF_binning.yaml` the event category used in each pT bin ([0,200], [200,400], [400,600], [600,1000]) of each era, top category and tag category (`null`: SF 1 ± 0), then (CMSSW_16_0_0):
```bash
cd TprimeAnalysis/NanoAODTools/python/postprocessing/postselection/TopSF-corrections/
python3 produceTrotaCorrLib.py --era 2024
```
It writes `2024/CorrLib_TrotaScaleFactors_2024.json` (fitted Loose, Tight and XTight SFs) and `2024/CorrLib_TrotaEfficiencies_2024.json` (efficiencies, -1 in the null bins).

**4. Application in step 2.** Put the two files in `TopSF_CorrLibFilePath_dict` and `TopSF_Eff_CorrLibFilePath_dict` of `postselection/postSelector.py`. `GetTrotaSF` (`postselection.h`) gives every top candidate the SF of its band, from its score: XTight (fitted), TightButNotXTight and LooseButNotTight (`TrotaButNotSF`: `(SF_looserWP·eff_looserWP − SF_tighterWP·eff_tighterWP)/(eff_looserWP − eff_tighterWP)`), 1 below the Loose WP. Only the selected top (`Top_idx`) enters the event weight `TotalTrotaEventWeight`, removed with `--noTrotaSF`; with `--syst` the variations are `TrotaResolved`, `TrotaMixed` and `TrotaMerged`.

**Plots** (standalone environment, from `postselection_prefitTopSF/`):
```bash
python3 plot_TopSF_stacks.py --era 2024 --TopCategory Mixed --wp_cat Tight --outdir *outdir*      # prefit/postfit stacks per tag category
python3 visualize_ScaleFactors.py --era 2024 --output *outdir*      # SF and efficiency plots of Loose/Tight/XTight: fitted/2D, fitted/1D (json of extract_ScaleFactors), applied/2D, applied/1D (correctionlib files)
python3 drawCorrelationMatrix_pois.py -i <outputfolder>/workspace_Tight/MT_W/fitDiagnostics_pt200to400.root -p SF_topmatched,SF_nonmatched -o *outname*
```
`plot_TopSF_stacks.sh` runs the stacks for all the categories of one era; `visualize_ScaleFactors.sh` writes the SF and efficiency plots of one era on EOS.

### Step 3: Statistical Analysis
For the statistical analysis, please refer to the [TprimeStats repository](https://github.com/acagnotta/TprimeStats).
