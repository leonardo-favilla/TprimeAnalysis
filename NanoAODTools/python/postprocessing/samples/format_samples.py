from samples import sample_dict
import pandas as pd
import argparse

parser              = argparse.ArgumentParser(description="Generate samples summary.")
parser.add_argument("--year", required=True, help="Year of the campaign (e.g., 2022, 2022EE, 2023, 2023postBPix)")
args                = parser.parse_args()

year                = args.year
csv_output_path     = None
tex_output_path     = f"samples_summary_{year}.tex"
caption             = f"Summary of datasets used for {year} campaign."


datasets_to_run = [
                    f"QCD_{year}",
                    f"TT_{year}",
                    f"ZJetsToNuNu_2jets_{year}",
                    f"WJets_2jets_{year}",
                    f"DataJetMET_{year}",

                    # "QCD_2022",
                    # "TT_2022",
                    # "ZJetsToNuNu_2jets_2022",
                    # "WJets_2jets_2022",
                    # "DataJetMET_2022",
                    
                    # "QCD_2022EE",
                    # "TT_2022EE",
                    # "ZJetsToNuNu_2jets_2022EE",
                    # "WJets_2jets_2022EE",
                    # "DataJetMET_2022EE",
                    
                    # "QCD_2023",
                    # "TT_2023",
                    # "ZJetsToNuNu_2jets_2023",
                    # "WJets_2jets_2023",
                    # "DataJetMET_2023",
                    
                    # "QCD_2023postBPix",
                    # "TT_2023postBPix",
                    # "ZJetsToNuNu_2jets_2023postBPix",
                    # "WJets_2jets_2023postBPix",
                    # "DataJetMET_2023postBPix",

                    ]

samples             = []
list_of_components  = []

for dataset_to_run in datasets_to_run:
    if hasattr(sample_dict[dataset_to_run], "components"):
        components = sample_dict[dataset_to_run].components
    else:
        components = [sample_dict[dataset_to_run]]

    list_of_components.append(components)
    samples.extend(components)

def summarize_samples_variables(samples):
    summary = []
    for sample in samples:
        if "Data" in sample.label:
            summary.append({
                "sample": sample.process,
                "component": sample.label,
                "dataset": sample.dataset,
                "sigma": "None",
            })
        else:
            summary.append({
                "sample": sample.process,
                "component": sample.label,
                "dataset": sample.dataset,
                "sigma": sample.sigma,
            })

    df = pd.DataFrame(summary)
    return df


def generate_latex_table(df_summary):
    latex_code  = "\\begin{table}[htbp] % sidewaystable\n"
    latex_code += "\\centering\n"
    latex_code += "\\tiny\n"
    latex_code += "\\begin{tabular}{|l|l|r|}\n"
    latex_code += "\\hline\n"
    latex_code += "\\textbf{Component} & \\textbf{Dataset} & \\textbf{Cross section [pb]} \\\\ \n"
    latex_code += "\\hline\n"
    
    previous_sample = df_summary.iloc[0]['sample']
    for _, row in df_summary.iterrows():
        if row['sample'] != previous_sample:
            latex_code += "\\hline\n"
            previous_sample = row['sample']

        latex_code += "{} & {} & {} \\\\ \n".format(
            row['component'].replace('_', '\\_'),
            row['dataset'].replace('_', '\\_').replace("NANOAODSIM", "*"),
            row['sigma']
        )
    
    latex_code += "\\hline\n"
    latex_code += "\\hline\n"
    latex_code += "\\multicolumn{3}{|l|}{\\scriptsize* = NANOAODSIM} \\\\ \n"
    latex_code += "\\hline\n"
    latex_code += "\\end{tabular}\n"
    latex_code += "\\caption{"+caption+"}\n"
    latex_code += "\\label{tab:datasets_summary_"+year+"}\n"
    latex_code += "\\end{table}\n"
    
    return latex_code

df_summary  = summarize_samples_variables(samples)
# print(df_summary.to_string(index=False))
latex_table = generate_latex_table(df_summary)






if csv_output_path is not None:
    df_summary.to_csv(csv_output_path, index=False)
    print(f"CSV file saved to {csv_output_path}")
if tex_output_path is not None:
    with open(tex_output_path, 'w') as f:
        f.write(latex_table)
    print(f"Latex table saved to {tex_output_path}")