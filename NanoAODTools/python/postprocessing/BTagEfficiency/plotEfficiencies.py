import os
import sys
import optparse
import yaml
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# 2D plots of the MC b-tagging efficiency eff(|eta|, pt) = BTagEff_<flavour>_<wp> / BTagEff_<flavour>_all,
# one per jet flavour and WP, from the histograms produced by postSelector.py (one <component>.root per component in the plots folder).
# For a dataset with components (e.g. TT_2024) the histograms of all its components are summed before computing the efficiency.
# With -d inclusive_<era> (e.g. inclusive_2024) all the samples of the era in the plots folder are summed:
# total efficiency, the same as the inclusive map <tagger>_efficiency written by CreateCorrLibFile.py.

config = {}
config_paths = os.environ.get('PWD')+'/../config/config.yaml'
if os.path.exists(config_paths):
    with open(config_paths, "r") as _f:
        config = yaml.safe_load(_f) or {}
    print(f"Loaded config file from {config_paths}")
else:
    print(f"Config file not found in {config_paths}, exiting")
    sys.exit(1)

usage                   = "python3 plotEfficiencies.py -d <dataset or component, e.g. TT_2024 or TT_semilep_2024, or inclusive_<era> for the total efficiency>"
parser                  = optparse.OptionParser(usage)
parser.add_option('-d', '--dataset',        dest='dataset',         type=str,   default="",             help='Dataset (its components are summed), single component, or inclusive_<era> (all the samples of the era) to plot')
parser.add_option(      '--plots_folder',   dest='plots_folder',    type=str,   default=None,           help='Folder with the postSelector.py output files (default: btagEfficiency_results of the era in config.yaml + plots/)')
parser.add_option(      '--output',         dest='output',          type=str,   default=None,           help='Folder where to save the plots (default: btagEfficiency_results of the era in config.yaml + efficiency_plots/)')
parser.add_option(      '--flavours',       dest='flavours',        type=str,   default="b,c,light",    help='Jet flavours to plot, comma separated: b, c, light')
(opt, args)             = parser.parse_args()
dataset                 = opt.dataset
inclusive               = dataset.startswith("inclusive_")
if not inclusive and dataset not in sample_dict:
    print(f"Dataset '{dataset}' not found in samples.py")
    print(usage)
    sys.exit(1)
era                     = dataset.split("_")[-1]
plots_folder            = opt.plots_folder if opt.plots_folder is not None else config["outputfolder"]["btagEfficiency_results"][era] + "plots/"
output                  = opt.output if opt.output is not None else config["outputfolder"]["btagEfficiency_results"][era] + "efficiency_plots/"
output_2D               = f"{output}/2D/"
output_1D               = f"{output}/1D/"
for folder in [output_2D, output_1D]:
    if not os.path.exists(folder):
        os.makedirs(folder)

flavour_titles          = {"b": "b jets", "c": "c jets", "light": "light jets"}
flavours                = {flavour: flavour_titles[flavour] for flavour in opt.flavours.split(",")}
wps                     = {"L": "Loose", "M": "Medium", "T": "Tight"}

def get_era(s):
    # as in postSelector.py
    if s.year == 2022:
        return "2022EE" if getattr(s, "EE", 0) == 1 else "2022"
    if s.year == 2023:
        return "2023postBPix" if getattr(s, "EE", 0) == 1 else "2023"
    return str(s.year)

if inclusive:
    # all the samples of the era found in the plots folder, as the inclusive map of CreateCorrLibFile.py
    labels      = [f.replace(".root", "") for f in sorted(os.listdir(plots_folder)) if f.endswith(".root")]
    components  = [label for label in labels if label in sample_dict and get_era(sample_dict[label]) == era]
else:
    components  = [s.label for s in sample_dict[dataset].components] if hasattr(sample_dict[dataset], "components") else [dataset]
input_files             = []
for component in components:
    file_path = f"{plots_folder}/{component}.root"
    if os.path.exists(file_path):
        input_files.append(file_path)
    else:
        print(f"WARNING: {file_path} not found, {component} not included")
