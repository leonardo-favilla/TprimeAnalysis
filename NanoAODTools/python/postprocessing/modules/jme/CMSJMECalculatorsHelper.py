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

loadJMESystematicsCalculators() # https://cms-jerc.web.cern.ch/Recommendations/

cvmfsPOGpath = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/"

versiontag = {
    "2018"      :   "2018_UL",
    "2022"      :   "Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23",
    "2022EE"    :   "Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07",
    "2023"      :   "Run3-23CSep23-Summer23-NanoAODv12/2025-10-07",
    "2023BPix"  :   "Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07",
    "2024"      :   "Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-07-17",
}
jestag = {
    "MC":{
        'AK8PFPuppi':{
            '2018'      : 'Summer19UL18_V5_MC',
            '2022'      : 'Summer22_22Sep2023_V3_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_V3_MC',
            '2023'      : 'Summer23Prompt23_V2_MC', 
            '2023BPix'  : 'Summer23BPixPrompt23_V3_MC',
        },
        'AK4PFPuppi':{
            '2018'      : 'Summer19UL18_V5_MC',
            '2022'      : 'Summer22_22Sep2023_V3_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_V3_MC',
            '2023'      : 'Summer23Prompt23_V2_MC',
            '2023BPix'  : 'Summer23BPixPrompt23_V3_MC', # place holder still not available 
        }
    },
    "DATA":{
        'AK8PFPuppi':{
            '2018'          : 'Summer19UL18_V5_DATA',
            '2022'          : 'Summer22_22Sep2023_RunCD_V3_DATA',
            '2022EE_E'      : 'Summer22EE_22Sep2023_RunE_V3_DATA',
            '2022EE_F'      : 'Summer22EE_22Sep2023_RunF_V3_DATA',
            '2022EE_G'      : 'Summer22EE_22Sep2023_RunG_V3_DATA',
            '2023_C1'       : 'Summer23Prompt23_V2_DATA',
            '2023_C2'       : 'Summer23Prompt23_V2_DATA',
            '2023_C3'       : 'Summer23Prompt23_V2_DATA',
            '2023_C4'       : 'Summer23Prompt23_V2_DATA',
            '2023BPix_D'    : 'Summer23BPixPrompt23_V3_DATA', # place holder still not available
        },
        'AK4PFPuppi':{
            '2018'          : 'Summer19UL18_V5_DATA',
            '2022'          : 'Summer22_22Sep2023_RunCD_V3_DATA',
            '2022EE_E'      : 'Summer22EE_22Sep2023_RunE_V3_DATA',
            '2022EE_F'      : 'Summer22EE_22Sep2023_RunF_V3_DATA',
            '2022EE_G'      : 'Summer22EE_22Sep2023_RunG_V3_DATA',
            '2023_C1'       : 'Summer23Prompt23_V2_DATA',
            '2023_C2'       : 'Summer23Prompt23_V2_DATA',
            '2023_C3'       : 'Summer23Prompt23_V2_DATA',
            '2023_C4'       : 'Summer23Prompt23_V2_DATA',
            '2023BPix_D'    : 'Summer23BPixPrompt23_V3_DATA', # place holder still not available
        }
    }
}
jertag = {
    "MC":{
        'AK8PFPuppi':{
            '2018'      : 'Summer19UL18_JRV2_MC',
            '2022'      : 'Summer22_22Sep2023_JRV1_MC', 
            '2022EE'    : 'Summer22EE_22Sep2023_JRV1_MC',
            '2023'      : 'Summer23Prompt23_RunCv1234_JRV1_MC', 
            '2023BPix'  : 'Summer23BPixPrompt23_RunD_JRV1_MC', 
        },
        'AK4PFPuppi':{
            '2018'      : 'Summer19UL18_JRV2_MC',
            '2022'      : 'Summer22_22Sep2023_JRV1_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_JRV1_MC',
            '2023'      : 'Summer23Prompt23_RunCv1234_JRV1_MC', 
            '2023BPix'  : 'Summer23BPixPrompt23_RunD_JRV1_MC', # place holder still not available
        }
    }
}
def configcreate(isMC=True, year=2022, EE=False, runPeriod="C", jetType="AK4PFPuppi", forMET=False, doJer=True):
    print("isMC, year, EE, runPeriod, jetType, forMET, doJer:", isMC, year, EE, runPeriod, jetType, forMET, doJer)
    if forMET:
        configCls = calcConfigs.METVariations
    elif "AK4" in jetType:
        configCls = calcConfigs.JetVariations
    elif "AK8" in jetType:
        configCls = calcConfigs.FatJetVariations
    else:
        print("Unsupported configurationType")

    year_ = str(year)
    if year == 2022:
        if EE: year_ += "EE"
    elif year == 2023:
        if EE: year_ += "BPix"
    
    tagver = versiontag[year_]
    print("tagver: ", tagver)
    if runPeriod != ".": 
        if ("2022EE" in year_) or ("2023" in year_):
            year_ += "_"+runPeriod
            print("year_ with runPeriod: ", year_)
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