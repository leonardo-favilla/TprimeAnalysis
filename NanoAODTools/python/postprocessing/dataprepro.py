import uproot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import awkward as ak
import vector
import mplhep as hep
import sys
import random
from math import sqrt
plt.style.use(hep.style.CMS)

folder_fileinput = "/eos/home-a/acagnott/DarkMatter/prepro/"
#fileinput = "tDM_mPhi500_mChi1_Skim.root"

folderoutput = "/eos/home-a/acagnott/DarkMatter/prepro/datanp/"
#"/afs/cern.ch/user/a/acagnott/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/python/postprocessing/macro_training_DNN/datanp/"

if not os.path.exists(folderoutput):
  os.mkdir(folderoutput)
  print(folderoutput+" has been created")

samples_signal = ['tDM_mPhi50_mChi1_Skim.root', 'tDM_mPhi500_mChi1_Skim.root', 'tDM_mPhi1000_mChi1_Skim.root']

samples_bkg = ['QCD_HT1000.root', 'QCD_HT1500.root']
'''
for fileinput in samples_signal :

  tree = uproot.open(folder_fileinput+fileinput+":Events")

  fname= fileinput
  if 'Skim' in fileinput:
    fname = fname.replace("_Skim","")
  fname = fname.replace(".root","")

  branches = tree.arrays(['Jet_matched','FatJet_matched'])
  Nevents = len(branches)
  print(Nevents)

  mask_top_had = ak.sum(branches['Jet_matched'], axis=1) +ak.sum(branches['FatJet_matched'], axis=1)
  mask_top_had = mask_top_had >2
  print(np.sum(mask_top_had))
  njets = tree['nJet'].array()
  print(len(njets))

  jet_nmatch = tree['Jet_matched'].array()
  njets_match = ak.sum(jet_nmatch>0, axis=1)
  print(len(njets_match))
  njets_bkg = np.array(njets)-np.array(njets_match)
  mask_bkg = njets_bkg>0
  print(len(mask_bkg))

  # jets matched
  list_jet_var = ['Jet_area', 'Jet_btagDeepFlavB', 'Jet_eta', 'Jet_mass',
                  'Jet_phi', 'Jet_pt']

  branches_jet_match = tree.arrays(list_jet_var, 'Jet_matched>0', library='pd')
  branches_jet_notmatch = tree.arrays(list_jet_var, 'Jet_matched==0', library='pd')
  event_tojump1000 = 16128
  event_tojump500 = 1611

  sgn_jet_dataset_list = []
  for i in range(Nevents):
    if '1000' in fname and i== event_tojump1000:
      continue
    if '500' in fname and i== event_tojump500:
      continue
    if mask_top_had[i]:
      np_obj = branches_jet_match.loc[(i, slice(None))].to_numpy()
      np_obj_pad = np.pad(np_obj , ((0,3-np_obj.shape[0]),(0,0)))
      sgn_jet_dataset_list.append(np_obj_pad)
    sgn_jet_data = np.array(sgn_jet_dataset_list)

  print(sgn_jet_data.shape)

  bkg_jet_dataset_list = []
  for i in range(Nevents):
    if '1000' in fname and i== event_tojump1000:
      continue
    if '500' in fname and i== event_tojump500:
      continue
    if mask_bkg[i]:
      np_obj = branches_jet_notmatch.loc[(i, slice(None))].to_numpy()  
      shape0 = np_obj.shape[0]
      if shape0<4:
        np_obj_pad = np.pad(np_obj , ((0,3-shape0),(0,0)))
      else:
        for j in range(shape0-3):
          np_obj = np.delete(np_obj,-1,0)
          np_obj_pad = np_obj
      bkg_jet_dataset_list.append(np_obj_pad)

  bkg_jet_data = np.array(bkg_jet_dataset_list)

  print(bkg_jet_data.shape)

  file = folderoutput+fname+'_class1_jet_data.npy'
  np.save(file, sgn_jet_data)

  file = folderoutput+fname+'_class0_jet_data.npy'
  np.save(file, bkg_jet_data)

  #fatjet data
  nfatjets = tree['nFatJet'].array()
  at_least_1fj = nfatjets>0

  fatjet_matched = tree['FatJet_matched'].array()
  nfatjet_match = np.sum(fatjet_matched>0, axis=1)
  at_least_1fj_match = nfatjet_match>0

  list_fatjet_var = ['FatJet_area', 'FatJet_btagDeepB', 'FatJet_deepTagMD_TvsQCD',
                     'FatJet_deepTagMD_WvsQCD', 'FatJet_deepTag_QCD', 'FatJet_deepTag_QCDothers',
                     'FatJet_deepTag_TvsQCD', 'FatJet_deepTag_WvsQCD', 'FatJet_eta',
                     'FatJet_mass', 'FatJet_phi', 'FatJet_pt']
  fatjet_match = tree.arrays(list_fatjet_var, 'FatJet_matched>0', library='pd')
  fatjet_notmatch = tree.arrays(list_fatjet_var, 'FatJet_matched==0', library='pd')
  fatjet = tree.arrays(list_fatjet_var, library='pd')

  sgn_fj_dataset_list = []
  for i in range(Nevents):
    if '1000' in fname and i== event_tojump1000:
      continue
    if '500' in fname and i== event_tojump500:
      continue
    if mask_top_had[i]:   # nr eventi deve essere compatibile con quello dei jets
      if at_least_1fj[i]:  # se ho almeno 1fatjet nell'evento da associare
        if at_least_1fj_match[i]:   # se c'( un fatjetmatchato prendo quello
          np_obj = fatjet_match.loc[(i, slice(None))].to_numpy()   # la shape la controllo alal fine
          shape0 = np_obj.shape[0]
          #else:                       # else uno a caso (pt maggiore) [non mettere nessun FatJet!]
          #np_obj = fatjet.loc[(i, slice(None))].to_numpy()
          #shape0 = np_obj.shape[0]
          # aggiustiamo la shape dell'evento
          if shape0>1:
            for j in range(shape0-1):
              np_obj = np.delete(np_obj, -1, 0)
            np_obj_pad = np_obj
          else:      # non ho altre possibilit)  visto che ne ho chiesto almeno 1
            np_obj_pad = np_obj
        else:
          np_obj_pad = np.zeros(shape=(1,len(list_fatjet_var)))
      else:                # else: padding
        np_obj_pad = np.zeros(shape=(1,len(list_fatjet_var)))
      sgn_fj_dataset_list.append(np_obj_pad)

  sgn_fj_data = np.array(sgn_fj_dataset_list)
  print('signal fatjet data ', sgn_fj_data.shape)


  bkg_fj_dataset_list = []
  for i in range(Nevents):
    if '1000' in fname and i== event_tojump1000:
      continue
    if '500' in fname and i== event_tojump500:
      continue
    if mask_bkg[i]:   # nr eventi deve essere compatibile con quello dei jets
                    # mask_bkg richiede almeno un jet non matchato (senza quello 
                    #     finirei a mandare un evento con tutti 0)
      if at_least_1fj[i]:  # se ho almeno 1fatjet nell'evento da associare
        np_obj = fatjet.loc[(i, slice(None))].to_numpy()   # la shape la controllo alal fine
        shape0 = np_obj.shape[0]
        # aggiustiamo la shape dell'evento
        if shape0>1:
          for j in range(shape0-1):
            np_obj = np.delete(np_obj, -1, 0)
          np_obj_pad = np_obj
        else:      # non ho altre possibilit  visto che ne ho chiesto almeno 1
          np_obj_pad = np_obj
      else:                # else: padding
        np_obj_pad = np.zeros(shape=(1,len(list_fatjet_var)))
      bkg_fj_dataset_list.append(np_obj_pad)

  bkg_fj_data = np.array(bkg_fj_dataset_list)
  print('bkg fatjet data ', bkg_fj_data.shape)


  file = folderoutput+fname+'_class1_fj_data.npy'
  np.save(file, sgn_fj_data)
  file = folderoutput+fname+'_class0_fj_data.npy'
  np.save(file, bkg_fj_data)
  print(fileinput+" done")
'''

