import os
from samples.samples import *
import optparse
import json
import sys
from tqdm import tqdm

usage = 'python3 postselection_rdf.py'
parser = optparse.OptionParser(usage)
parser.add_option('--opt', dest='opt', default = 'update',  help='update the dict_samples or recreate')
parser.add_option('-d', '--dataset', dest='dataset', default = '', help='make histos of this dataset if present')
(opt, args) = parser.parse_args()

def get_files_string(d):
    folder_files = "../../crab/macros/files/"
    infile_string = open(folder_files+d.label+".txt")
    strings = infile_string.readlines()
    #for s in strings: s.replace('\n', '')
    # print(d.label, strings)
    return strings

def samp_writer(dat, samples, opt, isMC):
    if hasattr(dat, "components"):  
        listOfSamples = dat.components
    else:
        listOfSamples = [dat]

    if opt == "update":
        samples[dat.label] = {}
    elif opt == "recreate":
        samples = {dat.label: {}}
    print("looping on samples", [l.label for l in listOfSamples])
    nofiles = False
    
    for s in listOfSamples:
        strings = get_files_string(s)
        #print("strings : ", strings)
        #if "No files to retrieve." in strings[0] or not "root://cms-xrd-global.cern.ch//" in strings[0]:
        if "No files to retrieve." in strings[0] :
            print("No files for: ", s.label) 
            strings = [""]
            nofiles = True
        ntot = []
        #print("looping on strings: ", len(strings))
        if isMC and not nofiles:
            print("Opening files strings of ", s.label)
            for f in tqdm(strings): 
                ifile = ROOT.TFile.Open(f)
                h_genweight = ROOT.TH1F(ifile.Get("plots/h_genweight"))
                ntot.append(h_genweight.GetBinContent(1))
                ifile.Close()
        else:
            ntot = [None for f in strings]
                
        samples[dat.label][s.label] = {'strings': strings, 'ntot': ntot}
        samples[s.label] = {}
        samples[s.label][s.label] = {'strings': strings, 'ntot': ntot}
        #print(samples[dat.label][s.label])
    return samples

if not opt.dataset in sample_dict.keys():
    datasets = [#DataHT_2018, QCD_2018, ZJetsToNuNu_2018, TT_2018, WJets_2018, TprimeToTZ_700_2018, TprimeToTZ_1000_2018,TprimeToTZ_1800_2018,
                DataJetMET_2022, DataMuon_2022, QCD_2022, ZJetsToNuNu_2022, WJets_2022, WJets_2jets_2022, TT_2022, TprimeToTZ_700_2022, TprimeToTZ_1800_2022,
                #TprimeToTZ_1000_2022, TT_2022
                ]
    opt = "recreate"
else : 
    datasets = [sample_dict[opt.dataset]]
    opt = opt.opt


print([dat.label for dat in datasets])
print("opt: ", opt)
print("Uploading samples dict")
json_string = "samples/dict_samples_2022.json"
if os.path.exists(json_string):
    sample_file = open(json_string, "rb")
    samples = json.load(sample_file)
    sample_file.close()
else:
    samples = {}

for dat in datasets:
    if "Data" in dat.label : 
        isMC = False
    else:
        isMC = True
    print("Processing "+dat.label+" ...")
    print("isMC flag is ", isMC)
    tmp_samples = samp_writer(dat, samples, opt, isMC)
    opt = "update"
#print(tmp_samples)
# sample_file = open("samples/dict_samples.pkl", "wb")
# pkl.dump(samples, sample_file)
# sample_file.close()    

with open("samples/dict_samples_2022.json", "w") as f:
    json.dump(samples, f, indent = 2)
