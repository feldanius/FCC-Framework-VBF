import os, copy
# list of processes (mandatory)
processList = {
#   'wzp6_ee_eeH_ecm365':    {'fraction':1, 'crossSection': 0.00739}, 
#    'wzp6_ee_mumuH_ecm365':  {'fraction':1, 'crossSection': 0.004185},
#    'wzp6_ee_tautauH_ecm365':   {'fraction':1, 'crossSection': 0.004172},
#    'p8_ee_tt_ecm365': {'fraction':1, 'crossSection': 0.8},
#    'p8_ee_WW_ecm365': {'fraction':1, 'crossSection': 10.7165},
    'p8_ee_ZZ_ecm365': {'fraction':1, 'crossSection': 0.6428},
    'wzp6_ee_nunuH_ecm365': {'fraction':1, 'crossSection': 0.05394},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Optional: output directory, default is local running directory

#outputDir   = "./outputs/treemaker_no_cuts/flavor/"

outputDir   = "/eos/user/f/fdmartin/FCC365_jets_no_e_mu"

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
    # Analysers function to define the analysers to process
    def analysers(df):
        # Definir alias para colecciones de partículas
        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon0", "Muon#0.index")
        df = df.Alias("Electron0", "Electron#0.index")
        
        # get all the leptons from the collection
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")

        # Eliminate particles that correspond to muons y electrons
        df = df.Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons_all)")
        df = df.Define("ReconstructedParticlesNoLeptons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons, electrons_all)")

        
        # Clustering de jets usando partículas sin muones ni electrones
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
           # "MCRecoAssociations0": "MCRecoAssociations0",
           # "MCRecoAssociations1": "MCRecoAssociations1",
        }

        collections_noleptons = copy.deepcopy(collections)  
        collections_noleptons["PFParticles"] = "ReconstructedParticlesNoLeptons"

        jetClusteringHelper = ExclusiveJetClusteringHelper(collections_noleptons["PFParticles"], 2)
        df = jetClusteringHelper.define(df)

        
        jetFlavourHelper = JetFlavourHelper(collections_noleptons, jetClusteringHelper.jets, jetClusteringHelper.constituents)
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

      
        
        df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(365., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy)")
        df = df.Define("missing_p", "FCCAnalyses::ReconstructedParticle::get_p(missingEnergy)")

        df = df.Filter("event_njet > 1")
       
        df = df.Define("jets_p4", "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
        df = df.Define("jj_m", "JetConstituentsUtils::InvariantMass(jets_p4[0], jets_p4[1])")
        
        return df

    # __________________________________________________________
    # Output function
    def output():
        branchList = [
            "missingEnergy",
            "cosTheta_miss",
            "missing_p",  # MET
            "jj_m",  # Masa invariante de los jets
        ]

        # Outputs jet scores y propiedades de los jets
        branchList += jetFlavourHelper.outputBranches()

        return branchList
