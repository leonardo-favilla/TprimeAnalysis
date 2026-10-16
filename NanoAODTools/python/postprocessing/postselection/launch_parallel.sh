####################################################################################################
#How to use postSelector_submitter_large.py 
# ### ==> Main features: 
# You can split jobs with --partsize X, where it will create jobs running on X root files each  
# There are several working options that you can select with the -m (or --mode) option:  
# -m s --> submits
# -m r --> resubmits failed jobs by looking at the condor output (still perfectible)
# -m c --> checks failed jobs by looking at the condor output
# -m h --> hadd files together after is finished.
# NOTA BENE: there are two paths :
# --mergepath is for MERGED files, i.e. the TRUE FOLDER you will use for plots 
# --outpath is the path for SPLIT files, i.e. you DO NOT have to use it for plots
#
### ==> Sequence of operations:
# first run it with -s, then with -r to resubmit failed jobs (usually after a few minutes the jobs that had to fail will fail
# Both -r and -c options will tell you how many jobs are resubmitted / to resubmit.
# 
# ### ==> Other options:
# you can customize the config with the --config_paths option
# you can just prepare the condor folders with the --dryrun option
# the option --verbose (number) makes it so some extra printouts are shown
# ### ==> Examples:
# Below you find examples (with a semi-optimized partsize selection) for each file. Just be mindful of changing the paths! 
# For simplicity, it's done with bash variables here - make your scripting however you want! 
####################################################################################################

export OPT=r
export OUTPATH="/eos/user/o/oiorio/tDM/FrameworkTestV5/"
export MERGEPATH="/eos/user/o/oiorio/tDM/MergedV5/"
export CONFIGPATH="../config/config.yaml" 

### TTBar
python3 postSelector_submitter_large.py -d TT_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 10 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH --verbose 1


### ZJets
python3 postSelector_submitter_large.py -d ZJetsToNuNu_2jets_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 20 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH 
#
#HT binned - careful incomplete samples at the moment
#3 postSelector_submitter_large.py -d ZJetsToNuNu_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths "../config/config_zj.yaml" --partsize 50 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH 
#
#WJets
python3 postSelector_submitter_large.py -d WJets_2jets_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 20 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH --verbose 1
#
#Single top TW
python3 postSelector_submitter_large.py -d TW_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 25 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH 
#
#QCD
python3 postSelector_submitter_large.py -d QCD_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 20 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH 
#
#
python3 postSelector_submitter_large.py -d DataJetMET_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 20 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH 
#
python3 postSelector_submitter_large.py -d DataEGamma_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 20 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH 
#
python3 postSelector_submitter_large.py -d DataMuon_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_paths $CONFIGPATH --partsize 20 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH
#
#
python3 postSelector_submitter_large.py -d TBDM_s_2024,TBDM_ps_2024,TTDM_s_2024,TTDM_ps_2024,TWDM_s_2024,TWDM_ps_2024 --suffix TestParallelV3 --noSFbtag --noPuWeight --noTrotaSF --noTopPtWeight --config_path $CONFIGPATH --partsize 25 -m $OPT --mergepath $MERGEPATH --outpath $OUTPATH --dict_samples_file "../samples/dict_samples_2024_tdm.json"
#
