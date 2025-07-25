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


def matching(genpart, gen, jet, sgn_top, dR = 0.4):
    b       = sgn_top*5
    w       = sgn_top*24
    sgn_u   = sgn_top
    sgn_d   = -sgn_top
    match   = False
    jet_out = None

    # Matching della b proveniente da un top con un jet/fatjet
    if (gen.pdgId == b and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == sgn_top*6):
        #print('b quark cand ', gen.pdgId)
        j, dr =  closest_(gen, jet)
        if dr < dR:
            #print('found match b quark', j)
            jet_out = j
            match   = True
    # Matching di un u/c proveniente da una W proveniente dal top con un jet/fatjet      
    elif (gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId) == sgn_u and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un top 
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('u quark cand', gen.pdgId)
            j, dr = closest_(gen, jet)
            if dr < dR:
                #print('found match up quark', j)
                jet_out = j
                match   = True
    # Matching di un d/s proveniente da una W proveniente dal top con un jet/fatjet            
    elif (gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId) == sgn_d and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un to
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('d quark cand')
            j, dr =  closest_(gen, jet)
            if dr < dR:
                #print('found match down quark', j)
                jet_out = j
                match = True
    return match, jet_out

def hadronicTop(genpart, i):
    for gen in genpart:
        if gen.genPartIdxMother_prompt > -1 and abs(genpart[gen.genPartIdxMother_prompt].pdgId) == 24 and genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt == i and abs(gen.pdgId) <5 and abs(gen.pdgId) > 0:
            return True
        elif gen.genPartIdxMother_prompt > -1 and abs(genpart[gen.genPartIdxMother_prompt].pdgId) == 24 and genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt == i and abs(gen.pdgId) >5 :
            return False
    # return False

