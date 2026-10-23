//#ifndef POST_H
//#define POST_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TFile.h"
#include "TH2D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include <map>
#include "correction.h"

#include "TDavixFile.h"
#include <vector>
#include <complex>
#include <cmath>
#include <algorithm>
#include "TLorentzVector.h"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;
using rvec_b = const RVec<bool> &;
using rvec_rvec_i = const RVec<RVec<int>> &;

const float TopRes_trs_5fpr  = 0.625; // tight
const float TopMix_trs_5fpr  = 0.950; // tight
const float TopRes_trs_10fpr = 0.425; // loose
const float TopMix_trs_10fpr = 0.900; // loose
const float TopMer_trs_loose = 0.075; // loose
const float TopMer_trs_tight = 0.250; // tight
const float dR=  0.8;
//  Top Resolved threshold 2022 training { 'fpr 10': 0.1422998, 'fpr 5': 0.29475874, 'fpr 1': 0.59264845, 'fpr 01': 0.86580896}
//  Top Mixed threshold 2022 training {"10%": {"thr": 0.7214655876159668,},"5%": {"thr": 0.8474694490432739,},"1%": {"thr": 0.9436638951301575,},"0.1%": {"thr": 0.9789741635322571,}}

const float btagPNet_tightWP_2022           = 0.6734;
const float btagPNet_tightWP_2022EE         = 0.6915;
const float btagPNet_tightWP_2023           = 0.6172;
const float btagPNet_tightWP_2023postBPix   = 0.6133;
const float btagUParTAK4B_tightWP_2024      = 0.4648;

const float btagDeepB_mediumWP_2018         = 0.2783;
const float btagPNet_mediumWP_2022          = 0.245 ;
const float btagPNet_mediumWP_2022EE        = 0.2605;
const float btagPNet_mediumWP_2023          = 0.1917;
const float btagPNet_mediumWP_2023postBPix  = 0.1919;
const float btagUParTAK4B_mediumWP_2024     = 0.1272;

const float btagDeepB_looseWP_2018          = 0.0490;
const float btagPNet_looseWP_2022           = 0.047 ;
const float btagPNet_looseWP_2022EE         = 0.0499;
const float btagPNet_looseWP_2023           = 0.0358;
const float btagPNet_looseWP_2023postBPix   = 0.0359;
const float btagUParTAK4B_looseWP_2024      = 0.0246;

// ########################################################
bool isMC(int SampleFlag){
  if (SampleFlag == 0) return false;
  else return true;
}

RVec<int> SubtractIntVectors(rvec_i vec1, rvec_i vec2) {
  RVec<int> result;
  for (auto v : vec1) {
    if (std::find(vec2.begin(), vec2.end(), v) == vec2.end()) {
      result.emplace_back(v);
    }
  }
  return result;
}

// ############### from skimtree_utils

float deltaPhi (float phi1, float phi2){
  float dphi = (phi1-phi2);
  while(dphi >  M_PI) dphi -= 2*M_PI;
  while(dphi < -M_PI) dphi += 2*M_PI;
  return dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2){
  return hypot(eta1 - eta2, deltaPhi(phi1, phi2)); 
}

// ########################################################
// ############## Un/Ov flow bin ##########################
// ########################################################

float UnOvBin(float var, int bins, float xmin, float xmax){ 
  float fvar;
  float half_step = ((xmax-xmin)/float(bins))/2.; 

  if(var>=xmax) fvar = xmax-half_step;
  else if(var<=xmin) fvar = xmin+half_step;
  else fvar = var; 

  return fvar;
}

// ########################################################
// ##############  MC weights  ##########################
// ########################################################
RVec<float> QCDScale_variations(rvec_f LHEScaleWeight){
    RVec<float> result(3); 
    float lheSF = 1.;
    float lheUp = 1.;
    float lheDown = 1.;
    
    if(LHEScaleWeight.size() > 1){
       lheDown = Min(LHEScaleWeight);
       lheUp = Max(LHEScaleWeight);
    }
    
    result[0] = LHEScaleWeight[4];
    result[1] = lheUp;
    result[2] = lheDown;
    
    return result;
}
RVec<float> PSWeight_variations(rvec_f PSWeight){
    RVec<float> result(4);
    
    float isrmin = 1.;
    float isrmax = 1.;
    float fsrmin = 1.;
    float fsrmax = 1.;
    if (PSWeight.size() > 1){
        isrmin = min(PSWeight[0], PSWeight[2]);
        isrmax = max(PSWeight[0], PSWeight[2]);
        fsrmin = min(PSWeight[1], PSWeight[3]);
        fsrmax = max(PSWeight[1], PSWeight[3]);
    }
    else{
        isrmin = PSWeight[0];
        isrmax = PSWeight[0];
        fsrmin = PSWeight[0];
        fsrmax = PSWeight[0];
    }
    
    result[0] = isrmin;
    result[1] = isrmax;
    result[2] = fsrmin;
    result[3] = fsrmax;
    
    return result;
}

RVec<float> PdfWeight_variations(rvec_f PdfWeight, int ntot){
    
    RVec<float> result(3);
    
    float pdf_totalUp = 1.;
    float pdf_totalDown = 1.;
    float pdf_totalSF = 1.;
    
    if (PdfWeight.size() > 0){
        float pdfweight_sum = 0.;
        float mean_pdf = 0.;
        float rms = 0.;
        pdf_totalSF = PdfWeight[0];

        for (int j = 0; j < PdfWeight.size(); j++) pdfweight_sum += PdfWeight[j];
        float pdf_xsweight = pdfweight_sum/ntot;

        for(int j = 0; j < PdfWeight.size(); j++) mean_pdf = mean_pdf + PdfWeight[j];
        mean_pdf = mean_pdf / PdfWeight.size();
        
        for (int j = 0; j < PdfWeight.size(); j++) rms = rms + pow(PdfWeight[j]-mean_pdf, 2);
        rms = sqrt(rms / PdfWeight.size());

        pdf_totalUp = (1+rms)*mean_pdf;
        pdf_totalDown = (1-rms)*mean_pdf;
    }
    
    result[0] = pdf_totalSF;
    result[1] = pdf_totalUp;
    result[2] = pdf_totalDown;

    return result;
}

// ########################################################
// ############## Data2018 ################################
// ########################################################

bool hemveto(rvec_f Jet_eta, rvec_f Jet_phi, rvec_f Electron_eta, rvec_f Electron_phi){
  float hemvetoetaup = -3.05;
  float hemvetoetadown = -1.35;
  float hemvetophiup = -1.62;
  float hemvetophidown = -0.82;
  bool passesMETHEMVeto = true;

  for(size_t i = 0; i < Jet_eta.size(); i++){
    if(Jet_eta[i]>hemvetoetaup && Jet_eta[i]<hemvetoetadown && Jet_phi[i]>hemvetophiup && Jet_phi[i]<hemvetophidown){
      passesMETHEMVeto = false;
    }
  }
  for(size_t i = 0; i < Electron_eta.size(); i++){
    if(Electron_eta[i]>hemvetoetaup && Electron_eta[i]<hemvetoetadown && Electron_phi[i]>hemvetophiup && Electron_phi[i]<hemvetophidown){
      passesMETHEMVeto = false;
    }
  }
  return passesMETHEMVeto; 
}

int w_nominalhemveto(float w_nominal, bool HEMVeto){
  int w_nominal_update = w_nominal;
  if (HEMVeto == false){
    w_nominal_update = w_nominal * 0.354;
    // w_nominal_update = w_nominal * 0.932;
  }
  return w_nominal_update;
}

// ########################################################
// ############## TT correction ###########################
// ########################################################

bool tt_mtt_doublecounting(rvec_f GenPart_pdgId, rvec_f GenPart_pt, rvec_f GenPart_eta, rvec_f GenPart_phi, rvec_f GenPart_mass){ 
  TLorentzVector top;
  TLorentzVector antitop;
  bool pass = true;
  for(size_t i = 0; i<GenPart_pdgId.size(); i++){
    if(GenPart_pdgId[i]==6){
      top.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i]);
      
    } else if(GenPart_pdgId[i]==-6){
      antitop.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i]);
      
    }
  }
  float Mtt = (top+antitop).M();
  if(Mtt>=700){
    pass = false;
  }
  return pass;
}


// ########################################################
// ############## NLO EW correction #######################
// ########################################################

// sto usando lower_bound quindi quando il pt si trova tra due chiavi prende quella maggiore:
// es. pt = 75 -> prende 100
// quindi prima chiave a 50 avrà la correzione 0-50, seconda chiave a 100 avrà la correzione 50-100
// e così via


float getZPtCorrection(float zPt, std::map<float, float> zPtCorrectionMap) {
  auto it = zPtCorrectionMap.lower_bound(zPt);
  if (it == zPtCorrectionMap.end()) {
    return 1.0; // Default correction if zPt is out of range
  }
  return it->second;
}

float nloewcorrectionZ(float w_nom, rvec_i genpart_pdg, rvec_f genpart_pt, rvec_i genpart_statusFlags)
{ 
    std::map<float, float> zPtCorrectionMap = {
    {100.0,  0.99},
    {200.0,  0.97},
    {300.0,  0.95},
    {400.0,  0.92},
    {500.0,  0.90},
    {600.0,  0.88},
    {700.0,  0.86},
    {800.0,  0.84},
    {900.0,  0.83},
    {1000.0, 0.81},
    {1100.0, 0.80},
    {1200.0, 0.78},
    {1300.0, 0.77},
    {1400.0, 0.76},
    {1500.0, 0.75},
    {1600.0, 0.74},
    {1700.0, 0.73},
    {1800.0, 0.72},
    {1900.0, 0.71},
    {2000.0, 0.70}
  }; 
  float w_final;
  float zpart_pt=0;
  for(int i = 0; i<genpart_pt.size();i++)
  {
    if(abs(genpart_pdg[i])==23 && (genpart_statusFlags[i] & 1<<13))
    {
      zpart_pt = genpart_pt[i];
    }
  }
  float zptcorr = getZPtCorrection(zpart_pt, zPtCorrectionMap);
  w_final = w_nom*zptcorr;
  return w_final;
}  

float nloewcorrectionW(float w_nom, rvec_i genpart_pdg, rvec_f genpart_pt, rvec_i genpart_statusFlags)
{  
  std::map<float, float> wPtCorrectionMap = {
    {100.0,  0.99},
    {200.0,  0.97},
    {300.0,  0.93},
    {400.0,  0.90},
    {500.0,  0.87},
    {600.0,  0.85},
    {700.0,  0.82},
    {800.0,  0.80},
    {900.0,  0.78},
    {1000.0, 0.76},
    {1100.0, 0.74},
    {1200.0, 0.72},
    {1300.0, 0.71},
    {1400.0, 0.69},
    {1500.0, 0.68},
    {1600.0, 0.67},
    {1700.0, 0.65},
    {1800.0, 0.64},
    {1900.0, 0.63},
    {2000.0, 0.62}
  };  
  float w_final;
  float wpart_pt=0;
  for(int i = 0; i<genpart_pt.size();i++)
  {
    if(abs(genpart_pdg[i])==24 && (genpart_statusFlags[i] & 1<<13))
    {
      wpart_pt = genpart_pt[i];
    }
  }
  float wptcorr = getZPtCorrection(wpart_pt, wPtCorrectionMap);
  w_final = w_nom*wptcorr;
  return w_final;
}  

// ########################################################
// ############## MET_HLT_filter ##########################
// ########################################################

bool MET_HLT_filter(bool HLT_PFMET120_PFMHT120_IDTight, bool HLT_PFMETNoMu120_PFMHTNoMu120_IDTight, bool flag_goodVertices, bool flag_globalSuperTightHalo2016Filter, bool flag_HBHENoiseFilter, bool flag_HBHENoiseIsoFilter, bool flag_EcalDeadCellTriggerPrimitiveFilter, bool flag_BadPFMuonFilter, bool flag_BadPFMuonDzFilter, bool flag_ecalBadCalibFilter, bool flag_eeBadScFilter){
  
  // bool good_HLT = HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight;
  bool good_MET = flag_goodVertices && flag_globalSuperTightHalo2016Filter && flag_HBHENoiseFilter && flag_HBHENoiseIsoFilter && flag_EcalDeadCellTriggerPrimitiveFilter && flag_BadPFMuonFilter && flag_BadPFMuonDzFilter && flag_ecalBadCalibFilter && flag_eeBadScFilter; //  && flag_hfNoisyHitsFilter && flag_BadChargedCandidateFilter;
  
  return good_MET; //good_HLT
}

bool MET_filter(bool flag_goodVertices, bool flag_globalSuperTightHalo2016Filter, bool flag_HBHENoiseFilter, bool flag_HBHENoiseIsoFilter, bool flag_EcalDeadCellTriggerPrimitiveFilter, bool flag_BadPFMuonFilter, bool flag_BadPFMuonDzFilter, bool flag_ecalBadCalibFilter, bool flag_eeBadScFilter){
  bool good_MET = flag_goodVertices && flag_globalSuperTightHalo2016Filter && flag_HBHENoiseFilter && flag_HBHENoiseIsoFilter && flag_EcalDeadCellTriggerPrimitiveFilter && flag_BadPFMuonFilter && flag_BadPFMuonDzFilter && flag_ecalBadCalibFilter && flag_eeBadScFilter;
  return good_MET;
}

// ########################################################
// ############## CorrectionSet cache #####################
// ########################################################

