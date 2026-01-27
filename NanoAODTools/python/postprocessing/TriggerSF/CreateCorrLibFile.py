import json
import correctionlib.schemav2 as cs

def CreateCorrectionLibfile(triggerSF):

    corr = cs.Correction(
        name="triggerSF",
        version=1,
        inputs=[
            cs.Variable(name="PuppiMET_pt", type="real", description="Puppi MET pt"),
            cs.Variable(name="era", type="string", description="data taking era: 2022, 2022EE, 2023, 2023BPix"),
            cs.Variable(name="type", type="string", description="insert: sf, stat_err")
        ],
        output=cs.Variable(
            name="triggerSF", type="real", description="trigger scale factor"
        ),
        data=cs.Category(
            nodetype="category",
            input="era",
            content=[
                {
                    "key": key,
                    "value": cs.Category(
                        nodetype="category",
                        input="type",
                        content=[
                            {
                                "key": "sf",
                                "value": cs.Binning(
                                    nodetype="binning",
                                    input="PuppiMET_pt",
                                    edges=[100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000],
                                    content=triggerSF[key]["SF_values"],
                                    flow="clamp"
                                )
                            },
                            {
                                "key": "stat_err",
                                "value": cs.Binning(
                                    nodetype="binning",
                                    input="PuppiMET_pt",
                                    edges=[100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 500, 1000],
                                    content=triggerSF[key]["SF_errors"],
                                    flow="clamp"
                                )
                            }
                        ]
                    )
                } for key in triggerSF.keys()
            ]
        )
    )
            
    cset = cs.CorrectionSet(schema_version=2, corrections=[corr])
    with open(f"TriggerSF.json", "w") as f:
        json.dump(cset.dict(), f, indent=2)
    return 0


# inputs
SFtrigger = {
    "2022": {
        "SF_values": [1.39, 0.88, 0.710, 0.747, 0.817, 0.876, 0.933, 0.963, 0.989, 0.988, 0.987, 1.01],
        "SF_errors": [0.02, 0.01, 0.008, 0.007, 0.007, 0.007, 0.006, 0.006, 0.006, 0.007, 0.008, 0.01]
    },
    "2022EE": {
        "SF_values": [2.16, 1.198, 0.984, 0.938, 0.936, 0.951, 0.968, 0.976, 0.985, 0.989, 0.987, 0.972],
        "SF_errors": [0.02, 0.007, 0.005, 0.004, 0.004, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.006]
    },
    "2023": {
        "SF_values": [0.97, 0.961, 0.896, 0.893, 0.920, 0.941, 0.975, 0.985, 0.992, 0.996, 1.002, 0.998],
        "SF_errors": [0.01, 0.008, 0.006, 0.006, 0.005, 0.004, 0.004, 0.004, 0.002, 0.002, 0.002, 0.003]
    },
    "2023BPix": {
        "SF_values": [0.85, 0.80, 0.793, 0.827, 0.876, 0.918, 0.959, 0.975, 0.993, 0.995, 1.003, 0.999],
        "SF_errors": [0.01, 0.01, 0.008, 0.007, 0.007, 0.006, 0.005, 0.005, 0.003, 0.003, 0.003, 0.004]
    }
}

CreateCorrectionLibfile(SFtrigger)