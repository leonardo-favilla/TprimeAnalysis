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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
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
p=PostProcessor('.', ['root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/130X_mcRun3_2022_realistic_v5-v2/2530000/723afcf8-b4ba-45ac-a44b-f4b0198689d5.root'], '', modules=[MCweight_writer(),MET_Filter(year = 2022),JetVetoMaps_run3(year=2022,EE=0),preselection(),PUreweight(year=2022,EE=0),BTagSF(year=2022,EE=0),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(),nanoTopcand(isMC=True),globalvar(), nanoTopevaluate_MultiScore(year = 2022, modelMix_path='/afs/cern.ch/user/l/lfavilla/TprimeAnalysis/NanoAODTools/python/postprocessing/data/dict_tresholds/model_TopMixed_2022_p2.h5', modelRes_path='/afs/cern.ch/user/l/lfavilla/TprimeAnalysis/NanoAODTools/python/postprocessing/data/dict_tresholds/model_TopResolved_2022.h5')], provenance=True, haddFileName='tree.root', fwkJobReport=False, histFileName='hist.root', histDirName='plots', outputbranchsel='/afs/cern.ch/user/l/lfavilla/TprimeAnalysis/NanoAODTools/scripts/keep_and_drop.txt')
p.run()
print('DONE')
