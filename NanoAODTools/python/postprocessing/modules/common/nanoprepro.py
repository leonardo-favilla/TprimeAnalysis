import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *


def matching (genpart, gen, p_jet, sgn_top, dR = 0.4):
    
    b = sgn_top*5
    w = sgn_top*24
    sgn_u = sgn_top
    sgn_d = -sgn_top

    match = False
    p_gen = ROOT.TLorentzVector()
    p_gen.SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
    
    if( gen.pdgId==b and gen.genPartIdxMother_prompt>-1 
        and genpart[gen.genPartIdxMother_prompt].pdgId==sgn_top*6):
        if (deltaR(p_jet.Eta(), p_jet.Phi(),p_gen.Eta(), p_gen.Phi())<dR):
            match = True

    elif( gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_u and gen.genPartIdxMother_prompt>-1 
          and genpart[gen.genPartIdxMother_prompt].pdgId==w ):
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId==sgn_top*6):
            if deltaR(p_jet.Eta(), p_jet.Phi(),p_gen.Eta(), p_gen.Phi())<dR :
                match = True

    elif( gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==sgn_d and gen.genPartIdxMother_prompt>-1
          and genpart[gen.genPartIdxMother_prompt].pdgId==w ):
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId==sgn_top*6):
            if deltaR(p_jet.Eta(), p_jet.Phi(),p_gen.Eta(), p_gen.Phi())<dR :
                match = True
        
    return match

