#!/usr/bin/env python
import os, ROOT
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
)
from CMSJMECalculators import config as calcConfigs

loadJMESystematicsCalculators()

cvmfsPOGpath = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"
versiontag = {
    "2018"      :   "2018_UL",
    "2022"      :   "2022_Summer22",
    "2022EE"    :   "2022_Summer22EE",
    "2023"      :   "2023_Summer23",
    "2023BPix"  :   "2023_Summer23BPix",
}
jestag = {
    "MC":{
        'AK8PFPuppi':{
            '2018'      : 'Summer19UL18_V5_MC',
            '2022'      : 'Summer22_22Sep2023_V2_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_V2_MC',
            '2023'      : '.', 
        },
        'AK4PFPuppi':{
            '2018'      : 'Summer19UL18_V5_MC',
            '2022'      : 'Summer22_22Sep2023_V2_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_V2_MC',
            '2023'      : '.', # place holder still not available 
        }
    },
    "DATA":{
        'AK8PFPuppi':{
            '2018'          : 'Summer19UL18_V5_DATA',
            '2022'          : 'Summer22_22Sep2023_RunCD_V2_DATA',
            '2022EE_E'      : 'Summer22EE_22Sep2023_RunE_V2_DATA',
            '2022EE_F'      : 'Summer22EE_22Sep2023_RunF_V2_DATA',
            '2022EE_G'      : 'Summer22EE_22Sep2023_RunG_V2_DATA',
            '2023'          : '.', # place holder still not available
        },
        'AK4PFPuppi':{
            '2018'          : 'Summer19UL18_V5_DATA',
            '2022'          : 'Summer22_22Sep2023_RunCD_V2_DATA',
            '2022EE_E'      : 'Summer22EE_22Sep2023_RunE_V2_DATA',
            '2022EE_F'      : 'Summer22EE_22Sep2023_RunF_V2_DATA',
            '2022EE_G'      : 'Summer22EE_22Sep2023_RunG_V2_DATA',
            '2023'          : '.', # place holder still not available 
        }
    }
}
jertag = {
    "MC":{
        'AK8PFPuppi':{
            '2018'      : 'Summer19UL18_JRV2_MC',
            '2022'      : 'Summer22_22Sep2023_JRV1_MC', # place holder still not available 
            '2022EE'    : 'Summer22EE_22Sep2023_JRV1_MC', # place holder still not available
            '2023'      : '.', # place holder still not available 
        },
        'AK4PFPuppi':{
            '2018'      : 'Summer19UL18_JRV2_MC',
            '2022'      : 'Summer22_22Sep2023_JRV1_MC', # place holder still not available
            '2022EE'    : 'Summer22EE_22Sep2023_JRV1_MC', # place holder still not available
            '2023'      : '.', # place holder still not available 
        }
    }
}
def configcreate(isMC=True, year=2022, EE=False, runPeriod="C", jetType="AK4PFPuppi", forMET=False, doJer=True):
    if forMET:
        configCls = calcConfigs.METVariations
    elif "AK4" in jetType:
        configCls = calcConfigs.JetVariations
    elif "AK8" in jetType:
        configCls = calcConfigs.FatJetVariations
    else:
        print("Unsupported configurationType")

    year_ = str(year)
    if EE: year_ += "EE"
    tagver = versiontag[year_]
    if runPeriod != ".": 
        if "2022EE" in year_:
            year_ += "_"+runPeriod        
    if (forMET or "AK4" in jetType):
        jsonFile = cvmfsPOGpath + tagver + "/jet_jerc.json.gz"
    else:
        jsonFile = cvmfsPOGpath + tagver + "/fatJet_jerc.json.gz"

    print("year, RunTag, jetType: ", year_, tagver, jetType)
    print("JES :", jestag["MC" if isMC else "DATA"][jetType][year_])

    config = configCls(jsonFile, jetType)
    config.jecTag = jestag["MC" if isMC else "DATA"][jetType][year_]
    config.jecLevel = "L1L2L3Res"
    if isMC: config.jesUncertainties = ["Total", "AbsoluteMPFBias", "AbsoluteScale", "AbsoluteStat","Fragmentation", "PileUpDataMC", "PileUpPtRef", "RelativeFSR", "RelativeStatFSR", "SinglePionECAL", "SinglePionHCAL", "TimePtEta"]
    # print("config.jesUncertainties ", config.jesUncertainties)
    if doJer and isMC:
        print("JER :", jertag["MC" if isMC else "DATA"][jetType][year_])
        config.jerTag = jertag["MC"][jetType][year_]
        config.splitJER = False
        config.jsonFileSmearingTool = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/jer_smear.json.gz" #path to your json file with jer smearing tool
        config.smearingToolName = "JERSmear"

    if "AK8" in jetType:
        config.jsonFileSubjet = cvmfsPOGpath + tagver + "/jet_jerc.json.gz"
        config.jetAlgoSubjet = "AK4PFPuppi" if year_ !="2018" else "AK4PFchs"
        config.jecTagSubjet = jestag["MC" if isMC else "DATA"]["AK4PFPuppi" if year_ !="2018" else "AK4PFchs"][year_]
        config.jecLevelSubjet = "L1L2L3Res"
        config.jsonFileSmearingTool = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/jer_smear.json.gz" #path to your json file with jer smearing tool
        config.smearingToolName = "JERSmear"
    if "AK4" in jetType:
        calc = config.create() # ROOT.JetVariationsCalculator(config.create())
    elif forMET:
        calc = config.create() # ROOT.Type1METVariationsCalculator(config.create())
    elif "AK8" in jetType:
        calc = config.create() # ROOT.FatJetVariationsCalculator(config.create()) 
    # return config.create()
    return calc

#  "FlavorQCD",  
#  "PileUpPtBB", "PileUpPtEC1", "PileUpPtEC2", "PileUpPtHF", 
#  "RelativeJEREC1", "RelativeJEREC2", "RelativeJERHF", "RelativePtBB", "RelativePtEC1", "RelativePtEC2", "RelativePtHF", "RelativeBal", "RelativeSample", "RelativeStatEC",  
#  "RelativeStatHF" 