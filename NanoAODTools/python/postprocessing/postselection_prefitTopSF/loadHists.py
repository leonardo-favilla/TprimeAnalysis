import ROOT
import copy
###### Retrieve histograms saved into a .root file ######
def loadHists(inFilePath):
    inFile      = ROOT.TFile.Open(inFilePath, "READ")
    keyList     = inFile.GetListOfKeys()
    histList    = {}
    for key in keyList:
        keyName = key.GetName()
        # print(keyName)
        hist    = copy.deepcopy(inFile.Get(keyName))
        # if (type(hist) == ROOT.TH1F) or (type(hist) == ROOT.TH2F):
        #     hist.SetDirectory(ROOT.gROOT)
        hist.SetName(keyName)
        histList[keyName]=hist
    if len(histList)==0: 
        raise Exception("ERROR: histList is empty!")
    inFile.Close()
    return histList