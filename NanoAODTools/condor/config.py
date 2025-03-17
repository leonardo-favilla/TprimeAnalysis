import os

username        = str(os.environ.get("USER"))
inituser        = str(os.environ.get("USER")[0])
uid             = os.getuid()





######## machine learning models ########
path_to_model_folder        = "/afs/cern.ch/user/" + inituser + "/" + username + "/TprimeAnalysis/NanoAODTools/python/postprocessing/data/dict_tresholds/"
folder_model_antimo         = "/afs/cern.ch/user/" + inituser + "/" + username + "/TprimeAnalysis/NanoAODTools/python/postprocessing/data/dict_tresholds/"

TopMixed2023                = "model_TopMixed_2022_p2.h5"
TopMixed2022                = "model_TopMixed_2022_p2.h5"
TopMixed2018                = "model_base2.h5"
TopResolved2023             = "model_TopResolved_2022.h5"
TopResolved2022             = "model_TopResolved_2022.h5"
TopResolved2018             = "DNN_phase1_test_lowpt_DNN.h5"

models                      = {}

models["TopMixed_2018"]     = path_to_model_folder+TopMixed2018
models["TopMixed_2022"]     = path_to_model_folder+TopMixed2022
models["TopMixed_2023"]     = path_to_model_folder+TopMixed2023


models["TopResolved_2018"]  = path_to_model_folder+TopResolved2018
models["TopResolved_2022"]  = path_to_model_folder+TopResolved2022
models["TopResolved_2023"]  = path_to_model_folder+TopResolved2023
