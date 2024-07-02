import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import awkward as ak
import vector
import tensorflow as tf
import tensorflow.keras
import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, MaxPooling1D, Reshape
from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.backend import sigmoid
from tensorflow.keras import regularizers
# from keras.utils.generic_utils import get_custom_objects
import sys
import random
from math import sqrt
import pickle as pkl

seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)
import random
random.seed(seed_value)
np.random.seed(seed_value)
import keras
import tensorflow as tf
tf.random.set_seed(12345)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
from tensorflow.python.keras import backend as K
K.set_session(sess)
import mplhep as hep
hep.style.use(hep.style.CMS)

reduce_dataset = True
dnn_name = 'DNN_Resolved_2022'
folder = '/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/'+dnn_name+'/'
if not os.path.exists(folder):
    os.mkdir(folder)

infolder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_year_2022_1/pkls"
samples = []
for s in os.listdir(infolder):
    if s.startswith("trainingSet") and s.endswith(".pkl"):
        samples.append(s)
categories = ['3j0fj']
dict_samples = {}
datasets = []
for d in samples:
    if ("70to100" in d) or ("100to200" in d) or ("200to400" in d): continue
    file = open(infolder+"/"+d, "rb")
    tmp = pkl.load(file)
    for k in tmp.keys():
        datasets.append(k)
        dict_samples[k] = tmp[k]
    file.close()

if reduce_dataset:
    for d in datasets:
        for c in categories:
            idx_falsetop = [i for i, x in enumerate(dict_samples[d][c][3]==0) if x==True]
            ids_todrop = random.sample(idx_falsetop, int(len(idx_falsetop)*(9/10)))
            dict_samples[d][c][0] = np.delete(dict_samples[d][c][0], ids_todrop, axis=0)
            dict_samples[d][c][1] = np.delete(dict_samples[d][c][1], ids_todrop, axis=0)
            dict_samples[d][c][2] = np.delete(dict_samples[d][c][2], ids_todrop, axis=0)
            dict_samples[d][c][3] = np.delete(dict_samples[d][c][3], ids_todrop, axis=0)

pt_sep = 250
X_jet_lowpt = np.concatenate([dict_samples[d][c][0][:,:,:-2][dict_samples[d][c][2][:,2]<pt_sep]
                              for d in datasets for c in categories ])
X_mass_lowpt = np.concatenate([dict_samples[d][c][2][dict_samples[d][c][2][:,2]<pt_sep]
                               for d in datasets for c in categories])
y_lowpt = np.concatenate([dict_samples[d][c][3][dict_samples[d][c][2][:,2]<pt_sep]
                          for d in datasets for c in categories] )

X_jet_lowpt_train, X_jet_lowpt_test, X_mass_lowpt_train, X_mass_lowpt_test, y_lowpt_train, y_lowpt_test = train_test_split(X_jet_lowpt, X_mass_lowpt, y_lowpt, stratify=y_lowpt, shuffle=True, test_size=0.3)

dropout = 0.1

jet0_inputs = tf.keras.Input(shape=(X_jet_lowpt_train.shape[2],), name = 'jet0')    #y
jet1_inputs = tf.keras.Input(shape=(X_jet_lowpt_train.shape[2],), name = 'jet1')
jet2_inputs = tf.keras.Input(shape=(X_jet_lowpt_train.shape[2],), name = 'jet2')
#mass_input = tf.keras.Input(shape=(2, ), name = 'top_mass')
#x = Masking(mask_value=0)(fj_inputs) # ultima modifica

y0 = Masking(mask_value=0.)(jet0_inputs)
y1 = Masking(mask_value=0.)(jet1_inputs)
y2 = Masking(mask_value=0.)(jet2_inputs)
y0 = BatchNormalization()(y0)
y1 = BatchNormalization()(y1)
y2 = BatchNormalization()(y2)

y = concatenate([y0,y1,y2])
y = Dense(25, activation='relu')(y)#tanh
# y = Dropout(dropout)(y)
y = Dense(30, activation='relu')(y)# con 10 celle a testa sembra buono ma lo score non si distribuisce fino a 1
# y = Dropout(dropout)(y)

outputs = Dense(1, activation='sigmoid')(y) 
#model = tf.keras.Model(inputs=[fj_inputs, jet_inputs, mass_input], outputs=outputs)
model2 = tf.keras.Model(inputs=[jet0_inputs, jet1_inputs, jet2_inputs], outputs=outputs)

trainer = tf.keras.optimizers.Adam(learning_rate=0.01)
loss = tf.keras.losses.BinaryCrossentropy()
model2.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])
model2.summary()

early_stop = keras.callbacks.EarlyStopping(monitor = 'val_loss',
                                           mode='min',# quantity that has to be monitored(to be minimized in this case)
                                           patience = 30, # Number of epochs with no improvement after which training will be stopped.
                                           min_delta = 1e-4,
                                           restore_best_weights = True) # update the model with the best-seen weights

#Reduce learning rate when a metric has stopped improving
reduce_LR = keras.callbacks.ReduceLROnPlateau(monitor = 'auc',
                                              mode='max',# quantity that has to be monitored
                                              min_delta=1e-4,
                                              factor = 0.5, # factor by which LR has to be reduced...
                                              patience = 10, #...after waiting this number of epochs with no improvements 
                                              #on monitored quantity
                                              min_lr= 1e-15 ) 


