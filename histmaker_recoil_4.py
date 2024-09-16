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
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions_3.h"]

# Define the input dir (optional)
#inputDir    = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"
#inputDir    = "./localSamples/"

#Optional: output directory, default is local running directory
outputDir   = "./outputs/histmaker_3/recoil_3/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 2400000 # 2.4 /ab


# define some binning for various histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (2000, 0, 200) # 100 MeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (10000, 0, 1)

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
    
    # define some aliases to be used later on
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Muon0", "Muon#0.index")
    #df = df.Alias("Electron0", "Electron#0.index")  #######

    # get all the leptons from the collection
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    #df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")############
    
    # select leptons with momentum > 20 GeV
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
    #df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)") #########
    
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    ########################
   # df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
   # df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
   # df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
   # df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
   # df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")    
    
    # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    df = df.Define("muons_iso", "FCCAnalyses::HIGGS_ANALYSIS::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
    df = df.Define("muons_sel_iso", "FCCAnalyses::HIGGS_ANALYSIS::sel_iso(0.25)(muons, muons_iso)")
  #  df = df.Define("electrons_iso", "FCCAnalyses::HIGGS_ANALYSIS::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
  #  df = df.Define("electrons_sel_iso", "FCCAnalyses::HIGGS_ANALYSIS::sel_iso(0.25)(electrons, electrons_iso)")
    
        
    # baseline histograms, before any selection cuts (store with _cut0) muons
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))

    # baseline histograms, before any selection cuts (store with _cut0) electrons
   # results.append(df.Histo1D(("electrons_p_cut0", "", *bins_p_mu), "electrons_p"))
   # results.append(df.Histo1D(("electrons_theta_cut0", "", *bins_theta), "electrons_theta"))
   # results.append(df.Histo1D(("electrons_phi_cut0", "", *bins_phi), "electrons_phi"))
   # results.append(df.Histo1D(("electrons_q_cut0", "", *bins_charge), "electrons_q"))
   # results.append(df.Histo1D(("electrons_no_cut0", "", *bins_count), "electrons_no"))
   # results.append(df.Histo1D(("electrons_iso_cut0", "", *bins_iso), "electrons_iso"))
    

    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))


    #########
    ### CUT 1: at least 1 muon with at least one isolated one (muons)
    #########
    df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0")
    df = df.Define("cut1_muons", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1_muons"))

    ### CUT 1: at least 1 electron with at least one isolated one (electrons)
    #########
  #  df = df.Filter("electrons_no >= 1 && electrons_sel_iso.size() > 0")
  #  df = df.Define("cut1_electrons", "1")
  #  results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1_electrons"))

    
    #########
    ### CUT 2 :at least 2 opposite-sign (OS) leptons
    #########
   # df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")
    df = df.Filter("muons_no >= 2 && Sum(muons_q) == 0")
    df = df.Define("cut2_muons", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2_muons"))

    #########
    ### CUT 2 :at least 2 opposite-sign (OS) leptons
    #########
    # df = df.Filter("electrons_no >= 2 && abs(Sum(electrons_q)) < electrons_q.size()")
   # df = df.Filter("electrons_no >= 2 && Sum(electrons_q) == 0")
   # df = df.Define("cut2_electrons", "2")
   # results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2_electrons"))

    # Higgs mass window
   # df = df.Define("combined_leptons", "Concatenate(muons, electrons)")
   # df = df.Define("higgsbuilder_result", "FCCAnalyses::HIGGS_ANALYSIS::HiggsResonanceBuilder(125, 150, 0.4, 365, false)(combined_leptons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("higgsbuilder_result", "FCCAnalyses::HIGGS_ANALYSIS::HiggsResonanceBuilder(125, 150, 0.4, 365, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("higgs", "Vec_rp{higgsbuilder_result[0]}") # the Higgs
    df = df.Define("higgs_muons", "Vec_rp{higgsbuilder_result[1],higgsbuilder_result[2]}") # the leptons 
    df = df.Define("higgs_m", "FCCAnalyses::ReconstructedParticle::get_mass(higgs)")
    df = df.Define("higgs_p", "FCCAnalyses::ReconstructedParticle::get_p(higgs)")
    df = df.Define("higgs_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(365)(higgs)")
    df = df.Define("higgs_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(higgs_recoil)[0]")
    df = df.Define("higgs_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(higgs_muons)") 

    #########
    ### CUT 3: Higgs mass window
    ######### 
    df = df.Filter("higgs_m > 120 && higgs_m < 130")
    df = df.Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))

    #########
    ### CUT 4: Higgs momentum
    #########
    df = df.Filter("higgs_p > 20 && higgs_p < 70")
    df = df.Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    
    #########
    ### CUT 5: cosThetaMiss
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::HIGGS_ANALYSIS::missingEnergy(365., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::HIGGS_ANALYSIS::get_cosTheta_miss(MissingET)")
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss")) # plot it before the cut

    df = df.Filter("cosTheta_miss < 0.98")
    df = df.Define("cut5", "5")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    #########
    ### CUT 6: recoil mass window
    #########  
    df = df.Filter("higgs_recoil_m < 140 && higgs_recoil_m > 120")
    df = df.Define("cut6", "6")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))
    

    ########################
    # Final histograms
    ########################
    results.append(df.Histo1D(("higgs_m", "", *bins_m_ll), "higgs_m"))
    results.append(df.Histo1D(("higgs_recoil_m", "", *bins_recoil), "higgs_recoil_m"))
    results.append(df.Histo1D(("higgs_p", "", *bins_p_ll), "higgs_p"))
    results.append(df.Histo1D(("higgs_muons_p", "", *bins_p_mu), "higgs_muons_p"))
    

    return results, weightsum
