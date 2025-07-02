import correctionlib
from correctionlib import _core

# Path to the .json.gz file
# filepath    = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2023_Summer23/btagging.json.gz"
filepath    = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2023_Summer23BPix/btagging.json.gz"
# filepath    = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz"

# Load the correction set from the file
cset        = _core.CorrectionSet.from_file(filepath)
print([key for key in cset])
corr        = cset["particleNet_wp_values"]
print("Inputs:", corr.inputs)
print("Description:", corr.description)
print(corr.inputs[0].name)

# For example, get the discriminator threshold for the 'M' working point
threshold_L     = corr.evaluate("L")
threshold_M     = corr.evaluate("M")
threshold_T     = corr.evaluate("T")
threshold_XT    = corr.evaluate("XT")
threshold_XXT   = corr.evaluate("XXT")
print("Discriminator threshold for L:   ", threshold_L)
print("Discriminator threshold for M:   ", threshold_M)
print("Discriminator threshold for T:   ", threshold_T)
print("Discriminator threshold for XT:  ", threshold_XT)
print("Discriminator threshold for XXT: ", threshold_XXT)