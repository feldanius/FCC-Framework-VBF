# list of processes (mandatory)
processList = {
    'wzp6_ee_numunumuH_Hbb_ecm365_vbf': {'fraction':1, 'crossSection': 0.004814},
    'wzp6_ee_nuenueH_Hbb_ecm365':  {'fraction':1, 'crossSection': 0.02181},
    'wzp6_ee_nunuH_Hbb_ecm365':   {'fraction':1, 'crossSection': 0.03143},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag     = "/eos/user/f/fdmartin/FCC365_jets_no_e_mu"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Define the input dir (optional)
inputDir    = "./outputs/treemaker_bjet/flavor"
#inputDir    = "./outputs/treemaker_bjet/plots/cuts/dijet_cut_mjj-mH_30Gev"

#Optional: output directory, default is local running directory
outputDir   = "/eos/user/f/fdmartin/FCC365_jets_b_tagging_cut_missing_p-15"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 3000000 # 3 /ab


# define some binning for various histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (2000, 0, 200) # 100 MeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (10000, 0, 1)

bins_m_jj = (100, 95, 155)  # 1 GeV bins
bins_score = (50, 0, 2.0)  #

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)



# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
   
    #########
    ### CUT : cut on the jet tagging score to select H->bb events
    #########
    df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")
    results.append(df.Histo1D(("scoresum_B", "", *bins_score), "scoresum_B"))
    #########
    ### CUT : cut jj_m
    #########
    df = df.Filter("jj_m > 95 && jj_m < 155")
    df = df.Filter("All(missing_p > 15 && missing_p < 170)")
   #df = df.Filter("missing_p > 15 && missing_p < 170")
    df = df.Filter("scoresum_B > 1.0")

    #results.append(df.Histo1D(("higgs_recoil_m_mu", "", *bins_recoil), "higgs_recoil_m_mu"))
    #results.append(df.Histo1D(("higgs_recoil_m_el", "", *bins_recoil), "higgs_recoil_m_el"))
    #results.append(df.Histo1D(("higgs_p_mu", "", *bins_p_ll), "higgs_p_mu"))
    #results.append(df.Histo1D(("higgs_p_el", "", *bins_p_ll), "higgs_p_el"))
    results.append(df.Histo1D(("jj_m", "", *bins_m_jj), "jj_m"))
    results.append(df.Histo1D(("missingEnergy_energy", "", *bins_recoil), "missingEnergy.energy"))
    results.append(df.Histo1D(("cosTheta_miss", "", *bins_cosThetaMiss), "cosTheta_miss"))
    results.append(df.Histo1D(("missing_p", "", *bins_p_ll), "missing_p"))

    return results, weightsum
