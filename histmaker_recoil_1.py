import ROOT
import os

# Lista de procesos (obligatoria)
processList = {
    'p8_ee_WW_mumu_ecm240':    {'fraction': 1, 'crossSection': 0.25792}, 
    'p8_ee_ZZ_mumubb_ecm240':  {'fraction': 1, 'crossSection': 2 * 1.35899 * 0.034 * 0.152},
    'p8_ee_ZH_Zmumu_ecm240':   {'fraction': 1, 'crossSection': 0.201868 * 0.034},
}

# Ruta al diccionario de secciones transversales (obligatoria)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Incluye rutas adicionales a los archivos de encabezado personalizados
includePaths = ["functions_1.h"]

# Define el input dir (opcional)
inputDir = "./localSamples/"

# Directorio de salida opcional, por defecto es el directorio local de ejecución
outputDir = "./outputs/histmaker/recoil/"

# Número de CPUs opcional, por defecto es 4, -1 usa todos los núcleos disponibles
nCPUS = -1

# Escala los histogramas con la sección transversal y la luminosidad integrada
doScale = True
intLumi = 5000000  # 5 /ab

# Define la binning para varios histogramas
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

# Función para compilar los archivos de encabezado personalizados
def compile_headers(includePaths):
    for path in includePaths:
        if os.path.exists(path):
            ROOT.gInterpreter.Declare(f'#include "{path}"')
        else:
            print(f"Archivo {path} no encontrado.")

# Compila las cabeceras personalizadas antes de realizar el análisis
compile_headers(includePaths)

# Función build_graph que contiene la lógica de análisis, cortes y histogramas (obligatorio)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    
    # Escala de peso por sección transversal y luminosidad
    if doScale:
        crossSection = processList[dataset]['crossSection']
        weightScale = crossSection * intLumi
        df = df.Define("weight", f"1.0 * {weightScale}")

    weightsum = df.Sum("weight")
    
    # Define algunos alias para usar más adelante
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Alias("Electron0", "Electron#0.index")

    # Obtén todos los leptones de la colección
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")

    # Selecciona leptones con momento > 20 GeV
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

    # Calcula el aislamiento de muones y electrones y guarda los leptones con un corte de aislamiento de 0.25 en una columna separada
    df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
    df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
    df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")
    df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")

    # Filtra jets que contienen muones o electrones
    df = df.Define("jets_no_leptons", "FCCAnalyses::ZHfunctions::removeJetsWithLeptons(Jets, muons, electrons)")

    # Histograma base, antes de cualquier selección de corte (guardar con _cut0)
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))

    #########
    ### CUT 0: todos los eventos
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: al menos 1 muón o electrón con al menos uno aislado
    #########
    df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0 || electrons_no >= 1 && electrons_sel_iso.size() > 0")
    df = df.Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    #########
    ### CUT 2: al menos 2 leptones de signo opuesto (OS)
    #########
    df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")
    df = df.Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))

    # Construye la resonancia de Higgs
    df = df.Define("higgsbuilder_result", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(125, 125, 0.4, 240, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("higgs", "Vec_rp{higgsbuilder_result[0]}") # el Higgs
    df = df.Define("higgs_muons", "Vec_rp{higgsbuilder_result[1],higgsbuilder_result[2]}") # los leptones 
    df = df.Define("higgs_m", "FCCAnalyses::ReconstructedParticle::get_mass(higgs)")
    df = df.Define("higgs_p", "FCCAnalyses::ReconstructedParticle::get_p(higgs)")
    df = df.Define("higgs_recoil_m", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(higgs)")

    # Histogramas después del corte 4
    results.append(df.Histo1D(("higgs_m_cut4", "", *bins_m_ll), "higgs_m"))
    results.append(df.Histo1D(("higgs_p_cut4", "", *bins_p_ll), "higgs_p"))
    results.append(df.Histo1D(("higgs_recoil_m_cut4", "", *bins_recoil), "higgs_recoil_m"))
    results.append(df.Histo1D(("higgs_muons_p_cut4", "", *bins_p_mu), "higgs_muons_p"))

    return results
