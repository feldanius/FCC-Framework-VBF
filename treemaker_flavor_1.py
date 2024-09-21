import os, copy
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

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Optional: output directory, default is local running directory
outputDir   = "./outputs/treemaker_2/flavor_2/"

## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
)
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
)

jetFlavourHelper = None
jetClusteringHelper = None

class RDFanalysis:

    # __________________________________________________________
    # Mandatory: analysers function to define the analysers to process
    # please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
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
        df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
  
        df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")

        df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")
   
        # CUT 1: at least 1 muon with at least one isolated one
        df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0")
        df = df.Filter("electrons_no >= 1 && electrons_sel_iso.size() > 0")
        
        # CUT 2: at least 2 opposite-sign (OS) leptons
        df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")
        df = df.Filter("electrons_no >= 2 && abs(Sum(electrons_q)) < electrons_q.size()")
        
        df = df.Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons)")
        df = df.Define("ReconstructedParticlesNoElectrons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,electrons)")

        # Perform N=2 jet clustering
        global jetClusteringHelper
        global jetFlavourHelper

        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        collections_nomuons = copy.deepcopy(collections)
        collections_nomuons["PFParticles"] = "ReconstructedParticlesNoMuons"

        jetClusteringHelper = ExclusiveJetClusteringHelper(collections_nomuons["PFParticles"], 2)
        df = jetClusteringHelper.define(df)

        jetFlavourHelper = JetFlavourHelper(collections_nomuons, jetClusteringHelper.jets, jetClusteringHelper.constituents)
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        # Higgs-related definitions
        df = df.Define("higgsbuilder_result_muons", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(125, 240, 0.4, 365, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        df = df.Define("higgsbuilder_result_electrons", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(125, 240, 0.4, 365, false)(electrons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        
        df = df.Define("higgs_mu", "Vec_rp{higgsbuilder_result_muons[0]}")  # the Higgs
        df = df.Define("higgs_el", "Vec_rp{higgsbuilder_result_electrons[0]}")  # the Higgs
        df = df.Define(
            "higgs_muons", "Vec_rp{higgsbuilder_result_muons[1],higgsbuilder_result_muons[2]}"
        ) 
        df = df.Define(
            "higgs_electrons", "Vec_rp{higgsbuilder_result_electrons[1],higgsbuilder_result_electrons[2]}"
        ) 
        
        df = df.Define("higgs_m_mu", "FCCAnalyses::ReconstructedParticle::get_mass(higgs_mu)")
        df = df.Define("higgs_m_el", "FCCAnalyses::ReconstructedParticle::get_mass(higgs_el)")
       
        df = df.Define("higgs_p_mu", "FCCAnalyses::ReconstructedParticle::get_p(higgs_mu)")
        df = df.Define("higgs_p_el", "FCCAnalyses::ReconstructedParticle::get_p(higgs_el)")
       
        df = df.Define("higgs_recoil_mu", "FCCAnalyses::ReconstructedParticle::recoilBuilder(365)(higgs_mu)")
        df = df.Define("higgs_recoil_el", "FCCAnalyses::ReconstructedParticle::recoilBuilder(365)(higgs_el)")
        df = df.Define("higgs_recoil_m_mu", "FCCAnalyses::ReconstructedParticle::get_mass(higgs_recoil_mu)[0]")
        df = df.Define("higgs_recoil_m_el", "FCCAnalyses::ReconstructedParticle::get_mass(higgs_recoil_el)[0]")
        df = df.Define("higgs_recoil_p_mu", "FCCAnalyses::ReconstructedParticle::get_p(higgs_muons)[0]")
        df = df.Define("higgs_recoil_p_el", "FCCAnalyses::ReconstructedParticle::get_p(higgs_electrons)[0]")

        df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(365., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(MissingET)")
        df = df.Define("missing_p", "FCCAnalyses::ReconstructedParticle::get_p(MissingET)")
   
        # CUT 3: Njets = 2
        df = df.Filter("event_njet > 1")

        df = df.Define("jets_p4", "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
        df = df.Define("jj_m", "JetConstituentsUtils::InvariantMass(jets_p4[0], jets_p4[1])")

        return df

    # __________________________________________________________
    # Mandatory: output function
    def output():
        branchList = [
            "higgs_m_mu",
            "higgs_m_el",
            "higgs_p_mu",
            "higgs_p_el",
            "higgs_recoil_m_mu",
            "higgs_recoil_m_el",
            #"higgs_recoil_p_mu",
            #"higgs_recoil_p_el",
            "cosTheta_miss",
            "missing_p",
            "jj_m",
            #"missingEnergy",
        ]

        # Outputs jet properties
        # branchList += jetClusteringHelper.outputBranches()

        # Outputs jet scores and constituent breakdown
        branchList += jetFlavourHelper.outputBranches()

        return branchList

