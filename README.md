# B2G-25-006 Analysis
Analysis code for T'→tZ search, where t→bqq' and Z→νν

## Overview
This repository contains the analysis code for the B2G-25-006 analysis, focusing on the T'→tZ decay channel with hadronic top quark decay and invisible Z boson decay.

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
# Personal environment setup + JMECalcilators lib installation
source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
python -m venv myvenv
source myvenv/bin/activate
pip install git+https://gitlab.cern.ch/cms-analysis/general/CMSJMECalculators.git

# Clone the repository
git clone git@github.com:acagnotta/TprimeAnalysis.git
cd TprimeAnalysis

# NanoAOD Tools standalone
cd ..../TprimeAnalysis/NanoAODTools/
bash standalone/env_standalone.sh build
source standalone/env_standalone.sh
```


## Usage
### Step 0: env setup
```bash
# analysis_TPrime.sh 
source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
cd ..../TprimeAnalysis/
source myvenv/bin/activate
cd ..../TprimeAnalysis//NanoAODTools/
source standalone/env_standalone.sh
```

### Step 1: Skimming
```bash
cd condor/
python3 postproc_submitter.py -d *dataset_name* --syst (to include jes and jer calc) --s (submit jobs) --r (resubmit failed jobs) --status (running jobs report)
```
When jobs are successfull ended, you need to include the file to the dict_file.json with

```bash
python3 getoutputs -d *dataset_name*
```
### Step 2: Histogram Production
```bash
cd ..../TprimeAnalysis//NanoAODTools/python/postprocessing/postselection/
python3 postSelector_submitter.py -d *dataset_name* --syst
```

### Step 3: Statistical Analysis
For the statistical analysis, please refer to the [TprimeStats repository](https://github.com/acagnotta/TprimeStats).
