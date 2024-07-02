import ROOT
import os 

folder = "test81223"
sample = "DataHTA_2018"

## davix library
# {} -E /tmp/x509up_u0 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/
tier_folder = "davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/"
proxy_file = "/tmp/x509up_u140541"
capath = "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"

url = tier_folder + folder + "/"
grid_input = "-E " + proxy_file + " --capath " + capath

if not os.path.exists(proxy_file):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')

print("remote folder: ", url)

chain = ROOT.TChain("events_nominal")

files = os.popen("davix-ls "+ url + " " + grid_input ).readlines()
for f in files:
    if "snap_"+sample in f:
        f = f.replace("\n","")
        # print(f)
        # print(url + "" + f + " " + grid_input)
        chain.Add("root://cms-xrd-global.cern.ch//store/user/acagnott/test81223/"+f)

print(chain.GetEntries())
hist = ROOT.TH1D("MET_pt", "MET_pt", 100, 0, 1000)
cut = "(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight) && (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_ecalBadCalibFilter && Flag_eeBadScFilter)"
chain.Project("MET_pt", "MET_pt", cut)

outfile = ROOT.TFile.Open("/eos/home-a/acagnott/DarkMatter/nosynch/test_snapshot/test.root", "RECREATE")
hist.Write()
outfile.Close()