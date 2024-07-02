import pickle as pkl
import os

# folder = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/" % os.environ['CMSSW_BASE']
folder = "/afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/python/postprocessing/data/dict_tresholds/"
#folder = "./data/dict_tresholds/"
with open(folder+"tresholds_LSTM.pkl", "rb") as f:
    trs_lowptLSTM = pkl.load(f)
with open(folder+"tresholds_DNN.pkl", "rb") as f:
    trs_lowptDNN = pkl.load(f)    
#with open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_highpt/tresholds.pkl", "rb") as f:
#    trs_highpt = pkl.load(f)
with open(folder+"tresholds.pkl", "rb") as f:
    trs_highpt_2 = pkl.load(f)
trs_res = trs_lowptDNN['fpr 1']
trs_mix = trs_highpt_2['fpr 10']
trs_mer = 0.99
