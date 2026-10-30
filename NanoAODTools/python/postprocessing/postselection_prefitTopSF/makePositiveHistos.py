import ROOT
import argparse
from PhysicsTools.NanoAODTools.postprocessing.postselection.loadHists import loadHists

parser  = argparse.ArgumentParser(description='Process ROOT files to fix zero bin contents in histograms.')
parser.add_argument("-i", "--infile", type=str, help='Input ROOT file', required=True)
args    = parser.parse_args()

infilename      = args.infile
outfilename     = infilename.replace(".root","_zerosFixed.root")

histo_dict      = loadHists(infilename)
outfile         = ROOT.TFile.Open(outfilename, "RECREATE")
thrInput        = 0.00000001 # if content less than this threshold
thrOutput       = 0.000001  # set value to this

print(histo_dict.keys())

for histo_name,histo in histo_dict.items():
    tmp = histo.Clone(histo_name)
    if not histo_name.startswith("data_"): # data histograms are kept as they are
        for i in range(0, histo.GetNbinsX()+2):
            if histo.GetBinContent(i) < thrInput :
                print(f"Setting bin {i} of histogram {histo.GetName()} to {thrOutput} because it content is {histo.GetBinContent(i)} which is below the threshold {thrInput}")
                tmp.SetBinContent(i, thrOutput)
                tmp.SetBinError(i, thrOutput*0.99)

    outfile.cd()
    tmp.Write(histo_name, ROOT.TObject.kOverwrite)

outfile.Close()
print(f"Histograms with fixed zero bins saved to {outfilename}")
