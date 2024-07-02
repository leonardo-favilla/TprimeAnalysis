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


def event_counting(dataset, variabili, valori_cut): #dataset --> da sample.py 
    b = {
        v: {cut: 0 for cut in valori_cut[v]} for v in variabili
    }
    eff = {
        v: {cut: 0 for cut in valori_cut[v]} for v in variabili
    }
    if hasattr(dataset, "components"):
        samples = dataset.components
    else:
        samples = [dataset]
    print("Launching dataset: ", dataset.label)
    for s in samples:
        print("...launching sample: ", s.label)
        tmp = {v: {cut: [] for cut in valori_cut[v]} for v in variabili} # contenitore temporaneo del #eventi per ogni taglio
        tmp_ = {v: {cut: [] for cut in valori_cut[v]} for v in variabili} # contenitore temporaneo del #eventi per ogni taglio
        tmp_txtf = open(folder+s.label+'.txt',"r")
        tmp_txtRfiles = tmp_txtf.readlines()
        if len(tmp_txtRfiles)<maxFiles:  nfiles = len(tmp_txtRfiles)
        else: nfiles = maxFiles
        for i in range(nfiles):
            rfile_string=tmp_txtRfiles[i].replace('\n', '')
            rfile =ROOT.TFile.Open(rfile_string)
            h_genweight = ROOT.TH1F(rfile.Get("plots/h_genweight"))
            w = lumi*s.sigma/h_genweight.GetBinContent(1)
            rfile.Close()
            rdf = ROOT.RDataFrame("Events", rfile_string)
            for v in variabili:
                for c in valori_cut[v]:
                    new_df = rdf.Filter(v+">"+str(c))
                    tmp[v][c].append(new_df.Count().GetValue()*w) #filling lists of tmp
                    if not 'Tp' in s.label: 
                        tmp_[v][c].append(new_df.Count().GetValue()/h_genweight.GetBinContent(1))
                    else :
                        tmp_[v][c].append(new_df.Count().GetValue()/(h_genweight.GetBinContent(1)*0.665*0.20))
        for v in variabili:
            for c in valori_cut[v]:
                b[v][c] = np.mean(tmp[v][c]) # filling # of bkg events
                eff[v][c]=np.mean(tmp_[v][c])
    return b, eff

def makegraph(variabili, valori_cut, sign_label):
    n = {d.label: 0  for d in bkg_set+sgn_set}
    for d in bkg_set+sgn_set:
        if not os.path.exists("./punzi_significance/"+d.label+".pkl"):
            print( d.label +" does not exists! Please launch with -c addind the dataset to the list")
            continue
        fin = open("./punzi_significance/"+d.label+".pkl", "rb")
        n[d.label] = pkl.load(fin)
        fin.close()
    bkg = {v: {cut: 0 for cut in valori_cut[v]} for v in variabili}
    sig = {v: {cut: 0 for cut in valori_cut[v]} for v in variabili}
    for d in n.keys():
        if not ('Tp' in d or 'tDM' in d):
            for v in variabili:
                for cut in valori_cut[v]:
                    bkg[v][cut] += n[d][v][cut]
        else:
            for v in variabili:
                for cut in valori_cut[v]:
                    sig[v][cut] = n[d][v][cut]
    for v in variabili:
        fig, ax = plt.subplots()
        y_arr=[]
        for cut in valori_cut[v]:
            y_arr.append(sig[v][cut]/sqrt(bkg[v][cut]))
            
        ax.plot(np.array(valori_cut[v]), np.array(y_arr))
        ax.set_xlabel(v)
        ax.set_ylabel("s/$\sqrt{b}$")
        ax.set_title(sign_label)
        fig.savefig("/eos/home-a/acagnott/DarkMatter/punzi_significance_plots/test_significance_"+v+"_"+sign_label+".png")


# come migliorare: aprire una sola volta i files ed estrarre i valori per ogni taglio 


bkg_set = [QCD_2018, ZJetsToNuNu_2018, TT_2018]
sgn_set = [TprimeToTZ_700_2018]
print("Bkg datasets :", [b.label for b in bkg_set])
print("Signal datasets :", [b.label for b in sgn_set])

if len(sgn_set)>1: print("Ci sono + di 1 segnale --> se devi fare i plot indicarne solo 1")

variabili = ["MET_pt", "MinDelta_phi"]
valori_cut = {"MET_pt": [100, 150, 200, 250, 300],  #non 50 --> imposto nel module preselection 
              "MinDelta_phi": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
}
print("cuts dict :", valori_cut)

'''n = {
     d.label:  for d in bkg_set+sgn_set
 } 
'''
if count:
    for d in bkg_set+sgn_set:
        n, eff = event_counting(d, variabili, valori_cut)
        print(n)
        fout = open("./punzi_significance/"+d.label+".pkl", "wb")
        pkl.dump(n, fout)
        fout.close()
        fout = open("./punzi_significance/"+d.label+"_eff.pkl", "wb")
        pkl.dump(eff, fout)
        fout.close()
if plot:
    makegraph(variabili, valori_cut, sgn_set[0].label)

