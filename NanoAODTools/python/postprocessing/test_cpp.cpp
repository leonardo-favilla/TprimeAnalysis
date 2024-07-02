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
using rvec_rvec_i = const RVec<RVec<int>> &;

const float TopMix_trs=  0.7584613561630249;

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
  // cout<<"intersection "<<intersection.empty()<<endl;
  bool check_jets = !intersection.empty();

  bool check_fj = (idx_fj_1 == idx_fj_2)||(idx_fj_1 == -1 || idx_fj_2 == -1);
  
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

RVec<RVec<int>> findTopClusters(rvec_f TopMixed_TopScore, rvec_f TopMixed_idxFatJet, rvec_f TopMixed_idxJet0, rvec_f TopMixed_idxJet1, rvec_f TopMixed_idxJet2)
{
  RVec<RVec<int>> clusters;
  const RVec<int> scores_indices_ = Argsort(TopMixed_TopScore);
  RVec<int> scores_indices = Reverse(scores_indices_);
  RVec<int> tmp;
  for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      tmp.emplace_back(i);
    }
  RVec<int> ids_sorted = Take(tmp, scores_indices);
  cout<<ids_sorted<<endl;
  
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
        if(check_same_top(TopMixed_idxFatJet[fixedtop], TopMixed_idxJet0[fixedtop], TopMixed_idxJet1[fixedtop], TopMixed_idxJet2[fixedtop], TopMixed_idxFatJet[survived_top[i]], TopMixed_idxJet0[survived_top[i]], TopMixed_idxJet1[survived_top[i]], TopMixed_idxJet2[survived_top[i]]))
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

RVec<RVec<int>> findTopClusterstype2(rvec_f TopMixed_TopScore, rvec_f TopMixed_idxFatJet, rvec_f TopMixed_idxJet0, rvec_f TopMixed_idxJet1, rvec_f TopMixed_idxJet2)
{
  RVec<RVec<int>> clusters;
  const RVec<int> scores_indices_ = Argsort(TopMixed_TopScore);
  RVec<int> scores_indices = Reverse(scores_indices_);
  RVec<int> tmp;
  for(int i = 0; i < TopMixed_TopScore.size(); i++)
    {
      tmp.emplace_back(i);
    }
  RVec<int> ids_sorted = Take(tmp, scores_indices);
  cout<<ids_sorted<<endl;
  
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
        if(check_same_top_type2(TopMixed_idxFatJet[fixedtop], TopMixed_idxJet0[fixedtop], TopMixed_idxJet1[fixedtop], TopMixed_idxJet2[fixedtop], TopMixed_idxFatJet[survived_top[i]], TopMixed_idxJet0[survived_top[i]], TopMixed_idxJet1[survived_top[i]], TopMixed_idxJet2[survived_top[i]]))
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

RVec<int> MCTaggedTopCluster(rvec_rvec_i topcluster, rvec_i TopMixed_truth)
{
  RVec<int> tagged;
  for (int i = 0; i < topcluster.size(); i++)
  {
    int flag = 0;
    for(int j = 0; j < topcluster[i].size(); j++)
    {
      if (TopMixed_truth[topcluster[i][j]]){ flag =1; }
    }
    if (flag){tagged.emplace_back(1);}
    else{tagged.emplace_back(0);}
  }
  return tagged;
}

RVec<int> RecoTaggedTopClusterMixed(rvec_rvec_i topcluster, rvec_f TopMixed_TopScore)
{
  RVec<int> tagged;

  for (int i = 0; i < topcluster.size(); i++)
  {
    int flag=0;
    for(int j = 0; j < topcluster[i].size(); j++)
    {
      // cout<<"Top mixed score "<<TopMixed_TopScore[topcluster[i][j]]<<endl;
      if (TopMixed_TopScore[topcluster[i][j]] >= TopMix_trs){
        flag =1;
        cout<<"TEST"<<endl;}
    }

    if (flag==1){tagged.emplace_back(1);}
    else{tagged.emplace_back(0);
  }
  }
  return tagged;
}

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

RVec<int> UniqueFlavList(int idxJet0, int idxJet1, int idxJet2, bool debug) 
{
  if(debug){
    cout<<"pdgIdidxJet0 "<<idxJet0<<endl;
    cout<<"pdgIdidxJet1 "<<idxJet1<<endl;
    cout<<"pdgIdidxJet2 "<<idxJet2<<endl;
  }
  RVec<int> common_element = Intersect(get_pos_nums(idxJet0), get_pos_nums(idxJet1));
  RVec<int> tmp_ = SetDifference(get_pos_nums(idxJet1), common_element);
  RVec<int> jetflavs_list_ = Concatenate(get_pos_nums(idxJet0), tmp_);
  RVec<int> common_element_ = Intersect(jetflavs_list_, get_pos_nums(idxJet2));
  RVec<int> tmp__ = SetDifference(get_pos_nums(idxJet2), common_element_);
  RVec<int> jetflavs_list = Concatenate(jetflavs_list_, tmp__); 
  if(debug){
    cout<<"common_element "<<common_element<<endl;
    cout<<"tmp_ "<<tmp_<<endl;
    cout<<"jetflavs_list_ "<<jetflavs_list_<<endl;
    cout<<"common_element_ "<<common_element_<<endl;
    cout<<"tmp__ "<<tmp__<<endl;
    cout<<"jetflavs_list "<<jetflavs_list<<endl;
  }
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

        if (matchedJets >= 2 && FatJet_matched[idxFatJet] > 0 && (Jet_topMother[idxJet0] == Jet_topMother[idxJet1] || Jet_topMother[idxJet0] == Jet_topMother[idxJet2] || Jet_topMother[idxJet1] == Jet_topMother[idxJet2]) && (Jet_topMother[idxJet0] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet1] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet2] == FatJet_topMother[idxFatJet])) 
        {
          jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2], false);
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
            jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2], false);
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
        top_truth = 0;
    } else {
      if (idxFatJet != -1) {
        int matchedJets = 0;
        if (Jet_matched[idxJet0] > 0) matchedJets++;
        if (Jet_matched[idxJet1] > 0) matchedJets++;
        if (Jet_matched[idxJet2] > 0) matchedJets++;

        if (matchedJets >= 1 && FatJet_matched[idxFatJet] > 0 && (Jet_topMother[idxJet0] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet1] == FatJet_topMother[idxFatJet] || Jet_topMother[idxJet2] == FatJet_topMother[idxFatJet])) 
        {
          jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2], false);
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
            jetflavs_list = UniqueFlavList(Jet_pdgId[idxJet0], Jet_pdgId[idxJet1], Jet_pdgId[idxJet2], false);  
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