// Read each correctionlib json only once (at the first call) instead of at every event:
// from_file at every event costs ~7 ms/event for the b-tag jsons, the cached lookup ~0.01 ms/event.
// Not thread-safe: fine as long as ROOT::EnableImplicitMT() is off.
const correction::CorrectionSet& GetCachedCorrectionSet(const std::string& path)
{
  static std::map<std::string, std::unique_ptr<correction::CorrectionSet>> cache;   // one CorrectionSet per file path
  auto it = cache.find(path);
  if (it == cache.end())
    it = cache.emplace(path, correction::CorrectionSet::from_file(path)).first;
  return *it->second;
}

// ########################################################
// ############## Trigger SF     ##########################
// ########################################################

float GetTriggerSF(float PuppiMET_pt, std::string era, std::string type){
  const auto& cset = GetCachedCorrectionSet("../TriggerSF/TriggerSF.json");
  auto triggerSF_corr = cset.at("triggerSF");
  float weight = 1.0;
  if (PuppiMET_pt > 100){
    weight = triggerSF_corr->evaluate({PuppiMET_pt, era, type});
  }
  return weight;
}


// ########################################################
// ###########Alternative Truth definition ################
// ########################################################

//  Alternative truth definition
RVec<int> get_pos_nums(int num) 
{
    RVec<int> pos_nums;
    while (num != 0) {
        if (num % 10 != 0) pos_nums.emplace_back(num % 10);
        num = num / 10;
    }
    return pos_nums;
}

RVec<int> SetDifference(rvec_i v2, rvec_i v1) 
{
  RVec<int> diff;
  for (int i = 0; i < v2.size(); i++) {
    if (std::find(v1.begin(), v1.end(), v2[i]) == v1.end()) {
      diff.emplace_back(v2[i]);
    }
  }
  return diff;
}

RVec<int> UniqueFlavList(int idxJet0, int idxJet1, int idxJet2) 
{
  RVec<int> common_element = Intersect(get_pos_nums(idxJet0), get_pos_nums(idxJet1));
  RVec<int> tmp_ = SetDifference(get_pos_nums(idxJet1), common_element);
  RVec<int> jetflavs_list_ = Concatenate(get_pos_nums(idxJet0), tmp_);
  RVec<int> common_element_ = Intersect(jetflavs_list_, get_pos_nums(idxJet2));
  RVec<int> tmp__ = SetDifference(get_pos_nums(idxJet2), common_element_);
  RVec<int> jetflavs_list = Concatenate(jetflavs_list_, tmp__); 
    
  return jetflavs_list;
}

int truth_2(int idxJet0, int idxJet1, int idxJet2, int idxFatJet, rvec_i Jet_matched, rvec_i Jet_topMother, rvec_i Jet_pdgId, rvec_i FatJet_matched, rvec_i FatJet_topMother, rvec_i FatJet_pdgId) 
{
    int top_truth = 0;
    RVec<int> jetflavs_list;
    RVec<int> fatjetflavs_list;

    if (idxJet2==-1) 
    {
        int matchedJets = 0;
        if (Jet_matched[idxJet0] > 0) matchedJets++;
        if (Jet_matched[idxJet1] > 0) matchedJets++;

        if ( matchedJets >=2 && FatJet_matched[idxFatJet] > 0 && (FatJet_topMother[idxFatJet] == Jet_topMother[idxJet1] && FatJet_topMother[idxFatJet] == Jet_topMother[idxJet0])) 
        {
          RVec<int> common_element = Intersect(get_pos_nums(Jet_pdgId[idxJet0]), get_pos_nums(Jet_pdgId[idxJet1]));
          RVec<int> tmp_ = SetDifference(get_pos_nums(Jet_pdgId[idxJet1]), common_element);
          jetflavs_list = Concatenate(get_pos_nums(Jet_pdgId[idxJet0]), tmp_);
          fatjetflavs_list = get_pos_nums(FatJet_pdgId[idxFatJet]);
        }
    } else {
      if (idxFatJet != -1) {
        int matchedJets = 0;
        if (Jet_matched[idxJet0] > 0) matchedJets++;
        if (Jet_matched[idxJet1] > 0) matchedJets++;
        if (Jet_matched[idxJet2] > 0) matchedJets++;

        if (matchedJets >= 2 && FatJet_matched[idxFatJet] > 0 && (Jet_topMother[idxJet0] == Jet_topMother[idxJet1] || Jet_topMother[idxJet0] == Jet_topMother[idxJet2] || Jet_topMother[idxJet1] == Jet_topMother[idxJet2]) && (Jet_topMother[idxJet0] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet1] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet2] == FatJet_topMother[idxFatJet])) 
        {
          jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2]);
          fatjetflavs_list = get_pos_nums(FatJet_pdgId[idxFatJet]);
        }
        }else 
        {
          // cout<<"3j0fj"<<endl;
          int matchedJets = 0;
          if (Jet_matched[idxJet0] > 0) matchedJets++;
          if (Jet_matched[idxJet1] > 0) matchedJets++;
          if (Jet_matched[idxJet2] > 0) matchedJets++;
          if (matchedJets>=2 && (Jet_topMother[idxJet0] == Jet_topMother[idxJet1] || Jet_topMother[idxJet1] == Jet_topMother[idxJet2] || Jet_topMother[idxJet0] == Jet_topMother[idxJet2])) 
          {
            jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2]);
            RVec<int> fatjetflavs_list {};
          }          
        }
    }

    if (jetflavs_list.size() >= 2 || fatjetflavs_list.size() >= 2) 
    {
      top_truth = 1;
    } else 
    {
      RVec<int> flavs_list = Intersect(jetflavs_list, fatjetflavs_list);
      if (flavs_list.size() >= 2) {
          top_truth = 1;
      } else {
          top_truth = 0;
      }
    }

    return top_truth;
}

int truth_1(int idxJet0, int idxJet1, int idxJet2, int idxFatJet, rvec_i Jet_matched, rvec_i Jet_topMother, rvec_i Jet_pdgId, rvec_i FatJet_matched, rvec_i FatJet_topMother, rvec_i FatJet_pdgId) 
{
    int top_truth = 0;
    RVec<int> jetflavs_list;
    RVec<int> fatjetflavs_list;

    if (idxJet2==-1) 
    {
        int matchedJets = 0;
        if (Jet_matched[idxJet0] > 0) matchedJets++;
        if (Jet_matched[idxJet1] > 0) matchedJets++;

        if ( matchedJets >=1 && FatJet_matched[idxFatJet] > 0 && (FatJet_topMother[idxFatJet] == Jet_topMother[idxJet1] || FatJet_topMother[idxFatJet] == Jet_topMother[idxJet0])) 
        {
          RVec<int> common_element = Intersect(get_pos_nums(Jet_pdgId[idxJet0]), get_pos_nums(Jet_pdgId[idxJet1]));
          RVec<int> tmp_ = SetDifference(get_pos_nums(Jet_pdgId[idxJet1]), common_element);
          jetflavs_list = Concatenate(get_pos_nums(Jet_pdgId[idxJet0]), tmp_);
          fatjetflavs_list = get_pos_nums(FatJet_pdgId[idxFatJet]);
        }
    } else {
      if (idxFatJet != -1) {
        int matchedJets = 0;
        if (Jet_matched[idxJet0] > 0) matchedJets++;
        if (Jet_matched[idxJet1] > 0) matchedJets++;
        if (Jet_matched[idxJet2] > 0) matchedJets++;

        if (matchedJets >= 1 && FatJet_matched[idxFatJet] > 0 && (Jet_topMother[idxJet0] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet1] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet2] == FatJet_topMother[idxFatJet])) 
        {
          jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2]);
          fatjetflavs_list = get_pos_nums(FatJet_pdgId[idxFatJet]);
        }
        }else 
        {
          int matchedJets = 0;
          if (Jet_matched[idxJet0] > 0) matchedJets++;
          if (Jet_matched[idxJet1] > 0) matchedJets++;
          if (Jet_matched[idxJet2] > 0) matchedJets++;
          if (matchedJets>=1) 
          {
            jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2]);  
            RVec<int> fatjetflavs_list {};
          }          
        }
    }

    if (jetflavs_list.size() >= 1 || fatjetflavs_list.size() >= 1) 
    {
      top_truth = 1;
    } else 
    {
      RVec<int> flavs_list = Intersect(jetflavs_list, fatjetflavs_list);
      if (flavs_list.size() >= 1) {
          top_truth = 1;
      } else {
          top_truth = 0;
      }
    }

    return top_truth;
}

RVec<int> CalculateToptruth2(rvec_i TopMixed_idxJet0, rvec_i TopMixed_idxJet1, rvec_i TopMixed_idxJet2, rvec_i TopMixed_idxFatJet, rvec_i Jet_matched, rvec_i Jet_topMother, rvec_i Jet_pdgId, rvec_i FatJet_matched, rvec_i FatJet_topMother, rvec_i FatJet_pdgId)
{
  RVec<int> TopMixed_truth;
  RVec<int> idxFatJet;
  if(TopMixed_idxFatJet.size()==0) 
  {
    RVec<int> tmp;
    for(int i = 0; i < TopMixed_idxJet0.size(); i++)
    {
      tmp.emplace_back(-1);
    }
    idxFatJet = tmp;
  }else
  {
    idxFatJet = TopMixed_idxFatJet;
  }
  for (int i = 0; i < TopMixed_idxJet0.size(); i++)
  {
    TopMixed_truth.emplace_back(truth_2(TopMixed_idxJet0[i], TopMixed_idxJet1[i], TopMixed_idxJet2[i], idxFatJet[i], Jet_matched, Jet_topMother, Jet_pdgId, FatJet_matched, FatJet_topMother, FatJet_pdgId));
  }
  return TopMixed_truth;
}

RVec<int> CalculateToptruth1(rvec_i TopMixed_idxJet0, rvec_i TopMixed_idxJet1, rvec_i TopMixed_idxJet2, rvec_i TopMixed_idxFatJet, rvec_i Jet_matched, rvec_i Jet_topMother, rvec_i Jet_pdgId, rvec_i FatJet_matched, rvec_i FatJet_topMother, rvec_i FatJet_pdgId)
{
  RVec<int> TopMixed_truth;
  RVec<int> idxFatJet;
  if(TopMixed_idxFatJet.size()==0) 
  {
    RVec<int> tmp;
    for(int i = 0; i < TopMixed_idxJet0.size(); i++)
    {
      tmp.emplace_back(-1);
    }
    idxFatJet = tmp;
  }else
  {
    idxFatJet = TopMixed_idxFatJet;
  }
  for (int i = 0; i < TopMixed_idxJet0.size(); i++)
  {
    TopMixed_truth.emplace_back(truth_1(TopMixed_idxJet0[i], TopMixed_idxJet1[i], TopMixed_idxJet2[i], idxFatJet[i], Jet_matched, Jet_topMother, Jet_pdgId, FatJet_matched, FatJet_topMother, FatJet_pdgId));
  }
  return TopMixed_truth;
}

// ########################################################
// ########## PRESELECTION ################################
// ########################################################
int nTightElectron(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased, rvec_i Electron_mvaIso_WP80, rvec_f Electron_minDeltaR_fromGoodJets)
{
  int n=0;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=4 && Electron_pt[i] > 50 && abs(Electron_eta[i])<2.5 && Electron_mvaIso_WP80[i]==1 && Electron_minDeltaR_fromGoodJets[i] > 0.4) n+=1;
  }
  return n;
}

RVec<int> TightElectron_idx(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased, rvec_i Electron_mvaIso_WP80, rvec_f Electron_minDeltaR_fromGoodJets)
{
  RVec<int> ids;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=4 && Electron_pt[i] > 50 && abs(Electron_eta[i])<2.5 && Electron_mvaIso_WP80[i]==1 && Electron_minDeltaR_fromGoodJets[i] > 0.4) ids.emplace_back(i);
  }
  return ids;
}

int nLooseElectron(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased, rvec_i Electron_mvaIso_WP80, rvec_f Electron_minDeltaR_fromGoodJets)
{
  int n=0;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=1 && Electron_pt[i] > 50 && abs(Electron_eta[i])<2.5 && Electron_mvaIso_WP80[i]==1 && Electron_minDeltaR_fromGoodJets[i] > 0.4) n+=1;
  }
  return n;
}

RVec<int> LooseElectron_idx(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased, rvec_i Electron_mvaIso_WP80, rvec_f Electron_minDeltaR_fromGoodJets)
{
  RVec<int> ids;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=1 && Electron_pt[i] > 50 && abs(Electron_eta[i])<2.5 && Electron_mvaIso_WP80[i]==1 && Electron_minDeltaR_fromGoodJets[i] > 0.4) ids.emplace_back(i);
  }
  return ids;
}

int nVetoElectron(rvec_f Electron_pt, rvec_f Electron_cutBased, rvec_f Electron_eta, rvec_i Electron_mvaIso_WP80, rvec_f Electron_minDeltaR_fromGoodJets)
{
  int n=0;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=1 && Electron_pt[i] > 30 && abs(Electron_eta[i])<2.5 && Electron_mvaIso_WP80[i]==1 && Electron_minDeltaR_fromGoodJets[i] > 0.4) n+=1;
  }
  return n;
}

