from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
)
from CMSJMECalculators import config as calcConfigs

import ROOT as gbl

# import tarfile
# import tempfile
import os


# stringFile = "root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/60000/b9d48100-f36a-4422-b17c-6605da590baa.root"
stringFile = 'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/260000/7EB23839-6971-464E-9E95-03CB9C2824F1.root'

def getEventWith(f, condition=lambda ev : True, treeName="Events"):
    tup = f.Get(treeName)
    tup.GetEntry(0)
    i = 0
    while not condition(tup):
        i += 1
        tup.GetEntry(i)
    yield tup

def nanojetargsMC22(tup):
    # f = gbl.TFile.Open(stringFile)
    # tup = getEventWith(f)
    # tup = f.Get("Events")
    # tup.GetEntry(n)
    return getJetMETArgs(tup, isMC=True, addHEM2018Issue=False, forMET=False, NanoAODv=12)

def nanoMETargsMC22(n):
    # return getJetMETArgs(tup, isMC=True, addHEM2018Issue=False, forMET=True, PuppiMET=True, NanoAODv=12)
    return getJetMETArgs(tup, isMC=True, addHEM2018Issue=False, forMET=True, PuppiMET=False, NanoAODv=9)

def nanofatjetargsMC22(tup):
    f = gbl.TFile.Open(stringFile)
    # tup = getEventWith(f)
    tup = f.Get("Events")
    tup.GetEntry(n)
    print("PuppiMET", tup.PuppiMET_pt)
    return getFatJetArgs(tup, isMC=True, addHEM2018Issue=False, NanoAODv=12)

def jetvarcalc_empty():
    config = calcConfig.JetVariations()
    loadJMESystematicsCalculators()
    return config.create()

# def jetvarcalcMC16_smear():
#     config = calcConfig.JetVariations()
#     configureCalc(config, jerTag="Summer16_25nsV1_MC", splitJER=True,
#             jecDBCache=jecDBCache, jrDBCache=jrDBCache)
#     loadJMESystematicsCalculators()
#     yield config.create()
def jetvarcalcMC22_jer():
    configCls = calcConfigs.JetVariations
    tagfile = "2022_Prompt"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    jetType = "AK4PFPuppi"
    config = configCls(jsonFile, jetType)
    # config.jecTag = "Summer22_22Sep2023_V2_MC"
    # config.jerTag = "Summer22_22Sep2023_V2_MC"
    # config.jecTag = "Winter22Run3_V2_MC"
    config.jerTag = "JR_Winter22Run3_V1_MC"
    # config.jecLevel = "L1L2L3Res"
    # config.jesUncertainties = ["Total"]#, "AbsoluteStat", "AbsoluteScale"]
    config.splitJER = False
    loadJMESystematicsCalculators()
    return config.create()

def jetvarcalcMC22_jec():
    loadJMESystematicsCalculators()
    configCls = calcConfigs.JetVariations
    tagfile = "2022_Summer22"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    jetType = "AK4PFPuppi"
    config = configCls(jsonFile, jetType)
    config.jecTag = "Summer22_22Sep2023_V2_MC"
    # config.jerTag = "Summer22_22Sep2023_V2_MC"
    # config.jecTag = "Winter22Run3_V2_MC"
    # config.jerTag = "JR_Winter22Run3_V1_MC"
    config.jecLevel = "L1L2L3Res"
    # config.jesUncertainties = ["Total"]#, "AbsoluteStat", "AbsoluteScale"]
    # config.splitJER = False
    loadJMESystematicsCalculators()
    c_ = config.create()
    return gbl.JetVariationsCalculator(c_)
    # return config.create()

def metvarcalcMC22():
    print("entering in config definition")
    configCls = calcConfigs.METVariations
    print("configCLs defined")
    tagfile = "2018_UL"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    jetType = "AK4PFchs"
    config = configCls(jsonFile, jetType)
    print("config defined")
    # config.jecTag = "Winter22Run3_V2_MC"
    # config.jerTag = "JR_Winter22Run3_V1_MC"
    config.jecTag = "Summer19UL18_V5_MC"
    # config.jerTag = "Summer19UL18_JRV2_MC"
    config.jecLevel = "L1L2L3Res"
    # config.jesUncertainties = ["Total"]
    # config.splitJER = False
    # loadJMESystematicsCalculators()
    loadJMESystematicsCalculators()
    c_ = config.create()
    print("config created")
    calc = gbl.Type1METVariationsCalculator(c_)
    print("calculator created")
    # return config.create()
    return calc


def fatjetvarcalcMC22():
    configCls = calcConfigs.FatJetVariations
    tagfile = "2022_Summer22"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/fatJet_jerc.json.gz"
    jetType = "AK8PFPuppi"
    config = configCls(jsonFile, jetType)
    config.jecTag = "Summer22_22Sep2023_V2_MC"
    # config.jerTag = "Summer22_22Sep2023_V2_MC"
    # config.jecTag = "Winter22Run3_V2_MC"
    # config.jerTag = "JR_Winter22Run3_V1_MC"
    config.splitJER = False
    config.jecLevel = "L1L2L3Res"
    config.jesUncertainties = ["Total","FlavorQCD","TimePtEta"]
    config.jsonFileSubjet = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    config.jetAlgoSubjet = "AK4PFPuppi"
    config.jecTagSubjet = "Summer22_22Sep2023_V2_MC"
    config.jecLevelSubjet = "L1L2L3Res"
    return config.create()

loadJMESystematicsCalculators()
from datetime import datetime
start = datetime.now()
jec = jetvarcalcMC22_jec()#metvarcalcMC22()#fatjetvarcalcMC22()#jetvarcalcMC22_jec()
# jer = jetvarcalcMC22_jer()#metvarcalcMC22()#fatjetvarcalcMC22()#jetvarcalcMC22_jec()
# jec = metvarcalcMC22()

# empty = jetvarcalc_empty()
f = gbl.TFile.Open(stringFile)
tup = f.Get("Events")
for n in range(5):
    print(n)
    tup.GetEntry(n)
    # print(tup.Jet_pt[0])
    var = nanojetargsMC22(tup)#nanoMETargsMC22(tup)#nanoMETargsMC22(n)#nanofatjetargsMC22()#
    res = jec.produce(*var)
    # res1 = jer.produce(*var)
    print(jec.available())
    # print(dir(res))
    for i in range(jec.available().size()):
        print(res.pt(i))
    # print(jer.available())
    # for i in range(jer.available().size()):
    #     print(res1.pt(i))
end = datetime.now()
print(end-start)

#  più veloce se definito jer all'inizio e basta