class nanoprepro(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        # "branches TopGenLevel"
        self.out.branch("nTopGenHadr", "I")
        self.out.branch("TopGenTopPart_pt", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenTopPart_eta", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenTopPart_phi", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenTopPart_mass", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_pt", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_eta", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_phi", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_mass", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_idxGenPartproduct0", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_idxGenPartproduct1", "F", lenVar="nTopGenHadr")
        self.out.branch("TopGenProductsSum_idxGenPartproduct2", "F", lenVar="nTopGenHadr")
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("Jet_matched",      "F", lenVar="nJet")    # 0,1,2,3
        self.out.branch("Jet_pdgId",        "F", lenVar="nJet")    # quark flav 
        self.out.branch("Jet_topMother",    "F", lenVar="nJet")
        self.out.branch("FatJet_matched",   "F", lenVar="nFatJet") # 0,1,2,3
        self.out.branch("FatJet_pdgId",     "F", lenVar="nFatJet") # quark flav
        self.out.branch("FatJet_topMother", "F", lenVar="nFatJet")

    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"Jet")
        Njets      = len(jets)
        fatjets    = Collection(event,"FatJet")
        Nfatjets   = len(fatjets)
        muons      = Collection(event, "Muon")
        electrons  = Collection(event, "Electron")
        if self.isMC==1:
            #LHE     = Collection(event, "LHEPart")
            genpart = Collection(event, "GenPart")
        '''init variables to branch'''
        #jets_deltar = []
        #ind_fatjets = []
        #ind_jets    = []
        jets_pdgId        = np.zeros(Njets)
        jets_matched      = np.zeros(Njets)
        jets_topMother    = np.zeros(Njets)
        fatjets_pdgId     = np.zeros(Nfatjets)
        fatjets_matched   = np.zeros(Nfatjets)
        fatjets_topMother = np.zeros(Nfatjets)
        fatjets_truth = np.zeros(Nfatjets)
        if self.isMC==1:
            ntop    = 0
            sgn_top = 0
            for gen in genpart:
                # Trova i top nei tDM e TTbar
                if (gen.genPartIdxMother_prompt == -1 and abs(gen.pdgId)==6):
                    if (gen.genPartIdxMother == 0):
                        ntop   += 1
                        sgn_top = gen.pdgId/abs(gen.pdgId)
                # Trova i top nei Tprime
                elif (gen.genPartIdxMother_prompt != -1 and abs(gen.pdgId)==6):
                    if ((gen.genPartIdxMother == 0 or abs(genpart[gen.genPartIdxMother_prompt].pdgId) == 8000001)):
                        ntop   += 1
                        sgn_top = gen.pdgId/abs(gen.pdgId)
            #print('# top ',ntop)
            #print(' top sgn ', sgn_top)
            if ntop == 1:
                uquark_matched   = False
                dquark_matched   = False 
                bquark_matched   = False 
                uquarkFJ_matched = False
                dquarkFJ_matched = False 
                bquarkFJ_matched = False 
            elif ntop == 2:
                b_matched        = False
                u_matched        = False
                dbar_matched     = False
                bbar_matched     = False                    
                d_matched        = False
                ubar_matched     = False
                bFJ_matched      = False
                uFJ_matched      = False
                dbarFJ_matched   = False
                bbarFJ_matched   = False                    
                dFJ_matched      = False
                ubarFJ_matched   = False
            for gen in genpart:
                tosave = False
                if ntop == 1:
                    match, j = matching(genpart, gen, jets, sgn_top)
                    #if match: print("jet matched ", match, gen.pdgId, j, sgn_top)
                elif ntop ==2:
                    match, j = matching(genpart, gen, jets, +1)
                    #print('top +6 :', match, j)
                    sgn_top = 1
                    if not match:
                        match, j = matching(genpart, gen, jets, -1)
                        sgn_top = -1
                        #print('top -6 :', match, j)
                else: match = False
                #print("genpart (b,u,d)", bquark_matched, uquark_matched, dquark_matched)
                #print(match)
                if (match and ntop == 1 and not (bquark_matched*uquark_matched*dquark_matched)):
                    #print("genpart matched (b,u,d)", bquark_matched, uquark_matched, dquark_matched)
                    if (not bquark_matched and gen.pdgId==sgn_top*5) :
                        #print('b quark matched')
                        bquark_matched = True
                        tosave = True
                    elif (not uquark_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                        #print('u quark matched')
                        uquark_matched = True
                        tosave = True
                    elif (not dquark_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                        #print('d quark matched')
                        dquark_matched = True
                        tosave = True
                    if tosave:
                        #print("saving jet #", j, gen.pdgId)
                        if jets_topMother[j] == 0: 
                            jets_topMother[j] = sgn_top*6
                            jets_matched[j] += 1
                            if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                            elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                            elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                        elif jets_topMother[j] == sgn_top*6:
                            jets_matched[j] += 1
                            if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                            elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                            elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                            #ind_jets[j] = j

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
                            if jets_topMother[j] == 0:
                            #print "...saving jet pgd"
                                jets_topMother[j] = sgn_top*6
                                jets_matched[j] += 1
                                if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                            elif jets_topMother[j] == sgn_top*6:
                                jets_matched[j] += 1
                                if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                            #ind_jets[-1] = j
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
                        elif (not d_matched and gen.pdgId%2 != 0 and abs(gen.pdgId)!=5 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                            #print "   d matched"
                            d_matched = True
                            tosave = True
                        if tosave:
                            #print "...saving jet pgd"
                            if jets_topMother[j] == 0:
                                jets_topMother[j] = sgn_top*6
                                jets_matched[j]  += 1
                                #print(jets_matched[j])
                                if jets_matched[j]  ==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                            elif jets_topMother[j] == sgn_top*6:
                                jets_matched[j] += 1
                                if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                            #ind_jets[-1] = j

            for gen in genpart:
                tosave = False
                if ntop == 1:
                    match,j = matching(genpart, gen, fatjets, sgn_top, dR=0.8)
                elif ntop ==2:
                    match,j = matching(genpart, gen, fatjets, +1, dR=0.8)
                    sgn_top = 1
                    if not match:
                        match,j = matching(genpart, gen, fatjets, -1, dR=0.8)
                        sgn_top = -1
                else: match = False

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
                        if fatjets_topMother[j] == 0:
                            fatjets_topMother[j] = sgn_top*6
                            fatjets_matched[j] += 1
                            if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                            elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                            elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                        elif fatjets_topMother[j] == sgn_top*6:
                            fatjets_matched[j] += 1
                            if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                            elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                            elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100

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
                        elif (not dbarFJ_matched and gen.pdgId%2 != 0 and abs(gen.pdgId)!=5 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                            #print "   dbar matched"
                            dbarFJ_matched = True
                            tosave = True
                        if tosave :
                            #print "...saving jet pgd"
                            if fatjets_topMother[j] == 0:
                                fatjets_topMother[j] = sgn_top*6
                                fatjets_matched[j] += 1
                                if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                                elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                                elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                            elif fatjets_topMother[j] == sgn_top*6:
                                fatjets_matched[j] += 1
                                if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                                elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                                elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                        
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
                            if fatjets_topMother[j] == 0:
                                fatjets_topMother[j] = sgn_top*6
                                fatjets_matched[j] += 1
                                if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                                elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                                elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                            elif fatjets_topMother[j] == sgn_top*6:
                                fatjets_matched[j] += 1
                                if fatjets_matched[j]==1: fatjets_pdgId[j] = abs(gen.pdgId)
                                elif fatjets_matched[j]==2: fatjets_pdgId[j] += abs(gen.pdgId)*10
                                elif fatjets_matched[j]==3: fatjets_pdgId[j] += abs(gen.pdgId)*100
                            
                            
            # Filling TopGen branches
            topgenpt    = []
            topgeneta   = []
            topgenphi   = []
            topgenmass  = []
            topgenidx   = []
            ntopgenhadr = 0
            for i, gen in enumerate(genpart):
                if abs(gen.pdgId)==6 and (gen.statusFlags & (1<<13)): # statusFlag &(1<<13) serve per richiedere che sia la last copy di quell'oggetto
                    if hadronicTop(genpart, i):
                        topgenidx.append(i)
                        ntopgenhadr += 1
                        topgenpt.append(gen.pt)
                        topgeneta.append(gen.eta)
                        topgenphi.append(gen.phi)
                        topgenmass.append(gen.mass)
                        # print("topgenmass ", ntopgenhadr, topgenmass)
            # la massa della somma viene molto diversa da quella calcolata sopra
            # ma i valori sembrano sensati
            topgensumpt     = []
            topgensumeta    = []
            topgensumphi    = []
            topgensumm      = []
            topgenproduct0  = []
            topgenproduct1  = []
            topgenproduct2  = []
            # print("topgenidx ", ntopgenhadr, topgenidx)
            bmomentum, q1momentum, q2momentum = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
            for top in topgenidx:
                flag1, flag2, flag3 = False, False, False
                for i, gen in enumerate(genpart):
                    if gen.genPartIdxMother_prompt > -1:
                        if gen.genPartIdxMother_prompt == top and abs(gen.pdgId)==5 and bool(gen.statusFlags & (1<<13)):
                            # print("trovato b ", gen.pdgId, genpart[gen.genPartIdxMother_prompt].pdgId )
                            flag1 = True
                            bmomentum.SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                            topgenproduct0.append(i)
                        if genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt == top and abs(gen.pdgId)<5 and abs(gen.pdgId)%2==0 and bool(gen.statusFlags & (1<<13)):
                            # print("trovato q1", gen.pdgId, genpart[gen.genPartIdxMother_prompt].pdgId, genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)
                            flag2 = True
                            q1momentum.SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                            topgenproduct1.append(i)
                        if genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt == top and abs(gen.pdgId)<5 and abs(gen.pdgId)%2!=0 and bool(gen.statusFlags & (1<<13)):
                            # print("trovato q2", gen.pdgId, genpart[gen.genPartIdxMother_prompt].pdgId, genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)
                            flag3 = True
                            q2momentum.SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                            topgenproduct2.append(i)
                if flag1 and flag2 and flag3:
                    topmomentum = bmomentum + q1momentum + q2momentum
                    topgensumpt.append(topmomentum.Pt())
                    topgensumeta.append(topmomentum.Eta())
                    topgensumphi.append(topmomentum.Phi())
                    topgensumm.append(topmomentum.M())
                    # print("topgensum ", topgensumm)
                else:
                    topgensumpt.append(0)
                    topgensumeta.append(0)
                    topgensumphi.append(0)
                    topgensumm.append(0)
                    # print("Un top hadr non ha tutti i figli")
            # print(ntopgenhadr)
            self.out.fillBranch("nTopGenHadr", ntopgenhadr)
            self.out.fillBranch("TopGenTopPart_pt", topgenpt)
            self.out.fillBranch("TopGenTopPart_eta", topgeneta)
            self.out.fillBranch("TopGenTopPart_phi", topgenphi)
            self.out.fillBranch("TopGenTopPart_mass", topgenmass)
            self.out.fillBranch("TopGenProductsSum_pt", topgensumpt)
            self.out.fillBranch("TopGenProductsSum_eta", topgensumeta)
            self.out.fillBranch("TopGenProductsSum_phi", topgensumphi)
            self.out.fillBranch("TopGenProductsSum_mass", topgensumm)
            # self.out.fillBranch("TopGenProductsSum_idxGenPartproduct0", topgenproduct0)
            # self.out.fillBranch("TopGenProductsSum_idxGenPartproduct1", topgenproduct1)
            # self.out.fillBranch("TopGenProductsSum_idxGenPartproduct2", topgenproduct2)

            #self.out.fillBranch("Jet_deltaR", jets_deltar)
            #print(jets_topMother)

            self.out.fillBranch("Jet_matched", jets_matched)
            self.out.fillBranch("Jet_pdgId", jets_pdgId)
            self.out.fillBranch("Jet_topMother", jets_topMother)
            
            self.out.fillBranch("FatJet_matched", fatjets_matched)
            self.out.fillBranch("FatJet_pdgId", fatjets_pdgId)
            self.out.fillBranch("FatJet_topMother", fatjets_topMother)

        
        return True