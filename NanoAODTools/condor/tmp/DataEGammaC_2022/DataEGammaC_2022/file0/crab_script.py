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
p=PostProcessor('.', ['root://cms-xrd-global.cern.ch//store/data/Run2022C/EGamma/NANOAOD/22Sep2023-v1/40000/cbf47164-81b5-47a2-ae31-d68c7f5e722a.root'], '', modules=[lumiMask(year = 2022),MET_Filter(year = 2022),JetVetoMaps_run3(year=2022,EE=0),preselection(),CMSJMECalculators(configcreate(isMC=False,year=2022,EE=0,runPeriod='C',jetType='AK4PFPuppi',forMET=False,doJer=True),jetType='AK4PFPuppi',isMC=False,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=False,year=2022,EE=0,runPeriod='C',jetType='AK8PFPuppi',forMET=False,doJer=True),jetType='AK8PFPuppi',isMC=False,forMET=False,PuppiMET=False,addHEM2018Issue=False,NanoAODv=12),CMSJMECalculators(configcreate(isMC=False,year=2022,EE=0,runPeriod='C',jetType='AK4PFPuppi',forMET=True,doJer=True),jetType='AK4PFPuppi',isMC=False,forMET=True,PuppiMET=True,addHEM2018Issue=False,NanoAODv=12),nanoTopcand(isMC=False),globalvar(), nanoTopevaluate_MultiScore(isMC=0,year = 2022)], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/work/a/acagnott/Analysis/NanoAODTools/scripts/keep_and_drop.txt')
p.run()
print('DONE')