RVec<int> CalculateTopTruth2(rvec_i TopMixed_idxJet0, rvec_i TopMixed_idxJet1, rvec_i TopMixed_idxJet2, rvec_i TopMixed_idxFatJet, rvec_i Jet_matched, rvec_i Jet_topMother, rvec_i Jet_pdgId, rvec_i FatJet_matched, rvec_i FatJet_topMother, rvec_i FatJet_pdgId)
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

RVec<int> CalculateTopTruth1(rvec_i TopMixed_idxJet0, rvec_i TopMixed_idxJet1, rvec_i TopMixed_idxJet2, rvec_i TopMixed_idxFatJet, rvec_i Jet_matched, rvec_i Jet_topMother, rvec_i Jet_pdgId, rvec_i FatJet_matched, rvec_i FatJet_topMother, rvec_i FatJet_pdgId)
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


int test_cpp(){
  TFile *file = TFile::Open("root://cms-xrd-global.cern.ch//store/user/acagnott/DM_Run3_v0/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TT_semilep_2018/231222_110917/0000/tree_hadd_635.root");
  TTree *tree = (TTree*)file->Get("Events");

  Int_t nTopMixed;
  UInt_t nJet;
  UInt_t nFatJet;
  Float_t topmixed_TopScore[1000];
  Int_t topmixed_truth[1000];
  Int_t topmixed_idxFatJet[1000];
  Int_t topmixed_idxJet0[1000];
  Int_t topmixed_idxJet1[1000];
  Int_t topmixed_idxJet2[1000];
  Float_t jet_matched[1000];
  Float_t jet_pdgId[1000];
  Float_t jet_topmother[1000];
  Float_t fatjet_matched[1000];
  Float_t fatjet_pdgId[1000];
  Float_t fatjet_topmother[1000];

  tree->SetBranchAddress("TopMixed_TopScore",  &topmixed_TopScore);
  tree->SetBranchAddress("TopMixed_truth",     &topmixed_truth);
  tree->SetBranchAddress("TopMixed_idxFatJet", &topmixed_idxFatJet);
  tree->SetBranchAddress("TopMixed_idxJet0",   &topmixed_idxJet0);
  tree->SetBranchAddress("TopMixed_idxJet1",   &topmixed_idxJet1);
  tree->SetBranchAddress("TopMixed_idxJet2",   &topmixed_idxJet2);
  tree->SetBranchAddress("nTopMixed",   &nTopMixed);
  tree->SetBranchAddress("nJet",   &nJet);
  tree->SetBranchAddress("nFatJet",   &nFatJet);
  tree->SetBranchAddress("Jet_matched", &jet_matched);
  tree->SetBranchAddress("Jet_pdgId", &jet_pdgId);
  tree->SetBranchAddress("Jet_topMother", &jet_topmother);
  tree->SetBranchAddress("FatJet_matched", &fatjet_matched);
  tree->SetBranchAddress("FatJet_pdgId", &fatjet_pdgId);
  tree->SetBranchAddress("FatJet_topMother", &fatjet_topmother);


  int nEntries = tree->GetEntries();
  int nLoops = 20;
  if (nEntries < nLoops) {
    nLoops = nEntries;
  }

  for (int i = 10; i < nLoops; i++) {
    tree->GetEntry(i);
    // Call your functions here using the TopMixed_ branches
    // Example:
    cout<<"------------------------------------------------------"<<endl;
    cout<<"Entry "<<i<<endl;
    // cout<<"nTopMixed "<<nTopMixed<<endl;
    RVec<float> TopMixed_TopScore(nTopMixed);
    RVec<int> TopMixed_truth(nTopMixed);
    RVec<int> TopMixed_idxFatJet(nTopMixed);
    RVec<int> TopMixed_idxJet0(nTopMixed);
    RVec<int> TopMixed_idxJet1(nTopMixed);
    RVec<int> TopMixed_idxJet2(nTopMixed);
    RVec<int> Jet_matched(nJet);
    RVec<int> Jet_pdgId(nJet);
    RVec<int> Jet_topMother(nJet);
    RVec<int> FatJet_matched(nFatJet);
    RVec<int> FatJet_pdgId(nFatJet);
    RVec<int> FatJet_topMother(nFatJet);

    for (int j = 0; j < nTopMixed; j++) {
      TopMixed_TopScore[j] = topmixed_TopScore[j];
      TopMixed_truth[j] = topmixed_truth[j];
      TopMixed_idxFatJet[j] = topmixed_idxFatJet[j];
      TopMixed_idxJet0[j] = topmixed_idxJet0[j];
      TopMixed_idxJet1[j] = topmixed_idxJet1[j];
      TopMixed_idxJet2[j] = topmixed_idxJet2[j];
    }
    for(int j = 0; j<nJet; j++)
    {
      Jet_matched[j] = jet_matched[j];
      Jet_pdgId[j] = jet_pdgId[j];
      Jet_topMother[j] = jet_topmother[j];
    }
    for(int j = 0; j<nFatJet; j++)
    {
      FatJet_matched[j] = fatjet_matched[j];
      FatJet_pdgId[j] = fatjet_pdgId[j];
      FatJet_topMother[j] = fatjet_topmother[j];
    }
  auto toptruth1 = CalculateTopTruth1(TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_idxFatJet, Jet_matched, Jet_topMother, Jet_pdgId, FatJet_matched, FatJet_topMother, FatJet_pdgId);
  auto toptruth2 = CalculateTopTruth2(TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2, TopMixed_idxFatJet, Jet_matched, Jet_topMother, Jet_pdgId, FatJet_matched, FatJet_topMother, FatJet_pdgId);

  cout<<"TopMixed_idxJet0"<<TopMixed_idxJet0<<endl;
  cout<<"TopMixed_idxJet1"<<TopMixed_idxJet1<<endl;
  cout<<"TopMixed_idxJet2"<<TopMixed_idxJet2<<endl;
  cout<<"TopMixed_idxFatJet"<<TopMixed_idxFatJet<<endl;
  cout<<"Jet_matched"<<Jet_matched<<endl;
  cout<<"Jet_pdgId"<<Jet_pdgId<<endl;
  cout<<"Jet_topMother"<<Jet_topMother<<endl;
  cout<<"FatJet_matched"<<FatJet_matched<<endl;
  cout<<"FatJet_pdgId"<<FatJet_pdgId<<endl;
  cout<<"FatJet_topMother"<<FatJet_topMother<<endl;
  cout<<"TopTruth1 "<<toptruth1<<endl;
  cout<<"TopTruth2 "<<toptruth2<<endl;

  //   auto res = findTopClusters(TopMixed_TopScore, TopMixed_idxFatJet, TopMixed_idxJet0, TopMixed_idxJet1, TopMixed_idxJet2);
    
  //   if (res.size()>1){
  //   cout<<"TopMixed_idxFatJet "<<TopMixed_idxFatJet<<endl;
  //   cout<<"TopMixed_idxJet0 "<<TopMixed_idxJet0<<endl;
  //   cout<<"TopMixed_idxJet1 "<<TopMixed_idxJet1<<endl;
  //   cout<<"TopMixed_idxJet2 "<<TopMixed_idxJet2<<endl;
  //   cout<<"Top clusters" << endl;
  //   cout<<res<< endl;
  // }
  }
  // Free memory of RVecs

  file->Close();

  return 0;
}