RVec<int> VetoElectron_idx(rvec_f Electron_pt, rvec_f Electron_cutBased, rvec_f Electron_eta, rvec_i Electron_mvaIso_WP80, rvec_f Electron_minDeltaR_fromGoodJets)
{
  RVec<int> ids;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=1 && Electron_pt[i] > 30 && abs(Electron_eta[i])<2.5 && Electron_mvaIso_WP80[i]==1 && Electron_minDeltaR_fromGoodJets[i] > 0.4) ids.emplace_back(i);
  }
  return ids;
}

int nTightMuon(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_tightId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets)
{
  int n=0;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_tightId[i]==1 && Muon_pt[i] > 50 && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3 && Muon_minDeltaR_fromGoodJets[i] > 0.4) n+=1;
  }
  return n;
}

RVec<int> TightMuon_idx(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_tightId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets)
{
  RVec<int> ids;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_tightId[i]==1 && Muon_pt[i] > 50 && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3 && Muon_minDeltaR_fromGoodJets[i] > 0.4) ids.emplace_back(i);
  }
  return ids;
}

int nLooseMuon(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_looseId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets)
{
  int n=0;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_looseId[i]==1 && Muon_pt[i] > 50 && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3 && Muon_minDeltaR_fromGoodJets[i] > 0.4) n+=1;
  }
  return n;
}

RVec<int> LooseMuon_idx(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_looseId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets)
{
  RVec<int> ids;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_looseId[i]==1 && Muon_pt[i] > 50 && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3 && Muon_minDeltaR_fromGoodJets[i] > 0.4) ids.emplace_back(i);
  }
  return ids;
}

int nVetoMuon(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_looseId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets)
{
  int n=0;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_looseId[i]==1 && Muon_pt[i] > 30 && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3 && Muon_minDeltaR_fromGoodJets[i] > 0.4) n+=1;
  }
  return n;
}

RVec<int> VetoMuon_idx(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_looseId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets)
{
  RVec<int> ids;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_looseId[i]==1 && Muon_pt[i] > 30 && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3 && Muon_minDeltaR_fromGoodJets[i] > 0.4) ids.emplace_back(i);
  }
  return ids;
}

bool LepVeto(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased, rvec_i Electron_mvaIso_WP80, rvec_f Muon_pt, rvec_f Muon_eta, rvec_b Muon_looseId, rvec_i Muon_pfIsoId)
{
  int EleVetoPassed = 0;
  int MuVetoPassed = 0;
  bool IsLepVetoPassed = true;
  
  for (size_t i = 0; i < Electron_pt.size(); i++) 
    {
      if(Electron_cutBased[i]>=1 && Electron_pt[i] > 30. && abs(Electron_eta[i])<2.4 && Electron_mvaIso_WP80[i]==1) EleVetoPassed+=1;
    }
  for (size_t i = 0; i< Muon_pt.size(); i++)
    {
      if(Muon_looseId[i]==1 && Muon_pt[i] > 30. && abs(Muon_eta[i])<2.4 && Muon_pfIsoId[i]>=3) MuVetoPassed+=1;
    }
  if(EleVetoPassed+MuVetoPassed >0) IsLepVetoPassed = false;
  
  return IsLepVetoPassed;
}

RVec<bool> Jet_passJetIdTight(rvec_f Jet_eta, rvec_i Jet_jetId, rvec_f Jet_neHEF, rvec_f Jet_neEmEF)
{
  RVec<bool> passJetIdTight;
  for(int i = 0; i<Jet_eta.size(); i++)
  {
    bool _passJetIdTight = false;
    if (abs(Jet_eta[i]) <= 2.7)
    {
      _passJetIdTight = Jet_jetId[i] & (1 << 1);
    }
    else if (abs(Jet_eta[i]) > 2.7 && abs(Jet_eta[i]) <= 3.0)
    {
      _passJetIdTight = (Jet_jetId[i] & (1 << 1)) && (Jet_neHEF[i] < 0.99);
    }
    else if (abs(Jet_eta[i]) > 3.0)
    {
      _passJetIdTight = (Jet_jetId[i] & (1 << 1)) && (Jet_neEmEF[i] < 0.4);
    }
    passJetIdTight.emplace_back(_passJetIdTight);
  }
  return passJetIdTight;
}

RVec<bool> Jet_passJetIdTightLepVeto(rvec_f Jet_eta, rvec_b Jet_passJetIdTight, rvec_f Jet_muEF, rvec_f Jet_chEmEF)
{
  RVec<bool> passJetIdTightLepVeto;
  for(int i = 0; i<Jet_eta.size(); i++)
  {
    bool _passJetIdTightLepVeto = false;
    if (abs(Jet_eta[i]) <= 2.7)
    {
      _passJetIdTightLepVeto = Jet_passJetIdTight[i] && (Jet_muEF[i] < 0.8) && (Jet_chEmEF[i] < 0.8);
    }
    else
    {
      _passJetIdTightLepVeto = Jet_passJetIdTight[i];
    }
    passJetIdTightLepVeto.emplace_back(_passJetIdTightLepVeto);
  }
  return passJetIdTightLepVeto;
}

RVec<int> GetGoodJet(rvec_f Jet_pt, rvec_f Jet_eta, rvec_i Jet_jetId)
{
  RVec<int> ids;
  for(int i = 0; i<Jet_pt.size(); i++)
  {
    // taglio in eta portato da 2.7 a 2.4 -> per definizione forward jets
      if (Jet_pt[i]>30 && abs(Jet_eta[i])<2.4 && Jet_jetId[i]==6)
      {
        ids.emplace_back(i);
      }
  }
  return ids;
}

RVec<int> GetGoodFatJet(rvec_f Jet_pt, rvec_f Jet_eta, rvec_i Jet_jetId)
{
  RVec<int> ids;
  for(int i = 0; i<Jet_pt.size(); i++)
  {
    // taglio in eta portato da 2.7 a 2.4 -> per definizione forward jets
      if (Jet_pt[i]>200 && abs(Jet_eta[i])<2.4 && Jet_jetId[i]==6)
      {
        ids.emplace_back(i);
      }
  }
  return ids;
}

int nGoodJet(rvec_i GoodJet_idx)
{
  return GoodJet_idx.size();
}

bool atLeast1verygoodjet(rvec_i GoodJet_idx, rvec_f Jet_pt, rvec_f Jet_eta)
{
  bool pass = false;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    if (Jet_pt[GoodJet_idx[i]]>30 && abs(Jet_eta[GoodJet_idx[i]])<4) 
    {
      pass = true;
    }
  }
  return pass;
}

bool atLeast1verygoodfatjet(rvec_f FatJet_pt, rvec_f FatJet_msoftdrop)
{
  bool pass = false;
  for(int i = 0; i < FatJet_pt.size(); i++)
  {
    if (FatJet_pt[i]>200 && FatJet_msoftdrop[i]>40) 
    {
      pass = true;
    }
  }
  return pass;
}

// ########################################################
// ######## Event variables (deltaphi, etajet) ############
// ########################################################

float min_DeltaPhi(float MET_phi, rvec_f Jet_phi, rvec_i GoodJet_idx)
{
  float min_dphi = 4;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    float dphi = deltaPhi(MET_phi, Jet_phi[GoodJet_idx[i]]);
    if (dphi < min_dphi) min_dphi = dphi;
  }
  return min_dphi;
}


float MHT(rvec_f GoodJet_idx, rvec_f Jet_pt, rvec_f Jet_phi, rvec_f Jet_eta, rvec_f Jet_mass)
{
  RVec<ROOT::Math::PtEtaPhiMVector> v;

  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    const ROOT::Math::PtEtaPhiMVector tmp_ {Jet_pt[GoodJet_idx[i]], Jet_eta[GoodJet_idx[i]], Jet_phi[GoodJet_idx[i]], Jet_mass[GoodJet_idx[i]]};
    v.emplace_back(tmp_);
  }
  auto v_sum_lv = Sum(v, ROOT::Math::PtEtaPhiMVector());
  return v_sum_lv.M();
}

// ########################################################
// ########## New functions for deb #######################
// ########################################################

bool atLeast1jet_setparams(rvec_f Jet_pt, rvec_f Jet_eta, rvec_f Jet_mass, rvec_i Jet_jetId, float minpt, float maxeta, float minmass, int jetId)
{
  bool pass = false;
  for(int i = 0; i < Jet_pt.size(); i++)
  {
    if (Jet_pt[i]>minpt && abs(Jet_eta[i])<maxeta && Jet_mass[i]>minmass && Jet_jetId[i]>=jetId) 
    {
      pass = true;
    }
  }
  return pass;
}

bool atLeast1fatjet_setparams(rvec_f FatJet_pt, rvec_f FatJet_msoftdrop, rvec_f FatJet_eta, rvec_i FatJet_jetId, float minpt, float maxeta, float minmsoftdrop, int jetId)
{
  bool pass = false;
  for(int i = 0; i < FatJet_pt.size(); i++)
  {
    if (FatJet_pt[i]>minpt && abs(FatJet_eta[i])<maxeta && FatJet_msoftdrop[i]>minmsoftdrop && FatJet_jetId[i]>=jetId) 
    {
      pass = true;
    }
  }
  return pass;
}

Int_t GetLeadingPtJet(rvec_f Jet_pt)
{
  RVec<float> pt;
  for(int i = 0; i < Jet_pt.size(); i++)
  {
    pt.emplace_back(Jet_pt[i]);
  }
  return ArgMax(pt);
}

Int_t GetLeadingPtLep(rvec_f Lep_pt, rvec_f Lep_eta, rvec_i Lep_looseId)
{
  RVec<float> pt;
  for(int i = 0; i < Lep_pt.size(); i++)
  {
    if (Lep_looseId[i]>0 && Lep_pt[i]>30 && abs(Lep_eta[i])<2.4)
    {
      pt.emplace_back(Lep_pt[i]);
    }
    else
    {
      pt.emplace_back(-10);
    }
  }
  if (pt.size() == 0) return -1;
  else return ArgMax(pt);
}

Float_t GetLeadingJetVar(int LeadingJet_idx, rvec_f Jet_var)
{
  if (LeadingJet_idx == -1) return 0;
  else return Jet_var[LeadingJet_idx];
}

// ########################################################
// ########## AH1lWR control region #######################
// ########################################################
int Lepton_flavour(int nTightElectron, int nTightMuon)
{
  int flav=0;
  if (nTightElectron == 1) flav = 1;
  else if (nTightMuon == 1) flav = 2;
  return flav;
}

float Lepton_var(int Lepton_flavour, rvec_f Electron_var, rvec_i tightElectron_idx, rvec_f Muon_var, rvec_i tightMuon_idx)
{
  float var=0;
  if (Lepton_flavour == 1) var = Electron_var[tightElectron_idx[0]];
  else if (Lepton_flavour == 2) var = Muon_var[tightMuon_idx[0]];
  else var = -1000;
  return var;
}

// ########################################################
// ############## MC/data comparison vars #################
// ########################################################

Float_t LeadingJetPt(rvec_i GoodJet_idx, rvec_f Jet_pt)
{
  RVec<float> GoodJet_pt;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    GoodJet_pt.emplace_back(Jet_pt[GoodJet_idx[i]]);
  }
  return Max(GoodJet_pt);
}

Float_t LeadingFatJetPt(rvec_f FatJet_pt)
{
  
  RVec<float> fj_pt;
  for(int i = 0; i < FatJet_pt.size(); i++)
  {
    fj_pt.emplace_back(FatJet_pt[i]);
  }
  return Max(fj_pt);
}

Int_t nForwardJet(rvec_f Jet_pt, rvec_f Jet_jetId, rvec_f Jet_eta)
{
  int nfwdjet = 0;
  for(int i = 0; i < Jet_pt.size(); i++)
  {
    if (Jet_pt[i]>30 && Jet_jetId[i]==6 && abs(Jet_eta[i])>2.4)
    {
      nfwdjet += 1;
    }
  }
  return nfwdjet;
}

RVec<int> GetJetBTag(rvec_i GoodJet, rvec_f Jet_btagDeepB, int year, bool EE, int wp){
  // WP legend: 0->loose, 1->medium, 2->tight
    RVec<int> ids;
    float bthres;    
    if(year == 2018){
      if(wp == 1){
        bthres = btagDeepB_mediumWP_2018;
      }
      else if(wp==0){
        bthres = btagDeepB_looseWP_2018;
      }
    }
    else if(year == 2022){
      if(EE){
        if(wp == 2){
          bthres = btagPNet_tightWP_2022EE;
        }
        else if(wp == 1){
          bthres = btagPNet_mediumWP_2022EE;
        }
        else if(wp==0){
          bthres = btagPNet_looseWP_2022EE;
        }
      }
      else{
        if(wp == 2){
          bthres = btagPNet_tightWP_2022;
        }
        else if(wp == 1){
          bthres = btagPNet_mediumWP_2022;
        }
        else if(wp==0){
          bthres = btagPNet_looseWP_2022;
        }
        
      }
    }
    else if(year == 2023){
      if(EE){
        if(wp == 2){
          bthres = btagPNet_tightWP_2023postBPix;
        }
        else if(wp == 1){
          bthres = btagPNet_mediumWP_2023postBPix;
        }
        else if(wp==0){
          bthres = btagPNet_looseWP_2023postBPix;
        }
      }
      else{
        if(wp == 2){
          bthres = btagPNet_tightWP_2023;
        }
        else if(wp == 1){
          bthres = btagPNet_mediumWP_2023;
        }
        else if(wp==0){
          bthres = btagPNet_looseWP_2023;
        }
      }
    }
    else if(year == 2024){
      if(EE){
        if(wp == 2){
          bthres = btagUParTAK4B_tightWP_2024;
        }
        else if(wp == 1){
          bthres = btagUParTAK4B_mediumWP_2024;
        }
        else if(wp==0){
          bthres = btagUParTAK4B_looseWP_2024;
        }
      }
      else{
        if(wp == 2){
          bthres = btagUParTAK4B_tightWP_2024;
        }
        else if(wp == 1){
          bthres = btagUParTAK4B_mediumWP_2024;
        }
        else if(wp==0){
          bthres = btagUParTAK4B_looseWP_2024;
        }
      }
    }
    // cout << "btag thr: " << bthres << endl;
    
    for(int i = 0; i<GoodJet.size(); i++)
    {
        if (Jet_btagDeepB[GoodJet[i]]>bthres)
        {
            ids.emplace_back(i);
        }
    }
    return ids;
}