class nanoprepro(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        "branches TopGenLevel"
        self.out.branch("nTopGen", "I")
        self.out.branch("TopGenTopPart_pt", "F", lenVar="nTopGen")
        self.out.branch("TopGenTopPart_eta", "F", lenVar="nTopGen")
        self.out.branch("TopGenTopPart_phi", "F", lenVar="nTopGen")
        self.out.branch("TopGenTopPart_mass", "F", lenVar="nTopGen")
        self.out.branch("TopGenProductsSum_pt", "F", lenVar="nTopGen")
        self.out.branch("TopGenProductsSum_eta", "F", lenVar="nTopGen")
        self.out.branch("TopGenProductsSum_phi", "F", lenVar="nTopGen")
        self.out.branch("TopGenProductsSum_mass", "F", lenVar="nTopGen")

        "branch deltaR to Jet collection"
        self.out.branch("Jet_deltaR", "F", lenVar="nJet") 
        
        self.out.branch("Jet_matched", "F", lenVar="nJet") #0,1,2,3
        
        self.out.branch("Jet_pdgId","F", lenVar="nJet")   # quark flav 
        
        self.out.branch("Jet_topMother", "F", lenVar="nJet")
        
        self.out.branch("FatJet_matched", "F", lenVar="nFatJet")#0,1,2,3
        self.out.branch("FatJet_pdgId","F", lenVar="nFatJet") #quark falv
        self.out.branch("FatJet_topMother", "F", lenVar="nFatJet")

        "branch top variables"
        #self.out.branch("Top_indFatJet", "I", lenVar="1") # fatjet index wrt to tree list
        #self.out.branch("Top_indJet", "I", lenVar="3") # jets indices wrt to tree list

        "branch top candidates"
        #self.out.branch("nTop", "I", lenVar = "")


    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets = Collection(event,"Jet")
        Njets = len(jets)
        fatjets = Collection(event,"FatJet")
        Nfatjets = len(fatjets)
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")

        if self.isMC==1:
            LHE = Collection(event, "LHEPart")
            genpart = Collection(event, "GenPart")
        

        '''init variables to branch'''
        jets_deltar = []
        ind_fatjets = []
        ind_jets = []
        jets_pdgId = []
        jets_matched = []
        jets_topMother = []
        fatjets_pdgId = []
        fatjets_matched = []
        fatjets_topMother = []
        #lepton veto
        
        #looseEle = []
        #looseMu = []
        
        #looseMu = list(filter(lambda x : x.looseId and x.pt>30 , muons))
        #looseEle = list(filter(lambda x : x.mvaFall17V2noIso_WPL and x.pt>30, electrons))

        if self.isMC==1:

            #if (len(looseMu)>0 or len(looseEle)>0):# and met.pt>25:
            if False:#abs(LHE[1].pdgId)>6 and abs(LHE[2].pdgId)>6:
                return False
            else:
                #print flavquarks
                #print "NEW EVENT <----------------------------"

                p_jet = ROOT.TLorentzVector()
                p_gen = ROOT.TLorentzVector()

                ntop = 0
                sgn_top = 0

                for gen in genpart:
                    
                    if (gen.genPartIdxMother == 0 and abs(gen.pdgId)==6):
                        ntop +=1
                        sgn_top = gen.pdgId/abs(gen.pdgId)
                        
                
                if ntop ==1 :
                    uquark_matched = False
                    dquark_matched = False 
                    bquark_matched = False 

                    uquarkFJ_matched = False
                    dquarkFJ_matched = False 
                    bquarkFJ_matched = False 
                elif ntop ==2:
                    b_matched = False
                    u_matched = False
                    dbar_matched = False

                    bbar_matched = False                    
                    d_matched = False
                    ubar_matched = False
                    
                    bFJ_matched = False
                    uFJ_matched = False
                    dbarFJ_matched = False

                    bbarFJ_matched = False                    
                    dFJ_matched = False
                    ubarFJ_matched = False

                for j in range(Njets):
                    #print "new jet"
                    jets_topMother.append(0)
                    jets_pdgId.append(0)
                    jets_matched.append(0)
                    jets_deltar.append(0)

                    ind_jets.append(-1)
                    p_jet.SetPtEtaPhiM(jets[j].pt, jets[j].eta, jets[j].phi, jets[j].mass)
                            
                    for gen in genpart:
                        tosave = False
                        if ntop == 1:
                            match = matching(genpart, gen, p_jet, sgn_top)
                        if ntop ==2:
                            match = matching(genpart, gen, p_jet, +1)
                            sgn_top = 1
                            if not match:
                                match = matching(genpart, gen, p_jet, -1)
                                sgn_top = -1
                            
                        if (match and ntop == 1 and not (bquark_matched*uquark_matched*dquark_matched)):
                            if (not bquark_matched and gen.pdgId==sgn_top*5) : 
                                bquark_matched = True
                                tosave = True
                            elif (not uquark_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                                uquark_matched = True
                                tosave = True
                            elif (not dquark_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                                dquark_matched = True
                                tosave = True
                            if tosave:
                                jets_topMother[-1] = sgn_top*6
                                jets_matched[-1] += 1
                                if jets_matched[-1]==1: jets_pdgId[-1] = abs(gen.pdgId)
                                elif jets_matched[-1]==2: jets_pdgId[-1] += abs(gen.pdgId)*10
                                elif jets_matched[-1]==3: jets_pdgId[-1] += abs(gen.pdgId)*100
                                ind_jets[-1] = j

                        elif (match and ntop == 2):
                            #print  sgn_top
                            if(sgn_top == 1 and not b_matched*u_matched*dbar_matched):
                                #print "t"
                                if (not b_matched and gen.pdgId==sgn_top*5) :
                                    #print "   b matched"
                                    b_matched = True
                                    tosave = True
                                elif (not u_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                    #print "   u matched"
                                    u_matched = True
                                    tosave = True
                                elif (not dbar_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                    #print "   dbar matched"
                                    dbar_matched = True
                                    tosave = True
                                if tosave :
                                    #print "...saving jet pgd"
                                    jets_topMother[-1] = sgn_top*6
                                    jets_matched[-1] += 1
                                    if jets_matched[-1]==1: jets_pdgId[-1] = abs(gen.pdgId)
                                    elif jets_matched[-1]==2: jets_pdgId[-1] += abs(gen.pdgId)*10
                                    elif jets_matched[-1]==3: jets_pdgId[-1] += abs(gen.pdgId)*100
                                    ind_jets[-1] = j
                            elif(sgn_top == -1 and not bbar_matched*ubar_matched*d_matched):
                                #print "tbar"
                                if (not bbar_matched and gen.pdgId==sgn_top*5) :
                                    #print "   bbar matched"
                                    bbar_matched = True
                                    tosave = True
                                elif (not ubar_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                    #print "   ubar matched"
                                    ubar_matched = True
                                    tosave = True
                                elif (not d_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                    #print "   d matched"
                                    d_matched = True
                                    tosave = True
                                if tosave:
                                    #print "...saving jet pgd"
                                    jets_topMother[-1] = sgn_top*6
                                    jets_matched[-1] += 1
                                    if jets_matched[-1]==1: jets_pdgId[-1] = abs(gen.pdgId)
                                    elif jets_matched[-1]==2: jets_pdgId[-1] += abs(gen.pdgId)*10
                                    elif jets_matched[-1]==3: jets_pdgId[-1] += abs(gen.pdgId)*100
                                    ind_jets[-1] = j
                                 
                        delr = 10000
                        p_fj = ROOT.TLorentzVector()
                        for fj in fatjets:
                            p_fj.SetPtEtaPhiM(fj.pt, fj.eta, fj.phi, fj.mass)
                            if deltaR(p_jet.Eta(), p_jet.Phi(), p_fj.Eta(), p_fj.Phi())<delr: delr=deltaR(p_jet.Eta(), p_jet.Phi(), p_fj.Eta(), p_fj.Phi())#p_jet.Eta(), p_jet.Phi(),p_gen.Eta(), p_gen.Phi()
                        jets_deltar[-1] = delr

                for fj in range(Nfatjets):
                    #print "NEW FATJET ---------------"
                    fatjets_topMother.append(0)
                    fatjets_pdgId.append(0)
                    fatjets_matched.append(0)
                    ind_fatjets.append(-1)
                    
                    p_jet.SetPtEtaPhiM(fatjets[fj].pt, fatjets[fj].eta, fatjets[fj].phi, fatjets[fj].mass)
                    
                    for gen in genpart:
                        tosave = False
                        if ntop == 1:
                            match = matching(genpart, gen, p_jet, sgn_top, dR=0.8)
                        if ntop ==2:
                            match = matching(genpart, gen, p_jet, +1, dR=0.8)
                            sgn_top = 1
                            if not match:
                                match = matching(genpart, gen, p_jet, -1, dR=0.8)
                                sgn_top = -1
                            
                        if (match and ntop ==1 and 
                            not (bquarkFJ_matched*uquarkFJ_matched*dquarkFJ_matched)):
                  
                            if (not bquarkFJ_matched and gen.pdgId==sgn_top*5) : 
                                bquarkFJ_matched = True
                                tosave = True
                            elif (not uquarkFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                                uquarkFJ_matched = True
                                tosave = True
                            elif (not dquarkFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                                dquarkFJ_matched = True
                                tosave = True
                            if tosave:
                                fatjets_topMother[-1] = sgn_top*6
                                fatjets_matched[-1] += 1
                                if fatjets_matched[-1]==1: fatjets_pdgId[-1] = abs(gen.pdgId)
                                elif fatjets_matched[-1]==2: fatjets_pdgId[-1] += abs(gen.pdgId)*10
                                elif fatjets_matched[-1]==3: fatjets_pdgId[-1] += abs(gen.pdgId)*100
                                ind_fatjets[-1] = j

                        elif (match and ntop == 2):
                            #print  sgn_top
                            if(sgn_top == 1 and not bFJ_matched*uFJ_matched*dbarFJ_matched):
                                #print "t"
                                if (not bFJ_matched and gen.pdgId==sgn_top*5) :
                                    #print "   b matched"
                                    bFJ_matched = True
                                    tosave = True
                                elif (not uFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                    #print "   u matched"
                                    uFJ_matched = True
                                    tosave = True
                                elif (not dbarFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                    #print "   dbar matched"
                                    dbarFJ_matched = True
                                    tosave = True
                                if tosave :
                                    #print "...saving jet pgd"
                                    fatjets_topMother[-1] = sgn_top*6
                                    fatjets_matched[-1] += 1
                                    if fatjets_matched[-1]==1: fatjets_pdgId[-1] = abs(gen.pdgId)
                                    elif fatjets_matched[-1]==2: fatjets_pdgId[-1] += abs(gen.pdgId)*10
                                    elif fatjets_matched[-1]==3: fatjets_pdgId[-1] += abs(gen.pdgId)*100
                                    ind_fatjets[-1] = j
                            elif(sgn_top == -1 and not bbarFJ_matched*ubarFJ_matched*dFJ_matched):
                                #print "tbar"
                                if (not bbarFJ_matched and gen.pdgId==sgn_top*5) :
                                    #print "   bbar matched"
                                    bbarFJ_matched = True
                                    tosave = True
                                elif (not ubarFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                    #print "   ubar matched"
                                    ubarFJ_matched = True
                                    tosave = True
                                elif (not dFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                    #print "   d matched"
                                    dFJ_matched = True
                                    tosave = True
                                if tosave:
                                    #print "...saving jet pgd"
                                    fatjets_topMother[-1] = sgn_top*6
                                    fatjets_matched[-1] += 1
                                    if fatjets_matched[-1]==1: fatjets_pdgId[-1] = abs(gen.pdgId)
                                    elif fatjets_matched[-1]==2: fatjets_pdgId[-1] += abs(gen.pdgId)*10
                                    elif fatjets_matched[-1]==3: fatjets_pdgId[-1] += abs(gen.pdgId)*100
                                    ind_fatjets[-1] = j
                        '''if deltaR(p_jet, p_gen)<0.8:
                            if( abs(gen.pdgId)==5 and gen.genPartIdxMother_prompt>-1
                                and abs(genpart[gen.genPartIdxMother_prompt].pdgId)==6 and not bquark_matched):
                                #print "deltaR bquark-jet", deltaR(p_jet,p_gen)
                                #print "Bquark"
                                bquark_matched = True
                                fatjets_matched[-1] += 1
                                if fatjets_matched[-1] == 1: fatjets_pdgId[-1] = abs(gen.pdgId)
                                if fatjets_matched[-1] == 2: fatjets_pdgId[-1] += abs(gen.pdgId)*10
                                if fatjets_matched[-1] == 3: fatjets_pdgId[-1] += abs(gen.pdgId)*100

                                ind_fatjets[-1] = fj
                                #print "fatjet "+str(fj)+" matched with a bquark"

                            if( abs(gen.pdgId)>0 and abs(gen.pdgId)<6 and gen.genPartIdxMother_prompt>-1
                                and abs(genpart[gen.genPartIdxMother_prompt].pdgId)==24 and gen.pdgId!= wjet1quark_matched):
                                if (abs(genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6
                                    and gen.pdgId!=wjet2quark_matched) :
                                    
                                    fatjets_matched[-1] += 1
                                    if fatjets_matched[-1] == 1: fatjets_pdgId[-1] = abs(gen.pdgId)
                                    if fatjets_matched[-1] == 2: fatjets_pdgId[-1] += abs(gen.pdgId)*10
                                    if fatjets_matched[-1] == 3: fatjets_pdgId[-1] += abs(gen.pdgId)*100
                                    
                                    if wjet1quark_matched==0 : wjet1quark_matched=gen.pdgId
                                    elif wjet2quark_matched==0 : wjet2quark_matched=gen.pdgId
                                    ind_fatjets[-1] = fj
                                    #print "fatjet "+str(fj)+" matched with a wjet "+str(gen.pdgId)
                        '''
                # Filling TopGen branches
                topgenpt    = []
                topgeneta   = []
                topgenphi   = []
                topgenmass  = []
                topgenidx   = []
                for i, gen in enumerate(genpart):
                    if abs(gen.pdgId==6) and (gen.statusFlags & (1<<13)): # statusFlag &(1<<13) serve per richiedere che sia la last copy di quell'oggetto
                        if hadronicTop(genpart, i):
                            topgenidx.append(i)
                            ntop += 1
                            topgenpt.append(gen.pt)
                            topgeneta.append(gen.eta)
                            topgenphi.append(gen.phi)
                            topgenmass.append(gen.mass)

                for top in topgenidx:
                    for gen in genpart:
                        if gen.genPartIdxMother_prompt == top and abs(gen.pdgId)==5 and (gen.statusFlags & (1<<13)):
                            bmomentum = ROOT.TLorentzVector().SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                        if genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt == top and abs(gen.pdgId)<5 and abs(gen.pdgId)>0 and (gen.statusFlags & (1<<13)) and abs(gen.pdgId)%2==0:
                            q1momentum = ROOT.TLorentzVector().SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                        if genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt == top and abs(gen.pdgId)<5 and abs(gen.pdgId)>0 and (gen.statusFlags & (1<<13)) and abs(gen.pdgId)%2!=0:
                            q2momentum = ROOT.TLorentzVector().SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                    topmomentum = bmomentum + q1momentum + q2momentum


                self.out.fillBranch("nTopGen", ntop)
                self.out.fillBranch("TopGenTopPart_pt", topgenpt)
                self.out.fillBranch("TopGenTopPart_eta", topgeneta)
                self.out.fillBranch("TopGenTopPart_phi", topgenphi)
                self.out.fillBranch("TopGenTopPart_mass", topgenmass)                            

                self.out.fillBranch("Jet_deltaR", jets_deltar)
                self.out.fillBranch("Jet_matched", jets_matched)
                self.out.fillBranch("Jet_pdgId", jets_pdgId)
                self.out.fillBranch("Jet_topMother", jets_topMother)
                
                self.out.fillBranch("FatJet_matched", fatjets_matched)
                self.out.fillBranch("FatJet_pdgId", fatjets_pdgId)
                self.out.fillBranch("FatJet_topMother", fatjets_topMother)

                #self.out.fillBranch("Top_indFatJet", ind_fatjets) 
                #self.out.fillBranch("Top_indJet", ind_jets) 
            
                return True

