import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np
from array import array

def check_same_top(topmixed1, topmixed2, resolved = False):
    if not resolved:
        idx_fj_1, idx_j0_1, idx_j1_1, idx_j2_1 = topmixed1.idxFatJet, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_j0_2, idx_j1_2, idx_j2_2 = topmixed2.idxFatJet, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    else:
        idx_fj_1, idx_j0_1, idx_j1_1, idx_j2_1 = -1, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_j0_2, idx_j1_2, idx_j2_2 = -1, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    list_1 = [idx_j0_1, idx_j1_1, idx_j2_1]
    list_2 = [idx_j0_2, idx_j1_2, idx_j2_2]

    intersection = list(set(list_1) & set(list_2))
    check_jets = len(intersection) > 0
    check_fj = (idx_fj_1 == idx_fj_2) and (idx_fj_1 != -1 and idx_fj_2 != -1) 
    return check_jets or check_fj

def selectTop(topmixed, resolved = False):
    if len(topmixed) == 0: return []
    # print([top.TopScore for top in topmixed])
    topmixed_sorted = sorted(topmixed, key=lambda x: x.TopScore, reverse=True)
    # print("sorted ", [top.TopScore for top in topmixed_sorted])
    topselected = []
    for i, top in enumerate(topmixed_sorted):
        if(i==0):
            topselected.append(top)
        else:
            same_top = False
            for bestTop in topselected:
                same_top = check_same_top(top, bestTop, resolved = resolved)
                if same_top: break
            if not same_top:
                topselected.append(top)
    return topselected

def removeResolved(topmixed):
    if len(topmixed) == 0: return []
    topselected = []
    for top in topmixed:
        if top.idxFatJet != -1:
            topselected.append(top)
    return topselected


# file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/TT_hadr_2018/20240731_213554/tree_hadd_378.root"
# file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/Zprime4top_1000_2018/20240731_215745/tree_hadd_95.root"
# file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/Zprime4top_2000_2018/20240731_215917/tree_hadd_7.root"
# file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/Zprime4top_500_2018/20240731_215716/tree_hadd_23.root"
file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/TT_semilep_2018/20240731_214516/tree_hadd_755.root"
chain = ROOT.TChain('Events')
chain.Add(file)
tree = InputTree(chain)

outfile = ROOT.TFile("output_TopMatchingStudies_ttsemilep_noResinMix.root","RECREATE")
 
#  candidato true con il mindR rispetto al topgen --> per ogni top gen viene fillato il mindR tra i top mixed (quando c'è il true nell'evento)
# succede che una parte di questi sono a dr alto --> sono top matchati all'altro candidato probabilmente
# in generale sono minori di top totali perchè non tutti i top gen hanno un match
h_dr_mix = ROOT.TH1D("h_deltaRtopmixedtopgen_mindr",";#Delta R (topmixed,topgen)",100,0,3)
h_dr_res = ROOT.TH1D("h_deltaRtopresolvedtopgen_mindr",";#Delta R (topresolved,topgen)",100,0,3)

# top mass gen, top mass candidate dr<0.4, top mass candidate true (select si intende best score dentro 0.4) 
h_topmass_gen = ROOT.TH1D("h_topmassgen",";TopGen mass",50,0,500)

h_topmass_dr04_mix = ROOT.TH1D("h_topmassdr04mix",";TopMixed mass",50,0,500)
h_topmass_true_mix = ROOT.TH1D("h_topmasstruemix",";TopMixed mass",50,0,500)
h_topmass_selectLoose_mix = ROOT.TH1D("h_topmassselectLoosemix",";TopMixed mass",50,0,500)
h_topmass_selectMedium_mix = ROOT.TH1D("h_topmassselectMediummix",";TopMixed mass",50,0,500)
h_topmass_selectTight_mix = ROOT.TH1D("h_topmassselectTightmix",";TopMixed mass",50,0,500)

h_topmass_dr04_res = ROOT.TH1D("h_topmassdr04res",";TopResolved mass",50,0,500)
h_topmass_selectLoose_res = ROOT.TH1D("h_topmassselectLooseres",";TopResolved mass",50,0,500)
h_topmass_selectMedium_res = ROOT.TH1D("h_topmassselectMediumres",";TopResolved mass",50,0,500)
h_topmass_selectTight_res = ROOT.TH1D("h_topmassselectTightres",";TopResolved mass",50,0,500)
h_topmass_true_res = ROOT.TH1D("h_topmasstrueres",";TopResolveded mass",50,0,500)



h_topmass_dr04_mer = ROOT.TH1D("h_topmassdr04mer",";Top Merged mass",50,0,500)
h_topmass_selectLoose_mer = ROOT.TH1D("h_topmassselectLoosemer",";Top Merged mass",50,0,500)
h_topmass_selectMedium_mer = ROOT.TH1D("h_topmassselectMediummer",";Top Merged mass",50,0,500)
h_topmass_selectTight_mer = ROOT.TH1D("h_topmassselectTightmer",";Top Merged mass",50,0,500)
h_topmass_true_mer = ROOT.TH1D("h_topmasstruemer",";Top Mergeded mass",50,0,500)

h_topptreco_select_mix = ROOT.TH1D("h_topptrecoselectmix",";Top Mixed pt",20,0,1000)
h_topptreco_select_res = ROOT.TH1D("h_topptrecoselectres",";Top Resolved pt",20,0,1000)
h_topptreco_select_mer = ROOT.TH1D("h_topptrecoselectmer",";Top Resolved pt",20,0,1000)

h_toppt_gen         = ROOT.TH1D("h_topptgen",";Top Gen pt",20,0,1000)
h_toppt_dr04_mix    = ROOT.TH1D("h_topptdr04mix",";TopMixed pt",20,0,1000)
h_toppt_select_mix  = ROOT.TH1D("h_topptselectmix",";Top Gen pt",20,0,1000)
h_toppt_selectLoose_mix  = ROOT.TH1D("h_topptselectLoosemix",";TopMixed pt",20,0,1000)
h_toppt_selectMedium_mix  = ROOT.TH1D("h_topptselectMediummix",";TopMixed pt",20,0,1000)
h_toppt_selectTight_mix  = ROOT.TH1D("h_topptselectTightmix",";TopMixed pt",20,0,1000)
h_topptgen_selectLoose_mix  = ROOT.TH1D("h_topptgenselectLoosemix",";Top gen pt",20,0,1000)
h_topptgen_selectMedium_mix  = ROOT.TH1D("h_topptgenselectMediummix",";Top gen pt",20,0,1000)
h_topptgen_selectTight_mix  = ROOT.TH1D("h_topptgenselectTightmix",";Top gen pt",20,0,1000)
h_toppt_true_mix    = ROOT.TH1D("h_toppttruemix",";TopMixed pt",20,0,1000)