RVec<float> GetJetBTagScore(rvec_i GoodJet, rvec_f Jet_btagDeepB)
{
    RVec<float> scores;
    for(int i = 0; i<GoodJet.size(); i++)
    {
        scores.emplace_back(Jet_btagDeepB[GoodJet[i]]);
    }
    return scores;
}

////// b-tag event weight with fixed WPs (L, M, T), BTV multi-WP prescription:
////// https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/#scale-factor-recommendations-for-event-reweighting
////// weight = P(DATA)/P(MC) = product over the good jets of a factor that depends on the WP band of the jet:
//////   score > T       ->  SF_T*eff_T / eff_T
//////   M < score <= T  ->  (SF_M*eff_M - SF_T*eff_T) / (eff_M - eff_T)
//////   L < score <= M  ->  (SF_L*eff_L - SF_M*eff_M) / (eff_L - eff_M)
//////   score <= L      ->  (1 - SF_L*eff_L) / (1 - eff_L)
////// eff = MC b-tag efficiency of the WP (our maps), SF = BTV scale factor of the WP
float GetBTagEventWeight_FixedWP(std::string btvFilePath, std::string effFilePath, std::string effCorrectionName,
                                 rvec_i GoodJet_idx, rvec_f Jet_pt, rvec_f Jet_eta, rvec_i Jet_hadronFlavour, rvec_f Jet_btagScore,
                                 float wpLoose, float wpMedium, float wpTight)
{
  const auto& btv_cset = GetCachedCorrectionSet(btvFilePath);
  const auto& eff_cset = GetCachedCorrectionSet(effFilePath);
  auto sf_heavy = btv_cset.at("UParTAK4_comb");                               // b, c jets
  auto sf_light = btv_cset.at("UParTAK4_light");                              // udsg jets
  auto eff      = eff_cset.at(effCorrectionName);                             // process map or inclusive map, chosen in postSelector.py

  float weight = 1.;
  for (int j : GoodJet_idx)
  {
    int   flavour = Jet_hadronFlavour[j];    // 5 = b, 4 = c, 0 = udsg, same convention as the BTV json
    float abseta  = std::abs(Jet_eta[j]);
    float pt      = Jet_pt[j];
    auto  sf      = (flavour > 3) ? sf_heavy : sf_light;

    float eff_L = eff->evaluate({"L", flavour, abseta, pt});
    float eff_M = eff->evaluate({"M", flavour, abseta, pt});
    float eff_T = eff->evaluate({"T", flavour, abseta, pt});
    float sf_L  = sf->evaluate({"central", "L", flavour, abseta, pt});
    float sf_M  = sf->evaluate({"central", "M", flavour, abseta, pt});
    float sf_T  = sf->evaluate({"central", "T", flavour, abseta, pt});

    float score = Jet_btagScore[j];
    if (score > wpTight)
      weight *= (sf_T*eff_T) / eff_T;
    else if (score > wpMedium)
      weight *= (sf_M*eff_M - sf_T*eff_T) / (eff_M - eff_T);
    else if (score > wpLoose)
      weight *= (sf_L*eff_L - sf_M*eff_M) / (eff_L - eff_M);
    else
      weight *= (1. - sf_L*eff_L) / (1. - eff_L);
  }

  if (!std::isfinite(weight) || weight < 0) return 1.;   // empty efficiency bin or non-monotonic SF*eff
  return weight;
}

// ########################################################
// ############## TopSelection ############################
// ########################################################

// Top Merged, FatJet over threshold of particleNet_TvsQCD
RVec<int> select_TopMer(rvec_f FatJet_particleNet_TvsQCD, rvec_i GoodFatJet_idx, float wp)
{
  RVec<int> ids;
  for (int i = 0; i < GoodFatJet_idx.size(); i++)
  {
    if(FatJet_particleNet_TvsQCD[GoodFatJet_idx[i]]>wp){
      ids.emplace_back(GoodFatJet_idx[i]);
    }
  }
  return ids;
}


bool check_same_top(int idx_fj_1, int idx_j0_1, int idx_j1_1, int idx_j2_1, int idx_fj_2, int idx_j0_2, int idx_j1_2, int idx_j2_2)
{
  std::vector<int> list_1 = {idx_j0_1, idx_j1_1, idx_j2_1};
  std::vector<int> list_2 = {idx_j0_2, idx_j1_2, idx_j2_2};
  
  // Remove elements equal to -1
  list_1.erase(std::remove(list_1.begin(), list_1.end(), -1), list_1.end());
  list_2.erase(std::remove(list_2.begin(), list_2.end(), -1), list_2.end());
  
  std::set<int> set_1(list_1.begin(), list_1.end());
  std::set<int> set_2(list_2.begin(), list_2.end());
  
  std::set<int> intersection;
  std::set_intersection(set_1.begin(), set_1.end(), set_2.begin(), set_2.end(), std::inserter(intersection, intersection.begin()));
  
  bool check_jets = !intersection.empty();

  bool check_fj = (idx_fj_1 == idx_fj_2) && (idx_fj_1 != -1 && idx_fj_2 != -1);
  
  return check_jets || check_fj;
}

bool check_same_top_type2(int idx_fj_1, int idx_j0_1, int idx_j1_1, int idx_j2_1, int idx_fj_2, int idx_j0_2, int idx_j1_2, int idx_j2_2)
{
  std::vector<int> list_1 = {idx_j0_1, idx_j1_1, idx_j2_1};
  std::vector<int> list_2 = {idx_j0_2, idx_j1_2, idx_j2_2};
  
  // Remove elements equal to -1
  list_1.erase(std::remove(list_1.begin(), list_1.end(), -1), list_1.end());
  list_2.erase(std::remove(list_2.begin(), list_2.end(), -1), list_2.end());
  
  std::set<int> set_1(list_1.begin(), list_1.end());
  std::set<int> set_2(list_2.begin(), list_2.end());
  
  std::set<int> intersection;
  std::set_intersection(set_1.begin(), set_1.end(), set_2.begin(), set_2.end(), std::inserter(intersection, intersection.begin()));
  
  int check_common_elements = intersection.size();
  // bool check_fj_p1 = (idx_fj_1 == -1 && idx_fj_2 != -1) || (idx_fj_1 != -1 && idx_fj_2 == -1);
  bool common_fatjet = (idx_fj_1 == idx_fj_2) && (idx_fj_1 != -1 && idx_fj_2 != -1);
  // se hanno il fatjet in comune ma che non sia per entrambi -1 
  bool sametop = true;
  if (check_common_elements==0 || (check_common_elements==1 && !common_fatjet)) sametop = false;
  return sametop;   
}

// Top Mixed, candidates over threshold of TopScore and candidates not overlapping (do not share any abject)
RVec<int> select_TopMix(rvec_f TopMixed_TopScore, rvec_f TopMixed_idxFatJet, rvec_f TopMixed_idxJet0, rvec_f TopMixed_idxJet1, rvec_f TopMixed_idxJet2, rvec_i GoodJet_idx, rvec_i GoodFatJet_idx, float wp)
{
  RVec<int> ids;
  RVec<float> scores;
  RVec<int> ids_selected;

  for (int i = 0; i < TopMixed_TopScore.size(); i++)
  {
    if( std::find(GoodJet_idx.begin(), GoodJet_idx.end(), TopMixed_idxJet0[i]) != GoodJet_idx.end() &&
        std::find(GoodJet_idx.begin(), GoodJet_idx.end(), TopMixed_idxJet1[i]) != GoodJet_idx.end() &&
        (std::find(GoodJet_idx.begin(), GoodJet_idx.end(), TopMixed_idxJet2[i]) != GoodJet_idx.end() || TopMixed_idxJet2[i] == -1) &&
        (std::find(GoodFatJet_idx.begin(), GoodFatJet_idx.end(), TopMixed_idxFatJet[i]) != GoodFatJet_idx.end() || TopMixed_idxFatJet[i] == -1)
        && TopMixed_TopScore[i] > wp)
    {
      ids.emplace_back(i);
      scores.emplace_back(TopMixed_TopScore[i]);
    }
  }
  const RVec<int> scores_indices_ = Argsort(scores);
  RVec<int> scores_indices = Reverse(scores_indices_);
  RVec<int> ids_sorted = Take(ids, scores_indices);
  RVec<float> scores_sorted = Take(scores, scores_indices);
  
  for(int i = 0; i < ids_sorted.size(); i++)
  {
    if(i==0)
    {
      ids_selected.emplace_back(ids_sorted[i]);
    }
    else 
    {
      bool same_top = false;
      int bestTop_idx = 0;
      while(!same_top and bestTop_idx < ids_selected.size())
      {
        same_top = check_same_top(TopMixed_idxFatJet[ids_sorted[i]], TopMixed_idxJet0[ids_sorted[i]], TopMixed_idxJet1[ids_sorted[i]], TopMixed_idxJet2[ids_sorted[i]], TopMixed_idxFatJet[ids_selected[bestTop_idx]], TopMixed_idxJet0[ids_selected[bestTop_idx]], TopMixed_idxJet1[ids_selected[bestTop_idx]], TopMixed_idxJet2[ids_selected[bestTop_idx]]);
        bestTop_idx += 1;
      }
      if(!same_top)
      {
        ids_selected.emplace_back(ids_sorted[i]);
      }
    }

  }
  return ids_selected;
}

RVec<int> select_TopRes(rvec_f TopResolved_TopScore, rvec_f TopResolved_idxJet0, rvec_f TopResolved_idxJet1, rvec_f TopResolved_idxJet2, rvec_i GoodJet_idx, float wp)
{
  RVec<int> ids;
  RVec<float> scores;
  RVec<int> ids_selected;
  for (int i = 0; i < TopResolved_TopScore.size(); i++)
  {
	  if(TopResolved_TopScore[i]>wp && 
        std::find(GoodJet_idx.begin(), GoodJet_idx.end(), TopResolved_idxJet0[i]) != GoodJet_idx.end() &&
        std::find(GoodJet_idx.begin(), GoodJet_idx.end(), TopResolved_idxJet1[i]) != GoodJet_idx.end() &&
        std::find(GoodJet_idx.begin(), GoodJet_idx.end(), TopResolved_idxJet2[i]) != GoodJet_idx.end())
    {
	    ids.emplace_back(i);
	    scores.emplace_back(TopResolved_TopScore[i]);
	  }
  }
  const RVec<int> scores_indices_ = Argsort(scores);
  RVec<int> scores_indices = Reverse(scores_indices_);
  RVec<int> ids_sorted = Take(ids, scores_indices);
  RVec<float> scores_sorted = Take(scores, scores_indices);

  for(int i = 0; i < ids_sorted.size(); i++)
  {
    if(i==0)
    {
      ids_selected.emplace_back(ids_sorted[i]);
    }
    else 
    {
      bool same_top = false;
      int bestTop_idx = 0;
      while(!same_top and bestTop_idx < ids_selected.size())
      {
        same_top = check_same_top(-1, TopResolved_idxJet0[ids_sorted[i]], TopResolved_idxJet1[ids_sorted[i]], TopResolved_idxJet2[ids_sorted[i]], -1, TopResolved_idxJet0[ids_selected[bestTop_idx]], TopResolved_idxJet1[ids_selected[bestTop_idx]], TopResolved_idxJet2[ids_selected[bestTop_idx]]);
        bestTop_idx += 1;
      }
      if(!same_top)
      {
        ids_selected.emplace_back(ids_sorted[i]);
      }
    }

  }
  return ids_selected;
}

Int_t nTop(rvec_i ids)
{
  return ids.size();
}

Int_t select_TopCategory(rvec_i TightTopMer_idx, rvec_i TightTopMix_idx, rvec_i TightTopRes_idx, rvec_i LooseNotTightTopMer_idx, rvec_i LooseNotTightTopMix_idx, rvec_i LooseNotTightTopRes_idx)
{
  //return:  1- Event Resolved, 2- Event Mixed, 3- Event Merged, 4- Event Nothing, ...

  int nTightRes = TightTopRes_idx.size();
  int nTightMix = TightTopMix_idx.size();
  int nTightMer = TightTopMer_idx.size();
  int nLooseRes = LooseNotTightTopRes_idx.size();
  int nLooseMix = LooseNotTightTopMix_idx.size();
  int nLooseMer = LooseNotTightTopMer_idx.size();

  // SRs with top tight 
  if (nTightRes==1 && nTightMix==0 && nTightMer==0){
    return 1;
  }
  else if (nTightRes<=1 && nTightMix==1 && nTightMer==0){
    return 2;
  }
  else if ((nTightRes==0 && nTightMix==0 && nTightMer==1) || (nTightRes<=1 && nTightMix==1 && nTightMer==1)){
    return 3;
  }

  // da qua vanno sviluppate le CR quindi vanno definite 4,5,6 dove si chiedono 0 top tight ma ne esistono di loose 
  else if (nLooseRes==1 && nLooseMix==0 && nLooseMer==0){
    return 4;
  }
  else if (nLooseRes<=1 && nLooseMix==1 && nLooseMer==0){
    return 5;
  }
  else if ((nLooseRes==0 && nLooseMix==0 && nLooseMer==1) || (nLooseRes<=1 && nLooseMix==1 && nLooseMer==1)){
    return 6;
  }
  else 
  {
    return 7;
  }
}

