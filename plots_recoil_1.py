import ROOT

# global parameters
intLumi = 1
intLumiLabel = "L = 2.4 ab^{-1}"
ana_tex = "(VBF) e^{+}e^{-} #rightarrow #nu^{+}#nu^{-} H, H #rightarrow  b b"
delphesVersion = "3.4.2"
energy = 365.0
collider = "FCC-ee"
formats = ["png", "pdf"]

outdir         = './outputs/plots/flavor_higgs/' 
inputDir       = './outputs/histmaker_higgs/flavor_1/' 

plotStatUnc = True

colors = {}
colors["VBF"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2
colors["WW"] = ROOT.kCyan - 2
colors["tt"] = ROOT.kBlue - 2
colors["eeH"] = ROOT.kMagenta - 8
colors["mumuH"] = ROOT.kMagenta - 5
colors["tautauH"] = ROOT.kMagenta - 1

procs = {}
procs["signal"] = {"VBF": ["wzp6_ee_nunuH_ecm365"]}
procs["backgrounds"] = {"ZZ": ["p8_ee_ZZ_ecm365"], "WW": ["p8_ee_WW_ecm365"], "tt": ["p8_ee_tt_ecm365"], "eeH": ["wzp6_ee_eeH_ecm365"], "mumuH": ["wzp6_ee_mumuH_ecm365"], "tautauH": ["wzp6_ee_tautauH_ecm365"] }

legend = {}
legend["VBF"] = "VBF"
legend["ZZ"] = "ZZ"
legend["WW"] = "WW"
legend["tt"] = "tt"
legend["eeH"] = "eeH"
legend["mumuH"] = "mumuH"
legend["tautauH"] = "tautauH"

hists = {}

hists["zmumu_recoil_m"] = {
    "output": "zmumu_recoil_m",
    "logy": False,
    "stack": True,
    "rebin": 100,
    "xmin": 120,
    "xmax": 140,
    "ymin": 0,
    "ymax": 2000,
    "xtitle": "Recoil (GeV)",
    "ytitle": "Events / 100 MeV",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 50,
    "xmax": 150,
    "ymin": 0,
    "ymax": 4000,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["scoresum_B"] = {
    "output": "scoresum_B",
    "logy": True,
    "stack": True,
    "rebin": 1,
    "xmin": 0,
    "xmax": 2.0,
    "ymin": 1,
    "ymax": 100000,
    "xtitle": "p_{1}(B) + p_{2}(B)",
    "ytitle": "Events",
}
