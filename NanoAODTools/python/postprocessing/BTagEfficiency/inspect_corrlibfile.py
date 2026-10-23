import correctionlib

filename = "BTagEfficiency_2024.json"
cset     = correctionlib.CorrectionSet.from_file(filename)

print("Available corrections:")
for name in cset:
    print(f"  {name}")


corr     = cset["UParTAK4_efficiency_TT"]
print(f"Name:        {corr.name}")
print(f"Version:     {corr.version}")
print(f"Description: {corr.description}")

print("Inputs:")
for variable in corr.inputs:
    print(
        f"  {variable.name:20s}"
        f"type={variable.type:8s}"
        f"description={variable.description}"
    )

print(
    f"Output: {corr.output.name} "
    f"({corr.output.type}) — {corr.output.description}"
)

eff_M_b_1p0_50  = corr.evaluate("M", 5, 1.0, 50.0)
eff_T_b_2p2_100 = corr.evaluate("T", 5, 2.2, 100.0)

print(f"Efficiency for Medium WP, b jet, |eta|=1.0, pT=50 GeV: {eff_M_b_1p0_50}")
print(f"Efficiency for Tight WP, b jet, |eta|=2.2, pT=100 GeV: {eff_T_b_2p2_100}")