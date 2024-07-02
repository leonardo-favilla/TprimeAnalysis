import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *
import keras.models 
from itertools import combinations, chain
from scipy.special import comb

def ncombs(n, k):  # return (n k) --> numero di k-ple dati n jets
    if (n-k)<0:
        return 0
    else:
        return factorial(n)/(factorial(n-k)*factorial(k))

def factorial(n):
    if n==0:
        return 1
    elif n<0:
        return 0
    else:
        return n*factorial(n-1)

def lowpt_top(j0, j1, j2):
    return j0.p4() + j1.p4() + j2.p4()

def highpt_top(j0, j1, j2, fj):
    if fj == None:
        top = j0.p4()+j1.p4()+j2.p4()
    elif j2==None:
        top = top2j1fj(fj, j0, j1)
    else:
        top = top3j1fj(fj, j0, j1, j2)
    return top

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj):
    if fj == None:#3j0fj
        top = j0.p4()+j1.p4()+j2.p4()
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
    elif j2 == None:#2j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
        top = top2j1fj(fj, j0, j1)
        mass_dnn[idx_top, 1] = top.M()
    else: #3j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        top = top3j1fj(fj, j0, j1, j2)
        mass_dnn[idx_top, 1] = top.M()
    return mass_dnn, top

def fill_fj(fj_dnn, fj, idx_top): 
    fj_dnn[idx_top, 0] = fj.area
    fj_dnn[idx_top, 1] = fj.btagDeepB
    fj_dnn[idx_top, 2] = fj.deepTagMD_TvsQCD
    fj_dnn[idx_top, 3] = fj.deepTagMD_WvsQCD
    fj_dnn[idx_top, 4] = fj.deepTag_QCD
    fj_dnn[idx_top, 5] = fj.deepTag_QCDothers
    fj_dnn[idx_top, 6] = fj.deepTag_TvsQCD
    fj_dnn[idx_top, 7] = fj.deepTag_WvsQCD
    fj_dnn[idx_top, 8] = fj.eta
    fj_dnn[idx_top, 9] = fj.mass
    fj_dnn[idx_top, 10] = fj.phi
    fj_dnn[idx_top, 11] = fj.pt
    return fj_dnn

def fill_jets(jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top): 

    jets_dnn[idx_top, 0, 0] = j0.area
    jets_dnn[idx_top, 0, 1] = j0.btagDeepB
    jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
    jets_dnn[idx_top, 0, 3] = j0.mass
    jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
    jets_dnn[idx_top, 0, 5] = j0.pt
    jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
    jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet
    
    jets_dnn[idx_top, 1, 0] = j1.area
    jets_dnn[idx_top, 1, 1] = j1.btagDeepB
    jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
    jets_dnn[idx_top, 1, 3] = j1.mass
    jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
    jets_dnn[idx_top, 1, 5] = j1.pt
    jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
    jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
    if hasattr(j2,"pt"):
        jets_dnn[idx_top, 2, 0] = j2.area
        jets_dnn[idx_top, 2, 1] = j2.btagDeepB
        jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
        jets_dnn[idx_top, 2, 3] = j2.mass
        jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
        jets_dnn[idx_top, 2, 5] = j2.pt
        jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
        jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
    
    return jets_dnn

