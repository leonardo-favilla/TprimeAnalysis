import math
import numpy as np
class variable(object):
    def __init__(self, name, title, taglio=None, nbins=None, xmin=None, xmax=None, xarray=None, MConly = False, noUnOvFlowbin = False):
        self._name = name
        self._title = title
        self._taglio = taglio
        self._nbins = nbins
        self._xmin = xmin
        self._xmax = xmax
        self._xarray = xarray
        self._MConly = MConly
        self._noUnOvFlowbin = noUnOvFlowbin
    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._title)+'\",\"'+str(self._taglio)+'\",'+str(self._nbins)+','+str(self._xmin)+','+str(self._xmax)

class variable2D(object):
    def __init__(self, name, xname, yname, xtitle, ytitle, taglio=None, nxbins=None, xmin=None, xmax=None, xarray=None, 
                    nybins=None, ymin=None, ymax=None, yarray=None):
        self._name = name
        self._xname = xname
        self._yname = yname
        self._xtitle = xtitle
        self._ytitle = ytitle
        self._taglio = taglio
        self._nxbins = nxbins
        self._xmin = xmin
        self._xmax = xmax
        self._xarray = xarray
        self._nybins = nybins
        self._ymin = ymin
        self._ymax = ymax
        self._yarray = yarray
    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._xtitle)+'\",\"'+str(self._ytitle)+'\",\"'+str(self._taglio)+'\",'+str(self._nxbins)+','+str(self._xmin)+','+str(self._xmax)+','+str(self._nybins)+','+str(self._ymin)+','+str(self._ymax)


### Definition of requeriments for plots (cut), variables and regions

requirements = ""

######## 1D variables for histos

vars = []

vars.append(variable(name = "TopResolved_TopScore_nominal",         title= "Top Resolved Score",            nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "TopMixed_TopScore_nominal",            title= "Top Mixed Score",               nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "TopMerged_TopScore_nominal",           title= "Top Merged Score",              nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))

vars.append(variable(name = "BestTopResolved_score",                title= "Best Top Resolved Score",       nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopMixed_score",                   title= "Best Top Mixed Score",          nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))
vars.append(variable(name = "BestTopMerged_score",                  title= "Best Top Merged Score",         nbins = 40, xmin = 0, xmax=1, noUnOvFlowbin = True))


######## 2D variables for histos
vars2D = []



#### REGIONS DEFINITION ####

regions = {

    "presel"                            : "",
    "BestTopResolved_topmatched"        : "BestTopResolved_process==0",
    "BestTopResolved_nonmatched"        : "BestTopResolved_process==1",
    "BestTopResolved_other"             : "BestTopResolved_process==2",
    "BestTopMixed_topmatched"           : "BestTopMixed_process==0",
    "BestTopMixed_nonmatched"           : "BestTopMixed_process==1",
    "BestTopMixed_other"                : "BestTopMixed_process==2",
    "BestTopMerged_topmatched"          : "BestTopMerged_process==0",
    "BestTopMerged_nonmatched"          : "BestTopMerged_process==1",
    "BestTopMerged_other"               : "BestTopMerged_process==2",
    "btagSFcheck"                       : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",

    }