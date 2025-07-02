# QCD_2023
# TT_2023
# ZJetsToNuNu_2023
# ZJetsToNuNu_2jets_2023
# WJets_2023
# WJets_2jets_2023
# DataJetMET_2023
# DataMuon_2023
# DataEGamma_2023
# QCD_2023postBPix
# TT_2023postBPix
# ZJetsToNuNu_2023postBPix
# ZJetsToNuNu_2jets_2023postBPix
# WJets_2023postBPix
# WJets_2jets_2023postBPix
# DataJetMET_2023postBPix
# DataMuon_2023postBPix
# DataEGamma_2023postBPix


for dataset in DataJetMET_2023 DataJetMET_2023postBPix DataEGamma_2023 DataEGamma_2023postBPix DataMuon_2023 DataMuon_2023postBPix; do
  python3 getoutputs.py -d "$dataset" --output "dict_samples_2023.json"
done