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

#include "TDavixFile.h"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;
using rvec_b = const RVec<bool> &;

const float btag_mediumWP = 0.2783;
const float TopRes_minpt=  0.;
const float TopRes_maxpt=  300.;
const float TopMix_minpt=  300.;
const float TopMix_maxpt=  500.;
const float TopMer_minpt=  500.;
const float TopMer_maxpt=  10000.;
const float TopRes_trs=  0.5411276;
const float TopMix_trs=  0.39578277;
const float TopMer_trs=  0.99;
const float dR=  0.8;

unordered_map<int,float> xsecs({
{21000, 23590000},
{21001, 1555000},
{21002, 324500},
{21003, 30310},
{21004, 6444},
{21005, 1127},
{21006, 109.8},
{21007, 21.98},
{21102, 66.85},
{21103, 16.42},
{21104, 687.1},
{21101, 687.1},
{21200, 267.0},
{21201, 73.08},
{21202, 9.904},
{21203, 2.413},
{21204, 1.071},
{21205, 0.2497},
{21206, 0.005618},
{21200, 1292},
{21201, 1395},
{21202, 407.9},
{21203, 57.48},
{21204, 12.87},
{21205, 5.366},
{21206, 1.074},
{21207, 0.008001},
{22000, 0.00045},
{22001, 0.01362},
{22002, 0.07804},
{22102, 0.7},
{22101, 0.004385},
{22100, 0.0002499},
});

unordered_map<int,float> nevents({ // ATTENTO così non puoi girare file singoli! ti manca quella informazione
{21000, 23219113.0},
{21001, 14812828.0},
{21002, 20357076.0},
{21003, 17563112.0},
{21004, 16905782.0},
{21005, 5125446.0},
{21006, 2814040.0},
{21007, 1911808.0},
{21102, 29874765.0},
{21103, 22971051.0},
{21104, 31095000.0},
{21101, 48768000.0},
{21200, 10025780.0},
{21201, 12002543.0},
{21202, 12095841.0},
{21203, 4967187.0},
{21204, 1906123.0},
{21205, 115370.0},
{21206, 17244.0},
{21200, 0},
{21201, 27914221.0},
{21202, 24428914.0},
{21203, 5932701.0},
{21204, 16074541.0},
{21205, 1903070.0},
{21206, 4874413.0},
{21207, 693087.0},
{22000, 246700.0},
{22001, 338800.0},
{22002, 389500.0},
{22102, 0},
{22101, 0},
{22100, 0},
});

float deltaPhi (float phi1, float phi2){
  float dphi = (phi1-phi2);
  while(dphi >  M_PI) dphi -= 2*M_PI;
  while(dphi < -M_PI) dphi += 2*M_PI;
  return dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2){
  return hypot(eta1 - eta2, deltaPhi(phi1, phi2)); 
}

int isMC(int Sample){
    // int digit1 = SampleFlag / 10000; // 1
    int digit2 = (Sample / 1000) % 10; // 2
    // int digit3 = (num / 100) % 10; // 3
    // int digit4 = (num / 10) % 10; // 4
    // int digit5 = num % 10; // 5    
    int a;
    if (digit2 != 0){
        a = 1;
    }
    else{
        a = 0;
    };

    return a;
}

int Year(int Sample){
    int digit1 = Sample / 10000; // 1
    if (digit1 == 0)
    {
        return 2016;
    }
    else if (digit1 == 1)
    {
        return 2017;
    }
    else if (digit1 == 2)
    {
        return 2018;
    }
    else if (digit1 == 3)
    {
        return 2022;
    }
    else if (digit1 == 4)
    {
        return 2023;
    }
    else{
        return 0;
    }
}

float getXSec(int Sample, bool IsMC){
    if (IsMC == false) return 1.;
    else{
        return  xsecs[Sample];
    }
}

float getNevents(int Sample, bool IsMC){
    if (IsMC == false) return 1.;
    else{
        return  nevents[Sample];
    }
}

