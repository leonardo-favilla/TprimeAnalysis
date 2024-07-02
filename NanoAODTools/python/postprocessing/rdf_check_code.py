import ROOT
from tools import *
from samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from datetime import datetime
import optparse
import math
import sys

usage = 'python rdf_check_code.py -d dataset'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
(opt, args) = parser.parse_args()

def HEMveto(jets, electrons):
    hemvetoetaup = -3.05
    hemvetoetadown = -1.35
    hemvetophiup = -1.62
    hemvetophidown = -0.82;
    passesMETHEMVeto = True

    for jet in jets:
        if(jet.eta>hemvetoetaup and jet.eta<hemvetoetadown and jet.phi>hemvetophiup and jet.phi<hemvetophidown):
            passesMETHEMVeto = False

    for ele in electrons:
        if(ele.eta>hemvetoetaup and ele.eta<hemvetoetadown and ele.phi>hemvetophiup and ele.phi<hemvetophidown):
            passesMETHEMVeto = False
 
    return passesMETHEMVeto
    
def leptonveto(electron, muon):
    EleVetoPassed = 0
    MuVetoPassed = 0
    IsLepVetoPassed = True
  
    for el in electron: 
        if(el.cutBased>=1 and el.pt > 30. and abs(el.eta)<2.5): 
            EleVetoPassed+=1
    for mu in muon:
        if(mu.looseId == 1 and mu.pt > 30. and abs(mu.eta) < 2.4): 
            MuVetoPassed+=1
    if(EleVetoPassed+MuVetoPassed >0): 
        IsLepVetoPassed = False
    return IsLepVetoPassed

def atleast1Ak4good(jets):
    b = False
    for j in jets:
        if(j.pt>30 and abs(j.eta)<4 and j.jetId>1):
           b = True
    return b
def atleast1Ak8good(fatjets):
    b = False
    for j in fatjets:
        if(j.pt>200 and j.msoftdrop>40):
           b = True
    return b

if not(opt.dat in sample_dict.keys()):
    print( sample_dict.keys())
dataset = sample_dict[opt.dat]

if hasattr(dataset, 'components'): # How to check whether this exists or not
    print("please enter a single subsample")
    sys.exit()
else:
    print("You are launching a single sample and not an entire bunch of samples")
    s = dataset

chain = ROOT.TChain('Events')
 
folder_files = "../../crab/macros/files/"
infile_string = open(folder_files+s.label+".txt")
file_list = infile_string.readlines()

print("Adding %s to the chain" %(len(file_list)))
for infile in file_list: 
    chain.Add(infile)

tree = InputTree(chain)
nevents = tree.GetEntries()
print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++ Defining histos ++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

hist_workflow = ROOT.TH1F("workflow", "workflow", 10, -0.5, 10)
hist_workflow.GetXaxis().SetBinLabel(1, "All events")
hist_workflow.GetXaxis().SetBinLabel(2, "HEM veto")
hist_workflow.GetXaxis().SetBinLabel(3, "MET Filt")
hist_workflow.GetXaxis().SetBinLabel(4, "HLT")
hist_workflow.GetXaxis().SetBinLabel(5, "AH")
hist_workflow.GetXaxis().SetBinLabel(6, "SL")

hist_met = ROOT.TH1F("MET_pt", "MET p_{T}", 8, 0, 800)
hist_deltaphi = ROOT.TH1F("MinDelta_phi", "min #Delta #phi", 18, 0, math.pi)

passMETfilt = 0
passHLT = 0
passHEMveto = 0

if 'Data' in s.label: isMC = False
else: isMC = True

print("sample: ", s.label)
print("isMC: ", isMC)
print("starting events loop : ", datetime.now().strftime("%H:%M:%S"))

for i in range(nevents):
    if i%100000==0: print(i)
    chain.GetEntry(i)
    event = Event(tree,i)
    jets = Collection(event, "Jet")
    fatjets = Collection(event, "FatJet")
    met = Object(event, "MET")
    mindeltaphi = Object(event, "MinDelta")
    electron = Collection(event, "Electron")
    muon = Collection(event, "Muon")
    HLT = Object(event, "HLT")
    flag = Object(event, "Flag")
    nelectron = len(electron)
    nmuon = len(muon)

    hist_workflow.AddBinContent(1)

    passesMETHEMVeto = HEMveto(jets, electron)
    if(s.year == 2018 and not passesMETHEMVeto):
        if(not isMC and chain.run > 319077.):
            continue
        # elif(isMC):
        #     w_nominal_nominal[0] *= 0.354
    hist_workflow.AddBinContent(2)
    passHEMveto +=1

    good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.ecalBadCalibFilter and flag.eeBadScFilter #and flag.BadPFMuonDzFilter
    if not (good_MET):
        continue
    hist_workflow.AddBinContent(3)
    passMETfilt += 1

    good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight
    if not (good_HLT and good_MET):
        continue
    hist_workflow.AddBinContent(4)
    passHLT += 1

    hist_met.Fill(met.pt)
    hist_deltaphi.Fill(mindeltaphi.phi)

    
    

print("Ending events loop : ", datetime.now().strftime("%H:%M:%S"))
print("HEM Veto Efficiency: ", passHEMveto/nevents)
print("MET filt Efficiency: ", passMETfilt/passHEMveto)
print("HLT Efficiency: ", passHLT/passMETfilt)
print("Total Efficiency: ", passHLT/nevents)

print("\n Total Events (start): ", nevents)
print("Total Events Select", passHLT)

outfile = ROOT.TFile("/eos/home-a/acagnott/DarkMatter/nosynch/pycodecheck/"+s.label+".root", "recreate")
hist_workflow.Write()
hist_met.Write()
hist_deltaphi.Write()
outfile.Close()