Int_t select_bestTop(int EventTopCategory, rvec_f FatJet_particleNet_TvsQCD, rvec_f TopMixed_TopScore, rvec_f TopResolved_TopScore){
  //RVec<int> topselect ;
  //int bestTop_idx;
  RVec<float> scores;
  int idx;
  if (EventTopCategory==3){ 
    //topselect = GoodTopMer_idx;
    for(int i = 0; i < FatJet_particleNet_TvsQCD.size(); i++)
    {
      scores.emplace_back(FatJet_particleNet_TvsQCD[i]);
    }
    idx = ArgMax(scores);
  }
  else if (EventTopCategory==2){
    for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      scores.emplace_back(TopMixed_TopScore[i]);
    }
    idx = ArgMax(scores); 
  }
  else if (EventTopCategory==1){ 
    for(int i = 0; i < TopResolved_TopScore.size(); i++)
    {
      scores.emplace_back(TopResolved_TopScore[i]);
    } 
    idx = ArgMax(scores);
  }
  else if (EventTopCategory==6){
    for(int i = 0; i < FatJet_particleNet_TvsQCD.size(); i++)
    {
      scores.emplace_back(FatJet_particleNet_TvsQCD[i]);
    }
    idx = ArgMax(scores);    
  }
  else if (EventTopCategory==5){
    for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      scores.emplace_back(TopMixed_TopScore[i]);
    }
    idx = ArgMax(scores); 
  }
  else if (EventTopCategory==4){
    for(int i = 0; i < TopResolved_TopScore.size(); i++)
    {
      scores.emplace_back(TopResolved_TopScore[i]);
    } 
    idx = ArgMax(scores);
  }
  else 
  {
    if (TopMixed_TopScore.size()>0)
    {      
      for(int i = 0; i < TopMixed_TopScore.size(); i++)
      {
        scores.emplace_back(TopMixed_TopScore[i]);
      }
      idx = ArgMax(scores); 
    }
    else if (TopResolved_TopScore.size()>0)
    {
      for(int i = 0; i < TopResolved_TopScore.size(); i++)
      {
        scores.emplace_back(TopResolved_TopScore[i]);
      } 
      idx = ArgMax(scores);
    }
    else if (FatJet_particleNet_TvsQCD.size()>0)
    {
      for(int i = 0; i < FatJet_particleNet_TvsQCD.size(); i++)
      {
        scores.emplace_back(FatJet_particleNet_TvsQCD[i]);
      }
      idx = ArgMax(scores);
    }
    else
    {
      idx = -1;
    }
  }
  return idx;
}

// Best top restricted to the candidates that define the EventTopCategory (score above WP and good jets):
// Tight*_idx for categories 1-3, LooseNOTTight*_idx for categories 4-6. Category 7 falls back to select_bestTop.
Int_t select_bestTopInCategory(int EventTopCategory, rvec_i TightTopMer_idx, rvec_i TightTopMix_idx, rvec_i TightTopRes_idx, rvec_i LooseNOTTightTopMer_idx, rvec_i LooseNOTTightTopMix_idx, rvec_i LooseNOTTightTopRes_idx, rvec_f FatJet_particleNet_TvsQCD, rvec_f TopMixed_TopScore, rvec_f TopResolved_TopScore)
{
  RVec<int> candidates;
  RVec<float> scores;
  if (EventTopCategory==1 || EventTopCategory==4)
  {
    candidates = (EventTopCategory==1) ? TightTopRes_idx : LooseNOTTightTopRes_idx;
    scores     = TopResolved_TopScore;
  }
  else if (EventTopCategory==2 || EventTopCategory==5)
  {
    candidates = (EventTopCategory==2) ? TightTopMix_idx : LooseNOTTightTopMix_idx;
    scores     = TopMixed_TopScore;
  }
  else if (EventTopCategory==3 || EventTopCategory==6)
  {
    candidates = (EventTopCategory==3) ? TightTopMer_idx : LooseNOTTightTopMer_idx;
    scores     = FatJet_particleNet_TvsQCD;
  }
  else
  {
    return select_bestTop(EventTopCategory, FatJet_particleNet_TvsQCD, TopMixed_TopScore, TopResolved_TopScore);
  }

  int idx = -1;
  for (int i = 0; i < candidates.size(); i++)
  {
    if (idx == -1 || scores[candidates[i]] > scores[idx]) idx = candidates[i];
  }
  return idx;
}

Float_t select_TopVar(Int_t EventTopCategory, Int_t Top_idx, rvec_f FatJet_pt, rvec_f TopMixed_pt, rvec_f TopResolved_pt)
{
  if (EventTopCategory==1) return TopResolved_pt[Top_idx];
  else if (EventTopCategory==2) return TopMixed_pt[Top_idx];
  else if (EventTopCategory==3) return FatJet_pt[Top_idx];
  else if (EventTopCategory==4) return TopResolved_pt[Top_idx];
  else if (EventTopCategory==5) return TopMixed_pt[Top_idx];
  else if (EventTopCategory==6) return FatJet_pt[Top_idx];
  else if (EventTopCategory==7) 
  {
    if (TopMixed_pt.size()>0) return TopMixed_pt[Top_idx];
    else if (TopResolved_pt.size()>0) return TopResolved_pt[Top_idx];
    else if (FatJet_pt.size()>0) return FatJet_pt[Top_idx];
    else return -10000.0;
  }
  else return -10000.0;
}

// ########################################################
// ############## TopClusters  ############################
// ########################################################
// NB: queste funzioni vanno debuggate

// return the list of indices of tops that share the same objects, at least 1 (fatjet and/or jets)
// this is our definition of top cluster
// To be clear, we define clusters starting from the best Top (best Top = Top with highest score),
// then we collect all the tops that share object with the fist one, and so on

// utiliziamo il fatto che posso storare una lista di liste in RDataFrame e poi raggiungere tutti gli elementi

RVec<RVec<int>> findTopClustersType1(rvec_f TopMixed_TopScore, rvec_f TopMixed_idxFatJet, rvec_f TopMixed_idxJet0, rvec_f TopMixed_idxJet1, rvec_f TopMixed_idxJet2)
{
  RVec<int> idxFatJet;
  if (TopMixed_idxFatJet.size() != TopMixed_TopScore.size())
  {
    RVec<int> tmp_idx;
    for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      tmp_idx.emplace_back(-1);
    }
    idxFatJet = tmp_idx;
  }
  else{idxFatJet = idxFatJet;}

  RVec<RVec<int>> clusters;
  const RVec<int> scores_indices_ = Argsort(TopMixed_TopScore);
  RVec<int> scores_indices = Reverse(scores_indices_);
  RVec<int> tmp;
  for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      tmp.emplace_back(i);
    }
  RVec<int> ids_sorted = Take(tmp, scores_indices);

  // ids_sorted is the list of indices of tops sorted by score we need to loop
  RVec<int> survived_top = ids_sorted;
  while(survived_top.size()!=0)
    {
      int fixedtop = survived_top[0];
      RVec<int> cluster;
      cluster.emplace_back(fixedtop);
      RVec<int> tokeep;
      for(int i = 1; i < survived_top.size(); i++)
      {
        if(check_same_top(idxFatJet[fixedtop], TopMixed_idxJet0[fixedtop], TopMixed_idxJet1[fixedtop], TopMixed_idxJet2[fixedtop], idxFatJet[survived_top[i]], TopMixed_idxJet0[survived_top[i]], TopMixed_idxJet1[survived_top[i]], TopMixed_idxJet2[survived_top[i]]))
        {
          cluster.emplace_back(survived_top[i]);
        }
        else
        {
          tokeep.emplace_back(i);
        }
      }
      survived_top = Take(survived_top, tokeep);
      clusters.emplace_back(cluster);
    }
  return clusters;
}

// return the list of indices of tops that share the same objects, at least 2 (fatjet and/or jets)
// this is our definition of top cluster
// To be clear, we define clusters starting from the best Top (best Top = Top with highest score),
// then we collect all the tops that share object with the fist one, and so on

// utiliziamo il fatto che posso storare una lista di liste in RDataFrame e poi raggiungere tutti gli elementi

RVec<RVec<int>> findTopClustersType2(rvec_f TopMixed_TopScore, rvec_f TopMixed_idxFatJet, rvec_f TopMixed_idxJet0, rvec_f TopMixed_idxJet1, rvec_f TopMixed_idxJet2)
{
  RVec<int> idxFatJet;
  if (TopMixed_idxFatJet.size() != TopMixed_TopScore.size())
  {
    RVec<int> tmp_idx;
    for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      tmp_idx.emplace_back(-1);
    }
    idxFatJet = tmp_idx;
  }
  else{idxFatJet = idxFatJet;}

  RVec<RVec<int>> clusters;
  const RVec<int> scores_indices_ = Argsort(TopMixed_TopScore);
  RVec<int> scores_indices = Reverse(scores_indices_);
  RVec<int> tmp;
  for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      tmp.emplace_back(i);
    }
  RVec<int> ids_sorted = Take(tmp, scores_indices);

  // ids_sorted is the list of indices of tops sorted by score we need to loop
  RVec<int> survived_top = ids_sorted;
  while(survived_top.size()!=0)
    {
      int fixedtop = survived_top[0];
      RVec<int> cluster;
      cluster.emplace_back(fixedtop);
      RVec<int> tokeep;
      for(int i = 1; i < survived_top.size(); i++)
      {
        if(check_same_top_type2(idxFatJet[fixedtop], TopMixed_idxJet0[fixedtop], TopMixed_idxJet1[fixedtop], TopMixed_idxJet2[fixedtop], idxFatJet[survived_top[i]], TopMixed_idxJet0[survived_top[i]], TopMixed_idxJet1[survived_top[i]], TopMixed_idxJet2[survived_top[i]]))
        {
          cluster.emplace_back(survived_top[i]);
        }
        else
        {
          tokeep.emplace_back(i);
        }
      }
      survived_top = Take(survived_top, tokeep);
      clusters.emplace_back(cluster);
    }
  return clusters;
}

// return a bool that is true if one of the tops in the cluster is tagged as real top
RVec<int> MCTaggedTopCluster(rvec_rvec_i topcluster, rvec_i TopMixed_truth)
{
  RVec<int> tagged;
  for (int i = 0; i < topcluster.size(); i++)
  {
    int flag = 0;
    for(int j = 0; j < topcluster[i].size(); j++)
    {
      if (TopMixed_truth[topcluster[i][j]] == 1)
      {
        flag =1;
      }
    }
    if (flag){tagged.emplace_back(1);}
    else{tagged.emplace_back(0);
  }
  }
  return tagged;
}

// return a bool that is true if one of the tops in the cluster is selected as top
RVec<int> RecoTaggedTopClusterMixed(rvec_rvec_i topcluster, rvec_i TopMixed_TopScore)
{
  RVec<int> tagged;

  for (int i = 0; i < topcluster.size(); i++)
  {
    int flag = 0;
    for(int j = 0; j < topcluster[i].size(); j++)
    {
      if (TopMixed_TopScore[topcluster[i][j]] >= TopMix_trs_5fpr)
      {
        flag =1;
      }
    }
    if (flag){tagged.emplace_back(1);}
    else{tagged.emplace_back(0);
  }
  }
  return tagged;
}
RVec<int> RecoTaggedTopClusterResolved(rvec_rvec_i topcluster, rvec_i TopResolved_TopScore)
{
  RVec<int> tagged;

  for (int i = 0; i < topcluster.size(); i++)
  {
    int flag = 0;
    for(int j = 0; j < topcluster[i].size(); j++)
    {
      if (TopResolved_TopScore[topcluster[i][j]] >= TopRes_trs_5fpr)
      {
        flag =1;
      }
    }
    if (flag){tagged.emplace_back(1);}
    else{tagged.emplace_back(0);
  }
  }
  return tagged;
}

// ########################################################
// ##############   TopUtils   ############################
// ########################################################


// ---------------------------------------------


Int_t select_TopCategoryWithTruth(int EventTopCategory, rvec_i FatJet_matched, rvec_i GoodTopMer_idx, rvec_i TopMixed_truth, rvec_i GoodTopMix_idx, rvec_i TopResolved_truth, rvec_i GoodTopRes_idx)
{
  int category;
  if(EventTopCategory==1)
  {
    for(int i = 0; i < GoodTopRes_idx.size(); i++)
    {
      if (TopResolved_truth[GoodTopRes_idx[i]]==1) 
      {
        category = 1;
      }
    }
  }
  else if(EventTopCategory==2)
  {
    for(int i = 0; i < GoodTopMix_idx.size(); i++)
    {
      if (TopMixed_truth[GoodTopMix_idx[i]]==1)
      {
        category = 2;
      } 
    }
  }
  else if(EventTopCategory==3)
  {
    for(int i = 0; i < GoodTopMer_idx.size(); i++)
    {
      if (FatJet_matched[GoodTopMer_idx[i]]==3)
      {
        category = 3;
      } 
    }
  }
  else if (EventTopCategory==4) 
  {
    for(int i = 0; i < GoodTopRes_idx.size(); i++)
    {
      if (TopResolved_truth[GoodTopRes_idx[i]]==1)
      {
        category = 4;
      } 
    }
    for(int i = 0; i < GoodTopMix_idx.size(); i++)
    {
      if (TopMixed_truth[GoodTopMix_idx[i]]==1)
      {
        category = 4;
      } 
    }
    for(int i = 0; i < GoodTopMer_idx.size(); i++)
    {
      if (FatJet_matched[GoodTopMer_idx[i]]==3)
      {
        category = 4;
      } 
    }
  }
  else
  {
    category = -1;
  }
  return category;
}

