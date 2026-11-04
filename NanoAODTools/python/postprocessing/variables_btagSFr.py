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


### Variables and regions for the b-tag shape SF normalization study (BTV factor r = sum w_noSFbtag / sum w_SFbtag):
### no b-tag cut, r measured vs the jet multiplicity. Run with --weightset allWeights --weightset noSFbtag.

requirements = ""

######## 1D variables for histos

vars = []

vars.append(variable(name = "nGoodJet",                 title = "# Good Jet",                           nbins = 10, xmin = -0.5,    xmax = 9.5))
vars.append(variable(name = "nJet",                     title = "# Jet",                                nbins = 10, xmin = -0.5,    xmax = 9.5))
vars.append(variable(name = "PuppiMET_T1_pt_nominal",   title = "p_{T}^{miss}(Puppi) nominal [GeV]",    nbins = 12, xmin = 250,     xmax = 850))


######## 2D variables for histos
vars2D = []



#### REGIONS DEFINITION ####

regions = {
    "MET250"                : "PuppiMET_T1_pt_nominal>250",
    "btagSFcheck"           : "PuppiMET_T1_pt_nominal>250 && MinDelta_phi>0.6 && (nVetoElectron==0 && nVetoMuon==0)",
}