for fileinput in samples_bkg :

  tree = uproot.open(folder_fileinput+fileinput+":Events")

  fname= fileinput
  if 'Skim' in fileinput:
    fname = fname.replace("_Skim","")
  fname = fname.replace(".root","")
  branches = tree.arrays(['nJet'])
  tot_events = len(branches)
  print(tot_events)
  Nevents = 20000
  print(Nevents)
  events = random.sample(range(tot_events), Nevents)
  to_avoid = [18732, 34132, 91938, 130443, 199926, 215761, 318536, 331759, 334611]
  while (to_avoid in events):
    events = random.sample(range(tot_events), Nevents)
  # jets matched
  list_jet_var = ['Jet_area', 'Jet_btagDeepFlavB', 'Jet_eta', 'Jet_mass',
                  'Jet_phi', 'Jet_pt']
  branches_jet_notmatch = tree.arrays(list_jet_var,  library='pd')
  mask_bkg = tree['nJet'].array()>0
  event_tojump1000 = 16128
  event_tojump500 = 1611
  event_tojumptt = [31588, 37050]
  bkg_jet_dataset_list = []
  for i in events:
    if '1000' in fname and i== event_tojump1000:
      continue
    if '500' in fname and i== event_tojump500:
      continue
    if 'tt' in fname and i in event_tojumptt:
      continue
    
    if mask_bkg[i]:
      np_obj = branches_jet_notmatch.loc[(i, slice(None))].to_numpy()  
      shape0 = np_obj.shape[0]
      if shape0<4:
        np_obj_pad = np.pad(np_obj , ((0,3-shape0),(0,0)))
      else:
        for j in range(shape0-3):
          np_obj = np.delete(np_obj,random.sample(range(np_obj.shape[0]), 1),0)
        np_obj_pad = np_obj
      if i%100==0: print('event ',i)
      bkg_jet_dataset_list.append(np_obj_pad)

  bkg_jet_data = np.array(bkg_jet_dataset_list)
  print('bkg jet data shape ',bkg_jet_data.shape)
  nfatjets = tree['nFatJet'].array()
  at_least_1fj = nfatjets>0
  list_fatjet_var = ['FatJet_area', 'FatJet_btagDeepB', 'FatJet_deepTagMD_TvsQCD',
                     'FatJet_deepTagMD_WvsQCD', 'FatJet_deepTag_QCD', 'FatJet_deepTag_QCDothers',
                     'FatJet_deepTag_TvsQCD', 'FatJet_deepTag_WvsQCD', 'FatJet_eta',
                     'FatJet_mass', 'FatJet_phi', 'FatJet_pt']
  fatjet_notmatch = tree.arrays(list_fatjet_var, library='pd')
  bkg_fj_dataset_list = []
  for i in events:
    if '1000' in fname and i== event_tojump1000:
      continue
    if '500' in fname and i== event_tojump500:
      continue
    if 'tt' in fname and i in event_tojumptt:
      continue
    if mask_bkg[i]:   # nr eventi deve essere compatibile con quello dei jets
                       # mask_bkg richiede almeno un jet non matchato (senza quello 
                      #     finirei a mandare un evento con tutti 0)
      if at_least_1fj[i]:  # se ho almeno 1fatjet nell'evento da associare
        np_obj = fatjet_notmatch.loc[(i, slice(None))].to_numpy()   # la shape la controllo alal fine
        shape0 = np_obj.shape[0]
        # aggiustiamo la shape dell'evento
        if shape0>1:
          for j in range(shape0-1):
            np_obj = np.delete(np_obj, random.sample(range(np_obj.shape[0]), 1), 0)
          np_obj_pad = np_obj
        else:      # non ho altre possibilit visto che ne ho chiesto almeno 1
          np_obj_pad = np_obj
      else:                # else: padding
        np_obj_pad = np.zeros(shape=(1,len(list_fatjet_var)))
      if i%100==0: print('event ',i)
      bkg_fj_dataset_list.append(np_obj_pad)

  bkg_fj_data = np.array(bkg_fj_dataset_list)
  print('bkg fj data', bkg_fj_data.shape)
  file = folderoutput+fname+'_class0_jet_data.npy'
  np.save(file, bkg_jet_data)
  file = folderoutput+fname+'_class0_fj_data.npy'
  np.save(file, bkg_fj_data)
  print(fileinput+' done')