#callback_list = [reduce_LR, early_stop]
callback_list = [early_stop]

epochs = 10000
batch_size = 100 # 150 più o meno ok

#history = model.fit({'fatjet': X_fatjet_train, 'jet':X_jet_train, 'top_mass': X_mass_train}, y_train, callbacks=callback_list, 
#                    validation_split = 0.1,
#                    epochs=epochs, batch_size=batch_size, verbose=1)
history2 = model2.fit({'jet0':X_jet_lowpt_train[:,0], 'jet1':X_jet_lowpt_train[:,1], 'jet2':X_jet_lowpt_train[:,2]}, 
                     y_lowpt_train, callbacks=callback_list, 
                    validation_split = 0.2,
                    epochs=epochs, batch_size=batch_size, verbose=1)

# list all data in history
print(history2.history.keys())
# summarize history for accuracy
fig, ax = plt.subplots(ncols=2, figsize=(25,10))
for var in history2.history.keys():
    if ('loss' in var) and (not 'val' in var): ax[1].plot(history2.history[var], label ='train')
    if 'val_loss' in var: ax[1].plot(history2.history[var], label ='val')
    if ('auc' in var) and (not 'val' in var): ax[0].plot(history2.history[var], label ='train')
    if 'val_auc' in var : ax[0].plot(history2.history[var], label ='val')

ax[0].set_title('model accuracy')
ax[0].set_ylabel('auc')
ax[0].set_xlabel('epoch')
ax[0].legend()
# summarize history for loss
ax[1].set_title('model loss')
ax[1].set_ylabel('loss')
ax[1].set_xlabel('epoch')
ax[1].legend()
#ax[1].set_yscale('Log')
plt.savefig(folder + 'auc_loss_DNN.png')

y_pred2 = model2.predict({'jet0':X_jet_lowpt_test[:,0], 'jet1':X_jet_lowpt_test[:,1], 'jet2':X_jet_lowpt_test[:,2]})
y_pred_train2 = model2.predict({'jet0':X_jet_lowpt_train[:,0], 'jet1':X_jet_lowpt_train[:,1], 'jet2':X_jet_lowpt_train[:,2]})
y_pred_train_bkg2 = y_pred_train2[y_lowpt_train==0]
y_pred_train_sgn2 = y_pred_train2[y_lowpt_train==1]
y_pred_bkg2 = y_pred2[y_lowpt_test==0]
y_pred_sgn2 = y_pred2[y_lowpt_test==1]
bins = 30

fig, ax = plt.subplots(figsize=(10,10))


bins_count_bkg = ax.hist(y_pred_train_bkg2, alpha=0.5, color='blue', 
                         density=True, label='B (train)', range = [0,1], bins = bins)
bins_count_sgn = ax.hist(y_pred_train_sgn2, alpha=0.5,color='red', 
                         density=True, label='S (train)', range = [0,1], bins = bins)

hist, bins = np.histogram(y_pred_bkg2, range = [0,1], bins=bins, density=True)
scale = len(y_pred_bkg2) / sum(hist)
err = np.sqrt(hist * scale) / scale
center = (bins[:-1] + bins[1:]) / 2
ax.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

hist, bins = np.histogram(y_pred_sgn2, range = [0,1], bins=bins, density=True)
scale = len(y_pred_sgn2) / sum(hist)
err = np.sqrt(hist * scale) / scale
center = (bins[:-1] + bins[1:]) / 2
ax.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')

ax.set_xlabel('score')
ax.set_ylabel('arbitrary units')
ax.legend()
plt.yscale('log')
plt.savefig(folder+'traintestDiscrimination_DNN.png')
model2.save(folder+dnn_name+".h5")

from sklearn.metrics import roc_curve, roc_auc_score
y_score2 = y_pred2.ravel()
y_true2 = y_lowpt_test.ravel()
fpr, tpr, trs =roc_curve(y_true = y_true2, y_score = y_score2, pos_label=1)
fig, ax = plt.subplots()
ax.plot(fpr, tpr) 
ax.set_title('ROC')
ax.set_xlabel('False Positive Rate') 
ax.set_ylabel('True Positive Rate') 
plt.xscale('log')

plt.savefig(folder+'ROC_DNN.png')


print('10%   trs', trs[fpr<0.1][-1], 'tpr ',tpr[fpr<0.1][-1])
print('5%    trs',trs[fpr<0.05][-1], 'tpr ', tpr[fpr<0.05][-1])
print('1%    trs',trs[fpr<0.01][-1], 'tpr ', tpr[fpr<0.01][-1])
print('0.1%  trs',trs[fpr<0.001][-1], 'tpr ', tpr[fpr<0.001][-1])

tresholds = {'fpr 10': trs[fpr<0.1][-1], 
      'fpr 5': trs[fpr<0.05][-1], 
      'fpr 1': trs[fpr<0.01][-1], 
      'fpr 01':trs[fpr<0.001][-1]}
with open(folder+"tresholds_DNN_training2022.pkl", "wb") as file:
     pkl.dump(tresholds, file)