class nanoTopcand(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        "branches Top candidate high pt"
        self.out.branch("nTopMixed", "I")
        self.out.branch("TopMixed_idxFatJet", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet0", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet1", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet2", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_pt", "F", lenVar="nTopMixed")
        # self.out.branch("TopMixed_pt_nominal", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_eta", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_phi", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_mass", "F", lenVar="nTopMixed")
        # self.out.branch("TopMixed_mass_nominal", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_truth", "F", lenVar="nTopMixed")
        "branches Top candidate low pt"
        self.out.branch("nTopResolved", "I")
        self.out.branch("TopResolved_idxJet0", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet1", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet2", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_pt", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_eta", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_phi", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_mass", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_truth", "F", lenVar="nTopResolved")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets = Collection(event,"Jet")
        njets = len(jets)
        fatjets = Collection(event,"FatJet")
        nfatjets = len(fatjets)
        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets = len(goodjets)
        ngoodfatjets = len(goodfatjets)

        pt_cut_low = 10000
        pt_cut_high = 0
        
        '''init variables to branch'''
        ntoplowpt = 0
        toplow_idxfatjet = []
        toplow_idxjet0 = []
        toplow_idxjet1 = []
        toplow_idxjet2 = []
        toplow_pt_ = []
        toplow_eta_ = []
        toplow_phi_ = []
        toplow_mass_ = []
        toplow_sumjetdeltarfatjet = []
        toplow_sumjetmaxdeltarjet = []
        toplow_truth = []
        ntophighpt = 0
        tophigh_idxfatjet = []
        tophigh_idxjet0 = []
        tophigh_idxjet1 = []
        tophigh_idxjet2 = []
        tophigh_pt_ = []
        tophigh_eta_ = []
        tophigh_phi_ = []
        tophigh_mass_ = []
        tophigh_sumjetdeltarfatjet = []
        tophigh_sumjetmaxdeltarjet = []
        tophigh_truth = []
        #low pt top loop
        for idx_j0 in range(ngoodjets):
            for idx_j1 in range(idx_j0):
                for idx_j2 in range(idx_j1):
                    j0, j1, j2 = goodjets[idx_j0], goodjets[idx_j1], goodjets[idx_j2]
                    top_p4 = lowpt_top(j0, j1, j2)
                    if top_p4.Pt()<pt_cut_low:
                        ntoplowpt+=1
                        toplow_idxjet0.append(idx_j0)
                        toplow_idxjet1.append(idx_j1)
                        toplow_idxjet2.append(idx_j2)
                        toplow_pt_.append(top_p4.Pt())
                        toplow_eta_.append(top_p4.Eta())
                        toplow_phi_.append(top_p4.Phi())
                        toplow_mass_.append(top_p4.M())
                        if self.isMC:
                            toplow_truth.append(truth(j0=j0, j1=j1, j2=j2))
                        else:
                            toplow_truth.append(0)
        
        for idx_j0 in range(ngoodjets):
                for idx_j1 in range(idx_j0):
                    for idx_fj in range(ngoodfatjets):
                        j0, j1 = goodjets[idx_j0],goodjets[idx_j1]
                        fj = goodfatjets[idx_fj]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=None, fj=fj)
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(idx_fj)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(-1)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            if self.isMC:
                                tophigh_truth.append(truth(j0=j0, j1=j1, fj=fj))
                            else:
                                tophigh_truth.append(0)
                    for idx_j2 in range(idx_j1):
                        j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=None)
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(-1)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(idx_j2)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            if self.isMC:
                                tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2))
                            else:
                                tophigh_truth.append(0)
                        for idx_fj in range(ngoodfatjets):
                            j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                            fj = goodfatjets[idx_fj]
                            top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=fj)
                            if top_p4.Pt()>pt_cut_high:
                                ntophighpt += 1
                                tophigh_idxfatjet.append(idx_fj)
                                tophigh_idxjet0.append(idx_j0)
                                tophigh_idxjet1.append(idx_j1)
                                tophigh_idxjet2.append(idx_j2)
                                tophigh_pt_.append(top_p4.Pt())
                                tophigh_eta_.append(top_p4.Eta())
                                tophigh_phi_.append(top_p4.Phi())
                                tophigh_mass_.append(top_p4.M())
                                if self.isMC:
                                    tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2, fj=fj))
                                else: 
                                    tophigh_truth.append(0)
        
        self.out.fillBranch("nTopResolved", ntoplowpt)
        self.out.fillBranch("TopResolved_idxJet0", toplow_idxjet0)
        self.out.fillBranch("TopResolved_idxJet1", toplow_idxjet1)
        self.out.fillBranch("TopResolved_idxJet2", toplow_idxjet2)
        self.out.fillBranch("TopResolved_pt", toplow_pt_)
        self.out.fillBranch("TopResolved_eta", toplow_eta_)
        self.out.fillBranch("TopResolved_phi", toplow_phi_)
        self.out.fillBranch("TopResolved_mass", toplow_mass_)
        self.out.fillBranch("TopResolved_truth", toplow_truth)
        self.out.fillBranch("nTopMixed", ntophighpt)
        self.out.fillBranch("TopMixed_idxFatJet", tophigh_idxfatjet)
        self.out.fillBranch("TopMixed_idxJet0", tophigh_idxjet0)
        self.out.fillBranch("TopMixed_idxJet1", tophigh_idxjet1)
        self.out.fillBranch("TopMixed_idxJet2", tophigh_idxjet2)
        self.out.fillBranch("TopMixed_pt", tophigh_pt_)
        self.out.fillBranch("TopMixed_eta", tophigh_eta_)
        self.out.fillBranch("TopMixed_phi", tophigh_phi_)
        self.out.fillBranch("TopMixed_mass", tophigh_mass_)
        self.out.fillBranch("TopMixed_truth", tophigh_truth)
        # t1 = datetime.now()
        # print("TopCandidate module time :", t1-t0)  
        return True

