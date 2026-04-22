import ROOT
import ctypes
import copy



fitDiagnostics_FilePath             = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep_nobjetlep_inside_tophadr_using_tightbjet/workspace_MixedTight_test/MT_W/fitDiagnostics_pt0to200.root"
prefitDistributions_FilePath        = "/eos/user/l/lfavilla/RDF_DManalysis/TopSF/results/run2023_SemiLep_nobjetlep_inside_tophadr_using_tightbjet/workspace_MixedTight_test/MT_W/pt0to200.root"

fitDiagnostics_File                 = ROOT.TFile.Open(fitDiagnostics_FilePath, "READ")
prefitDistributions_File            = ROOT.TFile.Open(prefitDistributions_FilePath, "READ")



# norm_match_mc_data # 
fit                                         = fitDiagnostics_File.Get("fit_s")
norm_factor                                 = fit.constPars().find("norm_match_mc_data")

# prefit unscaled yields #
mc_prefit_unscaled_fail_topmatched          = prefitDistributions_File.Get("topmatched_MT_W_pt0to200_fail_nominal")
mc_prefit_unscaled_fail_nonmatched          = prefitDistributions_File.Get("nonmatched_MT_W_pt0to200_fail_nominal")
mc_prefit_unscaled_fail_other               = prefitDistributions_File.Get("other_MT_W_pt0to200_fail_nominal")
mc_prefit_unscaled_fail_total               = copy.deepcopy(mc_prefit_unscaled_fail_topmatched)
mc_prefit_unscaled_fail_total.Add(mc_prefit_unscaled_fail_nonmatched)
mc_prefit_unscaled_fail_total.Add(mc_prefit_unscaled_fail_other)

mc_prefit_unscaled_fail_topmatched_err      = ctypes.c_double(0.0)
mc_prefit_unscaled_fail_topmatched_integral = mc_prefit_unscaled_fail_topmatched.IntegralAndError(1, mc_prefit_unscaled_fail_topmatched.GetNbinsX(), mc_prefit_unscaled_fail_topmatched_err)
mc_prefit_unscaled_fail_nonmatched_err      = ctypes.c_double(0.0)
mc_prefit_unscaled_fail_nonmatched_integral = mc_prefit_unscaled_fail_nonmatched.IntegralAndError(1, mc_prefit_unscaled_fail_nonmatched.GetNbinsX(), mc_prefit_unscaled_fail_nonmatched_err)
mc_prefit_unscaled_fail_other_err           = ctypes.c_double(0.0)
mc_prefit_unscaled_fail_other_integral      = mc_prefit_unscaled_fail_other.IntegralAndError(1, mc_prefit_unscaled_fail_other.GetNbinsX(), mc_prefit_unscaled_fail_other_err)
mc_prefit_unscaled_fail_total_err           = ctypes.c_double(0.0)
mc_prefit_unscaled_fail_total_integral      = mc_prefit_unscaled_fail_total.IntegralAndError(1, mc_prefit_unscaled_fail_total.GetNbinsX(), mc_prefit_unscaled_fail_total_err)


# prefit scaled yields #
mc_prefit_scaled_fail_topmatched            = fitDiagnostics_File.Get("shapes_prefit/fail/topmatched")
mc_prefit_scaled_fail_nonmatched            = fitDiagnostics_File.Get("shapes_prefit/fail/nonmatched")
mc_prefit_scaled_fail_other                 = fitDiagnostics_File.Get("shapes_prefit/fail/other")
mc_prefit_scaled_fail_total                 = fitDiagnostics_File.Get("shapes_prefit/fail/total")