Float_t TopIsolation_NJets( int EventTopCategory, int Top_idx, rvec_i TopMixed_idxFatJet, rvec_i TopMixed_idxJet0, rvec_i TopMixed_idxJet1, rvec_i TopMixed_idxJet2, rvec_f TopMixed_pt, rvec_f TopMixed_phi, rvec_f TopMixed_eta, rvec_i TopResolved_idxJet0, rvec_i TopResolved_idxJet1, rvec_i TopResolved_idxJet2, rvec_f TopResolved_pt,  rvec_f TopResolved_phi, rvec_f TopResolved_eta, rvec_f FatJet_pt, rvec_f FatJet_eta, rvec_f FatJet_phi, rvec_i FatJet_jetId, rvec_f Jet_pt, rvec_f Jet_eta, rvec_f Jet_phi, rvec_f Jet_jetId, float valR, int b)
{
  Float_t njet_near = 0;
  Float_t pt_near = 0;
  Float_t pt_isolation = 0;

  if(EventTopCategory == 1) //resolved
  {
    for(int i = 0; i<Jet_pt.size(); i++)
    {
      if((Jet_pt[i]>30 && Jet_jetId[i]==6) && deltaR(Jet_eta[i], Jet_phi[i], TopResolved_eta[Top_idx], TopResolved_phi[Top_idx])<valR)
      {
        if(i!=TopResolved_idxJet0[Top_idx] && i!=TopResolved_idxJet1[Top_idx] && i!=TopResolved_idxJet2[Top_idx])
        {
          njet_near += 1;
          pt_near += Jet_pt[i];
        }
      }
    }
    pt_isolation = static_cast<Float_t>(pt_near)/static_cast<Float_t>(TopResolved_pt[Top_idx]);
  }
  else if(EventTopCategory == 2) //mixed
  {
    for(int i = 0; i<Jet_pt.size(); i++)
    {
      if((Jet_pt[i]>30 && Jet_jetId[i]==6) && deltaR(Jet_eta[i], Jet_phi[i], TopMixed_eta[Top_idx], TopMixed_phi[Top_idx])<valR)
      {
        if(i!=TopMixed_idxJet0[Top_idx] && i!=TopMixed_idxJet1[Top_idx] && i!=TopMixed_idxJet2[Top_idx])
        {
          njet_near += 1;
          pt_near += Jet_pt[i];
        }
      }
    }
    for(int i = 0; i<FatJet_pt.size(); i++)
    {
      if((FatJet_pt[i]>30 && FatJet_jetId[i]==6) && deltaR(FatJet_eta[i], FatJet_phi[i], TopMixed_eta[Top_idx], TopMixed_phi[Top_idx])<valR)
      {
        if(i!=TopMixed_idxFatJet[Top_idx])
        {
          njet_near += 1;
          pt_near += FatJet_pt[i];
        }
      }
    }
    pt_isolation = static_cast<Float_t>(pt_near)/static_cast<Float_t>(TopMixed_pt[Top_idx]);
  }
  else if(EventTopCategory == 3) //merged
  {
    for(int i = 0; i<FatJet_pt.size(); i++)
    {
      if((FatJet_pt[i]>30 && FatJet_jetId[i]==6) && deltaR(FatJet_eta[i], FatJet_phi[i], FatJet_eta[Top_idx], FatJet_phi[Top_idx])<valR)
      {
        if(i!=TopMixed_idxFatJet[Top_idx])
        {
          njet_near += 1;
          pt_near += FatJet_pt[i];
        }
      }
    }
    pt_isolation = static_cast<Float_t>(pt_near)/static_cast<Float_t>(FatJet_pt[Top_idx]);
  }
  else
  {
    pt_isolation = -1.;
    njet_near = -1.;
  }

  Float_t var_to_return;
  if( b == 1)
  {
    var_to_return = static_cast<Float_t>(pt_isolation);
  } 
  else if( b== 0)
  { 
    var_to_return = njet_near;
  }
  return var_to_return;
}

// Leptonic
int BJetTopLep_MCtag(rvec_i Jet_matched, rvec_i Jet_pdgId, rvec_i Jet_topMother, int BJetTopLep)
{
    int t = 0, tbar = 0;
    int tagged = 0;
    for(int i = 0; i< Jet_topMother.size(); i++)
    {
      if(Jet_topMother[i] == 6)  t +=1;
      if(Jet_topMother[i] == -6) tbar +=1;
    }
    if(Jet_matched[BJetTopLep] == 1 && Jet_pdgId[BJetTopLep] == 5 && ((t==1 && Jet_topMother[BJetTopLep]==6)||(tbar==1 && Jet_topMother[BJetTopLep]==-6)))
    {
      tagged = 1;
    }
    return tagged;
}

//////
float genpartTopPt(rvec_f GenPart_pt, rvec_i GenPart_pdgId, rvec_i GenPart_genPartIdxMother, rvec_i GenPart_genPartIdxMother_prompt)
{
  float top_pt = -1;
  bool ptfilled = false;
  for(int i = 0; i < GenPart_pt.size(); i++)
  {
    if(abs(GenPart_pdgId[i]) <= 5 && abs(GenPart_pdgId[GenPart_genPartIdxMother_prompt[i]])==24 && abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother_prompt[i]]])==6)
    {
      top_pt = GenPart_pt[i];
      ptfilled = true;
    }
    if(ptfilled) break;
  }

  return top_pt;
}


////// Matching between Top Candidates and Gen Tops requiring their deltaR to be below a certain threshold
Int_t TopMatched_to_GenTop_with_dR(rvec_f TopGenTopPart_eta, rvec_f TopGenTopPart_phi, float BestTopCand_eta, float BestTopCand_phi, float deltaR_thr)
{
  if(TopGenTopPart_eta.size()==0) // no gen tops in the event (QCD, etc.)
  {
    return 0;
  }
  
  Int_t matched = 0;
  for(int i = 0; i < TopGenTopPart_eta.size(); i++)
  {
    if(deltaR(TopGenTopPart_eta[i], TopGenTopPart_phi[i], BestTopCand_eta, BestTopCand_phi) < deltaR_thr)
    {
      matched = 1;
      break;
    }
  }
  return matched;
}

RVec<int> JetBTag_NotInsideBestTopCand_idx(rvec_i JetBTag_idx, rvec_i TopCand_idxJet0, rvec_i TopCand_idxJet1, rvec_i TopCand_idxJet2, int BestTopCand_idx)
{
  int jet0 = TopCand_idxJet0[BestTopCand_idx];
  int jet1 = TopCand_idxJet1[BestTopCand_idx];
  int jet2 = TopCand_idxJet2[BestTopCand_idx];

  RVec<int> bjets_not_in_tophadr;
  for(int i = 0; i < JetBTag_idx.size(); i++)
  {
    if(JetBTag_idx[i] != jet0 && JetBTag_idx[i] != jet1 && JetBTag_idx[i] != jet2)
    {
      bjets_not_in_tophadr.emplace_back(JetBTag_idx[i]);
    }
  }
  return bjets_not_in_tophadr;
}

////// Return indexes of b-jets that are matched to good muons within deltaR < 2.0
RVec<int> idx_of_bJetsMatched_to_GoodMuon_with_dR(rvec_i GoodMu_idx, rvec_f Muon_eta, rvec_f Muon_phi, rvec_i JetBTag_idx, rvec_f Jet_eta, rvec_f Jet_phi, float deltaR_thr)
{
  RVec<int> b;
  if (JetBTag_idx.size() == 0 || GoodMu_idx.size() == 0)
  {
    return b;
  }
  for(int i=0; i < JetBTag_idx.size(); i++)
  {
    bool alreadycounted = false;
    
    for(int m=0; m < GoodMu_idx.size(); m++)
    {
      if(deltaR(Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]], Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]) < deltaR_thr) 
      {
        b.emplace_back(JetBTag_idx[i]);
        alreadycounted = true;
      }
      if(alreadycounted) 
      {
          break;
      }
    }
    
  }
  return b;
}

////// Return dR(bjet,mu) of b-jets that are matched to good muons within deltaR < 2.0
RVec<float> dR_of_bJetsMatched_to_GoodMuon_with_dR(rvec_i GoodMu_idx, rvec_f Muon_eta, rvec_f Muon_phi, rvec_i JetBTag_idx, rvec_f Jet_eta, rvec_f Jet_phi, float deltaR_thr, float BestTopCand_eta, float BestTopCand_phi)
{
  RVec<float> b;
  if (JetBTag_idx.size() == 0 || GoodMu_idx.size() == 0)
  {
    return b;
  }
  for(int i=0; i < JetBTag_idx.size(); i++)
  {
    bool alreadycounted = false;
    
    for(int m=0; m < GoodMu_idx.size(); m++)
    {
      if(deltaR(BestTopCand_eta, BestTopCand_phi, Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]]) >= 1.2) // require that the b-jet is not coming from the hadronic top candidate
      {
        if(deltaR(BestTopCand_eta, BestTopCand_phi, Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]) >= 1.2) // require that the muon is not coming from the hadronic top candidate
        {
          if(deltaR(Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]], Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]) < deltaR_thr) // if the b-jet is matched to the good muon within the deltaR threshold
          {
            b.emplace_back(deltaR(Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]], Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]));
            alreadycounted = true;
          }
        }
      }
      if(alreadycounted)
      {
          break;
      }
    }
    
  }
  return b;
}

// Return dR(bjet,mu) of b-jets that are matched to good muons within deltaR_min < deltaR < 2.0
RVec<float> dR_bJets_to_GoodMuons_within_dRthr(rvec_i GoodMu_idx, rvec_f Muon_eta, rvec_f Muon_phi, rvec_i JetBTag_idx, rvec_f Jet_eta, rvec_f Jet_phi, float deltaR_min, float deltaR_thr)
{
  RVec<float> dR_sel;
  RVec<int> b_sel;
  RVec<int> m_sel;

  if (JetBTag_idx.size() == 0 || GoodMu_idx.size() == 0)
  {
    return dR_sel;
  }
  for(int i=0; i < JetBTag_idx.size(); i++)
  {
    for(int m=0; m < GoodMu_idx.size(); m++)
    {
      float dR = deltaR(Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]], Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]);
      if(dR < deltaR_thr && dR >= deltaR_min)
      {
        dR_sel.emplace_back(dR);
        b_sel.emplace_back(JetBTag_idx[i]);
        m_sel.emplace_back(GoodMu_idx[m]);
      }
    }
  }

  return dR_sel;
}

// Return index of b-jets that are matched to good muons within deltaR_min < deltaR < 2.0
RVec<float> bidx_bJets_to_GoodMuons_within_dRthr(rvec_i GoodMu_idx, rvec_f Muon_eta, rvec_f Muon_phi, rvec_i JetBTag_idx, rvec_f Jet_eta, rvec_f Jet_phi, float deltaR_min, float deltaR_thr)
{
  RVec<float> dR_sel;
  RVec<int> b_sel;
  RVec<int> m_sel;

  if (JetBTag_idx.size() == 0 || GoodMu_idx.size() == 0)
  {
    return b_sel;
  }
  for(int i=0; i < JetBTag_idx.size(); i++)
  {
    for(int m=0; m < GoodMu_idx.size(); m++)
    {
      float dR = deltaR(Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]], Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]);
      if(dR < deltaR_thr && dR >= deltaR_min)
      {
        dR_sel.emplace_back(dR);
        b_sel.emplace_back(JetBTag_idx[i]);
        m_sel.emplace_back(GoodMu_idx[m]);
      }
    }
  }

  return b_sel;
}

// Return index of muons that are matched to good muons within deltaR_min < deltaR < 2.0
RVec<float> midx_bJets_to_GoodMuons_within_dRthr(rvec_i GoodMu_idx, rvec_f Muon_eta, rvec_f Muon_phi, rvec_i JetBTag_idx, rvec_f Jet_eta, rvec_f Jet_phi, float deltaR_min, float deltaR_thr)
{
  RVec<float> dR_sel;
  RVec<int> b_sel;
  RVec<int> m_sel;

  if (JetBTag_idx.size() == 0 || GoodMu_idx.size() == 0)
  {
    return m_sel;
  }
  for(int i=0; i < JetBTag_idx.size(); i++)
  {
    for(int m=0; m < GoodMu_idx.size(); m++)
    {
      float dR = deltaR(Jet_eta[JetBTag_idx[i]], Jet_phi[JetBTag_idx[i]], Muon_eta[GoodMu_idx[m]], Muon_phi[GoodMu_idx[m]]);
      if(dR < deltaR_thr && dR >= deltaR_min)
      {
        dR_sel.emplace_back(dR);
        b_sel.emplace_back(JetBTag_idx[i]);
        m_sel.emplace_back(GoodMu_idx[m]);
      }
    }
  }

  return m_sel;
}


