import ROOT

# global parameters
intLumi = 1
intLumiLabel = "L = 3 ab^{-1}"
ana_tex = "(VBF) e^{+}e^{-} #rightarrow #nu^{+}#nu^{-} H, H #rightarrow  b b"
delphesVersion = "3.4.2"
energy = 365.0
collider = "FCC-ee"
formats = ["png", "pdf"]

outdir         = '/eos/user/f/fdmartin/FCC365_histograms/cut_missing_p-15_new_vbf_zh' 
inputDir       = './outputs/treemaker_bjet/plots/cuts/dijet_cut_missing_p-15' 

plotStatUnc = True

colors = {}
colors["VBF"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2
colors["WW"] = ROOT.kCyan - 2
colors["tt"] = ROOT.kBlue - 2
colors["ZH"] = ROOT.kMagenta - 8

procs = {}
procs["signal"] = {"VBF": ["wzp6_ee_nuenueH_Hbb_ecm365"]} 
#, "VBF": ["wzp6_ee_numunumuH_Hbb_ecm365_vbf"]
procs["backgrounds"] = { "ZZ": ["p8_ee_ZZ_ecm365"], "WW": ["p8_ee_WW_ecm365"], "tt": ["p8_ee_tt_ecm365"], "ZH": ["wzp6_ee_numunumuH_Hbb_ecm365"] }

legend = {}
legend["VBF"] = "VBF"
legend["ZZ"] = "ZZ"
legend["WW"] = "WW"
legend["tt"] = "tt"
legend["ZH"] = "ZH"

hists = {}

#hists["higgs_recoil_m_mu"] = {
 #   "output": "higgs_recoil_m_mu",
 #   "logy": False,
 #   "stack": True,
 #   "rebin": 100,
 #   "xmin": 120,
 #   "xmax": 140,
 #   "ymin": 0,
 #   "ymax": 2000,
 #   "xtitle": "Recoil (GeV)",
 #   "ytitle": "Events / 100 MeV",
#}

#hists["higgs_recoil_m_el"] = {
#    "output": "higgs_recoil_m_el",
#    "logy": False,
#    "stack": True,
#    "rebin": 100,
#    "xmin": 120,
#    "xmax": 140,
#    "ymin": 0,
#    "ymax": 2000,
#    "xtitle": "Recoil (GeV)",
#    "ytitle": "Events / 100 MeV",
#}

hists["missingEnergy_energy"] = {
    "output": "missingEnergy_energy",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 0,
    "xmax": 200,
    "ymin": 0,
    "ymax": 100,
    "xtitle": "MET (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["missing_p"] = {
    "output": "missing_p",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 15,
    "xmax": 170,
    "ymin": 0,
    "ymax": 2000,
    "xtitle": "Missing_p (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 95,
    "xmax": 155,
    "ymin": 0,
    "ymax": 20000,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events / 2 GeV",
}


hists["scoresum_B"] = {
    "output": "scoresum_B",
    "logy": True,
    "stack": True,
    "rebin": 1,
    "xmin": 0,
    "xmax": 1.0,
    "ymin": 1,
    "ymax": 5000000000,
    "xtitle": "p_{1}(B) + p_{2}(B)",
    "ytitle": "Events",
}


hists["cosTheta_miss"] = {
    "output": "cosTheta_miss",
    "logy": False,
    "stack": True,
    "rebin": 1,
    "xmin": 0,
    "xmax": 1.0,
    "ymin": 0,
    "ymax": 1000,
    "xtitle": "cosTheta_miss",
    "ytitle": "Events",
}