if len(input_files) == 0:
    print(f"No files of {dataset} found in {plots_folder}")
    sys.exit(1)
print(f"Plotting {dataset} from: {input_files}")


############# Sum the histograms of the components #############
histos = {}
for file_path in input_files:
    in_file = ROOT.TFile.Open(file_path)
    for flavour in flavours:
        for wp in ["all"] + list(wps):
            name = f"BTagEff_{flavour}_{wp}"
            if name not in histos:
                histos[name] = in_file.Get(name).Clone(f"{name}_sum")
                histos[name].SetDirectory(0)
            else:
                histos[name].Add(in_file.Get(name))
    in_file.Close()


############# Efficiency maps, same definition as in CreateCorrLibFile.py #############
def efficiency_map(flavour, wp):
    # pass/all in each bin, limited to [0, 1]; empty bins (e.g. pt 20-30 GeV, good jets have pt > 30 GeV) are set to -1:
    # below the minimum of the 2D plots, so they are drawn blank, and skipped in the 1D plots
    h_all, h_pass   = histos[f"BTagEff_{flavour}_all"], histos[f"BTagEff_{flavour}_{wp}"]
    h_eff           = h_all.Clone(f"eff_{flavour}_{wp}")
    h_eff.Reset()
    for ix in range(1, h_all.GetNbinsX()+1):
        for iy in range(1, h_all.GetNbinsY()+1):
            if h_all.GetBinContent(ix, iy) <= 0:
                h_eff.SetBinContent(ix, iy, -1.)
                continue
            n_pass  = h_pass.GetBinContent(ix, iy)                                      # number of jets passing the WP in the bin
            n_all   = h_all.GetBinContent(ix, iy)                                       # number of all jets in the bin
            print(f"Bin ({ix}, {iy}): n_all = {n_all}, h_pass = {n_pass}")
            eff     = min(max(n_pass / n_all, 0.), 1.)
            h_eff.SetBinContent(ix, iy, eff)
    return h_eff

def equal_size_bins(h):
    # copy of h where all the bins have the same size on the plot, the axis labels show the real bin edges
    nx, ny  = h.GetNbinsX(), h.GetNbinsY()
    h_plot  = ROOT.TH2D(h.GetName()+"_plot", "", nx, 0, nx, ny, 0, ny)
    for ix in range(1, nx+1):
        for iy in range(1, ny+1):
            h_plot.SetBinContent(ix, iy, h.GetBinContent(ix, iy))
    for ix in range(1, nx+1):
        h_plot.GetXaxis().SetBinLabel(ix, f"{h.GetXaxis().GetBinLowEdge(ix):g}-{h.GetXaxis().GetBinUpEdge(ix):g}")
    for iy in range(1, ny+1):
        h_plot.GetYaxis().SetBinLabel(iy, f"{h.GetYaxis().GetBinLowEdge(iy):.0f}-{h.GetYaxis().GetBinUpEdge(iy):.0f}")
    return h_plot


############# Plots #############
for flavour, flavour_title in flavours.items():
    for wp, wp_title in wps.items():
        h_eff   = equal_size_bins(efficiency_map(flavour, wp))
        h_eff.SetTitle(f"{dataset}: b-tagging efficiency, {flavour_title}, {wp_title} WP;Jet |#eta|;Jet p_{{T}} [GeV];Efficiency")
        h_eff.SetMarkerSize(1.5)
        h_eff.SetMinimum(-1e-9)                                                         # draw also the bins with efficiency 0
        h_eff.SetMaximum(h_eff.GetMaximum())
        h_eff.GetXaxis().SetLabelSize(0.05)
        h_eff.GetYaxis().SetLabelSize(0.04)
        h_eff.GetYaxis().SetTitleOffset(2.0)
        h_eff.GetZaxis().SetTitleOffset(1.4)
        ROOT.gStyle.SetPaintTextFormat("4.3f" if h_eff.GetMaximum() > 0.05 else "5.4f")  # more digits for the small (light/c) efficiencies

        canvas  = ROOT.TCanvas(f"c_{flavour}_{wp}", "", 850, 700)
        canvas.SetLeftMargin(0.18)
        canvas.SetRightMargin(0.19)
        h_eff.Draw("COLZ TEXT")
        for extension in ["png", "pdf"]:
            canvas.SaveAs(f"{output_2D}/BTagEfficiency_{dataset}_{flavour}_{wp}.{extension}")
        canvas.Close()


