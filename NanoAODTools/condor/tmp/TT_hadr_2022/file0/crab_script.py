#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.JetVetoMaps_run3 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.JetVetoMaps_run3 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.BTagSF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PUreweight import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_syst import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_syst import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lumiMask import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculators_module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsHelper import *
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
)
from CMSJMECalculators import config as calcConfigs
loadJMESystematicsCalculators()
p=PostProcessor('.', ['root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/NANOAODSIM/130X_mcRun3_2022_realistic_v5_ext1-v2/2530000/502d69c0-ff56-4c39-98c9-ac1bbd1f1246.root'], '', modules=[MCweight_writer(),MET_Filter(year = 2022),JetVetoMaps_run3(year=2022,EE=0),preselection(),PUreweight(year=2022,EE=0),BTagSF(year=2022,EE=0),CMSJMECalculators(configcreate(isMC=True,year=2022,EE=0,runPeriod='.',jetType='AK4PFPuppi',forMET=False,doJer=True),jetType='AK4PFPuppi',isMC=True,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=True,year=2022,EE=0,runPeriod='.',jetType='AK8PFPuppi',forMET=False,doJer=True),jetType='AK8PFPuppi',isMC=True,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=True,year=2022,EE=0,runPeriod='.',jetType='AK4PFPuppi',forMET=True,doJer=True),jetType='AK4PFPuppi',isMC=True,forMET=True,PuppiMET=True,addHEM2018Issue=False,NanoAODv=12),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(),nanoTopcand(isMC=True),globalvar(), nanoTopevaluate_MultiScore(year = 2022)], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/user/l/lfavilla/TprimeAnalysis/NanoAODTools/scripts/keep_and_drop.txt')
p.run()
print('DONE')