mc_prefit_scaled_fail_topmatched_err        = ctypes.c_double(0.0)
mc_prefit_scaled_fail_topmatched_integral   = mc_prefit_scaled_fail_topmatched.IntegralAndError(1, mc_prefit_scaled_fail_topmatched.GetNbinsX(), mc_prefit_scaled_fail_topmatched_err)
mc_prefit_scaled_fail_nonmatched_err        = ctypes.c_double(0.0)
mc_prefit_scaled_fail_nonmatched_integral   = mc_prefit_scaled_fail_nonmatched.IntegralAndError(1, mc_prefit_scaled_fail_nonmatched.GetNbinsX(), mc_prefit_scaled_fail_nonmatched_err)
mc_prefit_scaled_fail_other_err             = ctypes.c_double(0.0)
mc_prefit_scaled_fail_other_integral        = mc_prefit_scaled_fail_other.IntegralAndError(1, mc_prefit_scaled_fail_other.GetNbinsX(), mc_prefit_scaled_fail_other_err)
mc_prefit_scaled_fail_total_err             = ctypes.c_double(0.0)
mc_prefit_scaled_fail_total_integral        = mc_prefit_scaled_fail_total.IntegralAndError(1, mc_prefit_scaled_fail_total.GetNbinsX(), mc_prefit_scaled_fail_total_err)


norms                                       = fitDiagnostics_File.Get("norm_prefit")
norm_mc_prefit_scaled_fail_topmatched       = norms.find("fail/topmatched")
norm_mc_prefit_scaled_fail_nonmatched       = norms.find("fail/nonmatched")
norm_mc_prefit_scaled_fail_other            = norms.find("fail/other")
norm_mc_prefit_scaled_fail_total            = norms.find("fail/total")



print(f"norm_match_mc_data:                     {norm_factor.getVal()}")
print("\n")
print("Prefit UNSCALED yields using histo.IntegralAndError():")
print(f"mc_prefit_unscaled_fail_topmatched:     {mc_prefit_unscaled_fail_topmatched_integral}\t±\t{mc_prefit_unscaled_fail_topmatched_err.value}")
print(f"mc_prefit_unscaled_fail_nonmatched:     {mc_prefit_unscaled_fail_nonmatched_integral}\t±\t{mc_prefit_unscaled_fail_nonmatched_err.value}")
print(f"mc_prefit_unscaled_fail_other:          {mc_prefit_unscaled_fail_other_integral}\t±\t{mc_prefit_unscaled_fail_other_err.value}")
print(f"mc_prefit_unscaled_fail_total:          {mc_prefit_unscaled_fail_total_integral}\t±\t{mc_prefit_unscaled_fail_total_err.value}")

print("\n")
print("Prefit SCALED yields using histo.IntegralAndError():")
print(f"mc_prefit_scaled_fail_topmatched:       {mc_prefit_scaled_fail_topmatched_integral}\t±\t{mc_prefit_scaled_fail_topmatched_err.value}")
print(f"mc_prefit_scaled_fail_nonmatched:       {mc_prefit_scaled_fail_nonmatched_integral}\t±\t{mc_prefit_scaled_fail_nonmatched_err.value}")
print(f"mc_prefit_scaled_fail_other:            {mc_prefit_scaled_fail_other_integral}\t±\t{mc_prefit_scaled_fail_other_err.value}")
print(f"mc_prefit_scaled_fail_total:            {mc_prefit_scaled_fail_total_integral}\t±\t{mc_prefit_scaled_fail_total_err.value}")

print("\n")
print("Prefit SCALED yields using norm_prefit:")
print(f"mc_prefit_scaled_fail_topmatched:       {norm_mc_prefit_scaled_fail_topmatched.getVal()}\t±\t{norm_mc_prefit_scaled_fail_topmatched.getError()}")
print(f"mc_prefit_scaled_fail_nonmatched:       {norm_mc_prefit_scaled_fail_nonmatched.getVal()}\t±\t{norm_mc_prefit_scaled_fail_nonmatched.getError()}")
print(f"mc_prefit_scaled_fail_other:            {norm_mc_prefit_scaled_fail_other.getVal()}\t±\t{norm_mc_prefit_scaled_fail_other.getError()}")
print(f"mc_prefit_scaled_fail_total:            {norm_mc_prefit_scaled_fail_total.getVal()}\t±\t{norm_mc_prefit_scaled_fail_total.getError()}")