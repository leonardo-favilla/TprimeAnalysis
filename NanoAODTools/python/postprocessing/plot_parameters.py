import os

var_names = ["top_pt", "top_m", "met_pt", "min_dphi", "max_eta_jet"]
categories = ["resolved", "mix","merged"]

nbins = { 
    "top_pt":
             { "resolved" : 15,
               "mix": 10,
               "merged": 6 }, 
    "top_m":
             { "resolved" : 15,
               "mix": 15,
               "merged": 8 } ,
    "met_pt":
             { "resolved" : 20,
               "mix": 20,
               "merged":  5} ,
    "min_dphi":
             { "resolved" : 24,
               "mix": 24,
               "merged": 5} ,
    "max_eta_jet":
             { "resolved" : 6,
               "mix": 6,
               "merged": 4 }, 
    "mt":
             { "resolved" : 30,
               "mix": 30,
               "merged": 30 }
    }

xmin = { 
    "top_pt":
             { "resolved" : 0,
               "mix": 300,
               "merged":  400}, 
    "top_m":
             { "resolved" : 50,
               "mix": 50,
               "merged":  50} ,
    "met_pt":
             { "resolved" : 150,
               "mix": 150,
               "merged": 150 } ,
    "min_dphi":
             { "resolved" : 0.6,
               "mix": 0.6,
               "merged":  0.6} ,
    "max_eta_jet":
             { "resolved" : 0,
               "mix": 0,
               "merged":0  },
        "mt":
             { "resolved" : 0,
               "mix": 0,
               "merged": 0 }
    }

xmax = { 
    "top_pt":
             { "resolved" : 400,
               "mix": 500,
               "merged":  1000} ,
    "top_m":
             { "resolved" : 350,
               "mix": 350,
               "merged":  350} ,
    "met_pt":
             { "resolved" : 1000,
               "mix": 1000,
               "merged":  1000} ,
    "min_dphi":
             { "resolved" : 3,
               "mix": 3,
               "merged": 3 } ,
    "max_eta_jet":
             { "resolved" : 6,
               "mix": 6,
               "merged":6  },
    "mt":
             { "resolved" : 1000,
               "mix": 1000,
               "merged": 1000 }
    }

minimum_stack ={"Tprime": 
                {'efficiency':10**(-4),
                 'workflow': 10**(-2),
                 'top_pt': 10**(-2),
                 'top_m':10**(-3),
                 'met_pt':10**(-2),
                 'min_dphi':10**(-3),
                 "max_eta_jet":10**(-2),
                 "mt": 10**(-3)
                       },
                "DM":
                {'efficiency':10**(-5),
                 'workflow': 10**(-2),
                 'top_pt': 10**(-2),
                 'top_m':10**(-3),
                 'met_pt':10**(-2),
                 'min_dphi':10**(-3),
                 "max_eta_jet":10**(-2),
                 "mt": 10**(-3)
             }
}
