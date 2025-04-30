import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np
from array import array

def matchingGenJetGenPart(genpart, genjet):
    # GenPart_genPartIdxMother_prompt è diversa da -1 solo per i quark e le W
    # quindi basta distinguere il b proveniente dal top hadronic

    # funziona per tt semilep da modificare se c'è più di 1 top hadr

    b  = None
    q  = None
    q_ = None
    sign_w = 0

    for part in genpart:
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
            if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
                sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
                if(q==None): q = part
                elif(q_==None): q_ = part
                else: continue
    for part in genpart:
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
            if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
                b = part       
    
    if (b!=None and q!=None and q_!=None): 
        bjet, drb    = closest(b, genjet)
        qjet, drq    = closest(q, genjet)
        q_jet, drq_  = closest(q_, genjet)
    else:
        bjet, qjet, q_jet = None, None, None

    if(drb<0.4 and drq<0.4 and drq_<0.4):
        return [bjet, qjet, q_jet]
    else:
        return [None, None, None]

def matchingGenJetGenTop(gentop, matchedGenJet_wGenPart):
    # if len(gentop)==1:  top = gentop[0] # sempre vero per tt semilep
    match = False
    recoTop = matchedGenJet_wGenPart[0].p4() + matchedGenJet_wGenPart[1].p4() + matchedGenJet_wGenPart[2].p4()
    # controllare questa somma
    dRGenTopRecoTop = deltaR(gentop[0].eta, gentop[0].phi, recoTop.Eta(), recoTop.Phi()) 
    if(dRGenTopRecoTop<0.4): match = True
    return match, dRGenTopRecoTop

file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/TT_semilep_2018/20240731_214516/tree_hadd_755.root"
chain = ROOT.TChain('Events')
chain.Add(file)
tree = InputTree(chain)

outfile = ROOT.TFile("output_GenJetGenTopMatchStudy_ttsemilep_noResinMix.root","RECREATE")

h_gentop_pt              = ROOT.TH1D("h_gentop_pt","; genTop pT", 30, 0, 1000)
h_genjet_pt              = ROOT.TH1D("h_genjet_pt","; genJet pT", 30, 0, 1000)
h2_gentopgenminjet_pt       = ROOT.TH2D("h2_gentopgenminjet_pt", "genTop matched min pt genJet; genTop pT; genJet pT", 20, 0, 1000, 50, 0, 1000)
h2_gentopgenmidjet_pt       = ROOT.TH2D("h2_gentopgenmidjet_pt", "genTop matched mid pt genJet; genTop pT; genJet pT", 20, 0, 1000, 50, 0, 1000)
h2_gentopgenmaxjet_pt       = ROOT.TH2D("h2_gentopgenmaxjet_pt", "genTop matched max pt genJet; genTop pT; genJet pT", 20, 0, 1000, 50, 0, 1000)
h_gentop_pt_excluded   = ROOT.TH1D("h_gentop_pt_excluded","Top where genjet are not matched with quark (at least 1); genTop pT", 20, 0, 1000)
h_gentop_pt_notmathced   = ROOT.TH1D("h_gentop_pt_notmatched","Top not matched; genTop pT", 20, 0, 1000)
h_gentop_pt_mathced   = ROOT.TH1D("h_gentop_pt_matched","Top matched; genTop pT", 20, 0, 1000)
h_genJet_minpt_notmathced   = ROOT.TH1D("h_genJet_minpt_notmatched","min pT genJet not matched; genJet pT", 30, 0, 1000)
h_genJet_midpt_notmathced   = ROOT.TH1D("h_genJet_midpt_notmatched","mid pT genJet not matched; genJet pT", 30, 0, 1000)
h_genJet_maxpt_notmathced   = ROOT.TH1D("h_genJet_maxpt_notmatched","max pT genJet not matched; genJet pT", 30, 0, 1000)
h_dRGenTopGenJetsum   = ROOT.TH1D("h_dRGenTopGenJetsum","#DeltaR GenTop GenJet_sum; #Delta R", 20, 0, 2)
h_dRGenTopGenJetsumgentoppt   = ROOT.TH2D("h_dRGenTopGenJetsumGentoppt","#DeltaR GenTop GenJet_sum Vs genTop pt; #Delta R; genTop pT", 20, 0, 2, 30, 0, 1000)
h_dRGenTopGenJetsumgenjetminpt   = ROOT.TH2D("h_dRGenTopGenJetsumGenjetminpt","#DeltaR GenTop GenJet_sum Vs genJet min pt; #Delta R; genJet pT", 20, 0, 2, 30, 0, 1000)
h_dRGenTopGenJetsumgenjetmaxpt   = ROOT.TH2D("h_dRGenTopGenJetsumGenjetmaxpt","#DeltaR GenTop GenJet_sum Vs genJet max pt; #Delta R; genJet pT", 20, 0, 2, 30, 0, 1000)

# test addizionali
h_dRGenTopGen2Jetsum   = ROOT.TH1D("h_dRGenTopGen2Jetsum","#DeltaR GenTop GenJet_sum; #Delta R", 20, 0, 2)
h_deltaetadeltaphi     = ROOT.TH2D("h_deltaetadeltaphi", "delta eta delta phi jetsum gentop; deltaEta; deltaPhi", 18, -6, 6, 18, -3.14, 3.14)