// #########################################
// ############## Muon SF     ##############
// #########################################
float GetMuonSF(std::string json_file, rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_tightId, rvec_i Muon_pfIsoId, rvec_f Muon_minDeltaR_fromGoodJets, std::string unc){
  auto cset = correction::CorrectionSet::from_file(json_file);
  auto MuonSF_corr = cset->at("NUM_HLT_DEN_TrkHighPtTightRelIsoProbes");
  RVec<int> ids = TightMuon_idx(Muon_pt, Muon_eta, Muon_tightId, Muon_pfIsoId, Muon_minDeltaR_fromGoodJets);
  float muon_eta = Muon_eta[ids[0]];
  float muon_pt = Muon_pt[ids[0]];
  float weight = 1.0;
  if (muon_pt >= 50){
    weight = MuonSF_corr->evaluate({muon_eta, muon_pt, unc});
  }
  return weight;
}

// #########################################
// ############## Utilities   ##############
// #########################################

float TransverseMass_part1part2(float pt1, float phi1, float pt2, float phi2)
{
  return sqrt(2*pt1*pt2*(1-cos(deltaPhi(phi1,phi2))));
}

float WtoLNu_pt(float lep_pt, float lep_eta, float lep_phi, float lep_mass, float nu_pt, float nu_eta, float nu_phi, float nu_mass)
{
  TLorentzVector lep;
  TLorentzVector nu;
  lep.SetPtEtaPhiM(lep_pt, lep_eta, lep_phi, lep_mass);
  nu.SetPtEtaPhiM(nu_pt, nu_eta, nu_phi, nu_mass);

  float W_pt = (lep + nu).Pt();
  return W_pt;
}

float WtoLNu_phi(float lep_pt, float lep_eta, float lep_phi, float lep_mass, float nu_pt, float nu_eta, float nu_phi, float nu_mass)
{
  TLorentzVector lep;
  TLorentzVector nu;
  lep.SetPtEtaPhiM(lep_pt, lep_eta, lep_phi, lep_mass);
  nu.SetPtEtaPhiM(nu_pt, nu_eta, nu_phi, nu_mass);

  float W_phi = (lep + nu).Phi();
  return W_phi;
}

// ################################################
// ############## Top pT reweighting ##############
// ################################################
int countTopGenLep(rvec_i pdgId, rvec_i motherIdx, rvec_i motherIdx_prompt, rvec_i statusFlags)
{
  int nLeptonicTops = 0;
  for (int i = 0; i < pdgId.size(); ++i) 
  {
    if (abs(pdgId[i]) == 11 || abs(pdgId[i]) == 13 || abs(pdgId[i]) == 15) // ele, mu, tau
    {
      if ((abs(pdgId[motherIdx[i]]) == 24) && (statusFlags[motherIdx[i]] & (1 << 13))) // the mother of the lepton is a W boson
      {
        if ((abs(pdgId[motherIdx_prompt[motherIdx[i]]]) == 6) && (statusFlags[motherIdx_prompt[motherIdx[i]]] & (1 << 13))) // the mother of the W boson is a top quark (last copy)
        {
          nLeptonicTops++;
        }
      } 
    }
  }
  return nLeptonicTops;
}

RVec<int> TopGenLep_genPartIdx(rvec_i pdgId, rvec_i motherIdx, rvec_i motherIdx_prompt, rvec_i statusFlags)
{
  RVec<int> idx = {};
  for (int i = 0; i < pdgId.size(); ++i) 
  {
    if (abs(pdgId[i]) == 11 || abs(pdgId[i]) == 13 || abs(pdgId[i]) == 15) // ele, mu, tau
    {
      if ((abs(pdgId[motherIdx[i]]) == 24) && (statusFlags[motherIdx[i]] & (1 << 13))) // the mother of the lepton is a W boson
      {
        if ((abs(pdgId[motherIdx_prompt[motherIdx[i]]]) == 6) && (statusFlags[motherIdx_prompt[motherIdx[i]]] & (1 << 13))) // the mother of the W boson is a top quark (last copy)
        {
          idx.emplace_back(motherIdx_prompt[motherIdx[i]]);
        }
      } 
    }
  }
  return idx;
}

RVec<float> TopGenLep_var(rvec_i TopGenLep_idx, rvec_f GenPart_var)
{
  RVec<float> var;
  for (int i = 0; i < TopGenLep_idx.size(); ++i)
  {
    var.emplace_back(GenPart_var[TopGenLep_idx[i]]);
  }
  return var;
}

float topPtReweighting(float top_pt, float antitop_pt)
{
  // TOP PAG twiki for Top pT reweighting: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
  // if (top_pt > 500) // the reweighting is only defined up to 500 GeV, above that we keep the weight constant at the value it has at 500 GeV (according to the recommendation of the TOP PAG: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting)
  // {
  //   top_pt = 500;
  // }
  // if (antitop_pt > 500)
  // {
  //   antitop_pt = 500;
  // }
  // float q = 0.0615;
  // float m = -0.0005;
  // float w = sqrt(exp(m*top_pt + q) * exp(m*antitop_pt + q));


  float sf_top = (0.103*exp(-0.0118*top_pt)-0.000134*top_pt+0.973)*(0.991+0.000075*top_pt);
  float sf_antitop = (0.103*exp(-0.0118*antitop_pt)-0.000134*antitop_pt+0.973)*(0.991+0.000075*antitop_pt);
  float w = sqrt(sf_top * sf_antitop);
  return w;
}


////////////////
/// Trota SF ///
////////////////

////// Matching between Top Candidates and Gen Tops requiring their deltaR to be below a certain threshold
RVec<int> TopMatched_to_GenTop_with_dR(rvec_f TopGenTopPart_eta, rvec_f TopGenTopPart_phi, rvec_f TopCand_eta, rvec_f TopCand_phi, float deltaR_thr)
{
  RVec<int> matched;
  if(TopGenTopPart_eta.size()==0) // no gen tops in the event (QCD, etc.)
  {
    for(int j = 0; j < TopCand_eta.size(); j++)
    {      
      matched.push_back(0);
    }
  }
  else
  {
    for(int j = 0; j < TopCand_eta.size(); j++)
    {
      int matching_found = 0;
      for(int i = 0; i < TopGenTopPart_eta.size(); i++)
      {
        if(deltaR(TopGenTopPart_eta[i], TopGenTopPart_phi[i], TopCand_eta[j], TopCand_phi[j]) < deltaR_thr)
        {
          matching_found = 1;
          break;
        }
      }
      matched.push_back(matching_found);
    }
  }
  return matched;
}

////// Definition of the process category for each top candidate based on the matching to gen tops and on the sample process (TT, TW, QCD, etc.)
////// 0: topmatched, 1: notmatched, 2: other
RVec<int> top_process_category(std::string sample_process, rvec_i TopTruth_MatchedToGenTop)
{
  RVec<int> top_process;
  for(int i = 0; i < TopTruth_MatchedToGenTop.size(); i++)
  {
    if (TopTruth_MatchedToGenTop[i] == 1)
    {
      if(sample_process == "TT" || sample_process == "TW" || sample_process == "TprimeToTZ")
      {
        top_process.push_back(0);
      }
    }
    else if (TopTruth_MatchedToGenTop[i] == 0)
    {
      if(sample_process == "TT" || sample_process == "TW" || sample_process == "TprimeToTZ")
      {
        top_process.push_back(1);
      }
      else if(sample_process == "QCD" || sample_process == "ZJetsToNuNu" || sample_process == "WJets")
      {
        top_process.push_back(2);
      }
    }
  }
  return top_process;
}

////// Calculate the Trota SF for each top candidate of a given category
RVec<float> GetTrotaSF(std::string corrLibFilePath, std::string TopCat, rvec_i TopCandidate_TagCat, rvec_f TopCandidate_score, float wpLoose, float wpTight, rvec_f TopCandidate_pt, std::string scenario){
  /**
  * @brief Compute the Trota scale factor for each top candidate.
  *
  * This function loops over all top candidates and evaluates the
  * "TrotaScaleFactors" correction from a CorrectionLib JSON file.
  *
  * For each candidate:
  * - read its score, pT, and tag category
  * - determine whether it belongs to the "pass" or "fail" region
  *   according to the tagger working points
  * - evaluate the scale factor with CorrectionLib using:
  *     {TopCat, wpTag, TagCat, channel, "value", pt}
  * - store the resulting weight in the output vector
  *
  * @param corrLibFilePath Path to the CorrectionLib JSON file.
  * @param TopCat Top category string passed to the correction: Resolved, Mixed, Merged.
  * @param TopCandidate_TagCat Per-candidate tag category: 0-->topmatched, 1-->nonmatched, 2-->other.
  * @param TopCandidate_score Per-candidate Trota score.
  * @param wpLoose Loose working-point threshold used to define pass/fail.
  * @param wpTight Tight working-point threshold used to define pass/fail.
  * @param TopCandidate_pt Per-candidate transverse momentum used in the SF evaluation.
  * @param scenario String to select whether to return nominal SF ("nominal") or systematic variations ("up"/"down").
  *
  * @return RVec<float> weights containing one scale factor per top candidate.
  *
  * @note The function assumes that all input vectors have the same size.
  */

  auto cset             = correction::CorrectionSet::from_file(corrLibFilePath);
  auto trotaSF_corr     = cset->at("TrotaScaleFactors");
  RVec<float> weights_nominal;
  RVec<float> weights_up;
  RVec<float> weights_down;
  RVec<float> errors;
  for (int i = 0; i < TopCandidate_pt.size(); i++)
  {
    float score   = TopCandidate_score[i];
    float pt      = TopCandidate_pt[i];
    std::string TagCat;
    std::string channel;
    std::string wpTag;
    float weight  = 1.0;
    float error   = 0.0;

    if (TopCandidate_TagCat[i] == 0)
    {
      TagCat = "topmatched";
    }
    else if (TopCandidate_TagCat[i] == 1)
    {
      TagCat = "nonmatched";
    }
    else if (TopCandidate_TagCat[i] == 2)
    {
      TagCat = "other";
    }
  
    
    if(score >= wpTight)
    {
      wpTag   = "Tight";
      channel = "pass";
    }
    else if(score < wpTight)
    {
      if(score >= wpLoose)
      {
        wpTag   = "LooseButNotTight";
        channel = "pass";
      }
      else if(score < wpLoose)
      {
        wpTag   = "Loose";
        channel = "fail";
      }
    }

    // case a: all processes, pass and fail
    weight  = trotaSF_corr->evaluate({TopCat, wpTag, TagCat, channel, "value", pt});
    error   = trotaSF_corr->evaluate({TopCat, wpTag, TagCat, channel, "error", pt});

    // case b: all processes, only pass
    if (channel == "fail")
    {
      weight = 1.0;
      error = 0.0;
    }

    // case c: only topmatched, pass and fail
    // if (TagCat != "topmatched")
    // {
    //   weight = 1.0;
    //   error = 0.0;
    // }
    
    // case d: only topmatched, only pass
    // if ((TagCat != "topmatched") || (channel == "fail"))
    // {
    //   weight = 1.0;
    //   error = 0.0;
    // }

    weights_nominal.push_back(weight);
    weights_up.push_back(weight + error);
    weights_down.push_back(weight - error);
    errors.push_back(error);
  }
  if (scenario == "nominal")
  {
    return weights_nominal;
  }
  else if (scenario == "up")
  {
    return weights_up;
  }
  else if (scenario == "down")
  {
    return weights_down;
  }
  else
  {
    std::cout << "WARNING: GetTrotaSF: unknown scenario '" << scenario
              << "'. Returning nominal SFs." << std::endl;
    return weights_nominal;
  }
}




RVec<int> TopCandidates_NonOverlapping_AcrossTopCategories_idx(rvec_i TopIndependentCandidates_TopCategoryOne_idx, rvec_f TopCandidates_TopCategoryOne_eta, rvec_f TopCandidates_TopCategoryOne_phi, rvec_i TopIndependentCandidates_TopCategoryTwo_idx, rvec_f TopCandidates_TopCategoryTwo_eta, rvec_f TopCandidates_TopCategoryTwo_phi, float deltaR_thr)
{
  RVec<int> non_overlapping_idx;
  for (int j = 0; j < TopIndependentCandidates_TopCategoryTwo_idx.size(); j++) // Example: loop over TopMerged independent candidates
  {
    int overlap_found = 0;
    for (int i = 0; i < TopIndependentCandidates_TopCategoryOne_idx.size(); i++) // loop over TopMixed independent candidates
    {
      if (deltaR(TopCandidates_TopCategoryOne_eta[TopIndependentCandidates_TopCategoryOne_idx[i]],
                 TopCandidates_TopCategoryOne_phi[TopIndependentCandidates_TopCategoryOne_idx[i]],
                 TopCandidates_TopCategoryTwo_eta[TopIndependentCandidates_TopCategoryTwo_idx[j]],
                 TopCandidates_TopCategoryTwo_phi[TopIndependentCandidates_TopCategoryTwo_idx[j]]) < deltaR_thr)
      {
        overlap_found = 1;
        break; // if it overlaps, we do not consider it for the list of non-overlapping candidates
      }
    }
    if (overlap_found == 0) // if it does not overlap with any of the TopMixed candidates, we can consider it for the list of non-overlapping candidates
    {
      non_overlapping_idx.push_back(TopIndependentCandidates_TopCategoryTwo_idx[j]);
    }
  }
  return non_overlapping_idx;
}