RVec<int> GetGoodElectron(rvec_f Electron_pt, rvec_f Electron_eta, rvec_i Electron_mvaFall17V2Iso_WPL, rvec_f Electron_dxy)
{
  RVec<int> ids;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
      if (Electron_pt[i]>30 && abs(Electron_eta[i]) < 2.4 && Electron_mvaFall17V2Iso_WPL[i] == 1 && abs(Electron_dxy[i]) < 0.05)
      {
        ids.emplace_back(i);
      }
  }
  return ids;
}

RVec<int> GetGoodMuon(rvec_f Muon_pt, rvec_f Muon_eta, rvec_i Muon_looseId, rvec_f Muon_dxy)
{
  RVec<int> ids;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
      if (Muon_pt[i] > 30 && abs(Muon_eta[i]) < 2.4 && Muon_looseId[i] == 1 && abs(Muon_dxy[i]) < 0.2)
      {
        ids.emplace_back(i);
      }
  }
  return ids;
}

RVec<int> GetGoodJet(rvec_f Jet_pt, rvec_i Jet_jetId)
{
  RVec<int> ids;
  for(int i = 0; i<Jet_pt.size(); i++)
  {
      if (Jet_pt[i]>25 && Jet_jetId[i]>0)
      {
        ids.emplace_back(i);
      }
  }
  return ids;
}

RVec<int> GetJetBTag(rvec_i GoodJet, rvec_f Jet_btagDeepB){
    RVec<int> ids;
    for(int i = 0; i<GoodJet.size(); i++)
    {
        if (Jet_btagDeepB[GoodJet[i]]>btag_mediumWP)
        {
            ids.emplace_back(i);
        }
    }
    return ids;
}

bool atLeast1GoodLep(rvec_i GoodMu_idx, rvec_i GoodEl_idx){
    if ((GoodMu_idx.size() + GoodEl_idx.size())>=1) return true;
    else return false;
}

RVec<int> select_TopMer(rvec_f FatJet_tagger, rvec_f FatJet_pt, rvec_f FatJet_eta, rvec_f FatJet_phi)
{
  RVec<int> ids;
  for (int i = 0; i < FatJet_tagger.size(); i++)
  {
  	if(FatJet_tagger[i]>TopMer_trs && FatJet_pt[i]>TopMer_minpt && FatJet_pt[i]<TopMer_maxpt){
      ids.emplace_back(i);
	  }
  }
  return ids;
}

RVec<int> select_TopMix(rvec_f TopHighPt_score2, rvec_f TopHighPt_pt, rvec_f TopHighPt_eta, rvec_f TopHighPt_phi)
{
  RVec<int> ids;
  RVec<float> scores;
  for (int i = 0; i < TopHighPt_score2.size(); i++)
  {
  	if(TopHighPt_score2[i]>TopMix_trs && TopHighPt_pt[i]>TopMix_minpt && TopHighPt_pt[i]<TopMix_maxpt)
    {
      ids.emplace_back(i);
	    scores.emplace_back(TopHighPt_score2[i]);
	  }
  }
    
  RVec<int> ids_ = ids;
  RVec<int> ids_select;
  RVec<float> scores_ = scores;
  int n_notzero = 0;
    
  for(int j=0; j<scores_.size(); j++)
  { 
    if(scores_[j]!=0)
    {
	    n_notzero += 1;
    }
    else 
    {
	    n_notzero += 0;
    }
  }

  while(n_notzero!=0)
  {
    RVec<float> deltaRs;
    int bestTop_idx = ArgMax(scores_);
      
    for(int i = 0; i < ids_.size(); i++)
    {
	    if(i == bestTop_idx) continue;
	    if(scores_[i]!=0 && deltaR(TopHighPt_eta[bestTop_idx], TopHighPt_phi[bestTop_idx], TopHighPt_eta[i], TopHighPt_phi[i])<dR)  scores_[i]=0;
     
    }
    ids_select.emplace_back(bestTop_idx);
    scores_[bestTop_idx]=0;
    n_notzero =0;
    for(int j=0; j<scores_.size(); j++)
    { 
	    if(scores_[j]!=0)
      {
	      n_notzero += 1;
	    }
	    else 
      {
	      n_notzero += 0;
	    }
    }
  }
  return ids_select;
}

