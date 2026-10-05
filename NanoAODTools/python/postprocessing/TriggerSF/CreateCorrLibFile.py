import json
import correctionlib.schemav2 as cs

def CreateCorrectionLibfile(triggerSF):

    corr = cs.Correction(
        name="triggerSF",
        version=1,
        inputs=[
            cs.Variable(name="PuppiMET_pt", type="real", description="Puppi MET pt"),
            cs.Variable(name="era", type="string", description="data taking era: 2022, 2022EE, 2023, 2023BPix, 2024"),
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
        "SF_values": [0.69502, 0.60488, 0.60392, 0.71083, 0.80534, 0.88085, 0.94704, 0.97209, 0.98547, 0.99269, 0.99775, 0.99474],
        "SF_errors": [0.01889, 0.01282, 0.00960, 0.00880, 0.00787, 0.00712, 0.00609, 0.00524, 0.00370, 0.00393, 0.00256, 0.00376]
    },
    "2022EE": {
        "SF_values": [0.94458, 0.92988, 0.89969, 0.91737, 0.94110, 0.96287, 0.97668, 0.98601, 0.99434, 0.99716, 0.99701, 0.99888],
        "SF_errors": [0.01312, 0.00937, 0.00664, 0.00528, 0.00428, 0.00353, 0.00305, 0.00272, 0.00182, 0.00189, 0.00141, 0.00211]
    },
    "2023": {
        "SF_values": [0.97, 0.961, 0.896, 0.893, 0.920, 0.941, 0.975, 0.985, 0.992, 0.996, 1.002, 0.998],
        "SF_errors": [0.01, 0.01, 0.007, 0.006, 0.005, 0.004, 0.004, 0.003, 0.002, 0.002, 0.002, 0.003]
    },
    "2023BPix": {
        "SF_values": [0.85, 0.80, 0.793, 0.827, 0.876, 0.918, 0.959, 0.975, 0.993, 0.995, 1.003, 0.999],
        "SF_errors": [0.02, 0.01, 0.01, 0.008, 0.007, 0.006, 0.005, 0.005, 0.003, 0.003, 0.003, 0.004]
    },
    "2024": {
        "SF_values": [0.68945, 0.71855, 0.77743, 0.82538, 0.89126, 0.94004, 0.97226, 0.98788, 0.99729, 0.99802, 1.00101, 0.99924],
        "SF_errors": [0.00503, 0.00413, 0.00348, 0.00294, 0.00260, 0.00224, 0.00198, 0.00182, 0.00125, 0.00133, 0.00122, 0.00115]
    }
}

CreateCorrectionLibfile(SFtrigger)