############# 1D plots: efficiency vs pt for each |eta| bin, the 3 WPs overlaid (as plot_btagging_efficiency in BTV lib/plotting.py) #############
wp_colors   = {"L": ROOT.TColor.GetColor("#dc3428"), "M": ROOT.TColor.GetColor("#f4c040"), "T": ROOT.TColor.GetColor("#4cac58")}   # Loose red, Medium yellow, Tight green
tagger      = "btagUParTAK4B" if era == "2024" else "btagPNetB"
for flavour, flavour_title in flavours.items():
    h_effs  = {wp: efficiency_map(flavour, wp) for wp in wps}
    h_ref   = h_effs["L"]
    h_all   = histos[f"BTagEff_{flavour}_all"]
    for ix in range(1, h_ref.GetNbinsX()+1):
        eta_lo, eta_hi  = h_ref.GetXaxis().GetBinLowEdge(ix), h_ref.GetXaxis().GetBinUpEdge(ix)
        pt_hi           = h_ref.GetYaxis().GetXmax()

        canvas  = ROOT.TCanvas(f"c1D_{flavour}_{ix}", "", 800, 700)
        canvas.SetLeftMargin(0.13)
        # pt axis from 0; only the bins with jets are drawn, so with good jets at pt > 30 GeV the first point is the 30-50 GeV bin
        frame   = canvas.DrawFrame(0., 0., pt_hi, 1.05, f"|#eta^{{jet}}| #in [{eta_lo:.3f}, {eta_hi:.3f}];p_{{T}}^{{jet}} [GeV];Efficiency")
        frame.GetYaxis().SetTitleOffset(1.3)

        legend  = ROOT.TLegend(0.15, 0.15, 0.32, 0.32) if flavour == "b" else ROOT.TLegend(0.15, 0.72, 0.32, 0.89)
        legend.SetBorderSize(0)
        graphs  = []
        for wp in wps:
            graph = ROOT.TGraphErrors()
            for iy in range(1, h_ref.GetNbinsY()+1):
                if h_all.GetBinContent(ix, iy) <= 0:                                    # empty bin (e.g. 20-30 GeV), not drawn
                    continue
                pt_center   = h_ref.GetYaxis().GetBinCenter(iy)
                pt_halfwidth= h_ref.GetYaxis().GetBinWidth(iy) / 2
                n_points    = graph.GetN()
                graph.SetPoint(n_points, pt_center, h_effs[wp].GetBinContent(ix, iy))
                graph.SetPointError(n_points, pt_halfwidth, 0.)                         # horizontal bar = pt bin, no vertical error
            graph.SetMarkerStyle(20)
            graph.SetMarkerColor(wp_colors[wp])
            graph.SetLineColor(wp_colors[wp])
            graph.Draw("P SAME")
            legend.AddEntry(graph, f"WP {wp}", "lp")
            graphs.append(graph)
        legend.Draw()

        label   = ROOT.TLatex()
        label.SetNDC()
        label.SetTextSize(0.033)
        label.SetTextAlign(33 if flavour != "b" else 31)
        y_text  = 0.88 if flavour != "b" else 0.16
        for i, line in enumerate([dataset, flavour_title, tagger] if flavour != "b" else [tagger, flavour_title, dataset]):
            label.DrawLatex(0.88, y_text - 0.04*i if flavour != "b" else y_text + 0.04*i, line)

        for extension in ["png", "pdf"]:
            canvas.SaveAs(f"{output_1D}/BTagEfficiency1D_{dataset}_{flavour}_eta_{eta_lo:.3f}_{eta_hi:.3f}.{extension}")
        canvas.Close()

print(f"Plots saved in {output}")
