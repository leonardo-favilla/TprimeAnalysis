import uproot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import awkward as ak
import vector
import mplhep as hep
hep.style.use(hep.style.CMS)
import tensorflow as tf
import tensorflow.keras
import keras
import sys
import random
import pickle as pkl

folder_model = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/"
model_name = "DNN_withtopmass_phase2_withoutTopmass.h5"
model = keras.models.load_model(folder_model+model_name)

file = open("/eos/home-a/acagnott/DarkMatter/trainingSet/trainingset_phase2.pkl", "rb")
dict_samples = pkl.load(file)
file.close()

categories = ['3j1fj', '3j0fj','2j1fj']
datasets = ['tDM_mPhi1000_mChi1', 'QCD_HT1000']

X_jet = {c: 0 for c in categories}
X_fatjet = {c: 0 for c in categories}
X_mass = {c: 0 for c in categories}
y = {c: 0 for c in categories}
pred_all = {c: 0 for c in categories}

for c in categories:
    X_jet[c] = np.concatenate([dict_samples[d][c][0] for d in datasets ])
    X_fatjet[c] = np.concatenate([dict_samples[d][c][1] for d in datasets])
    X_mass[c] = np.concatenate([dict_samples[d][c][2][:,1] for d in datasets])
                          
    y[c] = np.concatenate([dict_samples[d][c][3] for d in datasets] )
    pred_all[c] = model.predict({'fatjet': X_fatjet[c], 'jet': X_jet[c], 'top_mass': X_mass[c]})
folder_plot = '/eos/home-a/acagnott/DarkMatter/plotTrainingStudies/'
if not os.path.exists(folder_plot):
    os.mkdir(folder_plot)

for x in np.arange(0,0.45, 0.05):
    x1 = round(x,2)
    x2 = round(x,2) + round(0.05, 2)
    folder_plot_ = folder_plot+'range'+str(x1)+'_'+str(x2)+'/'
    if not os.path.exists(folder_plot_):
        os.mkdir(folder_plot_)
        #for c in categories: print(X_jet[c].shape)
    for n in range(X_jet['3j1fj'].shape[2]):
        fig, ax = plt.subplots(ncols = 3, figsize = (30, 10))
        bins = 50
        for c in categories:
            cut = (pred_all[c]>x1)*(pred_all[c]<x2)#pred_all[n]>0.38#
            cut = cut.flatten()
            cut2 = y[c].flatten()==1
            ax[0].hist(X_jet[c][cut*cut2][:,0, n], histtype = 'step', bins = bins, label = c )
            ax[1].hist(X_jet[c][cut*cut2][:,1, n], histtype = 'step', bins = bins, label = c )
            ax[2].hist(X_jet[c][cut*cut2][:,2, n][X_jet[c][cut*cut2][:,2, n]>0], histtype = 'step', bins = bins, label = c )
        ax[0].set_title('variable #'+str(n)+' of jets with predict in range ['+str(x1)+','+str(x2)+']')
        ax[0].legend()
        ax[1].legend()
        ax[2].legend()
        plt.savefig(folder_plot_+'Jet_'+str(n))
        plt.close('all')
    for n in range(X_fatjet['3j1fj'].shape[1]):
        fig, ax = plt.subplots()
        bins = 50
        for c in categories:
            if c =='3j0fj': continue
            cut = (pred_all[c]>x1)*(pred_all[c]<x2)#pred_all[n]>0.38#
            cut = cut.flatten()
            cut2 = y[c].flatten()==1
            ax.hist(X_fatjet[c][cut*cut2][:,n], histtype = 'step', bins = bins, label = c )
        ax.legend()
        ax.set_title('variable #'+str(n)+' of fatjet with predict in range ['+str(x1)+','+str(x2)+']')
        plt.savefig(folder_plot_+'FatJet_'+str(n))
        plt.close('all')