h_toppt_dr04_res    = ROOT.TH1D("h_topptdr04res",";Top Resolved pt",20,0,1000)
h_toppt_select_res  = ROOT.TH1D("h_topptselectres",";Top Gen pt",20,0,1000)
h_toppt_selectLoose_res  = ROOT.TH1D("h_topptselectLooseres",";Top Resolved pt",20,0,1000)
h_toppt_selectMedium_res  = ROOT.TH1D("h_topptselectMediumres",";Top Resolved pt",20,0,1000)
h_toppt_selectTight_res  = ROOT.TH1D("h_topptselectTightres",";Top Resolved pt",20,0,1000)
h_topptgen_selectLoose_res  = ROOT.TH1D("h_topptgenselectLooseres",";Top gen pt",20,0,1000)
h_topptgen_selectMedium_res  = ROOT.TH1D("h_topptgenselectMediumres",";Top gen pt",20,0,1000)
h_topptgen_selectTight_res  = ROOT.TH1D("h_topptgenselectTightres",";Top gen pt",20,0,1000)
h_toppt_true_res    = ROOT.TH1D("h_toppttrueres",";Top Resolved pt",20,0,1000)


h_toppt_dr04_mer    = ROOT.TH1D("h_topptdr04mer",";Top Merged pt",20,0,1000)
h_toppt_select_mer  = ROOT.TH1D("h_topptselectmer",";Top Gen pt",20,0,1000)
h_toppt_selectLoose_mer  = ROOT.TH1D("h_topptselectLoosemer",";Top Merged pt",20,0,1000)
h_toppt_selectMedium_mer  = ROOT.TH1D("h_topptselectMediummer",";Top Merged pt",20,0,1000)
h_toppt_selectTight_mer  = ROOT.TH1D("h_topptselectTightmer",";Top Merged pt",20,0,1000)
h_topptgen_selectLoose_mer  = ROOT.TH1D("h_topptgenselectLoosemer",";Top gen pt",20,0,1000)
h_topptgen_selectMedium_mer  = ROOT.TH1D("h_topptgenselectMediummer",";Top gen pt",20,0,1000)
h_topptgen_selectTight_mer  = ROOT.TH1D("h_topptgenselectTightmer",";Top gen pt",20,0,1000)
h_toppt_true_mer    = ROOT.TH1D("h_toppttruemer",";Top Merged pt",20,0,1000)