RVec<int> select_TopRes(rvec_f TopLowPt_scoreDNN, rvec_f TopLowPt_pt, rvec_f TopLowPt_eta, rvec_f TopLowPt_phi)
{
  RVec<int> ids;
  RVec<float> scores;
  for (int i = 0; i < TopLowPt_scoreDNN.size(); i++)
  {
	  if(TopLowPt_scoreDNN[i]>TopRes_trs && TopLowPt_pt[i]>TopRes_minpt && TopLowPt_pt[i]<TopRes_maxpt)
    {
	    ids.emplace_back(i);
	    scores.emplace_back(TopLowPt_scoreDNN[i]);
	  }
  }
    
  RVec<int> ids_ = ids;
  RVec<float> ids_select;
  RVec<float> scores_ = scores;
  int n_notzero = 0;
    
  for(int j=0; j<scores_.size(); j++)
  { 
    if(scores_[j]!=0)
    {
	    n_notzero += 1;
    }
    else 
    {
	    n_notzero += 0;
    }
  }

  while(n_notzero!=0)
  {
    RVec<float> deltaRs;
    int bestTop_idx = ArgMax(scores_);
      
    for(int i = 0; i < ids_.size(); i++)
    {
	    if(i == bestTop_idx) continue;
	    if(scores_[i]!=0 && deltaR(TopLowPt_eta[bestTop_idx], TopLowPt_phi[bestTop_idx], TopLowPt_eta[i], TopLowPt_phi[i])<dR)  scores_[i]=0;
    }
    ids_select.emplace_back(bestTop_idx);
    scores_[bestTop_idx]=0;
    n_notzero =0;
    for(int j=0; j<scores_.size(); j++)
    { 
      if(scores_[j]!=0)
      {
	      n_notzero += 1;
	    }
	    else 
      {
	      n_notzero += 0;
	    }
    }
  }
  return ids_select;
}

Int_t select_TopCategory(rvec_i GoodTopMer_idx, rvec_i GoodTopMix_idx, rvec_i GoodTopRes_idx){
  //return:  0- no top sel, 1- top merged, 2- top mix, 3- top resolved
  int nRes = GoodTopRes_idx.size();
  int nMix = GoodTopMix_idx.size();
  int nMer = GoodTopMer_idx.size();
  
  if (nRes>0 && nMix==0 && nMer==0){
    return 3;
  }
  else if (nRes<2 && nMix>0 && nMer==0){
    return 2;
  }
  else if (nRes==0 && nMix<2 && nMer>0){
    return 1;
  }
  else return 0;
}

Int_t select_bestTop(int EventTopCategory, rvec_i GoodTopMer_idx, rvec_i GoodTopMix_idx, rvec_i GoodTopRes_idx, rvec_f FatJet_tagger, rvec_f TopHighPt_score2, rvec_f TopLowPt_scoreDNN){
  //RVec<int> topselect ;
  //int bestTop_idx;
  RVec<float> scores;
  if (EventTopCategory==1){ 
    //topselect = GoodTopMer_idx;
    for(int i = 0; i < GoodTopMer_idx.size(); i++)
    {
      scores.emplace_back(FatJet_tagger[i]);
    }
  }
  else if (EventTopCategory==2){
    for(int i = 0; i < GoodTopMix_idx.size(); i++)
    {
      scores.emplace_back(TopHighPt_score2[i]);
    } 
  }
  else if (EventTopCategory==3){ 
    for(int i = 0; i < GoodTopRes_idx.size(); i++)
    {
      scores.emplace_back(TopLowPt_scoreDNN[i]);
    } 
  }
  else return -1;

  return ArgMax(scores);
}

Float_t select_TopVar(Int_t EventTopCategory, Int_t Top_idx, rvec_f FatJet_pt, rvec_f TopHighPt_pt, rvec_f TopLowPt_pt){
  if (EventTopCategory==1) return FatJet_pt[Top_idx];
  else if (EventTopCategory==2) return TopHighPt_pt[Top_idx];
  else if (EventTopCategory==3) return TopLowPt_pt[Top_idx];
  else return -1000;
}