nEvGenJetGenQuarkNotMatched = 0
nEvGenJetSumGenTopNotMatched = 0
nEvGenJetMinptl25 = 0
for i in range(tree.GetEntries()):
# for i in range(1000):
    event   = Event(tree,i)
    gentop  = Collection(event, "TopGenTopPart", lenVar = "nTopGenHadr")
    genjet  = Collection(event, "GenJet")
    genpart = Collection(event, "GenPart")

    nTopGenHadr = len(gentop)
    nGenJet     = len(genjet)
    nGenPart    = len(genpart)

    matchedGenJet_wGenPart = matchingGenJetGenPart(genpart, genjet)
    # print(matchedGenJet_wGenPart)
    if matchedGenJet_wGenPart[0]!= None:
        flag_matchedGenJet_wGenTop, dRGenTopGenJetsum  = matchingGenJetGenTop(gentop, matchedGenJet_wGenPart)
        h_dRGenTopGenJetsum.Fill(dRGenTopGenJetsum)
        genjetspt = [j.pt for j in matchedGenJet_wGenPart]
        h_dRGenTopGenJetsumgentoppt.Fill(dRGenTopGenJetsum, gentop[0].pt)
        h_dRGenTopGenJetsumgenjetminpt.Fill(dRGenTopGenJetsum, min(genjetspt))
        h_dRGenTopGenJetsumgenjetmaxpt.Fill(dRGenTopGenJetsum, max(genjetspt))
        if min(genjetspt)<25: nEvGenJetMinptl25+=1
        # test addizionali
        # DeltaR (jet1+jet2, top) jet ordine di pt decr
        # plot 2D (deltaEta, deltaPhi) tra gentop e somma genjet
        idxsorted=  sorted(range(len(genjetspt)), key=lambda i: genjetspt[i], reverse=True)
        genjet1 = matchedGenJet_wGenPart[idxsorted[0]]
        genjet2 = matchedGenJet_wGenPart[idxsorted[1]]
        # if(not flag_matchedGenJet_wGenTop):
        h_dRGenTopGen2Jetsum.Fill(deltaR(gentop[0].eta, gentop[0].phi, (genjet1.p4()+genjet2.p4()).Phi(), (genjet1.p4()+genjet2.p4()).Eta()))

        recoTop = matchedGenJet_wGenPart[0].p4() + matchedGenJet_wGenPart[1].p4() + matchedGenJet_wGenPart[2].p4()
        h_deltaetadeltaphi.Fill(deltaEta(gentop[0].eta, recoTop.Eta()), deltaPhi(gentop[0].phi, recoTop.Phi())) 


        for jet in matchedGenJet_wGenPart:
            h_genjet_pt.Fill(jet.pt)
        for top in gentop:
            h_gentop_pt.Fill(top.pt)

        top = gentop[0]
        if flag_matchedGenJet_wGenTop:
            # genjetspt = [j.pt for j in matchedGenJet_wGenPart]
            h2_gentopgenminjet_pt.Fill(top.pt, min(genjetspt))
            h2_gentopgenmidjet_pt.Fill(top.pt, genjetspt[idxsorted[1]])
            h2_gentopgenmaxjet_pt.Fill(top.pt, max(genjetspt))
            h_gentop_pt_mathced.Fill(top.pt)
        else:
            # aggiugni divisione in top con 1 e 2 match --> prova anche ad allargare il dr
            nEvGenJetSumGenTopNotMatched+=1
            h_gentop_pt_notmathced.Fill(top.pt)
            genjetspt = [j.pt for j in matchedGenJet_wGenPart]
            h_genJet_minpt_notmathced.Fill(min(genjetspt))
            h_genJet_midpt_notmathced.Fill(genjetspt[idxsorted[1]])
            h_genJet_maxpt_notmathced.Fill(max(genjetspt))

    else: 
        h_gentop_pt_excluded.Fill(gentop[0].pt)
        nEvGenJetGenQuarkNotMatched+=1
    
outfile.cd()
h_gentop_pt.Write()
h_genjet_pt.Write()
h2_gentopgenminjet_pt.Write()
h2_gentopgenmidjet_pt.Write()
h2_gentopgenmaxjet_pt.Write()
h_gentop_pt_notmathced.Write()
h_genJet_minpt_notmathced.Write()
h_genJet_midpt_notmathced.Write()
h_genJet_maxpt_notmathced.Write()
h_dRGenTopGenJetsum.Write()
h_dRGenTopGenJetsumgentoppt.Write()
h_dRGenTopGenJetsumgenjetminpt.Write()
h_dRGenTopGenJetsumgenjetmaxpt.Write()
h_gentop_pt_mathced.Write()
h_gentop_pt_excluded.Write()

# additional plot
h_dRGenTopGen2Jetsum.Write()
h_deltaetadeltaphi.Write()

outfile.Close()

print("Fraction of Events where at least 1 genquark is not matched with a genjet: %.4f" %(nEvGenJetGenQuarkNotMatched/tree.GetEntries()))
print("Fraction of Events where gentop is not matched with the genjet sum: %.4f" %(nEvGenJetSumGenTopNotMatched/tree.GetEntries()))
print("Fraction of Events with gentop matched with genJet sum where min genJet pt < 25: %.4f" %(nEvGenJetMinptl25/tree.GetEntries()))

# Fraction of Events where at least 1 genquark is not matched with a genjet: 0.13580660613000511
# Fraction of Events where gentop is not matched with the genjet sum: 0.8004777695317077