////// Calculate the TrotaEventWeight for all 3 TopCategories together for each event based on the Trota SF of the selected top candidates in the event
float CalculateTrotaEventWeight(rvec_f TopMerged_TrotaSF, rvec_f TopMixed_TrotaSF, rvec_f TopResolved_TrotaSF, rvec_i TopMerged_forEvWeight_idx, rvec_i TopMixed_forEvWeight_idx, rvec_i TopResolved_forEvWeight_idx)
{
  float weight = 1.0;
  for (int i = 0; i < TopMerged_forEvWeight_idx.size(); i++)
  {
    weight *= TopMerged_TrotaSF[TopMerged_forEvWeight_idx[i]];
  }
  for (int i = 0; i < TopMixed_forEvWeight_idx.size(); i++)
  {
    weight *= TopMixed_TrotaSF[TopMixed_forEvWeight_idx[i]];
  }
  for (int i = 0; i < TopResolved_forEvWeight_idx.size(); i++)
  {
    weight *= TopResolved_TrotaSF[TopResolved_forEvWeight_idx[i]];
  }
  
  return weight;
}

////// Calculate the TrotaEventWeight for a single TopCategory (Resolved, Mixed or Merged) for each event based on the Trota SF of the selected top candidates in the event
float CalculateCategoryTrotaEventWeight(rvec_f TopCand_TrotaSF, rvec_i TopCand_forEvWeight_idx)
{
  float weight = 1.0;
  for (int i = 0; i < TopCand_forEvWeight_idx.size(); i++)
  {
    weight *= TopCand_TrotaSF[TopCand_forEvWeight_idx[i]];
  }
  
  return weight;
}

////// Calculate dR between each lepton (can be either Muon or Electron) with all good jets in the event, and return a vector of the minimum dR for each lepton
RVec<float> MinDeltaR_Lepton_Jets(rvec_f Lepton_eta, rvec_f Lepton_phi, rvec_f Jet_eta, rvec_f Jet_phi, rvec_i GoodJet_idx)
{
  RVec<float> min_dR;
  for (int i = 0; i < Lepton_eta.size(); i++)
  {
    float min_dR_i = 9999.0;
    for (int j = 0; j < GoodJet_idx.size(); j++)
    {
      float dR_ij = deltaR(Lepton_eta[i], Lepton_phi[i], Jet_eta[GoodJet_idx[j]], Jet_phi[GoodJet_idx[j]]);
      if (dR_ij < min_dR_i)
      {
        min_dR_i = dR_ij;
      }
    }
    min_dR.push_back(min_dR_i);
  }
  return min_dR;
}



namespace TopReco {

template <typename T>
inline std::vector<T> EquationSolver(const T& a, const T& b, const T& c, const T& d)
{
    std::vector<T> result;
    if (a == T(0)) return result;

    std::complex<T> x1, x2, x3;
    const T q = (T(3)*a*c - b*b) / (T(9)*a*a);
    const T r = (T(9)*a*b*c - T(27)*a*a*d - T(2)*b*b*b) / (T(54)*a*a*a);
    const T Delta = q*q*q + r*r;

    std::complex<T> s, t;
    if (Delta <= T(0)) {
        const T rho = std::sqrt(-(q*q*q));
        const T theta = std::acos(r / rho);
        s = std::polar(std::sqrt(-q),  theta / T(3));
        t = std::polar(std::sqrt(-q), -theta / T(3));
    } else {
        s = std::complex<T>(std::cbrt(r + std::sqrt(Delta)), 0);
        t = std::complex<T>(std::cbrt(r - std::sqrt(Delta)), 0);
    }

    const std::complex<T> I(0, 1);

    x1 = s + t - std::complex<T>(b / (T(3)*a), 0);
    x2 = (s + t) * std::complex<T>(-0.5, 0)
       - std::complex<T>(b / (T(3)*a), 0)
       + (s - t) * I * std::complex<T>(std::sqrt(T(3)) / T(2), 0);
    x3 = (s + t) * std::complex<T>(-0.5, 0)
       - std::complex<T>(b / (T(3)*a), 0)
       - (s - t) * I * std::complex<T>(std::sqrt(T(3)) / T(2), 0);

    if (std::abs(x1.imag()) < T(1e-4)) result.push_back(x1.real());
    if (std::abs(x2.imag()) < T(1e-4)) result.push_back(x2.real());
    if (std::abs(x3.imag()) < T(1e-4)) result.push_back(x3.real());

    return result;
}

inline ROOT::Math::PxPyPzEVector MakeP4(float pt, float eta, float phi, float mass)
{
    ROOT::Math::PtEtaPhiMVector v(pt, eta, phi, mass);
    return ROOT::Math::PxPyPzEVector(v.Px(), v.Py(), v.Pz(), v.E());
}

inline ROOT::Math::PxPyPzEVector NuMomentum(
    float leptonPx, float leptonPy, float leptonPz,
    float leptonPt, float leptonE,
    float metPx, float metPy)
{
    constexpr double mW = 80.399;
    ROOT::Math::PxPyPzEVector result(0., 0., 0., 0.);

    const double misET2 = metPx*metPx + metPy*metPy;
    const double denom  = leptonE*leptonE - leptonPz*leptonPz;

    if (std::abs(denom) < 1e-9) return result;
    if (std::abs(leptonPt) < 1e-9) return result;
    if (std::abs(leptonPx) < 1e-9) return result;

    const double mu = (mW*mW)/2. + metPx*leptonPx + metPy*leptonPy;
    const double a  = (mu * leptonPz) / denom;
    const double a2 = a*a;
    const double b  = ((leptonE*leptonE)*misET2 - mu*mu) / denom;

    double pznu = 0.;

    if (a2 - b > 0.) {
        const double root = std::sqrt(a2 - b);
        const double pz1  = a + root;
        const double pz2  = a - root;
        pznu = (std::abs(pz1) < std::abs(pz2)) ? pz1 : pz2;

        const double Enu = std::sqrt(misET2 + pznu*pznu);
        result = ROOT::Math::PxPyPzEVector(metPx, metPy, pznu, Enu);
        return result;
    }

    const double ptlep = leptonPt;
    const double pxlep = leptonPx;
    const double pylep = leptonPy;
    const double metpx = metPx;
    const double metpy = metPy;

    const double EquationA = 1.;
    const double EquationB = -3. * pylep * mW / ptlep;
    const double EquationC =
        mW*mW * (2. * pylep*pylep) / (ptlep*ptlep)
        + mW*mW
        - 4. * pxlep*pxlep*pxlep * metpx / (ptlep*ptlep)
        - 4. * pxlep*pxlep*pylep * metpy / (ptlep*ptlep);
    const double EquationD =
        4. * pxlep*pxlep * mW * metpy / ptlep
        - pylep * mW*mW*mW / ptlep;

    const auto solutions  = EquationSolver<long double>(
        (long double)EquationA, (long double)EquationB,
        (long double)EquationC, (long double)EquationD
    );
    const auto solutions2 = EquationSolver<long double>(
        (long double)EquationA, -(long double)EquationB,
        (long double)EquationC, -(long double)EquationD
    );

    double deltaMin = 14000. * 14000.;
    const double zeroValue = -mW*mW / (4. * pxlep);
    double minPx = 0.;
    double minPy = 0.;

    for (int i = 0; i < (int)solutions.size(); ++i) {
        if (solutions[i] < 0.) continue;

        const double p_x = (solutions[i]*solutions[i] - mW*mW) / (4. * pxlep);
        const double p_y = (mW*mW*pylep + 2.*pxlep*pylep*p_x - mW*ptlep*solutions[i])
                         / (2. * pxlep * pxlep);
        const double Delta2 = (p_x - metpx)*(p_x - metpx) + (p_y - metpy)*(p_y - metpy);

        if (Delta2 < deltaMin && Delta2 > 0.) {
            deltaMin = Delta2;
            minPx = p_x;
            minPy = p_y;
        }
    }

    for (int i = 0; i < (int)solutions2.size(); ++i) {
        if (solutions2[i] < 0.) continue;

        const double p_x = (solutions2[i]*solutions2[i] - mW*mW) / (4. * pxlep);
        const double p_y = (mW*mW*pylep + 2.*pxlep*pylep*p_x + mW*ptlep*solutions2[i])
                         / (2. * pxlep * pxlep);
        const double Delta2 = (p_x - metpx)*(p_x - metpx) + (p_y - metpy)*(p_y - metpy);

        if (Delta2 < deltaMin && Delta2 > 0.) {
            deltaMin = Delta2;
            minPx = p_x;
            minPy = p_y;
        }
    }

    const double pyZeroValue    = (mW*mW*pxlep + 2.*pxlep*pylep*zeroValue);
    const double delta2ZeroValue =
        (zeroValue - metpx)*(zeroValue - metpx) +
        (pyZeroValue - metpy)*(pyZeroValue - metpy);

    if (deltaMin == 14000. * 14000.) return result;

    if (delta2ZeroValue < deltaMin) {
        minPx = zeroValue;
        minPy = pyZeroValue;
    }

    const double muMinimum = (mW*mW)/2. + minPx*pxlep + minPy*pylep;
    pznu = (muMinimum * leptonPz) / denom;

    const double Enu = std::sqrt(minPx*minPx + minPy*minPy + pznu*pznu);
    result = ROOT::Math::PxPyPzEVector(minPx, minPy, pznu, Enu);
    return result;
}

inline ROOT::Math::PxPyPzEVector Top4Momentum(
    float leptonPx, float leptonPy, float leptonPz, float leptonE,
    float jetPx, float jetPy, float jetPz, float jetE,
    float metPx, float metPy)
{
    const float leptonPt = std::hypot(leptonPx, leptonPy);
    const auto nu  = NuMomentum(leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy);
    const ROOT::Math::PxPyPzEVector lep(leptonPx, leptonPy, leptonPz, leptonE);
    const ROOT::Math::PxPyPzEVector jet(jetPx, jetPy, jetPz, jetE);
    return lep + jet + nu;
}

inline ROOT::Math::PxPyPzEVector Top4MomentumFromPtEtaPhiM(
    float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
    float jet_pt,    float jet_eta,    float jet_phi,    float jet_mass,
    float met_pt,    float met_phi)
{
    const auto lep = MakeP4(lepton_pt, lepton_eta, lepton_phi, lepton_mass);
    const auto jet = MakeP4(jet_pt,    jet_eta,    jet_phi,    jet_mass);

    const float metPx = met_pt * std::cos(met_phi);
    const float metPy = met_pt * std::sin(met_phi);

    return Top4Momentum(
        lep.Px(), lep.Py(), lep.Pz(), lep.E(),
        jet.Px(), jet.Py(), jet.Pz(), jet.E(),
        metPx, metPy
    );
}

inline float TopMassFromPtEtaPhiM(
    float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
    float jet_pt,    float jet_eta,    float jet_phi,    float jet_mass,
    float met_pt,    float met_phi)
{
    return Top4MomentumFromPtEtaPhiM(
        lepton_pt, lepton_eta, lepton_phi, lepton_mass,
        jet_pt, jet_eta, jet_phi, jet_mass,
        met_pt, met_phi
    ).M();
}

inline float TopPtFromPtEtaPhiM(
    float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
    float jet_pt,    float jet_eta,    float jet_phi,    float jet_mass,
    float met_pt,    float met_phi)
{
    return Top4MomentumFromPtEtaPhiM(
        lepton_pt, lepton_eta, lepton_phi, lepton_mass,
        jet_pt, jet_eta, jet_phi, jet_mass,
        met_pt, met_phi
    ).Pt();
}

inline float TopMtwFromPtEtaPhiM(
    float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
    float jet_pt,    float jet_eta,    float jet_phi,    float jet_mass,
    float met_pt,    float met_phi)
{
    const auto lep = MakeP4(lepton_pt, lepton_eta, lepton_phi, lepton_mass);
    const auto jet = MakeP4(jet_pt,    jet_eta,    jet_phi,    jet_mass);

    const float metPx = met_pt * std::cos(met_phi);
    const float metPy = met_pt * std::sin(met_phi);

    const auto lb  = lep + jet;
    const double mlb2  = lb.M2();
    const double etlb  = std::sqrt(std::max(0.0, mlb2 + lb.Pt()*lb.Pt()));
    const double metPT = std::hypot(metPx, metPy);

    return std::sqrt(std::max(
        0.0,
        mlb2 + 2.0 * (etlb * metPT - lb.Px() * metPx - lb.Py() * metPy)
    ));
}

float TopEtaFromPtEtaPhiM(
    float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
    float jet_pt,    float jet_eta,    float jet_phi,    float jet_mass,
    float met_pt,    float met_phi)
{
    return Top4MomentumFromPtEtaPhiM(
        lepton_pt, lepton_eta, lepton_phi, lepton_mass,
        jet_pt, jet_eta, jet_phi, jet_mass,
        met_pt, met_phi
    ).Eta();
}

float TopPhiFromPtEtaPhiM(
    float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
    float jet_pt,    float jet_eta,    float jet_phi,    float jet_mass,
    float met_pt,    float met_phi)
{
    return Top4MomentumFromPtEtaPhiM(
        lepton_pt, lepton_eta, lepton_phi, lepton_mass,
        jet_pt, jet_eta, jet_phi, jet_mass,
        met_pt, met_phi
    ).Phi();
}

} // namespace TopReco