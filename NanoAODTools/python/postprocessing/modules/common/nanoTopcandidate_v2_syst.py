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

def lowpt_top(j0, j1, j2, s):
    # top_p4 = ROOT.TLorentzVector()
    j0_p4 = ROOT.TLorentzVector()
    j1_p4 = ROOT.TLorentzVector()
    j2_p4 = ROOT.TLorentzVector()
    if s == "nominal":
        j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
        j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
    elif s == "jesTotalup":
        j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
        j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup) 
    elif s == "jesTotaldown":
        j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
        j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
    elif s == "jerup":
        j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
        j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
    elif s == "jerdown":
        j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
        j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
    top_p4 = j0_p4+j1_p4+j2_p4
    return top_p4

def highpt_top(j0, j1, j2, fj, s):
    if fj == None:
        top = lowpt_top(j0, j1, j2, s)
    elif j2==None:
        top = top2j1fj(fj, j0, j1, s)
    else:
        top = top3j1fj(fj, j0, j1, j2, s)
    return top


class nanoTopcand(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        if isMC : self.scenarios = ["nominal", "jesTotalup", "jesTotaldown", "jerup", "jerdown"]
        else: self.scenarios = ["nominal"]
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
        self.out.branch("TopMixed_eta", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_phi", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_truth", "F", lenVar="nTopMixed")
        "branches Top candidate low pt"
        self.out.branch("nTopResolved", "I")
        self.out.branch("TopResolved_idxJet0", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet1", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet2", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_eta", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_phi", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_truth", "F", lenVar="nTopResolved")
        for scenario in self.scenarios:
            self.out.branch("TopMixed_pt_"+scenario, "F", lenVar="nTopMixed")
            self.out.branch("TopMixed_mass_"+scenario, "F", lenVar="nTopMixed")
            self.out.branch("TopResolved_pt_"+scenario, "F", lenVar="nTopResolved")
            self.out.branch("TopResolved_mass_"+scenario, "F", lenVar="nTopResolved")

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
        toplow_eta_ = []
        toplow_phi_ = []
        toplow_truth = []

        ntophighpt = 0
        tophigh_idxfatjet = []
        tophigh_idxjet0 = []
        tophigh_idxjet1 = []
        tophigh_idxjet2 = []
        tophigh_eta_ = []
        tophigh_phi_ = []
        tophigh_truth = []
        
        if self.isMC:
            tophigh_pt_   = {s: [] for s in self.scenarios}
            tophigh_mass_ = {s: [] for s in self.scenarios}
            toplow_pt_    = {s: [] for s in self.scenarios}
            toplow_mass_  = {s: [] for s in self.scenarios}
        #low pt top loop
        for idx_j0 in range(ngoodjets):
            for idx_j1 in range(idx_j0):
                for idx_j2 in range(idx_j1):
                    j0, j1, j2 = goodjets[idx_j0], goodjets[idx_j1], goodjets[idx_j2]
                    top_p4 = lowpt_top(j0, j1, j2, s="nominal")
                    if top_p4.Pt()<pt_cut_low:
                        ntoplowpt+=1
                        toplow_idxjet0.append(idx_j0)
                        toplow_idxjet1.append(idx_j1)
                        toplow_idxjet2.append(idx_j2)
                        toplow_eta_.append(top_p4.Eta())
                        toplow_phi_.append(top_p4.Phi())
                        for scenario in self.scenarios:
                            top_p4 = lowpt_top(j0, j1, j2, s= scenario)
                            toplow_pt_[scenario].append(top_p4.Pt())
                            toplow_mass_[scenario].append(top_p4.M())
                        if self.isMC:
                            toplow_truth.append(truth(j0=j0, j1=j1, j2=j2))
                        else:
                            toplow_truth.append(0)
        
        for idx_j0 in range(ngoodjets):
                for idx_j1 in range(idx_j0):
                    for idx_fj in range(ngoodfatjets):
                        j0, j1 = goodjets[idx_j0],goodjets[idx_j1]
                        fj = goodfatjets[idx_fj]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=None, fj=fj, s="nominal")
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(idx_fj)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(-1)
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            for scenario in self.scenarios:
                                top_p4 = highpt_top(j0=j0, j1=j1, j2=None, fj=fj, s=scenario)
                                tophigh_pt_[scenario].append(top_p4.Pt())
                                tophigh_mass_[scenario].append(top_p4.M())
                            if self.isMC:
                                tophigh_truth.append(truth(j0=j0, j1=j1, fj=fj))
                            else:
                                tophigh_truth.append(0)
                    for idx_j2 in range(idx_j1):
                        j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=None, s="nominal")
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(-1)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(idx_j2)
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            for scenario in self.scenarios:
                                top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=None, s = scenario)
                                tophigh_pt_[scenario].append(top_p4.Pt())
                                tophigh_mass_[scenario].append(top_p4.M())
                            if self.isMC:
                                tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2))
                            else:
                                tophigh_truth.append(0)
                        for idx_fj in range(ngoodfatjets):
                            j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                            fj = goodfatjets[idx_fj]
                            top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=fj, s = "nominal")
                            if top_p4.Pt()>pt_cut_high:
                                ntophighpt += 1
                                tophigh_idxfatjet.append(idx_fj)
                                tophigh_idxjet0.append(idx_j0)
                                tophigh_idxjet1.append(idx_j1)
                                tophigh_idxjet2.append(idx_j2)
                                tophigh_eta_.append(top_p4.Eta())
                                tophigh_phi_.append(top_p4.Phi())
                                for scenario in self.scenarios:
                                    top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=fj, s = scenario)
                                    tophigh_pt_[scenario].append(top_p4.Pt())
                                    tophigh_mass_[scenario].append(top_p4.M())
                                if self.isMC:
                                    tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2, fj=fj))
                                else: 
                                    tophigh_truth.append(0)
        
        self.out.fillBranch("nTopResolved", ntoplowpt)
        self.out.fillBranch("TopResolved_idxJet0", toplow_idxjet0)
        self.out.fillBranch("TopResolved_idxJet1", toplow_idxjet1)
        self.out.fillBranch("TopResolved_idxJet2", toplow_idxjet2)
        self.out.fillBranch("TopResolved_eta", toplow_eta_)
        self.out.fillBranch("TopResolved_phi", toplow_phi_)
        self.out.fillBranch("TopResolved_truth", toplow_truth)
        self.out.fillBranch("nTopMixed", ntophighpt)
        self.out.fillBranch("TopMixed_idxFatJet", tophigh_idxfatjet)
        self.out.fillBranch("TopMixed_idxJet0", tophigh_idxjet0)
        self.out.fillBranch("TopMixed_idxJet1", tophigh_idxjet1)
        self.out.fillBranch("TopMixed_idxJet2", tophigh_idxjet2)
        self.out.fillBranch("TopMixed_eta", tophigh_eta_)
        self.out.fillBranch("TopMixed_phi", tophigh_phi_)
        self.out.fillBranch("TopMixed_truth", tophigh_truth)
        for scenario in self.scenarios:
            self.out.fillBranch("TopResolved_pt_"+scenario, toplow_pt_[scenario])
            self.out.fillBranch("TopResolved_mass_"+scenario, toplow_mass_[scenario])
            self.out.fillBranch("TopMixed_pt_"+scenario, tophigh_pt_[scenario])
            self.out.fillBranch("TopMixed_mass_"+scenario, tophigh_mass_[scenario])

        # t1 = datetime.now()
        # print("TopCandidate module time :", t1-t0)  
        return True