h_topgen_ptmass     = ROOT.TH2D("h_topgen_ptmass",";Top pt;Top mass",20,0,1000,50,0,500)
h_topmixedsel_ptmass     = ROOT.TH2D("h_topmixedsel_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmixedselLoose_ptmass     = ROOT.TH2D("h_topmixedselLoose_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmixedselMedium_ptmass     = ROOT.TH2D("h_topmixedselMedium_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmixedselTight_ptmass     = ROOT.TH2D("h_topmixedselTight_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmixeddr04_ptmass    = ROOT.TH2D("h_topmixeddr04_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmixedtrue_ptmass    = ROOT.TH2D("h_topmixedtrue_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topresolvedsel_ptmass     = ROOT.TH2D("h_topresolvedsel_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topresolvedselLoose_ptmass     = ROOT.TH2D("h_topresolvedselLoose_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topresolvedselMedium_ptmass     = ROOT.TH2D("h_topresolvedselMedium_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topresolvedselTight_ptmass     = ROOT.TH2D("h_topresolvedselTight_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topresolveddr04_ptmass    = ROOT.TH2D("h_topresolveddr04_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topresolvedtrue_ptmass    = ROOT.TH2D("h_topresolvedtrue_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)

h_topmergedsel_ptmass     = ROOT.TH2D("h_topmergedsel_ptmass",";Top merged pt;Top merged mass",20,0,1000,50,0,500)
h_topmergedselLoose_ptmass     = ROOT.TH2D("h_topmergedselLoose_ptmass",";Top merged pt;Top merged mass",20,0,1000,50,0,500)
h_topmergedselMedium_ptmass     = ROOT.TH2D("h_topmergedselMedium_ptmass",";Top merged pt;Top merged mass",20,0,1000,50,0,500)
h_topmergedselTight_ptmass     = ROOT.TH2D("h_topmergedselTight_ptmass",";Top merged pt;Top merged mass",20,0,1000,50,0,500)
h_topmergeddr04_ptmass    = ROOT.TH2D("h_topmergeddr04_ptmass",";Top merged pt;Top merged mass",20,0,1000,50,0,500)
h_topmergedtrue_ptmass    = ROOT.TH2D("h_topmergedtrue_ptmass",";Top merged pt;Top merged mass",20,0,1000,50,0,500)

# score dei candidati top mixed che hanno dr<0.4 e dr<0.8 rispetto al topgen (ci sono tutti i candidati senza nessun esclusione)
h_score_dr04_mix = ROOT.TH1D("h_topmixedscoredeltaR0p4",";TopMixed score #Delta R 0.4",40,0,1)
h_score_dr04_res = ROOT.TH1D("h_topresolvedscoredeltaR0p4",";TopResolved score #Delta R 0.4",40,0,1)
# distribuzione dR vs score per tutti i candidati topmixed
h_dr_score_mix   = ROOT.TH2D("h_deltaRtopmixedtopgenVsscore",";#Delta R (topmixed,topgen);TopMixed score",100,0,3,40,0,1)
h_dr_score_res   = ROOT.TH2D("h_deltaRtopresolvedtopgenVsscore",";#Delta R (topresolved,topgen);TopResolved score",100,0,3,40,0,1)
# distribuzione dR vs score tenendo solo il candidato più vicino in dR al topgen
h_dr_score_onextopgen_mix   = ROOT.TH2D("h_deltaRtopmixedtopgenVsscore_1pertogen",";#Delta R (topmixed,topgen);TopMixed score",100,0,3,40,0,1)
h_dr_score_onextopgen_res   = ROOT.TH2D("h_deltaRtopresolvedtopgenVsscore_1pertogen",";#Delta R (topresolved,topgen);TopResolved score",100,0,3,40,0,1)
# distribuzione degli score di tutti i candidati top mixed true per il matching definito da noi
h_score_true_mix = ROOT.TH1D("h_topmixedscoretrue",";TopMixed score",40,0,1)
h_score_true_res = ROOT.TH1D("h_topresolvedscoretrue",";TopResolved score",40,0,1)
h_score_true_mer = ROOT.TH1D("h_topmergedscoretrue",";TopMerged score",40,0,1)
# distribuzione degli score dei candidati top mixed che hanno dr<0.4 rispetto al topgen, per ogni top gen si prendono tutti i candidati indR<0.4 e si plotta lo score più alto tra questi
h_scores_mix = ROOT.TH1D("h_topmixedscore_bestcandMixXtopgen",";TopMixed score",500,0,1)
h_scores_res = ROOT.TH1D("h_topresolvedscore_bestcandResXtopgen",";TopResolved score",500,0,1)
h_scores_mer = ROOT.TH1D("h_topmergedscore_bestcandMerXtopgen",";TopMerged score",500,0,1)

# Top Reconstructed pt (dR and 3match)
h_highestscoretopmixedreco_pt              = ROOT.TH1D("h_highestscoretopmixedreco_pt",";TopMixed pt",20,0,1000)
h_highestscoretopresolvedreco_pt           = ROOT.TH1D("h_highestscoretopresolvedreco_pt",";TopResolved pt",20,0,1000)
h_highestscoretopmergedreco_pt             = ROOT.TH1D("h_highestscoretopmergedreco_pt",";Top Merged pt",20,0,1000)
h_highestscoretopmixedreco3match_pt        = ROOT.TH1D("h_highestscoretopmixedreco3match_pt",";TopMixed pt",20,0,1000)
h_highestscoretopresolvedreco3match_pt     = ROOT.TH1D("h_highestscoretopresolvedreco3match_pt",";TopResolved pt",20,0,1000)
h_highestscoretopmergedreco3match_pt       = ROOT.TH1D("h_highestscoretopmergedreco3match_pt",";Top Merged pt",20,0,1000)

# Top Reconstructed score (dR and 3match) --> PLOT per le ROC curve
h_highestscoretopmixedreco_score           = ROOT.TH1D("h_topmixedscore_HighestScoreMixXtopgen",";Top Mixed score",500,0,1)
h_highestscoretopresolvedreco_score        = ROOT.TH1D("h_topresolvedscore_HighestScoreMixXtopgen",";Top Resolved score",500,0,1)
h_highestscoretopmergedreco_score          = ROOT.TH1D("h_topmergedscore_HighestScoreMixXtopgen",";Top Merged score",500,0,1)
h_highestscoretopmixedreco3match_score     = ROOT.TH1D("h_topmixedscore_HighestScoreMixXtopgen3match",";Top Mixed score",500,0,1)
h_highestscoretopresolvedreco3match_score  = ROOT.TH1D("h_topresolvedscore_HighestScoreMixXtopgen3match",";Top Resolved score",500,0,1)
h_highestscoretopmergedreco3match_score    = ROOT.TH1D("h_topmergedscore_HighestScoreMixXtopgen3match",";Top Merged score",500,0,1)
#                 PLOT PER LE ROC A DIVERSI PT
h_highestscoretopmixedreco_scorePt         = ROOT.TH2D("h_topmixedscorePt_HighestScoreMixXtopgen",";Top Mixed score;Top Mixed pt",500,0,1, 4, array('d',[0,200,400,600,1000]))
h_highestscoretopresolvedreco_scorePt      = ROOT.TH2D("h_topresolvedscorePt_HighestScoreMixXtopgen",";Top Resolved score;Top Resolved pt",500,0,1, 4, array('d',[0,200,400,600,1000]))
h_highestscoretopmergedreco_scorePt        = ROOT.TH2D("h_topmergedscorePt_HighestScoreMixXtopgen",";Top Merged score;Top Merged pt",500,0,1, 4, array('d',[0,200,400,600,1000]))
h_highestscoretopmixedreco3match_scorePt   = ROOT.TH2D("h_topmixedscorePt_HighestScoreMixXtopgen3match",";Top Mixed score;Top Mixed pt",500,0,1, 4, array('d',[0,200,400,600,1000]))
h_highestscoretopresolvedreco3match_scorePt= ROOT.TH2D("h_topresolvedscorePt_HighestScoreMixXtopgen3match",";Top Resolved score;Top Resolved pt",500,0,1, 4, array('d',[0,200,400,600,1000]))
h_highestscoretopmergedreco3match_scorePt  = ROOT.TH2D("h_topmergedscorePt_HighestScoreMixXtopgen3match",";Top Merged score;Top Merged pt",500,0,1, 4, array('d',[0,200,400,600,1000]))

# Top Tagged variables only for pt gen ->(dR and 3match)
#   mixed
h_topmass_HighestScoreselectLoose_mix           = ROOT.TH1D("h_topmass_HighestScoreselectLoose_mix",";Top Mixed mass",50,0,500)
h_toppt_HighestScoreselectLoose_mix             = ROOT.TH1D("h_toppt_HighestScoreselectLoose_mix",";Top Mixed pt",20,0,1000)
h_topptgen_HighestScoreselectLoose_mix          = ROOT.TH1D("h_topptgen_HighestScoreselectLoose_mix",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectLoose_mix    = ROOT.TH1D("h_topptgen_HighestScore3matchselectLoose_mix",";Top Gen pt",20,0,1000)
h_topmixedselHighestScoreLoose_ptmass           = ROOT.TH2D("h_topmixedselHighestScoreLoose_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmass_HighestScoreselectMedium_mix          = ROOT.TH1D("h_topmass_HighestScoreselectMedium_mix",";Top Mixed mass",50,0,500)
h_toppt_HighestScoreselectMedium_mix            = ROOT.TH1D("h_toppt_HighestScoreselectMedium_mix",";Top Mixed pt",20,0,1000) 
h_topptgen_HighestScoreselectMedium_mix         = ROOT.TH1D("h_topptgen_HighestScoreselectMedium_mix",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectMedium_mix   = ROOT.TH1D("h_topptgen_HighestScore3matchselectMedium_mix",";Top Gen pt",20,0,1000)
h_topmixedselHighestScoreMedium_ptmass          = ROOT.TH2D("h_topmixedselHighestScoreMedium_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
h_topmass_HighestScoreselectTiht_mix            = ROOT.TH1D("h_topmass_HighestScoreselectTight_mix",";Top Mixed mass",50,0,500)
h_toppt_HighestScoreselectTight_mix             = ROOT.TH1D("h_toppt_HighestScoreselectTight_mix",";Top Mixed pt",20,0,1000)
h_topptgen_HighestScoreselectTight_mix          = ROOT.TH1D("h_topptgen_HighestScoreselectTight_mix",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectTight_mix    = ROOT.TH1D("h_topptgen_HighestScore3matchselectTight_mix",";Top Gen pt",20,0,1000)
h_topmixedselHighestScoreTight_ptmass           = ROOT.TH2D("h_topmixedselHighestScoreTight_ptmass",";Top Mixed pt;Top Mixed mass",20,0,1000,50,0,500)
#   resolved
h_topmass_HighestScoreselectLoose_res           = ROOT.TH1D("h_topmass_HighestScoreselectLoose_res",";Top Resolved mass",50,0,500)
h_toppt_HighestScoreselectLoose_res             = ROOT.TH1D("h_toppt_HighestScoreselectLoose_res",";Top Resolved pt",20,0,1000)
h_topptgen_HighestScoreselectLoose_res          = ROOT.TH1D("h_topptgen_HighestScoreselectLoose_res",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectLoose_res    = ROOT.TH1D("h_topptgen_HighestScore3matchselectLoose_res",";Top Gen pt",20,0,1000)
h_topresolvedselHighestScoreLoose_ptmass        = ROOT.TH2D("h_topresolvedselHighestScoreLoose_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topmass_HighestScoreselectMedium_res          = ROOT.TH1D("h_topmass_HighestScoreselectMedium_res",";Top Resolved mass",50,0,500)
h_toppt_HighestScoreselectMedium_res            = ROOT.TH1D("h_toppt_HighestScoreselectMedium_res",";Top Resolved pt",20,0,1000)
h_topptgen_HighestScoreselectMedium_res         = ROOT.TH1D("h_topptgen_HighestScoreselectMedium_res",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectMedium_res   = ROOT.TH1D("h_topptgen_HighestScore3matchselectMedium_res",";Top Gen pt",20,0,1000)
h_topresolvedselHighestScoreMedium_ptmass       = ROOT.TH2D("h_topresolvedselHighestScoreMedium_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
h_topmass_HighestScoreselectTight_res           = ROOT.TH1D("h_topmass_HighestScoreselectTight_res",";Top Resolved mass",50,0,500)
h_toppt_HighestScoreselectTight_res             = ROOT.TH1D("h_toppt_HighestScoreselectTight_res",";Top Resolved pt",20,0,1000)
h_topptgen_HighestScoreselectTight_res          = ROOT.TH1D("h_topptgen_HighestScoreselectTight_res",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectTight_res    = ROOT.TH1D("h_topptgen_HighestScore3matchselectTight_res",";Top Gen pt",20,0,1000)
h_topresolvedselHighestScoreTight_ptmass        = ROOT.TH2D("h_topresolvedselHighestScoreTight_ptmass",";Top Resolved pt;Top Resolved mass",20,0,1000,50,0,500)
#   merged
h_topmass_HighestScoreselectLoose_mer           = ROOT.TH1D("h_topmass_HighestScoreselectLoose_mer",";Top Merged mass",50,0,500)
h_toppt_HighestScoreselectLoose_mer             = ROOT.TH1D("h_toppt_HighestScoreselectLoose_mer",";Top Merged pt",20,0,1000)
h_topptgen_HighestScoreselectLoose_mer          = ROOT.TH1D("h_topptgen_HighestScoreselectLoose_mer",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectLoose_mer    = ROOT.TH1D("h_topptgen_HighestScore3matchselectLoose_mer",";Top Gen pt",20,0,1000)
h_topmergedselHighestScoreLoose_ptmass          = ROOT.TH2D("h_topmergedselHighestScoreLoose_ptmass",";Top Merged pt;Top Merged mass",20,0,1000,50,0,500)
h_topmass_HighestScoreselectMediunm_mer         = ROOT.TH1D("h_topmass_HighestScoreselectMedium_mer",";Top Merged mass",50,0,500)
h_toppt_HighestScoreselectMedium_mer            = ROOT.TH1D("h_toppt_HighestScoreselectMedium_mer",";Top Merged pt",20,0,1000)
h_topptgen_HighestScoreselectMedium_mer         = ROOT.TH1D("h_topptgen_HighestScoreselectMedium_mer",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectMedium_mer   = ROOT.TH1D("h_topptgen_HighestScore3matchselectMedium_mer",";Top Gen pt",20,0,1000)
h_topmergedselHighestScoreMedium_ptmass         = ROOT.TH2D("h_topmergedselHighestScoreMedium_ptmass",";Top Merged pt;Top Merged mass",20,0,1000,50,0,500)
h_topmass_HighestScoreselectTight_mer           = ROOT.TH1D("h_topmass_HighestScoreselectTight_mer",";Top Merged mass",50,0,500)
h_toppt_HighestScoreselectTight_mer             = ROOT.TH1D("h_toppt_HighestScoreselectTight_mer",";Top Merged pt",20,0,1000)
h_topptgen_HighestScoreselectTight_mer          = ROOT.TH1D("h_topptgen_HighestScoreselectTight_mer",";Top Gen pt",20,0,1000)
h_topptgen_HighestScore3matchselectTight_mer    = ROOT.TH1D("h_topptgen_HighestScore3matchselectTight_mer",";Top Gen pt",20,0,1000)
h_topmergedselHighestScoreTight_ptmass          = ROOT.TH2D("h_topmergedselHighestScoreTight_ptmass",";Top Merged pt;Top Merged mass",20,0,1000,50,0,500)

h_NtopgenrecoMixed      = ROOT.TH1D("h_NtopgenrecoMixed",";N top gen reco (Ntot= 4)",5,-0.5,4.5)
h_NtopgenrecoResolved   = ROOT.TH1D("h_NtopgenrecoResolved",";N top gen reco (Ntot=4)",5,-0.5,4.5)
h_NtopgenrecoMerged     = ROOT.TH1D("h_NtopgenrecoMerged",";N top gen reco (Ntot=4)",5,-0.5,4.5)

Top_threshold = {"Resolved" : {'WPloose': "0.24193972", 'WPmedium': "0.5411276", 'WPtight': "0.77197933"},
                 "Mixed"    :{'WPloose': "0.2957885265350342", 'WPmedium': "0.7584613561630249", 'WPtight': "0.9129540324211121"},
                 "Merged"   :{'WPloose': "0.79", 'WPmedium': "0.91", 'WPtight': "0.97"}}

for i in range(tree.GetEntries()):
# for i in range(10000):
    event = Event(tree,i)
    topgen = Collection(event, "TopGenTopPart", lenVar = "nTopGenHadr")
    nTopGenHadr = len(topgen)
    topresolved = Collection(event, "TopResolved")
    topmixed = Collection(event, "TopMixed")
    topmerged = Collection(event, "FatJet")

    topMixedSelect = selectTop(topmixed)
    topMixedSelect = removeResolved(topMixedSelect)
    topResolvedSelect = selectTop(topresolved, resolved = True)
    topMergedSelect = sorted(topmerged, key=lambda x: x.particleNet_TvsQCD, reverse=True)

    ntopMixReco = 0
    ntopMerReco = 0
    ntopResReco = 0

    for top in topgen:

        scores = []
        top_dr04 = []
        dr_max = 100
        dr_max_idx = -1
        h_topmass_gen.Fill(top.mass)
        h_toppt_gen.Fill(top.pt)
        h_topgen_ptmass.Fill(top.pt,top.mass)

        for i, t in enumerate(topMixedSelect):
            if deltaR(top, t)<0.4:
                ntopMixReco+=1
                h_highestscoretopmixedreco_pt.Fill(top.pt)
                h_highestscoretopmixedreco_score.Fill(t.TopScore)
                h_highestscoretopmixedreco_scorePt.Fill(t.TopScore, top.pt)
                if t.truth: 
                    h_highestscoretopmixedreco3match_score.Fill(t.TopScore)
                    h_highestscoretopmixedreco3match_pt.Fill(top.pt)
                    h_highestscoretopmixedreco3match_scorePt.Fill(t.TopScore, t.pt)
                if t.TopScore > float(Top_threshold['Mixed']['WPloose']):
                    h_topmass_HighestScoreselectLoose_mix.Fill(t.mass)
                    h_toppt_HighestScoreselectLoose_mix.Fill(t.pt)
                    h_topptgen_HighestScoreselectLoose_mix.Fill(top.pt)
                    h_topmixedselHighestScoreLoose_ptmass.Fill(t.pt, t.mass)
                    if t.truth : h_topptgen_HighestScore3matchselectLoose_mix.Fill(top.pt)
                if t.TopScore > float(Top_threshold['Mixed']['WPmedium']):
                    h_topmass_HighestScoreselectMedium_mix.Fill(t.mass)
                    h_toppt_HighestScoreselectMedium_mix.Fill(t.pt)
                    h_topptgen_HighestScoreselectMedium_mix.Fill(top.pt)
                    h_topmixedselHighestScoreMedium_ptmass.Fill(t.pt, t.mass)
                    if t.truth : h_topptgen_HighestScore3matchselectMedium_mix.Fill(top.pt)
                if t.TopScore > float(Top_threshold['Mixed']['WPtight']):
                    h_topmass_HighestScoreselectTiht_mix.Fill(t.mass)
                    h_toppt_HighestScoreselectTight_mix.Fill(t.pt)
                    h_topptgen_HighestScoreselectTight_mix.Fill(top.pt)
                    h_topmixedselHighestScoreTight_ptmass.Fill(t.pt, t.mass)
                    if t.truth : h_topptgen_HighestScore3matchselectTight_mix.Fill(top.pt)
             
        for i, t in enumerate(topResolvedSelect):
            if deltaR(top, t)<0.4:
                ntopResReco+=1
                h_highestscoretopresolvedreco_pt.Fill(top.pt)
                h_highestscoretopresolvedreco_score.Fill(t.TopScore)
                h_highestscoretopresolvedreco_scorePt.Fill(t.TopScore, top.pt)
                if t.truth: 
                    h_highestscoretopresolvedreco3match_score.Fill(t.TopScore)
                    h_highestscoretopresolvedreco3match_pt.Fill(top.pt)
                    h_highestscoretopresolvedreco3match_scorePt.Fill(t.TopScore, t.pt)
                if t.TopScore > float(Top_threshold['Resolved']['WPloose']):
                    h_topmass_HighestScoreselectLoose_res.Fill(t.mass)
                    h_toppt_HighestScoreselectLoose_res.Fill(t.pt)
                    h_topptgen_HighestScoreselectLoose_res.Fill(top.pt)
                    h_topresolvedselHighestScoreLoose_ptmass.Fill(t.pt, t.mass)
                    if t.truth : h_topptgen_HighestScore3matchselectLoose_res.Fill(top.pt)
                if t.TopScore > float(Top_threshold['Resolved']['WPmedium']):
                    h_topmass_HighestScoreselectMedium_res.Fill(t.mass)
                    h_toppt_HighestScoreselectMedium_res.Fill(t.pt)
                    h_topptgen_HighestScoreselectMedium_res.Fill(top.pt)
                    h_topresolvedselHighestScoreMedium_ptmass.Fill(t.pt, t.mass)
                    if t.truth : h_topptgen_HighestScore3matchselectMedium_res.Fill(top.pt)
                if t.TopScore > float(Top_threshold['Resolved']['WPtight']):
                    h_topmass_HighestScoreselectTight_res.Fill(t.mass)
                    h_toppt_HighestScoreselectTight_res.Fill(t.pt)
                    h_topptgen_HighestScoreselectTight_res.Fill(top.pt)
                    h_topresolvedselHighestScoreTight_ptmass.Fill(t.pt, t.mass)
                    if t.truth : h_topptgen_HighestScore3matchselectTight_res.Fill(top.pt)

        for i, t in enumerate(topMergedSelect):
            if deltaR(top, t)<0.4:
                ntopMerReco+=1
                h_highestscoretopmergedreco_pt.Fill(top.pt)
                h_highestscoretopmergedreco_score.Fill(t.particleNet_TvsQCD)
                h_highestscoretopmergedreco_scorePt.Fill(t.particleNet_TvsQCD, top.pt)
                if t.matched==3: 
                    h_highestscoretopmergedreco3match_pt.Fill(top.pt)
                    h_highestscoretopmergedreco3match_score.Fill(t.particleNet_TvsQCD)
                    h_highestscoretopmergedreco3match_scorePt.Fill(t.particleNet_TvsQCD, t.pt)
                if t.particleNet_TvsQCD > float(Top_threshold['Merged']['WPloose']):
                    h_topmass_HighestScoreselectLoose_mer.Fill(t.mass)
                    h_toppt_HighestScoreselectLoose_mer.Fill(t.pt)
                    h_topptgen_HighestScoreselectLoose_mer.Fill(top.pt)
                    h_topmergedselHighestScoreLoose_ptmass.Fill(t.pt, t.mass)
                    if t.matched==3 : h_topptgen_HighestScore3matchselectLoose_mer.Fill(top.pt)
                if t.particleNet_TvsQCD > float(Top_threshold['Merged']['WPmedium']):
                    h_topmass_HighestScoreselectMediunm_mer.Fill(t.mass)
                    h_toppt_HighestScoreselectMedium_mer.Fill(t.pt)
                    h_topptgen_HighestScoreselectMedium_mer.Fill(top.pt)
                    h_topmergedselHighestScoreMedium_ptmass.Fill(t.pt, t.mass)
                    if t.matched==3 : h_topptgen_HighestScore3matchselectMedium_mer.Fill(top.pt)
                if t.particleNet_TvsQCD > float(Top_threshold['Merged']['WPtight']):
                    h_topmass_HighestScoreselectTight_mer.Fill(t.mass)
                    h_toppt_HighestScoreselectTight_mer.Fill(t.pt)
                    h_topptgen_HighestScoreselectTight_mer.Fill(top.pt)
                    h_topmergedselHighestScoreTight_ptmass.Fill(t.pt, t.mass)
                    if t.matched==3 : h_topptgen_HighestScore3matchselectTight_mer.Fill(top.pt)
            
        for i, t in enumerate(topmerged):
            dr = deltaR(top.eta, top.phi, t.eta, t.phi)
            if dr <0.4 : 
                scores.append(t.particleNet_TvsQCD)
                top_dr04.append(i)
            # h_dr_score_mer.Fill(dr,t.TopScore)
            # if t.truth and dr < dr_max:
            #     dr_max = dr
            #     dr_max_idx = i
            # if dr < 0.4:
            #     h_topmass_dr04_mix.Fill(t.mass)
            #     h_toppt_dr04_mix.Fill(t.pt)
            #     h_score_dr04_mix.Fill(t.TopScore)
            #     h_topmixeddr04_ptmass.Fill(t.pt, t.mass)

        # if dr_max<100:
        #     h_dr_mix.Fill(dr_max)
        #     h_dr_score_onextopgen_mix.Fill(dr_max,topmixed[dr_max_idx].TopScore)
        if len(scores) == 0: 
            continue
        else:
            scores = np.array(scores)
            h_scores_mer.Fill(max(scores))
            idx = top_dr04[int(np.argmax(scores))]
            # print(scores, max(scores), int(np.argmax(scores)))
            h_toppt_select_mer.Fill(top.pt)
            h_topptreco_select_mer.Fill(topmerged[idx].pt)
            h_topmergedsel_ptmass.Fill(topmerged[idx].pt, topmerged[idx].mass)
            if max(scores) > float(Top_threshold['Merged']['WPloose']):
                h_toppt_selectLoose_mer.Fill(topmerged[idx].pt)
                h_topptgen_selectLoose_mer.Fill(top.pt)
                h_topmass_selectLoose_mer.Fill(topmerged[idx].mass)
                h_topmergedselLoose_ptmass.Fill(topmerged[idx].pt,topmerged[idx].mass)
            if max(scores) > float(Top_threshold['Merged']['WPmedium']):
                h_toppt_selectMedium_mer.Fill(topmerged[idx].pt)
                h_topptgen_selectMedium_mer.Fill(top.pt)
                h_topmass_selectMedium_mer.Fill(topmerged[idx].mass)
                h_topmergedselMedium_ptmass.Fill(topmerged[idx].pt,topmerged[idx].mass)
            if max(scores) > float(Top_threshold['Merged']['WPtight']):
                h_toppt_selectTight_mer.Fill(topmerged[idx].pt)
                h_topptgen_selectTight_mer.Fill(top.pt)
                h_topmass_selectTight_mer.Fill(topmerged[idx].mass)
                h_topmergedselTight_ptmass.Fill(topmerged[idx].pt,topmerged[idx].mass)
            if topmerged[idx].matched==3:
                h_topmass_true_mer.Fill(topmerged[idx].mass)
                h_toppt_true_mer.Fill(topmerged[idx].pt)
                h_score_true_mer.Fill(topmerged[idx].particleNet_TvsQCD)
                h_topmergedtrue_ptmass.Fill(topmerged[idx].pt, topmerged[idx].mass)

        scores = []
        top_dr04 = []
        dr_max = 100
        dr_max_idx = -1
        for i, t in enumerate(topmixed):
            dr = deltaR(top.eta, top.phi, t.eta, t.phi)
            if dr <0.4 : 
                scores.append(t.TopScore)
                top_dr04.append(i)
            h_dr_score_mix.Fill(dr,t.TopScore)
            if t.truth and dr < dr_max:
                dr_max = dr
                dr_max_idx = i
            if dr < 0.4:
                h_topmass_dr04_mix.Fill(t.mass)
                h_toppt_dr04_mix.Fill(t.pt)
                h_score_dr04_mix.Fill(t.TopScore)
                h_topmixeddr04_ptmass.Fill(t.pt, t.mass)

        if dr_max<100:
            h_dr_mix.Fill(dr_max)
            h_dr_score_onextopgen_mix.Fill(dr_max,topmixed[dr_max_idx].TopScore)
        if len(scores) == 0: 
            continue
        else:
            scores = np.array(scores)
            h_scores_mix.Fill(max(scores))
            idx = top_dr04[int(np.argmax(scores))]
            # print(scores, max(scores), int(np.argmax(scores)))
            h_toppt_select_mix.Fill(top.pt)
            h_topptreco_select_mix.Fill(topmixed[idx].pt)
            h_topmixedsel_ptmass.Fill(topmixed[idx].pt, topmixed[idx].mass)
            if max(scores) > float(Top_threshold['Mixed']['WPloose']):
                h_toppt_selectLoose_mix.Fill(topmixed[idx].pt)
                h_topptgen_selectLoose_mix.Fill(top.pt)
                h_topmass_selectLoose_mix.Fill(topmixed[idx].mass)
                h_topmixedselLoose_ptmass.Fill(topmixed[idx].pt,topmixed[idx].mass)
            if max(scores) > float(Top_threshold['Mixed']['WPmedium']):
                h_toppt_selectMedium_mix.Fill(topmixed[idx].pt)
                h_topptgen_selectMedium_mix.Fill(top.pt)
                h_topmass_selectMedium_mix.Fill(topmixed[idx].mass)
                h_topmixedselMedium_ptmass.Fill(topmixed[idx].pt,topmixed[idx].mass)
            if max(scores) > float(Top_threshold['Mixed']['WPtight']):
                h_toppt_selectTight_mix.Fill(topmixed[idx].pt)
                h_topptgen_selectTight_mix.Fill(top.pt)
                h_topmass_selectTight_mix.Fill(topmixed[idx].mass)
                h_topmixedselTight_ptmass.Fill(topmixed[idx].pt,topmixed[idx].mass)
            if topmixed[idx].truth:
                h_topmass_true_mix.Fill(topmixed[idx].mass)
                h_toppt_true_mix.Fill(topmixed[idx].pt)
                h_score_true_mix.Fill(topmixed[idx].TopScore)
                h_topmixedtrue_ptmass.Fill(topmixed[idx].pt, topmixed[idx].mass)
        scores = []
        top_dr04 = []
        dr_max = 100
        dr_max_idx = -1
        for i, t in enumerate(topresolved):
            dr = deltaR(top.eta, top.phi, t.eta, t.phi)
            if dr <0.4 :
                top_dr04.append(i) 
                scores.append(t.TopScore)
            h_dr_score_res.Fill(dr,t.TopScore)
            if t.truth and dr < dr_max:
                dr_max = dr
                dr_max_idx = i
            if dr < 0.4:
                h_score_dr04_res.Fill(t.TopScore)
                h_topmass_dr04_res.Fill(t.mass)
                h_toppt_dr04_res.Fill(t.pt)
                h_topresolveddr04_ptmass.Fill(t.pt,t.mass)

        if dr_max<100:
            h_dr_res.Fill(dr_max)
            h_dr_score_onextopgen_res.Fill(dr_max,topmixed[dr_max_idx].TopScore)
        if len(scores) == 0: 
            continue
        else: 
            h_scores_res.Fill(max(scores))
            idx = top_dr04[int(np.argmax(scores))]
            h_toppt_select_res.Fill(top.pt)
            h_topptreco_select_res.Fill(topresolved[idx].pt)
            h_topresolvedsel_ptmass.Fill(topresolved[idx].pt,topresolved[idx].mass)
            if max(scores) > float(Top_threshold['Resolved']['WPloose']):
                h_toppt_selectLoose_res.Fill(topresolved[idx].pt)
                h_topptgen_selectLoose_res.Fill(top.pt)
                h_topmass_selectLoose_res.Fill(topresolved[idx].mass)
                h_topresolvedselLoose_ptmass.Fill(topresolved[idx].pt,topresolved[idx].mass)
            if max(scores) > float(Top_threshold['Resolved']['WPmedium']):
                h_toppt_selectMedium_res.Fill(topresolved[idx].pt)
                h_topptgen_selectMedium_res.Fill(top.pt)
                h_topmass_selectMedium_res.Fill(topresolved[idx].mass)
                h_topresolvedselMedium_ptmass.Fill(topresolved[idx].pt,topresolved[idx].mass)
            if max(scores) > float(Top_threshold['Resolved']['WPtight']):
                h_toppt_selectTight_res.Fill(topresolved[idx].pt)
                h_topptgen_selectTight_res.Fill(top.pt)
                h_topmass_selectTight_res.Fill(topresolved[idx].mass)
                h_topresolvedselTight_ptmass.Fill(topresolved[idx].pt,topresolved[idx].mass)
            if topresolved[idx].truth:
                h_topmass_true_res.Fill(topresolved[idx].mass)
                h_toppt_true_res.Fill(topresolved[idx].pt)
                h_score_true_res.Fill(topresolved[idx].TopScore)
                h_topresolvedtrue_ptmass.Fill(topresolved[idx].pt, topresolved[idx].mass)
    if nTopGenHadr==4:
        h_NtopgenrecoMixed.Fill(nTopGenHadr-ntopMixReco)
        h_NtopgenrecoMixed.AddBinContent(0,1)
        h_NtopgenrecoResolved.Fill(nTopGenHadr-ntopResReco)
        h_NtopgenrecoResolved.AddBinContent(0,1)
        h_NtopgenrecoMerged.Fill(nTopGenHadr-ntopMerReco)
        h_NtopgenrecoMerged.AddBinContent(0,1)

# h_NtopgenrecoMixed.SetBinContent(0,tree.GetEntries())
# h_NtopgenrecoResolved.SetBinContent(0,tree.GetEntries())
# h_NtopgenrecoMerged.SetBinContent(0,tree.GetEntries())


print("Top Mixed, Ntot matched", h_scores_mix.Integral())
for wp, t in Top_threshold['Mixed'].items():
    bin = h_scores_mix.FindBin(float(t))
    maxbin = h_scores_mix.GetNbinsX()
    Npass = h_scores_mix.Integral(bin, maxbin)
    Ntot = h_scores_mix.Integral()
    print(f"WP {wp} : {float(Npass)/Ntot}")
print("Top Resolved, Ntot matched", h_scores_res.Integral())
for wp, t in Top_threshold['Resolved'].items():
    bin = h_scores_res.FindBin(float(t))
    maxbin = h_scores_res.GetNbinsX()
    Npass = h_scores_res.Integral(bin, maxbin)
    Ntot = h_scores_res.Integral()
    print(f"WP {wp} : {float(Npass)/Ntot}")




outfile.cd()
h_dr_mix.Write()
h_score_dr04_mix.Write()
h_dr_score_mix.Write()
h_score_true_mix.Write()
h_dr_score_onextopgen_mix.Write()
h_dr_res.Write()
h_score_dr04_res.Write()
h_dr_score_res.Write()
h_score_true_res.Write()
h_dr_score_onextopgen_res.Write()
h_scores_mix.Write()
h_scores_res.Write()
h_topmass_gen.Write()
h_topmass_dr04_mix.Write()
h_topmass_true_mix.Write()
h_toppt_gen.Write()
h_toppt_dr04_mix.Write()
h_toppt_true_mix.Write()
h_topmass_dr04_res.Write()
h_topmass_true_res.Write()
h_toppt_dr04_res.Write()
h_toppt_true_res.Write()
h_topptreco_select_mix.Write()
h_topmass_selectLoose_mix.Write()
h_toppt_select_mix.Write()
h_toppt_selectLoose_mix.Write()
h_topptreco_select_res.Write()
h_topmass_selectLoose_res.Write()
h_toppt_select_res.Write()
h_toppt_selectLoose_res.Write()
h_topmass_selectMedium_mix.Write()
h_toppt_selectMedium_mix.Write()
h_topmass_selectMedium_res.Write()
h_toppt_selectMedium_res.Write()
h_topmass_selectTight_mix.Write()
h_toppt_selectTight_mix.Write()
h_topmass_selectTight_res.Write()
h_toppt_selectTight_res.Write()
h_topgen_ptmass.Write()
h_topmixeddr04_ptmass.Write()
h_topmixedtrue_ptmass.Write()
h_topmixedsel_ptmass.Write()
h_topmixedselLoose_ptmass.Write()
h_topresolvedsel_ptmass.Write()
h_topresolvedselLoose_ptmass.Write()
h_topmixedselMedium_ptmass.Write()
h_topresolvedselMedium_ptmass.Write()
h_topmixedselTight_ptmass.Write()
h_topresolvedselTight_ptmass.Write()
h_topresolveddr04_ptmass.Write()
h_topresolvedtrue_ptmass.Write()
h_topptgen_selectLoose_res.Write()
h_topptgen_selectMedium_res.Write()
h_topptgen_selectTight_res.Write()
h_topptgen_selectLoose_mix.Write()
h_topptgen_selectMedium_mix.Write()
h_topptgen_selectTight_mix.Write()
h_scores_mer.Write()
h_toppt_dr04_mer.Write()
h_toppt_select_mer.Write()
h_toppt_selectLoose_mer.Write()
h_toppt_selectMedium_mer.Write()
h_toppt_selectTight_mer.Write()
h_topptgen_selectLoose_mer.Write()
h_topptgen_selectMedium_mer.Write()
h_topptgen_selectTight_mer.Write()
h_toppt_true_mer.Write()
h_topmergedsel_ptmass.Write()
h_topmergedselLoose_ptmass.Write()
h_topmergedselMedium_ptmass.Write()
h_topmergedselTight_ptmass.Write()
h_topmergeddr04_ptmass.Write()
h_topmergedtrue_ptmass.Write()
h_score_true_mer.Write()
h_highestscoretopmixedreco_pt.Write()
h_highestscoretopmixedreco3match_pt.Write()
h_highestscoretopresolvedreco_pt.Write()
h_highestscoretopresolvedreco3match_pt.Write()
h_highestscoretopmergedreco_pt.Write()
h_highestscoretopmergedreco3match_pt.Write()
h_topmass_HighestScoreselectLoose_mix.Write()
h_toppt_HighestScoreselectLoose_mix.Write()
h_topptgen_HighestScoreselectLoose_mix.Write()
h_topptgen_HighestScore3matchselectLoose_mix.Write()
h_topmixedselHighestScoreLoose_ptmass.Write()
h_topmass_HighestScoreselectMedium_mix.Write()
h_toppt_HighestScoreselectMedium_mix.Write()
h_topptgen_HighestScoreselectMedium_mix.Write()
h_topptgen_HighestScore3matchselectMedium_mix.Write()
h_topmixedselHighestScoreMedium_ptmass.Write()
h_topmass_HighestScoreselectTiht_mix.Write()
h_toppt_HighestScoreselectTight_mix.Write()
h_topptgen_HighestScoreselectTight_mix.Write()
h_topptgen_HighestScore3matchselectTight_mix.Write()
h_topmixedselHighestScoreTight_ptmass.Write()
h_topmass_HighestScoreselectLoose_res.Write()
h_toppt_HighestScoreselectLoose_res.Write()
h_topptgen_HighestScoreselectLoose_res.Write()
h_topptgen_HighestScore3matchselectLoose_res.Write()
h_topresolvedselHighestScoreLoose_ptmass.Write()
h_topmass_HighestScoreselectMedium_res.Write()
h_toppt_HighestScoreselectMedium_res.Write()
h_topptgen_HighestScoreselectMedium_res.Write()
h_topptgen_HighestScore3matchselectMedium_res.Write()
h_topresolvedselHighestScoreMedium_ptmass.Write()
h_topmass_HighestScoreselectTight_res.Write()
h_toppt_HighestScoreselectTight_res.Write()
h_topptgen_HighestScoreselectTight_res.Write()
h_topptgen_HighestScore3matchselectTight_res.Write()
h_topresolvedselHighestScoreTight_ptmass.Write()
h_topmass_HighestScoreselectLoose_mer.Write()
h_toppt_HighestScoreselectLoose_mer.Write()
h_topptgen_HighestScoreselectLoose_mer.Write()
h_topptgen_HighestScore3matchselectLoose_mer.Write()
h_topmergedselHighestScoreLoose_ptmass.Write()
h_topmass_HighestScoreselectMediunm_mer.Write()
h_toppt_HighestScoreselectMedium_mer.Write()
h_topptgen_HighestScoreselectMedium_mer.Write()
h_topptgen_HighestScore3matchselectMedium_mer.Write()
h_topmergedselHighestScoreMedium_ptmass.Write()
h_topmass_HighestScoreselectTight_mer.Write()
h_toppt_HighestScoreselectTight_mer.Write()
h_topptgen_HighestScoreselectTight_mer.Write()
h_topptgen_HighestScore3matchselectTight_mer.Write()
h_topmergedselHighestScoreTight_ptmass.Write()
h_highestscoretopmixedreco_score.Write()
h_highestscoretopresolvedreco_score.Write()
h_highestscoretopmergedreco_score.Write()
h_highestscoretopmixedreco3match_score.Write()
h_highestscoretopresolvedreco3match_score.Write()
h_highestscoretopmergedreco3match_score.Write()
h_highestscoretopmixedreco_scorePt.Write()
h_highestscoretopresolvedreco_scorePt.Write()
h_highestscoretopmergedreco_scorePt.Write()
h_highestscoretopmixedreco3match_scorePt.Write()
h_highestscoretopresolvedreco3match_scorePt.Write()
h_highestscoretopmergedreco3match_scorePt.Write()
h_NtopgenrecoMixed.Write()
h_NtopgenrecoResolved.Write()
h_NtopgenrecoMerged.Write()
outfile.Close()