import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import json

class lumiMask(Module):
    def __init__(self, year = None):
        self.year = year
        pass
    def endJob(self):
        pass
    def beginJob(self):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        run = str(event.run)
        lumiblock = event.luminosityBlock
        
        if(self.year == 2016):
            jsonInput = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'  
        elif(self.year == 2017):
            jsonInput = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
        elif(self.year == 2018):
            jsonInput = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
        elif(self.year == 2022):
            jsonInput = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json'
        elif(self.year == 2023):
            jsonInput = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json'
        else:
            print ("Please specify the year: possible choices are 2016, 2017 , 2018 , 2022 or 2023")
        b = False
        # print(run, lumiblock)
        with open(jsonInput) as json_file:
            jsondict = json.load(json_file)
        if run in jsondict.keys():
            # print("run in jsondict.keys()")
            for i in range(len(jsondict[run])):
                if lumiblock>=jsondict[run][i][0] and lumiblock<=jsondict[run][i][1]:
                    # print("lumiblock in jsondict[run][i][0] and jsondict[run][i][1]")
                    b= True    
        return b