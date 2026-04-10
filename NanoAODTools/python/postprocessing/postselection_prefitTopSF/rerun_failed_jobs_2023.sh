#!/bin/bash

python3 postSelector_submitter.py -d TT_semilep_2023 --syst --dryrun
condor_submit ./condor_syst/TT_semilep_2023_syst/condor.sub
echo resubmitting job for TT_semilep_2023_syst

python3 postSelector_submitter.py -d TT_hadr_2023 --syst --dryrun
condor_submit ./condor_syst/TT_hadr_2023_syst/condor.sub
echo resubmitting job for TT_hadr_2023_syst

python3 postSelector_submitter.py -d ZJetsToNuNu_2jets_PT40to100_2J_2023 --syst --dryrun
condor_submit ./condor_syst/ZJetsToNuNu_2jets_PT40to100_2J_2023_syst/condor.sub
echo resubmitting job for ZJetsToNuNu_2jets_PT40to100_2J_2023_syst

