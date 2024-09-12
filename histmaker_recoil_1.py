import ROOT
import os

# list of processes (mandatory)
#processList = {
#    'wzp6_ee_eeH_ecm365':    {'fraction':1, 'crossSection': 0.00739}, 
#    'wzp6_ee_mumuH_ecm365':  {'fraction':1, 'crossSection': 0.004185},
#    'wzp6_ee_tautauH_ecm365':   {'fraction':1, 'crossSection': 0.004172},
#}

processList = {
    'wzp6_ee_eeH_ecm365': {
        'files': [
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_018107429.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_104473316.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_117039771.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_130128294.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_173768499.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_047118042.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_107849662.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_118636096.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_153113508.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_eeH_ecm365/events_182514790.root"
        ],
        'crossSection': 0.00739
    },
    'wzp6_ee_mumuH_ecm365': {
        'files': [
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_023261681.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_034927544.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_058572739.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_073291643.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_092281869.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_189404834.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_033570460.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_036028207.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_068513877.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_075232335.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_183713990.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm365/events_197337122.root"
        ],
        'crossSection': 0.004185
    },
    'wzp6_ee_tautauH_ecm365': {
        'files': [
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_015660911.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_058437289.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_094523955.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_160031364.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_175873169.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_192276123.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_043999218.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_090181769.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_116046380.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_162671919.root",
            "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_tautauH_ecm365/events_186940475.root"
        ],
        'crossSection': 0.004172
    }
}

prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions_2.h"]

# Define the input dir (optional)
#inputDir = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA"

#Optional: output directory, default is local running directory
outputDir = "./outputs/histmaker_1/recoil_1/"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 2400000  # 2.4 /ab

# Define binning several histograms
bins_p_mu = (2000, 0, 200)  # Bins de 100 MeV
bins_m_ll = (2000, 0, 200)  # Bins de 100 MeV
bins_p_ll = (2000, 0, 200)  # Bins de 100 MeV
bins_recoil = (200000, 0, 200)  # Bins de 1 MeV
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)

# Function to compile custom header files
def compile_headers(includePaths):
    for path in includePaths:
        if os.path.exists(path):
            ROOT.gInterpreter.Declare(f'#include "{path}"')
        else:
            print(f"Archivo {path} no encontrado.")

# Compile custom header files before analysis
compile_headers(includePaths)

# Function to load files
def load_files(process_name):
    if process_name not in processList:
        raise KeyError(f"Process name '{process_name}' not found in processList.")
    chain = ROOT.TChain("events")  
    for file in processList[process_name]['files']:
        # Intenta abrir el archivo con TFile::Open para manejar archivos remotos
        f = ROOT.TFile.Open(f"root://eospublic.cern.ch/{file}")
        if f and not f.IsZombie():  # Verifica si el archivo fue abierto exitosamente
            chain.Add(file)
            f.Close()  # Cierra el archivo después de verificarlo
        else:
            print(f"Error to open de file {file}")
    return chain


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(process_name, *args):
    if not isinstance(process_name, str):
        raise TypeError(f"Expected a string for process_name, got {type(process_name).__name__} instead.")
    chain = load_files(process_name)
    df = ROOT.RDataFrame(chain)

    # Scale for weight by cross-section and luminosity 
    if doScale:
        crossSection = processList[process_name]['crossSection']
        weightScale = crossSection * intLumi
        df = df.Define("weight", f"1.0 * {weightScale}")

    weightsum = df.Sum("weight")
    
    # define some aliases to be used later on
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Alias("Electron0", "Electron#0.index")

    # get all the leptons from the collection
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")

    # select leptons with momentum > 20 GeV
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)")
    
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

    # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
    df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
    df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")
    df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")

    # Filterjets that contain muons or electrons
    df = df.Define("jets_no_leptons", "FCCAnalyses::ZHfunctions::removeJetsWithLeptons(Jets, muons, electrons)")

    # baseline histograms, before any selection cuts (store with _cut0)
    results = []
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))

    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: at least 1 muon with at least one isolated one
    #########
    df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0 || electrons_no >= 1 && electrons_sel_iso.size() > 0")
    df = df.Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    #########
    ### CUT 2: at least 2 opposite-sign (OS) leptons
    #########
    df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")
    df = df.Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))

    #########
    ### CUT 3: Higgs mass window
    #########
    df = df.Define("higgsbuilder_result", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(125, 125, 0.4, 240, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("higgs", "Vec_rp{higgsbuilder_result[0]}") # el Higgs
    df = df.Define("higgs_muons", "Vec_rp{higgsbuilder_result[1],higgsbuilder_result[2]}") # los leptones 
    df = df.Define("higgs_m", "FCCAnalyses::ReconstructedParticle::get_mass(higgs)")
    df = df.Define("higgs_p", "FCCAnalyses::ReconstructedParticle::get_p(higgs)")
    df = df.Define("higgs_recoil_m", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(higgs)")
    
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
    df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(MissingET)")
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss"))  # Plot it before the cut

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
#save_to_output('p8_ee_ZH_Zmumu_ecm240', "output_ZH_Zmumu.root")
