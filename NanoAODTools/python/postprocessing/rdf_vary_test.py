import ROOT
import os
from samples.samples import *
#import optparse
import copy
import math
from CMS_lumi import CMS_lumi
from variables import *
ROOT.gInterpreter.Declare('#include "ROOT/RDataFrame.hxx"')
ROOT.gInterpreter.Declare('#include "ROOT/RVec.hxx"')

datasets = [ZJetsToNuNu_HT800to1200_2018]

def get_files_string(d):
    folder_files = "../../crab/macros/files/"
    infile_string = open(folder_files+d.label+".txt")
    strings = infile_string.readlines()
    for s in strings: s.replace('\n', '')
    return strings

outf = "/eos/home-a/acagnott/DarkMatter/nosynch/v2/test_vary/"

for d in datasets:
    strings = get_files_string(d)
    chain = ROOT.TChain("Events")
    for f in strings[:1]: chain.Add(f)
    df = ROOT.RDataFrame(chain)
    h_ = df.Histo1D(("firstDF_MET_pt",";MET p_{T}[GeV]", 30, 0, 1000), "PuppiMET_pt").GetValue()
    print("OK")
    if hasattr(df, "Vary"): print("attribute")

    df = df.Vary("MET_pt", "RVec<RVec<float>>{PuppiMET_pt, PuppiMET_ptJESUp}", variationTags=["nominal", "up"], variationName="MET")\
                               .Filter("PuppiMET_pt>150")
    
    h_nom = df.Histo1D(("firstDF_MET_pt",";MET p_{T}[GeV]", 30, 0, 1000), "PuppiMET_pt")
    h = ROOT.RDF.Experimental.VariationsFor(h_nom)
    h1=h["nominal"].GetValue()
    h2=h["met_pt:nominal"].GetValue()
    h3=h["met_pt:up"].GetValue()
    outfile = ROOT.TFile.Open("outhistos.root", "RECREATE")    
    h1.Write()
    h2.Write()
    h3.Write()
    outfile.Close()
