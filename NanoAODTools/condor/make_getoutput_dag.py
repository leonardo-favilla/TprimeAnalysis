import sys
import os
import argparse
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


parser  = argparse.ArgumentParser()
parser.add_argument("-d","--datasets",required=True,help="Comma-separated list of datasets (can be either entire samples or single components)")
args    = parser.parse_args()
username        = str(os.environ.get('USER'))
inituser        = str(os.environ.get('USER')[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"

# --------------------------------------------------
# Get datasets
# --------------------------------------------------

datasets    = [dataset.strip() for dataset in args.datasets.split(",") if dataset.strip()]
samples     = []
for dataset in datasets:
    if dataset not in sample_dict.keys():
        print(f"Dataset {dataset} not found")
        sys.exit()
    elif dataset in sample_dict.keys():
        if hasattr(sample_dict[dataset], "components"):
            samples.extend(sample_dict[dataset].components)
        else:
            samples.extend([sample_dict[dataset]])

print([sample.label for sample in samples])

# --------------------------------------------------
# Create DAG
# --------------------------------------------------

condor_folder   = f"/afs/cern.ch/user/{inituser}/{username}/TprimeAnalysis/NanoAODTools/condor/condor_getoutputs"
dag_file        = f"{condor_folder}/getoutputs.dag"

with open(dag_file, "w") as f:
    for i, component in enumerate(samples):
        jobname         = f"job_{i}"
        condor_subfolder   = f"/afs/cern.ch/user/{inituser}/{username}/TprimeAnalysis/NanoAODTools/condor/condor_getoutputs/{component.label}"
        # Define job
        f.write(
            f"JOB {jobname} {condor_subfolder}/condor.sub\n"
        )

        # Pass variables to the .sub file
        f.write(
            f'VARS {jobname} '
            f'dataset="{component.label}" '
            f'jobname="{jobname}"\n'
        )

        # Make this job depend on the previous one
        if i > 0:
            previous_job = f"job_{i - 1}"

            f.write(
                f"PARENT {previous_job} CHILD {jobname}\n"
            )


print(f"Created {dag_file}")
print(f"Number of jobs: {len(samples)}")

for i, component in enumerate(samples):
    print(f"  {i}: {component.label}")