info = {
    "qqZZ_powheg" : {
        "Name" : "q#bar{q} #rightarrow ZZ,Z#gamma^{*}",
        "Style" : "fill-lightblue",
        "add_perc_error" : 0.0,
        "Members" : [
            "zz4l-powheg"
        ]
    },
    "zzjj4l_ewk" : {
        "Name" : "ZZ + 2 jets EWK",
        "Style" : "fill-darkblue",
        "add_perc_error" : 0.0,
        "Members" : [
           "ZZJJTo4L-EWK"
        ]
    },
    "HZZ_signal" : {
        "Name" : "H #rightarrow ZZ",
        "Style" : "fill-lightred",
        "add_perc_error" : 0.0,
        "Members" : [
            "ggHZZ",
            "vbfHZZ",
            "ttH_HToZZ_4L",
            "WminusHToZZ",
            "WplusHToZZ",
            "ZHToZZ_4L"

        ]
    },
    "ggZZ" : {
        "Name" : "gg #rightarrow ZZ,Z#gamma^{*}",
        "Style" : "fill-blue",
        "add_perc_error" : 0.0,
        "Members" : [
            "ggZZ4e",
            "ggZZ4m",
            "ggZZ4t",
            "ggZZ2e2mu",
            "ggZZ2e2tau",
            "ggZZ2mu2tau"
        ]
    },
    "dy-jets" : {
        "Name" : "Drell-Yan",
        "Style" : "fill-green",
        "Members" : [
            "DYJetsToLLM-50"
        ]
    },
    "top" : {
        "Name" : "TT",
        "Style" : "fill-red",
        "add_perc_error" : 0.0,
        "Members" : [
            "tt-jets"
        ]
    },
    "wz3lnu-powheg" : {
        "Name" : "WZ",
        "Style" : "fill-maroon",
        "add_perc_error" : 0.0,
        "Members" : [
            "wz3lnu-powheg"
        ]
    },
    "VVV" : {
        "Name" : "t#bar{t}Z,VVV",
        "Style" : "fill-yellow",
        "add_perc_error" : 0.0,
        "Members" : [
            "ZZZ",
            "WZZ",
            "WWZ",
            "ttZ-jets"
        ]
    },
    "nonprompt" : {
        "Name" : "Z+X",
        "Style" : "fill-green",
        "add_perc_error" : 0.3,
        "Members" : [
            "DataEWKCorrected"
        ]
    },
    "data" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "AllData"
        ]
    },
    "data_all" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "AllData"
        ]
    },
    "data_B" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "data_DoubleEG_Run2017B-31Mar2018-v1",
            "data_DoubleMuon_Run2017B-31Mar2018-v1",
            "data_MuonEG_Run2017B-31Mar2018-v1",  
            "data_SingleMuon_Run2017B-31Mar2018-v1",
            "data_SingleElectron_Run2017B-31Mar2018-v1"
        ]
    },
    "data_C" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "data_DoubleEG_Run2017C-31Mar2018-v1",
            "data_DoubleMuon_Run2017C-31Mar2018-v1",
            "data_MuonEG_Run2017C-31Mar2018-v1",  
            "data_SingleMuon_Run2017C-31Mar2018-v1",
            "data_SingleElectron_Run2017C-31Mar2018-v1"
        ]
    },
    "data_D" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "data_DoubleEG_Run2017D-31Mar2018-v1",
            "data_DoubleMuon_Run2017D-31Mar2018-v1",
            "data_MuonEG_Run2017D-31Mar2018-v1",  
            "data_SingleMuon_Run2017D-31Mar2018-v1",
            "data_SingleElectron_Run2017D-31Mar2018-v1"
        ]
    },
    "data_E" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "data_DoubleEG_Run2017E-31Mar2018-v1",
            "data_DoubleMuon_Run2017E-31Mar2018-v1",
            "data_MuonEG_Run2017E-31Mar2018-v1",  
            "data_SingleMuon_Run2017E-31Mar2018-v1",
            "data_SingleElectron_Run2017E-31Mar2018-v1"
        ]
    },
    "data_F" : {
        "Name" : "Data",
        "Style" : "data",
        "Members" : [
            "data_DoubleEG_Run2017F-31Mar2018-v1",
            "data_DoubleMuon_Run2017F-31Mar2018-v1",
            "data_MuonEG_Run2017F-31Mar2018-v1",  
            "data_SingleMuon_Run2017F-31Mar2018-v1",
            "data_SingleElectron_Run2017F-31Mar2018-v1"
        ]
    }
}

tmpinfo = {}
for key, value in info.items():
    tmpinfo.update({key.replace("-", "_") : value})

info.update(tmpinfo)
