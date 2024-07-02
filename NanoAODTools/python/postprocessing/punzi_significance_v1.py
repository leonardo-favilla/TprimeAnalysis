import ROOT
import os
from samples.samples import *
from math import sqrt
import array
import numpy as np
import pickle as pkl
import optparse
import matplotlib.pyplot as plt
import mplhep as hep

hep.style.use(hep.style.CMS)

usage = "python3 punzi_significance.py"
parser = optparse.OptionParser(usage)
parser.add_option('-p', '--plot', dest='plot', default = False, action='store_true', help='Default make no plots')
parser.add_option('-c', '--count', dest='count', default= False, action='store_true', help='Default no count is done')
(opt, args) = parser.parse_args()

count = opt.count
plot = opt.plot

folder = '/afs/cern.ch/work/a/acagnott/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/crab/macros/files/'
maxFiles = 3
lumi = 100


def event_counting(dataset, valori_cut): #dataset --> da sample.py 
    b = {
        cut: {c: 0 for c in valori_cut["MinDelta_phi"]} for cut in valori_cut["MET_pt"]
    }
    eff = {
        cut: {c: 0 for c in valori_cut["MinDelta_phi"]} for cut in valori_cut["MET_pt"]
    }
    if hasattr(dataset, "components"):
        samples = dataset.components
    else:
        samples = [dataset]
    print("Launching dataset: ", dataset.label)
    for s in samples:
        print("...launching sample: ", s.label)
        tmp = { cut: {c: [] for c in valori_cut["MinDelta_phi"]} for cut in valori_cut["MET_pt"] }
        tmp_ = { cut: {c: [] for c in valori_cut["MinDelta_phi"]} for cut in valori_cut["MET_pt"] }
        tmp_txtf = open(folder+s.label+'.txt',"r")
        tmp_txtRfiles = tmp_txtf.readlines()
        if len(tmp_txtRfiles)<maxFiles:  nfiles = len(tmp_txtRfiles)
        else: nfiles = maxFiles
        for i in range(nfiles):
            rfile_string=tmp_txtRfiles[i].replace('\n', '')
            rfile =ROOT.TFile.Open(rfile_string)
            h_genweight = ROOT.TH1F(rfile.Get("plots/h_genweight"))
            ntot= h_genweight.GetBinContent(1)
            w = lumi*s.sigma/ntot#h_genweight.GetBinContent(1)
            rfile.Close()
            rdf = ROOT.RDataFrame("Events", rfile_string)
            #for v in variabili:
            v = "MET_pt"
            for c in valori_cut[v]:
                for cut in valori_cut["MinDelta_phi"]:
                    new_df = rdf.Filter(v+">"+str(c)).Filter("MinDelta_phi>"+str(cut)) 
                    tmp[c][cut].append(new_df.Count().GetValue()*w) #filling lists of tmp
                    if 'Tp' in s.label:
                        tmp_[c][cut].append(new_df.Count().GetValue()/(ntot*0.20*0.665))
                    else:
                        tmp_[c][cut].append(new_df.Count().GetValue()/ntot)
        for c in valori_cut[v]:
            for cut in valori_cut["MinDelta_phi"]:
                b[c][cut] = np.mean(tmp[c][cut]) # filling # of bkg events
                eff[c][cut] = np.mean(tmp_[c][cut]) # filling # of bkg events
    return b, eff

def makegraph(valori_cut, sign_label):
    n = {d.label: 0  for d in bkg_set+sgn_set}
    eff = {d.label: 0  for d in sgn_set}
    for d in bkg_set+sgn_set:
        if not os.path.exists("./punzi_significance/"+d.label+".pkl"):
            print( d.label +" does not exists! Please launch with -c addind the dataset to the list")
            continue
        fin = open("./punzi_significance/"+d.label+".pkl", "rb")
        n[d.label] = pkl.load(fin)
        if 'Tp' in d.label:
            fin = open("./punzi_significance/"+d.label+"_eff.pkl", "rb")
            eff[d.label] = pkl.load(fin)
            fin.close()
    v = "MET_pt"
    bkg = {cut: {c:0 for c in valori_cut["MinDelta_phi"]} for cut in valori_cut[v]} 
    sig = {cut: {c:0 for c in valori_cut["MinDelta_phi"]} for cut in valori_cut[v]}
    
    for d in n.keys():
        if not ('Tp' in d or 'tDM' in d):
            for cut in valori_cut[v]:
                for c in valori_cut["MinDelta_phi"]:
                    bkg[cut][c] += n[d][cut][c]
        else:
            for cut in valori_cut[v]:
                for c in valori_cut["MinDelta_phi"]:
                    sig[cut][c] = n[d][cut][c]
    fig, ax = plt.subplots(ncols=2, figsize =(20,10))
    for c in valori_cut["MinDelta_phi"]:
        y_arr=[]
        y_arr1=[]
        for cut in valori_cut[v]:
            y_arr.append(sig[cut][c]/sqrt(bkg[cut][c]))
            y_arr1.append(eff[sign_label][cut][c])
        ax[0].plot(np.array(valori_cut[v]), np.array(y_arr), label = "min$\Delta\phi$>"+str(c))
        ax[1].plot(np.array(valori_cut[v]), np.array(y_arr1), label = "min$\Delta\phi$>"+str(c))
        
    ax[0].set_xlabel(v)
    ax[1].set_xlabel(v)
    ax[0].set_ylabel("s/$\sqrt{b}$")
    ax[1].set_ylabel("$\epsilon_{S}$")
    ax[0].legend()
    ax[1].legend()
    ax[0].set_title(sign_label)
    fig.savefig("/eos/home-a/acagnott/DarkMatter/punzi_significance_plots/test_significance_"+v+"_"+sign_label+".png")


# come migliorare: aprire una sola volta i files ed estrarre i valori per ogni taglio 


bkg_set = [QCD_2018, 
           ZJetsToNuNu_2018, TT_2018
    ]
sgn_set = [#TprimeToTZ_700_2018,
           #TprimeToTZ_1000_2018,
           TprimeToTZ_1800_2018
]
print("Bkg datasets :", [b.label for b in bkg_set])
print("Signal datasets :", [b.label for b in sgn_set])

if len(sgn_set)>1: print("Ci sono + di 1 segnale --> se devi fare i plot indicarne solo 1")

#variabili = ["MET_pt", "MinDelta_phi"]
valori_cut = {"MET_pt": [100, 150, 200, 250, 300],  #non 50 --> imposto nel module preselection 
              "MinDelta_phi": [0, 0.2, 0.4, 0.6]
}
print("cuts dict :", valori_cut)

'''n = {
     d.label:  for d in bkg_set+sgn_set
 } 
'''
if count:
    for d in bkg_set+sgn_set:
        n,eff = event_counting(d, valori_cut)
        print(n)
        fout = open("./punzi_significance/"+d.label+".pkl", "wb")
        pkl.dump(n, fout)
        fout.close()
        fout = open("./punzi_significance/"+d.label+"_eff.pkl", "wb")
        pkl.dump(eff, fout)
        fout.close()
if plot:
    makegraph(valori_cut, sgn_set[0].label)

