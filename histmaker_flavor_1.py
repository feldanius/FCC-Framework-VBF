# list of processes (mandatory)
processList = {
   'wzp6_ee_eeH_ecm365':    {'fraction':1, 'crossSection': 0.00739}, 
    'wzp6_ee_mumuH_ecm365':  {'fraction':1, 'crossSection': 0.004185},
    'wzp6_ee_tautauH_ecm365':   {'fraction':1, 'crossSection': 0.004172},
    'p8_ee_tt_ecm365': {'fraction':1, 'crossSection': 0.8},
    'p8_ee_WW_ecm365': {'fraction':1, 'crossSection': 10.7165},
    'p8_ee_ZZ_ecm365': {'fraction':1, 'crossSection': 0.6428},
    'wzp6_ee_nunuH_ecm365': {'fraction':1, 'crossSection': 0.05394},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Define the input dir (optional)
inputDir    = "./outputs/treemaker_2/flavor_2/"

#Optional: output directory, default is local running directory
outputDir   = "./outputs/histmaker_higgs/flavor_1/"

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

bins_m_jj = (100, 50, 150)  # 1 GeV bins
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

    #df = df.Define("var_type_higgs_m_mu", "decltype(higgs_m_mu)")
    #df = df.Display({"var_type_higgs_m_mu"}).Print()

    #higgs_m_mu and higgs_m_el only has data until 100 GeV
   #########
    ### CUT 4: Higgs mass window
    #########
    #df = df.Filter("higgs_m_mu > 120 && higgs_m_mu < 130")
    #df = df.Filter("higgs_m_el > 120 && higgs_m_el < 130")

    #higgs_p_mu has data until 120 GeV
    #########
    ### CUT 5: Higgs momentum
    #########
    #df = df.Filter("higgs_p_mu > 10 && higgs_p_mu < 100")
    #df = df.Filter("higgs_p_el > 10 && higgs_p_el < 100")

    #########
    ### CUT 6: recoil mass window
    #########
    df = df.Filter("higgs_recoil_m_mu < 240 && higgs_recoil_m_mu > 220")
    df = df.Filter("higgs_recoil_m_el < 240 && higgs_recoil_m_el > 220")

  #  df = df.Define("higgs_m_mu_0", "higgs_m_mu[0]")
  #  df = df.Define("higgs_m_el_0", "higgs_m_el[0]")
  #  df = df.Define("higgs_p_mu_0", "higgs_p_mu[0]")
  #  df = df.Define("higgs_p_el_0", "higgs_p_el[0]")
  #  df = df.Define("higgs_recoil_m_mu_0", "higgs_recoil_m_mu[0]")
  #  df = df.Define("higgs_recoil_m_el_0", "higgs_recoil_m_el[0]")
 ### CUT 4: Higgs mass window
  #  df = df.Filter("higgs_m_mu_0 > 120 && higgs_m_mu_0 < 130")
  #  df = df.Filter("higgs_m_el_0 > 120 && higgs_m_el_0 < 130")
### CUT 5: Higgs momentum
  #  df = df.Filter("higgs_p_mu_0 > 10 && higgs_p_mu_0 < 100")
  #  df = df.Filter("higgs_p_el_0 > 10 && higgs_p_el_0 < 100")
### CUT 6: recoil mass window
  #  df = df.Filter("higgs_recoil_m_mu_0 < 240 && higgs_recoil_m_mu_0 > 220")
  #  df = df.Filter("higgs_recoil_m_el_0 < 240 && higgs_recoil_m_el_0 > 220")


  ##  df = df.Define("higgs_m_mu_0", "higgs_m_mu.fData")
  ##  df = df.Define("higgs_m_el_0", "higgs_m_el.fData")
  #  df = df.Define("higgs_p_mu_0", "higgs_p_mu.fData")
  #  df = df.Define("higgs_p_el_0", "higgs_p_el.fData")
  ##  df = df.Filter("higgs_m_mu_0 > 120 && higgs_m_mu_0 < 130")
  ##  df = df.Filter("higgs_m_el_0 > 120 && higgs_m_el_0 < 130")
  #  df = df.Filter("higgs_p_mu_0 > 10 && higgs_p_mu_0 < 100")
  #  df = df.Filter("higgs_p_el_0 > 10 && higgs_p_el_0 < 100")
 

   
    #########
    ### CUT 7: cut on the jet tagging score to select H->bb events
    #########
    df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")
    results.append(df.Histo1D(("scoresum_B", "", *bins_score), "scoresum_B"))

    df = df.Filter("scoresum_B > 1.0")

   # results.append(df.Histo1D(("higgs_m_mu", "", *bins_m_ll), "higgs_m_mu"))
   # results.append(df.Histo1D(("higgs_m_el", "", *bins_m_ll), "higgs_m_el"))
    results.append(df.Histo1D(("higgs_recoil_m_mu", "", *bins_recoil), "higgs_recoil_m_mu"))
    results.append(df.Histo1D(("higgs_recoil_m_el", "", *bins_recoil), "higgs_recoil_m_el"))
    results.append(df.Histo1D(("higgs_p_mu", "", *bins_p_ll), "higgs_p_mu"))
    results.append(df.Histo1D(("higgs_p_el", "", *bins_p_ll), "higgs_p_el"))
    results.append(df.Histo1D(("jj_m", "", *bins_m_jj), "jj_m"))

    return results, weightsum
